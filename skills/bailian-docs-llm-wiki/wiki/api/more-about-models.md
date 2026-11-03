# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的关键能力与工程实践要点，涵盖模型访问控制、异步任务管理、文件处理、多业务空间隔离及连接优化等核心场景。所有内容均基于当前稳定 API 行为整理，不包含营销性描述。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**：如 `qwen-plus`、`qwen3-vl-plus` 等文本/[多模态](../concepts/multi-modal.md)大模型，适用于低延迟、确定性响应场景；
- **异步模型**：明确标注为异步的模型（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-8k-v2` 等），需通过任务 ID 轮询或事件通知获取结果。详情见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

此外，平台提供以下关键辅助功能：
- 临时 API Key 生成，用于浏览器/移动端等不可信环境的安全调用；
- 本地文件上传并获取 `oss://` 前缀临时 URL，供[多模态](../concepts/multi-modal.md)模型输入使用；
- 子业务空间（Sub-workspace）模型调用隔离，支持权限管控与费用分账；
- 事件总线（EventBridge）回调通知，替代轮询以降低限流风险。

> **注意**：文档中提及的 `dashscope:System:AsyncTaskFinish` 事件类型在 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md) 中定义，但该事件的 `data.contain_result` 字段行为存在不一致——部分示例显示其为 `false`（需额外查询），而另一处说明称当为 `true` 时 `data.output_result` 包含完整结果。实际开发中应始终以查询 `/api/v1/tasks/{task_id}` 接口为准，不可依赖事件体是否携带结果。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串，由创建任务接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时必需的模型绑定标识 | 必须与后续调用模型完全一致（如 `qwen3-vl-plus`） | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定字符串，缺失将导致模型调用失败 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` / `max_connections` | SDK 连接池大小 | Java 默认 32，Python `httpx` 无默认限制；高并发建议设为 100–256 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 调用子业务空间模型
必须使用该子空间专属的 API Key，并显式指定地域与 WorkspaceId（或使用通用域名）：
- **DashScope SDK**：构造 `Client` 时传入 `workspace` 和 `region`（如 `"ap-southeast-1"`）；
- **OpenAI 兼容模式**：设置 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡）。

### 2. 处理异步任务
推荐优先采用 **事件总线回调** 方式（HTTP 或 RocketMQ），避免轮询触发 20 QPS 限流。若必须轮询，请按任务类型设置合理间隔（文本类可 1–2s，图像/视频类建议 ≥5s）。查询接口统一为 `GET /api/v1/tasks/{task_id}`。

### 3. 上传本地文件
- 调用 `POST /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；
- 使用策略参数直传至 OSS（非百炼后端）；
- 得到 `oss://...` URL 后，在模型请求中作为输入字段传入，并**必须添加请求头 `X-DashScope-OssResourceResolve: enable`**。

### 4. 启用连接复用
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数；
- **Python SDK**：创建 `httpx.Client` 或 `httpx.AsyncClient` 实例并传入 `dashscope.Client` 构造函数，复用底层 TCP 连接。

## 限制和注意事项

- **临时文件**：`oss://` URL 有效期严格为 **48 小时**，过期即失效；单文件上限 **1GB**；上传限流 **100 QPS（按主账号+模型维度）**；生产环境禁止使用，应迁移到 OSS 自有存储。
- **临时 API Key**：继承父 Key 全部权限，**无法提前撤销**，仅靠 TTL 自动过期；各地域 API Key 不互通。
- **异步任务数据保留**：任务完成后通常保留 **24 小时**，超时后自动清理，`/api/v1/tasks` 查询将返回 `UNKNOWN`。
- **子业务空间权限**：调用标准模型（如 `qwen-plus`）需**单独授权**；调优部署模型则仅限本空间 API Key 调用，且不支持 OpenAI 兼容模式。
- **连接复用配置**：Java SDK 的 `maximumAsyncRequests` 必须 ≤ `connectionPoolSize`，否则可能阻塞；Python 中 `httpx.Client` 应复用而非每次新建，避免资源泄漏。

> **注意**：[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 文档强调“文件与模型绑定”，但 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 未说明上传时是否需使用子空间 API Key。根据权限一致性原则，**上传操作必须使用与模型调用相同的主账号下、同一子业务空间的 API Key**，否则将因权限校验失败而拒绝上传。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


