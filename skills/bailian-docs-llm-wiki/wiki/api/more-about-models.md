# [more](more.md) about models

百炼平台提供多种高级模型调用能力，覆盖异步任务管理、跨业务空间调用、临时凭证安全分发、多模态文件处理及连接性能优化等场景。本文档面向开发者，系统梳理核心功能、关键参数、使用方式及限制条件，帮助构建稳定、高效、安全的模型服务集成。

## 支持的模型/功能

百炼支持标准大语言模型（如 `qwen-plus`、`qwen3-vl-plus`）、多模态模型、图像/视频生成模型（如 `wanx2.1-t2i-turbo`、`wanx2.1-kf2v-plus`）以及语音识别模型（如 `paraformer-8k-v2`）。关键扩展功能包括：

- **异步任务机制**：适用于图像生成、视频合成、长文本语音转写等耗时操作，需通过任务 ID 分两步完成（创建 + 查询），详见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **事件驱动通知**：为避免轮询限流与资源浪费，支持通过 HTTP 回调或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，实现任务完成后的实时响应，详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **子业务空间隔离调用**：支持在非默认业务空间中调用模型，用于权限管控与费用分账，调用时必须使用该子空间专属 API Key，并按地域配置对应 `base_url` 或 `workspace` 参数，详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 中明确指出“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但文档 2 的异步任务示例中却包含 `wanx2.1-kf2v-plus`（属调优后模型）的 `model_name` 查询字段。这表明调优模型虽免授权，但仍完全兼容异步任务管理接口——二者无矛盾，仅需注意调优模型**仅能由其所在业务空间的 API Key 调用**，不可跨空间访问。

## 关键参数

| 参数 | 说明 | 典型值/范围 | 来源 |
|------|------|-------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒（默认 60） | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识符 | UUID 格式字符串（如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1`） | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时绑定的模型名，决定 URL 可用性 | 必须与后续模型调用一致（如 `qwen3-vl-plus`） | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 `32`，高并发建议设为 `256` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

- **临时凭证安全分发**：在浏览器或移动 App 等不可信环境调用模型前，后端应调用 `/api/v1/tokens` 接口生成 `st-****` 格式临时 Token，其权限继承自生成它的永久 API Key，且不可手动删除，到期自动失效。
- **异步任务全流程**：  
  1. 提交任务（如 `client.images.jobs.create()`）→ 获取 `task_id`；  
  2. 轮询查询（`client.images.jobs.fetch(task_id)`）或配置事件总线监听 `dashscope:System:AsyncTaskFinish`；  
  3. 查询成功后，从 `output.results` 或 `output.text` 中提取结果。  
  > 注意：轮询频率需严格控制在 **20 QPS** 内，否则触发限流；推荐优先采用事件通知方案。
- **多模态文件上传**：调用 `/api/v1/uploads?action=getPolicy&model={model_name}` 获取 OSS 上传策略，再将文件 POST 至 `upload_host`，最终获得 `oss://...` 格式临时 URL；**模型调用时必须在 Header 中添加 `X-DashScope-OssResourceResolve: enable`**。
- **连接复用优化**：  
  - Java：通过 `Constants.connectionConfigurations` 配置 `connectionPoolSize`、`maximumAsyncRequests` 等；  
  - Python：传入自定义 `httpx.Client` 或 `httpx.AsyncClient` 实例，设置 `limits` 控制连接数与保活行为。

## 限制和注意事项

- **临时文件存储**：上传文件大小 ≤ 1 GB，有效期严格为 **48 小时**，且与模型强绑定、与主账号强绑定；**禁止用于生产环境**，生产环境请使用阿里云 OSS [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **地域与 API Key 绑定**：北京、新加坡、弗吉尼亚、中国香港四地 API Key **完全独立**，不可混用；调用子业务空间模型时，`workspace` 和 `region` 必须匹配（如新加坡地域 `region="ap-southeast-1"`）。
- **异步任务数据保留**：任务完成后数据默认保留 **24 小时**（具体以各模型文档为准），超时后自动清理，无法恢复。
- **限流策略**：  
  - 文件上传凭证接口：**100 QPS**（按主账号+模型维度）；  
  - 异步任务查询接口（`/api/v1/tasks/{task_id}` 和 `/api/v1/tasks`）：**20 QPS**（按主账号维度）；  
  - 所有限流均不支持扩容，高频场景务必通过事件通知或连接复用规避。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


