# 异步调用

异步调用是百炼平台对耗时较长（通常为秒级至数分钟）的模型任务所采用的标准执行模式：客户端发起请求后立即返回任务标识（`task_id` 或 `biz_id`），不等待实际计算完成；结果需通过轮询或事件通知方式后续获取。该模式保障了服务稳定性、资源利用率与高并发下的响应确定性。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成**：所有视频 API（如 HappyHorse、万相3.0、爱诗、数字人模型）均强制异步。调用需两步：① 发送 `POST /video-generation/video-synthesis` 创建任务（返回 `task_id`）；② 定期调用 `GET /tasks/{task_id}` 查询状态，直至 `task_status === "SUCCEEDED"`。任务 ID 有效期为 24 小时。

- **3D 生成**：Tripo 模型（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`）仅支持异步，且地域强约束于华北2（北京）。创建任务后必须轮询 `/tasks/{task_id}`，推荐间隔 ≥15 秒；成功响应中的 `pbr_model_url` 或 `base_model_url` 有效期仅 2 小时，须及时下载。

- **图像生成**：部分图像模型（如 `wanx2.1-t2i-turbo`、`kling-v3-omni-image-generation`）默认或仅支持异步；而 `qwen-image-3.0-pro`、`z-image-turbo` 等低延迟模型则支持同步调用。是否启用异步由 `X-DashScope-Async` 请求头控制，非模型固有属性。

- **文档解析与信息抽取（Parse/Extract）**：Overview 模块统一采用异步任务模型。调用 `/submit` 返回 `biz_id`，再通过 `/result?biz_id=xxx` 获取结构化结果。音视频解析、大文件处理等典型长耗时场景必须走此路径。

- **通用异步任务管理**：所有异步任务均纳入统一生命周期管理体系，支持通过 `/tasks/{id}` 查询、`/tasks` 批量列表、`/tasks/{id}/cancel` 主动取消，并可配置 HTTP 回调或 RocketMQ 订阅 `dashscope:System:AsyncTaskFinish` 事件，实现免轮询的结果交付。

## 关键参数和配置

- **`X-DashScope-Async`（HTTP 请求头）**  
  必填，值必须为 `"enable"`。缺失或设为其他值将直接报错：`"current user api does not support synchronous calls"`。这是触发异步流程的开关，与模型类型无关。

- **`task_id` / `biz_id`（响应体字段）**  
  创建任务成功后返回的唯一字符串（UUID 格式），用于后续结果查询。有效期依服务而定：视频/3D 任务为 24 小时；Parse/Extract 任务在控制台保留更久，但 API 查询建议 7 天内完成。

- **轮询建议间隔**  
  - 文本类任务（如向量生成）：≥1 秒  
  - 图像生成：≥5 秒  
  - 视频/3D 生成：≥15 秒  
  避免高频轮询触发 20 QPS 限流；生产环境强烈推荐使用事件驱动方式替代轮询。

- **事件通知配置（可选但推荐）**  
  在事件总线中订阅 `dashscope:System:AsyncTaskFinish` 事件，从回调 payload 的 `data.task_id` 提取 ID 后单次查询结果，彻底消除轮询开销与不确定性。

## 面向开发者，简洁实用

- ✅ **务必显式设置 `X-DashScope-Async: enable`** —— 这不是可选项，而是异步调用的硬性前提。  
- ✅ **不要假设响应体含最终结果** —— 异步接口的首次响应只含 `task_id`，业务逻辑必须实现结果获取闭环。  
- ✅ **立即记录 `task_id` 并启动轮询/事件监听** —— 任务 ID 一旦丢失即无法恢复结果。  
- ✅ **校验 `task_status` 而非仅看 HTTP 状态码** —— `200 OK` 仅表示查询成功，`task_status: "FAILED"` 表示任务执行失败。  
- ✅ **生产环境优先用事件驱动** —— 配置一次回调 URL 或 RocketMQ Topic，比维护轮询逻辑更可靠、更省资源。  
- ❌ **不要跨地域混用 API Key 与 Endpoint** —— 视频、3D 等服务对地域一致性要求严格，错误组合将返回 `InvalidApiKey` 或 `UnsupportedRegion`。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [more about models](../api/more-about-models.md)
- [overview](../guides/overview.md)


