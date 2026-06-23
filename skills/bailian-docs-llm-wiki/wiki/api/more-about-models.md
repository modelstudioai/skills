# [more](more.md) about models

阿里云百炼在模型 API 核心调用之外，还提供了一系列辅助能力来支撑生产环境中的安全、异步任务管理、文件上传、多空间隔离和高并发优化等需求。本页汇总了这些进阶功能的关键要点和使用方式，帮助开发者快速定位所需能力。

## 临时 API Key

在浏览器、移动 App 等不可信环境中，直接暴露永久 API Key 存在安全风险。百炼支持通过后端服务[生成临时 API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，有效期可自定义（1~1800 秒，默认 60 秒），到期后自动失效，无法手动删除。

**请求示例：**

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `token` | String | 生成的临时 API Key（`st-****` 格式） |
| `expires_at` | Number | 过期时间，UNIX 时间戳（秒） |

> **注意**：临时 API Key 继承生成它的 API Key 的全部权限，包括对特定模型或知识库的访问限制。各地域的 API Key 不同，新加坡地域需将 Endpoint 替换为对应 URL。

## 异步任务管理

图像生成、视频生成等长耗时模型采用异步调用机制。百炼提供了一组通用的[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)，支持三种操作：

### 查询单个任务结果

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

返回任务状态（`PENDING` / `RUNNING` / `SUCCEEDED` / `FAILED` / `CANCELED` / `UNKNOWN`）及完成后的结果。限流 20 QPS。

### 批量查询任务状态

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/
```

支持按 `task_id`、`start_time`/`end_time`（格式 `YYYYMMDDhhmmss`）、`model_name`、`status` 等条件组合筛选，分页返回。时间范围不超过 24 小时。

### 取消排队中的任务

```
POST https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}/cancel
```

仅支持取消状态为 `PENDING` 的任务，已在处理中的任务无法取消。

> **注意**：异步任务完成后通常保留 24 小时，超时后系统自动清理，无法再查询。支持查询当前 API Key 所属主账号下的所有任务。

## 异步任务完成通知

频繁轮询任务结果接口会消耗资源且可能触发限流。百炼已接入阿里云事件总线 EventBridge，支持在任务完成后主动推送通知，详见[通过 HTTP 回调 URL 或 MQ 接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

提供两种接收方案：

| 方案 | 适用场景 | 特点 |
|------|---------|------|
| **HTTP 回调 URL** | 通用场景 | 需公网或 VPC 可达的 HTTP POST 端点 |
| **RocketMQ** | 对消息可靠性要求高 | 支持失败重试，消息无丢失 |

**事件标识：** 事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`。事件 `data` 中包含 `task_id`、`task_status`、`region` 等字段，可据此调用查询结果接口一次获取最终结果。

配置步骤概要：
1. 在事件总线控制台（北京地域）进入 `default` 云服务专用总线
2. 创建事件规则，选择事件源 `acs.dashscope` 和事件类型 `dashscope:System:AsyncTaskFinish`
3. 配置事件目标为 HTTP 或 RocketMQ
4. 可通过事件模式按 `user_api_unique_key` 的模型后缀过滤特定事件

## 子[业务空间](../concepts/workspace.md)的模型调用

默认[业务空间](../concepts/workspace.md)的 API Key 可调用所有模型，权限较大。通过创建[子业务空间](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)，可以实现：

- **权限管控**：限制 RAM 用户只能通过指定子空间的 API Key 调用已授权的模型
- **费用分账**：每个子空间独立生成账单，便于多业务场景的费用拆分

**使用要点：**

- 必须使用子[业务空间](../concepts/workspace.md)自己的 API Key 调用
- 调用标准模型（如 `qwen-plus`）前需为该空间设置模型调用权限
- 调优并部署的模型无需额外授权，但仅能由其所在空间的 API Key 调用
- 支持 [OpenAI 兼容接口](../concepts/openai-compatible.md)和 [DashScope SDK](../concepts/dashscope-sdk.md) 两种调用方式
- 新加坡地域的 `base_url` 需包含 `{WorkspaceId}` 前缀

> **注意**：调优后的模型仅支持通过 DashScope 方式调用，不支持 OpenAI 兼容方式。

## 上传本地文件获取临时 URL

调用多模态、图像、视频或音频模型时，通常需要传入文件 URL。百炼提供了免费的临时存储空间，详见[上传本地文件获取临时 URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

**使用限制：**

| 限制项 | 说明 |
|--------|------|
| 文件与模型绑定 | 上传时必须指定模型名称，且须与后续调用的模型一致 |
| 文件与主账号绑定 | 上传和调用的 API Key 必须属于同一主账号 |
| 有效期 | 48 小时，超时自动清理 |
| 限流 | 上传凭证接口 100 QPS（按主账号 + 模型维度），不支持扩容 |
| 用途限制 | 不可查询、修改或下载，仅能通过 URL 在模型调用时使用 |

**上传流程：**
1. 调用 `GET https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证
2. 使用凭证将文件 POST 到 OSS，获取 `oss://` 前缀的临时 URL
3. 在模型调用中使用该 URL

> **注意**：临时 URL 仅适合开发测试，生产环境建议使用阿里云 OSS 等稳定存储。

## [DashScope SDK](../concepts/dashscope-sdk.md) 连接复用

高并发场景下，通过[连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)可减少资源消耗、提高请求效率。

### Java SDK

内置连接池，默认启用。关键配置参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `connectionPoolSize` | 32 | 最大连接数 |
| `maximumAsyncRequests` | 32 | 最大并发请求数（需 <= 最大连接数） |
| `connectTimeout` | 120s | 建立连接超时 |
| `readTimeout` | 300s | 读取数据超时 |
| `connectionIdleTimeout` | 300s | 空闲连接超时 |

通过 `ConnectionConfigurations.builder()` 构建配置并调用 `Constants.setConnectionConfigurations()` 设置。

### Python SDK

通过传入自定义 `requests.Session`（同步）或 `aiohttp.ClientSession`（异步）实现连接复用：

```python
import requests
from dashscope import Generation

session = requests.Session()
try:
    response = Generation.call(
        model='qwen-plus',
        prompt='你好',
        session=session
    )
finally:
    session.close()
```

推荐使用 `with` 语句自动管理 Session 生命周期。异步场景建议使用 `asyncio` + `aiohttp.ClientSession`。

## 最佳实践

- 不可信环境使用临时 API Key，避免永久 Key 泄露
- 高并发异步任务优先使用 EventBridge 通知而非轮询（轮询限流 20 QPS）
- 多业务场景使用子[业务空间](../concepts/workspace.md)隔离权限和费用
- 生产环境文件存储使用 OSS，临时 URL 仅用于开发测试
- Java SDK 根据并发量合理配置 `connectionPoolSize` 和 `maximumAsyncRequests`
- 所有接口调用失败时，参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)排查

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)




