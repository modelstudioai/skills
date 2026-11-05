# 异步调用

异步调用是百炼平台对长耗时、高资源消耗类模型任务（如文档/音视频解析、视频生成、3D建模等）采用的标准交互模式：客户端提交任务后立即返回唯一任务标识（如 `biz_id` 或 `task_id`），不阻塞等待结果；后续通过轮询查询或事件回调方式获取最终输出。该模式解耦请求与响应，保障服务稳定性与高并发能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **文档与音视频解析（ParseX）**：调用 `/parse/submit` 或 `/extract/submit` 接口提交任务，返回 `biz_id`；再通过 `/parse/result?biz_id=xxx` 或 `/extract/result?biz_id=xxx` 轮询状态（`init` → `processing` → `success`/`failed`）。解析结果默认保留 30 天，抽取复用需在 7 天内。
  
- **视频生成（Video Generation）**：所有视频 API（万相、PixVerse、Vidu、Kling 等）强制启用异步模式，请求头必须携带 `X-DashScope-Async: enable`；成功响应返回 `task_id`，需调用通用任务查询接口 `/api/v1/tasks/{task_id}` 获取结果。注意：未带该 Header 将直接报错 `"current user api does not support synchronous calls"`。

- **3D 生成（Tripo）**：全部接口均为异步，同样要求 `X-DashScope-Async: enable` 请求头；任务创建后返回 `task_id`，通过统一任务管理接口轮询；**仅支持华北2（北京）地域**，且 Endpoint 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。

- **其他异步模型**：包括图像生成（如 `wanx2.1-t2i-turbo`）、语音转写（`paraformer-16k-1`）等，均纳入统一异步任务管理体系，支持任务查询（`/api/v1/tasks/{task_id}`）、批量列表（`/api/v1/tasks`）和取消（仅限 `PENDING` 状态）。

> ✅ **最佳实践**：避免高频轮询（默认限流 20 QPS/账号），建议按任务类型设置合理间隔——视频/3D 类任务推荐 3–10 秒轮询，文档解析可设为 1–2 秒；生产环境强烈推荐配置 HTTP 回调 URL 或接入 EventBridge，由平台主动推送 `TASK_COMPLETED` 事件，彻底规避轮询开销与限流风险。

## 关键参数和配置

| 参数 | 位置 | 是否必填 | 说明 |
|------|------|----------|------|
| `X-DashScope-Async` | HTTP 请求头 | 是（视频、3D、通用异步任务） | 值必须为 `"enable"`；缺失或值错误将导致调用失败。ParseX 类接口虽未显式要求此 Header，但其 `biz_id` 机制本质等价于异步语义。 |
| `biz_id` / `task_id` | 响应体（JSON） | 是（返回值） | 任务唯一标识符，用于后续结果查询或管理操作；生命周期依服务而异（ParseX 的 `biz_id` 有效期与结果保留期一致；通用 `task_id` 默认 24 小时）。 |
| `model` | 请求体 JSON | 是（视频、3D、通用异步任务） | 明确指定模型全名（如 `wanx3.0-video-generation`、`Tripo/Tripo-H3.1`），决定输入格式、能力边界与计费策略。 |
| `callback_url` | 请求体 JSON（可选） | 否 | 配置 HTTP 回调地址，任务完成后平台将 POST 结果到该 URL（含签名验证），替代轮询；需确保公网可达且能处理重复通知。 |

> ⚠️ 注意：异步任务不支持同步返回结果；若误用同步 SDK 方法（如 `client.chat.completions.create(..., stream=False)`）调用异步模型，将触发协议不匹配错误。请始终使用对应异步接口路径与参数规范。

## 面向开发者，简洁实用

- **一句话判断是否为异步任务**：看接口文档是否提及“轮询”、“`task_id`”、“`biz_id`”、“`X-DashScope-Async`”，或明确标注“异步模型”。
- **调试技巧**：CLI 中 `bl video-synthesis submit` 支持 `--wait` 参数自动轮询至完成；其他异步任务建议先用 `curl` 提交，再用 `bl task fetch --task-id xxx` 快速验证。
- **错误排查重点**：
  - `400 Bad Request` + `"X-DashScope-Async header is required"` → 检查 Header 拼写与值；
  - `404 Not Found` → 确认 Endpoint 地域与 WorkspaceId 匹配，且模型已开通；
  - `429 Too Many Requests` → 降低轮询频率，或改用回调；
  - `TASK_EXPIRED` / `ParseResultExpired` → 检查任务 ID 生命周期与结果保留策略。
- **生产就绪建议**：启用回调 + 本地任务状态缓存 + 重试退避（指数退避至最大 30 秒），并监控 `task_status` 变更链路完整性。

## 关联主题页

- [api overview](../api/api-overview.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)


