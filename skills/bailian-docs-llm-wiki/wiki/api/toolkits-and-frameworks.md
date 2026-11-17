# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)工具包与框架，覆盖文本生成、多模态理解、向量化、批量推理、会话管理及主流开发框架集成等场景。所有接口均通过统一的 `compatible-mode/v1` 路径提供标准化调用能力，开发者可复用现有 OpenAI 生态代码快速迁移，仅需调整 `base_url`、`api_key` 和模型名称即可。

## 支持的模型/功能

- **文本生成**：`qwen4-max`、`qwen3.8-max`、`qwen3.7-plus` 等全系列 Qwen 文本模型，支持 `chat/completions`（含 function calling）、`responses`（智能体原生接口）、`conversations`（上下文持久化）三类核心能力 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持视觉输入，兼容 OpenAI Vision 协议，支持 `image_url` 格式传图 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等 7 款 Embedding 模型，支持多维度、多语种向量化，但**不支持稀疏向量输出**（`output_type=sparse` 无效）[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **文件处理**：`Qwen-Long`、`Qwen-Doc-Turbo` 支持文档问答与数据提取；`batch` 用途支持批量推理任务输入；`fine-tune` 用途支持模型调优数据集上传 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **批量推理**：提供两种模式：
  - **Batch File**（异步）：通过 JSONL 文件提交大批量请求，成本为实时调用的 50% [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)；
  - **Batch Chat**（同步）：单请求阻塞等待，保持同步调用习惯，同样享 50% 成本优惠 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。
- **框架集成**：全面支持 LangChain（Python/JS/Java），提供 `langchain_openai`（OpenAI 兼容子集）和 `langchain_community.chat_models.tongyi`（全模型支持）双路径 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；而 `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，该限制未在 Conversations 或 Responses 文档中明确说明，属功能不一致。

## 关键参数

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，官方强烈建议迁移。
- **`api_key`**：严格按地域绑定，北京地域 API Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误而非权限不足提示 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **`model`**：模型名需精确匹配文档列表，例如 `qwen3-vl-plus`（Vision）、`text-embedding-v4`（Embedding）、`qwen4-max`（Chat/Responses）；`batch-test-model` 仅用于链路测试，不可用于生产。
- **`purpose`（文件接口）**：必须指定为 `file-extract`（文档分析）、`batch`（批量输入）或 `fine-tune`（调优数据集），不同 purpose 对应不同文件格式与大小限制。
- **`enable_thinking`（Batch 场景）**：`qwen3.5+` 系列模型默认开启思考模式，需显式设为 `false` 关闭以避免额外 token 成本，且该参数必须与 `model` 同级置于 `body` 顶层，不可放入 `extra_body` [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

## 使用方式

- **SDK 调用**：推荐使用最新版 `openai` SDK（Python/Node.js/Java/Go/C#）或 `langchain_openai`，配置 `base_url` 与 `api_key` 后，直接复用 OpenAI 原生方法（如 `client.chat.completions.create`、`client.embeddings.create`、`client.files.create`）。
- **HTTP 调用**：构造标准 REST 请求，`Authorization: Bearer $DASHSCOPE_API_KEY`，`Content-Type: application/json`，endpoint 与 SDK `base_url` + path 一致（如 `/v1/chat/completions`、 `/v1/embeddings`、`/v1/files`）。
- **LangChain 集成**：
  - 优先选用 `ChatOpenAI`（轻量、兼容性好，但仅支持部分模型）；
  - 如需全模型支持（含部署模型、Omni、Audio），必须使用 `ChatTongyi`（Python）或 `ChatAlibabaTongyi`（JS）或 `ChatTongyi`（Java）。
- **流式响应**：所有 `chat/completions` 接口均支持 `stream=True`，`responses` 接口需设置 `stream_options={"include_usage": True}` 获取最终 token 统计。
- **上下文管理**：
  - `responses` 接口通过 `previous_response_id` 自动关联历史，无需维护消息数组；
  - `conversations` 接口提供 `create`/`items.create`/`retrieve` 全生命周期管理，实现跨设备会话延续。

## 限制和注意事项

- **地域隔离**：API Key 与 endpoint 地域强绑定，跨地域调用必失败，错误码统一为 `invalid_api_key`，非 `invalid_region` [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **文件配额**：文件服务总容量上限 100 GB，文件总数上限 10,000 个，达任一上限后上传失败，需手动清理。
- **Batch 限制**：
  - `batch-test-model` 仅限 ≤1 MB、≤100 行的 JSONL 文件，且并发上限 2；
  - 正式模型单次请求上下文最大 256K tokens（`qwen3.5-omni-plus` 等 Omni 模型除外）；
  - `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，该限制未在 Omni 相关文档中体现，属隐含约束。
- **Embedding 限制**：`output_type=sparse` 参数在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中被静默忽略，返回空 embedding，如需稀疏向量，必须切换至 DashScope 原生接口。
- **模型兼容性差异**：`Qwen-Audio` 不支持任何 OpenAI 兼容协议，而 `Qwen-VL`、`Qwen-OCR` 仅支持 Vision 协议，`Qwen-Long` 仅支持文件协议，不存在“全协议兼容模型”。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


