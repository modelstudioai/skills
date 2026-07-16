# [more](more.md) about models

阿里云百炼在模型调用的核心流程之外，提供了一系列辅助能力，涵盖安全认证、异步任务管理、文件上传、子[业务空间](../concepts/workspace.md)隔离以及高并发场景下的连接优化。本文汇总这些进阶用法的关键要点，帮助开发者在生产环境中安全、高效地使用模型服务。

## 临时 [API Key](../concepts/api-key.md)

在浏览器或移动端等不可信环境中，直接暴露永久 [API Key](../concepts/api-key.md) 存在安全风险。百炼提供了[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)的接口，通过后端服务生成有限时效的临时凭证。

**请求方式**：

```
POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=<TTL>
```

- `expire_in_seconds`：有效期，范围 [1, 1800] 秒，默认 60 秒。
- 返回的 `token` 字段即为临时 [API Key](../concepts/api-key.md)，`expires_at` 为 UNIX 过期时间戳。
- 临时 API Key 继承生成它的永久 API Key 的全部权限，到期后自动失效，无法手动删除。

> **注意**：各地域的 API Key 不同，新加坡地域需将 Endpoint 中的 WorkspaceId 替换为实际值。

## 异步任务管理

图像生成、视频生成等耗时较长的模型采用[异步调用](../concepts/async-invocation.md)机制。百炼提供了三个通用的[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)：

### 查询单个任务

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

返回 `output.task_status` 标识任务状态：`PENDING` / `RUNNING` / `SUCCEEDED` / `FAILED` / `UNKNOWN`。已完成任务通常保留 24 小时后自动清理。

### 批量查询任务状态

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/?start_time=xxx&end_time=xxx&status=xxx
```

支持按时间范围、模型名称、任务状态等条件组合过滤，单次查询时间跨度不超过 24 小时。

### 取消任务

```
POST https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}/cancel
```

仅支持取消 `PENDING` 状态的任务，已开始处理的任务无法取消。

以上三个接口的流量限制均为 20 QPS（主账号维度）。

## 异步任务完成通知

频繁轮询任务结果接口会浪费资源且可能触发限流。百炼已接入阿里云事件总线 EventBridge，支持在任务完成后主动推送通知。详见[通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

两种接入方案：

| 方案 | 适用场景 | 特点 |
|------|----------|------|
| HTTP 回调 URL | 通用场景 | 需要公网或 VPC 可达的 HTTP 接口，接入较简单 |
| RocketMQ | 消息可靠性要求高的场景 | 保证无丢失、支持失败重试，需额外开通 RocketMQ 实例 |

事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`。事件体中 `data.task_status` 和 `data.task_id` 是关键字段，收到通知后只需调用一次查询接口即可获取结果。

## 子[业务空间](../concepts/workspace.md)的模型调用

默认[业务空间](../concepts/workspace.md)的 API Key 拥有所有模型的调用权限。如需按业务线隔离权限或分账，可使用[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

**使用要点**：

- 必须使用子[业务空间](../concepts/workspace.md)自身的 API Key 进行调用。
- 调用标准模型（如 `qwen-plus`）前，需为该空间设置模型调用权限。
- 调用在百炼上调优并部署的模型无需额外授权，但仅能由其所在空间的 API Key 调用。
- 支持 OpenAI 兼容方式和 DashScope 方式调用，但调优后模型仅支持 DashScope 方式。

## 上传本地文件获取临时 URL

[多模态](../concepts/multimodal.md)、图像、视频、音频模型调用时通常需要传入文件 URL。百炼提供了免费的临时存储空间，支持上传本地文件并获取 `oss://` 前缀的临时 URL，详见[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

**关键限制**：

- 文件有效期 48 小时，过期自动清理。
- 上传时必须指定模型名称，且与后续调用的模型一致，不同模型无法共享文件。
- 上传与调用的 API Key 必须属于同一阿里云主账号。
- 单文件不超过 1GB，上传凭证接口限流 100 QPS。
- 使用 `oss://` 形式的 URL 调用模型时，HTTP 请求头中必须添加 `X-DashScope-OssResourceResolve: enable`。

> **注意**：临时 URL 不适用于生产环境。生产环境建议使用阿里云 OSS 等稳定存储方案。

上传方式包括 Python/Java 代码上传和 DashScope 命令行工具（`dashscope oss.upload`）上传。

## [DashScope SDK](../concepts/dashscope-sdk.md) 连接复用配置

高并发场景下，频繁创建连接会导致超时和资源消耗过大。[DashScope SDK](../concepts/dashscope-sdk.md) 支持连接复用来优化性能，详见[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

**Java SDK** 内置连接池，默认启用，核心配置参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `connectionPoolSize` | 32 | 连接池最大连接数 |
| `maximumAsyncRequests` | 32 | 最大并发请求数（需 <= 连接数） |
| `connectTimeout` | 120s | 建立连接超时 |
| `readTimeout` | 300s | 读取数据超时 |
| `connectionIdleTimeout` | 300s | 空闲连接超时 |

**Python SDK** 通过传入自定义 Session 实现连接复用：

- 异步场景：使用 `aiohttp.ClientSession` 配合 `aiohttp.TCPConnector`，可配置 `limit`（总连接数，默认 100）和 `limit_per_host`（单主机连接数）。
- 同步场景：使用 `requests.Session`，同一 Session 内多次请求自动复用 TCP 连接。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)











