# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方模型，并统一通过业务空间专属域名接入，保障推理性能与稳定性。

## 支持的模型/功能

- **核心模型**：Qwen 系列（`qwen4-max-preview`、`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen3-vl-plus`、`qwen3.8-omni-flash` 等）、Qwen-Coder、Qwen-Audio（仅 DashScope 协议）、Qwen-Math；第三方模型包括 DeepSeek（v4 系列）、Kimi（k3/k3.1-pro）、GLM（5.x）、MiniMax（M2.5/M3.1-Flash）等。
- **多模态能力**：Qwen-VL、Qwen-Omni、QVQ 等模型支持图像、视频（URL 或 Base64）、音频（`input_audio`）输入；视频支持 `fps`、`min_pixels`、`max_pixels`、`total_pixels` 等精细控制参数 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **高级功能**：
  - **工具调用（Function Calling）**：OpenAI 兼容 Responses API 内置联网搜索、网页抓取、代码解释器、文搜图等工具；Anthropic 兼容 Messages API 支持自定义 `tools` 及 `web_search_20250305` 等服务端工具 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
  - **显式缓存**：通过 `cache_control: {type: "ephemeral"}` 在 `system`、`text` 或 `image` 内容块中标记缓存断点，提升重复请求效率。
  - **深度思考（Reasoning）**：Anthropic 协议通过 `thinking.type` 和 `output_config.effort` 控制；Responses API 通过 `reasoning.effort` 参数启用 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。

> **注意**：Qwen-Audio 明确不支持 OpenAI 兼容协议，仅可通过 DashScope 协议调用；QwQ 模型不建议设置 `system` 消息，QVQ 模型设置 `system` 不生效 —— 此矛盾信息在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中一致，属设计限制，非文档错误。

## 关键参数

| 参数 | 协议 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | 全协议必选 | 模型 ID，需与所选协议支持范围匹配 | `"qwen3.8-max"` |
| `messages` / `input` | OpenAI Chat / Responses | 对话上下文数组（Chat）或灵活输入（字符串/数组，Responses） | `[{"role":"user","content":"你好"}]` |
| `system` | Anthropic 必选（可选） | Anthropic 协议专用系统提示字段，支持字符串或结构化数组 | `"你是一个助手"` |
| `max_tokens` | Anthropic 必选 | 输出长度上限，语义因模型而异（如 `glm-5.3` 包含思考 Token） | `2048` |
| `stream` | 全协议可选 | 是否启用流式响应 | `true` |
| `temperature` | 全协议可选 | 采样温度，OpenAI/Anthropic 协议取值范围为 `[0, 2)`，非 `[0, 1)` | `0.7` |
| `reasoning.effort` | Responses 专用 | 思考强度控制（`none`/`low`/`high`/`max`） | `"high"` |
| `output_config.effort` | Anthropic 专用 | 替代已废弃的 `thinking.budget_tokens`，控制推理力度 | `"xhigh"` |

> **注意**：`thinking.budget_tokens` 参数在 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 中明确标注为“即将废弃”，新接入必须使用 `output_config.effort`，避免未来兼容性风险。

## 使用方式

- **接入地址（Base URL）**：  
  所有协议均推荐使用业务空间专属域名（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），替代旧版 `dashscope.aliyuncs.com`。`{WorkspaceId}` 需替换为控制台获取的真实 ID。  
  - OpenAI 兼容：`/compatible-mode/v1/chat/completions`（Chat）、`/compatible-mode/v1/responses`（Responses）  
  - Anthropic 兼容：`/apps/anthropic/v1/messages`  
  - DashScope 原生：`/api/v1/services/aigc/text-generation/generation`（文本）、`/api/v1/services/aigc/multimodal-generation/generation`（多模态）  

- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key`（Anthropic）请求头传入 [百炼 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **SDK 配置示例（Python）**：  
  ```python
  # OpenAI 兼容
  from openai import OpenAI
  client = OpenAI(api_key="sk-xxx", base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
  
  # Anthropic 兼容（需安装 anthropic>=0.40.0）
  from anthropic import Anthropic
  client = Anthropic(api_key="sk-xxx", base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic")
  ```

## 限制和注意事项

- **地域可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）仅在中国站华北2（北京）地域可用，调用前需在控制台开通对应服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。  
- **Responses API 特有约束**：  
  - 最大输入上下文约为模型窗口的 80%，超出部分自动截断（不报错）；  
  - `/api/v2/apps/protocols/compatible-mode/v1/responses` 旧路径已停用，必须迁移至 `/compatible-mode/v1/responses`；  
  - `previous_response_id` 与 `conversation` 参数互斥，不可同时使用。  
- **通用限制**：  
  - `store=false` 的响应无法被 `retrieve`、`delete` 或 `list-input-items` 访问；  
  - `response_id`（格式 `resp_xxx`）有效期为 7 天；  
  - 视频处理中 `fps` 范围为 `[0.1, 10]`，但 MiniMax 模型限定为 `[0.2, 5]`，需按模型校验。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)


