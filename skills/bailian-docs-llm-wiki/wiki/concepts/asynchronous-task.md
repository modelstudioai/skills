# 异步任务

异步任务是百炼平台对长耗时模型调用（如视频生成、3D建模、语音转写等）采用的标准执行模式：客户端提交请求后立即返回任务 ID，服务端后台执行计算并持久化结果，客户端通过轮询或事件回调方式获取最终输出。该机制解耦请求与响应，避免连接超时，保障高并发下的系统稳定性。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成（`/v1/videos/generations`）**：所有视频模型（如 `kling`、`wanxiang`）强制异步。调用返回 `id`，需轮询 `GET /v1/videos/generations/{id}` 查询 `status`（`succeeded`/`failed`），成功后从 `output.video_url` 下载成品（24 小时有效）。
- **3D 生成（Tripo 模型）**：必须显式携带请求头 `X-DashScope-Async: enable`，否则直接报错。创建任务返回 `task_id`，通过 `GET /api/v1/tasks/{task_id}` 查询状态，结果 URL（如 `pbr_model_url`）仅 2 小时有效。
- **[多模态](multi-modal.md)长耗时模型**：图像生成、语音转写等默认启用异步机制，需配合 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 使用 `fetch`/`list`/`cancel` 接口进行生命周期管理。
- **应用调用（Application Call）**：当智能体或工作流执行耗时操作（如 RAG 检索、大文件解析）时，若响应时间可能超过同步接口限制（通常 60 秒），平台自动降级为异步执行（部分场景需主动配置），此时返回结构含 `task_id` 字段，需按异步流程处理。
- **Realtime API 不适用**：Realtime API 专为低延迟流式交互设计，全程保持长连接，**不使用异步任务模型**；其任务生命周期由会话（session）管理，而非独立任务 ID。

> ✅ **最佳实践**：优先配置 **EventBridge HTTP 回调** 或 **RocketMQ 订阅**，监听 `dashscope:System:AsyncTaskFinish` 事件，替代高频轮询，规避 20 QPS 限流风险。

## 关键参数和配置

| 参数/配置 | 说明 | 示例/值域 | 注意事项 |
|-----------|------|------------|----------|
| `X-DashScope-Async: enable` | 强制启用异步模式的请求头 | `"enable"` | 3D 生成等接口**必需**；缺失将拒绝请求 |
| `task_id` / `id` | 任务唯一标识符 | `"task-abc123xyz"` | 所有异步接口响应中返回，用于后续查询或取消 |
| 轮询间隔 | 建议最小查询间隔 | ≥15 秒（3D）、≥5 秒（视频） | 过短易触发限流；生产环境应结合事件回调降低轮询频次 |
| 任务状态字段 | 标准化状态枚举 | `"PENDING"`, `"RUNNING"`, `"SUCCEEDED"`, `"FAILED"`, `"CANCELED"` | 仅 `PENDING` 状态可调用 `/cancel`；`RUNNING` 取消失败 |
| 结果 URL 有效期 | 输出资源临时访问链接时效 | 2–24 小时（依模型而定） | 必须在有效期内下载，过期不可恢复；建议服务端及时落库 |
| 任务元数据保留期 | `task_id` 可查询窗口 | 24 小时（3D）、72 小时（视频） | 超期后 `GET /tasks/{id}` 返回 `UNKNOWN`，无法补查 |

## 面向开发者，简洁实用

- **不要轮询，要回调**：在控制台配置 EventBridge 目标（HTTP URL 或 RocketMQ），订阅 `dashscope:System:AsyncTaskFinish` 事件，实时接收 JSON 格式结果，零延迟、免限流。
- **不要硬编码轮询逻辑**：SDK 中避免 `while status != 'succeeded': sleep(1); poll()`；改用 `wait_for_completion(task_id, timeout=300)` 类封装方法（参考 DashScope Python SDK `AsyncTask.wait()`）。
- **注意地域与 Workspace 绑定**：3D 生成仅支持华北2（北京），且 `task_id` 查询 URL 必须带对应 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；跨地域调用必然失败。
- **清理要及时**：异步任务不自动释放资源，长期未查询的任务仍占用后台队列；对已知失败或超时任务，主动调用 `/cancel`（若状态允许）或记录日志告警。
- **错误处理标准化**：检查响应 `status` 字段而非 HTTP 状态码（如 `200` 但 `status: "FAILED"`）；失败原因在 `output.error.code` 和 `output.error.message` 中，常见如 `InvalidInput`, `ResourceExhausted`, `Timeout`。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [application call](../api/application-call.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


