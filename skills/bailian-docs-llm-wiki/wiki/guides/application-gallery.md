# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一 Runtime 运行，支持快速集成、参数化配置与轻量定制。开发者可通过控制台或 OpenAPI 直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用已绑定适配的底层模型（如 Qwen-VL、Qwen-Audio、Qwen2.5-72B 等）及配套工具集，覆盖教育辅导、语音对话分析、客服机器人、数据挖掘、深度搜索、UI 自动化等场景。例如，[官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 集成 ASR + NLU + 摘要生成流水线；[通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 依赖多模态视觉理解与动作规划模型。部分应用（如 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)）还内置法律垂域知识图谱与推理规则引擎。

> **注意**：文档中列出的 [官方应用-伶鹊CCAI-客服对话Agent](../../raw/application-user-guide/application-gallery/official-application-voicepica-ccai-beebot-agent.md) 当前实际服务名已更新为 `lingque-ccai-customer-service-agent`，旧名称在 API 调用中将返回 404，需以控制台展示的最新 slug 为准。

## 关键参数

所有应用通过 `app_id` 唯一标识，调用时需传入：
- `input`: JSON 格式，结构依应用而异（如 `tingwu-agent` 接受 `audio_url` 或 `audio_base64`，`ui-agent` 接受 `screenshot` + `instruction`）；
- `parameters`: 可选，用于覆盖应用默认配置（如 `max_steps`、`temperature`、`enable_search`）；
- `stream`: 布尔值，仅部分应用（如 `web-search-agent`、`tongyi-deepsearch`）支持流式响应。

参数定义与约束详见各应用子文档，例如 [官方应用-通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 明确要求 `parameters.max_retrieve_count` 取值范围为 `[1, 10]`。

## 使用方式

1. **控制台调用**：进入「应用广场」页面，点击目标应用 → 「在线调试」填写输入并执行；
2. **OpenAPI 调用**：使用 `POST /v1/apps/{app_id}/chat` 接口，Header 中携带 `Authorization: Bearer <api_key>`；
3. **SDK 调用**（Python）：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = bailian_models.Client(...)
   resp = client.chat_with_app(app_id="app-xxx", input={"query": "..."})
   ```

## 限制和注意事项

- 单次请求 `input` 总大小上限为 10 MB（含 base64 编码图像/音频）；
- 免费试用应用有 QPS 限制（通常 ≤ 1），商用需开通对应应用的计费包；
- 应用间**不共享上下文**：即使同一 `app_id` 的多次调用，默认无会话状态保持，需显式传入 `session_id` 并启用 `enable_session` 参数（仅部分应用支持，参见 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md)）；
- 所有应用输出均为 JSON 格式，但字段命名不统一（如有的用 `output.text`，有的用 `result.content`），建议先查看对应应用的响应示例。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


