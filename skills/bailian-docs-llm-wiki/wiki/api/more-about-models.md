# [more](more.md) about models

阿里云百炼平台支持多种模型调用模式，涵盖同步与异步任务、子业务空间隔离、连接复用优化、临时文件托管及安全凭证管理等核心能力。本文档面向开发者，系统梳理模型调用的关键技术要点，包括适用模型类型、关键参数配置、标准使用方式，以及必须注意的限制与兼容性问题。

## 支持的模型/功能

百炼平台对不同任务类型采用差异化模型调度策略：
- **同步模型**：如 `qwen-plus`、`qwen-vl-plus` 等文本与多模态大模型，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)和 DashScope 原生 SDK 调用，适用于低延迟、确定性响应场景。
- **异步模型**：图像生成（`wanx2.1-t2i-turbo`）、视频生成（`wanx2.1-kf2v-plus`）、语音转写（`paraformer-16k-1`）等长耗时任务，强制采用异步机制，需通过任务 ID 查询结果或配置事件通知。详情见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **子业务空间专属模型**：在子空间中调优部署的模型（如微调后的 `qwen-plus-finetuned`）仅能被该空间的 API Key 调用，且无需额外模型权限授权；而调用标准模型（如 `qwen-plus`）则需显式配置模型调用权限 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 中明确指出“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”，但文档 1 的异步任务示例中列出的 `wanx2.1-kf2v-plus` 等模型名未说明其是否为子空间专属或全局可用，实际调用前须确认模型所属空间及权限状态。

## 关键参数

- **`task_id`**：所有异步任务的唯一标识符，用于查询、批量筛选或取消任务，生命周期默认为 24 小时（以对应任务文档为准）。
- **`model_name`**：上传临时文件时必须指定，且必须与后续模型调用的模型名称严格一致；文件与模型绑定，不可跨模型复用 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **`expire_in_seconds`**：生成临时 API Key 时指定有效期，取值范围为 `[1, 1800]` 秒，默认 60 秒 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **连接池参数**（Java/Python SDK）：如 `connectionPoolSize`（默认 32）、`limit_per_host`（Python 默认无限制），直接影响高并发下的吞吐与稳定性，需按业务负载调整。

## 使用方式

- **异步任务轮询**：调用 `fetch(task_id)` 查询单任务，或 `list()` 批量筛选（支持 `start_time`/`end_time`/`status`/`model_name` 等条件），QPS 限流为 20。推荐结合任务类型设置合理轮询间隔（如图像生成建议拉长间隔）。
- **异步任务事件通知**：为规避轮询限流与资源浪费，应优先配置事件总线（EventBridge）接收 `dashscope:System:AsyncTaskFinish` 事件，再通过 HTTP 回调或 RocketMQ 消费，实现任务完成后的精准触发 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **子空间模型调用**：必须使用该子空间生成的 API Key，并正确配置 `base_url`（如北京地域 OpenAI 兼容模式为 `https://dashscope.aliyuncs.com/compatible-mode/v1`）；调用 DashScope 原生接口时，需显式设置 `base_http_api_url` 指向子空间专属域名。
- **连接复用**：Java SDK 默认启用连接池，可通过 `Constants.connectionConfigurations` 配置超时与大小；Python SDK 推荐传入 `requests.Session`（同步）或 `aiohttp.ClientSession`（异步）复用底层 TCP 连接。
- **临时文件上传**：调用 `/api/v1/uploads?action=getPolicy&model={model_name}` 获取凭证后上传至 OSS，返回 `oss://` URL，有效期 48 小时；**调用模型时必须在 Header 中添加 `X-DashScope-OssResourceResolve: enable`**。

## 限制和注意事项

- **临时文件限制**：上传限流为 100 QPS（按“主账号+模型”维度），且不支持扩容；文件大小上限 1GB，但各模型对输入文件有独立限制；**临时 URL 严禁用于生产环境**，生产环境应使用阿里云 OSS [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **异步任务取消限制**：仅支持取消 `PENDING` 状态的任务，`RUNNING` 或已完成状态无法取消；取消接口同样受 20 QPS 限流约束。
- **CLI 功能不完整**：`dashscope CLI` 当前仅 `video-synthesis` 子命令支持 `fetch`/`list`/`cancel`，其他异步任务（如 `image-synthesis`、`transcription`）需使用 Python SDK 或 curl [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **地域与 Endpoint 绑定**：API Key 具有地域属性（北京/新加坡/弗吉尼亚/中国香港），子空间调用必须匹配对应地域的 `base_url`；通用域名（`dashscope.aliyuncs.com`）与工作空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）均可调用异步任务接口，但 API Key 必须与业务空间匹配。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)


