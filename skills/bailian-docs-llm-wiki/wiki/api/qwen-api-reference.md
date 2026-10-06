# qwen api reference

阿里云百炼平台提供多种 API 接口协议（OpenAI 兼容、Anthropic 兼容、DashScope 原生）调用 Qwen 系列大模型，支持文本、多模态、代码、数学、音频、视频等全场景能力。开发者可根据技术栈偏好选择对应协议，所有接口均基于业务空间专属域名统一接入，具备高性能与高稳定性保障。

## 支持的模型/功能

Qwen API 支持以下核心模型类型及能力：

- **文本生成模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen-turbo`、`qwen-coder-next`、`qwen-math` 等；
- **多模态模型**：`qwen3.8-omni-flash`（音视频理解）、`qwen3-vl-plus`、`qwen-vl-max`、`qwen3.5-Omni`、`QVQ` 系列（视觉推理）；
- **第三方直供模型**：DeepSeek（硅基流动/阿里云直供）、Kimi（月之暗面/阿里云直供）、GLM（智谱）、MiniMax（稀宇科技/阿里云直供）；
- **专用能力**：
  - 内置工具链（联网搜索、网页抓取、代码解释器、文搜图、图搜图、知识库搜索），仅 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 和 Anthropic Messages API 完整支持；
  - 结构化输出（JSON Schema 强约束），在 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 中通过 `output_config.format` 启用；
  - 显式缓存与 Session 缓存，降低多轮对话延迟，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 文档；
  - 音视频输入支持：`qwen3.8-omni-flash` 支持 `input_audio`/`input_video` 类型；`qwen3.5-Omni`、`Qwen3-VL`、`QVQ` 支持 `video_url`/`video`/`image_url` 等格式。

> **注意**：Qwen-Audio **不支持 OpenAI 兼容协议**，仅可通过 DashScope 原生 API 调用（见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）；QwQ 模型不建议设置 `system` 消息，QVQ 模型中 `system` 消息无效。

## 关键参数

| 参数 | 协议适用性 | 说明 | 示例值 |
|------|------------|------|--------|
| `model` | 全协议必选 | 模型 ID，需与所选协议支持列表严格匹配。[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)支持更广的三方模型，DashScope 原生接口对 Qwen-Audio 等专用模型支持更完整。 | `"qwen3.8-omni-flash"`, `"qwen3-vl-plus"` |
| `messages` / `input` | Chat & DashScope：`messages`；Responses：`input`（支持 string/array） | 对话上下文数组或纯文本输入。`messages` 中 `content` 支持 `text`/`image_url`/`video_url`/`input_audio` 等结构化类型。 | `[{"role":"user","content":[{"type":"text","text":"描述这张图"},{"type":"image_url","image_url":{"url":"https://x.jpg"}}]}]` |
| `max_tokens` | Anthropic & DashScope 必选；OpenAI 兼容可选（默认由模型决定） | 控制输出长度。**注意差异**：在 Anthropic 兼容中，`qwen3.8-max` 的 `max_tokens` 包含思考 [Token](../concepts/token.md)；而 DashScope 原生接口中该参数仅限输出文本，思考 [Token](../concepts/token.md) 由 `reasoning.effort` 或 `thinking.budget_tokens` 单独控制。 | `2048` |
| `stream` | 全协议可选 | 是否启用流式响应，默认 `false`。流式返回时，OpenAI 兼容使用 `data: ...` SSE 格式，Anthropic 使用 `event: content_block_delta`。 | `true` |
| `temperature` / `top_p` | 全协议可选 | 采样控制参数。**注意差异**：Anthropic 兼容协议中 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需校准。 | `temperature=0.7`, `top_p=0.9` |
| `min_pixels` / `max_pixels` / `total_pixels` | 多模态模型专用 | 图像/视频分辨率控制参数，用于平衡精度与 [Token](../concepts/token.md) 消耗。各模型默认值与取值范围在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中有详细定义，但两文档对 `qwen-vl-plus` 系列的 `min_pixels` 默认值描述不一致（前者写 `4096`，后者写 `3136`）。 > **注意**：以 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中的取值为准，因其为原生协议且更新更及时。 | `{"min_pixels": 65536, "max_pixels": 2621440}` |

## 使用方式

### 1. 接入地址（Base URL）
所有协议均采用**业务空间专属域名**，地域与路径组合如下（`{WorkspaceId}` 需替换为实际业务空间 ID）：

| 协议 | 地域 | Base URL 示例 | HTTP Endpoint 示例 |
|------|------|----------------|---------------------|
| **OpenAI 兼容** | 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `POST /chat/completions` 或 `POST /responses` |
| **Anthropic 兼容** | 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` | `POST /v1/messages` |
| **DashScope 原生** | 美国（弗吉尼亚） | `https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1` | `POST /services/aigc/text-generation/generation`（文本）或 `/multimodal-generation/generation`（多模态） |

> **重要**：旧域名（如 `dashscope.aliyuncs.com`）仍可用，但官方强烈建议迁移至业务空间专属域名以获得更高性能与稳定性，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

### 2. 认证方式
- OpenAI 兼容 & Anthropic 兼容：通过 `Authorization: Bearer <API_KEY>` 请求头传入；
- DashScope 原生：通过 `X-DashScope-Api-Key: <API_KEY>` 请求头传入；
- 所有协议均需提前[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

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
message = client.messages.create(model="qwen3.8-max", max_tokens=1024, messages=[{"role":"user","content":"你好"}])

# DashScope 原生
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
resp = dashscope.Generation.call(model="qwen3.8-max", messages=[{"role":"user","content":"你好"}])
```

## 限制和注意事项

- **地域可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，调用前需在百炼控制台开通对应服务。
- **API 路径弃用**：OpenAI 兼容-Responses 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移至 `/compatible-mode/v1/responses`（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **上下文长度**：Responses API 为预留工具调用空间，最大输入上下文约为模型窗口大小的 80%，超出部分将自动截断（不报错）；Chat API 无此显式限制，但受模型本身 context window 约束。
- **缓存行为**：Session 缓存（`x-dashscope-session-cache: enable`）仅在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中生效；显式缓存（`cache_control: {type: "ephemeral"}`）在 Anthropic 兼容接口中支持，需在 `system` 或 `messages.content` 中显式声明。
- **音视频支持边界**：
  - `qwen3.8-omni-flash` 支持 `input_audio`/`input_video`（仅 Responses API）；
  - `qwen3.5-Omni`、`Qwen3-VL`、`QVQ` 支持 `video_url`/`video`（仅 OpenAI 兼容 Chat API 和 DashScope 原生 API）；
  - `Qwen-Audio` 仅支持 DashScope 原生协议，不支持任何兼容协议。
- **计费单位**：Token 计费细粒度已暴露于响应 `usage` 字段（如 `input_tokens_details.cached_tokens`、`output_tokens_details.reasoning_tokens`），便于成本审计。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


