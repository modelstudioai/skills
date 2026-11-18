# 异步任务处理

异步任务处理是百炼平台对耗时型 AI 操作（如视频生成、3D 建模、长音频转写、文档解析等）的标准执行范式：用户通过一次请求提交任务，获得唯一 `task_id`，再通过独立查询接口轮询或事件通知方式获取最终结果，避免阻塞式等待与超时风险。

## 在百炼平台的不同场景中，这个概念如何使用

异步任务处理是以下核心能力的统一基础设施：

- **视频生成（Video Generation）**：所有文生/图生/参考生视频、动作迁移、口型同步等均强制异步。必须携带 `X-DashScope-Async: enable` 请求头，否则返回明确错误；任务创建后需轮询 `/api/v1/tasks/{task_id}`，直至状态为 `"SUCCESS"`，结果包含 `output.video_url` 等字段。

- **文档与音视频解析（ParseX）**：`/parse/submit` 和 `/extract/submit` 接口均返回 `biz_id`（逻辑任务 ID），开发者需周期性调用 `/parse/result` 或 `/extract/result` 查询状态（`processing` / `success` / `failed`）。注意：解析结果保留 30 天，抽取复用结果仅限 7 天内。

- **3D 内容生成（Tripo）**：全部接口（包括文生网格、图生 Gaussian Splatting、重拓扑、贴图生成等）仅支持异步，且**严格限定华北2（北京）地域**。`task_id` 有效期为 24 小时，首次轮询建议延迟 10 秒，后续间隔推荐 15–30 秒。

- **非实时音频处理（Audio API）**：长音频 ASR（如 `qwen-audio-asr-filetrans`）、批量 TTS、音视频翻译等均提供异步路径。ASR 异步任务必须设置 `X-DashScope-Async: enable`；TTS 异步任务则通过 `model` 后缀（如 `-async`）或参数显式标识。

- **通用模型调用扩展**：通过 `/api/v1/tokens` 获取临时凭证、多模态文件上传绑定模型、子业务空间调用等高级能力，均以异步任务为底层载体。SDK 中对应方法如 `client.images.jobs.create()`、`client.audio.asr.filetrans.create()` 等，均返回 `task_id` 并要求后续 `fetch()`。

> ✅ **最佳实践**：优先采用**事件驱动通知**（HTTP 回调或 RocketMQ 订阅 `dashscope:System:AsyncTaskFinish` 事件），而非高频轮询；若必须轮询，请将频率控制在 ≤20 QPS，并实现指数退避策略。

## 关键参数和配置

| 参数 | 位置 | 是否必填 | 说明 |
|------|------|----------|------|
| `X-DashScope-Async` | HTTP Header | 是（除部分 TTS/ASR 同步接口外） | 值必须为 `"enable"`，缺失或错误值将导致 `400 Bad Request`（错误信息含 `"does not support synchronous calls"`） |
| `task_id` / `biz_id` | 响应体（创建接口） + 路径/Query（查询接口） | 是 | 全局唯一任务标识符（UUID 格式），有效期统一为 **24 小时**（ParseX 的 `biz_id` 为 30 天，但查询接口行为一致） |
| `region` 与 `WorkspaceId` | 请求 URL（域名） | 是 | 必须与 API Key 所属地域和业务空间完全匹配；跨地域调用（如用北京 Key 调新加坡 Endpoint）将直接失败 |
| `Authorization: Bearer <API_KEY>` | HTTP Header | 是 | 使用环境变量 `DASHSCOPE_API_KEY` 注入，严禁硬编码 |

> ⚠️ 注意：  
> - 所有异步任务均不支持取消（Cancel）操作；  
> - 任务超时或失败后，`task_id` 不可重用，需重新提交；  
> - 部分模型（如 Tripo、早期万相）存在路径差异（如 `/video-generation/` vs `/3d-generation/`），请严格按模型文档指定路径调用。

## 面向开发者，简洁实用

- **不要写轮询死循环**：使用带 jitter 的指数退避（例如：初始 1s → 2s → 4s → 8s → 最大 30s），并在 `status == "failed"` 时立即终止。
- **检查错误码再重试**：常见失败原因包括 `FileFormatNotSupported`（400）、`FileSizeExceeded`（400）、`ServiceQuotaExhausted`（503）、`AccountOverdue`（403），需针对性处理而非盲目重试。
- **结果解析看 `output` 字段**：成功响应中，结构化结果通常位于 `data.output`（ParseX）或 `output.results`（通用模型 SDK），视频/3D/音频文件 URL 统一在 `output.*_url` 下（如 `output.video_url`, `output.model_url`, `output.audio_url`）。
- **本地开发调试建议**：用 `curl -v` 验证请求头与响应；生产环境务必启用 HTTPS 和连接池复用（Java 设置 `connectionPoolSize=256`，Python 传入自定义 `httpx.AsyncClient`）。
- **安全红线**：API Key 必须通过环境变量注入；临时文件（OSS URL）仅限 48 小时，禁止用于生产长期存储。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [api overview](../api/api-overview.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)
- [audio api directory](../api/audio-api-directory.md)


