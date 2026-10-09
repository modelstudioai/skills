# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型调用的进阶能力与关键配置要点，涵盖异步任务管理、子业务空间隔离、临时凭证与文件上传、连接复用等核心机制。所有功能均需配合有效的 API Key 使用，且部分能力（如异步通知、子空间调用）对地域和模型类型存在明确约束。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：  
- **同步模型**（如 `qwen-plus` 文本生成）：请求即响应，适用于低延迟、确定性场景；  
- **异步模型**（如 `wanx2.1-t2i-turbo` 图像生成、`video-synthesis` 视频生成、`paraformer-8k-v1` 语音转写）：需先提交任务获取 `task_id`，再轮询或接收事件通知查询结果。异步任务接口统一由 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提供，支持查询、批量列表及取消（仅限 `PENDING` 状态）。  
- **多模态模型**（如 `qwen-vl-plus`）：需通过 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 传入图像/视频/音频，该 URL 有效期为 48 小时，且与指定模型强绑定。

> **注意**：文档 3 中提到的 HTTP 回调与 RocketMQ 通知方案，其事件源 `acs.dashscope` 和事件类型 `dashscope:System:AsyncTaskFinish` 仅适用于已接入事件总线的异步模型（如文生图、文生视频），不适用于纯同步模型或未声明支持事件推送的模型。

## 关键参数

| 参数 | 说明 | 典型取值/范围 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒（默认 60） | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识符 | UUID 格式字符串（如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1`） | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时必需的模型标识，决定存储策略与后续调用兼容性 | `qwen-vl-plus`, `wanx2.1-t2i-turbo` 等 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 调用含 `oss://` URL 的请求头强制参数 | 字符串字面量 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` / `limit` | Java/Python SDK 连接池最大连接数 | Java 默认 32，Python `aiohttp.TCPConnector` 默认 100 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或移动 App 等前端场景中，**禁止硬编码永久 API Key**。应通过后端服务调用 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 接口，传入 `expire_in_seconds=1800` 获取 30 分钟有效期的 `st-****` 凭证，并将其用于后续模型请求。

### 2. 异步任务处理
- **轮询模式**：调用 `/api/v1/tasks/{task_id}` 查询状态，建议按任务类型设置合理间隔（文本向量可 1s，图像生成建议 ≥5s），避免触发 20 QPS 限流。  
- **事件驱动模式**：配置事件总线规则，将 `dashscope:System:AsyncTaskFinish` 事件路由至 HTTP 回调或 RocketMQ，收到通知后仅需一次查询即可获取结果，规避轮询开销与限流风险。详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 3. 子业务空间隔离
调用非默认空间模型时，**必须使用该子空间专属的 API Key**，并确保：
- OpenAI 兼容方式：`base_url` 指向工作空间专属域名（如 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）；  
- DashScope 原生方式：显式设置 `base_http_api_url` 或 SDK 初始化时传入协议与地址。  
> **注意**：子空间内调优部署的模型**不支持 OpenAI 兼容方式调用**，仅可通过 DashScope SDK 或原生 HTTP 接口访问。

### 4. 多模态文件上传
- 上传前调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取 OSS 签名策略；  
- 使用策略参数直传文件至 OSS，获得 `oss://...` URL；  
- 在模型请求中传入该 URL，并**必须添加请求头 `X-DashScope-OssResourceResolve: enable`**。

## 限制和注意事项

- **临时凭证与文件时效性**：临时 API Key 最长 1800 秒，临时文件 URL 最长 48 小时，二者均**不可续期**，超时后请求必然失败。生产环境严禁依赖此机制，应使用长期 OSS 存储。  
- **地域与权限隔离**：各地域（北京、新加坡、弗吉尼亚、中国香港）的 API Key **完全独立**，不可跨地域复用；子业务空间的 API Key 仅能调用该空间授权的模型，且调优模型仅限所属空间调用。  
- **限流策略**：  
  - 文件上传凭证接口：100 QPS（按主账号+模型维度）；  
  - 异步任务查询接口：20 QPS（按主账号维度）；  
  - 临时 API Key 生成：无明确文档说明，但受底层鉴权服务通用限流约束。  
- **连接复用实践**：Java SDK 默认启用连接池，Python 需显式传入 `session` 对象。高并发场景下，`connectionPoolSize`（Java）或 `limit`（Python）应与业务峰值请求数匹配，过低导致阻塞，过高可能压垮服务端。  
- **错误处理**：异步任务取消仅对 `PENDING` 状态有效，其他状态返回 `UnsupportedOperation` 错误码；文件上传失败常见原因为模型名称不匹配或文件超 1GB。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


