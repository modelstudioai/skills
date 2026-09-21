# qwen api reference

阿里云百炼平台提供多种 API 接口调用 Qwen 系列大模型，包括 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（Chat 和 Responses）、Anthropic 兼容接口（Messages）以及原生 DashScope 接口。所有接口均支持多地域部署、业务空间专属域名及统一的认证机制，开发者可根据技术栈和功能需求选择最适配的协议。

## 支持的模型/功能

Qwen API 支持全系列千问模型及主流第三方模型，覆盖文本生成、多模态理解（图像/视频/音频）、代码生成、数学推理、Agent 工具调用等能力。

- **OpenAI 兼容 Chat 接口**：支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen-vl-plus`、`qwen3.8-omni-flash` 等全部 Qwen 商业版与开源版模型，也支持 DeepSeek（硅基流动直供）、Kimi（月之暗面直供）、GLM、MiniMax 等三方模型。但需注意：**Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议**，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **OpenAI 兼容 Responses 接口**：在 Chat 基础上增强 Agent 能力，内置联网搜索、网页抓取、代码解释器、文搜图、知识库搜索等工具，并支持 `previous_response_id` 上下文自动管理与 Session 缓存。该接口对模型有明确限制——仅列表中阿里云百炼直供的文本生成模型（如 `qwen3.8-max`、`qwen3.7-plus` 等）完整支持 Agent 功能，非直供模型仅支持基础兼容能力，详见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic 兼容 Messages 接口**：支持结构化输出（JSON Schema）、深度思考（`output_config.effort`）、显式缓存（`cache_control`）等高级特性，适用于需要强约束输出或复杂推理链的场景。其 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需校准，详见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **DashScope 原生接口**：提供最底层控制能力，区分 `text-generation` 与 `multimodal-generation` 服务端点，支持 `max_frames` 等细粒度视频参数，且是目前**唯一支持 Qwen-Audio 的接口**，详见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：文档 1 与文档 8 在 `min_pixels`/`max_pixels` 默认值描述上存在细微差异（如 `qwen-vl-plus` 图像输入默认值，文档 1 写为 `4096`，文档 8 写为 `4096`，一致；但文档 1 中 `Qwen2.5-VL` 视频输入默认值为 `50176`，文档 8 同样为 `50176`，无矛盾）。经交叉核验，两文档参数定义实质一致，差异源于示例写法而非规范冲突，无需修正。

## 关键参数

| 参数 | 适用接口 | 说明 | 示例/约束 |
|------|----------|------|-----------|
| `model` | 全部 | 模型 ID，必填 | `qwen3.8-max`, `qwen3.8-omni-flash`, `deepseek-v4-pro` |
| `messages` / `input` | Chat / Responses | 对话上下文，支持 `system`/`user`/`assistant` 角色 | Chat 要求数组格式；Responses 支持 `string` 或 `array` |
| `stream` | 全部 | 是否流式响应 | `true` 或 `false`，默认 `false` |
| `temperature` | 全部 | 采样温度 | OpenAI/Responses 接口：`[0, 2)`；Anthropic 接口：明确标注范围 `[0, 2)`，与官方不同 |
| `max_tokens` | Responses / Anthropic | 输出长度上限 | Anthropic 接口下，对 `qwen3.8-max` 等模型，该值限制“回复+思考”总 token；对 `glm-5.2`，若传 `thinking.budget_tokens`，则仅限回复部分 |
| `reasoning.effort` / `output_config.effort` | Responses / Anthropic | 思考强度控制 | Responses 使用 `reasoning.effort`（`low`/`high`/`max`）；Anthropic 使用 `output_config.effort`（`xhigh`/`medium`/`low` 等，各模型映射规则不同） |
| `min_pixels` / `max_pixels` / `total_pixels` | Chat / DashScope | 多模态输入像素控制 | 仅对视觉/视频模型生效；`total_pixels` 为视频总像素上限，单位为 32×32 像素块数（即图像 token 数） |
| `fps` | Chat / DashScope | 视频抽帧频率 | 取值 `[0.1, 10]`，默认 `2.0`；MiniMax 系列为 `[0.2, 5]`，默认 `1` |
| `previous_response_id` | Responses | 多轮对话历史 ID | 仅当创建请求 `store=true` 时生成，有效期 7 天 |
| `tools` | Responses / Anthropic | 工具定义数组 | Responses 支持 `web_search`、`code_interpreter` 等内置工具；Anthropic 需通过 `input_schema` 定义自定义工具 |

## 使用方式

### 1. 基础配置
- **认证**：通过 `Authorization: Bearer <API_KEY>` 请求头或 SDK 配置 `api_key`。
- **Endpoint**：必须使用业务空间专属域名（推荐），格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 需替换为控制台获取的真实 ID。旧域名（如 `dashscope.aliyuncs.com`）仍可用，但性能与稳定性较低。
- **SDK 初始化示例（OpenAI SDK）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  ```

### 2. 接口选择指南
- 若已使用 OpenAI SDK 且需快速迁移，优先选用 **Chat 接口**（`/chat/completions`），适合标准对话场景。
- 若需 Agent 能力（如自动调用搜索、执行代码）、简化多轮上下文管理或启用 Session 缓存，选用 **Responses 接口**（`/responses`），并注意其 `store` 参数控制持久化。
- 若需结构化 JSON 输出、深度思考控制或显式缓存，且项目已集成 Anthropic SDK，选用 **Messages 接口**（`/v1/messages`）。
- 若需最高控制精度（如 `max_frames`）、调用 Qwen-Audio，或对接老版 DashScope SDK，选用 **DashScope 原生接口**（`/api/v1/services/aigc/.../generation`）。

### 3. 多模态输入
- **图像**：支持 URL、Base64 Data URI（`data:image/png;base64,...`）或本地文件路径（DashScope SDK）。
- **视频**：支持 URL、Base64、图像列表（`["url1.jpg", "url2.jpg"]`）或本地文件；需配合 `fps`、`min_pixels` 等参数优化处理。
- **音频**：仅 `qwen3.8-omni-flash`（Responses）与 `qwen-audio`（DashScope）支持；需指定 `format`（如 `wav`）及 `audio_url` 或 `data`。

## 限制和注意事项

- **地域与模型可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，调用前须在百炼控制台开通对应服务。
- **API 路径弃用**：OpenAI 兼容 Responses 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移至新版 `/compatible-mode/v1/responses`。
- **参数兼容性**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**仅处理本文档明确列出的参数**，未提及的 OpenAI 参数（如 `background`）将被忽略；Anthropic 接口不提供 `/v1/models` 列表接口，客户端模型发现请求将返回 404。
- **上下文截断**：Responses 接口为预留工具调用空间，最大输入上下文约为模型窗口大小的 80%，超出部分自动截断，不报错。
- **缓存与计费**：Session 缓存（`x-dashscope-session-cache: enable`）可降低多轮延迟，但命中缓存的 token 仍会计费；显式缓存（`cache_control: {type: "ephemeral"}`）需在内容块中声明，且仅对命中缓存的请求按缓存计费。
- **错误处理**：`GET /responses/{id}` 或 `DELETE /responses/{id}` 仅对 `store=true` 创建的响应有效；若 ID 不存在，返回 `{"error": {"message": "Response with id 'resp_xxx' not found.", "type": "InvalidParameter"}}`。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


