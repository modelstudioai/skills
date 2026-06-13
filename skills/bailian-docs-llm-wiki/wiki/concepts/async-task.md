# 异步任务

异步任务是百炼平台中用于处理长耗时 AI 生成请求的核心调用模式。开发者通过"创建任务获取 task_id → 轮询或回调获取结果"的两步流程，完成视频生成、3D 模型生成、图像生成、音乐生成等需要较长处理时间的 API 调用。

## 适用场景

百炼平台中以下类型的 API 均采用异步任务模式：

- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、数字人等，耗时通常 1-5 分钟。涵盖万相（Wan）、HappyHorse、PixVerse、可灵（Kling）、Vidu 等多家模型。
- **3D 模型生成**：通过 Tripo 模型实现文生 3D、单图生 3D、多图生 3D，生成高精度三维模型。
- **图像生成**：部分图像生成模型（如万相文生图 V1 版）仅支持异步调用；其他模型同时支持同步和异步两种模式。
- **音乐生成**：Fun-Music 系列模型支持非流式异步输出。
- **长语音识别**：长时间音频的转写任务。

## 调用流程

### 步骤 1：创建任务

通过 `POST` 请求向对应的模型端点提交参数。请求头中**必须**设置 `X-DashScope-Async: enable`，否则会收到错误 "current user api does not [support](../guides/support.md) synchronous calls"。

必选请求头：

| 请求头 | 值 |
|--------|-----|
| `Content-Type` | `application/json` |
| `Authorization` | `Bearer $DASHSCOPE_API_KEY` |
| `X-DashScope-Async` | `enable` |

成功后返回 `task_id`，有效期为 **24 小时**。请勿重复创建任务，获取 task_id 后直接轮询即可。

### 步骤 2：获取结果

通过 `GET` 请求查询任务状态：

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔 15 秒。

## 任务状态

任务在生命周期中经历以下状态：

| 状态 | 说明 |
|------|------|
| `PENDING` | 排队中，尚未开始执行 |
| `RUNNING` | 正在执行 |
| `SUCCEEDED` | 执行成功，可获取结果 |
| `FAILED` | 执行失败 |
| `CANCELED` | 已取消 |
| `UNKNOWN` | task_id 过期或无效 |

## 任务管理 API

百炼提供一组通用的异步任务管理接口：

| 接口 | 方法与路径 | 用途 |
|------|-----------|------|
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 获取任务状态与结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 按时间、模型名、状态等条件批量查询 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持 `PENDING` 状态的任务 |

三个接口共用 **20 QPS** 的账号级限流。查询结果仅保留 24 小时，过期后自动清理。权限范围限于同一阿里云主账号下的所有任务。

## 替代轮询：事件通知

高频轮询会消耗资源并触发限流。百炼支持通过 **EventBridge 事件总线**接收任务完成通知，任务完成时（无论成功或失败）会生成 `dashscope:System:AsyncTaskFinish` 事件。支持两种接收方式：

- **HTTP 回调 URL**：业务方提供一个公网或 VPC 可访问的 POST 接口接收 JSON 事件，配置简单，适合大多数场景。
- **云消息队列 RocketMQ**：事件转发至 RocketMQ Topic，保证消息不丢失、支持失败重试，适合高可靠性要求。

配置时需注意：事件规则的地域必须与任务地域一致，否则无法收到通知。

## 注意事项

- `X-DashScope-Async: enable` 请求头不可省略，缺少时接口会直接报错。
- `task_id` 有效期为 24 小时，过期后查询返回 `UNKNOWN` 状态。
- 取消操作仅对 `PENDING` 状态有效，`RUNNING` 及之后的状态不可取消。
- 结果中的文件下载链接（如视频 URL、3D 模型 URL）通常也有时效限制（一般为 2-24 小时），需及时下载。
- 部分模型（如 PixVerse、可灵、Vidu、Tripo）仅适用于北京地域，需使用对应地域的 API Key。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [more about models](../api/more-about-models.md)
- [music generation references](../api/music-generation-references.md)


