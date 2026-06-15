# 异步任务

异步任务是百炼平台中用于处理长耗时 AI 生成请求的核心调用模式。当模型推理需要较长时间（通常数十秒到数分钟）时，平台采用"先提交任务获取 task_id，再凭 task_id 轮询或接收结果"的异步机制，避免请求超时并支持高并发调度。

## 适用场景

异步任务模式广泛应用于以下百炼 API 场景：

- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、数字人等，耗时通常 1-5 分钟
- **3D 模型生成**：文生 3D、单图生 3D、多图生 3D
- **图像生成**：部分图像生成模型（如万相文生图 V1、部分编辑模型）仅支持异步调用
- **长语音识别**：大文件音频转写等长耗时推理任务

## 调用流程

### 第一步：创建任务

通过 `POST` 请求向对应模型端点提交参数。**必须**在请求头中设置：

```
X-DashScope-Async: enable
```

缺少该请求头会报错 `current user api does not support synchronous calls`。

请求成功后返回 `task_id`，有效期为 **24 小时**。获取 task_id 后不要重复创建任务。

### 第二步：获取结果

通过 `GET` 请求查询任务状态：

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔 15 秒。任务状态枚举值：

| 状态 | 说明 |
|------|------|
| `PENDING` | 排队中 |
| `RUNNING` | 执行中 |
| `SUCCEEDED` | 成功完成 |
| `FAILED` | 执行失败 |
| `CANCELED` | 已取消 |
| `UNKNOWN` | task_id 过期或无效 |

## 任务管理 API

百炼提供通用的异步任务管理接口，适用于所有异步模型：

| 接口 | 方法与路径 | 用途 |
|------|-----------|------|
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 获取任务状态及结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 按时间、模型名、状态等条件批量查询 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持 `PENDING` 状态的任务 |

三个接口共享 **20 QPS** 的账号级限流。查询结果仅保留 24 小时，过期自动清理。权限范围为同一阿里云主账号下的所有任务。

## 事件通知（替代轮询）

高频轮询会消耗系统资源并触发 QPS 限流。百炼支持通过**事件总线 EventBridge** 接收任务完成通知，业务侧仅需一次拉取结果：

- **HTTP 回调 URL**：业务方提供公网或 VPC 的 POST 接口接收 JSON 事件，配置简单
- **云消息队列 RocketMQ**：事件转发至 RocketMQ Topic，保证消息不丢失，支持失败重试，适合高可靠性要求

事件类型为 `dashscope:System:AsyncTaskFinish`，关键字段包括 `task_id`、`task_status`、`region` 等。可通过 `user_api_unique_key` 字段按模型过滤事件。

> **注意**：事件规则的地域必须与任务提交地域一致，否则无法接收通知。

## 关键注意事项

- `X-DashScope-Async: enable` 请求头为异步调用的必选项
- task_id 有效期 24 小时，超时后查询返回 `UNKNOWN` 状态
- 查询接口存在 20 QPS 限流，高并发场景建议配置事件通知
- 结果中的资源下载链接（如视频 URL、3D 模型 URL）通常有独立的过期时间（如 2 小时），需及时下载
- 北京、新加坡、弗吉尼亚等地域的 API Key 互相独立，任务需在对应地域查询

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)


