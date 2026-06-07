# 异步任务

异步任务是百炼平台处理长耗时 AI 推理请求的标准模式。客户端先提交请求获取 `task_id`，随后通过轮询或事件通知获取任务结果，避免长时间阻塞连接。

## 适用场景

百炼平台中以下能力均采用异步任务模式：

- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、数字人驱动等全部走异步流程。
- **3D 模型生成**：Tripo 系列模型的文生 3D、单图生 3D、多图生 3D。
- **图像生成与编辑**：万相系列、千问图像、可灵图像等大部分图像生成任务。
- **录音文件识别**：Qwen-ASR（`qwen3-asr-flash-filetrans`）、Paraformer、Fun-ASR 的长音频转写。
- **文本向量批处理**：`text-embedding-async-v2` / `text-embedding-async-v1`，单次最多 100,000 行。

## 基本流程

### 1. 创建任务

向对应模型的服务端点发送 POST 请求，**必须携带请求头** `X-DashScope-Async: enable`，否则会报错 "current user api does not [support](../guides/support.md) synchronous calls"。

请求成功后返回 `task_id`，有效期为 **24 小时**，超时后查询将返回 `UNKNOWN` 状态。

### 2. 查询任务状态

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔 **15 秒**。任务状态枚举值如下：

| 状态 | 含义 |
|------|------|
| `PENDING` | 排队等待执行 |
| `RUNNING` | 正在执行 |
| `SUCCEEDED` | 执行成功，可获取结果 |
| `FAILED` | 执行失败 |
| `CANCELED` | 已被取消 |
| `UNKNOWN` | task_id 过期或无法识别 |

### 3. 获取结果

任务成功后，响应体中包含模型输出（如视频/图片/音频的下载 URL、3D 模型文件链接、识别文本等）。下载链接通常有时效限制（视频 24 小时、3D 模型 2 小时），需及时转存。

## 任务管理 API

百炼提供一组通用的异步任务管理接口，适用于所有异步模型：

| 操作 | 方法与路径 | 说明 |
|------|-----------|------|
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 获取任务状态及结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 按时间、模型名、状态等条件批量筛选 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持 `PENDING` 状态的任务 |

三个接口共享 **20 QPS** 的账号级限流，查询结果保留 **24 小时**。权限范围为同一阿里云主账号下所有 API Key 提交的任务。

## 事件通知（替代轮询）

高频轮询会消耗资源并可能触发 QPS 限流。百炼通过阿里云事件总线 EventBridge 提供任务完成通知，事件类型为 `dashscope:System:AsyncTaskFinish`，支持两种接收方式：

- **HTTP 回调**：配置公网或 VPC 可达的 POST 接口接收 JSON 事件，适合大多数场景。
- **云消息队列 RocketMQ**：事件转发至 RocketMQ Topic，通过 PushConsumer 消费，适合高可靠性要求。

事件 Body 包含 `task_id`、`task_status`、`region` 等字段，还可通过 `user_api_unique_key` 配置事件模式过滤特定模型的任务。

> 事件规则的地域必须与任务地域一致，否则无法接收通知。

## 关键注意事项

- 获取 `task_id` 后应保存并轮询，**不要重复创建相同任务**。
- 北京、新加坡、弗吉尼亚三个地域的 API Key 互相独立，异步任务也需在对应地域查询。
- 批处理类异步模型（如 `text-embedding-async-v2`）与同步模型是独立的模型系列，不能混用。
- 高并发场景建议优先使用 EventBridge 事件通知，减少对查询接口的压力。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)
- [general text embedding](../api/general-text-embedding.md)
- [image generation](../api/image-generation.md)
- [music generation references](../api/music-generation-references.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)


