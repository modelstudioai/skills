# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一的 Runtime 执行环境部署，支持快速集成、参数化调用与轻量定制。开发者可通过 API 或控制台直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用均已绑定特定模型栈与功能边界，例如：
- `通义听悟Agent` 依赖 ASR + LLM + TTS 多阶段流水线，专用于会议纪要生成与语音内容结构化；
- `通义 UI Agent` 基于视觉语言模型（VLM）与动作规划模块，支持网页/APP 界面理解与自动化操作；
- `千问联网检索Agent` 集成 Qwen-Long 与实时搜索插件，提供带引用的动态知识响应。

全部官方应用列表及对应能力说明见 [应用广场](../../raw/application-user-guide/application-gallery.md)。各子应用的技术细节（如输入 schema、输出格式、支持的文件类型）请查阅其独立文档，例如 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md) 和 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（如 `tingwu-agent`, `ui-agent`），可在控制台或 [应用广场](../../raw/application-user-guide/application-gallery.md) 文档中查得；
- `input`：JSON 对象，结构依应用而异（如 `aipodcast` 要求 `{"script": "...", "voice": "zhitian_001"}`，而 `web-search-agent` 要求 `{"query": "..."}`）；
- `timeout`：最大执行时长（单位：秒），默认 300，部分长流程应用（如 `tongyi-deepsearch`）建议设为 600+。

> **注意**：部分旧版文档（如 [官方应用-伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md)）仍列出已弃用的 `session_id` 参数；当前 v2.3+ Runtime 已统一由平台自动管理会话状态，该字段可忽略。

## 使用方式

1. **API 调用**：向 `POST /v1/applications/{app_id}/invoke` 发送请求，Header 中携带 `Authorization: Bearer <api_key>`；
2. **控制台调试**：在「应用广场」页面点击目标应用 → 「在线调试」Tab，填写 input JSON 后执行；
3. **嵌入集成**：通过 SDK（如 `dashscope` Python 包）调用 `Application.invoke(app_id=..., input={...})`。

所有调用均遵循平台统一鉴权与配额体系，具体限流策略参见 [应用广场](../../raw/application-user-guide/application-gallery.md) 的「使用约束」章节。

## 限制和注意事项

- 单次调用 `input` 总大小上限为 10 MB（含 base64 编码文件），超出将返回 `413 Payload Too Large`；
- `通义数据挖掘` 和 `析言GBI` 等分析类应用暂不支持流式响应，必须等待全量结果返回；
- 应用间**不可跨实例共享上下文**：即使连续调用同一 `app_id` 的两次请求，平台也不保证状态延续（除非该应用明确声明支持 session，如 `lingque-ccai-dialogue-analysis-aio`）；
- 非官方应用（用户自建）不纳入本广场目录，亦不享受预置模型优化与 SLA 保障。

> **注意**：[官方应用-全妙轻应用系列](../../raw/application-user-guide/application-gallery/quanmiao-light-application-series.md) 文档中提及的“支持低代码编排”与当前平台实际能力不符——该系列所有应用均为原子能力封装，**不开放内部节点编排接口**；相关描述已在 v2.4 文档中修正，但原始文件尚未同步更新。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


