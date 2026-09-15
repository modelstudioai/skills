# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一 Runtime 运行，支持快速集成、参数化配置与轻量定制。开发者可通过控制台或 OpenAPI 直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用已绑定适配的底层模型（如 Qwen-VL、Qwen-Audio、Qwen2.5-72B 等）及配套工具集，覆盖教育辅导、语音对话分析、客服机器人、数据挖掘、深度搜索、UI 自动化等场景。例如，[官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 集成 ASR + NLU + 摘要生成流水线；[通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 依赖多模态视觉理解与动作规划模型；[通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 则组合检索增强与推理模型协同工作。

> **注意**：部分文档中提及的“支持 Qwen1.5 系列模型”已过时——自 v2.3.0 起，所有新上架应用默认使用 Qwen2 或 Qwen2.5 系列，旧模型仅限存量应用兼容运行，详见 [官方应用-通义数据挖掘](../../raw/application-user-guide/application-gallery/tongyi-docmining.md) 的版本说明章节。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（可在控制台应用详情页获取）；
- `input`：JSON 对象，结构由具体应用定义（如 `{"query": "..."}` 或 `{"audio_url": "..."}`）；
- `parameters`（可选）：覆盖应用默认配置，常见字段包括 `temperature`、`max_output_tokens`、`enable_citation`（仅限检索类应用）；
- `stream`（布尔值）：是否启用流式响应，默认 `false`。

各应用支持的 `parameters` 字段存在差异，完整列表请参考对应应用文档，例如 [官方应用-伶鹊CCAI-对话分析AIO](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-dialogue-analysis-aio.md) 明确列出 `analysis_dimensions` 和 `output_format` 可配置项。

## 使用方式

1. **控制台调用**：进入「应用广场」页面 → 选择目标应用 → 点击「试用」→ 填写输入并提交；
2. **OpenAPI 调用**：向 `POST /v1/applications/{app_id}/invoke` 发送请求，Header 中携带 `Authorization: Bearer <api_key>`；
3. **嵌入 SDK**：使用 `@alibaba/bailian-sdk` 的 `invokeApplication()` 方法，传入 `app_id` 与 `input` 即可（Node.js/Python/Java SDK 均支持）。

所有方式均复用同一鉴权与限流体系，无需额外配置模型 endpoint。

## 限制和注意事项

- 单次调用 `input` 大小上限为 10 MB（含 base64 编码图像/音频），超限将返回 `400 Bad Request`；
- 免费试用额度仅限控制台交互，API 调用需绑定计费项目并确保余额充足；
- 应用间**不共享上下文**：即使连续调用同一 `app_id` 的多次请求，也不会自动维护 session 状态，如需长程对话，请自行管理 `session_id` 并在 `input` 中显式传递；
- 部分应用（如 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)）对输入文本有法律领域术语校验，非合规内容将被拦截并返回结构化错误码 `INVALID_INPUT_DOMAIN`。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


