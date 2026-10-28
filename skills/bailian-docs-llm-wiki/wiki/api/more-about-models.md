# [more](more.md) about models

本文档面向开发者，汇总百炼平台模型调用的核心扩展能力，涵盖临时凭证、异步任务管理、子空间隔离、[文件上传](../concepts/file-upload.md)、连接复用等关键机制。这些功能不改变基础模型接口语义，但显著提升安全性、可靠性与生产可用性。所有能力均需配合有效的 API Key 使用，具体权限与地域约束请参考各功能文档。

## 支持的模型/功能

百炼平台支持以下增强型模型调用功能，适用于不同场景需求：

- **临时 API Key**：在浏览器、移动 App 等不可信环境调用模型服务时，通过后端安全生成短期有效（1–1800 秒）的临时密钥，避免永久密钥泄露。该密钥继承源 API Key 的全部权限（含模型与知识库访问限制）[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **异步任务管理**：图像生成、视频合成、长文本语音转写等耗时操作采用异步模式，需先创建任务再轮询或监听结果。平台提供统一的 `/api/v1/tasks/{task_id}` 查询接口及批量管理能力 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **HTTP 回调与 RocketMQ 通知**：替代轮询，通过事件总线（EventBridge）主动推送 `dashscope:System:AsyncTaskFinish` 事件至 HTTP URL 或 RocketMQ 队列，降低限流风险并提升实时性 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **子业务空间模型调用**：支持在非默认业务空间中调用标准模型（如 `qwen-plus`）或专属微调模型。子空间可独立管控权限与分账，调用时必须使用该空间的 API Key 并指定对应地域域名 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。
- **本地[文件上传](../concepts/file-upload.md)获取临时 URL**：多模态模型（如 VL 模型）需传入文件 URL 时，可将本地图片/音视频上传至百炼免费临时存储，获得 `oss://` 前缀的 48 小时有效 URL；调用时须在 Header 中显式添加 `X-DashScope-OssResourceResolve: enable` [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 5 明确指出“[文件上传](../concepts/file-upload.md)与模型调用所使用的 API Key 必须属于同一个阿里云主账号”，而文档 4 中子业务空间调用示例未强调此约束。实际使用中，若子空间属于某主账号，则其 API Key 与上传文件的 API Key 必须同属该主账号——二者逻辑一致，无实质矛盾，但文档 4 应补充此说明以避免歧义。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 文档依据 |
|------|------|----------------|-----------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串，由创建任务接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `contain_result` (事件字段) | 异步任务完成事件是否内嵌结果 | `true`/`false`；设为 `true` 可减少一次查询，但事件体更大 | [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md) |
| `model` (上传策略参数) | 文件上传时绑定的目标模型名 | 必须与后续模型调用的 `model` 完全一致，否则调用失败 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` / `max_connections` | SDK 连接池最大连接数 | Java 默认 32，Python `httpx` 无默认限制；高并发建议调大 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800` 发起 POST 请求，Header 带 `Authorization: Bearer $DASHSCOPE_API_KEY`，响应返回 `token` 字段。
- **异步任务查询**：使用 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}`，Header 带 `Authorization`，支持 Python SDK `client.images.jobs.fetch(task_id)` 等封装方法。
- **HTTP 回调配置**：在事件总线控制台创建规则，事件源选 `acs.dashscope`，类型选 `dashscope:System:AsyncTaskFinish`，目标设为您的公网或 VPC 内 HTTP 地址。
- **子空间调用（DashScope SDK）**：初始化 Client 时传入 `workspace` 和 `region`（如 `"ap-southeast-1"`），并确保 `api_key` 为该子空间生成的密钥。
- **文件上传（SDK 封装）**：Python 使用 `client.files.upload(file_path, purpose="inference")`；注意返回的 `oss://` URL 必须配合 `X-DashScope-OssResourceResolve: enable` Header 使用。
- **连接复用（Python）**：构造 `dashscope.Client` 或 `AsyncClient` 时传入自定义 `httpx.Client` 或 `httpx.AsyncClient` 实例，并配置 `limits`。

## 限制和注意事项

- **临时 API Key**：无法手动删除，到期自动失效；其权限完全继承自签发它的 API Key，务必严格管控源密钥权限。
- **异步任务查询**：单账号限流 20 QPS；任务数据保留期通常为 24 小时（以具体模型文档为准），超时后无法查询。
- **文件上传**：单文件 ≤ 1 GB；上传凭证接口限流 100 QPS（按主账号+模型维度）；临时 URL 仅 48 小时有效，**严禁用于生产环境**；生产环境应使用 OSS 自有存储 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **子业务空间**：调用标准模型前，需在控制台为该子空间**显式授权**对应模型；调用微调部署模型则无需额外授权，但仅限本空间 API Key 调用。
- **连接复用**：Java SDK 默认启用连接池，Python 需显式传入 `http_client`；异步客户端（`AsyncClient`）必须用 `async with` 或手动 `aclose()` 释放资源，否则可能泄漏连接。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


