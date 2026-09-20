# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的关键扩展能力，涵盖异步任务管理、子业务空间隔离、临时凭证与文件上传、连接复用等核心机制。这些能力不改变基础模型接口语义，但显著提升生产环境下的安全性、可观测性与资源效率。

## 支持的模型/功能

百炼平台支持两类主要模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、多模态理解等毫秒级响应场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）：适用于耗时较长（秒级至分钟级）的任务，需通过任务 ID 轮询或事件通知获取结果。  

异步任务统一由 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提供标准化生命周期管理（查询、批量列表、取消），且所有异步任务均接入事件总线，支持通过 HTTP 回调或 RocketMQ 主动接收完成通知，避免轮询限流风险。  
> **注意**：文档 4 中明确指出“任务完成事件”在成功或失败时均会上报，但文档 2 的响应示例中 `output.results` 字段在部分子任务失败时仍返回混合结果（含成功 URL 和失败 error object），实际开发需健壮解析 `task_metrics` 统计字段而非仅依赖 `results` 数组长度。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串，由创建任务接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时绑定的模型名 | 必须与后续模型调用的 `model` 参数完全一致，否则调用失败 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` 临时 URL 时必需的请求头 | 固定值，缺失将导致 400 错误 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

## 使用方式

### 1. 子业务空间调用
为实现权限隔离与费用分账，需使用子业务空间专属 API Key，并按地域配置正确 Base URL：  
- **DashScope SDK**：北京地域无需额外配置；新加坡地域需显式设置 `base_url = 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1'`；  
- **OpenAI 兼容模式**：北京地域使用 `https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡地域使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`。  
> **注意**：文档 3 明确要求调用标准模型前需在子空间中[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)，但该操作在控制台路径与文档描述存在偏差（文档指向旧版权限页），实际应通过「业务空间 → 模型权限」配置。

### 2. 异步任务结果获取
- **轮询方式**：调用 `/api/v1/tasks/{task_id}`，建议按任务类型设置合理间隔（文本向量可 1s，图像生成建议 ≥5s），避免触发 20 QPS 限流；  
- **事件驱动方式**：配置事件总线规则，监听 `dashscope:System:AsyncTaskFinish` 事件，从 `data.task_id` 提取 ID 后单次查询结果，彻底规避轮询开销。详情见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 3. 本地文件上传
调用多模态模型前，需先上传文件获取 `oss://` 临时 URL：  
- 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；  
- 使用策略参数直传 OSS；  
- **关键约束**：上传与调用必须使用同一主账号的 API Key，且 `model_name` 参数必须严格匹配。

### 4. 连接复用优化
高并发场景下必须启用连接复用：  
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize=256`）；  
- **Python SDK**：同步调用传入 `requests.Session()`，[异步调用](../concepts/asynchronous-invocation.md)传入 `aiohttp.ClientSession(connector=TCPConnector(...))`。

## 限制和注意事项

- **临时凭证安全**：临时 API Key 继承生成者 API Key 的全部权限，且无法手动删除，仅能等待自动过期（[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)）；  
- **文件时效性**：`oss://` 临时 URL 有效期固定为 48 小时，超时后不可恢复，**严禁用于生产环境长期服务**，生产环境应使用阿里云 OSS 自建存储；  
- **地域一致性**：API Key、业务空间、Base URL、事件总线地域必须严格匹配（如新加坡地域的 API Key 不能用于北京地域的 `dashscope.aliyuncs.com` 域名）；  
- **限流阈值**：文件上传凭证接口限流为 100 QPS（按主账号+模型维度），异步任务查询接口限流为 20 QPS（按主账号维度），超限将直接返回 `Throttling.RateQuota` 错误；  
- **模型授权差异**：在子业务空间中调用百炼官方标准模型需单独授权，但调优后部署的私有模型**无需额外授权**，仅限本空间 API Key 调用（[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)）。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


