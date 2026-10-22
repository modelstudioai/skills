# 异步任务

异步任务是百炼平台中用于处理耗时较长、无法在单次 HTTP 请求内完成的模型调用的标准模式。它将任务执行与结果获取解耦，通过“提交任务 → 获取唯一任务 ID → 轮询或接收事件通知 → 获取最终结果”四步流程实现可靠、可追踪、可扩展的长周期计算。

## 在百炼平台的不同场景中，这个概念如何使用

异步任务并非特定于某类模型，而是平台对**计算密集型、I/O 延迟高、资源调度复杂**能力的统一抽象。以下为典型使用场景：

- **图像生成**：`wan2.5-i2i-preview`（多图融合编辑）、`kling/*`（分镜组图）、`vidu/*`（高保真 UI/图表生成）、`wanx-style-repaint-v1`（人像风格重绘）等模型必须使用异步调用；任务创建后返回 `task_id`，需轮询 `GET /api/v1/tasks/{task_id}` 查询状态（`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`），`task_id` 有效期默认 24 小时。

- **视频生成**：所有视频模型（`kling`、`wanxiang`、`portrait-animation`、`vidu` 等）均强制异步。提交 `POST /api/v1/video-generation` 后获得 `job_id`，通过 `GET /api/v1/jobs/{job_id}` 查询状态；成功时返回 `output.video_url`（直链，有效期 24 小时）。

- **3D 生成**：Tripo 模型（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`）仅支持异步，且必须显式声明请求头 `X-DashScope-Async: enable`，否则直接报错；任务状态查询路径为 `GET /api/v1/tasks/{task_id}`，结果中的模型 URL（如 `pbr_model_url`）有效期仅 2 小时，需及时下载。

- **文档与音视频解析（ParseX）**：全部能力（PDF/Word 解析、ASR 转录、剧情摘要、字段抽取）均为异步。提交 `/parse/submit` 或 `/extract/submit` 后返回 `biz_id`，通过 `/parse/result` 或 `/extract/result` 查询；解析结果保留 30 天，但字段抽取复用的解析结果仅保留 7 天。

- **其他长耗时能力**：语音转写（`paraformer-16k-1`）、部分多模态理解（如大尺寸图像输入的 VL 模型）、定制化模型推理等，也统一纳入异步任务体系管理。

> ✅ **关键判断原则**：若模型文档明确标注“必须异步”、“不支持同步调用”、“需轮询 `task_id`”或要求设置 `X-DashScope-Async: enable`，即属于异步任务范畴。同步调用仅适用于毫秒级响应的轻量任务（如文本补全、向量嵌入）。

## 关键参数和配置

| 参数/配置 | 说明 | 示例/取值 | 注意事项 |
|-----------|------|------------|----------|
| `task_id` / `job_id` / `biz_id` | 任务唯一标识符，由提交接口返回，用于后续查询与管理 | `"a8532587-xxxx-xxxx-xxxx-0c46b17950d1"` | 所有异步任务的核心凭证；有效期依模型而定（常见为 24 小时），超期后查询返回 `UNKNOWN` 或 `TaskNotFound` |
| `X-DashScope-Async` | HTTP 请求头，显式启用异步模式 | `"enable"` | **3D 生成必需**；缺失将导致 `current user api does not support synchronous calls` 错误；其他模型通常通过 endpoint 或 model 名隐式启用 |
| `callback_url` | 可选回调地址，任务完成后平台主动推送 `POST` 通知 | `"https://your-server.com/webhook"` | 避免轮询限流（QPS ≤ 20），推荐用于生产环境；需自行实现幂等处理；支持 HTTP/HTTPS，不支持 localhost |
| `status` 字段 | 查询响应中的任务状态 | `"PENDING"`, `"RUNNING"`, `"SUCCEEDED"`, `"FAILED"`, `"CANCELED"` | 轮询时建议按任务类型设置间隔：图像/视频类 ≥15 秒，3D/解析类 ≥30 秒；持续 `RUNNING` 超 30 分钟应检查输入或联系支持 |
| 结果 URL 有效期 | 任务成功后返回的文件直链（如 `video_url`, `pbr_model_url`, `rendered_image_url`） | 通常为 **2 小时**（3D）、**24 小时**（图像/视频/ParseX） | **必须及时下载并持久化存储**；URL 过期后不可恢复，平台不提供续期接口 |

## 面向开发者，简洁实用

- **不要阻塞主线程**：永远避免在 Web 请求中同步等待异步任务完成。使用轮询（带退避）或事件回调。
- **轮询要节制**：QPS 限流 20，建议初始间隔 1–2 秒，随 `RUNNING` 时间增长逐步延长（如指数退避：1s → 2s → 4s → 8s）。
- **回调更可靠**：生产环境优先配置 `callback_url`，并在服务端验证 `X-DashScope-Signature` 签名防伪造。
- **ID 是生命线**：妥善保存 `task_id`/`job_id`/`biz_id`，它是查询、取消（仅 `PENDING` 状态支持）、审计的唯一依据。
- **URL 是临时凭证**：所有返回的文件 URL 均为临时直链，**禁止缓存、禁止长期引用、禁止前端直接展示**；务必在有效期内下载到自有存储（OSS、S3 等）。
- **错误要分类处理**：`FAILED` 状态需解析 `output.code` 和 `output.message`（参考[统一错误码文档](../../raw/model-api-reference/preparations/error-code.md)），区分 `InvalidParameter`（修复输入）、`ResourceNotReady`（重试）、`QuotaExhausted`（升配）等场景。
- **地域强绑定**：`task_id` 只能在创建时使用的地域 endpoint 上查询；跨地域调用 `GET /tasks/{id}` 必然失败。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)


