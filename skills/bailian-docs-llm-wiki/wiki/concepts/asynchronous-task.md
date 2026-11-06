# 异步任务

异步任务是百炼平台中用于处理耗时较长、无法在毫秒级内完成的模型推理或数据处理操作的核心执行范式。它通过“提交任务 → 获取唯一任务标识 → 轮询或接收事件通知获取结果”的两阶段流程，解耦请求与响应，保障服务稳定性与资源利用率。

## 在百炼平台的不同场景中，这个概念如何使用

异步任务是以下四类高计算开销能力的**默认且强制的调用方式**：

- **图像生成**：适用于 `wan2.5-i2i-preview`、`kling/*`、`vidu/*` 及所有垂直创意工具（如虚拟模特、海报生成、FaceChain 写真、图像擦除补全等），典型耗时 1–2 分钟；同步模型（如 `qwen-image-3.0`）虽支持同步调用，但当任务复杂度升高（如多图参考+高分辨率输出）时，平台也可能自动降级为异步执行。
- **视频生成**：**全部模型统一采用异步模式**，包括 HappyHorse、万相（WanX 2.7+/3.0）、PixVerse、Vidu、Kling、MiniMax 等，因视频合成涉及帧间一致性建模与大规模渲染，耗时通常为数十秒至数分钟。
- **文档与音视频解析（ParseX）**：所有解析（PDF/Word/MP4/MOV 等）和结构化字段抽取均必须异步提交，任务状态通过 `biz_id` 查询，结果保留期严格区分（解析结果 30 天，抽取复用结果仅限 7 天）。
- **3D 生成（Tripo）**：从文/图生 3D 网格、Gaussian Splatting 到后处理（分割、贴图、重拓扑、动画绑定）全流程均为异步，且**仅支持华北2（北京）地域**，`task_id` 有效期统一为 24 小时。

> ✅ 共同特征：所有异步任务均返回一个全局唯一、短期有效的任务标识（`task_id` 或 `biz_id`），开发者需主动轮询其状态或配置事件回调，不可直接等待 HTTP 响应体返回最终结果。

## 关键参数和配置

- **必需请求头**：
  - `X-DashScope-Async: enable` —— 必须显式设置，否则返回 `"current user api does not support synchronous calls"` 错误（视频、3D、ParseX 等接口强制校验）。
  - `Authorization: Bearer <API_KEY>` —— API Key 必须与 Endpoint 地域严格一致（如华北2 的 Key 不能调用新加坡 endpoint）。

- **任务标识生命周期**：
  - `task_id`（图像/视频/3D）：有效期 **24 小时**，超时后 `GET /api/v1/tasks/{task_id}` 返回 `404` 或 `TaskNotFound`。
  - `biz_id`（ParseX）：解析任务与抽取任务各自独立，有效期分别为 **30 天** 和 **7 天**（仅对复用场景有效）。

- **轮询建议**：
  - 初始延迟：首次查询建议延后 **5–10 秒**（避免任务尚未入队）；
  - 间隔策略：图像/3D 类任务推荐 **15–30 秒**；视频/ParseX 类可放宽至 **30–60 秒**；
  - 限流规避：所有 `/api/v1/tasks/{task_id}` 接口受 **20 QPS（主账号维度）限流**，高频轮询易触发 `429 Too Many Requests`，应避免短于 50ms 的密集请求。

- **替代方案（推荐）**：
  - 使用 **EventBridge HTTP 回调** 或 **RocketMQ 订阅** 接收 `dashscope:System:AsyncTaskFinish` 事件，实现零轮询、低延迟、抗限流的结果获取；
  - 回调事件体包含 `task_id`、`task_status`（`SUCCEEDED`/`FAILED`）、`output`（含 `video_url`/`model_url`/`parsed_result_url` 等）及错误详情。

## 面向开发者，简洁实用

- ✅ **不要**在代码中写死 `sleep(1000)` 后直接读响应体——异步任务永远返回轻量级任务创建响应（含 `task_id`），结果需另行获取。
- ✅ **务必校验地域一致性**：API Key、Endpoint URL、业务空间 ID（`{WorkspaceId}`）三者必须同属一个地域（华北2/新加坡/弗吉尼亚等），跨地域调用必然失败。
- ✅ **优先启用事件回调**：比轮询更可靠、更省资源，尤其适合生产环境；轮询仅建议用于调试或低频集成场景。
- ❌ **不要复用过期的 `task_id` 或 `biz_id`**：24 小时/7 天/30 天后失效，需重新提交任务。
- ❌ **不要忽略 `X-DashScope-Async` 头**：视频、3D、ParseX 等接口缺失该头将直接报错，无降级选项。

如需快速验证，可使用 CLI 工具（如 `bl image generate --async`、`bl parsex parse submit`）或 SDK 中的 `async_generate()` / `submit_task()` 方法，它们已封装任务创建与状态管理逻辑。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [api overview](../api/api-overview.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)


