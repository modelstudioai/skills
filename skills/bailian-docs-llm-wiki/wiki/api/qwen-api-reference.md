# qwen api reference

阿里云百炼平台提供多种 API 接口协议（OpenAI 兼容、Anthropic 兼容、DashScope 原生）调用 Qwen 系列大模型，支持文本、多模态、工具调用、结构化输出等能力。所有接口均基于业务空间（Workspace）隔离，需配置专属域名与 API Key。开发者可根据现有技术栈选择最适配的协议，无需修改核心逻辑即可迁移。

## 支持的模型/功能

Qwen API 支持全系列千问模型及部分第三方直供模型，按协议能力分层如下：

- **OpenAI 兼容 Chat API**：支持 `qwen4-max`、`qwen3.8-max`、`qwen3.7-plus` 等主流文本/多模态模型；**不支持 Qwen-Audio**（仅 DashScope 协议支持）；三方模型（如 DeepSeek、Kimi、GLM）仅在华北2（北京）地域可用，且需在控制台开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **OpenAI 兼容 Responses API**：增强版 Chat，内置联网搜索、网页抽取、代码解释器、文搜图、知识库检索等工具链，支持 `previous_response_id` 多轮上下文管理与 `x-dashscope-session-cache` 自动缓存，适用于复杂 Agent 场景 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic 兼容 Messages API**：支持 `qwen4-max`、`qwen3.8-max`、`qwen3.7-plus` 等模型，提供 `thinking` 内容块、`document` PDF 直传、`tool_use/tool_result` 工具交互，`temperature` 取值范围为 `[0, 2)`（区别于 Anthropic 官方 `[0.0, 1.0]`）[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **DashScope 原生 API**：最底层协议，支持全部模型（含 `qwen-audio`）、细粒度参数（如 `max_frames`、`vl_high_resolution_images`），适用于需要完全控制推理流程的场景。

> **注意**：文档 1 与文档 8 对 `min_pixels` / `max_pixels` 的默认值描述存在不一致（如 `qwen3.8-max` 图像输入的 `max_pixels` 默认值，文档 1 称 `2621440`，文档 8 未明确给出）。以文档 1 的 OpenAI 兼容协议说明为准，因该协议为当前主推路径，且参数定义更完整。

## 关键参数

| 参数 | 协议支持 | 说明 |
|------|----------|------|
| `model` | 全部 | 必填。模型 ID 需严格匹配，如 `qwen3.8-max`、`qwen3.7-plus`；第三方模型名含供应商前缀（如 `deepseek-v4.1-flash`）。 |
| `messages` / `input` | Chat & DashScope / Responses | Chat/DashScope 使用标准消息数组；Responses 支持 `string` 或 `array` 输入，更灵活。 |
| `system` | Chat & Anthropic & DashScope | Anthropic 协议中为顶层字段；Chat/DashScope 中为 `messages[0]` 的 `role: system` 消息。 |
| `detail`, `min_pixels`, `max_pixels`, `fps` | Chat & DashScope | 控制多模态输入精度。`detail` 仅对 `qwen4-max` 生效；`max_pixels` 在 `vl_high_resolution_images=true` 时被忽略；`fps` 同时影响抽帧与时间建模 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。 |
| `reasoning.effort` / `output_config.effort` | Responses / Anthropic | 控制思考强度（`low`/`medium`/`high`/`auto`），非 `none` 时返回 `reasoning` 类型输出项并计费。 |
| `store`, `previous_response_id` | Responses | `store=true` 后可调用 `/responses/{id}`、`/responses/{id}/input_items` 查询历史；`previous_response_id` 实现无状态多轮对话。 |

## 使用方式

### 域名与认证
- **统一域名格式**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 为业务空间 ID（控制台获取），`{region}` 如 `cn-beijing`、`ap-southeast-1`。
- **推荐迁移**：华北2（北京）、新加坡、中国香港地域已启用专属域名，性能与稳定性更优，旧域名（`dashscope.aliyuncs.com`）仍可用但不推荐 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key: <API_KEY>`（Anthropic 协议）传递，API Key 需提前在控制台获取并配置 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 协议选择指南
- **快速迁移 OpenAI 应用** → 使用 **Chat API**（`/compatible-mode/v1/chat/completions`）或 **Responses API**（`/compatible-mode/v1/responses`，推荐用于需工具调用的场景）。
- **迁移 Anthropic 应用** → 使用 **Messages API**（`/apps/anthropic/v1/messages`），注意 `temperature` 范围与缺失 `/v1/models` 接口。
- **需要音频、PDF 解析、显式缓存断点或最大控制权** → 使用 **DashScope API**（`/api/v1/services/aigc/.../generation`）。

## 限制和注意事项

- **地域限制**：第三方直供模型（DeepSeek/Kimi/GLM/MiniMax）仅在华北2（北京）地域可用，调用前必须在控制台开通对应服务。
- **缓存行为**：Session 缓存（`x-dashscope-session-cache: enable`）自动生效，但 Responses API 的上下文长度约为模型窗口的 80%，超出部分将静默截断 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **流式响应**：Chat 和 Responses API 支持 `stream=true`，但 Responses 的流式事件结构与 Chat 不同（如 `response.output_text.delta`）；Anthropic 协议流式需解析 SSE。
- **错误处理**：`Response ID` 仅当 `store=true` 时有效；查询/删除不存在的 ID 返回 `404` 错误，需捕获 `InvalidParameter` 类型。
- **计费差异**：`reasoning_tokens`、`cached_tokens` 等细粒度 Token 在 `usage` 字段中单独返回，需按实际消耗计费，非简单 `total_tokens`。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


