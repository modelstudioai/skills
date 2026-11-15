# 异步调用

异步调用是百炼平台对耗时较长的AI任务（如视频生成、3D建模、文档/音视频解析、复杂图像编辑等）所采用的标准执行模式：客户端提交任务后立即返回唯一任务标识（如 `task_id` 或 `biz_id`），实际计算在服务端后台执行，结果需通过轮询或事件通知方式后续获取。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成（video-generation-api）**：所有视频类API（文生视频、图生视频、口型同步等）强制异步。必须设置请求头 `X-DashScope-Async: enable`，否则报错；提交后返回 `task_id`，24小时内轮询 `GET /api/v1/tasks/{task_id}` 获取结果。
- **图像生成（image-generation）**：适用于高分辨率生成、多图融合编辑、FaceChain训练等长耗时任务。同步接口（如千问T2I）可直接返回Base64或URL；而万相2.5多图编辑、虚拟模特生成等则走异步流程，同样通过 `task_id` 轮询。
- **文档与音视频解析（api-overview / ParseX）**：全部接口均为异步。提交 `file_url` 后返回 `biz_id`，通过 `/parse/result` 或 `/extract/result` 查询状态；解析结果默认保留30天，抽取任务需复用有效期内的 `parsed_file_biz_id`。
- **3D生成（3d-generation）**：Tripo全系列接口（文生3D、图生Splat、网格重拓扑、自动绑骨等）仅支持异步，且**严格限定华北2（北京）地域**；必须携带 `X-DashScope-Async: enable`，`task_id` 有效期为24小时。
- **其他长耗时能力**：语音转写（paraformer）、部分多模态模型（如 `qwen3-vl-plus` 配合大图输入）、字段抽取等也归入异步范畴。是否启用异步由模型本身决定，开发者不可自行切换同步/异步模式。

> ✅ 统一特征：所有异步调用均遵循「提交 → 获取ID → 查询结果」三步范式，不支持阻塞式等待。

## 关键参数和配置

- **必需请求头**：
  - `X-DashScope-Async: enable` —— 显式声明启用异步模式，缺失将触发 `current user api does not support synchronous calls` 错误。
  - `Authorization: Bearer <API_KEY>` —— API Key 必须与 Endpoint 所属地域一致（如北京地域Key不可用于新加坡Endpoint）。
- **任务标识**：
  - 返回字段统一为 `task_id`（视频、3D、图像编辑）或 `biz_id`（ParseX解析/抽取），均为全局唯一字符串，有效期 **24小时**（ParseX解析结果保留期为30天，但查询ID本身24小时失效）。
- **轮询建议**：
  - 初始延迟 ≥10秒（避免空转）；
  - 后续间隔建议 15–30秒，采用指数退避策略（如 15s → 30s → 60s）；
  - 状态字段为 `data.status`，值为 `"processing"`（继续轮询）、`"success"`（成功，含结果）、`"failed"`（失败，含错误码）。
- **高级配置（可选）**：
  - 事件通知：配置 EventBridge 监听 `dashscope:System:AsyncTaskFinish` 事件，替代轮询，降低QPS压力；
  - 批量查询：使用 `/api/v1/tasks?page_no=1&page_size=50` 分页拉取历史任务（QPS限流20）；
  - 文件上传协同：若输入含本地文件，需先调用上传接口获取临时OSS URL，并在模型请求中添加 `X-DashScope-OssResourceResolve: enable`。

## 面向开发者，简洁实用

- 不要尝试同步调用异步模型——会直接报错；
- 每次调用前确认：API Key、Endpoint 域名、模型部署地域三者完全匹配；
- `task_id` / `biz_id` 是你追踪任务的唯一凭证，请妥善保存并及时消费（24小时内）；
- 生产环境优先使用事件通知（EventBridge）而非轮询，更稳定、更省资源；
- 调试阶段可用百炼 CLI 快速验证异步流程（`bailian task submit ...` → `bailian task get ...`）；
- 所有异步任务均受配额限制（如并发数、总任务数），详情见控制台「配额管理」。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)
- [api overview](../api/api-overview.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)


