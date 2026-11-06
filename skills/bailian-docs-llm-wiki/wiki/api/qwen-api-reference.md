# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容（Chat 和 Responses）、Anthropic 兼容（Messages）以及原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方模型，并统一通过业务空间专属域名接入，保障性能与稳定性。

## 支持的模型/功能

- **核心模型覆盖**：  
  - 文本生成：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen-coder-flash` 等全系千问商业版与开源版；  
  - 多模态：`qwen3-vl-plus`、`qwen3.8-omni-flash`（支持音视频理解）、`QVQ`、`Qwen2.5-VL`；  
  - 第三方直供：`deepseek-v4.1-flash`、`kimi-k3.1-pro`、`glm-5.3`、`MiniMax-M2.5`（部分仅限华北2地域）[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。  
- **高级功能支持**：  
  - 工具调用（Function Calling / Web Search / Code Interpreter）：在 OpenAI Responses API 和 Anthropic Messages API 中深度集成，支持自动调用、结果回传与多轮协同；  
  - 显式缓存（`cache_control: {type: "ephemeral"}`）：适用于系统提示、用户输入及工具结果，提升重复请求效率；  
  - 结构化输出与深度思考：Anthropic 兼容接口通过 `output_config.effort` 控制推理强度，DashScope 接口支持 `reasoning.effort` 参数 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)；  
  - 视频理解增强：支持 `fps`（抽帧率）、`min_pixels`/`max_pixels`（图像分辨率控制）、`total_pixels`（总像素上限）等精细化参数，适用于 Qwen-VL、Qwen-Omni 等模型 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：Qwen-Audio 模型**不支持 OpenAI 兼容协议**，仅可通过 DashScope 原生协议调用；QwQ 模型不建议设置 `system` 消息，QVQ 模型的 `system` 消息无效 —— 此矛盾信息在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中一致，属设计限制，非文档错误。

## 关键参数

| 参数 | 适用协议 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必选，模型 ID。注意不同协议支持列表有差异：OpenAI Chat 支持更广（含三方模型），Responses API 仅明确列出 `qwen3.8-*` 等主力型号，Anthropic Messages 对 `kimi`/`glm` 的支持更细粒度 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) | `"qwen3.7-plus"` |
| `messages` / `input` | Chat / Responses | 对话上下文。Chat 要求标准数组格式；Responses 支持 `string` 或 `array`，且支持 `ResponseOutputMessage` 类型复用上一轮输出 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) | `[{"role":"user","content":"你好"}]` |
| `previous_response_id` | Responses | 必须配合 `store=true` 使用，服务端自动拼接历史上下文，简化多轮管理 | `"resp_xxx"` |
| `stream` | 全部 | 是否流式响应，默认 `false` | `true` |
| `temperature` | 全部 | 采样温度。**OpenAI/Responses 协议范围为 [0, 2)，Anthropic 协议官方为 [0.0, 1.0]，百炼实际取值范围为 [0, 2)**，迁移时需校准 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) | `0.7` |
| `fps`, `min_pixels`, `max_pixels`, `total_pixels` | Chat / DashScope | 视频/图像预处理参数，控制抽帧、缩放与 [Token](../concepts/token.md) 消耗。DashScope 协议额外支持 `max_frames`（视频帧数上限），而 OpenAI Chat 不支持该参数 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) | `{"fps": 2, "min_pixels": 65536}` |

## 使用方式

- **协议选择建议**：  
  - 已使用 OpenAI SDK：优先选用 **OpenAI 兼容 Chat API**（简单对话）或 **Responses API**（需 Agent 能力、上下文自动管理）；  
  - 已使用 Anthropic SDK：直接对接 **Anthropic Messages API**，注意 `temperature` 范围与 `output_config.effort` 替代 `thinking.budget_tokens`；  
  - 需最大灵活性或调用 Qwen-Audio：使用 **DashScope 原生协议**，区分 `text-generation` 与 `multimodal-generation` 端点。  
- **接入配置**：  
  - 所有协议均需替换 `{WorkspaceId}` 为真实业务空间 ID，并配置百炼 API Key；  
  - **强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)；  
  - OpenAI SDK 示例（Python）：  
    ```python
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    )
    response = client.chat.completions.create(model="qwen3.7-plus", messages=[...])
    ```

## 限制和注意事项

- **地域与模型可用性**：  
  - 三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在百炼控制台手动开通服务；  
  - 新加坡、美国、德国、日本、中国香港等地域的模型支持列表可能略窄，调用前请确认控制台模型市场状态。  
- **功能限制**：  
  - OpenAI Responses API **不支持异步执行**（`background` 参数已废弃），仅同步调用；  
  - `qwen3.8-omni-flash` 支持 `input_audio`/`input_video`，但 `qwen3.7-plus` 等文本模型不支持音视频输入；  
  - `thinking.budget_tokens` 参数在 Anthropic Messages API 中**已标记为“即将废弃”**，新项目应使用 `output_config.effort` [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。  
- **计费与 [Token](../concepts/token.md)**：  
  - 图像/视频 [Token](../concepts/token.md) 按像素计算（每 32×32 像素 ≈ 1 Token），`total_pixels` 限制直接影响成本；  
  - Responses API 的 `usage.output_tokens_details.reasoning_tokens` 字段明确分离思考 Token，按独立计费项结算；  
  - Session 缓存（`x-dashscope-session-cache: enable`）可降低多轮对话延迟，命中缓存的 Token 计入 `usage.input_tokens_details.cached_tokens`。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


