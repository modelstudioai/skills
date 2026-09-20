# qwen api reference

阿里云百炼平台提供多种兼容标准协议的 Qwen 模型调用方式，包括 OpenAI 兼容 Chat 和 Responses API、Anthropic 兼容 Messages API，以及原生 DashScope API。所有接口均支持多地域部署与业务空间专属域名，推荐使用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com` 格式 endpoint 以获得更优性能和稳定性。开发者需先[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，并根据所选协议安装对应 SDK（如 OpenAI Python SDK 或 Anthropic SDK）。

## 支持的模型/功能

Qwen 系列模型（含 `qwen3.8-*`、`qwen3.7-*`、`qwen3.6-*`、`qwen3.5-*`、`qwen-plus`、`qwen-flash`、`qwen-turbo`、`qwen-coder-*`、`qwen-vl-*`、`qwen-omni-*`）是核心支持对象，同时兼容部分第三方模型（如 DeepSeek、Kimi、GLM、MiniMax），但功能支持程度因模型类型和接入协议而异：

- **OpenAI 兼容 Chat API**（[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）支持 Qwen 大语言模型、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math 等，但明确不支持 Qwen-Audio（仅 DashScope 协议支持）。
- **OpenAI 兼容 Responses API**（[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）提供增强能力：内置工具链（联网搜索、网页抽取、代码解释器、文搜图、知识库搜索等）、`previous_response_id` 多轮上下文管理、Session 缓存（通过 `x-dashscope-session-cache: enable` 启用）及结构化输出支持。
- **Anthropic 兼容 Messages API**（[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）支持 `output_config.effort` 控制推理强度、`format.json_schema` 结构化输出（严格模式适用于 qwen3.8/3.7/DeepSeek/GLM 系列），并支持显式缓存断点（`cache_control: {type: "ephemeral"}`）。
- **DashScope 原生 API**（[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）为最底层协议，区分文本生成（`/text-generation/generation`）与多模态生成（`/multimodal-generation/generation`）端点，支持 `max_frames` 等细粒度视频参数，但 OpenAI 兼容 API 不支持该参数。

> **注意**：文档 1 与文档 8 对 `min_pixels`/`max_pixels` 的默认值描述存在细微差异（如 `qwen-vl-plus` 图像输入默认值，文档 1 写为 `4096`，文档 8 写为 `4096`；但 `Qwen2.5-VL` 视频输入默认值，文档 1 写为 `50176`，文档 8 写为 `50176` —— 实际一致）。经交叉核对，两处数值无实质性矛盾，属表述口径差异，以最新发布模型规格为准。

## 关键参数

| 参数 | 协议支持 | 说明 | 示例/范围 |
|------|----------|------|-----------|
| `model` | 全部 | 必填，模型 ID。Responses API 支持列表最全（含 `qwen3.8-omni-flash` 等新模型），Chat API 列表较宽泛（含三方模型），DashScope 与 Anthropic 列表居中。 | `"qwen3.8-max"`, `"qwen3.8-omni-flash"` |
| `messages` / `input` | Chat/Responses/DashScope | 对话消息数组（Chat/DashScope）或字符串/数组混合输入（Responses）。Responses 支持 `previous_response_id` 自动拼接历史。 | `[{"role":"user","content":"你好"}]` |
| `system` | Chat/Anthropic/DashScope | 系统指令。Anthropic 支持字符串或带 `cache_control` 的数组；Chat 中 QwQ 不建议设置，QVQ 无效。 | `"你是一个专业助手"` |
| `stream` | 全部 | 是否流式响应。Responses API 流式事件格式为 `response.output_text.delta`。 | `true` |
| `temperature` | 全部 | 采样温度。**Anthropic 协议取值范围为 [0, 2)，与官方 [0.0, 1.0] 不同**，迁移时需校验。 | `0.8` |
| `max_tokens` | Anthropic/Responses | Anthropic 中含义依模型而异（如 qwen3.8-max 限制回复+思考总长）；Responses 中该参数未定义，由 `max_output_tokens`（非文档提及）或模型自身窗口隐式约束。 | `2048` |
| `vl_high_resolution_images` | DashScope/Chat | 布尔值，启用后 `max_pixels` 失效，图像最大像素固定为 `16777216`（Qwen3 系列）或 `12845056`（Qwen2.5-VL/QVQ）。 | `true` |
| `fps` / `max_frames` | Chat/DashScope | 视频抽帧参数。`fps` 控制频率（[0.1,10]），`max_frames` 限制总数（DashScope 支持，OpenAI 兼容 API 不支持）。 | `fps: 2.0`, `max_frames: 2000` |

## 使用方式

### 终端地址（Endpoint）
所有协议均按地域提供专属域名，**必须替换 `{WorkspaceId}` 为真实业务空间 ID**：
- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- 中国香港：`https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com`
- 其他地域（美东、德法兰克福、日东京）同理。

> **注意**：文档 1、4、7、8 均强调应从旧域名（如 `dashscope.aliyuncs.com`）迁移至上述业务空间专属域名，因其“提供卓越的性能和更高的稳定性”。旧域名虽仍可用，但非长期推荐路径。

### 协议选择指南
- **快速迁移 OpenAI 应用**：优先选用 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)（简单对话）或 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)（需工具、多轮、缓存）。
- **需要深度思考控制或结构化 JSON 输出**：选用 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)，利用 `output_config.effort` 和 `format.json_schema`。
- **需精细控制视频帧数或使用千问Audio等特殊模型**：必须使用 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)，因其支持 `max_frames` 和 `audio` 字段。

### 认证与 SDK
- 认证：统一使用百炼 API Key，通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key`（Anthropic 协议）头传递。
- SDK：OpenAI 协议用 `openai` 包，Anthropic 协议用 `anthropic` 包，DashScope 协议用 `dashscope` 包。各协议 SDK 初始化时均需显式设置 `base_url`（见各文档示例）。

## 限制和注意事项

- **地域可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在百炼控制台手动开通服务（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **协议差异**：OpenAI Responses API **不支持 `background` 异步参数**（当前仅同步），且会忽略任何未在文档中明确列出的 OpenAI 参数（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **缓存与计费**：Session 缓存（`x-dashscope-session-cache`）和显式缓存（`cache_control: {type: "ephemeral"}`）均影响 Token 计费，命中缓存的 Token 在 `usage.input_tokens_details.cached_tokens` 中体现。
- **响应存储与生命周期**：`store=true` 的 Responses 才可被 `retrieve`、`delete` 或作为 `previous_response_id` 引用，且 `previous_response_id` 有效期为 **7 天**（见 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)）。
- **视频处理限制**：`total_pixels`（视频总像素上限）在 Chat API 文档中定义详尽，但 Responses API 文档未提及此参数，实际调用时以 Chat API 行为为准；`max_frames` 仅 DashScope API 支持，OpenAI 兼容 API 会自动应用模型默认值。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


