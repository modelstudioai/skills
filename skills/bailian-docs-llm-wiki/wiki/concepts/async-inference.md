# 异步推理

异步推理是百炼平台针对计算密集、耗时较长的 AI 任务（如视频生成、3D 建模、文档/音视频解析等）所采用的标准调用模式：客户端提交请求后立即返回任务标识符（如 `task_id` 或 `biz_id`），服务端后台执行推理，客户端通过轮询或事件回调方式获取最终结果。

## 在百炼平台的不同场景中，这个概念如何使用

异步推理广泛应用于以下高延迟、高资源消耗的模型能力中：

- **视频生成**（`video-generation-api`）：所有文生视频、图生视频、人像驱动等任务均强制异步。调用 `/video-synthesis` 接口创建任务，返回 `task_id`；后续通过 `GET /api/v1/tasks/{task_id}` 轮询状态，典型耗时 1–5 分钟，`task_id` 有效期为 24 小时。

- **3D 模型生成**（`3d-generation`）：Tripo 系列模型（如 `Tripo/Tripo-H3.1`）仅支持异步。请求需携带 `X-DashScope-Async: enable` 头，成功后返回 `task_id`，轮询地址为统一任务查询接口 `GET /api/v1/tasks/{task_id}`，建议轮询间隔 ≥15 秒。

- **文档与音视频解析**（`api-overview`）：ParseX 所有解析与字段抽取任务均为异步。提交后返回 `biz_id`（非 `task_id`），通过 `/parse/result` 或 `/extract/result` 查询，结果默认保留 30 天（解析）或仅支持复用 7 天内解析结果（抽取）。

- **部分图像生成模型**（`image-generation`）：虽多数图像模型支持同步调用，但 `wanx2.1-t2i-turbo` 等特定版本明确归类为异步模型，需按异步流程处理；开发者应以具体模型文档为准，不可假设所有图像 API 均为同步。

- **语音与多模态长任务**（`more-about-models`）：如 `paraformer-16k-1` 语音转写、大文件 OCR 等，也统一纳入异步任务管理体系，共享同一套任务生命周期与回调机制。

> ✅ 共性特征：  
> - 请求头必须显式声明 `X-DashScope-Async: enable`（缺失将报错）；  
> - 严格地域绑定：API Key、Endpoint、任务查询地址必须同属一个地域（如 `cn-beijing`）；  
> - 任务 ID 有效期内可重复查询，无需重发请求；  
> - 不推荐高频轮询（如 <5 秒间隔），应遵守 QPS 限流（默认 20 QPS），生产环境强烈建议配置 HTTP 回调或 RocketMQ 事件通知。

## 关键参数和配置

| 参数 / 配置项 | 说明 | 是否必需 | 示例值 |
|---------------|------|----------|--------|
| `X-DashScope-Async` | 启用异步模式的强制请求头 | 是 | `"enable"`（字符串，大小写敏感） |
| `task_id` / `biz_id` | 任务唯一标识符，由创建接口返回 | — | `"a8532587-xxxx-xxxx-xxxx-0c46b17950d1"` |
| 轮询间隔 | 建议最小间隔，避免触发限流 | 否（但强烈建议） | ≥15 秒（3D）、≥30 秒（视频）、≥5 秒（解析） |
| 回调配置 | 替代轮询的推荐方案，需在控制台或调用时注册 | 否（可选） | HTTP URL 或 RocketMQ Topic 名称（见 `async-task-api.md`） |
| 任务有效期 | 超期后 `task_id` 不再可查，状态返回 `UNKNOWN` | — | 统一为 **24 小时**（视频、3D、语音等），ParseX 解析结果为 **30 天** |

> ⚠️ 注意：  
> - `X-DashScope-Async: enable` 是硬性开关，未设置将直接返回 `400 Bad Request` 并提示 “current user api does not [support](../guides/support.md) synchronous calls”；  
> - 所有异步任务的输出 URL（如 `output.video_url`, `pbr_model_url`, `url`）均为临时直链，有效期通常为 **1–2 小时**，请务必及时下载；  
> - 异步任务不支持取消或中断，失败任务需根据 `code` 和 `message` 排查（参考错误码文档），必要时重试。

## 面向开发者，简洁实用

- ✅ **第一步：确认模型是否异步**  
  查阅对应模型文档的「使用方式」章节——若明确出现“创建任务 → 轮询结果”、“`X-DashScope-Async: enable` 必须设置”等描述，则为异步模型。

- ✅ **第二步：构造请求**  
  ```bash
  curl -X POST \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -H "X-DashScope-Async: enable" \
    -d '{"model":"wan2.7-videoedit","input":{"prompt":"未来城市夜景"}}' \
    https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
  ```

- ✅ **第三步：获取并保管 `task_id`**  
  响应体中提取 `task_id`（JSON 字段），存入内存或数据库，**勿丢弃、勿重复创建**。

- ✅ **第四步：选择结果获取方式**  
  - *开发调试*：轮询 `GET /api/v1/tasks/{task_id}`，检查 `status` 字段（`QUEUED` → `RUNNING` → `SUCCESS`/`FAILED`）；  
  - *生产部署*：配置 [异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)，服务端收到事件后仅需一次查询即可取回结果，零轮询开销。

- ✅ **第五步：处理结果与清理**  
  成功时解析 `output.*_url` 并立即下载；失败时检查 `code`（如 `InvalidParameter`, `ResourceNotReady`）并重试或告警；任务超 24 小时后自动失效，无需主动清理。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [more about models](../api/more-about-models.md)
- [api overview](../api/api-overview.md)


