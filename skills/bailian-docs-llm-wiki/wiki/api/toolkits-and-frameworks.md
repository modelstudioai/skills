# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、嵌入向量、文件处理、批量推理及会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#/etc.），并提供业务空间专属域名以提升稳定性与性能。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 文本模型，以及 DeepSeek、GLM、Kimi 等第三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；  
- **视觉理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，支持多模态输入（图像+文本），但 [QVQ 模型仅支持流式输出](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；  
- **嵌入向量**：`text-embedding-v4`、`qwen3.7-text-embedding` 等，支持多语种与可变维度（如 `dimensions=1024`），但 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**不支持稀疏向量输出**（`output_type=sparse` 无效）；  
- **长文档与文件分析**：`Qwen-Long`、`Qwen-Doc-Turbo`，通过文件 ID 实现文档问答与数据提取；  
- **批量处理**：`Batch Chat`（单请求同步等待）与 `Batch File`（JSONL 文件异步处理），成本降低 50%，支持 `qwen3.8-max` 等模型在 Batch 场景下最高 256K 上下文；  
- **智能体增强**：`Responses API` 内置联网搜索、网页抓取、代码解释器等工具，区别于标准 Chat Completions，详情见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；  
- **会话持久化**：`Conversations API` 提供跨设备会话管理，支持创建、检索、更新、删除会话及追加消息项，配合 Responses API 自动注入历史上下文。

> **注意**：文档 1 与文档 2 对“支持的模型列表”存在范围差异——文档 1 明确限定 Responses API 仅对指定 `qwen3.x` 和 `deepseek-v4` 等模型启用完整 Agent 能力，而文档 2 声称支持更广谱的模型（含 Qwen-VL、Qwen-Omni、MiniMax 等），但未说明其在 Responses 或 Conversations 中是否可用。实际开发中应以文档 1 的模型列表为准，避免在非列表模型上调用 `responses.create` 导致工具调用失效。

## 关键参数

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `base_url` | string | 接口服务地址，**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`） | 旧域名（`dashscope.aliyuncs.com`）已逐步停用；[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 明确要求迁移至新版路径 `/compatible-mode/v1/conversations` |
| `model` | string | 模型名称，严格区分大小写与版本后缀（如 `qwen3.8-max` ≠ `qwen3.8-max-0902`） | 非列表模型可能仅支持基础文本生成，无工具/多模态能力 |
| `previous_response_id` | string | Responses API 多轮对话关键参数，传入上一轮响应顶层 `id`（UUID 格式），非 `output` 内 `msg_xxx` | 有效期为 7 天，见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |
| `enable_thinking` | boolean | Batch 场景下控制思考模式开关（`true`/`false`），影响 token 计费 | 必须作为 JSONL 请求体顶层参数，不可置于 `extra_body` 内 |
| `purpose` | string | 文件接口必填字段，取值 `file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集） | 单文件大小限制不同：`file-extract` ≤150 MB，`batch` ≤500 MB，`fine-tune` ≤300 MB |

## 使用方式

1. **环境准备**：获取对应地域的 API Key（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)），配置至环境变量 `DASHSCOPE_API_KEY`，安装 OpenAI SDK（`pip install -U openai`）；  
2. **初始化客户端**：设置 `base_url` 为业务空间专属地址（替换 `{WorkspaceId}`），例如北京地域：  
   ```python
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   ```  
3. **按场景调用**：  
   - 文本对话 → `client.chat.completions.create(...)`（Chat API）或 `client.responses.create(...)`（Responses API）；  
   - 视觉理解 → `client.chat.completions.create(...)` + `messages` 中含 `image_url`；  
   - 向量生成 → `client.embeddings.create(...)`；  
   - 文件上传 → `client.files.create(file=Path("x.txt"), purpose="file-extract")`；  
   - 批量任务 → `client.batches.create(input_file_id="file-batch-xxx", endpoint="/v1/chat/completions", ...)`；  
   - 会话管理 → `client.conversations.create(...)` / `.retrieve(...)` / `.update(...)` / `.delete(...)`；  
4. **流式与非流式**：所有 `chat.completions` 和 `responses` 接口均支持 `stream=True`，Embedding 与 Files 接口为同步；  
5. **LangChain 集成**：推荐使用 `langchain_openai.ChatOpenAI`（兼容部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部模型），详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 地域强绑定，北京 Key 不可调用弗吉尼亚 endpoint，否则返回 `invalid_api_key`（HTTP 401）；  
- **模型能力差异**：`qwen3.8-omni-flash` 支持音视频输入，但 `Qwen-Audio` 明确不支持 OpenAI 兼容协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；  
- **路径弃用**：Responses API 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 和 Conversations API 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已停止维护，必须迁移；  
- **文件配额**：百炼存储空间上限为 10,000 个文件或 100 GB 总大小，超限后上传失败；  
- **并发与超时**：Batch Chat 默认超时 3600 秒（1 小时），需显式设置 `timeout` 参数（如 Python 的 `with_options(timeout=1800.0)`）；  
- **错误处理**：统一参考 [错误码](../../raw/model-api-reference/preparations/error-code.md)，常见错误包括 `401 invalid_api_key`（地域不匹配）、`404 Not Found`（路径错误）、`413 Payload Too Large`（prompt 超长）。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


