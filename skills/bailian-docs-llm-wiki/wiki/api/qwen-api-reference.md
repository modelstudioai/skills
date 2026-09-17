# qwen api reference

阿里云百炼平台提供多种 API 接口调用 Qwen 系列模型，包括 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（Chat Completions 和 Responses）、Anthropic 兼容接口（Messages）以及原生 DashScope API。所有接口均支持多地域部署、业务空间专属域名和统一的认证机制，开发者可根据技术栈和功能需求选择最适配的协议。

## 支持的模型/功能

Qwen API 支持全系列千问模型及主流第三方模型，覆盖文本生成、多模态理解（图像/视频/音频）、代码生成、数学推理、Agent 工具调用等能力：

- **文本模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen-turbo`、`qwen-coder-next` 等；
- **多模态模型**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen3.5-ocr`、`qwen3.5-omni`（支持音视频端到端理解）；
- **第三方模型**：`deepseek-v4-pro`、`glm-5.3`、`kimi-k3`、`MiniMax-M2.5` 等（部分仅限华北2北京地域）；
- **专用能力**：
  - OpenAI 兼容 `Responses` API 内置联网搜索、网页抓取、代码解释器、文搜图、图搜图、知识库检索等工具，[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 文档详细说明了工具集成方式；
  - Anthropic 兼容 `Messages` API 支持结构化输出（JSON Schema）、深度思考（`output_config.effort`）和显式缓存，详见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)；
  - DashScope 原生 API 提供更细粒度的视频控制参数（如 `max_frames`），适用于对帧率与分辨率有强约束的场景，参见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：Qwen-Audio 模型**不支持 OpenAI 兼容协议**，仅可通过 DashScope API 调用；QwQ 模型不建议设置 `system` 消息，QVQ 模型中 `system` 消息无效 —— 此矛盾信息在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中均有明确提示，属设计一致，非文档错误。

## 关键参数

| 参数 | 作用 | 适用接口 | 说明 |
|------|------|----------|------|
| `model` | 指定模型名称 | 全部 | 必填。不同接口支持的模型列表存在差异：`Responses` API 明确列出 `qwen3.8-2.4t-a95b` 等大参数模型，而 `Chat Completions` 仅泛写为“Qwen 大语言模型”，需以 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 文档为准。 |
| `messages` / `input` | 输入内容 | Chat / Responses | `Chat Completions` 强制要求 `array` 格式；`Responses` 支持 `string` 或 `array`，且 `array` 元素类型更丰富（含 `input_file`、`function_call_output` 等）。 |
| `stream` | 流式响应开关 | 全部 | 默认 `false`。启用后返回 SSE 流，需客户端按行解析。 |
| `tools` | 工具定义与调用 | Responses / Anthropic | `Responses` 使用内置工具名（如 `{"type": "web_search"}`）；`Anthropic` 需传入完整 `input_schema`；二者均不兼容对方格式。 |
| `fps`, `min_pixels`, `max_pixels`, `total_pixels` | 视频/图像预处理控制 | Chat / DashScope | `Chat Completions` 和 `DashScope` 均支持，但 `DashScope` 独有 `max_frames` 参数；`Responses` 当前**不支持视频或语音输入**，此限制在 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 中明确声明。 |
| `reasoning.effort` / `output_config.effort` | 思考强度控制 | Responses / Anthropic | `Responses` 通过 `reasoning.effort`（值为 `none`/`low`/`high`）；`Anthropic` 通过 `output_config.effort`（值为 `xhigh`/`medium`/`low`），语义与默认值均不同，不可混用。 |

## 使用方式

### 1. 域名与认证
- **推荐域名**：使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧域名 `dashscope.aliyuncs.com`（[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 均强调此迁移建议）。
- **API Key**：通过 `Authorization: Bearer <key>` 或 `x-api-key`（Anthropic）头传递，需提前在控制台获取并配置。

### 2. 接口选型指南
- **快速迁移 OpenAI 应用** → 优先选用 `Chat Completions`（简单对话）或 `Responses`（需 Agent 能力）；
- **已有 Anthropic 集成** → 使用 `Messages` 接口，注意 `temperature` 范围为 `[0, 2)`（非官方 `[0.0, 1.0]`）；
- **需要精细控制视频帧数或本地文件直传** → 选用 `DashScope` 原生 API；
- **多轮对话管理**：`Responses` 提供 `previous_response_id` 和 `conversation` 两种模式；`Chat Completions` 需手动维护 `messages` 数组。

### 3. SDK 配置示例（Python）
```python
# OpenAI 兼容（Responses）
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
response = client.responses.create(model="qwen3.8-max", input="你好")

# Anthropic 兼容
import anthropic
client = anthropic.Anthropic(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"
)
message = client.messages.create(model="qwen3.8-max", max_tokens=1024, messages=[...])
```

## 限制和注意事项

- **地域限制**：第三方模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在控制台单独开通服务（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **功能禁用**：
  - `Responses` API **不支持异步执行**（`background` 参数已废弃）；
  - `Chat Completions` **不支持 Qwen-Audio**；
  - `Responses` **暂不支持视频或语音输入**（必须改用 `Chat Completions` 或 `DashScope`）。
- **参数兼容性**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**忽略未文档化的参数**（如 `n`、`logit_bias`），仅处理明确列出的字段（[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 中强调）。
- **缓存与计费**：显式缓存（`cache_control.type=ephemeral`）需在 `system` 或 `user` 消息中显式声明；Session 缓存（`x-dashscope-session-cache: enable`）仅 `Responses` API 支持，且自动生效无需修改请求体。
- **[Token](../concepts/token.md) 计费差异**：`Responses` API 的 `usage.output_tokens_details.reasoning_tokens` 单独计费；`Anthropic` 接口的 `thinking.budget_tokens` 参数**即将废弃**，新接入应使用 `output_config.effort`（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


