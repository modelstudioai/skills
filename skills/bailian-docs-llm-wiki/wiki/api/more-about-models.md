# [more](more.md) about models

百炼平台提供多种高级模型调用能力，覆盖异步任务管理、跨业务空间调用、临时凭证与文件上传、连接复用优化等关键场景。本文档面向开发者，系统梳理核心功能、参数约束、使用方式及实践限制，帮助构建稳定、高效、安全的模型服务集成。

## 支持的模型/功能

百炼支持同步与异步两类模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen3-vl-plus`）适用于低延迟文本生成、多模态推理等场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）需通过任务 ID 轮询或事件通知获取结果，详见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  

此外，平台支持子业务空间隔离调用、临时 API Key 生成、本地文件上传获取临时 OSS URL 等扩展能力，满足权限管控、费用分账、多模态输入等生产需求。

> **注意**：文档中提及的“标准模型”（如 `qwen-plus`）与“调优后部署的模型”在权限模型上存在差异——前者需显式配置模型调用权限，后者仅限所属业务空间的 API Key 调用且无需额外授权，详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

## 关键参数

| 参数 | 说明 | 取值范围 | 备注 |
|------|------|----------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒 | 默认 60 秒；超时后自动失效，不可手动删除，见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串 | 用于查询、取消任务；仅 `PENDING` 状态可取消 |
| `model_name` | 文件上传时绑定的模型名 | 与后续调用模型严格一致 | 上传凭证接口按 `主账号+model_name` 维度限流 100 QPS，见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定字符串 | 缺失将导致模型调用失败 |

## 使用方式

### 异步任务处理
推荐优先采用**事件总线回调**而非轮询：配置 HTTP 回调 URL 或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，避免触发 20 QPS 查询限流，并提升实时性。轮询仅建议用于低并发调试场景，且需合理设置间隔（如图像生成任务建议 ≥5s）。详情参见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 子业务空间调用
必须使用该空间专属的 API Key，并根据地域选择对应 endpoint：
- 北京地域：`https://dashscope.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容）或 `https://dashscope.aliyuncs.com/api/v1/...`（DashScope 原生）；
- 新加坡地域：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`，需显式传入 `workspace` 和 `region` 参数。

### 连接复用优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池（如 `connectionPoolSize=256`、`maximumAsyncRequests=256`），避免高并发下连接耗尽；  
- **Python SDK**：传入自定义 `httpx.Client` 或 `httpx.AsyncClient`，设置 `limits=httpx.Limits(max_connections=100)` 实现复用。同步调用推荐 `with httpx.Client() as client:` 确保资源释放。

## 限制和注意事项

- **临时文件 URL**：有效期严格为 **48 小时**，过期后无法访问；文件与模型强绑定，且仅限同一主账号下使用；**禁止用于生产环境或压测**，生产应使用阿里云 OSS 等持久化存储。
- **临时 API Key**：继承生成者 API Key 的全部权限（含知识库访问限制），且各地域 API Key 不互通；`WorkspaceId` 必须与实际业务空间匹配。
- **异步任务生命周期**：成功任务默认保留 **24 小时**，超时后自动清理，期间可通过 `task_id` 查询；`PENDING` 状态任务可取消，`RUNNING` 或已完成状态不可取消。
- **地域一致性**：API Key、`WorkspaceId`、Endpoint 地域（如 `cn-beijing`、`ap-southeast-1`）三者必须严格一致，否则返回 `InvalidApiKey` 等错误。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


