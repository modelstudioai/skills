# 异步任务

异步任务是百炼平台为长耗时 AI 生成请求（如视频生成、图像生成、3D 模型生成等）提供的标准调用模式。开发者通过"创建任务获取 task_id → 轮询或回调获取结果"的两步流程完成调用，避免 HTTP 连接因生成耗时过长而超时。

## 适用场景

百炼平台中以下类型的 API 强制或推荐使用异步任务模式：

- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、数字人等，耗时通常 1-5 分钟
- **图像生成**：部分模型（如万相 V1、可灵等）仅支持异步调用；千问、万相 V2 等同时支持同步和异步
- **3D 模型生成**：Tripo 系列文生 3D、图生 3D 均采用异步模式
- **音乐生成**：Fun-Music 系列支持非流式（异步）和 SSE 流式两种模式
- **长语音识别**等其他长耗时任务

## 调用流程

### 第一步：创建任务

通过 `POST` 请求提交生成参数，请求头中**必须**设置 `X-DashScope-Async: enable`，否则会报错 `current user api does not support synchronous calls`。

请求成功后返回 `task_id`，有效期为 **24 小时**。获取 task_id 后不要重复创建任务。

必选请求头：

| 请求头 | 值 |
|--------|-----|
| `Content-Type` | `application/json` |
| `Authorization` | `Bearer $DASHSCOPE_API_KEY` |
| `X-DashScope-Async` | `enable` |

### 第二步：轮询查询结果

通过 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 查询任务状态。建议轮询间隔 15 秒。

任务状态枚举值：

| 状态 | 说明 |
|------|------|
| `PENDING` | 排队等待中 |
| `RUNNING` | 正在执行 |
| `SUCCEEDED` | 执行成功，可获取结果 |
| `FAILED` | 执行失败 |
| `CANCELED` | 已取消 |
| `UNKNOWN` | task_id 过期或不存在 |

## 任务管理 API

百炼提供一组通用的异步任务管理接口，适用于所有异步场景：

| 接口 | 方法与路径 | 说明 |
|------|-----------|------|
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 获取任务状态及结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 按时间范围、模型名、状态等条件批量查询 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持 `PENDING` 状态的任务 |

三个接口共用 **20 QPS** 的账号级限流。查询结果仅保留 24 小时，过期自动清理。权限上只能查询或取消同一阿里云主账号下的任务。

## 任务完成通知（替代轮询）

高频轮询会消耗资源并触发限流。百炼已将异步任务接入**事件总线 EventBridge**，任务完成时（无论成功或失败）自动生成 `dashscope:System:AsyncTaskFinish` 事件，支持两种推送目标：

- **HTTP 回调 URL**：业务方提供公网或 VPC 内的 POST 接口接收事件，配置简单
- **云消息队列 RocketMQ**：事件转发至 RocketMQ Topic，保证消息不丢失、支持失败重试，适合高可靠性要求

配置时需注意事件规则的**地域必须与任务地域一致**，北京地域的规则不会转发其他地域的事件。

## 注意事项

- `X-DashScope-Async: enable` 请求头是异步调用的必要条件，缺少会直接报错
- `task_id` 有效期 24 小时，超时后查询返回 `UNKNOWN`
- 获取 task_id 后请勿重复创建相同任务
- 结果中的下载链接（如视频 URL、3D 模型 URL）通常有独立的有效期（一般为 2-24 小时），应及时下载
- 查询接口默认 20 QPS 限流，高并发场景建议使用 EventBridge 回调替代轮询
- 北京、新加坡、弗吉尼亚等不同地域的 API Key 互相独立，需在对应地域调用

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [music generation references](../api/music-generation-references.md)
- [more about models](../api/more-about-models.md)


