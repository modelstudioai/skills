# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与框架集成能力，覆盖文本生成、多模态理解、向量嵌入、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI 生态代码（如 SDK、LangChain），仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移。所有接口均支持标准 OpenAI 请求/响应格式，并针对百炼模型特性进行了功能增强与性能优化。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)按功能划分为多个类别，各接口支持的模型范围存在差异：

- **Chat Completions 接口**：支持 Qwen 系列（`qwen3.8-max`、`qwen3.7-plus` 等）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及第三方直供模型（DeepSeek、Kimi、GLM、MiniMax）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Responses API**（智能体原生接口）：聚焦 Agent 能力，支持 `qwen3.8-max`、`qwen3.8-omni-flash` 等最新模型，并内置联网搜索、网页抓取、代码解释器等工具；但非阿里云直供模型仅支持基础兼容能力，Agent 功能受限 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Vision 接口**：专用于多模态理解，支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型，要求输入为 `messages` 数组且含 `image_url` 或 base64 图片 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding 接口**：支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等向量模型，但**不支持稀疏向量输出**（`output_type=sparse` 会被忽略）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Completions 接口**：仅限代码补全场景，当前仅支持 `qwen-coder-turbo` 模型，且**仅适用于华北2（北京）地域** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **Conversations API**：用于跨设备/长时间对话状态管理，与 Responses API 配合使用，自动注入历史上下文 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。  
- **Batch 接口**：分文件批量（`/v1/batches`）和单请求批量（`/v1/chat/completions` + `batch.dashscope.aliyuncs.com`）两类，前者支持 256K 上下文及多模态模型，后者仅支持单请求同步等待 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  

> **注意**：文档 3（completions 接口）明确声明“本文档仅适用于华北2（北京）地域”，而文档 1、2、5、8、9 均推荐使用 `{WorkspaceId}` 专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。但文档 3 的示例 `base_url` 仍为旧版 `https://dashscope.aliyuncs.com`，未体现 WorkspaceId，存在配置不一致风险，实际使用应统一迁移到专属域名。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)共用以下核心参数，部分参数行为有百炼特有约束：

- **`base_url`**：必须替换为对应地域的专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），`{WorkspaceId}` 需从控制台获取。旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **`model`**：必须使用百炼支持的模型名（如 `qwen3.8-max`），不可直接复用 OpenAI 的 `gpt-4o` 等名称。  
- **`api_key`**：严格按地域绑定，北京地域 API Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **`stream` 与 `stream_options`**：流式调用时，`stream_options={"include_usage": true}` 可在最后一 chunk 返回 token 统计，此为百炼扩展字段。  
- **`enable_thinking`**：对 `qwen3.5+` 系列模型，默认开启思考模式（产生额外 reasoning tokens），建议显式设置 `true`/`false` 控制成本 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  
- **`dimensions`**：仅 `text-embedding-v3`/`v4` 支持，用于指定向量维度（如 `1024`），其他 embedding 模型不识别该参数。  

## 使用方式

### 1. 基础调用（SDK）
安装最新版 `openai` SDK 后，初始化客户端时传入 `base_url` 和 `api_key`：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```
- Chat：`client.chat.completions.create(model="qwen3.8-max", messages=[...])`  
- Responses：`client.responses.create(model="qwen3.8-max", input="...")`  
- Embeddings：`client.embeddings.create(model="text-embedding-v4", input="...")`  
- Files：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`  

### 2. LangChain 集成
- **OpenAI 方式**（有限模型支持）：使用 `langchain_openai.ChatOpenAI`，`base_url` 同上，模型名需匹配百炼列表 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  
- **DashScope 原生方式**（全模型支持）：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，需额外安装 `dashscope` 包，`model` 参数可填任意百炼模型名。  

### 3. HTTP 直连
构造标准 OpenAI 格式 JSON 请求，`Authorization` 头携带 `Bearer $DASHSCOPE_API_KEY`，Endpoint 为 `POST {base_url}/chat/completions` 等。  

### 4. 文件与批量任务
- **文件上传**：`purpose` 决定用途（`file-extract` 用于 Qwen-Long/Qwen-Doc-Turbo，`batch` 用于批量推理，`fine-tune` 用于调优）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **批量推理**：  
  - 文件批量：上传 JSONL 到 `/files`（`purpose="batch"`），再调用 `/batches` 创建任务；  
  - 单请求批量：将 `base_url` 改为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，其余参数不变，服务端异步处理后同步返回结果 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  

## 限制和注意事项

- **地域与密钥强绑定**：API Key 必须与 `base_url` 所属地域一致，跨地域调用必失败（HTTP 401），错误码为 `invalid_api_key`，非密钥失效 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **模型能力差异**：  
  - `Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；  
  - `qwen3.8-omni-flash` 在 Responses API 中支持 Session 缓存，但在 Chat Completions 中无此特性；  
  - `QVQ` 模型仅支持[流式输出](../concepts/streaming-output.md)，非流式调用将失败。  
- **路径与域名迁移**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 等旧路径已停止维护，必须迁移到 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **文件配额**：百炼文件存储上限为 10,000 个文件或 100 GB 总大小，超限后上传失败，需手动清理 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Embedding 特殊限制**：OpenAI 兼容接口不支持 `output_type=sparse`，传入该参数将导致 embedding 字段为空（HTTP 200 但无向量数据）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


