# qwen api reference

阿里云百炼平台提供多种 API 接口调用 Qwen 系列大模型，包括 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（Chat Completions、Responses）、Anthropic 兼容接口（Messages）以及原生 DashScope API。所有接口均支持多地域部署、显式缓存、多模态输入（图像/视频/音频）及高级推理能力（如工具调用、深度思考），开发者可根据技术栈和功能需求选择最适配的协议。

## 支持的模型/功能

Qwen API 支持全系列千问模型及主流第三方模型，覆盖文本生成、多模态理解、代码生成、数学推理、语音处理等场景：

- **Qwen 系列**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen3-vl-plus`、`qwen3-coder-next`、`qwen3.5-ocr`、`qwen-audio`（仅 DashScope 协议支持，见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）；
- **多模态模型**：`Qwen-VL`、`QVQ`、`Qwen-Omni`（视频理解需注意 `fps` 和 `total_pixels` 参数约束，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）；
- **第三方模型**：`deepseek-v4-pro`、`glm-5.2`、`kimi-k3`、`MiniMax-M2.5` 等（部分仅限华北2地域且需控制台开通，见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。

> **注意**：Qwen-Audio 明确不支持 OpenAI 兼容协议，仅可通过 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 调用；QwQ 模型不建议设置 system message，QVQ 模型的 system message 无效——该限制在 OpenAI 兼容与 DashScope 两套文档中一致，但 Anthropic 兼容文档未提及，实际行为以运行时为准。

## 关键参数

| 参数 | 类型 | 说明 | 适用接口 |
|------|------|------|----------|
| `model` | `string` | 必填，模型 ID。不同接口支持列表有差异：OpenAI Chat 支持 `Qwen-Audio`（不生效）、`Qwen-VL` 等；Responses API 明确列出 `qwen3.8-max` 等 30+ 专属型号；Anthropic Messages 支持 `qwen3.7-plus` 等并区分 Max/Plus/Flash 子系列；DashScope 则统一支持 `qwen-plus`、`qwen3-vl-plus` 等。 | 全部 |
| `messages` / `input` | `array` / `string` | 对话上下文。OpenAI Chat 和 DashScope 使用 `messages` 数组；Responses API 同时支持纯字符串 `input` 和结构化 `array`；Anthropic Messages 使用 `messages` + `system` 字段分离提示词。 | Chat、DashScope、Anthropic、Responses |
| `stream` | `boolean` | 是否流式响应，默认 `false`。所有接口均支持，但 Responses API 的 `store=false` 时流式响应不可被后续 `previous_response_id` 引用。 | 全部 |
| `tools` | `array` | 内置工具（`web_search`, `code_interpreter` 等）或自定义 function 工具。仅 Responses API 和 Anthropic Messages 支持完整工具链（含 `tool_result` 回传）；OpenAI Chat 不支持工具调用。 | Responses、Anthropic |
| `max_tokens` | `integer` | 输出长度上限。Anthropic Messages 中对 `deepseek-v4-pro` 和 `qwen3.8-max` 等模型含义为「回复+思考」总和；而 DashScope 和 OpenAI Chat 中仅为回复长度。 | Anthropic、DashScope、Chat |
| `fps`, `min_pixels`, `max_pixels`, `total_pixels` | `float`/`integer` | 视频/图像预处理参数。`fps` 控制抽帧频率与时间建模；`min/max_pixels` 控制单帧缩放；`total_pixels` 限制整段视频总像素（影响 token 消耗）。仅 OpenAI Chat 和 DashScope 支持，Anthropic Messages 未定义 `total_pixels`。 | Chat、DashScope |

## 使用方式

### 1. 基础接入
所有接口均需：
- 替换 `{WorkspaceId}` 为真实业务空间 ID（见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；
- 使用业务空间专属域名（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`（如华北2为 `cn-beijing`），替代旧版 `dashscope.aliyuncs.com`；
- 通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key`（Anthropic）传入认证凭据。

### 2. 接口选型指南
- **快速迁移 OpenAI 应用**：优先使用 `/compatible-mode/v1/chat/completions`（标准对话）或 `/compatible-mode/v1/responses`（增强对话，含工具、自动上下文管理）；
- **需要深度思考/结构化输出**：选用 Anthropic Messages 接口（`/apps/anthropic/v1/messages`），利用 `thinking.type` 和 `output_config.effort` 精细控制推理强度；
- **复杂多模态或低层控制**：使用 DashScope 原生 API（`/api/v1/services/aigc/multimodal-generation/generation`），支持 `video`、`image`、`audio` 字段直传及 `max_frames` 等底层参数；
- **管理历史对话**：Responses API 提供 `previous_response_id`（单轮引用）和 `conversation`（会话级管理），配合 `/responses/{id}/input_items` 查询完整输入历史。

### 3. 多模态输入示例（统一规范）
- 图像：`{"type": "image_url", "image_url": {"url": "https://xxx.jpg"}}`（OpenAI Chat）或 `{"image": "https://xxx.jpg"}`（DashScope）；
- 视频文件：`{"type": "video_url", "video_url": {"url": "https://xxx.mp4", "fps": 2}}`（OpenAI Chat）或 `{"video": "https://xxx.mp4", "fps": 2}`（DashScope）；
- 视频帧列表：`{"type": "video", "video": ["https://1.jpg", "https://2.jpg"], "fps": 2}`。

## 限制和注意事项

- **地域限制**：三方直供模型（如 SiliconFlow DeepSeek）仅在中国站华北2（北京）地域可用，调用前须在百炼控制台开通服务（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）；
- **协议差异**：OpenAI Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用，必须迁移到 `/compatible-mode/v1/responses`（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）；
- **参数兼容性**：Anthropic Messages 的 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需校准（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）；
- **缓存与计费**：显式缓存（`cache_control: {type: "ephemeral"}`）在 OpenAI Chat 和 Anthropic Messages 中均有效，但 DashScope API 使用独立的 `enable_cache` 参数；`cached_tokens` 计入 `usage.input_tokens_details`，影响计费；
- **视频处理边界**：`total_pixels` 是 Qwen-VL/QVQ 系列的关键限制，超限将触发帧缩放。其默认值因模型而异（如 `qwen3.8` 为 `819200000`，`qwen3-vl-235b` 为 `134217728`），务必按实际视频时长和分辨率预估（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）；
- **工具调用约束**：Responses API 的 `file_search` 工具当前仅支持传入**一个**知识库 ID（`vector_store_ids` 为单元素数组），多知识库检索需分步调用（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


