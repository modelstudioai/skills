# 异步任务

异步任务是百炼平台中用于处理耗时较长、无法即时返回结果的模型推理操作的核心执行模式。它将任务提交与结果获取解耦，开发者通过创建任务获取唯一标识（如 `task_id` 或 `biz_id`），再通过轮询或事件回调方式获取最终输出，适用于视频生成、3D建模、文档/音视频解析等计算密集型场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成（`video-generation-api`）**：所有视频生成任务均为强制异步，必须设置请求头 `X-DashScope-Async: enable`，否则报错；调用 `/api/v1/services/aigc/video-generation/video-synthesis` 创建任务，获得 `task_id` 后轮询 `/api/v1/tasks/{task_id}` 获取状态，典型耗时 1–5 分钟。
  
- **3D生成（`3d-generation`）**：Tripo 全链路能力（生成、后处理、动画）均采用统一异步流程，仅支持华北2（北京）地域；需严格匹配 API Key 地域，并通过 `task_id` 轮询，建议首次延迟 10 秒、后续每 15–30 秒查询一次。

- **图像生成（`image-generation`）**：部分模型（如 `wanx2.1-t2i-turbo`）明确标注为异步，但多数主流图像模型（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`）默认支持同步调用；是否启用异步由模型能力决定，非用户可选配置。

- **文档与音视频解析（`api-overview`）**：ParseX 所有接口（`/parse/submit`、`/extract/submit`）均为异步，返回 `biz_id` 作为任务句柄；注意 `biz_id` 类型隔离——解析类 `biz_id` 仅可用于 `/parse/result`，抽取类仅可用于 `/extract/result`。

- **通用异步管理（`more-about-models`）**：平台提供统一的异步任务生命周期管理能力，包括任务查询（单查/批量）、取消（仅限 `PENDING` 状态）、状态监听（HTTP 回调或 RocketMQ 事件总线），推荐优先使用事件通知替代轮询以降低延迟与资源消耗。

## 关键参数和配置

- **必需请求头**：
  - `X-DashScope-Async: enable`：显式声明启用异步模式，缺失将导致 `"current user api does not support synchronous calls"` 错误（视频、3D、ParseX 等均强制要求）。
  - `Authorization: Bearer <your_api_key>`：地域敏感，必须与目标服务所在地域一致（如北京地域模型不可用新加坡 Key）。

- **核心标识符**：
  - `task_id`：UUID 格式字符串（如 `a8532587-...-0c46b17950d1`），24 小时有效，用于 `/api/v1/tasks/{task_id}` 查询；由 `/submit` 接口响应体直接返回。
  - `biz_id`：ParseX 系统专用任务 ID（如 `parseX-Video-2026xxxx-xxxxxxx`），按业务类型分域，不可跨接口复用。

- **可选增强配置**：
  - `X-DashScope-OssResourceResolve: enable`：当输入为临时 OSS URL（如上传文件后生成的 `oss://` 地址）时必须添加，否则模型无法访问资源。
  - HTTP 回调配置（见 `more-about-models`）：在创建任务时指定 `callback_url`，平台将在任务完成时推送 `dashscope:System:AsyncTaskFinish` 事件，支持 `contain_result=true` 直接内嵌结果，避免二次查询。

## 面向开发者，简洁实用

- ✅ **必做**：检查模型文档是否标注“异步”，若标注则必须加 `X-DashScope-Async: enable`；确认 API Key 与服务地域一致；保存好 `task_id` 或 `biz_id` 并在 24 小时（或 30 天/7 天，依服务而定）内完成查询。
- ⚠️ **避坑**：
  - 不要重复提交相同任务（文档多次强调“请勿重复创建任务”，将被拒绝）；
  - 不要混用 `biz_id` 类型（解析 vs 抽取）或跨地域调用；
  - 异步任务不支持 OpenAI 兼容模式下的 `/v1/images/generations` 同步路径，需改用百炼原生异步接口。
- 🚀 **推荐实践**：
  - 高并发场景下，使用事件回调（HTTP 或 MQ）替代轮询，降低客户端压力；
  - 轮询时采用指数退避（如 1s → 2s → 4s → 8s），避免高频无效请求；
  - 利用 DashScope SDK（Python/Java）自动处理重试、连接复用与临时文件上传，减少胶水代码。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)


