# 异步任务

异步任务是阿里云百炼平台针对长耗时 AI 生成类 API（视频生成、图像生成、3D 生成、音乐生成、长语音识别等）提供的调用模型。客户端先提交任务获取 `task_id`，随后通过 `task_id` 查询或接收完成通知，避免单次 HTTP 请求因处理时间过长而超时。

## 通用调用流程

整个异步调用分两步完成：

1. **创建任务**：向对应模型的服务端点发起 `POST` 请求，请求头必须携带 `X-DashScope-Async: enable`，同时带上 `Authorization: Bearer $DASHSCOPE_API_KEY` 与 `Content-Type: application/json`。成功后返回 `task_id`。
2. **获取结果**：通过 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 轮询任务状态，或在任务完成时接收事件通知（详见下文"完成通知"）。

任务耗时通常在数十秒到数十分钟之间（例如视频生成 1–10 分钟、3D 生成数十秒），请勿重复提交相同任务。

## 任务状态

任务状态（`task_status`）在生命周期中按如下枚举流转：

| 状态 | 含义 |
| --- | --- |
| `PENDING` | 已受理，尚未开始执行 |
| `RUNNING` | 正在执行 |
| `SUCCEEDED` | 执行成功，`output` 中包含最终结果 |
| `FAILED` | 执行失败，`message` 中包含错误信息 |
| `CANCELED` | 已取消 |
| `UNKNOWN` | `task_id` 已过期或不存在 |

查询接口返回的结果**仅保留 24 小时**，超时后任务信息会被自动清理，因此务必在 24 小时内拉取并保存结果（包括模型产物 URL，部分模型如 3D 生成的下载链接有效期更短，仅 2 小时）。

## 任务管理 API

除模型自身的提交接口外，百炼提供一组通用的异步任务管理 API，方便在业务侧统一治理：

| 接口 | 方法/路径 | 用途 |
| --- | --- | --- |
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 拉取任务状态及结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 按 `start_time` / `end_time` / `model_name` / `status` 等条件批量检索 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅 `PENDING` 状态可取消，其他状态返回 `UnsupportedOperation` |

这三个接口共用**账号级 20 QPS** 的限流。权限上只能查询或取消**同一阿里云主账号**名下（含其所有 API Key 提交）的任务。

## 完成通知（替代轮询）

高频轮询既消耗业务侧资源，也容易触发查询接口的 20 QPS 限流。百炼已将异步任务接入**事件总线 EventBridge**：任务完成（无论成功或失败）会自动生成 `dashscope:System:AsyncTaskFinish` 事件，业务侧仅需**一次**拉取结果即可。支持两类事件目标：

- **HTTP 回调 URL**：业务方提供公网或 VPC 内可访问的 `POST` 接口接收 JSON 事件。配置简单，适合大多数场景。
- **云消息队列 RocketMQ**：事件转发至 RocketMQ Topic，业务方通过 PushConsumer 消费。保证消息不丢失并支持失败重试，适合高可靠性要求。

事件 Body 关键字段包括 `data.task_id`、`data.task_status`、`data.user_api_unique_key`、`data.region` 等。其中 `user_api_unique_key` 格式为 `apikey:version:group:task:function-call:model`，可用于事件模式过滤特定模型（例如按 `{\"suffix\": \":paraformer-8k-v1\"}` 过滤语音识别任务）。

配置步骤：在事件总线控制台查询事件 → 创建事件规则（事件源 `acs.dashscope`、事件类型 `dashscope:System:AsyncTaskFinish`）→ 选择 HTTP 或 RocketMQ 事件目标。需注意**事件规则的地域必须与任务地域一致**，否则不会收到转发。

## 关键参数与约定

异步任务在不同模型中遵循一组统一的约定：

- **请求头**：`X-DashScope-Async: enable` 必须显式设置，否则部分模型会报 "does not [support](../guides/support.md) synchronous calls" 错误。
- **请求体结构**：通常包含 `model`（模型名）、`input`（输入参数，如 `prompt`、媒体素材等）、`parameters`（生成参数，如 `resolution`、`duration`、`texture_quality` 等）。
- **Endpoint 与地域**：模型、Endpoint URL、API Key 必须属于同一地域（华北 2 北京、新加坡、美国弗吉尼亚、德国法兰克福等），跨地域调用会失败。新加坡/法兰克福等旧版 `dashscope-intl` 域名的 endpoint 正在下线，建议迁移至带 `WorkspaceId` 的新域名。
- **结果 URL 有效期**：任务返回的产物下载链接（视频、3D 模型、音频等）有效期从 2 小时到 24 小时不等，业务侧应在收到 `SUCCEEDED` 状态后立即下载或转存到自己的对象存储。

## 典型适用场景

异步任务模式覆盖百炼平台上绝大多数生成式模型：

- **视频生成**：万相 Wan、HappyHorse、可灵 Kling、Vidu、爱诗 PixVerse 等，耗时 1–10 分钟。
- **3D 生成**：Tripo 系列，文生 3D / 单图生 3D / 多图生 3D。
- **图像生成与编辑**：万相 V1/V2、万相 2.7、图像翻译、局部重绘、扩图、虚拟模特、创意海报等。
- **音乐生成**：Fun-Music 系列，支持非流式与 SSE 流式两种输出。
- **长语音识别**：Paraformer 等长音频转写任务。

对于这些场景，推荐优先配置 EventBridge 完成通知替代轮询，以降低查询接口压力并获得更及时的回调。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [music generation references](../api/music-generation-references.md)
- [more about models](../api/more-about-models.md)


