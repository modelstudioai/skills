# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、音视频、法律、金融、客服、数据挖掘、[多模态](../concepts/multi-modal.md)交互等多个垂直场景。所有应用均基于百炼托管模型构建，支持快速集成与二次开发。开发者可通过控制台或 API 直接调用，无需自行部署底层模型。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与能力组合，例如：
- 通义法睿（[官方应用-通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)）基于 Qwen2.5-72B-Instruct + 法律知识图谱；
- 通义听悟Agent（[官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md)）依赖 ASR + LLM + TTS 多阶段流水线；
- 通义 UI Agent（[官方应用-通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md)）使用 Qwen-VL 系列[多模态](../concepts/multi-modal.md)模型解析界面截图并生成操作指令。

> **注意**：部分轻应用（如全妙轻应用系列）实际调用的是共享推理实例，不独占模型资源，其响应延迟与并发能力不同于独立部署的官方应用（参见 [官方应用-全妙轻应用系列](../../raw/application-user-guide/application-gallery/quanmiao-light-application-series.md)）。

## 关键参数

调用任一应用时，需在请求体中指定以下必选参数：
- `app_id`：应用唯一标识（可在控制台「应用广场」页获取）；
- `input`：结构化输入对象，schema 因应用而异（详见各应用文档，如 [通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 要求 `query` + `filters`）；
- `timeout`：最大等待毫秒数（默认 30000，部分长任务应用如析言GBI建议设为 120000）。

所有应用统一支持 `stream: true` 启用流式响应，但仅限文本类输出应用（[多模态](../concepts/multi-modal.md)输出如音频/图像暂不支持流式）。

## 使用方式

1. **控制台调用**：进入「应用广场」→ 选择目标应用 → 点击「调试」，填写 input 示例后执行；
2. **API 调用**：向 `POST /v1/applications/{app_id}/invoke` 发送请求（需携带 `Authorization: Bearer <api_key>`）；
3. **SDK 集成**：使用 `BailianAppClient.invoke(app_id, input)`（Python SDK v1.8.0+ 支持自动重试与错误码映射）。

## 限制和注意事项

- 单应用默认 QPS 限制为 5，可通过工单申请提升；
- 所有应用输入 `input` 字段总大小不得超过 2MB（含 base64 编码图像等二进制内容）；
- 应用间**不共享上下文**：连续多次调用同一 `app_id` 不构成会话，如需状态保持，须自行维护 session_id 并传入（部分应用如伶鹊CCAI-客服对话Agent 显式支持 `session_id` 字段）；
- > **注意**：[通义点金](../../raw/application-user-guide/application-gallery/tongyi-dianjin.md) 文档中提及的“支持实时行情订阅”功能当前仅限金融云专有版，公有云用户调用将返回 `403 Forbidden`，该差异未在 [通义数据挖掘](../../raw/application-user-guide/application-gallery/tongyi-docmining.md) 文档中同步说明。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


