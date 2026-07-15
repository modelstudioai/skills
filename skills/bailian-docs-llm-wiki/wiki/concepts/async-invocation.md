# 异步调用与任务轮询

异步调用是百炼平台为耗时较长的模型任务（图像生成、视频生成、3D 生成、复杂智能体应用等）提供的调用模式：客户端先「创建任务」拿到一个 `task_id`，随后通过「轮询查询」或事件回调获取最终结果，从而避免长请求超时。

## 适用场景

在百炼平台上，凡是单次处理通常需要数十秒到数分钟的能力，基本都以异步为主：

- **图像生成**：文生图、图像编辑、扩图、虚拟模特等（通常 1-2 分钟）。部分新一代模型（如 `wan2.6-image`、`wan2.7-image`、`z-image-turbo`）额外提供 HTTP 同步调用。
- **视频生成**：万相、PixVerse、Vidu、Kling 及人像驱动等模型（通常 1-5 分钟），统一走 `video-synthesis` 接口，全部为异步。
- **3D 生成**：基于 Tripo 的文生 3D / 图生 3D，仅支持异步。
- **智能体 / 工作流应用**：Responses API 通过 `background=true` 开启异步，用于生成报告、多步骤工具调用等耗时任务（DashScope API 暂不支持异步）。

## 调用流程

异步调用统一分为两步：

1. **创建任务**：向对应模型的下发接口发送 `POST` 请求，成功后立即返回 `task_id`。
   - 大多数生成类接口必须携带请求头 `X-DashScope-Async: enable`，否则报错 `current user api does not support synchronous calls`。
   - 智能体应用（Responses API）则通过请求体参数 `background=true` 开启异步。
   - `task_id` 有效期为 **24 小时**，**请勿重复创建任务**，创建成功后轮询即可。

2. **轮询查询结果**：
   ```
   GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
   ```
   返回体中 `output.task_status` 标识当前状态，流转过程通常为 `PENDING`（排队中）→ `RUNNING`（处理中）→ `SUCCEEDED` / `FAILED`。仅当状态为 `SUCCEEDED` 时才返回结果内容（如图像 / 视频 / 模型下载 URL）。

## 任务状态枚举

| 状态 | 含义 |
| --- | --- |
| `PENDING` | 任务排队中 |
| `RUNNING` | 任务处理中 |
| `SUCCEEDED` | 任务成功，返回结果 |
| `FAILED` | 任务失败，返回 `code` / `message` |
| `CANCELED` | 任务已取消（仅 `PENDING` 状态可取消） |
| `UNKNOWN` | 任务不存在，或超过 24 小时有效期被清理 |

## 通用任务管理接口

除单任务查询外，百炼提供三个通用异步任务管理接口，流量限制均为 **20 QPS**（主账号维度）：

- **查询单个任务**：`GET .../api/v1/tasks/{task_id}`
- **批量查询任务状态**：`GET .../api/v1/tasks/?start_time=xxx&end_time=xxx&status=xxx`，可按时间范围、模型名、状态过滤，单次时间跨度不超过 24 小时。
- **取消任务**：`POST .../api/v1/tasks/{task_id}/cancel`，仅能取消尚在 `PENDING` 状态的任务，已开始处理的无法取消。

## 关键要点与最佳实践

- **轮询间隔**：建议约 15 秒查询一次，避免过于频繁触发限流（查询接口默认 20 RPS）。
- **事件通知替代轮询**：频繁轮询浪费资源且易触发限流。百炼已接入阿里云 EventBridge，支持任务完成后主动推送通知（HTTP 回调 URL 或 RocketMQ）。事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`，关键字段为 `data.task_status` 与 `data.task_id`；收到通知后只需查询一次即可拿到结果。
- **结果时效**：任务结果（如图像/视频 URL）与 `task_id` 有效期一般为 24 小时；3D 生成的模型下载链接有效期更短，仅 **2 小时**，需及时下载。
- **地域一致性**：模型、Endpoint、API Key 必须属于同一地域（如华北2·北京、新加坡等），跨地域调用会失败。3D 生成目前仅支持华北2（北京）。
- **接口路径差异**：不同模型的下发路径并不统一（如 `.../aigc/video-generation/video-synthesis`、`.../aigc/image2video/video-synthesis`、`.../text2image/image-synthesis` 等），接入前请以对应模型文档为准。

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)
- [application call](../api/application-call.md)
- [more about models](../api/more-about-models.md)


