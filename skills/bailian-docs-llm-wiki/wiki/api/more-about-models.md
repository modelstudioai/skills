# [more](more.md) about models

阿里云百炼平台提供多种模型调用增强能力，覆盖异步任务管理、临时凭证生成、文件上传、子空间隔离及连接优化等关键场景。本文档面向开发者，系统梳理核心功能、参数、使用方式及限制，帮助您高效、稳定地集成模型服务。

## 支持的模型/功能

百炼支持的模型类型广泛，包括大语言模型（如 `qwen-plus`）、多模态模型（如 `qwen3-vl-plus`）、图像生成（如 `wanx2.1-t2i-turbo`）、视频生成（如 `wanx2.1-kf2v-plus`）及语音识别（如 `paraformer-8k-v2`）等。部分计算密集型模型（如图像生成、视频生成、长文本语音转写）默认采用**异步调用机制**，需通过任务 ID 轮询或事件通知获取结果 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。此外，平台支持在可信后端生成**临时 API Key** 用于前端安全调用，以及为多模态模型上传本地文件获取临时 OSS URL [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 4 中提到“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，无需模型调用授权”，但文档 1 明确指出异步任务接口（如 `/api/v1/tasks/{task_id}`）仅支持查询当前 API Key 所属主账号下的任务，且调优模型仅能由其所在业务空间的 API Key 调用——二者逻辑一致，无矛盾；但需注意“无需授权”仅指平台级权限管控，不豁免业务空间隔离与 API Key 绑定约束。

## 关键参数

- **异步任务状态轮询**：推荐按任务类型设置合理间隔（文本向量可短至秒级，图像/视频建议 5–30 秒），避免触发 20 QPS 限流 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **临时 API Key TTL**：有效期范围为 `[1, 1800]` 秒（默认 60 秒），不可手动删除，到期自动失效 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **文件上传参数**：必须指定 `model_name`，且该值须与后续模型调用的模型严格一致；临时 URL 有效期固定为 48 小时，超时即不可用 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **连接复用配置**：Java SDK 默认启用连接池，关键参数包括 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）；Python SDK 需显式传入 `httpx.Client` 或 `httpx.AsyncClient` 并配置 `limits` [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 使用方式

- **异步任务管理**：优先推荐使用 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)，通过事件总线（EventBridge）订阅 `dashscope:System:AsyncTaskFinish` 事件，避免轮询资源浪费与限流风险；若必须轮询，统一使用 `/api/v1/tasks/{task_id}` 查询单任务或 `/api/v1/tasks` 批量查询。
- **子业务空间调用**：需使用该空间专属 API Key，并按地域选择正确 endpoint（北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`），标准模型还需提前配置调用权限 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。
- **本地文件上传**：调用 `/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略，再直传至 OSS；SDK 用户可直接使用 `client.files.upload(file_path, purpose="inference")`（Python）封装逻辑 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **连接复用**：Java 开发者通过 `Constants.connectionConfigurations` 全局配置；Python 开发者在构造 `dashscope.Client` 或 `dashscope.AsyncClient` 时传入自定义 `http_client` 实例 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 限制和注意事项

- **异步任务生命周期**：任务结果默认保留 24 小时（以各任务文档为准），超时后无法查询；仅 `PENDING` 状态任务可取消 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **临时文件与密钥风险**：临时 URL 和临时 API Key 均**严禁用于生产环境**——前者有效期短、限流严（100 QPS）、不支持扩容；后者权限继承源 Key，泄露即等同于永久 Key 泄露 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)、[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **地域与密钥绑定**：北京、新加坡、弗吉尼亚、中国香港等地域的 API Key **完全独立**，不可混用；子业务空间调用也必须匹配对应地域的 WorkspaceId 与 region 参数 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)、[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **文件模型强绑定**：上传文件时指定的 `model_name` 必须与后续模型请求中的 `model` 字段完全一致，否则调用失败；且文件仅限同一主账号下使用，无法跨账号共享 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


