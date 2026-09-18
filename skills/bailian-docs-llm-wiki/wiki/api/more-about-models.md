# [more](more.md) about models

本文档面向开发者，汇总百炼平台模型调用的关键技术要点，涵盖模型支持能力、核心参数配置、调用方式选择及常见限制。内容基于官方 API 行为与 SDK 实现，聚焦可落地的工程实践，不包含营销性描述。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**：如 `qwen-plus`、`qwen-vl-plus` 等文本/多模态生成模型，请求后直接返回结果；
- **异步模型**：如图像生成（`wanx2.1-t2i-turbo`）、视频生成（`wanx2.1-kf2v-plus`）、语音转写（`paraformer-16k-1`）等长耗时任务，需通过任务 ID 轮询或事件通知获取结果。详情见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

子业务空间（Workspace）支持模型权限隔离与费用分账，适用于 RAM 用户管控或多业务线独立计费场景。调用子空间模型时，**必须使用该空间专属的 API Key**，且标准模型需额外配置调用权限；而调优后部署的模型仅限其所在空间调用，无需额外授权 —— 详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

多模态输入依赖文件 URL。平台提供免费临时 OSS 存储，上传后生成 `oss://` 格式 URL（有效期 48 小时），但**文件与模型强绑定**：上传时指定的 `model_name` 必须与后续模型调用一致，且文件仅限同一主账号下使用。生产环境应避免依赖此机制，推荐使用阿里云 OSS 长期存储 —— 参考 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 5 明确指出“临时 URL 请勿用于生产环境”，而文档 4 中子空间调用示例未强调此风险。实际工程中，若在子空间内调用需上传文件的模型（如 `qwen-vl-plus`），仍须遵守该限制。

## 关键参数

| 参数 | 作用 | 典型值/范围 | 注意事项 |
|------|------|-------------|----------|
| `expire_in_seconds`（临时 API Key） | 设置临时密钥有效期 | `[1, 1800]` 秒 | 默认 60 秒，超时后自动失效且不可手动删除 —— 见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id`（异步任务） | 唯一标识异步任务 | UUID 字符串 | 查询/取消任务均需此 ID；仅 `PENDING` 状态可取消 |
| `page_size` / `page_no`（批量查询） | 控制分页结果数量 | `page_size` 默认 10，最大建议 ≤100 | 批量查询接口有 24 小时时间窗口限制，且任务数据保留期以具体模型文档为准 |
| `connectionPoolSize`（Java SDK） | HTTP 连接池最大连接数 | 默认 32，高并发建议调至 256 | 需与 `maximumAsyncRequests` 协同配置，后者不应超过前者 —— 来自 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `X-DashScope-OssResourceResolve: enable`（Header） | 启用临时 OSS URL 解析 | 固定字符串 | 调用含 `oss://` URL 的模型时**必须显式添加**，否则报错 |

## 使用方式

### 认证与环境适配
- **临时 API Key**：适用于浏览器、App 等不可信环境，由后端服务调用 `/api/v1/tokens` 接口生成，继承源 Key 全部权限（含模型/知识库访问限制）。
- **子空间调用**：区分地域与协议：
  - DashScope 原生协议：北京地域用 `https://dashscope.aliyuncs.com/api/v1/...`；新加坡等地域需替换为 `{WorkspaceId}.{region}.maas.aliyuncs.com`；
  - OpenAI 兼容协议：北京地域用 `https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡等地域需使用工作空间专属域名。

### 异步任务处理
避免轮询导致的限流（20 QPS）与资源浪费，推荐两种方案：
- **主动轮询**：适用于低并发场景，按任务类型设置合理间隔（文本向量可短，图像/视频宜长）；
- **事件驱动**：通过 [事件总线 EventBridge](../../raw/model-api-reference/more-about-models/async-task-api.md) 配置 HTTP 回调或 RocketMQ，任务完成即推送 `dashscope:System:AsyncTaskFinish` 事件，业务系统解析 `task_id` 后单次查询结果。

### 连接优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 全局配置连接池参数（如 `connectTimeout`、`connectionPoolSize`）；
- **Python SDK**：同步调用传入 `requests.Session`，异步调用传入 `aiohttp.ClientSession`，均支持复用底层 TCP 连接。

## 限制和注意事项

- **临时文件**：单文件 ≤1 GB；上传限流 100 QPS（按“主账号+模型”维度）；48 小时后自动清理；**禁止用于生产环境、压测及高并发场景**。
- **异步任务**：结果默认保留 24 小时（以对应模型文档为准），超时后无法查询；仅 `PENDING` 状态可取消；批量查询时间窗口不得超过 24 小时。
- **地域与 Key 绑定**：各 Region（北京/新加坡/弗吉尼亚/中国香港）的 API Key **完全独立**，不可混用；子空间 API Key 仅在其所属地域有效。
- **SDK 版本要求**：部分功能依赖新版 SDK，例如 `Files.upload(purpose='inference')` 需 Python SDK ≥ `1.27.3`；Java SDK 连接池配置需 ≥ `2.12.0`。
- **安全边界**：临时 API Key 权限继承自源 Key，务必最小化源 Key 权限；子空间模型调用权限需显式授予，避免默认开放。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


