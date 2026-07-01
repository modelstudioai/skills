# 异步调用

异步调用是百炼平台针对耗时较长的生成类任务（如图像生成、视频生成、3D 模型生成）所采用的统一调用模式。其核心流程为「创建任务获取 task_id → 轮询或回调获取结果」，避免长时间阻塞 HTTP 连接。

## 适用场景

异步调用适用于所有处理时间超出常规 HTTP 超时的模型服务，包括但不限于：

- **3D 模型生成**：文生 3D、图生 3D、多图生 3D（Tripo 系列）
- **视频生成**：文生视频、图生视频、视频编辑、数字人等（万相、可灵、PixVerse、Vidu 系列）
- **图像生成**：万相文生图、图像编辑、创意工具等（部分接口支持同步，大多数走异步）

## 调用流程

### 1. 创建任务

向对应模型的 API 端点发送 POST 请求，必须携带请求头：

```
X-DashScope-Async: enable
```

缺少此请求头会报错 `current user api does not support synchronous calls`。

成功后响应中返回 `task_id`，该 ID 是后续查询结果的唯一凭证。

### 2. 查询结果

通过通用查询接口轮询任务状态：

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔约 15 秒，直到状态变为终态。

## 任务状态

| 状态 | 含义 |
| --- | --- |
| `PENDING` | 排队中，等待处理 |
| `RUNNING` | 正在处理 |
| `SUCCEEDED` | 任务成功，可获取结果 |
| `FAILED` | 任务失败，查看错误信息 |
| `CANCELED` | 已被取消 |
| `UNKNOWN` | 任务不存在或超过有效期 |

## 异步任务管理接口

百炼提供三个通用的任务管理接口（限流均为 20 QPS）：

| 接口 | 方法与路径 | 用途 |
| --- | --- | --- |
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 根据 task_id 查询状态与结果 |
| 批量查询 | `GET /api/v1/tasks/` | 按时间/状态/模型等条件分页查询 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 取消排队中（PENDING）的任务 |

## 避免轮询：任务完成通知

频繁轮询会浪费资源并可能触发限流。百炼已接入阿里云事件总线 EventBridge，任务完成后主动推送通知，支持两种接收方式：

- **HTTP 回调 URL**：事件总线直接向公网接口 POST 推送，接入简单
- **RocketMQ 消息队列**：消息投递到 MQ 供业务消费，支持失败重试，可靠性更高

事件关键字段：事件源 `acs.dashscope`，事件类型 `dashscope:System:AsyncTaskFinish`，事件数据包含 `task_id`、`task_status`、`region` 等。

## 关键约束与注意事项

- **task_id 有效期 24 小时**：超时后无法再查询，状态返回 `UNKNOWN`
- **请勿重复创建任务**：拿到 task_id 后直接轮询即可
- **同地域要求**：模型端点、[API Key](api-key.md) 必须属于同一地域
- **产物链接时效**：生成结果的下载 URL 通常有效期 2 小时，需及时下载或转存
- **取消限制**：仅支持取消 `PENDING` 状态的任务
- **子任务机制**：含多个子任务的请求，只要有一个子任务成功，整体即为 `SUCCEEDED`；失败子任务的错误在 `output.results` 中单独展示

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)


