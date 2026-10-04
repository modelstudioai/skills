# 异步处理

异步处理是百炼平台对长耗时任务（如图像/视频/3D生成、语音转写、知识库同步等）采用的核心执行模式：调用方提交任务后立即返回唯一 `task_id`，不阻塞等待结果；实际计算在后台异步执行，结果通过轮询或事件通知方式获取。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：`wan2.7-image-pro`、`aitryon-plus` 等模型默认仅支持异步调用。需在请求头中显式设置 `X-DashScope-Async: enable`，否则报错；创建任务后通过 `GET /api/v1/tasks/{task_id}` 查询状态，成功时返回带 24 小时有效期的图片 URL。

- **视频生成**：所有视频模型（HappyHorse、万相、PixVerse、EMO 等）**强制异步**。HTTP 请求必须携带 `X-DashScope-Async: enable`，否则直接拒绝；任务生命周期为 24 小时，建议轮询间隔 ≥15 秒，或配置事件总线监听 `dashscope:System:AsyncTaskFinish` 事件实现零轮询。

- **3D 生成**：Tripo 模型（`Tripo/Tripo-H3.1` 等）仅支持异步，且**严格限定华北2（北京）地域**。同样依赖 `X-DashScope-Async: enable` 请求头，结果中的 GLB 模型 URL 有效期仅 2 小时，需及时下载。

- **语音与多模态模型**：`paraformer-8k-v1`（语音转写）、`qwen-vl-plus`（多模态理解）等长耗时模型均归入异步任务体系，统一由 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 管理状态、取消和批量查询。

- **RAG 知识库同步**：文档上传后的解析与切片（chunking）为异步过程，调用 `/v1/knowledge_bases/{kb_id}/sync` 后返回任务 ID，需轮询同步状态直至 `status=completed` 才可发起问答；该异步流程独立于问答接口本身（问答为同步调用）。

> ✅ 共性原则：  
> - 所有异步任务均返回标准 `task_id`（UUID 格式），全局唯一，有效期 24 小时；  
> - **绝不重试相同请求体**——重复提交将创建新任务，而非覆盖旧任务；  
> - 推荐优先使用**事件驱动方案**（HTTP 回调或 RocketMQ），避免轮询资源浪费；轮询接口有 20 QPS 限流，高频场景务必接入事件总线。

## 关键参数和配置

| 参数/配置项 | 说明 | 必填性 | 示例值 | 注意事项 |
|-------------|------|--------|--------|----------|
| `X-DashScope-Async` | HTTP 请求头，启用异步模式 | **必填**（对所有异步模型） | `"enable"` | 值必须为字符串 `"enable"`（区分大小写），缺失或设为 `"disable"` 将报错 |
| `task_id` | 异步任务唯一标识符 | 返回值（非输入） | `"a8532587-xxxx-xxxx-xxxx-0c46b17950d1"` | 用于后续查询、取消；24 小时内有效；不可用于跨地域查询 |
| `GET /api/v1/tasks/{task_id}` | 单任务状态查询接口 | 轮询时使用 | — | 响应含 `status`（`PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`）、`results`（成功时含结果 URL）、`error`（失败时含错误码） |
| `GET /api/v1/tasks` | 批量任务查询接口 | 可选 | `?status=SUCCEEDED&model_name=qwen-vl-plus&start_time=2025-04-01T00:00:00Z` | 支持按状态、模型名、时间范围过滤；适用于运维监控或批量重试 |
| 事件总线规则 | 配置 `dashscope:System:AsyncTaskFinish` 事件监听 | 推荐启用 | HTTP 回调地址 或 RocketMQ Topic | 事件体包含 `task_id`、`model`、`status`、`result_url` 等字段；实时性高，无轮询开销 |

> ⚠️ 重要提醒：  
> - 临时文件（如 `qwen-vl-plus` 的图片 URL）与异步任务解耦，但调用时仍需额外请求头 `X-DashScope-OssResourceResolve: enable`；  
> - 子业务空间调用异步 API 时，`base_url` 必须包含 WorkspaceId 和正确地域（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），否则任务创建失败；  
> - 所有异步结果 URL（图片、视频、GLB、预览图等）均有明确有效期（2–24 小时不等），请在响应中读取并及时持久化。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [rag api](../api/rag-api.md)


