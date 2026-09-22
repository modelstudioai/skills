# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一 Runtime 运行，支持快速集成、参数化配置与轻量定制。开发者可通过控制台或 OpenAPI 直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用已绑定适配的底层模型（如 Qwen-VL、Qwen-Audio、Qwen2.5-72B 等）及配套工具集，覆盖教育辅导、语音对话分析、客服机器人、数据挖掘、深度搜索、UI 自动化等场景。例如，[官方应用-通义拍照解题辅导](../../raw/application-user-guide/application-gallery/edu-tutor.md) 基于多模态理解模型实现图像+文本联合推理；[通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md) 集成法律垂类微调模型与法规知识图谱；[通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 则依赖视觉定位与动作规划双模块协同。

> **注意**：部分文档中提及的“支持 Qwen1.5-32B”已过时——当前所有新上线应用默认使用 Qwen2.5 系列模型，旧版模型仅在兼容模式下可选，详见 [官方应用-通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 的 runtime 版本说明。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（如 `edu-tutor`, `tongyi-farui`），可在控制台应用列表页获取；
- `input`：结构化输入对象，schema 因应用而异（如 `edu-tutor` 要求 `{"image_url": "...", "question": "..."}`，`web-search-agent` 要求 `{"query": "...", "max_results": 5}`）；
- `parameters`（可选）：覆盖应用默认配置，常见字段包括 `temperature`、`max_tokens`、`enable_citation`（是否返回引用来源）等。

所有参数定义以各应用子文档为准，例如 [官方应用-伶鹊CCAI-对话分析AIO](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-dialogue-analysis-aio.md) 明确要求 `input` 必须包含 `transcript` 字段且长度 ≤ 10000 字符。

## 使用方式

1. **控制台调用**：进入「应用广场」页面 → 选择目标应用 → 点击「调试」，填写 input 并提交；
2. **OpenAPI 调用**：POST `/v1/applications/{app_id}/invoke`，Header 中携带 `Authorization: Bearer <api_key>`；
3. **嵌入 SDK**：使用 `@alibaba/bailian-sdk` 的 `invokeApplication()` 方法，传入 `app_id` 与 `input` 对象。

所有方式均共享同一鉴权体系与配额限制，无需额外开通权限。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 10 MB（含 base64 图片/音频）；
- 音频类应用（如 [官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md)）仅支持 WAV/MP3 格式，采样率须为 16kHz；
- 应用间不共享会话状态，如需上下文连续，须自行维护 `session_id` 并在每次请求中显式传递（部分应用如 `lingque-ccai-voice-dialogue-robot` 已支持该字段）；
- 免费试用额度仅适用于首次部署的前 3 个应用实例，超出后按实际 token 消耗计费。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


