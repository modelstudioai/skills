# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及多模态能力（图像、视频、音频理解），并统一通过业务空间专属域名接入，保障推理性能与稳定性。

## 支持的模型/功能

- **核心模型**：Qwen 系列（`qwen3.8-*`、`qwen3.7-*`、`qwen3.6-*`、`qwen3.5-*`、`qwen-plus`、`qwen-flash`）、Qwen-VL（视觉语言）、Qwen-Omni（音视频多模态）、Qwen-Coder（代码）、Qwen-Math（数学）、Qwen-Audio（音频）；同时支持第三方直供模型（DeepSeek、Kimi、GLM、MiniMax 等），但[三方直供模型仅在中国站华北2（北京）地域可用](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **协议支持**：
  - **OpenAI 兼容**：提供 `/chat/completions`（标准对话）和 `/responses`（增强 Agent 能力）两类端点，后者内置联网搜索、网页抓取、代码解释器等工具，详见 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)；
  - **Anthropic 兼容**：提供 `/v1/messages` 端点，支持 `system` 提示、结构化输出（`output_config.format=json_schema`）和深度思考（`output_config.effort`），但[不提供 `/v1/models` 接口](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)；
  - **DashScope 原生协议**：提供 `/text-generation/generation`（纯文本）和 `/multimodal-generation/generation`（多模态）两个独立端点，参数粒度更细（如 `max_frames`、`vl_high_resolution_images`），适用于对输入控制要求严格的场景。
- **多模态能力**：
  - 图像：支持 URL、Base64 Data URI 及本地文件（SDK）；
  - 视频：支持 URL 或图像列表形式输入，可配置 `fps`（抽帧率）和 `max_frames`（最大帧数）；
  - 音频：仅 `qwen3.8-omni-flash` 在 Responses API 中支持 `input_audio` 类型，Qwen-Audio 模型**不支持 OpenAI 兼容协议**，仅支持 DashScope 协议 [qwen-api-via-dashscope.md](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：文档 2 和文档 8 对 `min_pixels`/`max_pixels` 的默认值描述存在差异（如 `qwen-vl-plus` 图像输入默认值，文档 2 写为 `4096`，文档 8 写为 `4096`，表面一致但文档 8 缺少部分型号说明）。经核对，以文档 2 的完整表格为准；文档 8 中 `max_frames` 参数在 OpenAI 兼容 API 中明确声明“不支持自定义”，该限制需严格遵守。

## 关键参数

| 参数 | 适用协议 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必选，模型 ID。OpenAI 兼容中支持 `qwen3.8-max` 等；DashScope 中还支持 `qwen-audio`。 | `"qwen3.7-plus"` |
| `messages` / `input` | OpenAI Chat / Responses | 对话上下文数组（Chat）或灵活输入（字符串/数组，Responses）。Responses 支持 `previous_response_id` 简化多轮管理。 | `[{"role":"user","content":"你好"}]` |
| `system` | Anthropic | 可选系统提示，支持字符串或带 `cache_control` 的数组。 | `"你是一个专业助手"` |
| `max_tokens` | Anthropic | 必选，控制输出长度。注意：对 `deepseek-v4`/`glm-5.3` 等模型，它限制“回复+思考”总长；对其他模型仅限回复。 | `1024` |
| `output_config.effort` | Anthropic | 控制思考强度（`low`/`high`/`max`/`xhigh`），替代已废弃的 `thinking.budget_tokens`。 | `{"effort": "high"}` |
| `min_pixels` / `max_pixels` | OpenAI Chat & DashScope | 控制图像/视频帧分辨率下限与上限，单位为总像素。取值因模型而异，详见各文档表格。 | `{"min_pixels": 65536, "max_pixels": 2621440}` |
| `fps` | OpenAI Chat & DashScope | 视频抽帧率（帧/秒），影响动态理解精度。取值范围 `[0.1, 10]`。 | `{"fps": 2}` |
| `tools` | OpenAI Responses | 启用内置工具（`web_search`, `code_interpreter`）或自定义 function 工具。 | `[{"type": "web_search"}]` |

## 使用方式

- **基础接入**：所有协议均需替换 `{WorkspaceId}` 为真实业务空间 ID，并使用百炼 API Key 认证（`Authorization: Bearer <key>` 或 `x-api-key` 头）。强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但新域名提供更高性能与稳定性 [qwen-api-via-openai-chat-completions.md](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **OpenAI SDK 调用**（推荐 Chat/Responses）：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="sk-xxx",
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  # Chat
  client.chat.completions.create(model="qwen3.7-plus", messages=[...])
  # Responses (带工具)
  client.responses.create(model="qwen3.8-max", input="分析这个图表", tools=[{"type": "code_interpreter"}])
  ```
- **Anthropic SDK 调用**：
  ```python
  import anthropic
  client = anthropic.Anthropic(
      api_key="sk-xxx",
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"
  )
  client.messages.create(model="qwen3.8-max", max_tokens=1024, messages=[...], output_config={"effort": "xhigh"})
  ```
- **DashScope SDK 调用**：
  ```python
  import dashscope
  dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
  # 纯文本
  dashscope.Generation.call(model="qwen-plus", input={"messages": [...]})
  # 多模态（含视频）
  dashscope.MultiModalConversation.call(model="qwen3-vl-plus", input={"messages": [{"role":"user","content":[{"video":"https://x.mp4","fps":2}]}]})
  ```

## 限制和注意事项

- **协议差异**：OpenAI 兼容的 `/responses` API 不支持 `background`（异步）参数，仅同步调用；其 `input` 字段比 Chat 更灵活（支持字符串、消息数组、上一轮 `ResponseOutputMessage` 直接复用），但[部分 OpenAI 参数会被忽略](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **上下文管理**：Responses API 的最大输入上下文约为模型窗口的 80%（预留 20% 给工具调用），超出部分自动截断；Anthropic 的 `system` 提示在 `qwen3.8-max` 等模型中默认生效，但 `QwQ` 模型不建议设置，`QVQ` 模型则无效。
- **缓存与计费**：启用 Session 缓存（`x-dashscope-session-cache: enable`）可降低多轮延迟；显式缓存（`cache_control: {type: "ephemeral"}`）需在 Anthropic 或 OpenAI Chat 的 `messages`/`system` 中标记，命中后按缓存计费。
- **错误处理**：`GET /responses/{id}` 和 `GET /responses/{id}/input_items` 仅当创建时 `store=true` 才可查询；`DELETE /responses/{id}` 同理。未找到 ID 时返回 `InvalidParameter` 错误。
- **模型能力边界**：Qwen-Audio 仅支持 DashScope 协议；QwQ/QVQ 模型对 `system` 消息的支持有限；结构化 JSON 输出在非 `qwen3.8+/deepseek/glm` 系列模型上需提示词含 "JSON" 关键词且显式传 `output_config`，否则报错。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


