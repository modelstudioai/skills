# 异步调用

异步调用是百炼平台对耗时较长的AI任务（如视频生成、3D建模、文档结构化解析等）所采用的标准交互范式：客户端提交任务后立即获得唯一 `task_id`（或 `biz_id`），不等待计算完成，而是通过后续轮询或事件通知方式获取最终结果。该模式避免了长连接阻塞、超时中断与资源浪费，是生产环境稳定集成的推荐方式。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成（Video Generation）**：所有接口（HappyHorse、万相、爱诗、可灵、Vidu）均强制异步。调用 `POST /api/v1/services/aigc/video-generation/video-synthesis` 创建任务，返回 `task_id`；再通过 `GET /api/v1/tasks/{task_id}` 查询状态（`PENDING` → `RUNNING` → `SUCCESS`/`FAILED`），成功时返回 `output.video_url`。轮询间隔建议 ≥5 秒。

- **3D生成（3D Generation）**：Tripo 全系列能力（文/图生3D、Gaussian Splat、网格分割、重拓扑、自动绑骨等）仅支持异步，且**严格限定华北2（北京）地域**。任务创建后返回 `task_id`，需轮询 `GET /api/v1/tasks/{task_id}`；首次查询建议延迟 10 秒，后续间隔 15–30 秒以降低限流风险。

- **文档与音视频解析（ParseX）**：文档解析与字段抽取均基于 `biz_id` 异步模型。提交 `POST /api/v2/apps/parse-x/parse/submit` 或 `/extract/submit` 后获取 `biz_id`，再调用对应 `result` 接口查询 `data.status`（`success`/`failed`/`processing`）。注意：两类任务系统隔离，`biz_id` 不可跨类型复用。

- **图像生成（Image Generation）**：并非全部图像模型都异步——`qwen-image-*`、`wan2.7-image-pro` 等低延迟模型支持同步调用；但 `wan2.5-i2i-preview`、`kling/kling-v3-omni-image-generation`、`vidu` 及所有创意工具类模型（如 `image-erase-completion`）**必须异步**，流程与视频一致：先创建任务得 `task_id`，再轮询结果。

- **通用异步任务管理**：平台提供统一的异步任务生命周期管理能力，包括任务查询、取消（部分模型支持）、事件通知（HTTP回调或RocketMQ）等。推荐在高并发场景下**优先使用事件驱动替代轮询**，订阅 `dashscope:System:AsyncTaskFinish` 事件，收到通知后再查一次结果，彻底规避 QPS 限流（默认轮询上限 20 QPS）。

## 关键参数和配置

- **必需请求头**：  
  `X-DashScope-Async: enable` —— 所有强制异步的模型均要求此 Header，缺失将返回明确错误：`"current user api does not support synchronous calls"`。

- **核心标识符**：  
  - `task_id`：视频、3D、部分图像模型返回的任务唯一ID（UUID格式），有效期 24 小时。  
  - `biz_id`：ParseX 解析与抽取任务使用的业务ID，有效期与结果保留期绑定（解析结果保留30天，抽取复用结果仅限7天）。

- **推荐轮询策略**：  
  - 初始延迟：5–10 秒（给服务端预留排队与初始化时间）；  
  - 间隔递增：前3次可设为 5s，后续逐步延长至 15–30s；  
  - 终止条件：状态为 `SUCCESS`/`FAILED`/`CANCELED`，或 `task_id` 超过24小时失效。

- **事件通知（高级用法）**：  
  配置 HTTP 回调 URL 或 RocketMQ Topic，订阅 `dashscope:System:AsyncTaskFinish` 事件，消息体含 `data.task_id` 和 `data.task_status`。启用后无需主动轮询，显著降低客户端复杂度与服务端压力。

## 面向开发者，简洁实用

- ✅ **务必检查模型文档**：同一模型不同版本可能调用模式不同（如万相2.7需 `X-DashScope-Async: enable`，而万相3.0虽未明写但实际仍强制异步）；不要凭经验跳过 Header。
- ✅ **地域必须一致**：API Key、Endpoint、Workspace ID、OSS 临时URL 均须同属一个地域（如北京），跨地域调用必然失败。
- ✅ **轮询不是唯一选择**：生产环境强烈推荐事件通知方案，尤其当任务量大或对实时性有要求时。
- ❌ **不要重用 `task_id` 或 `biz_id`**：它们是一次性凭证，不可重复提交或跨模型/跨账号使用。
- ❌ **不要忽略错误码**：`InvalidParameter`、`ParseResultNotReusable`、`FileSizeExceeded` 等均为可操作提示，应结合[错误码文档](../../raw/application-api-reference/api-overview/errors.md)做分类处理（如重试、修正输入、降级逻辑）。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)


