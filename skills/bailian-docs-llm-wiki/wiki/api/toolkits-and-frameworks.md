# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)及配套工具链，支持开发者无缝迁移现有应用。核心能力覆盖文本生成（Chat/Completions/Responses）、多模态理解（Vision）、向量化（Embedding）、批量处理（Batch）、文件管理（Files）以及会话状态管理（Conversations），并可通过 LangChain 等主流框架快速集成。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)按场景划分为以下几类：

- **Chat 接口**：兼容 `chat/completions` 标准路径，支持 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.3`、`kimi-k3` 等数十种文本与第三方模型；视觉模型如 `qwen3-vl-plus`、`qwen-vl-ocr` 也通过该接口实现图文理解 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Completions 接口**：专用于代码补全与 FIM（Fill-in-the-Middle）任务，当前仅支持 `qwen-coder-turbo` 模型，不支持后缀生成前缀 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **Responses 接口**：作为 Chat Completions 的演进版，内置联网搜索、网页抓取等智能体原生工具，支持 `qwen3.8-omni-flash` 处理音视频输入，并提供更简洁的字符串输入方式 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Vision 接口**：支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型，兼容 `image_url` 类型消息，QVQ 模型强制要求[流式输出](../concepts/streaming-output.md) [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding 接口**：支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等向量模型，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Batch 接口**：含 Batch Chat（单请求同步等待）和 Batch File（JSONL 文件[异步处理](../concepts/asynchronous-processing.md)），适用于数据标注、评测等非实时场景，成本降低 50%；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  
- **Files 接口**：支持 `file-extract`（文档问答）、`batch`（批量任务输入）、`fine-tune`（调优数据集）三类用途，文件大小限制因用途而异（150 MB / 500 MB / 300 MB）[OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Conversations 接口**：用于跨设备/长时间对话的状态持久化，配合 Responses API 实现上下文自动注入，旧版路径 `/api/v2/apps/protocols/...` 已废弃 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：文档 2（completions 接口）明确说明“本文档仅适用于华北2（北京）地域”，但文档 1、3、4、8、10 均指出北京、新加坡、弗吉尼亚、东京、法兰克福、香港等多地域均支持对应接口，且均要求使用地域绑定的 API Key 和 WorkspaceId 域名。该矛盾表明 completions 接口存在地域支持范围过时问题，实际部署应以最新控制台支持列表为准。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)共用以下核心参数：

- `base_url`：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（如 `https://dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- `api_key`：严格按地域绑定，北京地域 API Key 不可用于调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- `model`：需从各接口支持的模型列表中选择，例如 Responses 接口明确列出 `qwen3.8-omni-flash`，而 Completions 接口仅支持 `qwen-coder-turbo`。  
- `stream` 与 `stream_options`：[流式输出](../concepts/streaming-output.md)通用参数，`stream_options={"include_usage": true}` 可在最后一 chunk 返回 token 统计。  
- `enable_thinking`：Batch 场景下控制思考模式开关（`true`/`false`），默认开启，须作为 JSONL 请求体顶层参数与 `model` 同级传入，不可置于 `extra_body` 中 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  
- `previous_response_id`：Responses 接口多轮对话的关键参数，必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id` [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 使用方式

### SDK 调用（推荐）
- **Python**：安装 `openai>=1.0.0` 或 `langchain_openai`，配置 `base_url` 与环境变量 `DASHSCOPE_API_KEY`：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  # Chat 示例
  client.chat.completions.create(model="qwen3.8-max", messages=[{"role":"user","content":"你好"}])
  # Responses 示例
  client.responses.create(model="qwen3.8-max", input="你能做些什么？")
  # Files 示例
  client.files.create(file=Path("doc.pdf"), purpose="file-extract")
  ```
- **LangChain 集成**：`langchain_openai.ChatOpenAI` 仅支持部分模型（如 `qwen-plus`），而 `langchain_community.chat_models.tongyi.ChatTongyi` 支持全部百炼文本模型 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

### HTTP 调用
- 所有接口均支持标准 RESTful 请求，`Authorization: Bearer $DASHSCOPE_API_KEY` 头部认证，`Content-Type: application/json`。
- Batch File 接口需先上传 JSONL 文件（`purpose="batch"`），再调用 `/batches` 创建异步任务，轮询 `status` 直至 `completed` 后下载 `output_file_id` [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

## 限制和注意事项

- **地域与密钥强绑定**：API Key 必须与 `base_url` 所属地域一致，跨地域调用将被鉴权拒绝，错误码为 `invalid_api_key`，非密钥失效 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **模型能力差异**：非阿里云直供模型（如三方 DeepSeek、Kimi）在 Responses 接口中仅支持基础兼容，Agent 能力（内置工具）受限 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **功能缺失声明**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`completions` 接口暂不支持“通过后缀生成前缀” [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)、[completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **文件配额限制**：百炼存储空间上限为 10,000 个文件、总大小 100 GB，超限后新上传失败，需手动清理 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **超时与重试**：Batch Chat 默认超时 3600 秒（1 小时），需在 SDK 客户端显式设置 `timeout` 参数（如 Python 的 `with_options(timeout=1800.0)`）；HTTP 调用需自行处理连接超时 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


