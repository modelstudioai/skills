# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，覆盖文本生成、视觉理解、[向量嵌入](../concepts/vector-embedding.md)、批量处理、会话管理等核心场景，支持主流 SDK（如 OpenAI Python/Node.js SDK、LangChain）无缝集成。所有接口均基于统一的 `compatible-mode/v1` 路径体系，通过 `base_url` 和模型名称切换能力，无需修改业务逻辑即可迁移。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 文本模型，以及 DeepSeek、GLM、Kimi 等第三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **视觉理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，支持图像 URL 与 Base64 输入（详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **[向量嵌入](../concepts/vector-embedding.md)**：`text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash`，支持多维度与多语种（详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **长文档与文件分析**：`Qwen-Long`、`Qwen-Doc-Turbo`，需配合文件上传接口使用（详见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。
- **智能体与工具调用**：仅 `Responses API`（非 Chat Completions）支持内置联网搜索、代码解释器等原生工具能力，且仅限列表中阿里云直供模型（如 `qwen3.8-max`），第三方模型不支持 Agent 功能（详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。

> **注意**：文档 2 与文档 1 对“Agent 能力支持范围”的描述存在矛盾。文档 1 明确指出“非列表中阿里云百炼直供文本生成模型仅支持基础兼容能力，Agent 能力（内置工具等）受限”，而文档 2 在“支持的模型列表”中笼统包含 Qwen-VL、Qwen-Coder 等多类模型但未限定其 Agent 能力。实际以文档 1 的明确限制为准。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，服务端点。推荐使用业务空间专属域名以获得更高稳定性 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | 必填，模型名称，需严格匹配支持列表 | `"qwen3.8-max"`、`"text-embedding-v4"` |
| `previous_response_id` | Responses API 专用，用于自动关联多轮上下文（传入上一轮响应顶层 `id`） | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |
| `enable_thinking` | Batch 场景下控制思考模式开关（`true`/`false`），影响 token 成本与推理时长 | `false`（建议显式设置） |
| `dimensions` | Embedding API 专用，指定向量维度（仅 `text-embedding-v3`/`v4` 支持） | `1024` |
| `purpose` | 文件接口专用，标识文件用途：`file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优） | `"batch"` |

## 使用方式

- **SDK 调用**：安装 `openai` 或 `langchain_openai`，配置 `api_key` 与 `base_url` 即可复用 OpenAI 代码。LangChain 用户可选 `ChatOpenAI`（部分模型）或 `ChatTongyi`（全模型支持）[在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **HTTP 调用**：直接向对应 endpoint 发送 POST 请求，`Authorization: Bearer $DASHSCOPE_API_KEY` 头认证。
- **批量处理**：
  - **Batch File**：上传 JSONL 文件异步执行，适用于评测、标注等高吞吐低延迟场景（详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。
  - **Batch Chat**：同步阻塞调用，单请求等待结果返回，成本比实时 API 低 50%（详见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）。
- **会话管理**：Conversations API 提供 `create`/`retrieve`/`update`/`delete`/`items.create` 全生命周期操作，配合 Responses API 实现跨设备上下文延续（详见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）。

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 所属地域必须一致（如北京 Key 只能调用北京 endpoint），否则返回 `invalid_api_key` 错误（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **域名迁移**：旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/...` 已废弃，必须迁移到 `/compatible-mode/v1/...`；同时建议从 `dashscope.aliyuncs.com` 迁移至业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。
- **文件限制**：`file-extract` 用途单文件 ≤150 MB；`batch` 用途单文件 ≤500 MB；`fine-tune` 用途单文件 ≤300 MB（详见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。
- **Embedding 限制**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持稀疏向量输出（`output_type=sparse`），传入该参数将导致 embedding 字段为空（详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **模型能力差异**：`qwen3.8-omni-flash` 支持音视频输入，但 `qwen3.5-omni-plus` 不支持语音输出；`Qwen-Audio` 完全不支持 OpenAI 兼容协议（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


