# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型调用的核心能力与配置要点，涵盖模型发现、权限管理、异步任务处理、文件上传、限流控制及连接优化等关键环节。所有功能均通过标准 API 或 SDK 提供，无需依赖控制台操作即可完成全链路集成。

## 支持的模型/功能

百炼平台支持多模态、文本、语音、图像、视频及 3D 等全类型模型，可通过统一接口查询与管理。调用前需明确模型能力（如 `TG` 文本生成、`IG` 图片生成）、部署模式（`global`/`asia-pacific-china`）及推理供应商（如 `aliyun-bailian`）。模型列表可通过 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 接口动态获取，支持按 `capabilities`、`providers`、`features` 等多维度筛选，并返回上下文长度、定价及模态信息等元数据。

子业务空间支持细粒度模型管控：非默认空间的 API Key 默认无模型调用权限，需显式授权；而调优后部署的模型仅能被其所在空间的 API Key 调用，且不支持 OpenAI 兼容方式（详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)）。

> **注意**：文档中“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”与 [查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md) 的实际行为矛盾——后者明确要求对 `inference` 权限进行显式授权。以 `list-model-permissions` 和 `update-model-permissions` 接口为准，所有标准模型及调优模型均需完成推理授权方可调用。

## 关键参数

- **模型标识**：使用 `model` 字段指定模型 ID（如 `qwen3-max`），而非名称；该 ID 必须与 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 返回的 `model` 字段完全一致。
- **地域与 Endpoint**：各服务地域需匹配对应 Endpoint（如北京为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），`{WorkspaceId}` 为业务空间 ID，不可省略。
- **临时文件绑定**：上传本地文件时必须指定 `model_name` 参数，且该值必须与后续模型调用的 `model` 完全一致，否则调用失败。
- **异步任务状态**：任务完成事件中 `data.task_status` 字段取值为 `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`/`CANCELED`/`UNKNOWN`，其中 `SUCCEEDED` 表示整体成功（即使部分子任务失败），需结合 `output.task_metrics` 判断子任务详情。

## 使用方式

### 模型调用与权限
1. **查询可用模型**：调用 `GET /api/v1/models` 获取模型元数据；
2. **检查授权状态**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 确认目标模型是否已获 `inference: true` 权限；
3. **授权（如需）**：调用 `POST /api/v1/models/permissions` 设置 `inference: true`；
4. **发起调用**：使用对应模型的 API（如 `/chat/completions`）或 SDK，传入正确 `model` 和 `api_key`。

### 异步任务处理
对图像/视频等长耗时任务，推荐采用事件驱动方式接收结果，避免轮询：
- 配置事件总线 HTTP 回调或 RocketMQ 目标，监听 `dashscope:System:AsyncTaskFinish` 类型事件；
- 解析事件 `data.task_id` 和 `data.task_status`，再调用一次 `GET /api/v1/tasks/{task_id}` 获取结果；
- 若无法接入事件总线，则使用 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 进行轮询，注意其 20 QPS 限流。

### 文件上传
调用多模态模型前，需先上传文件获取临时 URL：
- 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证；
- 使用凭证将文件上传至 OSS，获得 `oss://` 开头的 URL；
- 在模型请求中传入该 URL，并**必须添加 Header**：`X-DashScope-OssResourceResolve: enable`；
- 注意：临时 URL 有效期 48 小时，且上传接口本身有 100 QPS 限流，**生产环境应使用 OSS 直传**。

### 连接优化
高并发场景下，应启用连接复用：
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize`、`readTimeout`）；
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession()` 并配置 `TCPConnector`；
- 具体配置方法详见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 限制和注意事项

- **限流策略分层**：模型调用受账号级（`model_limit`）与业务空间级（`workspace_limit`）双重限制，后者不能超过前者。可通过 [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md) 查看实时配额，并用 [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md) 动态调整。
- **临时凭证时效性**：临时 API Key 最长 TTL 为 1800 秒（30 分钟），且**无法提前撤销**，仅能等待自动过期。
- **文件安全边界**：上传文件与 API Key 所属主账号强绑定，不同主账号间不可共享；且文件仅支持单次读取，不可查询、修改或下载。
- **异步任务保留期**：任务结果默认保留 24 小时，超时后 `GET /api/v1/tasks/{task_id}` 将返回 `UNKNOWN` 状态，需及时获取。
- **地域一致性**：API Key、Endpoint、事件总线地域三者必须一致（如均在北京），跨地域调用将失败。

## 来源文档

- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


