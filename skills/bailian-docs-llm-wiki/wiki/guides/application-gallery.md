# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一的 Runtime 执行环境部署，支持快速集成、参数化调用与轻量定制。开发者可通过 API 或控制台直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用均已绑定特定模型栈与功能边界，例如：
- `通义听悟Agent` 依赖 ASR + LLM + TTS 多阶段流水线，专用于会议纪要生成与语音内容结构化；
- `通义 UI Agent` 基于视觉语言模型（VLM）与动作规划模块，支持网页/APP 界面理解与自动化操作；
- `千问联网检索Agent` 集成 Qwen-72B + RAG 检索增强模块，实时调用搜索引擎接口补充知识。

全部官方应用清单及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。

## 关键参数

调用任一应用时，需传入以下通用参数（部分应用支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，如 `tingwu-agent`、`ui-agent`，可在 [应用广场](../../raw/application-user-guide/application-gallery.md) 中查得 |
| `input` | object | 是 | 输入数据结构，格式因应用而异（如 `tingwu-agent` 接受音频 URL，`ui-agent` 接受截图 base64） |
| `parameters` | object | 否 | 可选配置项，例如 `max_steps`（UI Agent 最大操作步数）、`enable_web_search`（联网检索 Agent 开关） |

具体参数定义请参考各应用子文档，例如 [官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 和 [通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md)。

## 使用方式

1. **获取 app_id**：从 [应用广场](../../raw/application-user-guide/application-gallery.md) 列表中确认目标应用 ID（如 `web-search-agent`）；  
2. **构造请求体**：按对应子文档要求组织 `input` 与 `parameters`；  
3. **调用 API**：向 `/v1/applications/{app_id}/invoke` 发送 POST 请求（需携带有效 `Authorization` 头）；  
4. **处理响应**：返回为标准 JSON，含 `output` 字段（结构化结果）与 `trace_id`（用于问题排查）。

> **注意**：部分旧版文档（如 [官方应用-伶鹊CCAI-客服对话Agent](../../raw/application-user-guide/application-gallery/official-application-voicepica-ccai-beebot-agent.md)）中仍标注使用 `/v1/agents/{id}/run` 路径，该路径已废弃，请统一使用 `/v1/applications/{app_id}/invoke`。

## 限制和注意事项

- 单次调用最大输入长度受限于底层模型上下文窗口（如 `tongyi-farui` 为 32k tokens，`web-search-agent` 为 8k tokens），超长内容将被截断；
- 音频类应用（如 `tingwu-agent`、`aipodcast`）仅支持 MP3/WAV 格式，且单文件 ≤ 100MB；
- 所有应用默认启用流式响应（`stream=true`），若需完整响应请显式设置 `stream=false`；
- 应用间不共享会话状态，如需持久化上下文，须由调用方自行维护 `session_id` 并传入 `parameters.session_id`（部分应用支持，详见对应子文档，例如 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)）。

---  
*注：本文档依据截至 2024Q3 的平台能力编写，具体行为以实际 API 响应为准。*

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


