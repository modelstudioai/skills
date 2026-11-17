# 异步任务

异步任务是百炼平台对耗时较长、无法即时返回结果的模型调用所采用的标准执行范式：用户提交请求后立即获得唯一任务标识（如 `task_id` 或 `biz_id`），随后通过轮询或事件回调方式获取最终结果，避免长连接阻塞与超时风险。

## 在百炼平台的不同场景中，这个概念如何使用

异步任务是百炼多模态与重计算类能力的统一调度机制，广泛应用于以下核心场景：

- **视频生成**（Video Generation）：所有文生视频、图生视频、参考生视频等接口均强制异步。需携带 `X-DashScope-Async: enable` 请求头，创建任务后通过 `GET /api/v1/tasks/{task_id}` 轮询状态，典型处理时长为数秒至数分钟。
- **文档与音视频解析**（ParseX）：结构化解析（PDF/Word/MP4/MP3 等）和字段抽取均基于 `biz_id` 实现异步解耦。任务提交后，结果在 30 天内可查（解析结果）或 7 天内复用（抽取依赖）。
- **3D 内容生成**（Tripo）：全链路 3D 任务（网格生成、高斯泼溅、重拓扑、贴图、动画绑定）仅支持异步，且**严格限定华北2（北京）地域**；`task_id` 有效期为 24 小时，需在此窗口内完成轮询。
- **多模态翻译**（Qwen-MT-Uni）：提供同步/异步双模式。大文档（≤200页）、长音频（>60分钟）或高保真格式重构必须启用异步；小文本/短文件可选同步，但异步仍是生产环境推荐路径。
- **通用多模态任务**（如文生图、语音转写、微调模型推理等）：默认采用异步机制，可通过 `/api/v1/tasks` 系统接口统一管理、批量查询与事件订阅，支持 HTTP 回调或 RocketMQ 推送。

> ✅ 共性特征：所有异步任务均返回唯一 ID（`task_id` 或 `biz_id`），状态机统一为 `init → processing → success/failed`；失败时附带标准错误码与可操作提示；结果保留期明确（24h–30d），超期自动清理。

## 关键参数和配置

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `X-DashScope-Async` | Header 字符串 | **是**（多数场景） | 必须设为 `enable`，否则返回 `"current user api does not support synchronous calls"` 错误。部分模型（如 Qwen-MT-Uni）支持同步/异步双模式，但视频、3D、ParseX 等强制启用。 |
| `task_id` / `biz_id` | 响应体字符串 | — | 创建任务成功后返回的唯一标识，用于后续轮询或事件溯源；大小写敏感，有效期依服务而定（常见 24 小时）。 |
| `polling interval` | 客户端控制 | 推荐 | 首次轮询建议延迟 5–10 秒，后续间隔 15–30 秒；高并发场景请实现指数退避（如 `min(2^N * 1s, 60s)`），避免触发限流（默认 20 QPS）。 |
| `callback_url`（事件驱动） | 请求体字符串 | 否 | 通过事件总线配置 HTTP 回调地址，任务完成后主动推送 `dashscope:System:AsyncTaskFinish` 事件，替代轮询。需自行实现幂等处理。 |

> ⚠️ 注意事项：
> - 所有异步任务的输入资源（如 `file_url`、`image_url`）必须可公开访问（HTTPS，无中文路径，无鉴权跳转）；
> - 使用临时 OSS URL 时，必须同时传入 `X-DashScope-OssResourceResolve: enable` 请求头；
> - `task_id` 不可重用，重复轮询同一 ID 不计费，但超期后返回 `TaskNotFound`；
> - 不要重提相同请求——`ResultNotReady` 表示任务进行中，应继续轮询，而非新建任务。

## 面向开发者，简洁实用

- **快速起步**：只需两步  
  ① `POST /.../submit` + `X-DashScope-Async: enable` → 得到 `task_id`；  
  ② `GET /api/v1/tasks/{task_id}` → 检查 `status` 字段，循环直到 `success` 或 `failed`。

- **生产建议**：  
  ✅ 优先使用事件回调（EventBridge + HTTP/RocketMQ），降低轮询开销与延迟；  
  ✅ 对 `task_id` 做本地缓存+过期标记，避免无效轮询；  
  ✅ 失败时检查 `code`（如 `FileSizeExceeded`, `ProcessingTimeout`, `ParseResultNotReusable`）并按[错误码文档](../../raw/application-api-reference/api-overview/errors.md)针对性修复；  
  ❌ 禁止在前端硬编码 API Key 发起异步任务——应由后端代理并签发短期 [Token](token.md)。

- **调试技巧**：  
  使用百炼 CLI 快速验证：`bl async task result --task-id <id>`；  
  开启 `curl -v` 查看响应头 `X-RateLimit-Remaining`，监控配额；  
  所有异步任务日志可在控制台「任务中心」按时间/模型/状态筛选追溯。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [api overview](../api/api-overview.md)
- [3d generation](../api/3d-generation.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [more about models](../api/more-about-models.md)


