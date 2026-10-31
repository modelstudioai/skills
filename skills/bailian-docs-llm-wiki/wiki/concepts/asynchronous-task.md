# 异步任务

异步任务是百炼平台对耗时较长、无法即时返回结果的模型调用所采用的标准执行范式：用户提交请求后立即获得唯一任务标识（如 `task_id` 或 `biz_id`），后续通过轮询或事件订阅方式获取最终结果。该模式解耦了请求与响应，保障服务稳定性，并支持批量处理、长周期计算及资源密集型任务（如视频生成、3D建模、大文件解析）。

## 在百炼平台的不同场景中，这个概念如何使用

异步任务是以下核心能力的**默认且强制的调用方式**：

- **视频生成（Video Generation）**：所有视频模型（如 `wan3.0`、`kling/kling-v3-omni-video-generation`、`vidu/viduq3-pro_text2video`）均要求设置请求头 `X-DashScope-Async: enable`，调用统一 endpoint 创建任务，再通过 `GET /api/v1/tasks/{task_id}` 查询状态与结果 URL。
  
- **3D生成（3D Generation）**：Tripo 系列模型（如 `Tripo/Tripo-H3.1`、`Tripo/Tripo-ImageToSplat`）全部采用异步流程，仅支持华北2（北京）地域，创建任务后需轮询至 `status == "SUCCESS"` 才可下载 `.glb`、`.splat` 等产物。

- **文档与音视频解析（ParseX API）**：无论是 PDF/Word 解析还是 MP4/MP3 分析，均使用 `biz_id` 作为任务凭证；提交 `/parse/submit` 或 `/extract/submit` 后，必须调用 `/parse/result` 或 `/extract/result` 获取结构化输出（如 `markdown`、`extract_result_json`）。

- **图像生成（Image Generation）**：虽支持同步调用，但**图像编辑、虚拟模特、多图融合、局部重绘等高耗时场景强烈推荐异步模式**（如 `facechain-finetune`、`image-erase-completion`、`wanx-virtualmodel`），避免请求超时，提升成功率。

- **其他长耗时模型**：语音转写（`paraformer-16k-1`）、部分多模态推理（如大尺寸图生图）、模型微调任务等，也统一纳入异步任务管理体系，由 `/api/v1/tasks/{id}` 统一纳管生命周期。

> ✅ 共同特征：所有异步任务均具备明确状态机（`QUEUED` → `PROCESSING` → `SUCCESS` / `FAILED`），结果有效期有限（通常 24 小时），且不支持 OpenAI 兼容协议（仅 DashScope 原生接口支持）。

## 关键参数和配置

| 类别 | 参数/配置 | 说明 | 必填性 | 示例值 |
|--------|-----------|------|---------|---------|
| **请求头** | `X-DashScope-Async` | 显式声明启用异步模式 | ✅ 所有异步模型必填 | `"enable"` |
| **请求头** | `Authorization` | 使用地域匹配的 API Key 鉴权 | ✅ 全局必填 | `"Bearer sk-xxx"` |
| **请求体** | `model` | 指定具体模型名（区分大小写、含命名空间） | ✅ 全局必填 | `"kling/kling-v3-omni-video-generation"` |
| **响应字段** | `task_id` / `biz_id` | 任务唯一标识，用于后续查询与回调 | ✅ 创建成功后必返 | `"task-abc123xyz"` |
| **轮询接口** | `GET /api/v1/tasks/{task_id}` | 标准结果查询端点（视频/3D/图像） | — | `https://xxx.cn-beijing.maas.aliyuncs.com/api/v1/tasks/task-abc123` |
| **轮询接口** | `GET /parse/result?biz_id=...` | ParseX 专用结果查询端点 | — | `https://xxx.cn-beijing.maas.aliyuncs.com/parse/result?biz_id=biz-456` |
| **高级配置** | `contain_result` | 控制回调事件是否内嵌完整结果（减少一次查询） | ❌ 可选 | `true` |

> ⚠️ 注意事项：
> - **禁止高频轮询**：建议按任务类型设置合理间隔（文本类 ≥1s，图像类 ≥5s，视频/3D类 ≥10–30s），避免触发限流（默认 20 QPS）；
> - **地域强一致**：`model`、API Key、Endpoint URL 必须属于同一地域（如 `cn-beijing`），否则直接失败；
> - **结果有效期**：`task_id` 默认 24 小时有效，`biz_id`（ParseX）解析结果保留 30 天、抽取复用窗口为 7 天；
> - **错误重试策略**：遇 `ResultNotReady`（HTTP 409）应继续轮询；`FileDownloadFailed` 等不可恢复错误需检查输入源权限。

## 面向开发者，简洁实用

- ✅ **快速上手三步法**：  
  1. 发送 `POST` 请求（带 `X-DashScope-Async: enable` + `Authorization` + `model` + 输入数据）→ 获取 `task_id`；  
  2. 定期 `GET /api/v1/tasks/{task_id}` → 检查 `status` 字段；  
  3. `status == "SUCCESS"` 时，从 `output.*_url`（视频/3D）或 `data.*`（ParseX）提取结果。

- ✅ **生产环境推荐**：  
  - 使用 **事件驱动替代轮询**：配置 EventBridge 监听 `dashscope:System:AsyncTaskFinish` 事件，实现毫秒级结果通知；  
  - 对高并发场景，**复用 HTTP 连接池**（Python 用 `httpx.Client`，Java 配 `connectionPoolSize=256`）；  
  - 敏感环境（如前端）**禁用永久 Key**，改用后端签发的临时 API Key（`expire_in_seconds=1800`）。

- ❌ **避坑提醒**：  
  - 不要省略 `X-DashScope-Async: enable` —— 缺失将报错 “current user api does not [support](../guides/support.md) synchronous calls”；  
  - 不要跨地域混用 Key 和 Endpoint —— 必然返回 `InvalidRegion` 或鉴权失败；  
  - 不要假设异步接口返回结果体 —— 初始响应仅含 `task_id`，结果需单独查询。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)


