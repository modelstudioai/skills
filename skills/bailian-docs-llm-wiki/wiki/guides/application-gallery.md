# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一 Runtime 运行，支持快速集成、参数化配置与轻量定制。开发者可通过控制台或 OpenAPI 直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用已绑定适配的底层模型（如 Qwen-VL、Qwen-Audio、Qwen2.5-72B 等）及配套工具集，覆盖教育辅导、语音对话分析、客服机器人、数据挖掘、深度搜索、UI 自动化等场景。例如，[官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 集成 ASR + NLU + 摘要生成流水线；[通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 依赖多模态视觉理解与动作规划模型；[通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 则组合检索增强与推理模型协同工作。

> **注意**：部分文档中提及的“支持 Qwen1.5 系列模型”已过时——自 v2.3.0 起，所有新上架应用默认使用 Qwen2 或 Qwen2.5 系列，旧模型仅限存量应用兼容运行，详见 [官方应用-通义数据挖掘](../../raw/application-user-guide/application-gallery/tongyi-docmining.md) 的版本说明章节。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（可在控制台应用详情页获取）；
- `input`：JSON 对象，结构由具体应用定义（如 `{"query": "..."}` 或 `{"audio_url": "..."}`）；
- `parameters`（可选）：用于覆盖应用默认配置，常见字段包括 `temperature`（仅对 LLM 类应用生效）、`max_output_tokens`、`enable_citation`（启用引用溯源）等；
- `stream`（布尔值）：是否启用流式响应，默认 `false`。

各应用支持的 `parameters` 字段存在差异，完整列表请参考对应应用文档，例如 [官方应用-伶鹊CCAI-对话分析AIO](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-dialogue-analysis-aio.md) 明确要求 `analysis_type` 必填。

## 使用方式

1. **控制台调用**：进入「应用广场」页面 → 选择目标应用 → 点击「试用」→ 填写输入并提交；
2. **OpenAPI 调用**：向 `POST /v1/applications/{app_id}/invoke` 发送请求，Header 中携带 `Authorization: Bearer <api_key>`；
3. **嵌入 SDK**：使用 `@alibaba/bailian-sdk` 的 `invokeApplication()` 方法（Node.js/Python SDK 均支持），示例见 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md) 的 Quick Start 章节。

## 限制和注意事项

- 单次调用 `input` 总大小上限为 10 MB（含文本、Base64 图片、音频 URL 等）；
- 流式响应仅支持文本类应用，多模态输出（如图像生成、视频摘要）不支持 `stream=true`；
- 应用间**不共享会话状态**，如需上下文保持，须自行维护 `session_id` 并在每次请求中显式传入（部分应用如 `lingque-ccai-voice-dialogue-robot` 已内置 session 管理，详见其文档）；
- 免费额度仅覆盖基础调用量，高并发或长上下文场景需提前申请配额扩容。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


