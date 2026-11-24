# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 qwen4-max、qwen3.8-plus、qwen3-vl-plus 等）及部分第三方模型。核心能力覆盖文本生成、多模态理解（图像/视频/音频/PDF）、工具调用、深度思考与显式缓存等。

## 支持的模型/功能

Qwen API 支持三类主要调用协议，对应不同功能侧重：

- **OpenAI 兼容 Chat API**：适用于标准对话场景，支持 `chat/completions` 端点，兼容 `messages` 数组输入，适用于绝大多数 LLM 应用迁移。支持模型包括 `qwen4-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3-vl-plus`、`qwen3.8-omni-flash` 及部分第三方模型（如 `deepseek-v4.1-flash`、`kimi-k3.1-pro`）。注意：Qwen-Audio **不支持** OpenAI 兼容协议，仅支持 DashScope 协议 [qwen-api-via-dashscope.md](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

- **OpenAI 兼容 Responses API**：面向复杂 Agent 场景设计，内置联网搜索、代码解释器、文搜图、知识库检索等工具链，支持 `previous_response_id` 简化多轮上下文管理，并提供 `x-dashscope-session-cache: enable` 自动会话缓存。该 API 专为提升 Agent 效能优化，详细参数见 [qwen-api-via-openai-responses.md](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。

- **Anthropic 兼容 Messages API**：适用于已使用 Anthropic SDK 的用户，支持 `system` 提示、`tool_use`/`tool_result` 结构化工具交互、`thinking` 深度推理块及 `cache_control` 显式缓存断点。`temperature` 范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需校准 [anthropic-api-messages.md](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

- **DashScope 原生 API**：提供最底层控制能力，区分 `text-generation` 和 `multimodal-generation` 服务端点，支持 `qwen-audio`、`qwen-math` 等专属模型，以及 `max_frames` 等细粒度视频参数。是调用音频、数学或需精确控制输入格式场景的首选。

> **注意**：文档 2 与文档 8 在 `detail` 参数位置描述存在不一致——文档 2（OpenAI Chat）指出 `detail` 可置于 `image_url` 内部或同级；文档 8（DashScope）明确要求 `detail` 与 `image` 同级。实际行为以 DashScope 协议为准，OpenAI 兼容层为兼容性做了一定适配，但建议在 DashScope 调用中严格遵循 `{"image":"...", "detail":"high"}` 格式。

## 关键参数

| 参数 | 协议适用性 | 说明 |
|--------|-------------|------|
| `model` | 全部 | 必填。模型 ID 需从[百炼控制台模型市场](https://bailian.console.aliyun.com/model/market)获取。OpenAI Chat 与 Responses API 支持列表略有差异（如 Responses 明确列出 `qwen3.8-omni-flash`，而 Chat 文档未单列），以各接口文档所列为准。 |
| `messages` / `input` / `system` | 分别对应 Chat / Responses / Anthropic | 输入结构不同：Chat 与 Anthropic 使用 `messages` 数组；Responses 支持 `string` 或 `array`（含 `EasyInputMessage`）；Anthropic 支持顶层 `system` 字符串或数组。 |
| `max_tokens` | Anthropic、DashScope | Anthropic 协议中，`max_tokens` 含义因模型而异（如 `qwen4-max` 包含思考 [Token](../concepts/token.md)，`glm-5.2` 则可分离控制）；DashScope 中该参数不存在，由 `max_output_tokens` 控制（见其文档）。 |
| `detail`, `min_pixels`, `max_pixels`, `fps` | OpenAI Chat、DashScope | 多模态精度控制参数。`detail` 默认 `high`；`min_pixels`/`max_pixels` 用于缩放图像/视频帧；`fps` 控制视频抽帧频率。DashScope 还额外支持 `max_frames`，而 OpenAI 兼容 API 不支持此参数 [qwen-api-via-dashscope.md](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。 |
| `reasoning.effort` / `thinking.type` | Responses / Anthropic | 控制深度思考强度。Responses 使用 `reasoning.effort`（如 `"high"`），Anthropic 使用 `thinking.type: "enabled"` + `budget_tokens`（即将废弃）或 `effort`。 |
| `store`, `previous_response_id` | Responses API 专属 | `store=true` 后返回的 `response_id` 才可用于后续 `GET /responses/{id}` 或 `GET /responses/{id}/input_items` 查询，是实现可追溯多轮对话的基础 [retrieve-a-response.md](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)。 |

## 使用方式

### 1. 基础配置
所有协议均需：
- 替换 `{WorkspaceId}` 为真实业务空间 ID（控制台「业务空间详情」页获取）；
- 使用百炼 API Key（非 DashScope 旧 Key），通过 `Authorization: Bearer <key>` 或 `x-api-key`（Anthropic）传入；
- **强烈建议迁移至业务空间专属域名**：华北2（北京）用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。

### 2. 协议端点速查
| 协议 | 端点（华北2 示例） | SDK `base_url` / `region` |
|------|---------------------|----------------------------|
| OpenAI Chat | `POST /compatible-mode/v1/chat/completions` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| OpenAI Responses | `POST /compatible-mode/v1/responses` | 同上 |
| Anthropic Messages | `POST /apps/anthropic/v1/messages` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| DashScope Text | `POST /api/v1/services/aigc/text-generation/generation` | `workspace="{WorkspaceId}", region="cn-beijing"` |
| DashScope Multimodal | `POST /api/v1/services/aigc/multimodal-generation/generation` | 同上 |

### 3. 核心操作链（Responses API 示例）
1. `POST /responses` 提交请求，设 `store=true` → 获取 `response_id`；
2. `GET /responses/{response_id}` 查询最终结果；
3. `GET /responses/{response_id}/input_items` 查看完整输入历史（含多轮串联）；
4. `DELETE /responses/{response_id}` 清理已存储响应（仅限 `store=true` 创建的）。

## 限制和注意事项

- **地域与模型可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在百炼控制台单独开通服务 [qwen-api-via-openai-chat-completions.md](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **上下文截断**：Responses API 为预留工具调用空间，实际最大输入上下文约为模型窗口的 80%，超出部分自动截断且不报错，需自行监控 `usage.input_tokens`。
- **音频/视频支持差异**：Qwen-Audio 仅 DashScope 协议支持；Qwen-Omni 视频理解能力（含音频）强于 Qwen-VL（仅视觉）；`input_audio` 在 Responses API 中仅限 `qwen3.8-omni-flash` 模型。
- **缓存行为**：Session 缓存（`x-dashscope-session-cache`）对 Responses API 透明生效；显式缓存（`prompt_cache_breakpoint` 或 `cache_control`）需模型支持（如 `qwen4-max`），且 `ttl` 仅在 Qwen4 中有效。
- **废弃参数**：`thinking.budget_tokens`（Anthropic 协议）已被标记为“即将废弃”，新接入应使用 `output_config.effort` 或 `thinking.effort`（Responses）替代。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


