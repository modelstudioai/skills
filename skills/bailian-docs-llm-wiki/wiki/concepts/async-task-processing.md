# 异步任务处理

异步任务处理是百炼平台针对高耗时、长周期 AI 推理与训练场景设计的标准交互机制。通过该机制，客户端提交请求后不会阻塞 HTTP 连接，而是立即获取任务标识（`task_id`），随后通过状态轮询或 Webhook 回调异步获取最终执行结果。

## 跨场景应用模式
在百炼平台的不同业务域中，异步任务处理的具体实现略有差异，但均遵循统一的调度范式：
- **多模态推理与生成**：视频生成 (`wan`、`happyhorse` 等)、3D 模型生成 (`Tripo`) 及长音频/录音文件识别等场景，因模型计算密集或输入体积大，强制或推荐采用异步模式。详见 `[[video-generation-api]]`、`[[3d-generation]]` 与 `[[speech-recognition-api]]`。
- **模型调优训练**：LLM 微调、视频模型 LoRA 训练及 ASR 热词定制任务耗时通常为数分钟至数小时，全生命周期通过异步接口管理。详见 `[[model-training]]`。
- **应用与工作流调用**：复杂智能体推理或长链路工作流报告生成，可通过开启后台模式将同步请求转为异步任务，避免客户端超时。详见 `[[application-call]]`。

## 关键参数与配置
| 触发方式 | 适用协议/API | 配置说明 |
|:---|:---|:---|
| **请求头触发** | HTTP REST / 推理 API | 必须携带 Header `X-DashScope-Async: enable`，否则服务端将直接拦截或降级为同步模式（若支持）。 |
| **请求体参数触发** | 应用调用 API (`/apps/...`) | 设置 `"background": true`。注意该参数与[[streaming-output|流式输出]]参数 (`"stream": true`) **严格互斥**，不可同时传入。 |
| **状态查询** | 统一查询接口 | `GET /tasks/{task_id}` 或使用 `[[dashscope-sdk]]` 提供的 `wait()` / `retrieve()` 方法。默认限流 20 RPS，高频查询建议结合业务降级或改用回调。 |
| **轮询间隔** | 全平台通用 | 建议设置为 **10~15 秒**。过短易触发网关限流，过长会延迟业务响应。高并发或长耗时任务强烈建议配置 `[[异步任务回调]]` (Webhook)。 |

## 生命周期与状态管理
- **状态流转**：标准状态机为 `PENDING`/`QUEUING`（排队中）→ `RUNNING`（处理中）→ `SUCCEEDED`/`completed`（成功）或 `FAILED`/`failed`/`cancelled`（失败/取消）。
- **ID 有效期**：`task_id` 及状态查询接口有效期为 **24 小时**。超时后查询将返回 `UNKNOWN` 状态且不可恢复，建议结合 `[[异步任务管理]]` 策略进行本地超时清理。
- **资源时效**：生成类任务成功后返回的文件下载链接（如 `.glb`、`.webp`、`.mp4`）有效期通常仅 **2 小时**，业务侧必须在成功回调或轮询成功后立即持久化存储。
- **计费规则**：平台仅对 `SUCCEEDED` / `completed` 终态任务计入用量计费；排队中或失败任务通常不计费，失败时需解析 `code`/`message` 参考 `[[错误码说明]]` 进行重试。

## 开发者最佳实践
1. **严格保障幂等性**：成功获取 `task_id` 后，**请勿重复提交相同请求**。应直接使用 `task_id` 进行状态追踪，重复下发可能导致重复计费或底层资源冲突。
2. **流式与异步互斥**：当前架构下，异步任务模式不支持 SSE [[streaming-output|流式输出]]。若需实时增量文本，请使用同步流式调用；若任务预计耗时较长，请直接采用异步模式。
3. **封装重试与容错**：针对网络抖动或临时性模型负载导致的 `FAILED` 状态，建议在 SDK 层或业务网关实现指数退避重试。训练类任务（`[[model-training]]`）需额外注意 `hyper_parameters` 一致性，避免 Checkpoint 加载异常。
4. **地域与鉴权隔离**：所有异步任务均强依赖地域路由，`model`、Endpoint 与 `[[api-key]]` 必须归属同一地域（如中国大陆北京或新加坡），跨地域混用将直接触发鉴权失败或 `404`。
5. **调试优先**：生产环境集成前，建议优先通过控制台 **API 调试** 功能验证异步参数组合与回调地址可达性，确认状态流转符合预期后再进行服务部署。

## 关联主题页

- [[model-inference|model inference]] — `../guides/model-inference.md`
- [[3d-generation|3d generation]] — `../api/3d-generation.md`
- [[video-generation-api|video generation api]] — `../api/video-generation-api.md`
- [[speech-recognition-api-reference|speech recognition api reference]] — `../api/speech-recognition-api-reference.md`
- [[model-training|model training]] — `../api/model-training.md`
- [[application-call|application call]] — `../api/application-call.md`

