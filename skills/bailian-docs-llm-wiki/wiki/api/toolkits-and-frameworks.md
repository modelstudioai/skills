# toolkits and [frameworks](frameworks.md)

阿里云百炼提供一系列 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、向量嵌入、批量处理、对话管理等核心场景。开发者可复用现有 OpenAI SDK 和工程实践，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移。所有接口均支持标准 OpenAI SDK（Python/Node.js/Java/Go/C#）及原生 HTTP 调用。

## 支持的模型/功能

- **文本与智能体**：`qwen4-max`、`qwen3.8-max`、`qwen3.7-plus` 等全系 Qwen 文本模型；支持 `function_call`、内置工具（联网搜索、代码解释器等）及 `tool_choice` 控制，详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **多模态**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像理解；`qwen3.5-omni-plus`、`qwen3.5-omni-flash` 支持音视频输入；`Qwen-Audio` **不支持** OpenAI 兼容协议，仅支持 DashScope 协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等全系列 Embedding 模型，支持多维度输出（如 `dimensions=1024`），但 **不支持稀疏向量（`output_type=sparse`）** —— 该参数在 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)中将被忽略并返回空 embedding [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **文件与批量**：`Qwen-Long`、`Qwen-Doc-Turbo` 支持文档问答；`batch-test-model` 用于链路验证；`qwen3.8-max` 等主流模型在 Batch 场景下最大上下文支持 256K tokens [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **对话状态管理**：`Conversations API` 提供会话生命周期管理（创建、更新、删除、追加消息），配合 `Responses API` 的 `previous_response_id` 实现跨设备上下文延续。

> **注意**：文档 2（Responses API）与文档 9（Conversations API）均提及 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations` 为新版路径，但文档 2 明确指出旧版 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，而文档 9 仅称旧版 `/api/v2/apps/protocols/compatible-mode/v1/conversations` “即将停止维护”。实际开发中应以文档 2 的“已停止维护”为准，统一迁移到新版路径。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，地域专属业务空间域名，**非全局通用域名** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | 必填，**严格按地域绑定**：北京地域 Key 只能调北京 endpoint | `sk-xxx`（从控制台对应地域获取） |
| `model` | 必填，模型名需与所选接口能力匹配（如 Vision 接口必须用 `qwen3-vl-plus`） | `qwen4-max`, `qwen3-vl-plus`, `text-embedding-v4` |
| `enable_thinking` | 部分模型（如 `qwen3.8-*` 系列）默认开启思考模式，显式设为 `false` 可降本 | `true` / `false`（须与 `model` 同级，不可置于 `extra_body`） |
| `previous_response_id` | Responses API 多轮对话关键参数，**必须传顶层 `id`（`resp_xxx`），非 `output` 内 `msg_xxx`** | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |

## 使用方式

1. **初始化客户端**：配置 `api_key`（推荐环境变量）和 `base_url`（含 `{WorkspaceId}`）；
2. **选择接口**：
   - 标准对话 → `client.chat.completions.create()`
   - 智能体响应 → `client.responses.create()`（自动注入工具、简化历史）
   - 向量计算 → `client.embeddings.create()`
   - 文件上传 → `client.files.create(purpose="file-extract")`
   - 批量任务 → `client.batches.create(input_file_id=...)` 或 `client.chat.completions.create()`（Batch Chat）
   - 对话管理 → `client.conversations.*`（创建/追加/查询会话）
3. **传参调用**：按接口要求传入 `model`、`input`/`messages`、`stream` 等参数；
4. **处理响应**：流式响应需遍历 `chunk`；非流式直接取 `response.choices[0].message.content` 或 `response.output_text`（Responses API）。

## 限制和注意事项

- **地域强绑定**：API Key 与 `base_url` 所属地域必须一致，跨地域调用返回 `invalid_api_key`（HTTP 401），而非权限错误 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **域名迁移强制性**：`dashscope.aliyuncs.com` 等旧域名虽仍可用，但官方明确建议迁移至业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性，该要求适用于 Chat、Responses、Vision、Embedding、Conversations 全系列接口。
- **文件服务配额**：文件上传总上限为 10,000 个文件或 100 GB，达任一上限后新上传失败，需手动清理。
- **Batch 超时**：Batch Chat 默认等待 3600 秒（1 小时），超时断连；Batch File 任务最长等待 24 小时（`completion_window="24h"`）。
- **LangChain 集成差异**：`langchain_openai` 仅支持部分模型（如 `qwen-plus`），而 `langchain-community` 的 `ChatTongyi` 支持全部百炼文本模型，选型时需注意能力覆盖范围 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


