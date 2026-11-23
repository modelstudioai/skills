# 异步处理

异步处理是百炼平台对耗时较长的 AI 任务（如视频生成、3D 建模、长文档解析等）采用的标准执行模式：客户端发起请求后立即返回任务标识（`task_id` 或 `biz_id`），实际计算在服务端后台执行，结果通过轮询或回调方式获取，避免阻塞 HTTP 连接与客户端线程。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像/视频/3D 生成类 API**（如 `image-generation`、`video-generation`、`3d-generation`）：所有调用必须显式声明 `X-DashScope-Async: enable` 请求头，否则直接报错；成功响应返回 `task_id`，需调用 `/api/v1/tasks/{task_id}` 轮询状态（`status` 字段为 `SUCCESS`/`FAILED`/`RUNNING`）。
- **音视频与音频处理类 API**（如 `audio-api-directory` 中的 ASR、音视频翻译、音频打标）：长耗时任务（如 >30 秒音频）自动转为异步，响应体含 `task_id`；短任务仍可能同步返回，但开发者应统一按异步流程兼容（检查响应是否含 `task_id`）。
- **文档与结构化抽取类 API**（如 `api-overview` / ParseX）：全部强制异步，无同步路径；提交后必须用 `biz_id` 轮询 `/result/{biz_id}`，不支持直接返回完整结果。
- **实时模型（如 `Qwen-Omni-Realtime`）不适用异步处理**：其设计目标是低延迟流式交互，采用 WebSocket 长连接与事件驱动（如 `DialogStateChanged`），与异步任务范式正交——二者不可混用。

> ✅ 统一实践建议：无论接口文档是否明确标注“异步”，只要响应中包含 `task_id` 或 `biz_id`，即表示该次调用已进入异步流程，必须按异步协议处理；切勿假设“无 `task_id` 就是同步成功”。

## 关键参数和配置

- **强制请求头**：`X-DashScope-Async: enable`  
  所有明确要求异步的 API（如视频、3D、部分音频）必须携带此 Header，缺失将返回 `400 Bad Request` 及错误码 `"current user api does not support synchronous calls"`。

- **任务标识字段**：  
  - `task_id`：通用异步任务 ID（视频、3D、部分音频 API 使用）；  
  - `biz_id`：ParseX 文档解析与结构化抽取专用任务 ID；  
  - 两者均为字符串，有效期统一为 **24 小时**（超时后查询返回 `UNKNOWN` 状态）。

- **轮询配置建议**：  
  - 初始延迟：首次查询建议等待 ≥10 秒（避免空转）；  
  - 查询间隔：根据任务类型动态调整（图像生成 ≥2 秒，视频/3D ≥15–30 秒）；  
  - 限流保护：主账号级轮询限流为 **20 QPS**，超限返回 `429 Too Many Requests`，请务必添加退避逻辑（如指数退避）。

- **免轮询替代方案**：  
  - **HTTP 回调**：在请求体中传入 `callback_url`（如 ParseX 的 `api-overview`、部分音频 API），服务端完成时主动 `POST` 结果至该地址；需确保服务可公网访问并正确处理 `application/json` 请求；  
  - **事件总线（EventBridge）**：适用于企业级高可靠场景，需在控制台配置事件规则与目标（如函数计算、消息队列），文档见《异步任务完成通知》。

## 面向开发者，简洁实用

- ✅ **必做**：检查每次响应是否含 `task_id` 或 `biz_id` —— 有则必须轮询或配置回调，无则视为同步完成（极少数轻量任务）。  
- ✅ **必设**：异步请求必须带 `X-DashScope-Async: enable`，且 `Authorization` 头有效、地域匹配（如北京地域 API Key 不能用于上海 Endpoint）。  
- ⚠️ **避坑**：不要轮询过频（触发 20 QPS 限流）、不要忽略 `status` 字段（`RUNNING` 不代表成功）、不要复用过期 `task_id`（24 小时后失效）。  
- 🚀 **进阶**：生产环境优先使用 `callback_url` 或事件总线，降低轮询开销与失败风险；轮询客户端需实现幂等重试与超时熔断（建议最大等待 ≤ 2 小时）。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [audio api directory](../api/audio-api-directory.md)
- [api overview](../api/api-overview.md)


