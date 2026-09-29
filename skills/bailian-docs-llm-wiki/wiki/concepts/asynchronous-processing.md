# 异步处理

异步处理是百炼平台对长耗时 AI 任务（如图像/视频/3D生成、音视频解析、字段抽取等）采用的核心调用范式：客户端发起请求后立即返回任务标识（如 `task_id` 或 `biz_id`），不阻塞等待结果；后续通过轮询或事件通知方式获取最终输出。该模式显著提升系统吞吐与资源利用率，是生产环境中处理高延迟、高计算开销任务的标准实践。

## 在百炼平台的不同场景中，这个概念如何使用

异步处理在百炼平台覆盖多个关键能力域，统一遵循“提交任务 → 获取标识 → 获取结果”三阶段流程，但具体实现和适配细节因场景而异：

- **多模态生成类**（图像、视频、3D）：  
  所有万相（WanX）、爱诗（PixVerse）、HappyHorse、Kling、Vidu 及 Tripo 等长耗时模型均**强制异步**。例如调用 `wan2.7-image-pro` 文生图或 `Tripo/Tripo-H3.1` 单图生3D 时，必须在请求头中显式设置 `X-DashScope-Async: enable`，否则直接报错。创建成功后返回 `task_id`，用于后续查询。

- **结构化解析与抽取类**（ParseX）：  
  文档解析（PDF/Word/PPT/图片）、音视频解析（MP4/AVI/音频）及基于 Schema 的字段抽取，全部采用异步模式。提交 `/parse/submit` 或 `/extract/submit` 后返回 `biz_id`，通过 `/parse/result` 或 `/extract/result` 轮询状态。注意：音视频无法直接用于抽取，需先解析为文本再复用其 `biz_id`。

- **语音与专业工具类**：  
  语音转写（`paraformer-16k-1`）、数字人驱动（`wan2.2-s2v`, `EMO`, `LivePortrait`）、视频编辑、风格重绘等能力，同样归入异步任务体系，统一由 `/api/v1/tasks/{task_id}` 接口管理生命周期。

- **同步 vs 异步的边界清晰**：  
  平台按模型类型和预期耗时自动划分——`qwen-plus`、`qwen-vl-plus` 等轻量文本模型默认同步；而所有图像/视频/3D/语音/解析类任务，无论是否标为“turbo”，只要平均响应超 30 秒，即强制异步。开发者无需自行判断，只需依据[各模型文档](../../raw/model-api-reference/)明确标注的调用模式选择对应 SDK 方法或 HTTP 头配置。

## 关键参数和配置

| 参数 | 说明 | 典型值/约束 | 使用场景 |
|------|------|-------------|----------|
| `task_id` / `biz_id` | 异步任务唯一标识符，全局唯一、大小写敏感，有效期通常为 **24 小时**（部分服务如 ParseX 解析结果保留 30 天） | UUID 格式字符串（如 `task-abc123def456`） | 所有异步任务查询、取消、结果拉取的必需凭证 |
| `X-DashScope-Async` | HTTP 请求头，**强制启用异步模式的开关**。缺失或值非 `"enable"` 将导致调用失败 | `"enable"`（字符串，区分大小写） | 图像、视频、3D、部分语音模型的 POST 创建请求必填 |
| `expire_in_seconds` | 临时 API Key 有效期（秒），用于前端直传等不可信环境 | `[1, 1800]`，默认 `60` | 生成临时凭证时指定，与异步任务本身无关，但常配合文件上传流程使用 |
| 轮询间隔与频次 | 避免触发限流的关键实践参数 | 建议 ≥15 秒；单账号 QPS ≤20（含批量查询 `/api/v1/tasks`） | 所有轮询场景，尤其在高并发批量任务中需主动退避 |
| 回调配置（EventBridge） | 替代轮询的事件驱动方案，需提前在阿里云控制台配置 | HTTP Endpoint（支持 HTTPS）或 RocketMQ Topic | 推荐用于生产级任务编排，规避轮询资源消耗与限流风险 |

> ⚠️ 注意：异步任务结果中的下载链接（如 `pbr_model_url`、`rendered_image_url`、`output_file_url`）通常**有效期仅 2 小时**，请务必及时保存至自有存储。

## 面向开发者，简洁实用

- ✅ **必做**：调用异步模型前，确认模型文档是否标注“异步”或要求 `X-DashScope-Async: enable`；创建请求后立即持久化 `task_id`/`biz_id`，勿依赖内存缓存。
- ✅ **推荐**：优先采用 [EventBridge 事件回调](https://help.aliyun.com/zh/eventbridge/product-overview/what-is-eventbridge) 接收 `dashscope:System:AsyncTaskFinish` 事件，而非轮询——降低客户端复杂度与服务端压力。
- ✅ **避坑**：  
  - 不要高频轮询（<15 秒间隔）；  
  - 不要复用过期的 `task_id`（24h 后状态变为 `UNKNOWN`）；  
  - 文件上传时指定的 `model_name` 必须与后续调用模型**完全一致**；  
  - 异步任务结果链接（URL）需在 2 小时内下载，过期不可恢复。
- ✅ **调试技巧**：使用 `curl -v` 或 Postman 查看响应头 `X-Request-ID` 和状态码（如 `409 ResultNotReady` 表示仍在处理），结合 [错误码文档](../../raw/application-api-reference/api-overview/errors.md) 快速定位问题。

异步不是“更慢”，而是“更稳、更可扩展”。合理运用，即可支撑每秒数百任务的稳定调度。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [image generation](../api/image-generation.md)


