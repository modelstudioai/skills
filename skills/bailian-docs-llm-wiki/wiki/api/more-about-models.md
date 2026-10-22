# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型调用的进阶能力与关键配置要点，涵盖[异步任务](../concepts/asynchronous-task.md)管理、子空间隔离、临时凭证、文件上传、连接复用等核心机制。所有功能均需配合有效的 API Key 使用，且多数能力受地域、权限和配额约束。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen3`）适用于低延迟文本生成场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-8k-v2`）需通过任务 ID 轮询或事件通知获取结果，详见[异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- 所有[异步任务](../concepts/asynchronous-task.md)均接入阿里云[事件总线 EventBridge](https://help.aliyun.com/zh/eventbridge/product-overview/what-is-eventbridge)，支持通过 HTTP 回调 URL 或 RocketMQ 主动接收任务完成事件，避免轮询限流，具体实现见[通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)。  
- 模型调用可限定在**子业务空间**内，实现模型权限隔离与费用分账，调用时必须使用该子空间专属的 API Key，且标准模型需额外授权，详见[子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 中明确指出“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，无需模型调用授权”，但文档 2 的[异步任务](../concepts/asynchronous-task.md)示例中却包含 `wanx2.1-kf2v-plus`（属调优后模型）的 `list` 查询，而未说明其是否受子空间权限限制。实际开发中，请以控制台模型授权配置为准，调优模型仅能由其所属子空间的 API Key 调用，跨空间调用将返回 `Forbidden` 错误。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `expire_in_seconds` | 临时 API Key 有效期，范围 `[1, 1800]` 秒 | `1800` | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识，用于查询、取消任务 | `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时必需，必须与后续模型调用的模型名严格一致 | `qwen3-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` 临时 URL 时必需的请求头 | — | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` / `limit_per_host` | Java/Python SDK 连接池核心参数，直接影响高并发吞吐 | `256` / `30` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

- **临时凭证**：在浏览器或移动端等不可信环境调用模型前，后端应调用 `/api/v1/tokens` 接口生成临时 API Key，其权限继承自父 Key，有效期最长达 30 分钟，详见[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **异步任务**：创建任务后，推荐优先采用事件总线回调（HTTP/RocketMQ）而非轮询。若必须轮询，需遵守 20 QPS 限流，并按任务类型设置合理间隔（如文生图建议 ≥2s，文生视频建议 ≥10s）。  
- **多模态文件**：调用图像、音视频模型前，需先上传本地文件获取 `oss://` 临时 URL（有效期 48 小时），且上传时指定的 `model_name` 必须与模型调用时一致；调用时务必添加 `X-DashScope-OssResourceResolve: enable` 请求头。  
- **连接优化**：高并发场景下，Java SDK 默认启用连接池，可通过 `Constants.connectionConfigurations` 调整；Python SDK 需显式传入 `requests.Session` 或 `aiohttp.ClientSession` 实现复用，详见[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 限制和注意事项

- **临时资源时效性**：临时 API Key 最长 1800 秒，临时文件 URL 最长 48 小时，**均不可续期，严禁用于生产环境长期服务**。生产环境请使用 OSS 等持久化存储。  
- **配额硬限制**：文件上传凭证接口限流为 100 QPS（按主账号+模型维度），异步任务查询接口限流为 20 QPS（按主账号维度），超限将直接拒绝请求。  
- **绑定关系严格**：上传文件的 API Key 与调用模型的 API Key 必须属于同一阿里云主账号；子业务空间的 API Key 仅能调用该空间已授权的模型（调优模型除外）；临时 API Key 继承父 Key 全部权限，无额外粒度控制。  
- **地域一致性**：各接口 Endpoint（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）与 API Key 地域强绑定，混用将导致 `InvalidApiKey` 错误，详见[Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


