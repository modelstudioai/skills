# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架，覆盖文本生成、多模态理解、[向量嵌入](../concepts/embedding.md)、批量推理、对话状态管理等核心场景。开发者可通过统一的 SDK 接口（如 `openai` 或 `langchain_openai`）快速迁移现有应用，仅需调整 `base_url`、`api_key` 和 `model` 参数即可完成适配。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#），并遵循 OpenAI REST API 规范。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（仅限华北2北京地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，支持图像 URL 与 Base64 编码输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)  
- **[向量嵌入](../concepts/embedding.md)**：`text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash`，支持 64–2048 维可选输出 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)  
- **批量处理**：`Batch Chat`（单请求同步等待）与 `Batch File`（JSONL 文件异步提交），支持最大 256K 上下文长度的 Qwen 系列模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)  
- **智能体增强**：`Responses API` 内置联网搜索、网页抓取、代码解释器等工具；`Conversations API` 提供跨设备会话持久化能力 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)  

> **注意**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，该限制未在文档 7 中明确说明但与文档 5 一致。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，服务端点地址，**必须匹配 API Key 所属地域** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | 必填，模型名称，需与所选接口能力匹配 | `qwen3.8-max`（Chat）、`qwen3-vl-plus`（Vision）、`text-embedding-v4`（Embedding） |
| `workspace_id` | 必填，业务空间 ID，从控制台「业务空间详情」获取 | `ws-abc123def456` |
| `previous_response_id` | Responses API 多轮对话必需，传入上一轮响应顶层 `id`（UUID 格式） | `0c842a11-c7d1-45da-b7ec-4e668c389xxx` |
| `enable_thinking` | Batch 场景下控制思考模式开关（`true`/`false`），须与 `model` 同级传入 | `{"model": "qwen3.8-max", "enable_thinking": false}` |

## 使用方式

1. **安装依赖**：  
   ```bash
   pip install -U openai langchain_openai  # Python
   npm install openai @langchain/openai    # Node.js
   ```

2. **初始化客户端**（以 Python 为例）：  
   ```python
   from openai import OpenAI
   import os

   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   ```

3. **按接口调用**：  
   - Chat Completions：`client.chat.completions.create(...)`  
   - Responses：`client.responses.create(...)`  
   - Embeddings：`client.embeddings.create(...)`  
   - Conversations：`client.conversations.create(...)`  
   - Files：`client.files.create(file=..., purpose="file-extract")`  
   - Batches：`client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`  

4. **LangChain 集成**：  
   - OpenAI 兼容层（部分模型）：`ChatOpenAI(base_url="...", model="qwen-plus")`  
   - DashScope 原生层（全模型支持）：`ChatTongyi(model="qwen-long", dashscope_api_key=...)` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)

## 限制和注意事项

- **地域绑定严格**：API Key 与 `base_url` 所属地域必须一致，跨地域调用将返回 `invalid_api_key` 错误（HTTP 401），而非密钥失效 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **域名迁移强制要求**：旧域名 `dashscope.aliyuncs.com` 已逐步停用，所有新项目必须使用业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），否则可能遭遇性能下降或连接失败  
- **文件接口配额**：总文件数上限 10,000 个，总大小上限 100 GB；单文件上传限制因用途而异：`file-extract`（150 MB）、`batch`（500 MB）、`fine-tune`（300 MB）  
- **Batch 超时约束**：`Batch Chat` 最长等待时间为 3600 秒（1 小时），超时后连接自动断开；`Batch File` 任务最长执行窗口为 `24h`  
- **流式响应兼容性**：`QVQ` 模型仅支持[流式输出](../concepts/streaming-output.md)，非流式调用将失败；`Responses API` 的 `stream_options={"include_usage": True}` 仅在流式调用中生效

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


