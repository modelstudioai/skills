# 异步任务

异步任务是百炼平台处理长耗时模型调用的核心协议。对于视频生成、3D 模型生成、部分图像生成以及模型微调等需要较长处理时间的操作，平台统一采用"先创建任务获取 task_id，再凭 task_id 轮询或接收回调获取结果"的两步式异步调用模型。

## 调用流程

### 第一步：创建任务

向对应模型的 API 端点发送 POST 请求，请求头中必须包含：

| 请求头 | 值 | 说明 |
| --- | --- | --- |
| `X-DashScope-Async` | `enable` | 启用异步模式，缺少此头会报错 |
| `Authorization` | `Bearer $DASHSCOPE_API_KEY` | API Key 鉴权 |
| `Content-Type` | `application/json` | 请求体格式 |

成功后返回 `task_id`，有效期 24 小时。获取 task_id 后切勿重复创建任务。

### 第二步：查询结果

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔 15 秒。高频轮询场景推荐改用事件通知替代轮询。

## 任务状态

| 状态 | 含义 |
| --- | --- |
| `PENDING` | 任务已提交，等待调度 |
| `RUNNING` | 任务执行中 |
| `SUCCEEDED` | 任务成功完成 |
| `FAILED` | 任务异常终止 |
| `CANCELED` | 用户主动取消 |
| `UNKNOWN` | task_id 已过期或无法识别 |

## 任务管理 API

百炼提供一组通用的异步任务管理接口，适用于所有异步任务类型：

| 操作 | 方法与路径 | 说明 |
| --- | --- | --- |
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 获取任务状态与结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 支持按时间范围、模型名、状态分页查询 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持 `PENDING` 状态的任务 |

三个接口共用 20 QPS 的账号级限流，查询结果仅保留 24 小时。权限范围为同一阿里云主账号下所有 API Key 提交的任务。

## 事件通知（替代轮询）

高频轮询会消耗业务资源并触发限流。百炼已将异步任务接入事件总线 EventBridge，任务完成时（无论成功或失败）会生成 `dashscope:System:AsyncTaskFinish` 事件，支持两种推送目标：

- **HTTP 回调 URL**：业务方提供一个 POST 接口接收 JSON 事件，配置简单，适合大多数场景。
- **云消息队列 RocketMQ**：事件转发至 RocketMQ Topic，支持失败重试，适合高可靠性要求。

事件规则的地域必须与任务地域一致，否则无法收到通知。事件 Body 中的 `data.user_api_unique_key` 字段支持按模型名过滤。

## 适用场景

| 场景 | 典型模型 | 任务耗时 |
| --- | --- | --- |
| 视频生成（文生视频、图生视频等） | wan2.7-t2v、kling-v3 等 | 1–10 分钟 |
| 3D 模型生成 | Tripo-H3.1、Tripo-P1.0 | 数分钟 |
| 图像生成（万相 2.5 及以下版本） | wanx2.1-t2i-turbo 等 | 数秒至数分钟 |
| 模型微调训练 | Qwen 系列基座模型 | 数十分钟至数小时 |

> **提示**：万相 2.6 及以上版本的图像生成已支持 HTTP 同步调用，无需异步流程。

## 多地域注意事项

模型、Endpoint URL 和 API Key 必须属于同一地域，跨地域调用会失败。主要地域包括华北2（北京）、新加坡、美国（弗吉尼亚）和德国（法兰克福），各地域的 Endpoint URL 格式不同，详见对应模型的 API 文档。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [more about models](../api/more-about-models.md)
- [fine tuning jobs api](../api/fine-tuning-jobs-api.md)


