# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一的 Runtime 执行环境部署，支持快速集成、参数化调用与轻量定制。开发者可通过控制台或 OpenAPI 直接访问，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用均已绑定特定模型栈与工作流逻辑，例如：
- 通义法睿（`tongyi-farui`）基于法律垂域微调模型 + 法规知识图谱检索；
- 通义 UI Agent 依赖 `qwen-vl-plus` 多模态模型 + 页面 DOM 解析与操作引擎；
- 千问联网检索Agent 使用 `qwen-max` + 实时网页抓取与摘要模块。

全部官方应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。部分应用（如 [官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md)）还额外集成了语音转写、语义摘要与会议纪要生成等复合功能。

## 关键参数

调用任一应用时，需传入标准化请求体，核心字段包括：
- `application_id`：应用唯一标识（如 `tongyi-farui`, `web-search-agent`），可在 [应用广场](../../raw/application-user-guide/application-gallery.md) 文档中查得；
- `input`：字符串或结构化对象，格式依应用而异（例如 `tongyi-dianjin` 要求 `{"query": "...", "industry": "finance"}`）；
- `parameters`（可选）：覆盖应用默认配置，如 `max_iterations=3`、`enable_web_search=true`；
- `stream`（布尔值）：控制是否启用流式响应，仅部分应用支持（参见 [官方应用-通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 的流式说明）。

> **注意**：`parameters` 字段的合法键名与取值范围因应用而异，部分文档（如 `xiyan-gbi.md`）未完整列出可覆盖参数，建议以实际 API Schema 或 SDK 类型定义为准。

## 使用方式

1. **控制台接入**：在百炼控制台「应用广场」页选择目标应用 → 点击「调试」或「集成」→ 获取 `application_id` 与示例请求；
2. **OpenAPI 调用**：向 `/v1/applications/{application_id}/invoke` 发送 POST 请求，携带认证 Header 与 JSON body；
3. **SDK 集成**：使用 `alibabacloud-bailian20231219` Python/Java SDK，调用 `InvokeApplicationRequest` 方法。

所有应用均遵循统一鉴权与限流策略，详细调用流程与错误码说明请参考 [应用广场](../../raw/application-user-guide/application-gallery.md)。

## 限制和注意事项

- 每个应用有独立的 QPS 与并发数限制（如 `web-search-agent` 默认 5 QPS），超出将返回 `429 Too Many Requests`；
- 输入文本长度上限为 32768 tokens（含系统提示词），超长内容将被截断，不触发自动分块；
- 应用间**不共享上下文状态**：连续多次调用同一 `application_id` 不构成会话，如需对话管理，须由客户端维护 `session_id` 并传入（部分应用如 `lingque-ccai-voice-dialogue-robot.md` 明确支持该字段）；
- 非官方应用（用户自建应用）不可通过应用广场目录发现，仅能通过 `ListApplications` API 查询。

> **注意**：文档中部分轻应用（如 [官方应用-全妙轻应用系列](../../raw/application-user-guide/application-gallery/quanmiao-light-application-series.md)）标注“支持私有化部署”，但当前平台版本仅开放 SaaS 模式调用，私有化能力尚未上线，该描述已过时。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


