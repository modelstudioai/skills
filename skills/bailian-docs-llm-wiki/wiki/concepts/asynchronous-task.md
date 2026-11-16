# 异步任务模式

异步任务模式是百炼平台为长耗时、高资源消耗的 AI 任务（如视频生成、3D 建模、大文件音视频解析、批量语音转写等）设计的标准调用范式：客户端通过一次请求提交任务并立即获得唯一 `task_id`，后续通过轮询或事件回调方式获取最终结果，避免阻塞式等待。

## 在百炼平台的不同场景中，这个概念如何使用

该模式广泛应用于以下五类核心能力，统一采用「提交 → 查询/监听 → 获取结果」三阶段流程：

- **视频生成（Video Generation）**：所有模型（HappyHorse、万相、PixVerse、Vidu、Kling 等）均强制启用异步。需设置请求头 `X-DashScope-Async: enable`，调用 `/api/v1/services/aigc/video-generation/video-synthesis` 创建任务，再通过 `/api/v1/tasks/{task_id}` 轮询状态，成功后返回 `output.video_url`。
  
- **文档与音视频解析（ParseX API）**：文档解析、音视频分析、结构化字段抽取全部基于异步任务模型。提交后返回 `biz_id`（等效于 `task_id`），通过 `/api/v2/apps/parse-x/parse/result` 或 `/extract/result` 查询，状态字段为 `data.status`（`processing` / `success` / `failed`）。

- **3D 生成（Tripo）**：文生/图生 3D 网格、Gaussian Splatting、后处理及动画绑定等全链路操作均仅支持异步。必须指定华北2（北京）地域 Endpoint，并携带 `X-DashScope-Async: enable`；`task_id` 有效期严格为 24 小时，建议首次查询延迟 10 秒，后续轮询间隔 15–30 秒。

- **音频处理（Audio API）**：长音频转写（如 `Qwen-Audio-ASR-Filetrans`）、批量 TTS 合成等场景采用异步模式。同步接口（如短音频 ASR）适用于低延迟场景，而 `Filetrans` 类必须启用 `X-DashScope-Async: enable` 并轮询 `/api/v1/tasks/{task_id}`。

- **通用异步任务管理（More About Models）**：平台提供统一的异步任务生命周期管理能力，支持跨模型查询、取消、结果拉取。开发者可通过 `/api/v1/tasks/{task_id}` 获取任意异步任务状态（含错误详情、耗时、输入摘要），也可配置 HTTP 回调或 RocketMQ 消息通知替代轮询，提升系统响应效率。

> ✅ 共性要点：  
> - 所有异步调用**必须显式声明** `X-DashScope-Async: enable` 请求头；  
> - `task_id`（或 `biz_id`）是唯一任务标识，**不可复用、不可跨地域共享**；  
> - 任务结果默认保留期为 **24 小时（视频/3D）或 30 天（ParseX 解析结果）**，超期后无法查询；  
> - 推荐优先使用**事件回调（HTTP/RocketMQ）** 替代高频轮询，避免触发 QPS 限流（平台默认轮询限速 20 QPS）。

## 关键参数和配置

| 参数 | 作用 | 是否必需 | 说明 |
|------|------|----------|------|
| `X-DashScope-Async` | 启用异步模式 | ✅ 必需 | 请求头，值固定为 `enable`；缺失将导致 400 错误或降级为同步（若模型支持） |
| `task_id` / `biz_id` | 任务唯一标识 | ✅ 返回值 | 创建任务后由服务端返回，用于后续查询或回调上下文；24 小时内有效 |
| `workspace_id` & `region` | 路由与隔离依据 | ✅ 必需（子空间场景） | 所有异步请求 URL 必须包含业务空间 ID 和地域（如 `cn-beijing`），否则报错 |
| `Authorization: Bearer <API_KEY>` | 鉴权凭证 | ✅ 必需 | API Key 必须与 `workspace_id` 和 `region` 地域一致，跨地域 Key 将拒绝访问 |

> ⚠️ 注意：  
> - 不同服务对 `task_id` 的命名略有差异（如 ParseX 使用 `biz_id`），但语义与行为完全一致；  
> - 异步任务不支持 OpenAI 兼容模式，仅限百炼原生 API 协议；  
> - 若需调试，可配合百炼 CLI 命令快速验证：`bl tasks get --task-id <id>`（需安装最新版 CLI）。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [api overview](../api/api-overview.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)
- [audio api directory](../api/audio-api-directory.md)


