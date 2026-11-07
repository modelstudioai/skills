# [more](more.md) about models

本文档面向开发者，汇总百炼平台模型服务的关键技术细节，涵盖模型调用的扩展能力、核心参数配置、接入方式及重要约束。内容聚焦于生产环境可用的机制，包括异步任务管理、子业务空间隔离、临时凭证与文件上传、连接复用等高频场景，不包含营销性描述。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen3-vl-plus`）适用于低延迟文本生成、多模态推理等场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频合成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）需通过任务 ID 轮询或事件通知获取结果，详见[异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  

所有模型均支持在**默认业务空间**和**子业务空间**中调用。子业务空间可用于权限隔离（如限制 RAM 用户仅能调用特定模型）或费用分账，但调用标准模型前需显式配置模型调用权限；而调优后部署的模型则无需额外授权，仅限其所在空间的 API Key 调用 [子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  

多模态模型（VL、OCR、ASR 等）依赖外部文件输入，平台提供免费临时存储服务，上传后返回 `oss://` 格式 URL（有效期 48 小时），调用时必须在请求头中添加 `X-DashScope-OssResourceResolve: enable` [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 5 明确指出“临时 URL 请勿用于生产环境”，而文档 3 中子业务空间调用示例未提及该限制，实际生产部署应统一使用 OSS 等长期存储方案。

## 关键参数

| 参数 | 说明 | 取值范围/默认值 | 注意事项 |
|------|------|------------------|----------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | 由[生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)接口指定，不可手动删除 |
| `task_id` | 异步任务唯一标识 | UUID 字符串 | 用于查询、批量列表、取消任务，仅 `PENDING` 状态可取消 |
| `page_size` / `page_no` | 批量查询任务分页参数 | `page_size` 默认 10，最大 100 | 适用于 `/api/v1/tasks` 接口，支持按 `start_time`/`end_time`/`status`/`model_name` 过滤 |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，建议高并发时设为 256 | 需与 `maximumAsyncRequests` 协调配置，避免阻塞 [DashScope SDK连接复用配置](raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `max_connections` | Python SDK `httpx.AsyncClient` 总连接数 | 默认无限制 | 高并发场景下建议显式设置，如 `max_connections=100` |

## 使用方式

### 1. 调用入口
- **DashScope 原生协议**：需指定 `workspace` 和 `region`（如 `ap-southeast-1`），适用于子业务空间调用；  
- **OpenAI 兼容模式**：使用通用域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`，但**仅支持标准模型**，不支持调优模型 [子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  

### 2. 异步任务结果获取
- **轮询模式**：调用 `GET /api/v1/tasks/{task_id}`，QPS 限流 20；建议按任务类型设置合理间隔（文本向量可短，图像/视频宜长）；  
- **事件驱动模式**：通过事件总线配置 HTTP 回调或 RocketMQ，接收 `dashscope:System:AsyncTaskFinish` 事件，再单次查询结果，规避限流 [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)。  

### 3. 文件上传与引用
- 先调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；  
- 再将文件 POST 至策略中的 `upload_host`；  
- 最终获得 `oss://` URL，在模型请求中作为输入字段传入，并**必须携带请求头 `X-DashScope-OssResourceResolve: enable`**。  

### 4. 连接复用
- **Java**：通过 `Constants.connectionConfigurations` 全局配置超时与连接池参数；  
- **Python**：构造 `Client` 或 `AsyncClient` 时传入自定义 `httpx.Client` / `httpx.AsyncClient` 实例，推荐使用 `with` 语句管理生命周期。  

## 限制和注意事项

- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港四地 API Key **完全独立**，不可混用；Endpoint 域名需匹配对应地域（如 `ap-southeast-1.maas.aliyuncs.com`）；  
- **临时资源时效性**：临时 API Key 最长 1800 秒，临时文件 URL 严格 48 小时，超时后不可恢复；  
- **限流策略**：  
  - 文件上传凭证接口：100 QPS（按主账号+模型维度）；  
  - 异步任务查询接口：20 QPS（按主账号维度）；  
  - 临时 API Key 生成无单独限流，但受上游 API Key 配额约束；  
- **安全约束**：  
  - 临时 API Key 继承生成者 API Key 的全部权限（含知识库访问），不可降权；  
  - 上传文件与调用模型的 API Key 必须属于同一阿里云主账号；  
- **生产警示**：  
  > **注意**：文档 5 多次强调“临时 URL 请勿用于生产环境”“文件上传凭证接口限流为 100 QPS 且不支持扩容”，而文档 3 的子业务空间示例未体现此风险。生产系统必须使用 OSS 等自有存储，并自行管理鉴权与生命周期。  
  > **注意**：文档 2 指出异步任务数据保留 24 小时（“具体以对应任务的 API 文档为准”），但文档 4 的事件总线示例中未明确事件留存策略，开发者应以任务查询接口的实际可用性为准，不可依赖事件持久化。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


