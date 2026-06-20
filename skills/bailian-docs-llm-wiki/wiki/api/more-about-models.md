# [more](more.md) about models

阿里云百炼在模型调用的基础能力之外，提供了一系列辅助功能来满足生产环境中的安全性、异步处理、文件管理、多租户隔离和高并发性能等需求。本页汇总了临时 API Key 生成、异步任务管理与通知、文件上传、子业务空间调用以及 SDK 连接复用等进阶用法，帮助开发者构建更健壮的模型调用方案。

## 临时 API Key

在浏览器、移动 App 等不可信环境中直接使用永久 API Key 存在泄露风险。百炼支持通过后端服务[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，要点如下：

- **生成方式**：向 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 发送请求，需在 Header 中携带永久 API Key
- **有效期**：默认 60 秒，可通过 `expire_in_seconds` 参数设置，范围 [1, 1800] 秒
- **权限继承**：临时 API Key 继承生成它的永久 API Key 的全部权限，包括模型和知识库的访问限制
- **不可删除**：临时 API Key 到期后自动失效，无法手动删除

请求示例：

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

响应中返回 `token`（临时 API Key）和 `expires_at`（UNIX 时间戳，秒）。

> **注意**：各地域的 API Key 不同，新加坡地域需使用对应的 Endpoint 并替换 WorkspaceId。

## 异步任务管理

图像生成、视频生成等处理时间较长的模型采用异步调用机制。百炼提供了三个通用的[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)，流量限制均为 20 QPS（按主账号维度）。

### 查询单个任务

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

返回 `output.task_status` 表示任务状态，可能的值包括：`PENDING`（排队中）、`RUNNING`（处理中）、`SUCCEEDED`（成功）、`FAILED`（失败）、`UNKNOWN`（不存在或未知）。对于包含多个子任务的任务，只要有一个子任务成功，整个任务即标记为成功。

### 批量查询任务状态

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/
```

支持按 `task_id`、`start_time`/`end_time`（格式 `YYYYMMDDhhmmss`）、`model_name`、`status` 等条件组合查询，支持分页。若未指定时间范围，默认查询最近 24 小时的数据，且时间跨度不可超过 24 小时。

### 取消任务

```
POST https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}/cancel
```

仅支持取消状态为 `PENDING` 的任务，其他状态的任务无法取消。

> **注意**：异步任务在完成后通常保留 24 小时（具体以对应 API 文档为准），超时后系统自动清理。查询和取消操作均支持当前 API Key 所属主账号下的所有任务，但无法操作其他主账号的任务。

## 异步任务完成通知

频繁轮询任务结果接口会造成资源浪费并可能触发限流。百炼已接入[事件总线 EventBridge](../../raw/model-api-reference/more-about-models/async-task-api.md)，支持在任务完成后主动推送通知，提供两种接收方案：

### 方案一：HTTP 回调 URL

任务完成后，事件总线将事件推送到您配置的 HTTP 回调接口。操作步骤：

1. 准备一个支持公网或 VPC 访问的 HTTP URL（POST 请求、JSON Body）
2. 在事件总线控制台（北京地域）查询事件，事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`
3. 创建事件规则，配置事件模式（可按 `user_api_unique_key` 等字段过滤）
4. 设置事件目标为 HTTP，填写回调 URL

### 方案二：RocketMQ 消息队列

适合对消息可靠性要求较高的场景。事件总线将事件转发到 RocketMQ 队列，业务方监听并消费消息。需先准备 RocketMQ 实例（含 Topic 和 Group），再在事件总线中配置转发规则。

两种方案的选型建议：

| 维度 | 主动轮询 | 事件通知 |
|------|----------|----------|
| 限流 | 查询接口 20 QPS 限流 | 不限流 |
| 实时性 | 依赖轮询频率 | 任务完成后立即推送 |
| 适用场景 | 低并发、小规模 | 高并发、大规模 |

