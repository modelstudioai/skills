# 异步调用

异步调用是百炼平台对长耗时模型任务（如视频生成、3D建模、大图渲染、语音转写等）的标准交互范式：客户端发起请求后立即返回任务标识 `task_id`，不阻塞等待结果；后续通过轮询或事件通知方式获取最终输出。该模式解耦请求与响应，保障服务稳定性与资源利用率。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成类 API**（如 HappyHorse、万相、爱诗、可灵、Vidu、MiniMax 等）：所有接口强制启用异步模式，必须在请求头中显式设置 `X-DashScope-Async: enable`，否则返回错误 `"current user api does not support synchronous calls"`。调用成功后返回 `task_id`，需轮询 `/api/v1/tasks/{task_id}` 获取状态与 `output.video_url`。

- **3D 生成类 API**（基于 Tripo 模型）：全部能力（文/图生3D、Gaussian Splatting、网格分割、绑骨、重定向等）均仅支持异步调用，且**严格限定华北2（北京）地域**。同样依赖 `X-DashScope-Async: enable` 头，并通过 `task_id` 查询任务状态（`PENDING → RUNNING → SUCCEEDED/FAILED`）。

- **其他长耗时模型**（如图像生成 `wanx2.1-t2i-turbo`、语音转写 `paraformer-16k-1`）：归类为“异步模型”，统一由平台级异步任务管理 API（`/api/v1/tasks/{task_id}`）支撑，支持查询、批量列表和取消（仅限 `PENDING` 状态）。推荐结合事件总线（HTTP 回调或 RocketMQ）替代轮询，避免限流与资源浪费。

> ✅ 共同特征：  
> - 所有异步调用均要求 `Authorization: Bearer <API_KEY>` 与请求参数严格同地域；  
> - `task_id` 有效期统一为 **24 小时**（任务完成后数据自动清理）；  
> - 不支持同步返回结果，强行省略异步头将直接报错。

## 关键参数和配置

| 参数 / 配置项 | 说明 | 是否必需 | 示例值 |
|----------------|------|-----------|---------|
| `X-DashScope-Async` 请求头 | 显式声明启用异步模式 | ✅ 必须 | `enable` |
| `task_id` | 任务唯一标识，用于后续轮询或事件消费 | ✅ 返回字段 | `task-abc123xyz456` |
| 轮询间隔 | 建议按任务类型差异化设置，避免高频触发限流 | ⚠️ 推荐 | 视频/3D类 ≥15s；图像类 ≥5s；文本向量类 ≥1s |
| 事件回调配置 | 替代轮询的推荐方案，需在控制台或 API 中注册 HTTP URL 或 RocketMQ Topic | ❌ 可选 | `https://your-domain.com/webhook` |
| `expire_in_seconds`（临时 Key 场景） | 若使用临时 API Key 调用异步任务，其有效期影响任务生命周期 | ⚠️ 注意 | 默认 60 秒，建议设为 ≥120 秒以覆盖典型任务排队时间 |

> 💡 提示：  
> - 跨地域调用（如用杭州 API Key 请求北京模型）将失败，务必校验 `region` 与 `API_KEY` 地域一致；  
> - 使用子业务空间时，`task_id` 仅在其所属空间内有效，不可跨空间查询；  
> - 异步任务不支持流式响应，所有输出均为最终态 JSON 结构（含 `output` 字段及元数据）。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)


