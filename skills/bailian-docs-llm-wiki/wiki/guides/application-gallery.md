# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一的 Runtime 执行环境部署，支持快速集成、参数化调用与轻量定制。开发者可通过 API 或控制台直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用均已绑定特定模型栈与功能边界，例如：
- `通义听悟Agent` 依赖 ASR + LLM + TTS 多阶段流水线，专用于会议纪要生成与语音内容结构化；
- `通义 UI Agent` 基于视觉语言模型（VLM）与动作规划模块，支持网页/APP 界面理解与自动化操作；
- `千问联网检索Agent` 集成 Qwen-72B + 检索增强（RAG）+ 实时 Web 抓取器，适用于动态信息查询场景。

全部官方应用清单及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。

## 关键参数

调用任一应用时，需传入标准化请求体，核心字段包括：
- `app_id`：应用唯一标识（如 `tingwu-agent`, `ui-agent`），必须与 [应用广场](../../raw/application-user-guide/application-gallery.md) 中列出的 slug 严格一致；
- `input`：字符串或结构化对象（如 `{ "audio_url": "..." }`），格式依具体应用而异，详细定义见各子应用文档（例如 [官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md)）；
- `parameters`：可选运行时参数，如 `max_steps`（仅对 `ui-agent` 有效）、`enable_web_search`（仅对 `web-search-agent` 有效）。

> **注意**：部分旧版文档（如 [官方应用-伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md)）仍将 `timeout_ms` 列为必填项，但自 v2.3.0 起该参数已废弃，实际以 `request_timeout`（单位秒）为准。

## 使用方式

1. **获取应用 ID**：从 [应用广场](../../raw/application-user-guide/application-gallery.md) 页面提取目标应用的 slug（如 `tongyi-farui`）；
2. **构造请求**：使用 `/v1/applications/{app_id}/invoke` 接口，`POST` JSON 请求体；
3. **处理响应**：返回 `status: "success"` 且含 `output` 字段即表示执行完成；流式应用（如 `tingwu-agent`）支持 `Accept: text/event-stream` 头启用 SSE。

示例调用链路与错误码说明参见 [官方应用-通义数据挖掘](../../raw/application-user-guide/application-gallery/tongyi-docmining.md) 的「API 调用」章节。

## 限制和注意事项

- 单次调用最大输入长度受底层模型限制（如 `ui-agent` 输入截图分辨率上限为 1920×1080，`web-search-agent` 查询词长度 ≤ 512 字符）；
- 所有应用默认启用速率限制（10 QPS / 账号），超出将返回 `429 Too Many Requests`；
- 应用间**不共享上下文**：即使连续调用同一 `app_id` 的两次请求，也不会继承前次会话状态，需自行维护 `session_id` 并在 `parameters` 中显式传入（若应用支持）；
- 非官方应用（即用户自建应用）不在本广场范围内，其管理与调用遵循独立的 [应用管理 API 规范](../../raw/application-user-guide/application-management.md)。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