## 子业务空间的模型调用

默认业务空间的 API Key 可调用所有模型，权限较大。通过创建[子业务空间](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)可以实现模型调用权限管控和费用分账。

### 准备工作

1. 在子业务空间中创建 API Key 并配置到环境变量
2. 为子业务空间设置模型调用权限（调用标准模型时需要；调优部署的模型无需授权，但仅限所在空间的 API Key 调用）

### 调用方式

子业务空间的模型调用与默认空间的唯一区别是**必须使用该子业务空间的 API Key**。支持两种调用协议：

- **OpenAI 兼容**：`base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，支持 Python、Java、Node.js、Go、C#、PHP、curl 等
- **DashScope**：使用 [DashScope SDK](../concepts/dashscope-sdk.md) 原生调用方式，支持 Python 和 Java

> **注意**：调优后的模型仅支持通过 DashScope 方式调用，不支持 OpenAI 兼容方式。新加坡地域的 `base_url` 格式为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`，需替换为实际的业务空间 ID。

## 上传本地文件获取临时 URL

调用多模态、图像、视频或音频模型时需要传入文件 URL。百炼提供免费临时存储空间，可通过[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)功能获取 `oss://` 前缀的临时 URL。

### 使用限制

- **文件与模型绑定**：上传时必须指定模型名称，且须与后续调用的模型一致
- **文件与主账号绑定**：上传和调用所使用的 API Key 必须属于同一主账号
- **有效期 48 小时**：过期后自动清理
- **不可查询/修改/下载**：仅能通过 URL 参数在模型调用时使用
- **限流 100 QPS**：按"主账号+模型"维度限流

### 上传方式

1. **代码上传**：通过 Python 或 Java 调用 `https://dashscope.aliyuncs.com/api/v1/uploads` 获取上传凭证，再将文件上传至 OSS
2. **命令行上传**：使用 `dashscope oss.upload --model <model> --file <file>` 命令（需 DashScope Python SDK >= 1.24.0）

> **注意**：使用 `oss://` 形式的临时 URL 调用模型时，**必须**在 HTTP 请求头中添加 `X-DashScope-OssResourceResolve: enable`。临时 URL 不适合生产环境，生产环境建议使用阿里云 OSS。

## [DashScope SDK](../concepts/dashscope-sdk.md) 连接复用配置

高并发场景下可能出现请求超时、资源消耗大等问题。通过[连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)可以优化网络连接效率。

### Java SDK

内置连接池机制，默认启用。关键可配置参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `connectTimeout` | 120s | 建立连接超时时间 |
| `readTimeout` | 300s | 读取数据超时时间 |
| `writeTimeout` | 60s | 写入数据超时时间 |
| `connectionIdleTimeout` | 300s | 空闲连接超时时间 |
| `connectionPoolSize` | 32 | 最大连接数 |
| `maximumAsyncRequests` | 32 | 最大并发请求数 |
| `maximumAsyncRequestsPerHost` | 32 | 单主机最大并发请求数 |

通过 `ConnectionConfigurations.builder()` 构建配置并赋值给 `Constants.connectionConfigurations`。

### Python SDK

支持同步和异步两种连接复用方式：

- **异步方式**：通过 `aiohttp.ClientSession` + `aiohttp.TCPConnector` 实现，可配置 `limit`（总连接数，默认 100）和 `limit_per_host`（单主机连接数，默认无限制），将 `session` 参数传入 `AioGeneration.call()`
- **同步方式**：通过 `requests.Session` 实现，在同一 Session 内的多次请求复用底层 TCP 连接，将 `session` 参数传入 `Generation.call()`

### 最佳实践

- Java SDK 根据业务并发量合理配置连接池参数，避免连接数过高或过低
- Python SDK 推荐使用 `with` 语句自动管理 Session 生命周期
- 异步架构（asyncio、FastAPI 等）使用异步调用方式，传统同步架构使用同步方式

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


