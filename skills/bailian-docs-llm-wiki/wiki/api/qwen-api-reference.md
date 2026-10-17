# qwen api reference

阿里云百炼平台提供多种兼容协议的 Qwen 模型调用方式，包括 OpenAI 兼容 Responses/Chat、Anthropic 兼容 Messages 以及原生 DashScope API。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.8-omni-flash` 等）及部分第三方模型。核心能力涵盖文本生成、[多模态](../concepts/multimodal.md)理解（图像/音视频）、工具调用（联网搜索、代码解释器等）与深度思考控制。

## 支持的模型/功能

- **模型覆盖**：  
  - 文本模型：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen3.5-397b-a17b` 等全系列商业版与开源版；  
  - [多模态](../concepts/multimodal.md)模型：`qwen3.8-omni-flash`（支持音视频输入）、`qwen3.7-vl-plus`、`qwen2.5-vl`、`qven3.5-ocr`（PDF 解析）；  
  - 第三方模型：`deepseek-v4-pro`、`glm-5.3`、`kimi-k3` 等（详见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。  
  > **注意**：Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

- **核心功能**：  
  - **内置工具链**：联网搜索（`web_search`）、网页抓取（`web_extractor`）、代码解释器（`code_interpreter`）、文搜图/图搜图、知识库搜索（`file_search`），均通过 `tools` 参数声明并自动触发；  
  - **多轮对话管理**：支持 `previous_response_id`（单轮上下文引用）与 `conversation`（会话级上下文）两种模式；  
  - **结构化输出**：通过 `output_config.format.type = "json"`（Anthropic 兼容）或 `response_format = {"type": "json_object"}`（OpenAI 兼容）启用强约束 JSON 输出；  
  - **显式缓存**：在 `messages` 或 `system` 内容块中添加 `cache_control: {type: "ephemeral"}` 标记可复用缓存前缀。

## 关键参数

| 参数 | 类型 | 说明 | 兼容性 |
|------|------|------|--------|
| `model` | `string` | 必填。模型 ID，如 `qwen3.8-max`。非列表中模型仅支持基础能力，Agent 功能受限 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 | 所有协议 |
| `input` / `messages` | `string` 或 `array` | 必填。OpenAI Responses 支持纯字符串或 EasyInputMessage 数组；OpenAI Chat 与 DashScope 使用标准消息数组（含 `role`/`content`）；Anthropic 使用 `messages` + `system` 字段。 | 协议专属 |
| `tools` | `array` | 可选。声明可用工具，如 `[{"type": "web_search"}]`。`qwen3.8-omni-flash` 仅支持 `web_search` 内置工具 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 | OpenAI Responses/Chat, Anthropic |
| `reasoning.effort` / `output_config.effort` | `string` | 控制思考强度。Responses API 用 `reasoning.effort`（值如 `high`, `xhigh`）；Anthropic 用 `output_config.effort`（值如 `max`, `low`）；二者语义不互通。 | Responses / Anthropic |
| `stream` | `boolean` | 可选。启用[流式输出](../concepts/streaming-output.md)（`true`），返回 `text/event-stream`。所有协议均支持。 | 所有协议 |
| `store` | `boolean` | Responses API 专用。`true` 时响应可被 `previous_response_id` 引用；`false` 则不可检索 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)。 | OpenAI Responses |

> **注意**：`temperature` 在 Anthropic 兼容接口中取值范围为 `[0, 2)`，而 Anthropic 官方为 `[0.0, 1.0]`，迁移时需校准 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

## 使用方式

- **Endpoint 配置**：  
  - **OpenAI 兼容**（Responses/Chat）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，例如北京地域为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；  
  - **Anthropic 兼容**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/apps/anthropic`；  
  - **DashScope 原生**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1`，路径按模型类型区分（`/services/aigc/text-generation/generation` 或 `/services/aigc/multimodal-generation/generation`）。  
  > `{WorkspaceId}` 为业务空间 ID，需从控制台获取；旧域名（如 `dashscope.aliyuncs.com`）仍可用但**强烈建议迁移至新域名**以获得更高性能与稳定性 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。

- **认证**：  
  - OpenAI/Anthropic 兼容：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key: <API_KEY>`（Anthropic）传入；  
  - DashScope SDK：配置环境变量 `DASHSCOPE_API_KEY` 或代码中显式设置。

- **[多模态](../concepts/multimodal.md)输入示例**（以 `qwen3.8-omni-flash` 为例）：  
  ```json
  {
    "input": [
      {
        "role": "user",
        "content": [
          {"type": "input_text", "text": "分析这段音频内容"},
          {"type": "input_audio", "audio_url": "https://example.com/audio.mp3", "format": "mp3"}
        ]
      }
    ]
  }
  ```

## 限制和注意事项

- **上下文长度**：Responses API 的最大输入上下文约为模型窗口的 80%（预留 20% 给工具调用与推理），超长部分将自动截断且不报错 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。  
- **参数兼容性**：OpenAI Responses API **不支持** `background`（异步执行）等部分 OpenAI 参数，仅处理文档明确列出的字段；未提及参数将被忽略。  
- **文件与媒体限制**：  
  - PDF 文件最大 100 MB（`qwen3.5-ocr` 支持），页数上限取决于 `ocr_options.task`（`document_parsing` 时最多 50 页）；  
  - 图片最大 20 MB，Base64 编码需为完整 Data URI（如 `data:image/png;base64,...`）；  
  - 视频抽帧 `fps` 范围 `[0.1, 10]`，`total_pixels` 默认 `819200000`（对应 80 万图像 [Token](../concepts/token.md)）。  
- **响应存储与查询**：`store=false` 时，响应无法通过 `GET /responses/{id}` 或 `/responses/{id}/input_items` 查询；`previous_response_id` 仅对 `store=true` 的响应有效 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)。  
- **废弃参数**：`thinking.budget_tokens`（Anthropic 兼容）已标记为**即将废弃**，新接入应使用 `output_config.effort` 替代 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


