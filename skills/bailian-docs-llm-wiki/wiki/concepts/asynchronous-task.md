# 异步任务

异步任务是百炼平台对长耗时模型调用（如文档/音视频解析、视频生成、3D建模、大文件翻译等）采用的标准执行模式：用户提交请求后立即获得唯一任务标识符（`task_id` 或 `biz_id`），平台后台异步执行计算，用户通过轮询或事件通知方式获取最终结果。该模式解耦请求与响应，避免连接超时，保障高可靠性与资源弹性。

## 在百炼平台的不同场景中，这个概念如何使用

- **文档与音视频解析（ParseX）**：所有解析和字段抽取任务均强制异步。提交后返回 `biz_id`，需轮询 `/parse/result` 或 `/extract/result` 接口查询状态；结果默认保留 30 天，但仅前 7 天可被抽取任务复用。
- **视频生成（Video Generation）**：全部模型（HappyHorse、万相、爱诗、可灵、Vidu 等）必须启用异步模式，请求头必须包含 `X-DashScope-Async: enable`，响应返回 `task_id`，通过 `GET /api/v1/tasks/{task_id}` 查询；任务有效期统一为 24 小时。
- **3D 生成（Tripo）**：全链路（文/图生3D、后处理、动画绑定等）仅支持异步，且**仅限华北2（北京）地域**；同样需设置 `X-DashScope-Async: enable` 请求头，`task_id` 用于轮询及取消操作。
- **Qwen-MT-Uni 翻译**：提供同步与异步双模式。文本或小文件（≤100 MB）推荐同步调用；PDF/DOCX/PPTX/长音频等大内容**必须异步**——添加 `X-DashScope-Async: enable` 后获取 `task_id`，再轮询 `/api/v1/tasks/{task_id}`；下载链接（`TranslatedFileUrl`）有效期也为 24 小时。
- **通用异步任务管理**：所有异步任务统一由 `/api/v1/tasks` 接口族管理，支持单任务查询、批量列表（`/tasks?status=...`）和主动取消（`POST /tasks/{task_id}/cancel`）。开发者可选择轮询（建议间隔 ≥1s）或配置 HTTP 回调/RocketMQ 事件总线接收 `dashscope:System:AsyncTaskFinish` 事件，实现零轮询的主动通知。
- **RAG 知识库构建**：虽 RAG 运行时接口（检索/问答）为同步，但知识库的**文档导入、切片构建、索引更新等后台作业均为异步任务**，其生命周期也受 `/api/v1/tasks` 统一管控，可通过 `task_id` 跟踪进度。

## 关键参数和配置

- **必需请求头**：
  - `X-DashScope-Async: enable`：所有异步模型接口的硬性要求，缺失将直接报错 `"current user api does not support synchronous calls"`。
  - `Authorization: Bearer <API_KEY>`：百炼标准鉴权方式，API Key 需与目标地域（如北京、新加坡）匹配。

- **核心标识符**：
  - `task_id`：视频生成、3D、Qwen-MT-Uni、通用任务管理等场景使用的 UUID 格式任务 ID。
  - `biz_id`：ParseX 解析与抽取任务专用的任务 ID，语义等同于 `task_id`，但命名不同。

- **轮询与结果获取**：
  - 统一查询接口：`GET https://{WorkspaceId}.{Region}.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
  - 响应关键字段：`status`（`PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`/`CANCELED`）、`output`（成功时含结果数据）、`error_code`/`error_message`（失败时）。
  - 轮询建议：初始间隔 1–2 秒，逐步退避；避免高频轮询（平台限流阈值为 20 QPS）。

- **高级配置（按场景）**：
  - **任务取消**：`POST /api/v1/tasks/{task_id}/cancel` 可终止 `PENDING` 或 `RUNNING` 中的任务。
  - **事件通知**：在事件总线配置回调 URL 或 RocketMQ Topic，设置 `contain_result=true` 可在通知中内嵌完整结果（减少额外查询）。
  - **OSS 输出控制**：部分接口（如 ParseX）支持 `oss_config` 参数，指定自定义 OSS 凭证以控制结果存储位置与权限。

> ⚠️ 注意：`task_id` 和 `biz_id` 均为一次性有效凭证，不可重用；过期后（通常 24 小时）查询将返回 `TaskNotFound` 错误。

## 关联主题页

- [api overview](../api/api-overview.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [more about models](../api/more-about-models.md)
- [rag api](../api/rag-api.md)


