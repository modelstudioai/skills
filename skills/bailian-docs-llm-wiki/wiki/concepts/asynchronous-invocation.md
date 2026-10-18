# 异步调用

异步调用是指客户端发起请求后不等待服务端即时返回结果，而是立即获得一个任务标识（如 `task_id`），后续通过轮询或回调机制获取最终执行结果的通信模式。该模式适用于计算耗时长、I/O 密集型或资源受限的任务，可显著提升客户端响应性与系统吞吐能力。

## 在百炼平台的不同场景中如何使用

- **图像生成**：多数图像模型（如 `qwen-image-*`、`wan2.*`、`kling`、`vidu`）同时支持同步与异步调用。当请求参数中显式设置 `X-DashScope-Async: enable` 请求头时，API 将返回 `202 Accepted` 及 `task_id`，开发者需调用 `/tasks/{task_id}` 接口轮询状态；未设置该头则走同步路径（阻塞等待，超时默认 120 秒）。注意：OpenAI 兼容模式（如 `/v1/images/generations`）仅支持同步调用。

- **视频生成**：**全部视频类 API 强制异步**。必须在请求头中设置 `X-DashScope-Async: enable`，否则返回 400 错误。调用成功后返回 `task_id` 和 `status: "QUEUED"`，需持续调用 `GET /tasks/{task_id}` 获取状态（`RUNNING` → `SUCCEEDED` 或 `FAILED`），结果包含视频 URL、时长、帧率等元信息。典型流程为「创建任务 → 轮询 → 下载/播放」。

- **世界模型**：Adventure 和 Directing 子系统仅支持同步调用（RESTful，`200 OK` 直接返回结果）；而 Acting 子系统因需低延迟[流式输出](streaming-output.md)，**强制使用 WebSocket 长连接**，属于事件驱动型异步通信，不依赖 `task_id` 轮询，而是按 SSE 格式分块推送动作帧、表情参数等实时数据。

## 关键参数和配置

- **必需请求头**：
  - `X-DashScope-Async: enable`：启用异步模式（图像、视频类接口必需；世界模型中仅 Acting 不适用此头）。
  
- **核心响应字段**（异步成功时返回）：
  - `"task_id"`：全局唯一任务标识符，用于后续查询与管理；
  - `"status"`：当前状态，常见值为 `"QUEUED"`、`"RUNNING"`、`"SUCCEEDED"`、`"FAILED"`、`"CANCELLED"`；
  - `"created_at"` / `"updated_at"`：时间戳，便于监控任务生命周期。

- **轮询建议**：
  - 初始间隔 ≥1s，随任务运行时间指数退避（如 1s → 2s → 4s → 8s）；
  - 设置最大重试次数（推荐 60 次，覆盖典型视频生成上限 5 分钟）；
  - 状态为 `"SUCCEEDED"` 时，响应体中必含 `output` 字段（如图像 URL 数组、视频下载链接、JSON 结构化结果）。

- **错误处理**：
  - 若轮询返回 `404 Not Found`，表示任务已过期（默认保留 24 小时）；
  - `status: "FAILED"` 时，检查 `error.code`（如 `InvalidParameter`、`ResourceExhausted`）与 `error.message` 进行针对性修复。

面向开发者：优先为耗时 >3 秒的请求启用异步；视频类务必强制异步；图像类按业务容忍度选择；世界模型中仅 Acting 需特殊处理 WebSocket。所有异步任务均无需额外鉴权，复用原 API Key 即可。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [world model api reference](../api/world-model-api-reference.md)


