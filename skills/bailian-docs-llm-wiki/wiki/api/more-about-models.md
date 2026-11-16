# [more](more.md) about models

百炼平台提供多种高级模型调用能力，覆盖异步任务管理、文件上传、连接复用、子业务空间隔离及安全凭证分发等场景。本文档面向开发者，系统梳理核心功能、关键参数、使用方式及限制条件，帮助您构建稳定、高效、可扩展的模型服务集成方案。

## 支持的模型/功能

百炼支持同步与异步两类模型调用模式：
- **同步模型**：如 `qwen-plus`、`qwen3-vl-plus` 等文本/多模态基础模型，适用于低延迟、确定性响应场景。
- **异步模型**：如图像生成（`wanx2.1-t2i-turbo`）、视频生成（`wanx2.1-kf2v-plus`）、语音转写（`paraformer-16k-1`）等长耗时任务，必须通过异步任务 API 管理生命周期 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **子业务空间专属模型**：在子业务空间中调优并部署的模型（如微调后的 `qwen-plus-finetuned`），仅限该空间 API Key 调用，且不支持 OpenAI 兼容方式 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 6 中“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”与文档 2 中“异步任务API支持查询当前 API Key 所属阿里云主账号下的所有任务（包括该主账号下通过任意 API Key 提交的任务）”存在隐含冲突——子空间模型实际**不可被主账号其他 API Key 查询或取消**，其任务隔离由 `workspace_id` 和 `region` 强约束，非权限配置层面实现。开发时应以 `workspace_id` 为路由依据，而非依赖跨空间任务可见性。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `model_name` | 文件上传时必需绑定的模型名，决定存储策略与访问权限 | `qwen3-vl-plus`, `wanx2.1-t2i-turbo` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `workspace_id` & `region` | 子业务空间调用必需参数，用于路由到专属服务端点 | `ap-southeast-1`, `cn-beijing`；`{WorkspaceId}` 为实际 UUID | [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) |
| `connectionPoolSize` / `max_connections` | Java/Python SDK 连接池核心参数，直接影响高并发吞吐 | Java 默认 32，建议按 QPS × 平均 RT 调整；Python `httpx.Limits` 推荐 `max_connections=100` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全调用（前端/不可信环境）
在浏览器或移动 App 中，**禁止硬编码永久 API Key**。应通过后端服务调用 `/api/v1/tokens` 接口生成临时 Key，并设置 `expire_in_seconds=1800`（30 分钟）平衡安全性与用户体验 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. 大文件输入
调用多模态模型前，需先上传本地文件获取 `oss://` URL：
- 必须指定 `model_name` 且与后续模型调用一致；
- 请求头需显式添加 `X-DashScope-OssResourceResolve: enable`；
- 生产环境**严禁使用此接口**，应迁移到 OSS 自有 Bucket [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

### 3. 高并发优化
- **Java SDK**：全局配置 `Constants.connectionConfigurations`，重点调整 `connectionPoolSize` 和 `maximumAsyncRequests`；
- **Python SDK**：使用 `httpx.Client` 或 `httpx.AsyncClient` 封装 `dashscope.Client`，避免每次请求重建连接 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

### 4. 异步任务结果获取
避免轮询（受限于 20 QPS）：
- **推荐方案**：配置事件总线 HTTP 回调或 RocketMQ，监听 `dashscope:System:AsyncTaskFinish` 事件，收到后仅一次 `GET /api/v1/tasks/{task_id}` 即可 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)；
- **备选方案**：若必须轮询，按任务类型设置合理间隔（文本向量：1–2s；图像生成：5–10s）。

## 限制和注意事项

- **临时文件**：`oss://` URL 有效期严格为 **48 小时**，超时后无法访问，且不支持续期或查询已上传文件列表。
- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港四地 API Key **完全独立**，不可混用；子业务空间 Endpoint（如 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`）必须匹配对应地域 API Key。
- **限流策略**：
  - 文件上传凭证接口：**100 QPS（主账号+模型维度）**，超出直接失败，不支持扩容；
  - 异步任务查询/取消接口：**20 QPS（主账号维度）**，包含所有子账号；
  - 临时 API Key 生成接口：未明文声明限流，但受后端配额管控，高频调用可能触发熔断。
- **生产环境禁用项**：
  - 临时文件上传（文档 4 明确警示“请勿用于生产环境、高并发及压测场景”）；
  - 临时 API Key（默认 60 秒 TTL 过短，30 分钟仍不满足多数会话周期，应结合业务会话管理设计刷新逻辑）；
  - 无连接复用的高频同步调用（易触发 TCP 连接耗尽或 TIME_WAIT 拥塞）。

> **注意**：文档 4 中“文件上传凭证接口限流为 100 QPS 且不支持扩容”与文档 2 中“异步任务查询接口限流 20 QPS”属于不同维度限流，但二者共用同一主账号配额池。当业务同时大量上传文件并轮询任务状态时，可能因账号级总 QPS 超限导致任一接口失败，需统一协调限流策略。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)


