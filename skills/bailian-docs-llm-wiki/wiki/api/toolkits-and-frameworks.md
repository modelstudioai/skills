# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)工具包与框架，覆盖文本生成、多模态理解、向量化、批量推理、对话状态管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和 `model` 参数即可快速迁移。所有接口均支持标准 OpenAI Python/Node.js/Java/Go SDK 及 HTTP 调用。

## 支持的模型/功能

- **文本生成**：`qwen4-max`、`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 文本模型；DeepSeek（硅基流动/快手万擎直供）、Kimi（月之暗面直供）、GLM、MiniMax 等三方模型（仅限华北2北京地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，支持图像/视频/文档输入与结构化输出 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)  
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash`，支持多语种及可选维度（如 `dimensions=1024`）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)  
- **批量处理**：`batch-test-model`（链路验证）、`qwen-long`（长文档问答）、`qwen3.5-omni-plus`（全模态批处理），支持单请求同步返回或 JSONL 文件异步提交 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)  
- **对话增强**：`Conversations API`（会话生命周期管理）、`Responses API`（内置工具调用、自动上下文注入、`previous_response_id` 多轮关联）  

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，与文档 5 和文档 6 的描述一致，但需注意其能力边界。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，业务空间专属域名（推荐）或通用域名 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（推荐）<br>`https://dashscope.aliyuncs.com/compatible-mode/v1`（兼容） |
| `api_key` | 必填，**严格按地域绑定**：北京 Key 不能调用弗吉尼亚 endpoint | `sk-xxx`（需从对应地域控制台获取） |
| `model` | 必填，模型名称需与所选接口能力匹配 | `qwen4-max`（Chat）、`qwen3-vl-plus`（Vision）、`text-embedding-v4`（Embedding） |
| `stream` | 可选，流式响应开关（`True`/`False`） | `True`（需配合 `stream_options={"include_usage": True}` 获取 token 统计） |
| `enable_thinking` | 可选，混合思考模型（如 `qwen3.8-max`）显式控制思考模式 | `false`（关闭以降低 token 成本） |
| `previous_response_id` | Responses API 专用，用于多轮上下文关联 | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"`（上一轮响应顶层 `id`） |

> **注意**：`enable_thinking` 必须作为 JSONL 请求体中 `body` 的顶层字段（与 `model` 同级），若误置于 `extra_body` 中将被忽略——该约束在 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 中均被强调，具有一致性。

## 使用方式

### 1. 初始化客户端（统一范式）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 推荐环境变量配置
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)
```

### 2. 按场景调用
- **Chat Completions**（标准对话）：`client.chat.completions.create(model="qwen-plus", messages=[...])`  
- **Responses API**（智能体原生）：`client.responses.create(model="qwen4-max", input="你好")`  
- **Embeddings**：`client.embeddings.create(model="text-embedding-v4", input="文本", dimensions=1024)`  
- **Files**（文档上传）：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`  
- **Batch**（文件异步）：`client.batches.create(input_file_id="file-batch-xxx", endpoint="/v1/chat/completions")`  
- **Conversations**（会话管理）：`client.conversations.create(items=[{"role":"system","content":"..."}])`  

### 3. LangChain 集成
- **OpenAI 兼容层**（部分模型）：使用 `langchain_openai.ChatOpenAI`，`base_url` 指向百炼兼容地址  
- **DashScope 原生层**（全模型支持）：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，需安装 `dashscope` 包 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)  

## 限制和注意事项

- **地域强绑定**：API Key 与 `base_url` 所属地域必须一致，跨地域调用返回 `invalid_api_key`（HTTP 401），非密钥失效 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **域名迁移**：华北2（北京）、新加坡、中国香港地域已启用业务空间专属域名（`{WorkspaceId}.xxx.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，**强烈建议迁移**  
- **文件服务配额**：总文件数 ≤ 10,000 个，总大小 ≤ 100 GB；单文件上限因用途而异：`file-extract`（150 MB）、`batch`（500 MB）、`fine-tune`（300 MB）  
- **Batch 超时**：同步 Batch Chat 最长等待 3600 秒（1 小时），需在 SDK 客户端显式设置 `timeout` 参数（如 Python 的 `.with_options(timeout=1800.0)`）  
- **Embedding 稀疏向量**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 `output_type=sparse`，传入该参数将导致 embedding 字段为空（HTTP 200）  
- **三方模型地域限制**：DeepSeek/Kimi/GLM/MiniMax 等直供模型仅在中国站华北2（北京）地域可用，且需在控制台单独开通服务

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


