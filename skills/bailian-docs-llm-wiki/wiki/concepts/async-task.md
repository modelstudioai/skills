# 异步任务

异步任务是百炼平台处理长耗时 AI 生成请求的标准调用模式。开发者提交请求后立即获得一个任务 ID（`task_id`），随后通过轮询或事件通知获取最终结果，无需保持长连接等待。

## 适用场景

百炼平台中以下类型的 API 采用异步任务模式：

- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、数字人等，耗时通常 1-5 分钟
- **3D 模型生成**：文生 3D、单图生 3D、多图生 3D
- **图像生成**：部分图像生成模型支持异步调用（大部分同时支持同步和异步）
- **音乐生成**：Fun-Music 系列（同时也支持非流式同步调用）
- **长语音识别**等其他长耗时任务

## 调用流程

所有异步任务遵循统一的两步流程：

### 1. 创建任务

通过 `POST` 请求提交生成参数，请求头中必须包含：

```
X-DashScope-Async: enable
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```

> **重要**：缺少 `X-DashScope-Async: enable` 请求头会导致报错 "current user api does not [support](../guides/support.md) synchronous calls"。

成功后返回 `task_id`，有效期为 **24 小时**。请勿对同一请求重复创建任务。

### 2. 获取结果

有两种方式获取任务结果：

**方式一：轮询查询**

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔 15 秒。任务状态流转为：`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED`。

**方式二：事件通知（推荐）**

通过阿里云事件总线 EventBridge 接收任务完成通知，避免高频轮询消耗资源和触发限流。支持两种事件目标：
- **HTTP 回调 URL**：配置简单，适合大多数场景
- **云消息队列 RocketMQ**：保证消息不丢失、支持失败重试，适合高可靠性要求

事件类型为 `dashscope:System:AsyncTaskFinish`，事件规则的地域必须与任务地域一致。

## 任务管理 API

百炼提供通用的异步任务管理接口：

| 接口 | 方法 | 用途 |
|------|------|------|
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 获取任务状态及结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 按时间、模型、状态等条件批量查询 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持 `PENDING` 状态的任务 |

三个接口共用 **20 QPS** 的账号级限流。查询结果仅保留 24 小时，过期自动清理。

## 任务状态枚举

| 状态 | 说明 |
|------|------|
| `PENDING` | 排队中，尚未开始处理 |
| `RUNNING` | 处理中 |
| `SUCCEEDED` | 任务成功完成 |
| `FAILED` | 任务失败 |
| `CANCELED` | 任务已被取消 |
| `UNKNOWN` | 未知状态（通常因 task_id 过期） |

## 注意事项

- **task_id 有效期**为 24 小时，超时后查询返回 `UNKNOWN` 状态
- **地域一致性**：API Key、任务提交、结果查询、事件规则必须使用同一地域（北京 / 新加坡 / 弗吉尼亚）
- **权限范围**：只能查询和取消同一阿里云主账号下的任务（含其名下所有 API Key 提交的任务）
- 结果中的下载链接（如视频 URL、3D 模型 URL）通常有独立的过期时间（如 2 小时），需及时下载

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)
- [music generation references](../api/music-generation-references.md)


