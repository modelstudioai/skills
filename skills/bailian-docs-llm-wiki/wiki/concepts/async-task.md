# 异步任务

异步任务是百炼平台处理长耗时 AI 生成请求的核心调用模式。客户端提交任务后立即获得 `task_id`，随后通过轮询或事件通知获取最终结果，避免了同步等待导致的连接超时问题。

## 适用场景

百炼平台中以下能力均采用异步任务模式：

- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、数字人驱动等全部视频类任务
- **3D 模型生成**：文生 3D、单图生 3D、多图生 3D（Tripo 模型）
- **图像生成与编辑**：文生图、图像编辑、局部重绘、背景生成、虚拟模特等
- **音乐生成**：Fun-Music 系列模型的非流式调用
- **长语音识别**：大文件语音转文字

## 调用流程

### 步骤 1：创建任务

向对应模型的服务端点发送 POST 请求，必须携带请求头：

```
X-DashScope-Async: enable
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```

> 缺少 `X-DashScope-Async: enable` 请求头会导致报错 "current user api does not [support](../guides/support.md) synchronous calls"。

成功后返回 `task_id`，有效期 24 小时。

### 步骤 2：获取结果

有两种方式获取任务结果：

**方式一：轮询查询**

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔 15 秒。查询接口受 20 QPS 账号级限流。

**方式二：事件通知（推荐）**

通过阿里云事件总线 EventBridge 接收 `dashscope:System:AsyncTaskFinish` 事件，支持：
- HTTP 回调 URL：业务方提供 POST 接口接收 JSON 事件
- 云消息队列 RocketMQ：保证消息不丢失，支持失败重试

使用事件通知可避免高频轮询带来的限流风险，业务侧仅需一次拉取结果。

## 任务状态

| 状态 | 说明 |
|------|------|
| `PENDING` | 排队等待执行 |
| `RUNNING` | 正在执行 |
| `SUCCEEDED` | 执行成功，可获取结果 |
| `FAILED` | 执行失败 |
| `CANCELED` | 已取消（仅 PENDING 状态可取消） |
| `UNKNOWN` | task_id 已过期或无效 |

## 任务管理 API

百炼提供通用的异步任务管理接口（与具体模型无关）：

| 接口 | 方法与路径 | 说明 |
|------|-----------|------|
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 获取任务状态及结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 支持按时间、模型名、状态过滤 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持 PENDING 状态 |

三个接口共享 20 QPS 的账号级限流。

## 关键限制

- **task_id 有效期**：24 小时，过期后查询返回 `UNKNOWN`
- **结果保留时间**：24 小时（具体以模型文档为准），过期自动清理
- **下载链接有效期**：因模型而异，通常为 2~24 小时，需及时转存
- **权限范围**：只能查询/取消同一阿里云主账号下的任务
- **地域一致性**：EventBridge 事件规则的地域必须与任务提交地域一致
- **请勿重复创建**：获取 task_id 后轮询即可，避免重复提交相同任务

## 最佳实践

1. 优先使用 EventBridge 事件通知替代轮询，降低限流风险
2. 轮询间隔不低于 15 秒，避免触发 QPS 限制
3. 获取结果后立即将文件转存到自有 OSS，不依赖临时下载链接
4. 利用批量查询接口统一管理大量并发任务的状态
5. 在事件规则中通过 `user_api_unique_key` 的后缀匹配过滤特定模型的事件

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)
- [music generation references](../api/music-generation-references.md)
- [image generation](../api/image-generation.md)


