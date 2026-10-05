# 异步处理

异步处理是百炼平台中用于应对长耗时任务的核心调用模式：客户端提交任务后立即返回唯一任务标识（如 `task_id` 或 `biz_id`），不阻塞等待结果；后续通过轮询或事件通知方式获取最终输出。该模式适用于计算密集、I/O 延迟高或资源调度周期长的 AI 任务，保障接口响应性与系统吞吐能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成（`/video-generation/`）**：所有视频类 API（文生视频、图生视频、人像驱动等）强制异步。提交后返回 `task_id`，任务执行耗时通常为 1–5 分钟，`task_id` 有效期为 24 小时。必须携带请求头 `X-DashScope-Async: enable`，否则报错。

- **文档与音视频解析（`/parse/submit`、`/extract/submit`）**：ParseX 全系列解析与抽取任务均采用异步流程。提交后返回 `biz_id`，结果默认保留 30 天（抽取复用需在 7 天内）。轮询接口为 `/parse/result` 或 `/extract/result`，状态字段为 `data.status`（`processing` / `success` / `failed`）。

- **图像生成（部分模型）**：非低延迟图像任务（如图像编辑、扩图、AI试衣、风格重绘等）需异步调用。例如 `wanx-style-repaint-v1`、`image-out-painting` 等模型，流程与视频一致：`POST` 创建任务 → 获取 `task_id` → `GET /api/v1/tasks/{task_id}` 查询结果。

- **语音转写、多模态长任务等**：如 `paraformer-16k-1`（语音识别）、`qwen-vl-plus` 配合大图/长视频输入等场景，当预估处理时间 >2 秒时，平台自动或推荐启用异步模式，统一纳入 `/api/v1/tasks/` 任务管理体系。

> ✅ 共同特征：  
> - 所有异步任务均通过统一任务管理接口 `GET /api/v1/tasks/{task_id}` 查询状态；  
> - 支持批量查询 `GET /api/v1/tasks?status=success&model=wan3.0&start_time=...`；  
> - 推荐搭配事件驱动（EventBridge）接收 `dashscope:System:AsyncTaskFinish` 事件，替代轮询以降低延迟与请求开销。

## 关键参数和配置

| 参数/配置 | 说明 | 必填性 | 示例值 |
|-----------|------|--------|--------|
| `X-DashScope-Async` 请求头 | 启用异步模式的开关，缺失将直接拒绝请求 | ✅（对异步模型强制要求） | `"enable"` |
| `task_id` / `biz_id` | 任务唯一标识符，由创建接口返回，用于结果查询与生命周期管理 | ✅（轮询必需） | `"task-20240520-abc123def456"` |
| 轮询间隔建议 | 避免高频轮询触发限流（默认 20 QPS），按任务类型差异化设置 | ⚠️（实践建议） | 文本类 ≥1s，图像类 ≥3s，视频类 ≥10s |
| 事件回调配置 | 在控制台配置 HTTP 回调地址或 RocketMQ Topic，接收任务完成事件 | ❌（可选，推荐生产环境启用） | `https://your-domain.com/webhook/async` |
| 任务保留期 | `task_id` 有效时长，超期后无法查询结果 | — | 视服务而定：视频类 24 小时，解析类 30 天 |

## 面向开发者，简洁实用

- ✅ **第一步：确认模型是否支持异步**  
  查阅对应模型文档 — 若明确要求 `X-DashScope-Async: enable` 或描述为“异步调用”，则不可使用同步方式。

- ✅ **第二步：构造请求**  
  - 请求头必加：`Authorization: Bearer <API_KEY>` + `X-DashScope-Async: enable`；  
  - 请求体按模型规范传 `input` 和 `parameters`；  
  - 使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），确保地域一致。

- ✅ **第三步：获取并消费结果**  
  - 成功响应含 `task_id` → 立即开始轮询或注册事件监听；  
  - 轮询时检查 `status` 字段：`"SUCCESS"` 表示就绪，`"FAILED"` 时读取 `error_code` 和 `error_message`；  
  - 成功结果中关键字段因服务而异：`output.video_url`（视频）、`result.url`（图像）、`extract_result_json`（抽取）、`segments`（音视频解析）。

- ⚠️ **避坑提示**  
  - 不要跨地域混用 API Key、Endpoint 和模型；  
  - 不要硬编码永久 API Key 到前端；高并发场景请调大 SDK 连接池（Java 默认 32，Python `aiohttp` 默认 100）；  
  - 异步任务不支持取消，失败任务需重试新任务。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)


