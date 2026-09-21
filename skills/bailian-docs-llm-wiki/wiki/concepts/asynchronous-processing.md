# 异步处理

异步处理是百炼平台对长耗时任务（如视频生成、大文件解析、批量推理等）的标准执行模式：客户端提交任务后立即获得任务标识，服务端在后台独立执行，客户端通过轮询或回调方式获取最终结果。该模式避免了 HTTP 连接长时间阻塞，提升了系统吞吐与稳定性。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成类 API**（如 `video-synthesis`）：所有视频模型（HappyHorse、万相系列、数字人驱动等）强制采用异步调用。请求必须携带 `X-DashScope-Async: enable` 头，成功响应返回 `task_id`；开发者需轮询 `/tasks/{task_id}` 或对应模型的任务查询接口，直至状态为 `SUCCESS`。`task_id` 有效期为 24 小时。

- **ParseX 文档解析与字段抽取**：`/parse/submit` 和 `/extract/submit` 接口均为异步设计，返回 `biz_id` 作为任务唯一标识。轮询 `/parse/result` 或 `/extract/result` 获取状态（`init` → `processing` → `success`/`failed`）。解析结果默认保留 30 天，但字段抽取复用时仅支持 7 天内的 `parsed_file_biz_id`。

- **通用模型 API**（LLM、多模态等）：通过请求体中显式设置 `"async": true`（部分模型也支持 `X-DashScope-Async: enable` 头），可将同步推理转为异步任务。适用于单次请求耗时可能超过 30 秒的场景（如超长文本生成、大图理解）。任务生命周期由 `/api/v1/tasks/{task_id}` 统一管理。

- **高级能力扩展**：支持配置 `callback_url` 实现服务端主动推送完成事件（需 HTTPS + 签名校验）；可通过 `task_group_id` 对一批异步任务进行分组管理；子业务空间调用同样兼容异步流程，只需确保 `X-DashScope-Workspace` 与 `workspace_id` 一致。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `task_id` / `biz_id` | 响应体 | string | 任务唯一标识，用于轮询或回调上下文，**不可重复使用**，不同服务命名习惯不同（视频用 `task_id`，ParseX 用 `biz_id`） |
| `X-DashScope-Async: enable` | 请求头 | string | 视频类 API **强制要求**，缺失将报错 `"current user api does not support synchronous calls"` |
| `"async": true` | 请求体 JSON | boolean | 通用模型 API 启用异步的推荐方式（部分旧接口仍支持 Header 形式） |
| `callback_url` | 请求体 | string | 可选，HTTPS 地址，服务端将在任务完成时发起 POST 回调（含签名头 `X-DashScope-Signature`，**必须校验**） |
| `task_group_id` | 请求体 | string | 可选，用于批量任务归类，便于后续按组查询或清理 |
| `expires_in`（临时 Key 场景） | 请求体 | integer | 临时凭证有效期（秒），不影响异步任务本身，但影响回调鉴权密钥时效 |

> ⚠️ 注意：  
> - 所有异步任务最大执行时长为 **10 分钟**，超时自动终止且不可续跑；  
> - 轮询建议采用指数退避策略（如初始 1s，逐步增至 5s），避免高频无效请求；  
> - `task_id` / `biz_id` 仅用于结果查询，**不可用于幂等控制**（幂等请使用 `X-DashScope-Request-ID` 或业务侧 `idempotency_key`）。

面向开发者：异步是百炼平台处理重计算任务的事实标准。请始终以“提交 → 标识 → 查询/监听”三步法设计集成逻辑，勿尝试同步等待。SDK（v3.12.0+）已内置异步任务封装与自动轮询工具，推荐优先使用。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [getting started overview](../guides/getting-started-overview.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)


