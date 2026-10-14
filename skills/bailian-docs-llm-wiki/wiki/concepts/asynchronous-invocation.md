# 异步调用

异步调用是百炼平台对耗时较长模型任务（通常 >3 秒）采用的标准执行模式：客户端提交请求后立即返回任务标识（如 `task_id` 或 `biz_id`），不阻塞等待结果；后续通过独立查询接口或事件通知机制获取最终输出。该模式兼顾系统吞吐、资源利用率与调用稳定性，是图像生成、视频生成、3D 生成、长音频转写及文档/音视频解析等场景的强制或推荐方式。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成（T2I/I2I/编辑等）**：所有创意工具类模型（如 `wanx-style-repaint-v1`、`virtualmodel-v2`）及部分万相、可灵、Vidu 模型**强制异步**；千问图像系列支持同步/异步双模式，但高分辨率或多图生成建议使用异步以避免超时。
- **视频生成（T2V/I2V/人像驱动等）**：全部模型统一采用异步任务模型；提交 `POST /v1/videos/generate` 后需轮询 `GET /v1/tasks/{task_id}`，或配置 `callback_url` 接收 HTTP 回调。
- **3D 生成（Tripo）**：**完全强制异步**，必须在请求头中显式携带 `X-DashScope-Async: enable`，否则直接报错；不提供同步入口。
- **文档与音视频解析（ParseX）**：全链路基于异步任务模型，使用 `biz_id` 而非 `task_id` 作为任务标识；解析与字段抽取均需“提交 → 轮询”两阶段，且复用解析结果时需确保其在 7 天有效期内。
- **通用模型能力（如 ASR 长音频转写）**：虽未在各子文档详述，但明确归类于“耗时较长任务”，统一纳入异步任务管理体系，支持通过 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 统一查询、取消与批量管理。

> ✅ 共同特征：  
> - 所有异步任务均返回唯一、短期有效的任务 ID（`task_id` / `biz_id`）；  
> - 结果 URL（图像、视频、3D 模型、解析文件等）均为临时链接，有效期严格限定（常见为 2–24 小时）；  
> - 支持事件总线（EventBridge）或 HTTP 回调（`callback_url`）主动推送完成事件，**强烈推荐替代轮询**，避免 QPS 浪费与限流风险。

## 关键参数和配置

| 参数 / 配置项 | 说明 | 示例值 | 注意事项 |
|--------------|------|--------|----------|
| `X-DashScope-Async: enable` | **3D 生成必需请求头**，其他异步接口通常隐式启用，但显式声明更健壮 | `"enable"` | 缺失将导致 Tripo 调用失败；其他模型虽非强制，建议统一添加 |
| `callback_url` | 异步完成后的 HTTP 回调地址（POST） | `"https://your-server.com/webhook"` | 必须能被公网访问；需正确响应 HTTP 200；平台重试策略为指数退避（最多 3 次） |
| `task_id` / `biz_id` | 任务唯一标识符，用于查询、取消、下载 | `"task-abc123..."` | 有效期通常为 24 小时，超时后无法查询；请立即持久化存储 |
| 轮询间隔 | 建议最小查询间隔，避免触发限流 | T2I ≥5s，T2V ≥30s，3D ≥15s，ParseX 建议指数退避 | 单账号异步任务查询限流 **20 QPS**；高频轮询易被限流，优先用回调 |
| `status` 字段值 | 任务状态机标准值 | `"PENDING"`, `"RUNNING"`, `"SUCCEEDED"`, `"FAILED"`, `"CANCELED"` | 仅 `PENDING` 状态可取消；`SUCCEEDED` 时检查 `output` 或 `results` 字段获取结果 URL |

## 面向开发者，简洁实用

- ✅ **立刻上手**：调用异步接口（如 `ImageSynthesis.async_invoke`、`VideoGeneration.async_invoke`、`Tripo.async_invoke` 或 `/parse/submit`）→ 提取响应中的 `task_id`/`biz_id` → 用该 ID 调用 `fetch()`（SDK）或 `GET /api/v1/tasks/{id}`（HTTP）。
- ✅ **规避陷阱**：
  - 不要硬编码轮询频率——按模型类型设合理间隔（参考上表），生产环境务必启用 `callback_url`；
  - 临时结果 URL（如 `video_url`, `pbr_model_url`, `output.file_url`）**必须在有效期内下载并持久化**，过期即失效；
  - Tripo 调用**必须加 `X-DashScope-Async: enable` 头**，且仅限华北2（北京）地域；
  - ParseX 的字段抽取不可直连音视频，必须先解析再复用 `parsed_file_biz_id`。
- ✅ **最佳实践**：
  - 使用 SDK 的 `fetch()` / `list()` / `cancel()` 方法（Python/Java 均支持），比手写 HTTP 更安全；
  - 在回调服务中校验 `X-DashScope-Signature` 请求头签名，确保事件来源可信；
  - 任务失败时，优先检查 `error.code`（如 `invalid_input`, `quota_exhausted`, `model_unavailable`），而非仅看 HTTP 状态码；
  - 高并发场景下，禁用临时文件上传（`Files.upload`），改用客户自有 OSS + `oss://` URL 直传。

> 💡 提示：所有异步任务均可通过 [统一异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 进行跨模型批量操作（如按时间范围、状态、模型名筛选），无需为每个模型单独对接。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)


