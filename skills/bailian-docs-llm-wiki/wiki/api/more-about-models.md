# [more](more.md) about models

本文档面向开发者，汇总百炼平台中与模型调用深度相关的进阶能力，包括[异步任务](../concepts/asynchronous-task.md)管理、子业务空间隔离、临时文件上传、连接复用优化及安全凭证生成等核心机制。这些功能不改变基础模型接口语义，但显著影响高并发、多租户、多模态和生产环境下的集成方式与稳定性。

## 支持的模型/功能

百炼平台支持多种模型调用模式，具体能力因模型类型而异：

- **异步模型**：图像生成（如 `wanx2.1-t2i-turbo`）、视频生成（如 `wanx2.1-kf2v-plus`）、语音转写（如 `paraformer-16k-1`）等长耗时任务必须通过[异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)完成，即先提交任务获取 `task_id`，再轮询或订阅事件获取结果。
- **多模态模型**：调用 `qwen3-vl-plus` 等视觉语言模型时，需先将本地图片/视频上传至百炼临时存储，获取 `oss://` 开头的临时 URL；该 URL 与模型强绑定，且**必须在请求头中显式添加 `X-DashScope-OssResourceResolve: enable`** 才能被正确解析 [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **子业务空间模型**：标准模型（如 `qwen-plus`）可在子业务空间中独立授权调用，实现权限隔离与费用分账；而调优后部署的私有模型仅限其所属子空间调用，且**不支持 OpenAI 兼容方式**，仅可通过 DashScope SDK 或原生 HTTP 接口访问 [子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 中“OpenAI 兼容方式调用子空间模型”的示例使用了通用域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`，但该地址**仅适用于北京地域默认业务空间**；子空间调用必须使用工作空间专属域名（如 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`），否则将返回鉴权失败。请严格按 [子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 中“新加坡地域”章节配置 `base_url`。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `contain_result` | [异步任务](../concepts/asynchronous-task.md)完成事件是否内嵌结果 | `true` / `false`；设为 `true` 可减少一次查询调用 | [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md) |
| `model_name` | 上传文件时必需指定的模型名 | 必须与后续模型调用的 `model` 字段完全一致（如 `qwen3-vl-plus`） | [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，高并发场景建议设为 256 | [DashScope SDK连接复用配置](raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器、移动 App 等前端环境调用模型时，**禁止硬编码永久 API Key**。应由后端服务调用 `/api/v1/tokens` 接口生成临时 Key，并设置合理 TTL（如 `expire_in_seconds=1800`），确保凭证最小权限与最短生命周期 [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. 高效异步处理
- **轮询方案**：对单个任务，使用 `GET /api/v1/tasks/{task_id}` 查询状态；避免高频轮询（限流 20 QPS），建议按任务类型动态调整间隔（文本向量可 1s，图像生成建议 ≥5s）。
- **事件驱动方案**：配置事件总线（EventBridge）监听 `dashscope:System:AsyncTaskFinish` 事件，目标设为 HTTP 回调或 RocketMQ；收到事件后解析 `data.task_id` 并调用一次结果接口，彻底规避轮询开销 [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)。

### 3. 多模态文件准备
调用多模态模型前，必须上传文件：
- 使用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；
- 按策略向 OSS 直传文件，获得 `oss://...` URL；
- 在模型请求中传入该 URL，并**在 Header 中添加 `X-DashScope-OssResourceResolve: enable`**。

### 4. 连接性能优化
- **Python**：复用 `httpx.Client` 或 `httpx.AsyncClient` 实例，配置 `limits` 参数控制连接池大小与保活策略。
- **Java**：通过 `Constants.connectionConfigurations` 全局配置连接池参数（如 `connectionPoolSize=256`），避免每次请求新建连接。

## 限制和注意事项

- **临时文件存储**：`oss://` URL 有效期固定为 48 小时，过期后无法使用；且文件与主账号、模型强绑定，**不可跨账号、跨模型共享**；生产环境务必使用阿里云 OSS 自行托管 [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **临时 API Key**：继承生成者 API Key 的全部权限（含知识库访问），且**无法手动删除**，仅能等待自动过期 [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **[异步任务](../concepts/asynchronous-task.md)保留期**：任务完成后数据默认保留 24 小时（部分模型可能更短），超时后 `GET /api/v1/tasks/{task_id}` 将返回 `UNKNOWN` 状态，需及时保存关键结果。
- **限流策略**：
  - 文件上传凭证接口：100 QPS（按主账号+模型维度）；
  - 异步任务查询接口：20 QPS（按主账号维度）；
  - 所有限流均不支持扩容，高并发场景必须采用事件驱动或连接复用方案缓解。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


