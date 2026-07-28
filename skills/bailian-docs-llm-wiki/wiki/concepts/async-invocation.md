# 异步调用

异步调用是百炼平台针对耗时较长的模型任务（如图像、视频、3D 生成）提供的一种调用机制：客户端先提交任务获得 `task_id`，再通过轮询或事件通知获取最终结果，从而避免长时间占用连接导致的请求超时。

## 基本流程

异步调用统一遵循"创建任务 → 查询结果"两步：

1. **创建任务**：向业务接口发起 POST 请求，HTTP 请求头中添加 `X-DashScope-Async: enable`（部分仅支持异步的接口若缺少该头会报错 `current user api does not support synchronous calls`）。响应返回 `output.task_id` 和初始状态 `PENDING`。
2. **查询结果**：调用通用任务查询接口获取状态与产物：

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

任务状态流转为：

```
PENDING → RUNNING → SUCCEEDED / FAILED
```

其他状态包括 `CANCELED`（已取消）和 `UNKNOWN`（任务不存在或已超过保留期）。建议轮询间隔 15 秒左右，查询接口默认[限流](rate-limit.md)约 20 QPS/RPS。

## 在不同场景中的使用

- **图像生成**：千问图像、万相 2.6+、Z-Image 等新版模型推荐同步调用；万相 2.5 及以下、可灵（Kling）、Vidu 等图像模型采用异步模式。
- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、数字人等所有视频类 API 统一采用异步任务模式（万相、HappyHorse、PixVerse、Vidu 等系列均是如此）。
- **3D 生成**：Tripo 系列（文生3D/单图生3D/多图生3D）仅支持异步调用，且仅限华北2（北京）地域；`task_id` 有效期 24 小时，产物 URL 有效期仅 2 小时，需及时下载。
- **应用调用**：OpenAI 兼容的 Responses API 通过设置 `background=true` 开启异步执行，适合生成报告、多步骤工具调用等长耗时任务；DashScope 应用 API 暂不支持异步。

## 任务管理 API

百炼提供三个通用的异步任务管理接口（均[限流](rate-limit.md) 20 QPS，主账号维度）：

| 操作 | 接口 | 说明 |
| --- | --- | --- |
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 返回 `output.task_status` 及结果；已完成任务通常保留 24 小时 |
| 批量查询 | `GET /api/v1/tasks/?start_time=...&end_time=...&status=...` | 支持按时间范围、模型、状态过滤，单次跨度不超过 24 小时 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅可取消 `PENDING` 状态的任务 |

## 任务完成通知（替代轮询）

频繁轮询浪费资源且易触发[限流](rate-limit.md)。百炼已接入阿里云事件总线 EventBridge，任务完成后可主动推送通知：

| 方案 | 适用场景 | 特点 |
| --- | --- | --- |
| HTTP 回调 URL | 通用场景 | 需公网或 VPC 可达的 HTTP 接口，接入简单 |
| RocketMQ | 消息可靠性要求高 | 无丢失、支持失败重试，需开通 RocketMQ 实例 |

事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`；收到通知后根据事件体中的 `data.task_id` 调用一次查询接口即可获取结果。

## 关键注意事项

- 创建任务后请保存 `task_id`，切勿因未及时收到结果而重复创建任务。
- 任务及产物有保留期限：任务记录一般保留 24 小时，生成的文件 URL（如 3D 模型、渲染图）可能仅 2 小时有效，应尽快下载转存。
- 部分接口需替换 Endpoint 中的 `{WorkspaceId}`，并使用对应地域的 API Key。
- 控制轮询频率，或优先采用 EventBridge 通知方案，避免触发限流。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)
- [application call](../api/application-call.md)


