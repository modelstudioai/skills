# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与专用工具链，支持开发者快速迁移现有应用或构建新场景。核心能力覆盖文本生成（Chat/Responses/Completions）、多模态理解（Vision）、向量化（Embedding）、文件处理（Files）、批量推理（Batch）及会话管理（Conversations），并可通过 LangChain 等主流框架无缝集成。所有接口均需配置地域绑定的 API Key 与业务空间专属 `base_url`。

## 支持的模型/功能

- **文本生成**：支持 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.3` 等数十个大语言模型，通过 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 和 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 提供标准调用能力；其中 Responses API 内置联网搜索、网页抓取、代码解释器等智能体工具，而 Chat API 支持 `function_call` 和多轮对话。
- **多模态理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-ocr` 等视觉模型通过 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) 支持图像+文本混合输入，但 QVQ 模型仅支持[流式输出](../concepts/streaming-output.md)。
- **补全与代码生成**：`qwen-coder-turbo` 是当前唯一支持 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) 的模型，专用于 FIM（Fill-in-the-Middle）代码补全。
- **向量化**：`text-embedding-v4`、`qwen3.7-text-embedding` 等模型通过 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) 提供同步嵌入服务，**注意：该接口不支持稀疏向量输出（`output_type=sparse`）**，否则返回空 embedding。
- **文件与批量处理**：`qwen-long`、`qwen-doc-turbo` 支持文档问答；`batch-test-model` 可用于 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 全链路测试；[OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 则适用于单请求高延迟容忍场景。
- **会话状态管理**：[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 提供 `conversations.create`、`items.add` 等操作，实现跨设备上下文持久化，配合 Responses API 的 `previous_response_id` 使用效果更佳。

> **注意**：文档 1 与文档 2 均列出支持模型，但文档 1 明确声明“非列表中阿里云百炼直供文本生成模型仅支持基础兼容能力，Agent 能力（内置工具等）受限”，而文档 2 未作此限制说明且包含更多第三方模型（如 SiliconFlow DeepSeek）。实际使用中，**仅文档 1 所列模型可保证 Responses API 的完整 Agent 功能**；其他模型在 Chat 接口下可能可用，但 Responses 的工具调用、reasoning 输出等高级特性不可用。

## 关键参数

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）已逐步停用。不同接口路径不同：
  - Chat/Embedding/Vision：`/chat/completions`、`/embeddings`、`/chat/completions`
  - Responses：`/responses`
  - Conversations：`/conversations`
  - Files/Batch：`/files`、`/batches`
- **`model`**：严格区分大小写与版本后缀（如 `qwen3.8-max` ≠ `qwen3.8-max-0902`），且模型能力随接口类型变化（例如 `qwen3.8-omni-flash` 仅在 Responses 中支持音视频输入）。
- **`previous_response_id`**（Responses）：传入上一轮响应的顶层 `id`（UUID 格式），**不是 `output` 数组内消息的 `id`**（见文档 1 示例注释）。
- **`enable_thinking`**（Batch）：`qwen3.5+` 系列模型默认开启思考模式，显式设为 `false` 可避免额外 reasoning token 成本（见文档 6 和文档 8）。
- **`purpose`**（Files）：必须指定为 `file-extract`（文档分析）、`batch`（批量任务）或 `fine-tune`（调优数据集），对应不同文件格式与大小限制（见文档 5）。

## 使用方式

1. **环境准备**：获取对应地域的 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`；安装 SDK（如 `pip install -U openai langchain_openai`）。
2. **初始化客户端**：设置 `base_url` 为业务空间专属地址（替换 `{WorkspaceId}`），例如：
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   ```
3. **按接口调用**：
   - **Chat**：`client.chat.completions.create(model="qwen-plus", messages=[...])`
   - **Responses**：`client.responses.create(model="qwen3.8-max", input="...")`
   - **Completions**：`client.completions.create(model="qwen-coder-turbo", prompt="<tool_call>...<tool_call>")`
   - **Embedding**：`client.embeddings.create(model="text-embedding-v4", input="...")`
   - **Files**：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`
   - **Conversations**：`client.conversations.create(items=[{"role":"system","content":"..."}])`
4. **LangChain 集成**：推荐使用 `langchain_openai.ChatOpenAI`（兼容部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部百炼模型），详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 地域必须严格匹配（如北京 Key + 北京 `base_url`），跨地域调用将返回 `invalid_api_key` 错误（见文档 2 “调用失败排查”）。
- **模型能力差异**：
  - `qwen-audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 协议（见文档 2）；
  - `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出（见文档 6 和文档 8）；
  - 多模态 Embedding 模型（如 `qwen3-vl-embedding`）**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**（见文档 7）。
- **路径与域名迁移**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已废弃，必须迁移到 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations`（见文档 1 和文档 9）。
- **Batch 文件限制**：JSONL 输入文件中 `enable_thinking` 必须作为 `body` 顶层参数传入，**不能放在 `extra_body` 中**（见文档 6 和文档 8）。
- **并发与配额**：文件上传总大小上限 100 GB、数量上限 10,000 个；Batch 测试模型并发上限 2 个任务（见文档 5 和文档 6）。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


