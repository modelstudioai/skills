# [more](more.md) about models

百炼平台提供多种高级模型调用能力，覆盖异步任务管理、文件上传、连接复用、子空间隔离及安全凭证生成等场景。本文档面向开发者，系统梳理核心功能、关键参数、使用方式及限制条件，帮助您高效、稳定地集成模型服务。

## 支持的模型/功能

百炼支持同步与异步两类模型调用模式：
- **同步模型**：如 `qwen-plus`、`qwen3-vl-plus` 等文本/多模态模型，直接返回结果；
- **异步模型**：如图像生成（`wanx2.1-t2i-turbo`）、视频合成（`wanx2.1-kf2v-plus`）、语音转写（`paraformer-16k-1`）等长耗时任务，需通过任务 ID 轮询或事件通知获取结果。

异步任务统一由 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提供标准化接口（`/api/v1/tasks/{task_id}`），支持查询、批量列表和取消（仅 `PENDING` 状态）。此外，为规避轮询限流与资源浪费，平台支持通过事件总线推送完成通知，详见 [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)。

> **注意**：文档 6 中提到“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但该描述与文档 2 中“异步任务API支持查询当前 API Key 所属阿里云主账号下的所有任务”存在隐含权限冲突——实际调用受业务空间隔离约束，调优模型**仅能被其所在子业务空间的 API Key 调用**，跨空间即使拥有主账号权限亦不可访问。

## 关键参数

| 参数 | 说明 | 典型值/范围 | 来源 |
|------|------|-------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒（默认 60） | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `model_name` | 文件上传时必需，绑定模型上下文 | `qwen3-vl-plus`, `wanx2.1-t2i-turbo` 等 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必须显式声明的请求头 | 固定字符串 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize`（Java） / `max_connections`（Python） | 连接池核心参数，直接影响高并发吞吐 | Java 默认 32；Python 建议设为 100+ | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全调用（前端/不可信环境）
在浏览器或移动 App 中调用模型前，**必须**通过后端服务生成临时 API Key，避免永久密钥泄露。调用 `/api/v1/tokens` 接口，传入主账号的 `DASHSCOPE_API_KEY` 并指定 `expire_in_seconds`，获得 `st-***` 格式令牌。该令牌继承原 Key 的全部权限（含模型/知识库访问限制），且**无法手动删除，到期自动失效**。

### 2. 异步任务处理
- **轮询模式**：调用模型 API 获取 `task_id` 后，以 20 QPS 为上限轮询 `/api/v1/tasks/{task_id}`。建议按任务类型设置间隔（文本向量可 1s，图像生成建议 ≥5s）。
- **事件驱动模式**：配置事件总线规则，监听 `dashscope:System:AsyncTaskFinish` 事件，通过 HTTP 回调或 RocketMQ 消费通知，再单次查询结果。此方式规避限流、节省资源，适合高并发场景。

### 3. 多模态文件输入
调用图像/视频/音频模型前，需先上传本地文件获取 `oss://` 临时 URL：
- 必须指定 `model_name`（如 `qwen3-vl-plus`），且后续调用模型必须一致；
- 上传后 URL 有效期 **48 小时**，超时自动清理；
- 使用该 URL 时，HTTP 请求头**必须包含** `X-DashScope-OssResourceResolve: enable`。

### 4. 子业务空间调用
为实现权限隔离与费用分账，需使用子空间专属 API Key：
- **OpenAI 兼容方式**：北京地域设 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"`；新加坡地域需替换为 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；
- **DashScope 原生方式**：Python SDK 构造 `Client` 时传入 `workspace` 和 `region`（如 `"ap-southeast-1"`）；Java SDK 需显式配置 `Protocol.HTTP` + 自定义 endpoint。

## 限制和注意事项

- **临时文件存储**：单文件 ≤1GB；上传限流为 **100 QPS（按主账号+模型维度）**；**严禁用于生产环境或压测**，生产应使用 OSS 等持久化存储。
- **异步任务保留期**：任务完成后通常保留 **24 小时**（具体以各模型文档为准），超时后数据自动清理，无法查询。
- **连接复用配置**：Java SDK 默认启用连接池，但 `connectionPoolSize` 过低（<50）易导致高并发下请求阻塞；Python SDK 需显式传入 `httpx.Client` 或 `httpx.AsyncClient`，否则每次调用新建连接。
- **地域与 API Key 绑定**：北京、新加坡、弗吉尼亚、中国香港四地 API Key **完全独立**，不可混用；调用时 endpoint 必须与 Key 所属地域匹配。
- **临时 API Key 权限继承**：其权限范围严格等于生成它的永久 API Key，包括对特定模型或知识库的访问控制策略。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)


