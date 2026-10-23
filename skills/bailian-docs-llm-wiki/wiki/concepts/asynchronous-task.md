# 异步任务

异步任务是百炼平台为处理长耗时、高资源消耗的模型调用而设计的核心执行范式，适用于图像生成、视频合成、3D建模、文档/音视频解析、大文件翻译等无法在秒级内完成的场景。它将任务提交与结果获取解耦，通过唯一 `task_id` 实现状态跟踪与结果拉取，避免客户端长时间阻塞和连接超时。

## 在百炼平台的不同场景中，这个概念如何使用

异步任务是以下能力的统一执行机制：

- **图像生成**：万相 2.5 编辑、可灵（Kling）、Vidu、FaceChain 训练等模型必须使用异步模式；调用 `POST /api/v1/services/aigc/image-synthesis/generation` 后返回 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 获取图像 URL（有效期通常为 24 小时）。
- **视频生成**：所有视频模型（HappyHorse、万相 2.7/3.0、PixVerse、Kling、Vidu 等）强制要求异步调用，且必须在请求头中显式设置 `X-DashScope-Async: enable`，否则报错；任务创建后需轮询 `GET /api/v1/tasks/{task_id}`，推荐间隔 ≥3 秒。
- **3D 生成**：Tripo-3D 模型仅支持异步，调用 `/v1/models/tripo-3d-generation:generate` 返回 `task_id`，轮询结果接口返回 `.glb` 文件下载地址（有效期 24 小时）。
- **文档与音视频解析（ParseX）**：所有解析与字段抽取任务均基于异步模型，提交 `/parse/submit` 或 `/extract/submit` 返回 `biz_id`（等效于 `task_id`），后续通过 `/parse/result` 或 `/extract/result` 查询结构化结果。
- **机器翻译（Qwen-MT-Uni）**：对大文档（≤200 页）或长音频（>60 分钟）等耗时场景，需添加 `X-DashScope-Async: enable` 头启用异步模式，响应中返回 `task_id`，轮询获取 `TranslatedFileUrl`。
- **通用任务管理**：所有异步任务统一由 `/api/v1/tasks` 系列 API 管理，支持查询单个任务、批量列表（`GET /api/v1/tasks?status=...`）及取消（仅限 `PENDING` 状态）。

> ✅ **最佳实践**：  
> - 避免高频轮询（如 <1s），推荐图像类间隔 ≥1s、视频/3D/解析类 ≥3s；  
> - 生产环境优先配置事件总线（HTTP 回调或 RocketMQ），监听 `dashscope:System:AsyncTaskFinish` 事件，减少轮询开销与限流风险；  
> - `task_id` 有效期统一为 **24 小时**（部分旧文档提及 300 秒为单次请求超时，非任务生命周期），过期后无法查询结果。

## 关键参数和配置

| 参数 | 说明 | 示例/约束 |
|------|------|-----------|
| `task_id`（或 `biz_id`） | 任务全局唯一标识符，UUID 格式字符串，用于所有后续查询与操作 | `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` |
| `X-DashScope-Async: enable` | **必需请求头**（视频、Qwen-MT-Uni 异步等场景显式要求） | 字符串字面量 `"enable"`，大小写敏感 |
| `status` 字段（响应体） | 任务当前状态，用于轮询判断是否完成 | 常见值：`PENDING`（排队中）、`RUNNING`（执行中）、`SUCCESS` / `SUCCEEDED`（成功）、`FAILED`（失败） |
| `output.*` 字段（成功时） | 最终结果载体，结构因模型而异 | 图像：`output.image_url`；视频：`output.video_url`；3D：`output.model_url`；解析：`output.result_json`；翻译：`output.Data.TranslatedFileUrl` |
| `error.code`（失败时） | 结构化错误码，用于精准重试或告警 | 如 `CONTENT_POLICY_VIOLATION`、`TIMEOUT`、`INVALID_INPUT`、`FILE_DOWNLOAD_FAILED` |

> ⚠️ 注意：  
> - 异步任务不支持 Webhook 主动推送（除事件总线外），也**不支持批量提交同一任务**——重复请求会生成新 `task_id`，结果不保证一致；  
> - 所有异步任务的输入资源（如 `file_url`、`image_url`）必须为公网可访问 HTTPS 地址；若使用 OSS 临时 URL，请求头须额外添加 `X-DashScope-OssResourceResolve: enable`；  
> - 任务创建与结果查询必须使用**同一地域、同一业务空间的 API Key 和 Endpoint**，跨地域或混用密钥将导致 401/404 错误。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


