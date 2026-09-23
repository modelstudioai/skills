# 异步处理

异步处理是百炼平台对耗时较长、无法即时返回结果的模型任务所采用的标准调用模式：客户端提交任务后立即获得唯一任务标识（如 `biz_id` 或 `task_id`），服务端在后台执行计算，客户端通过轮询或事件回调方式获取最终结果。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成（Video Generation）**：所有视频 API（如 `wan3-video-generation`、`happyhorse-text-to-video`）强制异步。提交请求必须携带 `X-DashScope-Async: enable` 头，否则报错；典型任务耗时 1–5 分钟，需轮询 `/video-synthesis/result` 接口获取状态与输出 URL。

- **图像生成（Image Generation）**：部分高质/长耗时模型（如 `wan2.7-image-pro`、`kling/kling-v3-omni-image-generation`）默认或推荐异步调用；轻量模型（如 `z-image-turbo`）支持同步，但异步仍是通用兜底方案，适用于批量生成或多图任务。

- **文档与音视频解析（ParseX）**：全部能力（Parse 解析、Extract 抽取）均为异步。无论输入是 PDF、MP4 还是 WAV，均需先调用 `/parse/submit` 或 `/extract/submit` 获取 `biz_id`，再持续轮询 `/result` 接口直至 `data.status == "success"`。

- **多模态与大模型任务**：当输入含大文件（如高清图、长视频）、或模型本身计算密集（如 `qwen-vl-plus` 图文理解+生成），平台自动路由至异步通道；开发者可通过 `task_status` 字段监控生命周期（`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`）。

- **统一任务管理**：所有异步任务均可通过 `/api/v1/tasks/{task_id}` 查询元信息（如创建时间、耗时、错误详情），并支持取消（仅限 `PENDING` 状态）。事件总线（EventBridge）也提供 `dashscope:System:AsyncTaskFinish` 回调，替代轮询，提升响应效率。

## 关键参数和配置

- **必需请求头**：
  - `X-DashScope-Async: enable`：显式启用异步模式（视频 API 强制要求，其他场景建议显式设置）；
  - `Authorization: Bearer <API_KEY>`：标准鉴权，需与模型、Endpoint 地域严格匹配。

- **核心返回字段**：
  - `biz_id`（ParseX）或 `task_id`（通用任务管理）：全局唯一任务标识，用于后续查询与取消；
  - `output.task_status`：当前状态（`PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`/`CANCELED`）；
  - `output.contain_result`（可选）：控制回调或查询响应是否内嵌完整结果体，减少二次请求。

- **轮询建议配置**：
  - 初始延迟 ≥1s，采用指数退避（如 1s → 2s → 4s → 8s）；
  - 超时阈值建议设为模型文档标注最大耗时的 2 倍（如视频生成标称 5 分钟，则设 10 分钟超时）；
  - 遇 `HTTP 409 ResultNotReady` 应重试，遇 `HTTP 404 NotExistBizId` 或 `HTTP 400 ParseResultNotReusable` 需检查参数或时效性。

- **回调通知（推荐生产环境使用）**：
  - 配置 HTTP 回调 URL 或 RocketMQ Topic；
  - 事件体含 `data.task_id`、`data.task_status`、`data.output_url`（若成功）等关键字段；
  - 需实现幂等消费（同一 `task_id` 可能重复投递）。

面向开发者，请始终将异步视为默认行为——除非模型文档明确声明“支持同步且推荐同步”，否则一律按异步流程设计调用逻辑。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)
- [getting started overview](../guides/getting-started-overview.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)


