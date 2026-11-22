# 异步任务

异步任务是百炼平台中用于处理长耗时、高资源消耗模型请求的核心执行模式：客户端提交任务后立即返回唯一任务标识（如 `task_id` 或 `biz_id`），服务端在后台执行计算，开发者通过轮询或事件通知方式获取最终结果，避免阻塞式等待。

## 在百炼平台的不同场景中，这个概念如何使用

异步任务广泛应用于以下高复杂度、长耗时的模型服务中：

- **视频生成**：所有视频类 API（文生视频、图生视频、参考生视频、数字人驱动等）强制采用异步模式，典型耗时 1–5 分钟。必须设置请求头 `X-DashScope-Async: enable`，否则报错 `"current user api does not support synchronous calls"`；成功响应返回 `task_id`，需调用 `GET /api/v1/tasks/{task_id}` 轮询状态直至 `status == "SUCCESS"`。

- **3D 生成**：Tripo 全链路能力（文/图生3D、Gaussian Splat、贴图、绑骨、重定向等）全部为异步任务，且**仅支持华北2（北京）地域**。同样依赖 `X-DashScope-Async: enable` 头和 `task_id` 查询机制，输入常通过前序任务 ID（如 `input.original_model_task_id`）复用中间结果。

- **文档与音视频解析（ParseX）**：结构化解析（PDF/Word/MP4 等）和基于 Schema 的字段抽取均采用异步模型，返回 `biz_id` 作为任务凭证。支持复用 7 天内的解析结果（`parsed_file_biz_id`），但需严格匹配类型与有效期。

- **[多模态](multi-modal.md)翻译（Qwen-MT-Uni / Qwen-MT-Image）**：当输入为大尺寸图像、长文档（PDF/XLSX）、或长音频（>60 秒）时，系统自动降级为异步模式（即使未显式设 `X-DashScope-Async`）。若需确定性异步行为，仍建议主动添加该请求头。

- **其他长耗时模型**：包括图像生成（如 `wanx2.1-t2i-turbo`）、语音转写（`paraformer-16k-1`）等，均归入异步任务体系，统一由 `/api/v1/tasks/` 接口管理生命周期。

> ✅ **关键共识**：异步 ≠ 慢，而是平台对资源调度、超时控制、失败重试、结果持久化的标准化封装；同步模型（如 `qwen-plus` 文本生成）仅适用于毫秒级响应场景。

## 关键参数和配置

| 参数 | 位置 | 说明 | 必填性 |
|------|------|------|--------|
| `X-DashScope-Async` | 请求头 | 固定值 `enable`，**所有异步调用必需显式声明**，缺失将直接拒绝请求 | ✅ 必填 |
| `task_id` / `biz_id` | 响应体 | 任务唯一标识符（UUID 格式），24 小时内有效，用于后续查询与取消 | ✅ 返回必含 |
| `Authorization: Bearer <API_KEY>` | 请求头 | API Key 必须与模型所在地域一致（如 `cn-beijing`），跨地域调用必然失败 | ✅ 必填 |
| `Content-Type: application/json` | 请求头 | 所有异步接口均要求 JSON 格式请求体 | ✅ 必填 |
| `model` | 请求体 | 模型名称（如 `pixverse/pixverse-v6-max-t2v`、`Tripo/Tripo-H3.1`），需与文档严格一致 | ✅ 必填（除部分复用场景） |

- **轮询建议间隔**：  
  - 文本/轻量任务（向量、小图）：≥1s  
  - 图像/3D 任务：≥3s  
  - 视频/长文档/音视频：≥5s（避免触发限流）  

- **替代轮询的方式**：  
  可配置 HTTP 回调 URL 或 RocketMQ 订阅 `dashscope:System:AsyncTaskFinish` 事件，收到通知后再调用一次 `/api/v1/tasks/{task_id}` 获取最终结果，更高效、低延迟。

- **取消任务**：  
  仅对 `status == "PENDING"` 的任务有效，调用 `POST /api/v1/tasks/{task_id}/cancel` 即可。

## 面向开发者，简洁实用

- ✅ **第一步：确认是否需要异步**  
  查阅对应模型文档 —— 若明确标注“异步调用”“不支持同步”或示例含 `X-DashScope-Async: enable`，则必须走异步流程。

- ✅ **第二步：构造请求**  
  ```bash
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "X-DashScope-Async: enable" \
    -d '{
          "model": "pixverse/pixverse-v6-max-t2v",
          "input": {"prompt": "a cyberpunk cat wearing neon glasses"},
          "parameters": {"resolution": "1080P"}
        }' \
    "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"
  ```

- ✅ **第三步：轮询或监听事件**  
  ```bash
  # 轮询示例（建议加指数退避）
  curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}"
  # → 检查 response.status ∈ ["PENDING", "PROCESSING", "SUCCESS", "FAILED"]
  ```

- ⚠️ **避坑提醒**：  
  - 地域三一致：模型、Endpoint 域名、API Key 必须同属一个地域（如 `cn-beijing`）；  
  - `task_id` 仅 24 小时有效，过期需重提；  
  - 不要重复提交相同语义任务 —— 平台不保证幂等，可能产生冗余计费；  
  - 使用 SDK 时，优先选用 `client.*.jobs.create()` 等异步方法，而非 `.call()`。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


