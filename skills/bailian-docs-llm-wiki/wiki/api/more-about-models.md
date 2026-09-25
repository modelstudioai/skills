# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的关键扩展能力，涵盖临时凭证、异步任务管理、子业务空间隔离、文件上传、连接复用等核心机制。所有能力均基于标准 API Key 体系构建，需配合正确的地域 Endpoint 和权限配置使用。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）适用于低延迟文本生成、多模态理解等场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）适用于耗时较长的任务，需通过任务 ID 轮询或事件通知获取结果。  

异步任务统一由 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提供标准化接口（`fetch`/`list`/`cancel`），支持跨模型、跨地域查询，且任务数据默认保留 24 小时（具体以各模型文档为准）。  
对于多模态输入（图像、音频、视频），需先调用 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口获取 `oss://` 格式临时 URL，并在模型请求头中显式添加 `X-DashScope-OssResourceResolve: enable` 才能被正确解析。

> **注意**：文档 5 明确要求“文件上传时必须指定模型名称，且该模型须与后续调用的模型一致”，但文档 3 中子业务空间调用示例未体现此约束；实际开发中务必确保 `model_name` 参数在文件上传与模型调用两个环节严格一致，否则将触发模型拒绝服务。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID v4 格式字符串，由创建任务接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `contain_result` | 事件通知是否内嵌结果 | `true`/`false`，设为 `true` 可减少一次查询调用 | [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，高并发建议调至 256 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `limit_per_host` | Python 异步 SDK 单主机连接上限 | 默认 0（无限制），建议设为 30 避免压垮服务端 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或移动 App 等前端场景，**禁止硬编码永久 API Key**。应通过后端服务调用 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 接口，传入 `expire_in_seconds=1800` 获取 30 分钟有效期的 `st-***` 凭证，并将其透传至前端用于模型请求。

### 2. 子业务空间隔离
当需按业务线分账或精细化授权时，应在子业务空间创建独立 API Key，并在 SDK 或 HTTP 请求中指定对应地域的专属域名（如新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`）。调用标准模型前，**必须在控制台为该空间单独开通模型权限**；而调优部署的模型则自动绑定空间，无需额外授权。

### 3. 异步任务结果获取
推荐两种方式避免轮询限流（20 QPS）：
- **主动轮询**：调用 `GET /api/v1/tasks/{task_id}`，根据 `task_status` 字段判断状态（`PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`）；  
- **事件驱动**：通过 [事件总线配置 HTTP 回调或 RocketMQ](../../raw/model-api-reference/more-about-models/async-task-api.md)，监听 `dashscope:System:AsyncTaskFinish` 事件，解析 `data.task_id` 后单次查询结果。

### 4. 连接复用优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 全局配置连接池参数（如 `connectionPoolSize=256`, `connectTimeout=10`）；  
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=TCPConnector(limit=100))`。

## 限制和注意事项

- **临时文件**：`oss://` URL 有效期严格为 **48 小时**，且与主账号及模型强绑定；生产环境必须使用 OSS 等长期存储方案，[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口明确禁止用于压测与高并发场景（QPS 限流 100，不可扩容）。  
- **临时 API Key**：继承生成者 API Key 的全部权限，**无法降权**；到期自动失效，不支持手动删除。  
- **异步任务取消**：仅支持取消 `PENDING` 状态任务，`RUNNING` 或已完成任务调用 `cancel` 接口将返回 `UnsupportedOperation` 错误码。  
- **地域一致性**：API Key、WorkspaceId、Endpoint 地域三者必须匹配（北京/新加坡/弗吉尼亚/中国香港），混用将导致 `InvalidApiKey` 或 404 错误。  
- **SDK 版本依赖**：Python SDK 文件上传需 `>=1.27.3`，Java SDK 连接池配置需 `>=2.12.0`，旧版本不支持对应能力。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


