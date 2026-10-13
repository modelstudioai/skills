# 异步任务模型

异步任务模型是百炼平台对长耗时、高资源消耗类 AI 服务（如文档解析、视频生成、图像翻译等）采用的标准调用范式：用户提交任务后立即获得唯一任务标识（`biz_id` 或 `task_id`），结果需通过轮询或事件回调方式获取，不阻塞请求线程。

## 在百炼平台的不同场景中，这个概念如何使用

- **文档与音视频解析（ParseX API）**：所有 `/parse/submit` 和 `/extract/submit` 请求均返回 `biz_id`，后续通过 `/parse/result?biz_id=...` 或 `/extract/result?biz_id=...` 轮询状态。适用于 PDF/Word/MP4 等大文件处理，典型耗时从数秒到数分钟不等。
  
- **视频生成（Video Generation API）**：必须显式声明 `X-DashScope-Async: enable` 请求头，否则直接报错；任务创建后返回 `task_id`，结果通过 `GET /api/v1/tasks/{task_id}` 查询。支持多模型（HappyHorse、Vidu、Kling 等）统一异步调度，适合生成 5–60 秒高清视频的长周期任务。

- **Qwen-MT 全模态翻译（`qwen-mt-uni`）**：当输入为 PDF、PPT、MP3 等非纯文本格式时，自动触发异步流程（同步模式仅支持纯文本字符串）；返回 `task_id`，需调用 `/api/v1/tasks/{task_id}` 获取最终翻译结果及重构后的文件 URL。

- **其他多模态/生成类模型（如文生图、语音转写）**：在 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 中统一支持生命周期操作（查询、取消、重试），开发者可基于 `task_id` 实现任务队列、失败重试、进度跟踪等生产级能力。

> ✅ 提示：异步任务不共享同步接口的限流策略（如 `/chat/completions` 的 tokens/min），但受独立的「异步任务并发数」和「轮询 QPS」限制（默认 20 QPS，建议文本类轮询间隔 ≥1s，视频/图像类 ≥3s）。

## 关键参数和配置

| 参数 | 位置 | 说明 | 是否必需 | 示例 |
|------|------|------|----------|------|
| `biz_id` / `task_id` | 响应体 & 查询路径 | 任务唯一标识符，由提交接口返回，用于结果查询和事件关联 | 是 | `"a8532587-xxxx-xxxx-xxxx-0c46b17950d1"` |
| `X-DashScope-Async: enable` | 请求 Header | 视频生成等强异步模型的强制开关，缺失将拒绝请求 | 视模型而定（如 Video Generation 必填） | `"enable"` |
| `output.oss_config` | 请求体 `output` 字段 | 指定结果持久化至客户 OSS，避免轮询期间结果过期（默认保留 30 天，OSS 存储可长期保留） | 否（推荐启用） | `{ "bucket": "my-bucket", "prefix": "results/" }` |
| `callback_url` | 请求体（部分模型支持） | 配置 HTTP 回调地址，任务完成时平台主动推送 `POST` 事件（替代轮询） | 否 | `"https://your-server.com/webhook"` |

- **状态字段**：所有异步结果响应中均含 `data.status`，取值为：
  - `"processing"`：任务执行中（需继续轮询）
  - `"success"`：成功，`data.output` 包含结果
  - `"failed"`：失败，`data.code` + `data.message` 提供错误定位依据（如 `ProcessingTimeout`, `ParseResultNotReusable`）

- **保留期约束**：
  - 解析类任务结果默认保留 **30 天**；
  - 字段抽取复用解析结果时，要求源 `biz_id` 创建时间 ≤ **7 天**；
  - 临时文件 URL（如上传后生成的 `oss://` 地址）有效期为 **48 小时**。

## 面向开发者，简洁实用

- ✅ **必做**：始终检查 `data.status`，不要假设首次轮询即成功；对 `processing` 状态设置指数退避重试（如 1s → 3s → 5s）。
- ✅ **推荐**：生产环境优先使用 **事件回调（EventBridge）** 替代轮询，降低延迟与限流风险；参考 [异步任务事件总线配置](raw/model-api-reference/more-about-models/async-task-api.md)。
- ⚠️ **注意**：`biz_id` 和 `task_id` **不可跨模型复用**（如 ParseX 的 `biz_id` 不能传给 Video Generation 接口）；`file_url` 必须公网可访问且稳定（建议使用带签名的 OSS URL）。
- 🛡️ **安全**：异步任务不改变鉴权逻辑——仍需 `Authorization: Bearer $API_KEY`，且 API Key 必须与任务所属地域、子业务空间匹配。

## 关联主题页

- [api overview](../api/api-overview.md)
- [video generation api](../api/video-generation-api.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [more about models](../api/more-about-models.md)


