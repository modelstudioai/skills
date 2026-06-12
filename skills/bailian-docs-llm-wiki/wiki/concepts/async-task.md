# 异步任务

异步任务是百炼平台中用于处理长耗时 AI 生成请求的调用模式。当模型推理需要较长时间（通常数十秒到数分钟）时，平台采用"先提交任务获取 task_id，再凭 task_id 轮询或接收回调获取结果"的两步式异步流程，避免 HTTP 连接超时。

## 适用场景

百炼平台中以下类型的 API 均采用异步任务模式：

- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、数字人等，耗时通常 1-5 分钟
- **图像生成**：部分模型（如万相文生图 V1）仅支持异步调用；大多数图像模型同时支持同步和异步
- **3D 模型生成**：文生 3D、单图/多图生 3D
- **音乐生成**：Fun-Music 系列的非流式模式
- **长语音识别**等其他长耗时任务

## 调用流程

### 步骤 1：创建任务

通过 `POST` 请求向对应模型的服务端点提交参数。请求头中**必须**包含：

```
X-DashScope-Async: enable
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```

> **重要**：缺少 `X-DashScope-Async: enable` 请求头会导致报错 "current user api does not [support](../guides/support.md) synchronous calls"。

成功后返回 `task_id`，有效期为 **24 小时**。请妥善保存 task_id，不要对同一请求重复创建任务。

### 步骤 2：获取结果

有两种方式获取任务结果：

**方式一：轮询查询**

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔 15 秒。任务状态流转为：`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED`。

**方式二：事件回调（推荐）**

通过阿里云事件总线 EventBridge 接收任务完成通知，避免高频轮询消耗资源和触发限流。支持两种事件目标：

- **HTTP 回调 URL**：业务方提供公网或 VPC 可达的 POST 接口接收 JSON 事件，配置简单
- **云消息队列 RocketMQ**：事件转发至 RocketMQ Topic，保证消息不丢失、支持失败重试，适合高可靠性场景

事件类型为 `dashscope:System:AsyncTaskFinish`，事件体包含 `task_id`、`task_status`、`region` 等字段。注意事件规则的地域必须与任务地域一致。

## 任务管理 API

百炼提供一组通用的异步任务管理接口：

| 接口 | 方法与路径 | 说明 |
|------|-----------|------|
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 获取任务状态及结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 按时间范围、模型名称、状态等条件批量查询 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持 `PENDING` 状态的任务 |

任务状态枚举值：`PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`、`CANCELED`、`UNKNOWN`。

## 关键限制

- **task_id 有效期**：24 小时，过期后查询返回 `UNKNOWN` 状态
- **查询限流**：三个管理接口共用 20 QPS 的账号级限流，高频场景建议使用事件回调替代轮询
- **权限范围**：只能查询/取消同一阿里云主账号下的任务（含其所有 API Key 提交的任务）
- **结果保留**：查询返回结果仅保留 24 小时，具体以对应模型文档为准
- **下载链接时效**：任务成功后返回的文件下载 URL 通常有独立的有效期（如 3D 模型为 2 小时），需及时下载

## 开发建议

1. 获取 task_id 后立即持久化存储，避免因进程重启丢失
2. 生产环境优先使用 EventBridge 回调替代轮询，降低资源消耗和限流风险
3. 对于高并发场景，配合 DashScope SDK 的连接池复用功能，减少 TCP 连接开销
4. 实现幂等性检查，避免对同一请求重复创建异步任务

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)
- [music generation references](../api/music-generation-references.md)


