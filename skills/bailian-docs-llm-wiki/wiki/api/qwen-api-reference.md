# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容 Chat/Responses、Anthropic 兼容 Messages 和原生 DashScope 协议。开发者可根据技术栈和功能需求选择合适接口，所有接口均基于业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）提供高性能、高稳定性服务。

## 支持的模型/功能

Qwen 系列模型通过不同协议接口支持广泛能力：

- **核心模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen3.5-ocr`、`qwen3-vl-plus`、`qwen3-coder-flash` 等商业版与开源版模型均被全面支持。
- **多模态能力**：Qwen-VL、Qwen-Omni、QVQ、QwQ 等视觉/音视频模型支持 `image_url`、`video_url`、`input_audio`、`input_video` 等输入类型，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **Agent 工具链**：Responses API 内置联网搜索、网页抓取、代码解释器、文搜图、知识库搜索等工具；Anthropic Messages 和 DashScope 接口支持自定义 Function Calling 与 MCP 工具集成。
- **结构化输出**：Anthropic 兼容接口通过 `output_config.format.type = "json_schema"` 提供强约束 JSON 输出能力，[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 中有详细说明。
- **音频支持**：Qwen-Audio 仅支持 DashScope 原生协议，不兼容 OpenAI 格式 —— 此限制在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 中明确指出。

> **注意**：文档 1（OpenAI兼容-Chat）与文档 8（DashScope API 参考）对 `max_frames` 参数的支持描述存在矛盾。文档 1 未提及该参数，而文档 8 明确说明“使用 OpenAI 兼容API调用时，不支持自定义`max_frames`参数”，且给出了具体取值范围。应以文档 8 的说明为准。

## 关键参数

各接口共性参数与关键差异如下：

| 参数 | OpenAI Chat | OpenAI Responses | Anthropic Messages | DashScope |
|------|-------------|------------------|---------------------|-----------|
| **`model`** | 必选，支持 Qwen、DeepSeek、Kimi、GLM、MiniMax 等多厂商模型（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)） | 必选，但仅列出 Qwen 及部分 DeepSeek/GLM/Kimi 商业版型号（如 `qwen3.8-max`, `deepseek-v4-pro`），第三方模型 Agent 能力受限 | 必选，支持更细粒度型号（含 `-latest` 后缀如 `qwen-plus-latest`）及更多第三方模型（如 `kimi-k2.7-code`, `MiniMax-M2.5`） | 必选，表述为“Qwen 大语言模型（商业版、开源版）、Qwen-VL、Qwen-Coder、千问Audio……”（见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)） |
| **`temperature`** | 取值范围 `[0, 2)` | 同左 | 取值范围 `[0, 2)`，**明确标注与 Anthropic 官方 `[0.0, 1.0]` 不同** | 未显式声明范围，但 SDK 行为与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)一致 |
| **`max_tokens`** | 不支持（由 `max_completion_tokens` 控制） | 不支持（由 `max_completion_tokens` 或 `reasoning.effort` 隐式控制） | 必选，语义因模型而异：对 `qwen3.8-max` 是回复+思考总长；对多数模型仅限回复长度（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)） | 不支持（由 `max_output_tokens` 控制） |
| **`system` / `messages[].role=system`** | 支持，但 QwQ 不建议、QVQ 不生效 | 支持 `instructions` 字段替代系统提示 | 支持独立 `system` 字段（字符串或数组） | 支持 `messages` 中 `role=system` 对象 |

其他重要参数：
- **图像/视频分辨率控制**：`min_pixels`、`max_pixels`、`total_pixels` 在 OpenAI Chat、Anthropic Messages、DashScope 三类接口中均有定义，但默认值与取值范围存在细微差异（如 `Qwen2.5-VL` 的 `min_pixels` 默认值在文档 1 和文档 8 中均为 `3136`，一致）。
- **思考强度**：Responses API 使用 `reasoning.effort`（`low`/`medium`/`high`/`max`）；Anthropic Messages 使用 `output_config.effort`（映射规则因模型而异）；DashScope 使用 `top_p`/`temperature` 组合调控。
- **缓存控制**：`cache_control.type="ephemeral"` 在 OpenAI Chat 和 Anthropic Messages 中均支持，用于显式缓存断点。

## 使用方式

### 接入地址（Base URL）
所有接口均需替换 `{WorkspaceId}` 为实际业务空间 ID，并优先使用地域专属域名：

- **华北2（北京）**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- **中国香港**：`https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com`

> **注意**：文档 1、2、7、8 均强调“现有域名（如 `dashscope.aliyuncs.com`）仍可正常使用，但**建议迁移至新域名**以获得卓越性能和更高稳定性”。该建议在全部四篇文档中完全一致，无矛盾。

### 协议选择指南
- **快速迁移 OpenAI 应用**：使用 `/compatible-mode/v1/chat/completions`（Chat）或 `/compatible-mode/v1/responses`（Responses）。后者额外支持 `previous_response_id` 简化多轮对话、内置工具链和 Session 缓存。
- **需要深度思考与结构化输出**：优先选用 `/apps/anthropic/v1/messages`（Anthropic Messages），其 `output_config.effort` 和 `format.json_schema` 提供更精细控制。
- **最大兼容性与底层控制**：使用 DashScope 原生 `/api/v1/services/aigc/{text-generation|multimodal-generation}/generation`，支持 Qwen-Audio 等非 OpenAI 兼容模型。

### 认证与 SDK
- **认证**：统一使用百炼 API Key，通过 `Authorization: Bearer <key>` 或 `x-api-key` 请求头传递（Anthropic 接口明确支持双方式；OpenAI 接口示例均用 `Authorization`）。
- **SDK 配置**：
  - OpenAI SDK：设置 `base_url`（如文档 1、2 所示）。
  - Anthropic SDK：设置 `base_url`（如文档 7 所示）。
  - DashScope SDK：设置 `base_http_api_url`（如文档 8 所示）。

## 限制和注意事项

- **地域可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站的华北2（北京）地域可用**，且需在百炼控制台手动开通服务（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **协议能力边界**：
  - Qwen-Audio **不支持 OpenAI 兼容协议**，必须使用 DashScope 原生接口（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
  - OpenAI Responses API **不支持异步执行**（`background` 参数已废弃），仅同步调用（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **上下文管理**：
  - Responses API 的最大输入上下文约为模型窗口的 80%，超出部分自动截断（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
  - `previous_response_id` 有效期为 7 天，且仅当创建请求中 `store=true` 时生成的 ID 才可被检索或删除（见 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md) 和 [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)）。
- **弃用提示**：`thinking.budget_tokens` 参数在 Anthropic Messages 接口中已被标记为“**即将废弃**”，新接入应使用 `output_config.effort`（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。
- **错误处理**：所有 REST 接口均返回标准 HTTP 状态码与 JSON 错误体（如 `{"error": {"message": "...", "type": "InvalidParameter"}}`），客户端需统一解析 `error.message` 字段。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


