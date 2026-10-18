# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容（Chat 和 Responses）、Anthropic 兼容（Messages）以及原生 DashScope 协议。开发者可根据现有技术栈和功能需求选择合适接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方直供模型（如 DeepSeek、GLM、Kimi）。统一通过业务空间专属域名接入，推荐使用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com` 格式 endpoint 以获得更优性能与稳定性。

## 支持的模型/功能

- **核心模型**：Qwen 系列（`qwen3.8-*`、`qwen3.7-*`、`qwen3.6-*`、`qwen3.5-*`、`qwen3-vl-plus`、`qwen3-coder-flash`）、Qwen-Audio（仅 DashScope 协议支持，[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）、Qwen-Omni（仅 OpenAI 兼容 Chat 支持视频文件输入）。
- **[多模态](../concepts/multi-modal.md)能力**：图像理解（Qwen-VL、QVQ）、视频理解（Qwen-VL、Qwen-Omni、QVQ）、音频理解（Qwen-Omni、Qwen-Audio）、文档解析（PDF via `input_file`）。
- **高级功能**：
  - 工具调用（Function Calling、联网搜索、网页抓取、代码解释器等），在 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 和 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 中完整支持；
  - 显式缓存（`cache_control.type = "ephemeral"`），见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)；
  - 结构化输出（JSON Schema 强约束），仅限 `qwen3.8`/`qwen3.7`/`deepseek`/`glm` 系列在 Anthropic 兼容 Messages 接口中支持；
  - Session 缓存（`x-dashscope-session-cache: enable`），仅 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 支持。

> **注意**：Qwen-Audio 明确不支持 OpenAI 兼容协议，仅可通过 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 调用；QwQ 模型不建议设置 system message，QVQ 模型的 system message 不生效 —— 这些限制在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中一致声明，无矛盾。

## 关键参数

| 参数 | 所属协议 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必填。模型 ID，需与所选协议支持列表匹配。OpenAI Chat 支持最广（含三方模型），Responses 与 Anthropic 有子集差异 | `"qwen3.8-max"`, `"deepseek-v4.1-flash-1017"` |
| `messages` / `input` / `content` | Chat / Responses / Anthropic | 输入格式不同：Chat 严格要求 `[{role, content}]`；Responses 支持 `string` 或 `array`；Anthropic 使用 `[{role, content}]` 且 `content` 可为 `text`/`image`/`video` 数组 | `{"role":"user","content":[{"type":"text","text":"你好"}]}` |
| `max_tokens` | Anthropic | 必填。语义因模型而异：对 `qwen3.8-max` 是「回复+思考」总长；对 `qwen3.7-plus` 仅限回复长度；`glm-5.2` 行为取决于是否传 `thinking.budget_tokens` | `2048` |
| `temperature` | 全部 | 控制随机性。**OpenAI/Responses 协议范围为 `[0, 2)`，Anthropic 协议亦为 `[0, 2)`，但官方 Anthropic 为 `[0.0, 1.0]`** —— 迁移时需校准 | `0.7` |
| `stream` | 全部 | 是否流式响应。`true` 时返回 SSE 流或分块 JSON | `true` |
| `tools` | Responses / Anthropic | 定义可调用工具。Responses 支持内置工具（`web_search`）与自定义 function；Anthropic 需声明 `web_search_20250305` 等带日期后缀类型 | `[{"type": "web_search"}]` |

> **注意**：`fps` 参数在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中描述一致（取值 `[0.1,10]`，默认 `2.0`），但 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 中对 `input_audio`/`input_video` 的 `fps` 字段明确要求为 `number` 类型（非字符串），此为关键类型约束，开发者需注意。

## 使用方式

- **Endpoint 与认证**：  
  所有协议均使用业务空间专属域名：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`。地域包括 `cn-beijing`、`ap-southeast-1`、`us-east-1`、`eu-central-1`、`ap-northeast-1`、`cn-hongkong`。`{WorkspaceId}` 需替换为控制台获取的真实 ID。API Key 通过 `Authorization: Bearer <key>` 或 `x-api-key`（Anthropic）传入。

- **协议选择指南**：
  - 优先选用 **OpenAI兼容-Responses**（`/compatible-mode/v1/responses`）：适合需要 Agent 能力（内置工具、Session 缓存、多轮上下文自动管理）的场景，且已弃用旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses`；
  - 选用 **OpenAI兼容-Chat**（`/compatible-mode/v1/chat/completions`）：适用于标准 Chat 场景，兼容性最高，但不支持 Responses 的高级上下文管理；
  - 选用 **Anthropic兼容-Messages**（`/apps/anthropic/v1/messages`）：适用于已集成 Anthropic SDK 的用户，需注意 `temperature` 范围与 `tools` 声明格式（如 `web_search_20250305`）；
  - 选用 **DashScope API**（`/api/v1/services/aigc/.../generation`）：适用于需要调用 Qwen-Audio 或精细控制 `max_frames` 等 DashScope 特有参数的场景。

- **SDK 配置示例（Python）**：  
  ```python
  # OpenAI SDK（Responses）
  from openai import OpenAI
  client = OpenAI(
      api_key="sk-xxx",
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.responses.create(model="qwen3.8-max", input="你好")
  ```

## 限制和注意事项

- **域名迁移强制建议**：华北2（北京）、新加坡、中国香港地域的旧域名（`dashscope.aliyuncs.com` 等）虽仍可用，但新应用**必须**迁移到业务空间专属域名，以保障性能与稳定性，详见各文档“重要”提示。
- **上下文长度限制**：Responses API 为内置工具预留约 20% 上下文空间，实际可用输入长度约为模型窗口的 80%，超出部分将自动截断（不报错）；Chat 与 Anthropic 协议按模型原生窗口处理。
- **音视频输入限制**：
  - `input_audio`/`input_video` 仅在 Responses 协议中对 `qwen3.8-omni-flash` 开放；
  - 视频 `fps` 在 Responses 中必须为 `number` 类型，在 Chat/DashScope 中可为数字或字符串（但推荐统一用数字）；
  - Qwen-Audio 仅 DashScope 协议支持，且不兼容 OpenAI 协议。
- **缓存与计费**：显式缓存（`cache_control`）需在 `content` 级别声明；Session 缓存（`x-dashscope-session-cache`）仅 Responses 支持且需 `store=true`；所有缓存命中均影响 `cached_tokens` 计费项。
- **错误处理**：`previous_response_id` 或 `response_id` 查询失败时，统一返回 `InvalidParameter` 错误（如 `Response with id 'resp_xxx' not found.`），需在客户端做健壮性处理。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


