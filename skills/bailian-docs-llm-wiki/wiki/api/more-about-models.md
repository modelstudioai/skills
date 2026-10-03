# [more](more.md) about models

阿里云百炼平台提供多种模型调用方式与配套能力，涵盖异步任务管理、临时凭证生成、文件上传、子空间隔离及连接复用等核心功能。本文面向开发者，系统梳理模型调用中关键的扩展能力、参数配置、使用约束及最佳实践，帮助构建稳定、高效、安全的生产级集成。

## 支持的模型/功能

百炼支持的模型按调用模式可分为同步与异步两类：
- **同步模型**：如 `qwen-plus`、`qwen-vl-plus` 等文本与多模态大模型，通过标准 HTTP 请求（如 `/api/v1/services/aigc/text-generation/generation`）即时返回结果；
- **异步模型**：如图像生成（`wanx2.1-t2i-turbo`）、视频生成（`wanx2.1-kf2v-plus`）、语音转写（`paraformer-16k-1`）等耗时较长的任务，必须通过[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提交并轮询或监听事件获取结果。

> **注意**：文档 4 中提到“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”，但该描述与权限模型实际行为存在偏差——调优模型虽不依赖全局模型权限开关，但仍需其所在子业务空间已开通对应模型服务，且 API Key 必须属于该空间。此为权限粒度差异，非功能缺失。

此外，平台提供以下关键辅助功能：
- 通过 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 实现前端/不可信环境的安全调用；
- 通过 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 支持多模态输入（如图片、视频），URL 有效期 48 小时；
- 通过 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 实现模型权限隔离与费用分账；
- 通过 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) 优化高并发场景下的网络资源消耗。

## 关键参数

| 参数 | 作用 | 典型值/范围 | 注意事项 |
|------|------|-------------|----------|
| `task_id` | 异步任务唯一标识 | UUID 格式字符串（如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1`） | 所有异步任务操作（查询、取消、批量列表）均以此为关键索引；[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 明确要求其为必填路径参数。 |
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒（默认 60 秒） | 超出范围将返回 `InvalidParameter` 错误；过短易导致客户端未完成调用即失效，过长则增加泄露风险。 |
| `model_name` | 文件上传绑定模型名 | 如 `qwen-vl-plus`, `wanx2.1-t2i-turbo` | 上传时指定的 `model_name` 必须与后续模型调用的 `model` 参数**完全一致**；跨模型复用 URL 将导致调用失败。 |
| `connectionPoolSize`（Java） / `limit`（Python aiohttp） | SDK 连接池大小 | Java 默认 32，Python 默认 100 | 高并发下需调优：过小引发阻塞，过大可能触发服务端限流；[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) 提供详细参数说明。 |

## 使用方式

### 异步任务处理
推荐两种模式：
- **轮询模式**：调用 `POST /api/v1/tasks` 创建任务后，使用 `GET /api/v1/tasks/{task_id}` 查询状态。建议按任务类型设置合理间隔（文本向量可 100ms，图像生成建议 ≥1s），避免触达 20 QPS 限流。
- **事件驱动模式**：配置[事件总线 EventBridge](../../raw/model-api-reference/more-about-models/async-task-api.md)，监听 `dashscope:System:AsyncTaskFinish` 事件，收到通知后再单次查询结果。此方式规避轮询开销与限流，适合高并发、实时性要求高的场景。

### 子空间调用
必须满足三要素：
1. 使用**子业务空间专属的 API Key**（非默认空间 Key）；
2. 若调用标准模型（如 `qwen-plus`），需在该子空间内[显式授权](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)；
3. 正确配置请求地址：
   - DashScope 方式：`base_url = https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1`；
   - OpenAI 兼容方式：`base_url = https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。

### 文件上传与引用
1. 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；
2. 使用策略参数直传至 OSS（非百炼后端中转）；
3. 得到 `oss://...` URL 后，在模型请求中：
   - 将其作为 `input` 字段值（如 `"image": "oss://..."`）；
   - **必须**在 HTTP Header 中添加 `X-DashScope-OssResourceResolve: enable`，否则服务端无法解析该 URL。

## 限制和注意事项

- **异步任务生命周期**：任务完成后保留 **24 小时**（以各任务 API 文档为准），超时后自动清理，`fetch` 接口将返回 `UNKNOWN` 状态。[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 明确指出此时限。
- **临时文件存储**：`oss://` URL 有效期严格为 **48 小时**，且**禁止用于生产环境**。文档 6 多次强调：“请勿用于生产环境、高并发及压测场景”，并明确建议生产环境使用阿里云 OSS 自建存储。
- **临时 API Key 限制**：仅继承源 API Key 的全部权限，**无法降权**；且不支持手动删除，到期自动失效。
- **连接复用配置**：Java SDK 的 `maximumAsyncRequestsPerHost` 必须 ≤ `connectionPoolSize`，否则可能导致请求阻塞；Python 同步 `requests.Session` 需显式 `close()` 或使用 `with` 语句确保资源释放。
- **地域与 Endpoint 绑定**：所有 API（包括异步任务、临时 Key、文件上传）均需匹配地域。例如北京地域使用 `dashscope.aliyuncs.com`，新加坡地域必须使用 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，混用将导致 `403 Forbidden` 或 `404 Not Found`。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)


