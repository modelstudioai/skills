# qwen api reference

阿里云百炼平台提供多种兼容主流协议的 Qwen 模型调用方式，包括 OpenAI 兼容 Chat/Responses、DashScope 原生 API 和 Anthropic 兼容 Messages。开发者可根据现有技术栈选择最适配的接口，所有路径均支持多地域部署与业务空间专属域名，兼顾性能、稳定性与功能完整性。

## 支持的模型/功能

Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen3-vl-plus`）是核心支持对象，同时兼容第三方直供模型（如 `deepseek-v4.1-flash`、`glm-5.3`、`kimi-k3`）。不同 API 协议支持的功能存在差异：

- **OpenAI 兼容 Chat API**：支持标准 `chat/completions` 流式/非流式调用，适用于通用对话场景；但明确不支持 Qwen-Audio 模型（仅 DashScope 协议支持）[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **OpenAI 兼容 Responses API**：在 Chat 基础上增强 Agent 能力，内置联网搜索、网页抓取、代码解释器等工具，并支持 `previous_response_id` 简化多轮上下文管理 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **DashScope 原生 API**：提供最完整的功能覆盖，包括纯文本生成（`text-generation`）与多模态生成（`multimodal-generation`）两类端点，且明确支持 Qwen-Audio 及 `max_frames` 等视频处理参数 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。
- **Anthropic 兼容 Messages API**：支持 `system` 提示、结构化输出（`format`）、深度思考（`thinking` 与 `output_config.effort`），但 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需注意调整 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

> **注意**：文档 1 与文档 7 对 `min_pixels`/`max_pixels` 的默认值描述存在细微差异（如 `Qwen2.5-VL` 图像输入最小值，文档 1 写为 `3136`，文档 7 未明确最小值但示例值一致），以文档 1 为准；文档 3 中 `responses` API 列出的模型列表（如 `qwen3.8-omni-flash`）未在文档 8 的 Anthropic 兼容模型列表中出现，表明 Omni 系列暂不支持 Anthropic 协议。

## 关键参数

| 参数 | 适用协议 | 说明 |
|------|----------|------|
| `model` | 全部 | 必填。模型名需严格匹配，例如 `qwen3.8-max`、`qwen3-vl-plus`；第三方模型需确认地域可用性（三方直供模型仅限华北2可用）[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。 |
| `messages` / `input` / `content` | Chat / Responses / Anthropic | 输入格式不同：Chat 使用标准消息数组；Responses 支持 `string` 或 `array`；Anthropic 使用 `content` 数组并区分 `text`/`image`/`video` 类型。多模态输入需匹配模型能力（如 `qwen3-vl-plus` 支持图像，`qwen3.8-omni-flash` 支持音视频）。 |
| `max_tokens` | Anthropic / Responses | Anthropic 协议中，其含义因模型而异（如 `glm-5.3` 包含思考 Token，`qwen3.7-plus` 仅限回复 Token）；Responses API 中该参数被 `reasoning.effort` 和输出长度隐式控制。 |
| `stream` | 全部 | 控制是否启用流式响应，默认 `false`。流式数据格式依协议而异（Chat 返回 SSE，Responses 返回 JSON Lines，Anthropic 返回 SSE）。 |
| `tools` | Responses / Anthropic | Responses 支持内置工具（`web_search`, `code_interpreter`）与自定义 function；Anthropic 需显式声明 `tools` 数组及 `tool_choice` 策略，且联网搜索需额外 `x-anthropic-billing-header` 标识。 |

## 使用方式

### 基础调用流程
1. **获取凭证**：在百炼控制台创建业务空间，获取对应地域的 [API Key](../../raw/model-api-reference/preparations/get-api-key.md) 与 [WorkspaceId](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)；
2. **配置 endpoint**：使用业务空间专属域名（推荐）或通用域名。例如华北2 Chat API：
   - 专属域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
   - 通用域名（不推荐）：`https://dashscope.aliyuncs.com/v1/chat/completions`
3. **发起请求**：按所选协议构造请求体（如 `messages` 数组），通过 HTTP POST 或 SDK（OpenAI/DashScope/Anthropic 官方 SDK 均可）调用。

### 多轮对话管理
- **Chat API**：手动维护 `messages` 数组，将上一轮 `assistant` 回复追加至数组末尾；
- **Responses API**：使用 `previous_response_id` 自动加载历史上下文，或通过 `conversation` 绑定会话；
- **Anthropic API**：在 `messages` 数组中按时间顺序追加 `user`/`assistant` 交互项。

### 多模态输入示例（图像）
```json
// OpenAI Chat 兼容
{
  "messages": [{
    "role": "user",
    "content": [{
      "type": "image_url",
      "image_url": { "url": "data:image/png;base64,iVBORw..." }
    }]
  }]
}
```

## 限制和注意事项

- **地域与模型绑定**：三方直供模型（如 SiliconFlow DeepSeek）仅在中国站华北2（北京）地域可用，调用前需在控制台开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **域名迁移强制要求**：旧版通用域名（`dashscope.aliyuncs.com`）虽仍可用，但官方强烈建议迁移至业务空间专属域名，以获得“卓越的性能和更高的稳定性”；旧版 Responses 路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移到 `/compatible-mode/v1/responses` [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **缓存与计费**：显式缓存（`cache_control`）仅对特定内容块生效，且命中后按缓存计费；Session 缓存（`x-dashscope-session-cache: enable`）自动生效，但需注意其对多轮对话延迟的优化效果依赖于服务端实现 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **视频处理参数**：`fps`、`min_pixels`、`max_pixels`、`total_pixels` 等参数在不同协议中支持程度不一（如 DashScope 支持 `max_frames`，OpenAI 兼容 Chat 不支持），且取值范围因模型版本而异，务必查阅对应模型文档 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)


