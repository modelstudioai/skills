# 异步处理

异步处理是百炼平台针对耗时较长的 AI 任务（如图像/视频/3D 生成、音视频解析、批量字段抽取等）提供的一种非阻塞调用模式：客户端提交请求后立即获得任务 ID，无需等待模型执行完成，而是通过轮询或事件回调方式获取最终结果。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：`qwen-image-3.0-pro`、`wan2.7-image-pro` 等高分辨率或复杂编辑任务默认需异步调用，必须在请求头中显式添加 `X-DashScope-Async: enable`，否则返回错误。
- **视频生成**：所有视频类模型（`kling`、`vidu`、`portrait-animation` 等）均强制异步，调用 `/v1/videos/generations` 返回 `task_id`，后续通过 `GET /v1/videos/generations/{id}` 轮询状态。
- **3D 生成**：Tripo 模型（`Tripo/Tripo-H3.1` 等）仅支持异步，且严格限定华北2（北京）地域，请求头必须含 `X-DashScope-Async: enable` 和地域匹配的 API Key。
- **音频类任务**：语音识别（ASR）、语音翻译（ST）等长音频处理推荐异步；而 TTS、音乐生成等支持同步/流式，异步非必需但可用于超长任务解耦。
- **文档与音视频解析（ParseX）**：全部接口强制异步，统一使用 `biz_id` 作为任务标识，适用于 PDF 解析、视频剧情摘要、结构化字段抽取等批量场景。
- **模型训练与微调**：虽未在当前材料中展开，但训练任务提交即计费、不可中断，天然符合异步语义，其生命周期管理（查询进度、获取模型地址）也采用相同任务 ID 机制。
- **大模型批量推理**：`test 1` 中明确支持“批量推理”，当输入样本量大或 `max_tokens` 较高时，建议切换为异步模式以避免 HTTP 超时（具体接口路径见对应模型文档）。

> ✅ 共性流程：**提交 → 获取 task_id/biz_id → 查询状态 → 获取结果**  
> ⚠️ 关键区别：图像/3D/视频类接口要求请求头强制启用异步；ParseX 类接口协议层即设计为异步；大模型类则按需选择同步或异步模式。

## 关键参数和配置

- **必需请求头**：
  - `X-DashScope-Async: enable`：所有显式异步接口的硬性要求，缺失将报错 `"current user api does not support synchronous calls"`。
  - `Authorization: Bearer <api_key>`：API Key 必须与调用地域一致（如北京地域需用北京生成的 Key）。

- **核心标识符**：
  - `task_id`：通用异步任务 ID（UUID v4 格式），由创建接口返回，用于轮询（如 `/api/v1/tasks/{task_id}`）或取消。
  - `biz_id`：ParseX 等应用级 API 使用的业务 ID，语义更贴近业务上下文（如 `"parseX-2026xxxx-xxxxxxx"`）。

- **轮询与回调配置**：
  - 建议轮询间隔 ≥15 秒（3D）、1–3 秒（ParseX）、≥5 秒（视频/图像），避免触发 QPS 限流（默认 20 RPS）。
  - 生产环境强烈推荐配置 [HTTP 回调或 RocketMQ 事件通知](../../raw/model-api-reference/more-about-models/async-task-api.md)，监听 `dashscope:System:AsyncTaskFinish` 事件，减少主动轮询开销。
  - 回调参数 `contain_result=true` 可在事件载荷中直接携带结果，省去一次查询调用。

- **生命周期约束（开发者必须关注）**：
  | 对象 | 有效期 | 说明 |
  |------|--------|------|
  | `task_id` / `biz_id` | 通常 24 小时 | 超期后查询返回 `UNKNOWN` 或 `ResultExpired` |
  | 下载 URL（如 `video_url`, `pbr_model_url`） | 2–24 小时不等 | 视模型而定，3D 模型为 2 小时，ParseX 为 30 天（结果本身），需及时下载 |
  | 临时文件（OSS URL） | 48 小时 | 由 [上传本地文件接口](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 生成，强绑定账号与模型 |

- **错误处理关键码**：
  - `ResultNotReady`（HTTP 409）：任务仍在排队或运行中，应继续轮询；
  - `TaskNotFound` / `UNKNOWN`：`task_id` 过期或不存在；
  - `InvalidParameter`：常见于异步场景下遗漏 `X-DashScope-Async` 头，或 `prompt`/`image`/`images` 互斥参数冲突。

## 面向开发者，简洁实用

- ✅ **立刻生效**：只要接口文档注明“支持异步”或要求 `X-DashScope-Async` 头，就可在 3 行代码内接入——加头、发 POST、轮询 GET。
- ✅ **规避超时**：HTTP 默认超时通常为 30–60 秒，而视频生成、3D 建模常需数分钟，异步是唯一可靠方案。
- ✅ **解耦架构**：前端提交后可立即响应用户，后端用消息队列或定时任务处理结果，提升系统健壮性。
- ❌ **切勿硬编码轮询**：高频短间隔轮询易被限流；务必用指数退避（如 1s→2s→4s）或改用事件回调。
- ❌ **勿忽略地域一致性**：API Key、Endpoint、Workspace ID、模型开通地域必须四者同地域，尤其图像/3D/视频类服务。
- 🛠️ **调试技巧**：用 `curl -v` 检查响应头 `X-Task-ID` 和状态码；生产环境开启 SDK 日志（如 DashScope Python SDK 的 `log_level=DEBUG`）跟踪任务流转。

## 关联主题页

- [test 1](../guides/test-1.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [audio api references](../api/audio-api-references.md)
- [more about models](../api/more-about-models.md)
- [api overview](../api/api-overview.md)


