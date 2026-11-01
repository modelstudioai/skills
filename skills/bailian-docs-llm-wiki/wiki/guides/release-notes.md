# release notes

百炼平台的 Release Notes 汇总了模型上下架、功能迭代、参数变更及服务调整等关键变更信息，面向开发者提供可落地的操作依据。所有变更均遵循明确的时间节点与通知机制，建议开发者定期查阅并及时适配。核心变更包括模型生命周期管理（上架/下线）、平台能力扩展（如异步调用、多模态 SDK）、计费与部署模式更新（如 MU 计费、[Token](../concepts/token.md) Plan 团队版）等。

## 支持的模型/功能

- **新模型上架**：持续引入多模态、垂直领域及高性能模型，例如 `qwen3.8-max`（2.4T MoE 旗舰）、`qwen-audio-3.1-realtime-flash`（实时双工语音）、`Tripo/Tripo-AutoRig`（3D 自动绑骨）、`decision-model-preview`（结构化决策）等，覆盖文本、视觉、音频、视频、3D、翻译、排序、向量等全模态类型。详情见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块升级**：
  - 异步能力：Responses API 新增 `background=true` 异步调用模式；[异步任务](../concepts/asynchronous-task.md)支持 EventBridge HTTP 回调与 RocketMQ 主动推送。
  - 知识库 RAG：上线知识检索与知识问答服务，支持多知识库联合检索、混合排序及指令干预模式。
  - 智能体托管：新增 Managed Agent 托管运行时 API，统一管理会话与工具执行。
  - 模型调优：新增强化学习（RL）训练（邀约制）、0 代码安全合规强化、图像/视频/视觉理解模型类型支持。
  - 多模态开发套件：新增 Linux C++、Android/iOS Lite、RTOS C SDK 及服务端 Java SDK。
- **平台服务调整**：企业知识库（旧）已于 2026 年 7 月 16 日下线；记忆库于 2026 年 3 月 20 日升级为 Memory 2.0，支持[长期记忆](../concepts/long-term-memory.md)与多应用共享。

> **注意**：文档 2 中“2026年7月16日 企业知识库（旧）下线通知”与文档 3 未提及该服务，但文档 2 明确标注其已下线，应以文档 2 的公告为准；文档 3 仅聚焦模型维度，不覆盖平台服务下线。

## 关键参数

- **模型版本标识**：正式版模型支持三种形态：系列名（如 `qwen-max`）、带日期后缀的快照名（如 `qwen-max-2025-01-25`）、`-latest` 别名（如 `qwen-max-latest`）。预览版模型 ID 含 `preview`/`beta`/`experimental` 等标识。
- **上下文与输出限制**：主流新模型（如 `qwen3.8-max`、`deepseek-v4.1-flash`、`GLM-5.3-FlashX`）普遍支持 **1M [Token](../concepts/token.md) 上下文窗口**，最大输出长度达 **128K–384K [Token](../concepts/token.md)**。
- **性能指标**：`qwen-audio-3.1-tts-flash` 面向低延迟场景，`GLM-5.3-Flash` 推理速度达 200 tokens/s，`qwen3.8-flash` 兼容 OpenAI 与 Anthropic 协议。
- **计费单元**：模型部署新增按模型单元（MU）时长计费模式；Token Plan 团队版支持跨坐席共享 Credits 弹性用量包。

## 使用方式

- **模型调用**：通过标准 API（如 `/v1/chat/completions`）调用，支持 OpenAI、Anthropic 兼容接口；新模型需使用对应 Model ID（如 `qwen3.8-flash`），不可复用旧别名。
- **功能接入**：
  - [异步任务](../concepts/asynchronous-task.md)：在请求中添加 `background=true`，后续通过轮询或 EventBridge 回调获取结果；
  - 知识库服务：调用 `/v1/knowledge_retrieval` 或 `/v1/knowledge_qa` 接口；
  - 智能体托管：使用 `managed-agents-api` 文档中定义的运行时 API；
  - 模型导入：通过 `model-fine-tuning-text-generation-api/custom-models-api` 提交 LoRA 微调模型。
- **配置与监控**：使用 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) 页面检查模型调用情况；用量与免费额度统计看板位于 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 限制和注意事项

- **模型下线强制迁移**：正式版模型自“启动下线”起逐步限流，3 个月后停止服务（EoS）；预览版仅 14 天窗口期。已调用待下线模型的用户将收到邮件/短信/站内信通知。详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **预览版风险**：预览版模型（含 `preview`/`beta` 标识）更新频繁、无长期 SLA 保障，可能随时下线，**禁止用于生产环境**。
- **地域与协议约束**：部分新功能（如多模态交互 SDK）存在平台/OS 适配限制；WebSocket 协议仅适用于通义听悟 Agent 工业指令转写等特定场景。
- **兼容性提醒**：`qwen-turbo` 资源包已于 2026 年 6 月 28 日启动退市；`qwen3.8-max` 等新模型不兼容旧版 Prompt 工程模板语法，需按 [Prompt 工程 API](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md) 重构。
- **临时凭证安全**：在不可信环境调用 API 时，应使用 [生成临时 API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 文档所述方式，避免永久密钥泄露。

> **注意**：文档 1 明确规定“正式版模型下线通知不晚于 EoS 前 3 个月”，但文档 2 中“2026年7月10日 部分老旧模型下线通知”（公告号 118434）与文档 1 列出的“2026年10月10日已下线”存在时间逻辑矛盾——若 7 月已发通知，则 EoS 应不早于 10 月，而文档 1 将其列为“已下线”，表明实际 EoS 可能早于通知发布时间。开发者应以官网公告原文时间戳为准，而非文档 1 的汇总列表。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


