# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多套 OpenAI 兼容的工具集与框架接口，覆盖文本生成、多模态理解、[向量嵌入](../concepts/embedding.md)、批量推理、对话管理及 LangChain 集成等核心场景。所有接口均通过统一的 `compatible-mode/v1` 路径暴露，支持标准 OpenAI SDK（Python/Node.js/Java/Go/C#）和原生 HTTP 调用，开发者可零代码改造迁移现有应用。

## 支持的模型/功能

百炼兼容接口支持三大类能力：  
- **基础文本生成**：包括 `chat/completions`（[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）、`completions`（代码补全专用，仅限 `qwen-coder-turbo`）和 `responses`（智能体原生接口，内置联网搜索、网页抓取等工具）；  
- **多模态理解**：`chat/completions` 支持图像输入（Qwen-VL、QVQ、Qwen-OCR），需使用 `image_url` 结构化内容；  
- **向量化与批量处理**：`embeddings` 接口支持 `text-embedding-v{1,2,3,4}` 及 `qwen3.7-text-embedding` 系列；`batch` 接口分两种形态——文件式批量（[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）和同步式批量（[OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）；  
- **上下文管理**：`conversations` 接口自动维护跨设备会话状态，配合 `responses` 的 `previous_response_id` 实现无状态上下文注入；  
- **文件协同**：`files` 接口支持 `file-extract`（文档问答）、`batch`（批量任务输入）、`fine-tune`（调优数据集）三类用途，文件 ID 可复用于 Qwen-Long、Qwen-Doc-Turbo 等模型。

> **注意**：`qwen-audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；`qwen3.8-omni-flash` 处理音视频输入时，必须使用 `responses` 接口而非 `chat/completions`，详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 关键参数

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填，服务端点。推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）仍可用但性能与稳定性较低 | `{WorkspaceId}` 需从控制台「业务空间详情」获取；地域与 API Key 必须严格匹配，跨地域调用将返回 `invalid_api_key` 错误 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `model` | 模型名称，区分大小写。不同接口支持范围不同：`chat/completions` 支持 Qwen、DeepSeek、Kimi 等数十种模型；`completions` 仅支持 `qwen-coder-turbo`；`responses` 仅支持 `qwen3.x-*` 和 `deepseek-v4-*` 等指定型号 | `qwen3.8-max` 在 `responses` 接口下支持 Omni 输入，但在 `chat/completions` 下不支持音视频 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |
| `stream` / `stream_options` | [流式输出](../concepts/streaming-output.md)开关。`stream_options={"include_usage": true}` 可在流末尾返回 token 统计，但 `completions` 接口不支持该选项 | `qwen-vl-plus` 等视觉模型强制要求 `stream=True`，否则调用失败 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) |
| `enable_thinking` | 批量场景下控制思考模式（影响 token 成本）。`qwen3.5/3.6/3.7/3.8` 系列默认开启，必须作为 `body` 顶层参数传入，不可置于 `extra_body` 内 | 该参数在 `chat/completions` 实时接口中无效，仅对 `batch` 文件输入和 `batch chat` 同步接口生效 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |

## 使用方式

### 通用配置
- **API Key**：必须按地域创建并配置到环境变量 `DASHSCOPE_API_KEY`，硬编码存在泄露风险；  
- **SDK 安装**：`pip install -U openai langchain_openai`（Python）、`npm install @langchain/openai @langchain/community`（JS）；  
- **LangChain 集成**：推荐 `ChatTongyi`（全模型支持）或 `ChatOpenAI`（部分模型），后者需显式设置 `base_url` 和 `model` [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

### 典型调用链
1. **单次对话**：`chat/completions`（低延迟）或 `batch chat`（高性价比，超时最长 3600 秒）；  
2. **长文档分析**：先 `files.create(purpose="file-extract")` 上传，再 `chat/completions` 中引用 `file_id`；  
3. **多轮智能体**：优先用 `responses.create()` + `previous_response_id`，避免手动拼接消息历史；  
4. **跨设备会话**：`conversations.create()` 初始化，后续请求通过 `conversation_id` 自动注入上下文；  
5. **批量任务**：准备 JSONL 文件 → `files.create(purpose="batch")` → `batches.create(input_file_id=...)` → 轮询 `batches.retrieve()` 获取 `output_file_id`。

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 地域必须一致，北京 Key 无法调用弗吉尼亚 endpoint，错误码为 `invalid_api_key`（非密钥失效）；  
- **文件配额**：`files` 接口总容量上限 100 GB、最多 10,000 个文件，超限时需手动清理；  
- **模型能力差异**：`responses` 接口的 Agent 功能（如内置工具）仅对 `qwen3.8-*`、`qwen3.7-*` 等直供模型完整支持，第三方模型（如 SiliconFlow DeepSeek）仅支持基础兼容 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **Embedding 稀疏向量**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 `output_type=sparse`，若需稀疏向量请改用 DashScope 原生接口；  
- **旧路径弃用**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已停用，必须迁移到 `/compatible-mode/v1/{responses,conversations}`；  
- **超时控制**：`batch chat` 默认等待 3600 秒，需在 SDK 客户端显式配置 timeout（如 Python 的 `with_options(timeout=1800)`），HTTP 调用需设置客户端连接超时。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)


