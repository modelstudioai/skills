# 异步任务

异步任务是百炼平台中处理高耗时、长周期模型推理的标准执行模式：客户端提交请求后立即获得唯一任务标识（如 `biz_id` 或 `task_id`），服务端后台执行实际计算，客户端通过轮询或回调方式获取最终结果。该模式解耦了请求与响应，避免连接超时，适用于文档解析、视频生成、3D建模、大文件翻译等资源密集型场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **ParseX 文档与字段处理**：所有 `/parse/submit` 和 `/extract/submit` 接口均强制异步。提交后返回 `biz_id`，需持续调用 `/parse/result` 或 `/extract/result` 查询 `data.status`（`success`/`failed`）；解析结果保留 30 天，但仅 7 天内可复用于字段抽取。
  
- **Video Generation（视频生成）**：全部模型（HappyHorse、万相、爱诗、Vidu 等）必须启用异步——请求头必须包含 `X-DashScope-Async: enable`，否则报错 `"current user api does not support synchronous calls"`。成功响应含 `task_id`（24 小时有效），通过 `GET /api/v1/tasks/{task_id}` 轮询状态，`SUCCESS` 时返回 `output.video_url`。

- **3D Generation（Tripo）**：所有接口仅支持异步，且**严格限定华北2（北京）地域**。请求头需含 `X-DashScope-Async: enable`，响应返回 `task_id`；后处理任务（如贴图、分割）常需引用前序任务的 `task_id` 作为 `original_model_task_id`，实现链式调用。

- **Qwen-MT-Uni 翻译**：提供同步与异步双模式。对大文档（≤200页）、长音频（3秒–60分钟）等高耗时输入，**必须设置 `X-DashScope-Async: enable` 头**，否则可能超时失败；异步响应返回 `task_id`，轮询 `/api/v1/tasks/{task_id}` 获取 `output.Data`（含 `TranslatedFileUrl` 或 `TranslatedTexts`）。

- **通用异步任务管理**：平台提供统一异步任务生命周期能力，包括任务提交（`async-generation` 路径）、状态查询、取消、HTTP 回调配置（`callback_url`）及结果拉取。任务默认保留 7 天，回调失败最多重试 3 次（间隔 1s/5s/15s）。

## 关键参数和配置

- **必需请求头**：
  - `X-DashScope-Async: enable` —— 所有异步接口的开关，缺失即报错（如视频、3D、Qwen-MT 异步模式）。
  - `Authorization: Bearer <API_KEY>` —— 地域需与模型 Endpoint 严格匹配（如华北2 的 Tripo 不接受华东1 Key）。
  - `Content-Type: application/json`

- **核心标识字段**：
  - `biz_id`：ParseX 独有，用于关联解析/抽取任务，全局唯一。
  - `task_id`：视频、3D、Qwen-MT、通用异步任务统一使用，24 小时有效（除通用任务默认 7 天）。

- **回调配置（可选但推荐）**：
  - `callback_url`：HTTPS 地址，需公网可达；任务完成时平台主动 POST 结果，避免轮询开销。
  - 需在请求体或独立接口中传入，详见 [配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。

- **轮询建议**：
  - 初始延迟：ParseX 建议首次查询延后 1–3 秒；3D 任务建议 ≥10 秒；视频任务 ≥5 秒。
  - 间隔策略：状态为 `PENDING`/`RUNNING` 时，建议 5–30 秒间隔；临近预期完成时间可缩短至 2–3 秒。
  - 终止条件：`task_status` 为 `SUCCEEDED` 或 `FAILED`，或 `status` 为 `success`/`failed`；不依赖 `output` 字段是否存在，而应以状态码为准。

- **错误处理关键点**：
  - `ParseResultNotReusable`（ParseX）：复用解析结果超 7 天窗口期。
  - `FileSizeExceeded`/`PageCountExceeded`：文件超限，需预检。
  - `FileDownloadTimeout`：可重试；`FileDownloadFailed`：不可重试，需修复 URL 权限。
  - `InvalidParameter`：常见于 `glossary` 格式错误、`domainHint` 非英文等。

面向开发者，请始终：  
✅ 显式添加 `X-DashScope-Async: enable` 头（除非明确使用同步模式）；  
✅ 用 `task_id`/`biz_id` 做幂等性控制，避免重复提交；  
✅ 实现带退避的轮询或优先配置 `callback_url`；  
✅ 根据文档明确的保留期（7天/24小时/30天）设计结果缓存与清理逻辑。

## 关联主题页

- [api overview](../api/api-overview.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [more about models](../api/more-about-models.md)


