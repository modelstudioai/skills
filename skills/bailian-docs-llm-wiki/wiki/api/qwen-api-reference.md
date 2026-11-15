# qwen api reference

阿里云百炼平台提供多种兼容协议的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方模型（如 DeepSeek、Kimi、GLM）。统一采用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）进行请求，推荐迁移以获得更高性能与稳定性。

## 支持的模型/功能

Qwen API 支持三类主流协议接口，覆盖不同使用场景：

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：提供 `/chat/completions`（标准对话）和 `/responses`（增强 Agent 能力）两类端点。其中 `/responses` 是百炼特有扩展，内置联网搜索、网页抓取、代码解释器、文搜图、图搜图、知识库搜索等工具，并支持 `previous_response_id` 多轮上下文管理与 `x-dashscope-session-cache` 自动缓存。该能力在 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 文档中有详细说明。
- **Anthropic 兼容接口**：提供 `/v1/messages` 端点，支持 `system` 提示、结构化 `content` 数组（含 `text`/`image`/`video`/`tool_use`）、显式缓存控制（`cache_control`）及深度思考配置（`thinking.type` 与 `output_config.effort`），适用于需要精细控制推理强度与输出格式的场景。
- **DashScope 原生接口**：提供 `/text-generation/generation`（纯文本）与 `/multimodal-generation/generation`（多模态）两个专用端点，是最早支持 Qwen-VL、Qwen-Audio 等多模态模型的协议，[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 文档中明确了其地域与模型路由规则。

> **注意**：Qwen-Audio 模型**仅支持 DashScope 协议**，不支持 OpenAI 兼容协议（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 中明确说明）。此外，`/responses` 接口的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移到新版 `/compatible-mode/v1/responses`（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。

## 关键参数

各协议共性参数（如 `model`, `temperature`, `top_p`）语义一致，但存在关键差异：

- **`model`**：必填。OpenAI 和 Anthropic 协议均接受 `qwen3.8-max`、`qwen3.7-plus` 等标准名称；DashScope 协议同理，但需注意多模态模型（如 `qwen3-vl-plus`）必须使用 `/multimodal-generation/generation` 端点（见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）。
- **多模态输入**：
  - OpenAI 协议：`messages` 中 `content` 为 `array`，元素 `type` 可为 `text`/`image_url`/`input_audio`/`video_url` 等，`image_url.url` 或 `video_url.url` 支持公网 URL 与 Base64 Data URI。
  - Anthropic 协议：`content` 数组中 `type` 为 `image` 或 `video`，`source.type` 指定 `url` 或 `base64`，并需提供 `media_type`。
  - DashScope 协议：`messages` 中 `content` 为 `object`，直接包含 `image`（字符串 URL/Base64）或 `video`（字符串 URL 或 `array` 图片列表）字段。
- **视频处理**：`fps` 参数在三类协议中均存在，但 `max_frames` 仅 DashScope 协议支持（见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)），OpenAI 和 Anthropic 协议由服务端自动应用默认值。
- **思考强度控制**：
  - OpenAI `/responses`：使用 `reasoning.effort`（如 `"high"`）。
  - Anthropic：使用 `output_config.effort`（如 `"max"`）或已废弃的 `thinking.budget_tokens`。
  - DashScope：未在原始文档中明确提及等效参数，需通过 `model` 选择预设思考强度的模型（如 `qwen3.8-max` 默认开启深度思考）。

## 使用方式

### 基础调用流程
1. **获取凭证**：先[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
2. **确定地域与 WorkspaceId**：在百炼控制台获取业务空间 ID，并根据部署地域（如华北2北京、新加坡）构造 `base_url`。
3. **选择协议与端点**：
   - 标准对话 → OpenAI `/chat/completions`
   - Agent 场景（需工具调用/多轮缓存）→ OpenAI `/responses`
   - 结构化输出/显式缓存 → Anthropic `/v1/messages`
   - 多模态（尤其 Audio）→ DashScope `/multimodal-generation/generation`
4. **发送请求**：使用 SDK（OpenAI Python/JS、Anthropic Python/JS、DashScope Python/Java）或 curl，按对应协议格式构造 `POST` 请求体。

### 示例：OpenAI `/responses` 多轮对话
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
# 第一轮：纯文本输入
resp1 = client.responses.create(model="qwen3.8-max", input="你好")
# 第二轮：复用上一轮 response_id 构建上下文
resp2 = client.responses.create(
    model="qwen3.8-max",
    input="请基于上文继续回答",
    previous_response_id=resp1.id
)
```
配套的 [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)、[获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md) 和 [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md) 接口可对存储的响应进行全生命周期管理。

## 限制和注意事项

- **地域可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站的华北2（北京）地域可用**，且需在百炼控制台单独开通（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **上下文长度**：`/responses` API 的最大输入上下文约为模型窗口的 80%，超出部分将自动截断（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）；而 `/chat/completions` 无此显式说明，应以模型文档为准。
- **参数兼容性**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**忽略所有未在文档中明确列出的参数**（如 `background` 异步参数不被支持），务必严格参照各协议文档定义（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 的“兼容性说明与限制”章节）。
- **计费单位差异**：`/responses` 接口的 `created_at` 返回秒级时间戳，而 `/responses/{id}/input_items` 接口返回毫秒级时间戳（见 [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)），集成时需注意时间解析逻辑。
- **工具调用约束**：使用 `web_search` 等内置工具时，Anthropic 协议要求在 `system` 中传入 `x-anthropic-billing-header: cc_entrypoint=cli;` 才能生效（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)），而 OpenAI `/responses` 协议则无需此额外头信息。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)


