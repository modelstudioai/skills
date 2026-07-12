# 异步调用与任务轮询

异步调用是百炼平台针对耗时较长的模型能力（如视频生成、3D 生成、部分图像生成、长任务应用调用）提供的一种调用模式：客户端先提交任务拿到 `task_id`，再通过轮询或事件通知获取最终结果，从而避免同步请求超时。

## 适用场景

异步调用主要用于生成过程需要数十秒到数分钟的能力，在百炼平台的多个场景中被采用：

- **视频生成**：万相（Wan）、HappyHorse、爱诗（PixVerse）、Vidu、可灵（Kling）等所有视频生成 API 均为异步模式（创建任务 → 轮询获取结果）。
- **3D 资产生成**：基于 Tripo 模型的文生 3D、单图生 3D、多图生 3D 全部走异步流程，且仅在华北2（北京）地域可用。
- **图像生成**：部分耗时较长的图像生成/编辑任务采用异步机制。
- **应用调用（智能体/工作流）**：OpenAI 兼容的 Responses API 支持异步执行；DashScope API 目前暂不支持异步，仅 Responses API 提供。

## 调用流程

异步调用通常包含两个步骤：

1. **创建任务**：向业务接口发起 `POST` 请求，成功后返回 `task_id`。以 3D 生成为例，需在请求头携带 `X-DashScope-Async: enable`，否则会报错 `current user api does not support synchronous calls`。应用调用（Responses API）则通过在请求体中设置 `background=true` 开启异步模式。
2. **轮询查询结果**：使用返回的 `task_id` 定期查询任务状态，直到任务结束。

### 通用异步任务管理 API

百炼提供了一组通用的任务管理接口（主账号维度限流均为 20 QPS）：

- **查询单个任务**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`
- **批量查询任务状态**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/?start_time=xxx&end_time=xxx&status=xxx`，单次时间跨度不超过 24 小时。
- **取消任务**：`POST https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}/cancel`，仅能取消 `PENDING` 状态的任务，已开始处理的任务无法取消。

应用调用场景下，可用 SDK 方法轮询，例如 Responses API 的 `client.responses.retrieve(task_id)`。

## 任务状态

查询接口返回 `output.task_status`，其状态流转与枚举值为：

- `PENDING`：排队中
- `RUNNING`：处理中
- `SUCCEEDED`：成功，此时 `output.results` 才会返回产物
- `FAILED`：失败，响应中通常带 `code` 与 `message`
- `CANCELED`：已取消
- `UNKNOWN`：任务不存在或超过 24 小时有效期

应用调用（Responses API）的终态则表现为 `completed`、`failed` 等。

## 关键要点与配置

- **异步请求头/开关**：模型 API 需 `X-DashScope-Async: enable`；应用 Responses API 需 `background=true`。
- **task_id 有效期**：一般为 24 小时，已完成任务保留约 24 小时后自动清理，超时查询返回 `UNKNOWN`。
- **不要重复创建任务**：创建成功后应仅轮询，重复创建会浪费额度。
- **轮询间隔**：建议按任务耗时设置合理间隔（如 3D 生成建议约 15 秒），查询接口默认 RPS/QPS 约为 20，避免高频轮询触发限流。
- **产物下载时效**：生成类产物下载链接有效期较短（如 3D 模型链接仅 2 小时），需及时下载。

## 异步任务完成通知

频繁轮询会浪费资源并可能触发限流。百炼已接入阿里云事件总线 EventBridge，支持任务完成后主动推送通知，替代或补充轮询：

- **HTTP 回调 URL**：接入简单，需公网或 VPC 可达的 HTTP 接口，适用于通用场景。
- **RocketMQ**：保证消息无丢失、支持失败重试，适用于可靠性要求高的场景，需额外开通 RocketMQ 实例。

事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`，事件体中的 `data.task_status` 与 `data.task_id` 为关键字段。收到通知后只需调用一次查询接口即可获取结果，从而显著降低轮询开销。

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)
- [application call](../api/application-call.md)
- [more about models](../api/more-about-models.md)



