# 异步任务

异步任务是百炼平台中一类需“提交后轮询或监听事件”才能获取最终结果的模型调用模式，适用于计算密集、耗时较长（通常数秒至数分钟）的 AIGC 任务，如视频生成、3D 模型构建、文档/音视频解析等。它将请求发起与结果返回解耦，避免客户端长时间阻塞，提升系统吞吐与稳定性。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成**：所有视频类 API（文生视频、图生视频、口型替换、超分等）强制采用异步模式。开发者需先 `POST /video-generation/video-synthesis` 创建任务，获得 `task_id`，再通过 `GET /tasks/{task_id}` 轮询状态；任务 ID 有效期为 24 小时。
  
- **3D 生成**：Tripo 系列 3D 模型（如 `Tripo/Tripo-H3.1`）仅支持异步调用，必须携带 `X-DashScope-Async: enable` 请求头，否则直接报错；结果中的模型 URL（如 `pbr_model_url`）有效期仅 2 小时，需及时下载。

- **文档与音视频解析（ParseX）**：所有解析与字段抽取任务均基于异步任务模型，使用 `biz_id`（而非 `task_id`）作为任务标识。提交后需轮询 `/parse/result` 或 `/extract/result`，结果默认保留 30 天，但字段抽取仅可复用 7 天内的解析结果。

- **其他异步模型**：包括部分图像生成（如 `wanx2.1-t2i-turbo`）、语音转写（如 `paraformer-8k-v2`）等，统一纳入平台异步任务管理体系，支持通过事件总线（EventBridge）配置 HTTP 回调或 RocketMQ 消息通知，替代轮询。

> ✅ **关键共性**：所有异步任务均不支持同步返回；必须显式启用异步开关（如 `X-DashScope-Async: enable`）；任务标识（`task_id`/`biz_id`）是后续查询、取消、回调的唯一凭证；结果资源（URL）具有明确时效性，不可长期缓存。

## 关键参数和配置

| 参数 / 配置 | 说明 | 是否必需 | 注意事项 |
|-------------|------|----------|----------|
| `X-DashScope-Async: enable` | 强制启用异步模式的 HTTP 请求头 | 是（对所有异步模型） | 缺失将返回 `"current user api does not support synchronous calls"` 错误；大小写敏感，值必须为 `enable`（小写） |
| `task_id` / `biz_id` | 任务唯一标识符，由创建接口响应体返回 | 是（用于轮询/回调） | `task_id` 格式为 UUID（如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1`），`biz_id` 为业务自定义前缀（如 `parseX-xxx`）；有效期统一为 **24 小时**（ParseX 解析结果除外） |
| `callback_url`（可选） | 事件回调地址，用于接收任务完成/失败通知 | 否 | 需在创建任务时通过 `callback_url` 字段或事件总线控制台配置；推荐用于生产环境，避免轮询限流（20 QPS） |
| `polling_interval`（建议） | 轮询间隔 | 否（但强烈建议） | 文生图 ≥2s，图生视频/3D ≥10s，文档解析 ≥15s；高频轮询易触发限流或被拒绝 |

## 面向开发者，简洁实用

- ✅ **必做三件事**：  
  1. 请求头务必添加 `X-DashScope-Async: enable`；  
  2. 从创建响应中提取 `task_id` 或 `biz_id`，并妥善保存；  
  3. 使用该 ID 调用 `/tasks/{id}` 或 `/parse/result?biz_id=xxx` 查询状态（检查 `status` 字段：`success`/`failed`/`processing`）。

- ⚠️ **避坑提示**：  
  - 不同服务使用不同任务 ID 命名空间（`task_id` vs `biz_id`），不可混用；  
  - 所有异步任务严格绑定地域——API Key、Endpoint、模型必须同属一个地域（如 `cn-beijing`），跨地域调用必然失败；  
  - 结果 URL（如 `video_url`、`pbr_model_url`、`rendered_image_url`）均为临时链接，有效期从 **2 小时到 30 天不等**，请立即下载或持久化存储；  
  - 生产环境优先使用 **EventBridge 回调**，而非轮询：降低延迟、规避 QPS 限制、提升可靠性。

- 🚀 **进阶推荐**：  
  - 高并发场景下，结合 SDK 连接池（如 Python 的 `aiohttp.ClientSession`）复用 HTTP 连接；  
  - 敏感业务中，为每个子业务空间分配独立 API Key，并启用子空间模型授权隔离；  
  - 文件类输入（图片、视频、PDF）建议先调用 `/files/upload` 获取 `oss://` 临时 URL，再传入模型调用，避免超时失败。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)


