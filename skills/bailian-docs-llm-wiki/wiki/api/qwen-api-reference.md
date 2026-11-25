# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（Chat Completions 和 Responses）、Anthropic 兼容接口（Messages）以及原生 DashScope 接口。开发者可根据现有技术栈和功能需求选择合适协议，所有接口均支持多模态输入、显式缓存、工具调用等高级能力。

## 支持的模型/功能

Qwen 系列模型在各协议下均支持主流文本与多模态能力，但具体支持范围因协议而异：

- **OpenAI 兼容 Chat 接口**（`/chat/completions`）支持 `qwen4-max`、`qwen3.8-*`、`qwen3.7-*`、`qwen3.6-*`、`qwen3.5-*`、`qwen-vl`、`qwen-omni`、`qwen-coder`、`qwen-math` 等，但明确**不支持 Qwen-Audio 的 OpenAI 兼容协议**，仅支持 DashScope 协议 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **OpenAI 兼容 Responses 接口**（`/responses`）专为复杂 Agent 场景设计，内置联网搜索、代码解释器、文搜图、知识库检索等工具，且支持 `previous_response_id` 多轮串联与自动 Session 缓存，是构建生产级对话 Agent 的推荐入口 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic 兼容 Messages 接口**（`/v1/messages`）支持 `qwen4-max`、`qwen3.7-plus`、`qwen3.8-flash` 等主流型号，并扩展了 `output_config.effort` 控制思考强度，但**不提供 `/v1/models` 列表接口**，客户端需自行维护模型白名单 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **DashScope 原生接口**（`/text-generation/generation` 或 `/multimodal-generation/generation`）是底层协议，支持全部模型（含 `qwen-audio`），且对多模态输入格式（如 `image`、`audio`、`video`）定义更细粒度，适用于需要完全控制请求体结构的场景。

> **注意**：文档 2 与文档 8 对 `qwen-audio` 的支持描述存在矛盾——文档 2 明确指出“Qwen-Audio 不支持 OpenAI 兼容协议”，而文档 8 在 DashScope 接口的模型列表中包含 `千问Audio`。该差异属实：`qwen-audio` 仅可通过 DashScope 原生接口调用，不可通过任何 OpenAI 兼容路径访问。

## 关键参数

| 参数 | 协议适用性 | 说明 |
|------|------------|------|
| `model` | 全协议必选 | OpenAI/Anthropic 接口要求模型名严格匹配（如 `qwen3.8-max`）；DashScope 接口同理，但部分旧版 SDK 可能接受别名。注意三方模型（如 `deepseek-v4.1-flash`）仅在特定地域开通后可用。 |
| `messages` / `input` | Chat & DashScope 使用 `messages`；Responses 使用 `input`（支持 string 或 array） | `messages` 数组中 `role` 仅支持 `user`/`assistant`/`system`；`input` 数组支持 `developer` 角色，用于调试注入。`system` 消息在 `qwen-omni` 和 `qwen-vl` 中可能被忽略。 |
| `max_tokens` | Chat & Anthropic 必选；DashScope 中为 `parameters.max_tokens` | Anthropic 协议下含义因模型而异：对 `qwen4-max` 和 `deepseek-v4.*` 表示「回复+思考」总长；对 `glm-5.2` 则需配合 `thinking.budget_tokens` 分离控制。 |
| `reasoning.effort` | 仅 Responses 接口 | 取值 `none`/`low`/`medium`/`high`，控制推理深度，影响 `output_tokens_details.reasoning_tokens` 计费。 |
| `x-dashscope-session-cache: enable` | 仅 Responses 接口 | 请求头启用服务端自动上下文缓存，无需修改业务逻辑即可降低多轮延迟。 |

## 使用方式

### 1. 基础配置
所有协议均需：
- 替换 `{WorkspaceId}` 为真实业务空间 ID（见控制台「业务空间详情」）；
- 使用百炼 API Key（非 DashScope 通用 Key），通过 `Authorization: Bearer <key>` 或对应 SDK 配置传入；
- **强烈建议迁移至业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

### 2. 协议选择指南
- 迁移 OpenAI 应用 → 优先用 `/chat/completions`（兼容性最高）或 `/responses`（需 Agent 能力）；
- 迁移 Anthropic 应用 → 用 `/v1/messages`，注意 `temperature` 范围为 `[0, 2)`（非 `[0.0, 1.0]`）；
- 需要音频/精细多模态控制/最大灵活性 → 用 DashScope 原生接口。

### 3. 多模态输入示例（统一规范）
- **图片**：`type: "image_url"` + `url`（HTTP URL 或 `data:image/...;base64,...`）；`detail` 参数控制精度（`high`/`low`/`auto`）；
- **视频**：`type: "video_url"` + `url`（支持 MP4/MOV 等），可选 `fps` 控制抽帧频率；
- **文件（PDF）**：仅 Responses 接口支持 `input_file` 类型，需公网 URL，最大 100 MB。

## 限制和注意事项

- **地域限制**：三方直供模型（如 SiliconFlow DeepSeek、MiniMax）**仅在中国站华北2（北京）地域可用**，调用前须在控制台开通对应服务。
- **上下文截断**：Responses 接口为预留工具调用空间，实际最大输入上下文约为模型窗口的 80%，超出部分自动截断且不报错。
- **Response ID 生命周期**：`/responses` 接口返回的 `resp_xxx` ID 仅在创建时设置 `store=true` 后才可被 `GET`、`DELETE` 或 `input_items` 查询；否则无法检索。
- **旧路径弃用**：OpenAI 兼容 Responses 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移到 `/compatible-mode/v1/responses`。
- **时间戳单位差异**：`/responses/{id}` 返回的 `created_at` 为秒级 Unix 时间戳；而 `/responses/{id}/input_items` 返回的 `created_at` 为毫秒级，使用时需注意单位转换。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


