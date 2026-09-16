# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型服务的核心能力与使用要点，涵盖支持的模型与功能、关键参数配置、调用方式、以及常见限制与注意事项。内容基于平台当前 API 与 SDK 行为整理，适用于生产环境集成与问题排查。

## 支持的模型/功能

百炼平台提供覆盖文本、图像、视频、语音、多模态等全栈模型能力。可通过 [查询模型列表](raw/model-api-reference/more-about-models/list-models.md) 接口（`GET /api/v1/models`）动态获取实时可用模型，支持按供应商（如 `qwen`, `wan`, `kling`）、能力（`TG` 文本生成、`IG` 图片生成、`VG` 视频生成、`ASR` 语音识别等）、部署模式（`global`, `asia-pacific-china`）等多维度筛选，并返回上下文长度、定价、输入/输出模态等元信息。

部分模型（如图像生成、视频生成、语音转写）采用异步执行模式，需通过任务 ID 查询结果；而文本生成类模型（如 `qwen-plus`, `qwen3-max`）通常支持同步调用。异步任务的生命周期管理由统一的 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提供，包括创建、查询、批量查询及取消。

> **注意**：文档 4 中提到“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”，但文档 10 和 11 明确要求对子业务空间中的标准模型（如 `qwen-plus`）必须显式配置推理权限。该矛盾表明：**调优后部署的模型虽免于权限中心管控，但仍受业务空间隔离约束，且其调用仍需通过该空间的 API Key 发起**——权限模型与部署模型是正交概念，不可混淆。

## 关键参数

- **模型标识**：所有调用均需指定 `model` 参数（如 `qwen3-max`, `wan2.6-i2v-flash`），该值必须与 [查询模型列表](raw/model-api-reference/more-about-models/list-models.md) 返回的 `model` 字段完全一致。
- **限流配额**：模型调用受双重限流控制：账号级（`model_limit`）和业务空间级（`workspace_limit`）。可通过 [查询模型限额](raw/model-api-reference/more-about-models/list-quotas.md) 接口（`GET /api/v1/models/limits`）查看当前配额，例如 `qwen3-max` 可能为 500 QPS，而 `wan2.6-i2v-flash` 仅为 5 QPS。
- **文件上传绑定**：调用多模态模型时，若使用临时 URL 上传文件，必须确保 `model_name` 参数与后续模型调用的 `model` 完全一致，否则请求将失败。该约束在 [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md) 文档中有明确说明。
- **连接复用**：高并发场景下，Java SDK 默认启用连接池，Python SDK 需显式传入 `requests.Session` 或 `aiohttp.ClientSession` 实现复用，详见 [DashScope SDK连接复用配置](raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 使用方式

- **同步调用**：适用于文本生成等低延迟模型。推荐使用 OpenAI 兼容方式（`base_url` 指向 `compatible-mode/v1`）或 DashScope 原生 SDK，需确保 API Key 与目标业务空间匹配（见 [子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)）。
- **异步调用**：适用于图像/视频生成等长耗时任务。流程为：1）发起任务获取 `task_id`；2）轮询或通过事件总线接收完成通知；3）用 `task_id` 查询结果。轮询需遵守 20 QPS 限流，建议按任务类型设置合理间隔（如图像生成建议 ≥5s）。
- **事件驱动通知**：为规避轮询限流与资源浪费，可配置 HTTP 回调或 RocketMQ 接收 [异步任务完成事件](raw/model-api-reference/more-about-models/async-task-api.md)，事件总线推送后仅需一次查询即可获取结果。
- **临时凭证**：在不可信环境（如浏览器）中，应通过后端服务调用 [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 接口（`POST /api/v1/tokens`）签发 TTL ≤1800 秒的短期凭证，避免永久密钥泄露。

## 限制和注意事项

- **临时文件有效期**：通过 [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md) 获取的 `oss://` URL 有效期严格为 48 小时，过期后无法访问，**禁止用于生产环境**；生产环境应使用 OSS 等长期存储。
- **API Key 绑定范围**：临时 API Key 继承父密钥全部权限，但文件上传、异步任务查询、模型调用均强制要求 API Key 所属主账号一致，跨账号操作必然失败。
- **地域与 Endpoint**：各 API 的 Endpoint 严格按地域区分（北京、新加坡、香港等），且不同地域的 API Key 不通用。调用前务必确认 WorkspaceId 与地域匹配，否则返回 401 或 404。
- **限流不可绕过**：文件上传接口限流为 100 QPS（按主账号+模型维度），且不支持扩容；异步任务查询接口为 20 QPS（按主账号维度）。高频调用必须自行实现退避与重试逻辑。
- **权限与模型强耦合**：子业务空间中，标准模型（如 `qwen-plus`）必须通过 [更新模型授权](raw/model-api-reference/more-about-models/update-model-permissions.md) 接口显式授予 `inference: true` 权限，否则调用返回 `403 Forbidden`；而调优模型仅需空间内 API Key 即可调用，无需额外授权。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)


