# 异步任务模式

异步任务模式是百炼平台中处理耗时较长的 AI 生成任务时采用的标准调用范式，其核心流程为"创建任务 -> 轮询/回调获取结果"，适用于视频生成、3D 模型生成、图像生成、模型调优与部署等场景。

## 工作原理

异步任务模式将一次完整的 API 调用拆分为两个独立步骤：

1. **创建任务**：客户端提交生成请求，服务端立即返回一个 `task_id`，不阻塞等待结果。
2. **获取结果**：客户端使用 `task_id` 轮询任务状态，或通过事件通知机制被动接收完成消息。

这种设计避免了长时间的 HTTP 连接占用，适合生成耗时从数秒到数分钟不等的多媒体内容。

## 适用场景

在百炼平台中，以下类型的 API 均采用异步任务模式：

- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、人像动画等全部视频生成 API。
- **3D 模型生成**：通过 Tripo 模型进行文生 3D、单图生 3D、多图生 3D。
- **部分图像生成**：万相 2.1 图像编辑、万相 2.6 文生图、涂鸦作画等异步接口（注意：千问图像系列和万相 2.5/2.7 等较新模型已支持同步调用）。
- **模型生产全流程**：模型调优（Fine-tuning）、模型压缩、模型部署均为异步操作，提交后需轮询获取最终状态。

## 统一调用流程

### 步骤 1：创建任务

向对应的 API 端点发送 POST 请求，必须在请求头中设置 `X-DashScope-Async: enable`，否则请求将报错。

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/<service-path>
Content-Type: application/json
Authorization: Bearer $DASHSCOPE_API_KEY
X-DashScope-Async: enable
```

请求成功后返回 `task_id`，有效期通常为 24 小时。在此期间内可随时查询任务状态，超时后任务记录将被系统清理。

### 步骤 2：查询任务状态

使用通用的任务查询接口轮询状态：

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
Authorization: Bearer $DASHSCOPE_API_KEY
```

任务状态流转为：`PENDING`（排队中） -> `RUNNING`（处理中） -> `SUCCEEDED`（成功） / `FAILED`（失败）。

## 任务管理 API

百炼提供三个通用的异步任务管理接口，流量限制均为 20 QPS（按主账号维度）：

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/v1/tasks/{task_id}` | GET | 查询单个任务的状态和结果 |
| `/api/v1/tasks/` | GET | 按条件批量查询任务（支持按时间、模型、状态过滤） |
| `/api/v1/tasks/{task_id}/cancel` | POST | 取消状态为 `PENDING` 的任务 |

批量查询默认返回最近 24 小时的数据，且时间跨度不可超过 24 小时。

## 结果通知机制

除了主动轮询，百炼还支持通过事件总线 EventBridge 实现任务完成后的被动通知，避免频繁轮询造成的资源浪费和限流风险：

- **HTTP 回调**：任务完成后，事件总线将结果推送到预配置的 HTTP URL，适合快速集成。
- **RocketMQ 消息队列**：事件总线将消息转发到 RocketMQ，业务方监听消费，适合对消息可靠性要求较高的场景。

| 获取方式 | 限流 | 实时性 | 适用场景 |
|----------|------|--------|----------|
| 主动轮询 | 查询接口 20 QPS | 依赖轮询频率 | 低并发、小规模 |
| 事件通知 | 不限流 | 任务完成后立即推送 | 高并发、大规模 |

## 关键注意事项

- **必须设置异步头**：请求头 `X-DashScope-Async: enable` 是异步调用的必要条件，缺少该头部会导致请求失败。
- **避免重复创建任务**：提交任务后应使用返回的 `task_id` 轮询结果，不要因未收到结果而重复发起创建请求。
- **task_id 有效期**：通常为 24 小时，超时后查询返回 `UNKNOWN` 状态。
- **下载链接有效期**：生成结果中的资源下载 URL 通常有独立的有效期（如 3D 模型为 2 小时），请及时下载保存。
- **地域限制**：部分模型仅在特定地域可用（如 3D 生成仅限北京地域），需使用对应地域的 API Key。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [more about models](../api/more-about-models.md)
- [model production](../api/model-production.md)


