# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一 Runtime 运行，支持快速集成、参数化配置与轻量定制。开发者可通过控制台或 OpenAPI 直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用已绑定适配的底层模型（如 Qwen-VL、Qwen-Audio、Qwen2.5-72B 等）及配套工具集，覆盖教育辅导、语音对话分析、客服机器人、数据挖掘、深度搜索、UI 自动化等场景。例如，[官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 集成 ASR + NLU + 摘要生成流水线；[通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 依赖多模态视觉理解与动作规划模型；[通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 则组合检索增强与推理模型协同工作。

> **注意**：部分文档中提及的“支持 Qwen1.5 系列模型”已过时——自 v2.3.0 起，所有新上架应用默认使用 Qwen2 或 Qwen2.5 系列，旧模型仅限存量应用兼容运行，详见 [官方应用-通义数据挖掘](../../raw/application-user-guide/application-gallery/tongyi-docmining.md) 的版本说明章节。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（可在控制台应用详情页获取）；
- `input`：JSON 对象，结构由具体应用定义（如 `{"image_url": "..."}` 或 `{"audio_url": "..."}`）；
- `parameters`（可选）：覆盖应用默认配置，常见字段包括 `temperature`、`max_output_tokens`、`enable_citation`（仅限检索类应用）；
- `stream`（布尔值）：是否启用流式响应，默认 `false`。

各应用专属参数详见其对应文档，例如 [官方应用-伶鹊CCAI-对话分析AIO](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-dialogue-analysis-aio.md) 要求必填 `conversation_id` 与 `speaker_role_map`。

## 使用方式

1. **控制台方式**：进入「应用广场」页面，点击目标应用 → 「立即体验」或「接入应用」，复制 `app_id` 并参考右侧 SDK 示例代码；
2. **OpenAPI 方式**：调用 `POST /v1/applications/{app_id}/chat` 接口，请求体为标准 `input` + `parameters` 结构；
3. **嵌入式集成**：通过 `@alibaba/bailian-sdk` 的 `ApplicationClient` 类初始化后调用 `.run()` 方法（Node.js/Python SDK 均支持）。

所有方式均复用平台鉴权机制（AccessKey 或 STS [Token](../concepts/token.md)），无需额外模型授权。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 50 MB（含图像、音频等二进制内容 Base64 编码后）；
- 流式响应仅支持文本输出型应用（如对话类），多模态生成类（如播客生成、UI 操作）不支持 `stream=true`；
- 应用间**不共享上下文**：即使同一 `app_id` 的多次调用，也无会话状态保持，需自行维护 `session_id` 并在 `parameters` 中透传（若应用支持）；
- 免费额度按应用独立计算，超出后按实际调用量计费，计费粒度为「成功完成的请求次数」，失败请求不计费。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


