# 异步任务调用

异步任务调用是百炼平台中一种通用的 API 交互模式，适用于耗时较长的生成类任务。调用方提交请求后立即获得任务标识，随后通过轮询查询任务状态与结果，避免长时间阻塞连接。

## 工作原理

异步任务调用遵循"创建任务 -> 轮询结果"两步模式：

1. **创建任务**：向对应 API 端点发送 POST 请求，服务端立即返回 `task_id`，不等待任务完成。
2. **轮询结果**：使用 `task_id` 调用查询接口，获取任务状态和最终结果。任务状态通常按 `PENDING` -> `RUNNING` -> `SUCCEEDED` / `FAILED` 流转。

这一模式的核心优势在于：调用方无需维持长连接等待生成完成，可以并行提交多个任务，按各自节奏获取结果。

## 适用场景

异步任务调用在百炼平台中广泛应用于以下场景：

- **图像生成**：所有图像生成 API（千问图像、万相、Z-Image、可灵等）均采用异步调用，文生图、图像编辑、风格迁移等任务通常在数秒到数十秒内完成。
- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、人像动画等视频生成任务耗时通常为 1-5 分钟，异步模式可避免超时。
- **3D 模型生成**：通过 Tripo 模型进行文生 3D、单图生 3D、多图生 3D，建议轮询间隔 15 秒。
- **应用调用**：Responses API 支持通过 `background=true` 参数开启异步模式，适用于耗时较长的智能体任务（如生成报告、多步骤工具调用）。
- **模型生产**：模型调优（微调训练）、模型压缩和模型部署均为异步操作，需轮询或回调获取任务状态。

## 关键参数与配置

### 请求头

对于 DashScope 原生 API，异步调用需要设置以下请求头：

| 请求头 | 值 | 说明 |
|--------|------|------|
| `X-DashScope-Async` | `enable` | 启用异步模式，必须设置，否则报错 |
| `Authorization` | `Bearer $DASHSCOPE_API_KEY` | API Key 认证 |
| `Content-Type` | `application/json` | 固定值 |

> 对于 Responses API（OpenAI 兼容协议），异步模式通过请求体中的 `background=true` 参数开启，无需设置 `X-DashScope-Async` 请求头。

### task_id

- 创建任务成功后返回，是后续查询、取消任务的唯一标识。
- 有效期为 **24 小时**，超时后无法查询结果，状态返回 `UNKNOWN`。
- 请勿对同一请求重复创建任务，应复用已有的 `task_id`。

### 任务状态

| 状态 | 含义 |
|------|------|
| `PENDING` | 任务已提交，排队等待执行 |
| `RUNNING` | 任务正在执行中 |
| `SUCCEEDED` | 任务执行成功，可获取结果 |
| `FAILED` | 任务执行失败，可查看错误信息 |

> Responses API 的异步任务状态略有不同，使用 `queued`、`running`、`completed`、`failed`、`cancelled`。

### 查询接口

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔根据任务类型调整：图像生成 3-5 秒，视频和 3D 生成 10-15 秒。查询接口默认 RPS 为 20。

## 与同步调用的对比

| 维度 | 同步调用 | 异步调用 |
|------|----------|----------|
| 响应方式 | 等待任务完成后返回结果 | 立即返回 task_id |
| 适用场景 | 实时对话、快速推理 | 图像/视频/3D 生成、模型训练等耗时任务 |
| 超时风险 | 任务耗时过长可能超时 | 无超时风险 |
| 并发控制 | 受连接数限制 | 可并行提交多个任务 |
| [流式输出](streaming.md) | 支持 | 部分场景不支持（如 Responses API 异步模式） |

## 注意事项

- 异步任务的结果（如图片 URL、3D 模型下载链接）通常有时效性，需在有效期内下载保存。例如 3D 模型下载链接有效期仅 2 小时。
- 不同模型的异步任务请求路径可能不同，请参考对应模型的 API 文档确认端点地址。
- Responses API 的异步模式暂不支持[流式输出](streaming.md)。
- 模型部署产生的在线服务会持续占用资源，不再使用时应及时下线。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [application call](../api/application-call.md)
- [model production](../api/model-production.md)


