# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容（Chat 和 Responses）、DashScope 原生协议及 Anthropic 兼容协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen4-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方直供模型。统一采用业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）进行调用，推荐迁移以获得更优性能与稳定性。

## 支持的模型/功能

Qwen API 支持三类核心调用协议，覆盖不同使用场景：

- **OpenAI 兼容 Chat**：适用于标准对话场景，完全兼容 `chat/completions` 接口，支持多模态输入（文本、图像、音频、视频），但 [Qwen-Audio 不支持 OpenAI 兼容协议](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)，仅支持 DashScope 协议。
- **OpenAI 兼容 Responses**：面向复杂 Agent 场景，内置联网搜索、代码解释器、知识库检索等工具链，支持 `previous_response_id` 简化多轮上下文管理，并提供 `x-dashscope-session-cache: enable` 自动缓存机制。其模型支持范围与 Chat 接口存在差异，例如 `qwen3.8-omni-flash` 在 Responses 中明确支持 `input_audio` 和 `input_video` 类型，而 Chat 接口中未列出该能力。
- **Anthropic 兼容 Messages**：适配 Anthropic 生态迁移，支持 `thinking` 块、结构化工具调用（`tool_use`/`tool_result`）及显式缓存控制，但 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，需注意参数适配。
- **DashScope 原生协议**：提供最底层、最完整的功能支持，如 `max_frames` 视频帧数控制（[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 明确支持，而 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)未提及），以及对 `qwen-audio` 的完整支持。

> **注意**：文档 1 与文档 7 对 `min_pixels` / `max_pixels` 的取值说明存在不一致。文档 1（OpenAI 兼容 Chat）中 `qwen4-max` 图像 `max_pixels` 最大值为 `16777216`；文档 7（DashScope）中相同字段描述为“最大值为 `16777216`”，但后续示例误写为 `"max_frame": 2000`（应为 `max_frames` 且属视频参数）。实际应以文档 1 的数值为准，`max_frames` 是独立参数，仅 DashScope 支持。

## 关键参数

| 参数 | 协议适用性 | 说明 |
|------|------------|------|
| `model` | 全部 | 必选。模型名需严格匹配，如 `qwen4-max`、`qwen3.7-plus`、`qwen3-vl-plus`。OpenAI Chat 与 Responses 支持的模型列表不完全重合，Responses 明确列出 `deepseek-v4.1-flash` 等型号，而 Chat 文档仅泛称“DeepSeek（阿里云直供、硅基流动直供……）”。 |
| `messages` / `input` / `content` | Chat / Responses / Anthropic | Chat 和 DashScope 使用 `messages` 数组；Responses 支持 `string` 或 `array` 格式的 `input`；Anthropic 使用 `messages` 但内容结构更丰富（支持 `image`/`video`/`document`/`tool_use` 等类型块）。 |
| `max_tokens` | Anthropic、Responses（隐含） | Anthropic 协议中为必选，语义因模型而异（如 `qwen4-max` 包含思考 Token）；Responses 协议通过 `reasoning.effort` 控制思考强度，不直接暴露 `max_tokens`。 |
| `reasoning.effort` | Responses | Responses 特有，用于控制思考强度（`none`/`low`/`medium`/`high`），替代 Anthropic 的 `thinking.budget_tokens`（后者已标记为“即将废弃”）。 |
| `detail`, `min_pixels`, `max_pixels`, `fps`, `max_frames` | Chat / DashScope / Anthropic | 多模态参数。`detail` 和 `fps` 在三者中均有定义；`min_pixels`/`max_pixels` 在 Chat 和 DashScope 中详细说明；`max_frames` 仅 DashScope 支持（见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）。 |

## 使用方式

1. **认证与端点配置**：  
   所有协议均需 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并通过 `{WorkspaceId}` 替换业务空间 ID 构建 `base_url`。地域端点统一格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，支持 `cn-beijing`、`ap-southeast-1`、`us-east-1`、`eu-central-1`、`ap-northeast-1`、`cn-hongkong`。  
   - OpenAI Chat/Responses：路径为 `/compatible-mode/v1/chat/completions` 或 `/compatible-mode/v1/responses`。  
   - Anthropic：路径为 `/apps/anthropic/v1/messages`。  
   - DashScope：路径为 `/api/v1/services/aigc/text-generation/generation`（文本）或 `/multimodal-generation/generation`（多模态）。

2. **SDK 调用示例（Python）**：  
   ```python
   # OpenAI Chat（兼容）
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   response = client.chat.completions.create(model="qwen3.7-plus", messages=[{"role":"user","content":"你好"}])

   # Responses（增强版）
   response = client.responses.create(
       model="qwen3.8-omni-flash",
       input=[{"role":"user","content":[{"type":"input_audio","format":"mp3","audio_url":"https://..."}]}]
   )

   # Anthropic（兼容）
   from anthropic import Anthropic
   client = Anthropic(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"
   )
   response = client.messages.create(
       model="qwen4-max",
       max_tokens=1024,
       messages=[{"role":"user","content":"分析这张图","type":"image","source":{"type":"url","url":"https://..."}}]
   )
   ```

3. **多轮对话管理**：  
   - Chat：需手动维护 `messages` 数组并追加历史交互。  
   - Responses：使用 `previous_response_id` 字段自动关联上一轮响应，无需拼接完整历史。  
   - Anthropic：通过 `messages` 数组自然延续，支持 `tool_use`/`tool_result` 交互。

## 限制和注意事项

- **地域与模型可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）仅在中国站华北2（北京）地域可用，调用前需在百炼控制台开通对应服务（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **协议能力边界**：  
  - Qwen-Audio 仅支持 DashScope 协议，不支持 OpenAI 兼容协议（[原文标题](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 明确指出）。  
  - OpenAI Responses API 不支持异步 `background` 参数，旧版 URL `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用，必须迁移至 `/compatible-mode/v1/responses`（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。  
- **缓存与计费**：Session 缓存（`x-dashscope-session-cache`）和显式缓存（`prompt_cache_breakpoint`、`cache_control`）均影响 Token 计费逻辑，命中缓存的 Token 会体现在 `usage.input_tokens_details.cached_tokens` 中，需在成本监控中关注。
- **错误处理**：`GET /responses/{id}` 和 `DELETE /responses/{id}` 仅对 `store=true` 创建的响应有效，否则返回 `Response with id 'resp_xxx' not found.` 错误（见 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md) 和 [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)）。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)


