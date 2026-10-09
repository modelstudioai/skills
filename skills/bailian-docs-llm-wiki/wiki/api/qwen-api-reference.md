# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容 Chat/Responses、Anthropic 兼容 Messages 和原生 DashScope 协议。开发者可根据现有技术栈选择适配路径，所有接口均支持多模态输入（文本、图像、音频、视频）与结构化输出能力，并统一通过业务空间专属域名接入。

## 支持的模型/功能

Qwen 系列模型覆盖全场景需求：  
- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen-turbo`、`qwen-coder-next` 等；  
- **多模态理解**：`qwen3.8-omni-flash`（音视频端到端）、`qwen3-vl-plus`、`qwen-vl-max`、`QVQ`；  
- **数学与代码**：`qwen-math`、`qwen3-coder-plus`；  
- **第三方直供模型**：`deepseek-v4-pro`、`glm-5.3`、`kimi-k3`、`MiniMax-M2.5`（仅限华北2北京地域，需在控制台开通）[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。  

核心功能包括：  
- 内置工具链（联网搜索、网页抓取、代码解释器、文搜图、知识库检索）；  
- 多轮对话管理（通过 `previous_response_id` 或 `conversation`）；  
- 显式缓存与 Session 缓存（降低重复请求延迟）；  
- 结构化 JSON 输出（支持强约束 Schema 验证）；  
- 视频理解（抽帧控制 `fps`、总像素限制 `total_pixels`、帧数上限 `max_frames`）。  

> **注意**：Qwen-Audio 不支持 OpenAI 兼容协议，仅可通过 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 调用；QwQ 模型不建议设置 `system` 消息，QVQ 模型中 `system` 消息无效。

## 关键参数

| 参数 | 说明 | 适用协议 | 示例值 |
|------|------|----------|--------|
| `model` | 必选，模型 ID | 全部 | `"qwen3.8-max"`、`"qwen3.8-omni-flash"` |
| `messages` / `input` | 对话上下文（数组）或纯文本（字符串） | OpenAI Chat / Responses | `[{"role":"user","content":"你好"}]` |
| `stream` | 是否流式响应 | 全部 | `true` |
| `temperature` | 采样温度，取值范围 `[0, 2)` | OpenAI、Anthropic、DashScope | `0.8`（Anthropic 官方为 `[0.0, 1.0]`，迁移时需校准）[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) |
| `max_tokens` | 输出最大 token 数（行为因模型而异） | Anthropic、DashScope | `2048`（`glm-5.3` 下含思考链；`qwen-plus` 下仅限回复） |
| `fps` | 视频抽帧频率（Hz），影响时间动态理解 | OpenAI Chat、DashScope | `2.0`（范围 `[0.1, 10]`） |
| `min_pixels` / `max_pixels` | 图像/视频帧像素缩放阈值 | OpenAI Chat、DashScope | `min_pixels=65536`, `max_pixels=2621440` |
| `total_pixels` | 视频总像素上限（单帧×帧数） | OpenAI Chat（仅部分模型） | `819200000`（对应 80 万图像 token） |
| `reasoning.effort` / `output_config.effort` | 思考强度控制（`xhigh`/`high`/`low`） | OpenAI Responses、Anthropic | `"xhigh"`（`qwen3.8-max` 默认） |

> **注意**：`thinking.budget_tokens` 已标记为**即将废弃**，新接入应使用 `output_config.effort` 或 `reasoning.effort` [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

## 使用方式

### 接入地址（统一模式）
所有协议均使用业务空间专属域名（推荐），格式为：  
`https://{WorkspaceId}.{region}.maas.aliyuncs.com/{path}`  
其中 `{WorkspaceId}` 为控制台「业务空间详情」中获取的真实 ID，`{region}` 如 `cn-beijing`、`ap-southeast-1` 等。

| 协议 | 路径 | 示例（北京） |
|------|------|--------------|
| OpenAI Chat | `/compatible-mode/v1/chat/completions` | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions` |
| OpenAI Responses | `/compatible-mode/v1/responses` | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses` |
| Anthropic Messages | `/apps/anthropic/v1/messages` | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages` |
| DashScope 原生 | `/api/v1/services/aigc/{text-generation\|multimodal-generation}/generation` | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` |

### 认证与 SDK
- **API Key**：通过环境变量 `DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer <key>` 传入；  
- **SDK 配置**：OpenAI SDK 设置 `base_url`；DashScope SDK 设置 `base_http_api_url`；Anthropic SDK 设置 `base_url` [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)；  
- **旧域名已弃用**：`dashscope.aliyuncs.com`（国内）和 `dashscope-intl.aliyuncs.com`（国际）仍可用，但性能与稳定性低于新域名，强烈建议迁移。

## 限制和注意事项

- **地域限制**：第三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在百炼控制台手动开通服务；  
- **参数兼容性**：OpenAI Responses API **不支持 `background` 异步参数**，仅同步调用；未文档化的 OpenAI 参数将被忽略；  
- **上下文长度**：Responses API 为内置工具预留约 20% 上下文空间，实际可用输入长度约为模型窗口的 80%，超长内容将自动截断而不报错；  
- **缓存行为**：`x-dashscope-session-cache: enable` 仅对 Responses API 生效；显式缓存（`cache_control: {type: "ephemeral"}`）需在 Anthropic Messages 或 OpenAI Chat 的 `content` 数组中显式声明；  
- **视频处理差异**：`max_frames` 仅 DashScope API 支持自定义，OpenAI 兼容 API 固定使用模型默认值；`total_pixels` 仅 OpenAI Chat 支持，DashScope 使用 `max_frames` + `max_pixels` 组合控制；  
- **响应存储**：`store=true` 是使用 `previous_response_id`、`GET /responses/{id}` 和 `GET /responses/{id}/input_items` 的前提条件，`store=false` 的响应不可检索或复用。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


