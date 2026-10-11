# qwen api reference

阿里云百炼平台提供多种 API 接口调用 Qwen 系列大模型，包括 OpenAI 兼容、Anthropic 兼容及原生 DashScope 协议三种方式。开发者可根据现有技术栈选择最适配的协议，所有接口均支持多模态输入（文本、图像、音视频）、工具调用、显式缓存与深度思考等高级能力。本文档聚焦核心参数、模型支持与使用约束，不包含营销性描述。

## 支持的模型/功能

Qwen API 支持全系列千问模型及部分第三方模型，但不同协议支持范围存在差异：

- **OpenAI 兼容 Chat API**（`/chat/completions`）：支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen3-vl-plus`、`qwen3.8-omni-flash` 等主流商业版与开源版模型；**Qwen-Audio 不支持该协议**，仅支持 DashScope 协议 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **OpenAI 兼容 Responses API**（`/responses`）：专为 Agent 场景设计，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.3` 等模型，并明确列出完整可用模型清单 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic 兼容 Messages API**（`/v1/messages`）：支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus`、`deepseek-v4-flash-0731`、`glm-5.2` 等，但**不支持 `qwen3.8-omni-flash` 的音视频输入**，且 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **DashScope 原生 API**（`/text-generation/generation` 或 `/multimodal-generation/generation`）：覆盖最广，支持 `Qwen-Audio`、`Qwen-Math`、`Qwen-Coder` 及全部视觉模型（如 `QVQ`、`Qwen2.5-VL`），是调用非文本模型的唯一途径 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：文档 2 与文档 7 对 `Qwen-VL` 系列模型的 `max_pixels` 默认值描述不一致——文档 2 称 `Qwen3-VL` 默认 `2621440`，文档 7 称 `Qwen3.7-VL` 默认 `2621440` 但未明确 `Qwen3-VL` 商业版是否等同；实际以控制台最新模型文档为准，建议通过 [百炼控制台](https://bailian.console.aliyun.com/model/market) 查验具体模型参数。

## 关键参数

| 参数 | 协议支持 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必选，模型 ID。OpenAI Chat 与 Responses API 的可选值存在差异，Responses API 列出更严格的白名单 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 | `"qwen3.8-max"` |
| `messages` / `input` | Chat & DashScope / Responses | Chat/DashScope 使用消息数组；Responses 支持 `string` 或 `array`，更灵活。`input` 中 `role` 支持 `developer`（Responses 特有）[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 | `[{ "role": "user", "content": "你好" }]` |
| `min_pixels` / `max_pixels` / `total_pixels` | Chat & DashScope | 控制图像/视频分辨率处理，单位为总像素数。`max_pixels` 行为受 `vl_high_resolution_images` 开关影响，且不同模型取值范围不同 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。 | `{"min_pixels": 65536, "max_pixels": 8388608}` |
| `fps` | Chat & DashScope | 视频抽帧频率（帧/秒），影响时间动态理解与 Token 消耗。`MiniMax/MiniMax-M3` 的取值范围为 `[0.2, 5]`，与其他模型不同 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。 | `{"fps": 2}` |
| `reasoning.effort` / `output_config.effort` | Responses / Anthropic | 控制思考强度。Responses API 使用 `reasoning.effort`（如 `"high"`），Anthropic API 使用 `output_config.effort`（如 `"xhigh"`），二者语义相同但参数路径不同 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 | `"xhigh"` |
| `tools` | Responses & Anthropic | 内置工具（如 `web_search`）与自定义 function 工具。Responses API 的 `tools` 数组结构与 Anthropic 的 `tools` schema 定义不兼容，不可直接复用 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 | `[{"type": "web_search"}]` |

## 使用方式

### 1. 基础调用
- **Endpoint**：所有协议均需替换 `{WorkspaceId}` 为真实业务空间 ID，并优先使用地域专属域名（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（如 `dashscope.aliyuncs.com`）仍可用但性能与稳定性较低 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key` 请求头传入百炼 API Key [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **SDK 配置**：OpenAI SDK 需设置 `base_url`；Anthropic SDK 同理；DashScope SDK 需配置 `base_http_api_url` [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

### 2. 多轮对话
- **Responses API**：推荐使用 `previous_response_id`（上一轮 `response.id`）自动拼接历史，或使用 `conversation` 字符串管理会话 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Chat API**：需手动维护 `messages` 数组，将上一轮 `assistant` 消息追加至数组末尾。
- **查询历史**：通过 `GET /responses/{id}/input_items` 获取某次响应的完整输入上下文（含多轮历史），支持分页 [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)。

### 3. 响应管理
- **获取/删除响应**：Responses API 提供 `GET /responses/{id}` 与 `DELETE /responses/{id}`，仅对 `store=true` 创建的响应生效 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)、[删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)。
- **[流式输出](../concepts/streaming.md)**：所有协议均支持 `stream=true`，但 Responses API 的流式事件字段为 `response.output_text.delta`，而 Chat API 为标准 OpenAI 流式格式。

## 限制和注意事项

- **协议兼容性**：OpenAI 兼容 API **不支持** OpenAI 的 `background`（异步）、`n`（并行生成）、`logit_bias` 等参数，仅处理文档明确列出的字段 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **上下文长度**：Responses API 的最大输入上下文约为模型窗口的 80%，超出部分自动截断；Chat API 无此显式说明，但受模型本身窗口限制。
- **音视频支持**：`qwen3.8-omni-flash` 是目前唯一支持 `input_audio` 和 `input_video` 的模型，且仅在 Responses API 中可用；Chat API 仅支持 `input_audio`（作为 `messages.content` 的 `type="input_audio"` 元素），不支持 `input_video` [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **废弃参数**：`thinking.budget_tokens`（Anthropic API）已被标记为“即将废弃”，新接入应使用 `output_config.effort` [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **地域限制**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，调用前需在控制台开通对应服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)


