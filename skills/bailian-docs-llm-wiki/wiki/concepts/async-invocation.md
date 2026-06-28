# 异步调用

异步调用是百炼平台处理耗时模型任务的统一调用模式：先通过创建任务接口拿到 `task_id`，再通过查询接口轮询或经事件总线接收完成通知，最终取回生成结果。它适用于图像生成、视频生成、3D 资产生成等单次请求耗时较长（数十秒到数分钟）的场景，避免长连接占用与超时。

## 在百炼平台的使用场景

异步调用贯穿多个生成类 API，但具体接口路径与模型支持略有差异：

- **图像生成**：V1 版及部分编辑/创意类模型（如 wan2.5-t2i-preview、wanx2.0/2.1/2.2 系列、wanx-v1、可灵图像）仅支持异步；千问图像系列、万相 2.6/2.7、Z-Image 等新版模型支持同步调用。创建任务走图像生成对应端点，查询走通用任务接口。
- **视频生成**：所有视频生成 API（万相 HappyHorse/Wan/wanx、爱诗 PixVerse、Vidu、可灵等）统一采用异步模式，任务通常耗时 1–5 分钟，视频编辑类约 5–10 分钟。创建任务向 `POST /api/v1/services/aigc/video-generation/video-synthesis`（部分模型走 `image2video/video-synthesis`）提交。
- **3D 生成**：基于 Tripo 模型的文生/图生/多图生 3D 全部走异步，创建任务端点为 `POST /api/v1/services/aigc/video-generation/3d-generation`，生成高精度模型可能耗时更长，轮询间隔建议约 15 秒。
- **应用调用**：百炼应用（智能体、工作流、Agent 2.0）在 OpenAI 兼容 Responses API 模式下，通过 `background` 参数（默认 `false`）选择是否异步执行；异步执行暂不支持[流式输出](streaming-output.md)。

## 标准调用流程

异步调用固定为两步：

1. **创建任务**：向对应模型的创建接口提交请求，响应中返回 `task_id`。
2. **查询结果**：调用 `GET /api/v1/tasks/{task_id}` 轮询任务状态，直到拿到最终结果。

`task_id` 有效期通常为 24 小时，超时后状态返回 `UNKNOWN` 且无法再查询。**请勿重复创建相同任务**，直接用已有 `task_id` 轮询即可，避免浪费配额。

任务状态流转为：`PENDING`（排队中）→ `RUNNING`（处理中）→ `SUCCEEDED` / `FAILED` / `CANCELED` / `UNKNOWN`。含多个子任务的任务，只要有一个子任务成功，整体状态即为 `SUCCEEDED`，失败子任务的错误信息在 `output.results` 中单独展示，`task_metrics` 给出 `TOTAL`/`SUCCEEDED`/`FAILED` 统计。

## 关键参数与请求头

创建异步任务时必须携带以下请求头，否则会报错 `current user api does not support synchronous calls`：

| 请求头 / 参数 | 必填 | 说明 |
| --- | --- | --- |
| `Authorization: Bearer $DASHSCOPE_API_KEY` | 是 | 使用百炼 [API Key](api-key.md) 鉴权 |
| `Content-Type: application/json` | 是 | 请求体格式 |
| `X-DashScope-Async: enable` | 是 | 标识为异步调用，缺少会直接报错 |
| `X-DashScope-WorkSpace` | 视情况 | RAM 子账号或子[业务空间](workspace.md)调用时需指定[业务空间](workspace.md) |
| `background`（应用 Responses API） | 否 | 默认 `false` 同步；设为 `true` 走异步 |

应用调用的 OpenAI 兼容模式中，异步通过 `background` 参数控制，而非 `X-DashScope-Async` 头。

## 结果获取：轮询与通知

- **轮询方案**：接入简单，适合低并发场景。查询接口 `GET /api/v1/tasks/{task_id}` 默认限流 20 QPS（按主账号 + 子账号维度计算），建议轮询间隔 15 秒左右。
- **通知方案**：百炼已接入事件总线 EventBridge，任务完成（无论成功或失败）后主动上报事件 `dashscope:System:AsyncTaskFinish`（事件源 `acs.dashscope`），推送到您配置的 HTTP 回调 URL 或 RocketMQ 消息队列，收到通知后查询一次即可拿结果。通知方案不限流、实时性高，适合高并发或对实时性要求高的任务。

事件 `data` 包含 `task_id`、`task_status`、`start_time`、`end_time`、`region`、`request_id`、`api_key_id`、`user_api_unique_key` 等字段，可在事件总线控制台创建事件规则按这些字段过滤（例如只转发某个模型的事件）。

## 通用异步任务管理接口

除模型自身的创建接口外，百炼提供一组通用任务管理接口（限流均为 20 QPS）：

| 接口 | 方法与路径 | 用途 |
| --- | --- | --- |
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 根据 task_id 查询状态与结果 |
| 批量查询 | `GET /api/v1/tasks/` | 按 time/status/model 等条件分页查询，时间窗口跨度不超过 24 小时 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持 `PENDING` 状态的任务，其他状态返回 `UnsupportedOperation` |

接口可查询/取消当前 [API Key](api-key.md) 所属主账号下的所有任务（含该主账号下任意 [API Key](api-key.md) 提交的任务），但无法跨主账号操作。

## 注意事项

- 模型、Endpoint URL、API Key 必须属于同一地域，跨地域调用会鉴权失败。华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立的 API Key 与请求地址，不可混用。建议使用[业务空间](workspace.md)专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以获得更好性能与稳定性。
- 异步任务完成后通常保留 24 小时（以对应模型 API 文档为准），超时自动清理。
- 产物下载链接有效期较短（如 3D 生成产物约 2 小时），请及时下载。
- 取消接口仅对 `PENDING` 状态生效；`RUNNING` 及之后的状态不可取消。

## 关联主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [more about models](../api/more-about-models.md)
- [application call](../api/application-call.md)


