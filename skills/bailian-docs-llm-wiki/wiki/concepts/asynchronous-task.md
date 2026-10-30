# 异步任务

异步任务是百炼平台对长耗时 AI 接口（如视频生成、3D 建模、文档解析等）采用的标准执行模式：调用方提交请求后立即获得唯一 `task_id`，不等待模型推理完成；结果需通过独立查询接口轮询或事件回调方式获取。该模式解耦请求与响应，保障服务稳定性与高并发能力，是生产环境集成的推荐且强制方式。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成（video-generation）**：所有视频类 API（文生视频、图生视频、动作迁移等）均强制异步。必须设置请求头 `X-DashScope-Async: enable`，否则返回错误 `"current user api does not support synchronous calls"`。创建任务后，通过 `GET /api/v1/tasks/{task_id}` 轮询状态，成功时返回 `output.video_url` 直链。
  
- **3D 生成（3d-generation）**：Tripo 全系列接口（网格生成、Gaussian Splatting、重拓扑、动画重定向等）仅支持异步，且**仅限华北2（北京）地域**。同样需携带 `X-DashScope-Async: enable`，`task_id` 有效期为 24 小时，轮询间隔建议 ≥15 秒。

- **文档与字段解析（api-overview / ParseX）**：所有解析类 API（PDF/音视频结构化解析、Schema 字段抽取）统一使用 `biz_id` 作为任务标识符，而非 `task_id`。提交后需调用 `/parse/result` 或 `/extract/result` 查询，状态流转为 `init` → `processing` → `success`/`failed`；结果默认保留 30 天（抽取复用仅限 7 天）。

- **图像生成（image-generation）**：非所有图像模型都异步——`qwen-image-*`、`wan2.7-image-pro` 等支持同步调用；但 `kling`、`vidu`、`wan2.5-i2i-preview` 等长耗时模型**必须异步**，且同样依赖 `X-DashScope-Async: enable` 请求头和 `task_id` 轮询机制。

- **通用能力扩展（[more](../api/more.md)-about-models）**：平台提供统一的异步任务管理 API（`/api/v1/tasks/{task_id}` 及 `/api/v1/tasks` 批量查询），支持取消任务、配置 HTTP 回调或 RocketMQ 事件通知（通过 `contain_result=true` 可在回调中直接获取结果，减少一次查询）。所有异步任务均受 20 QPS 限流保护。

## 关键参数和配置

- **必需请求头**：
  - `X-DashScope-Async: enable`：显式启用异步模式，**缺失即报错**，不可省略。
  - `Authorization: Bearer <API_KEY>`：地域对齐的 API Key（如北京地域 Key 不能用于新加坡 Endpoint）。
  - `Content-Type: application/json`

- **核心标识符**：
  - `task_id`：视频、3D、部分图像模型返回的任务唯一 ID，有效期 **24 小时**。
  - `biz_id`：ParseX（文档/字段解析）专用任务 ID，有效期 **30 天**（复用场景下仅支持 7 天内）。

- **可选增强配置**：
  - `contain_result=true`（在回调/事件通知中内嵌结果体）：适用于事件驱动架构，避免额外轮询。
  - 自定义轮询策略：建议首次查询延迟 ≥10 秒（给服务端预热时间），后续间隔 15–30 秒；高频轮询（<1s）易触发限流。

- **地域与域名强约束**：
  - 必须使用业务空间专属 Endpoint：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`
  - 禁止混用：API Key、模型部署地域、Endpoint URL 三者必须严格同地域（如 `cn-beijing`）。

## 面向开发者，简洁实用

✅ **正确做法**  
- 所有异步调用前，确认模型文档是否标注“仅支持异步”或要求 `X-DashScope-Async: enable`；  
- 提交后立即保存 `task_id` 或 `biz_id`，并启动轮询（建议用指数退避策略）；  
- 生产环境优先配置 HTTP 回调或 RocketMQ 事件监听，降低轮询开销；  
- 使用 SDK 时启用连接复用（如 Python 的 `httpx.Client`、Java 的 `connectionPoolSize` 配置）。

❌ **常见错误**  
- 忘记加 `X-DashScope-Async: enable` 请求头 → 报错 `does not support synchronous calls`；  
- 跨地域调用（如用北京 Key 请求新加坡 Endpoint）→ 鉴权失败或 `403 Forbidden`；  
- 轮询超时未处理 `ResultNotReady`（HTTP 409）→ 导致逻辑中断；  
- 复用过期 `biz_id` 进行字段抽取 → 返回 `ParseResultNotReusable` 错误。

💡 **提示**  
- 异步任务无超时中断机制，失败任务不会自动重试，请在业务层实现幂等重试逻辑；  
- `task_id` 和 `biz_id` 均为字符串，不可解析为数字或做算术运算；  
- 所有异步结果中的文件 URL（如 `video_url`、`oss://...`）均为临时直链，有效期由对应服务单独约定（通常 24 小时），需及时下载或转存。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)


