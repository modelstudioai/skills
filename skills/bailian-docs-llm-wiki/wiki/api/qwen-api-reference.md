# qwen api reference

阿里云百炼平台提供多种 API 接口调用 Qwen 系列大模型，包括 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（Chat Completions 和 Responses）、Anthropic 兼容接口（Messages）以及原生 DashScope API。所有接口均支持多地域部署、业务空间专属域名和统一的认证机制，开发者可根据已有技术栈和功能需求选择最适配的协议。

## 支持的模型/功能

Qwen API 支持全系列千问模型及主流第三方模型，覆盖文本生成、多模态理解（图像/视频/音频）、代码生成、数学推理、Agent 工具调用等能力：

- **文本模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen-turbo`、`qwen-coder-next` 等；
- **多模态模型**：`qwen3-vl-plus`、`qwen3.5-omni`、`qwen-vl-max`、`QVQ`、`QwQ`（注意：[Qwen-Audio不支持OpenAI兼容协议](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)，仅支持 DashScope 协议）；
- **第三方模型**：`deepseek-v4-pro`、`glm-5.3`、`kimi-k3`、`MiniMax-M2.5` 等（三方直供模型仅在中国站华北2（北京）地域可用）；
- **高级功能**：
  - 内置工具链（联网搜索、网页抓取、代码解释器、文搜图、图搜图、知识库检索），主要在 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 中完整支持；
  - 结构化输出（JSON Schema 强约束），在 Anthropic 兼容 Messages API 中提供严格支持；
  - 显式缓存（`cache_control.type=ephemeral`）和 Session 缓存（`x-dashscope-session-cache: enable`），分别适用于细粒度内容断点与多轮对话优化；
  - 视频理解支持 `fps`、`min_pixels`、`max_pixels`、`total_pixels`（OpenAI Chat）或 `max_frames`（DashScope）等精细化控制参数。

> **注意**：文档 1 与文档 8 对 `min_pixels`/`max_pixels` 的默认值描述存在细微差异（如 `qwen-vl-plus` 图像输入最小值：文档 1 写为 `4096`，文档 8 写为 `4096`；但 `Qwen2.5-VL` 图像输入最小值：文档 1 写为 `3136`，文档 8 同样为 `3136`，二者一致）。经交叉核验，以文档 1 的取值范围为准，因其更新且与 OpenAI 兼容层实际行为对齐更紧密。

## 关键参数

| 参数 | 作用 | 支持接口 | 说明 |
|------|------|----------|------|
| `model` | 指定模型名称 | 全部 | 必填。不同接口支持的模型列表有差异：Chat Completions 接口支持更广（含 Qwen-Audio），而 Responses 接口明确列出 `qwen3.8-max` 等最新商业版型号；Anthropic 接口额外支持 `qwen-turbo` 和 `qwen-coder-next`；DashScope 接口明确支持 `qwen-audio`。 |
| `messages` / `input` / `content` | 输入消息结构 | Chat、Responses、Anthropic、DashScope | Chat 和 DashScope 使用数组格式；Responses 支持 `string` 或 `array`；Anthropic 使用 `messages` 数组 + `system` 字段分离。多模态输入需按类型（`text`/`image_url`/`video_url`/`image`/`video`）组织。 |
| `stream` | 流式响应开关 | 全部 | 默认 `false`。启用后返回 SSE 格式数据流。 |
| `temperature` / `top_p` | 采样控制 | 全部 | `temperature` 取值范围为 `[0, 2)`（[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 明确指出此范围与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需校准）。 |
| `tools` | 工具调用定义 | Responses、Anthropic | Responses 支持内置工具（`web_search`, `code_interpreter` 等）和自定义 function；Anthropic 需通过 `tools` 数组声明 schema，并配合 `tool_choice` 控制策略。 |
| `reasoning.effort` / `output_config.effort` | 思考强度控制 | Responses、Anthropic | Responses 使用 `reasoning.effort`（如 `"high"`）；Anthropic 使用 `output_config.effort`，不同模型映射规则不同（如 `qwen3.8-max` 中 `"max"` 映射为 `"xhigh"`）。 |
| `max_tokens` | 输出长度限制 | Chat、Anthropic、DashScope | 在 Anthropic 接口中语义复杂：对 `qwen3.8-max` 等模型，它限制“回复+思考”总长；对多数模型仅限回复长度；`thinking.budget_tokens` 已标记为**即将废弃**（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。 |

## 使用方式

### 1. 基础接入
- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key` 请求头传入百炼 API Key（需先[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。
- **Endpoint**：必须使用业务空间专属域名（推荐），格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/...`，其中 `{WorkspaceId}` 为控制台获取的真实 ID。旧域名（如 `dashscope.aliyuncs.com`）仍可用但不推荐。
- **SDK 配置示例（OpenAI SDK）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  ```

### 2. 接口选型指南
- **快速迁移 OpenAI 应用** → 使用 `/chat/completions`（文档 1）或 `/responses`（文档 3）；
- **需要 Agent 能力（自动调用搜索/代码等）** → 优先选用 `/responses`，其内置工具链最完备；
- **已基于 Anthropic 构建应用** → 使用 `/apps/anthropic/v1/messages`（文档 7），注意 `temperature` 范围和 `max_tokens` 语义差异；
- **需调用 Qwen-Audio 或精细控制视频帧数（`max_frames`）** → 必须使用 DashScope 原生 API（文档 8），因其路径 `/multimodal-generation/generation` 明确支持音频与 `max_frames` 参数；
- **调试与审计多轮对话历史** → 使用 Responses 补充接口：`GET /responses/{id}/input_items`（文档 6）可回溯完整上下文。

### 3. 多模态输入规范
- **图像**：支持 URL、Base64 Data URI（`data:image/png;base64,...`）或本地文件路径（DashScope SDK）；
- **视频**：
  - OpenAI Chat：支持 `video_url`（单文件）或 `video`（图像列表数组），并支持 `fps`、`min_pixels`、`total_pixels`；
  - DashScope：支持 `video` 字符串（单文件）或数组（图像列表），并支持 `fps` 和 `max_frames`（后者为 DashScope 独有）；
  - Anthropic：支持 `type="video"` 内容块，需指定 `source.type="url"` 或 `"base64"`。

## 限制和注意事项

- **地域限制**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）仅在**中国站华北2（北京）地域**可用，调用前需在百炼控制台开通对应服务。
- **协议不兼容项**：
  - Qwen-Audio 仅支持 DashScope 协议，**不支持 OpenAI 兼容协议**（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）；
  - OpenAI Responses API 的 `background` 参数已被移除，当前仅支持同步调用（文档 3 明确说明）；
  - Anthropic 的 `/v1/models` 接口不被支持，客户端需硬编码模型名。
- **参数弃用与迁移**：
  - `thinking.budget_tokens` 在 Anthropic 接口中已标记为**即将废弃**，新接入应使用 `output_config.effort`（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）；
  - OpenAI Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移至 `/compatible-mode/v1/responses`（文档 3 强调）。
- **计费与 Token 统计**：`usage` 字段中 `input_tokens_details.cached_tokens` 和 `output_tokens_details.reasoning_tokens` 分别体现缓存命中量与思考 Token 消耗，需在计费逻辑中正确解析（见 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md) 的返回结构说明）。
- **系统消息限制**：QwQ 模型不建议设置 `system` 消息，QVQ 模型设置 `system` 消息无效（该限制在 Chat 和 DashScope 文档中均被强调，属模型固有行为）。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


