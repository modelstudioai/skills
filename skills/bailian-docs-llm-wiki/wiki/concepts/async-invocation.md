# 异步调用与任务轮询

异步调用是百炼平台为耗时较长的模型任务（图像生成、视频生成、3D 生成等）设计的调用模式：客户端先提交任务拿到 `task_id`，再通过轮询或事件通知获取最终结果，从而避免长连接等待与请求超时。

## 核心流程：创建任务 → 轮询获取

异步调用统一分为两步：

1. **创建任务**：向对应能力的生成端点发起 `POST` 请求，请求头必须携带 `X-DashScope-Async: enable`，否则会报错 `current user api does not support synchronous calls`。请求成功后返回一个 `task_id`。
2. **轮询查询结果**：用该 `task_id` 发起 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`，读取 `output.task_status` 直到任务进入终态（`SUCCEEDED` / `FAILED`），再从结果中取回产物 URL。

任务状态的典型流转为：`PENDING`（排队中）→ `RUNNING`（处理中）→ `SUCCEEDED`（成功）/ `FAILED`（失败）。不同能力还可能出现 `SUSPENDED`（挂起）、`CANCELED`（已取消）、`UNKNOWN`（任务不存在或已过期）等状态。

## 在不同场景中的使用

- **3D 生成（Tripo）**：仅支持异步，端点为 `.../aigc/video-generation/3d-generation`，轮询建议间隔约 15 秒，生成耗时较长，产物下载链接有效期仅 2 小时。
- **视频生成**：所有厂商模型（万相、PixVerse、Vidu、可灵等）统一走异步，端点通常为 `.../aigc/video-generation/video-synthesis`（部分数字人/换人类模型使用 `.../aigc/image2video/video-synthesis`）。单次任务通常耗时 1-5 分钟，个别统一编辑模型约 5-10 分钟。
- **图像生成**：多数传统模型仅支持异步（`text2image` / `image2image` 等端点），生成通常需 1-2 分钟；而新版模型（wan2.6 / wan2.7、z-image-turbo 等）走 `multimodal-generation/generation` 端点，支持 HTTP 同步一次拿结果。请勿把同步协议用在旧模型上。
- **应用调用（智能体/工作流）**：Responses API（OpenAI 兼容）通过设置 `background=true` 开启异步，创建任务后返回任务 ID 再轮询；DashScope 应用调用接口目前暂不支持异步。

## 关键参数与配置

- **请求头**：创建任务必须带 `X-DashScope-Async: enable`；同时需 `Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`。
- **`task_id` 有效期**：一般为 **24 小时**，过期查询返回 `UNKNOWN`。请勿重复创建任务，轮询即可。
- **`background`（应用 Responses API）**：布尔值，默认 `false`，设为 `true` 开启异步执行。
- **查询限流**：任务查询接口默认约 20 QPS / RPS（主账号维度）。

## 异步任务管理与完成通知

百炼提供三个通用的异步任务管理接口：

- **查询单个任务**：`GET .../api/v1/tasks/{task_id}`。
- **批量查询**：`GET .../api/v1/tasks/?start_time=xxx&end_time=xxx&status=xxx`，单次时间跨度不超过 24 小时。
- **取消任务**：`POST .../api/v1/tasks/{task_id}/cancel`，仅能取消 `PENDING` 状态的任务。

为避免频繁轮询浪费资源并触发限流，百炼已接入阿里云事件总线 EventBridge，支持任务完成后主动推送通知（HTTP 回调 URL 或 RocketMQ 两种方案）。事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`，收到通知后只需调用一次查询接口即可获取结果。

## 开发者建议

- 妥善保存 `task_id`，切勿因未及时轮询到结果而重复创建任务。
- 轮询间隔不宜过密（如约 15 秒），高频或生产场景优先使用异步完成通知。
- 及时下载产物：图像/视频 URL 有效期通常为 24 小时，3D 模型下载链接有效期仅 2 小时。
- 处理失败时读取响应中的 `code` 与 `message`，对照百炼错误码文档排查。

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)
- [more about models](../api/more-about-models.md)
- [application call](../api/application-call.md)


