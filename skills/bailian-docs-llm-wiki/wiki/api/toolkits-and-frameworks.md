# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、向量嵌入、批量处理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移，无需重写业务逻辑。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatibility.md)按能力维度划分如下：

- **基础对话（Chat Completions）**：支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen-coder-turbo-latest` 等主流文本模型，以及 `qwen-vl-plus`、`qwen3-vl-plus`、`qwen-vl-ocr` 等视觉模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **增强智能体（Responses API）**：专为 Agent 场景设计，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3.8-omni-flash` 处理音视频输入，并简化上下文管理 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；  
- **文件处理（Files API）**：用于上传文档供 `Qwen-Long` 和 `Qwen-Doc-Turbo` 进行问答与提取，或作为 Batch 任务输入，支持 `purpose="file-extract"`（最大 150 MB）、`"batch"`（最大 500 MB）和 `"fine-tune"`（最大 300 MB）三类用途 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)；  
- **向量嵌入（Embeddings）**：支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等多版本模型，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）；多模态 Embedding 模型（如 `qwen3-vl-embedding`）**不兼容 OpenAI 接口**，须使用 DashScope 原生接口 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)；  
- **批量推理（Batch Chat / Batch File）**：提供同步式 Batch Chat（单请求）与异步式 Batch File（JSONL 文件输入），成本降低 50%，支持 256K 上下文 Token，适用于数据标注、模型评测等非实时场景 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)；  
- **会话管理（Conversations API）**：配合 Responses API 实现跨设备上下文延续，支持创建、查询、更新、删除会话及追加消息项，避免手动维护消息历史 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)；  
- **补全（Completions）**：专为代码补全设计，当前**仅限华北2（北京）地域**，且仅支持 `qwen-coder-turbo-latest` 模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

> **注意**：文档 1 与文档 2 均提及旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/...` 已停用，但文档 2 明确指出 Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，而文档 9 中 Conversations API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 仅标注“即将停止维护”。实际开发中应统一迁移到新版 `/compatible-mode/v1/...` 路径，以确保长期可用性。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatibility.md)共用以下核心参数：

- `base_url`：必须替换为业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，其中 `{WorkspaceId}` 需从控制台获取；旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但**性能与稳定性较低**，强烈建议迁移 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- `api_key`：按地域绑定，**北京地域 API Key 无法调用弗吉尼亚 endpoint**，否则返回 `invalid_api_key` 错误（非密钥失效）；  
- `model`：必须使用文档明确列出的支持型号，例如 `qwen3.8-max`、`text-embedding-v4`、`qwen3-vl-plus`；`qwen-audio` 明确不支持 OpenAI 协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- `stream` 与 `stream_options`：流式调用时，`stream_options={"include_usage": true}` 可在最后一 chunk 返回 token 使用统计；  
- `enable_thinking`：仅 Batch 场景下生效，用于显式开关思考模式（默认开启），影响 token 计费，须作为 JSONL 请求体顶层参数传入，不可置于 `extra_body` 内；  
- `dimensions`：仅 `text-embedding-v3` 及 `v4` 支持，用于指定向量维度；  
- `previous_response_id`（Responses API）：用于多轮对话，**必须传入上一轮响应的顶层 `id`（`resp_xxx`）**，而非 `output` 数组内消息的 `id`（`msg_xxx`）。

## 使用方式

### 初始化客户端（通用）

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 推荐环境变量配置
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```

### 各接口典型调用

| 接口类型         | 方法调用示例                                                                 | 说明 |
|------------------|------------------------------------------------------------------------------|------|
| Chat Completions | `client.chat.completions.create(model="qwen3.8-max", messages=[...])`       | 支持 `function_call`、流式、`system` 角色等完整 OpenAI 功能 |
| Responses API    | `client.responses.create(model="qwen3.8-max", input="你好")`                | 输入可为字符串或消息数组；多轮需传 `previous_response_id` |
| Files API        | `client.files.create(file=Path("doc.pdf"), purpose="file-extract")`         | 返回 `file_id`，后续在 Qwen-Long 或 Batch 中引用 |
| Embeddings       | `client.embeddings.create(model="text-embedding-v4", input="hello", dimensions=1024)` | `encoding_format="float"` 为默认值 |
| Batch Chat       | `client.chat.completions.create(...)` + `base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"` | 同步等待，超时上限 3600 秒 |
| Batch File       | `client.files.create(..., purpose="batch")` → `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")` | 异步处理，结果通过 `output_file_id` 下载 |
| Conversations    | `client.conversations.create(items=[{"role":"system","content":"..."}])`     | 创建会话后，其 `id` 可用于后续 `responses.create(..., conversation_id=...)` |

### LangChain 集成

- **OpenAI 兼容层**（`langchain_openai`）：仅支持部分模型（如 `qwen-plus`），依赖 `base_url` 和标准 OpenAI 参数；  
- **DashScope 原生层**（`langchain-community`）：支持全部百炼模型（含部署模型），需使用 `ChatTongyi` 或 `ChatAlibabaTongyi` 类，参数前缀为 `dashscope_api_key` 或 `alibabaApiKey` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域强绑定**：API Key 与 `base_url` 所属地域必须一致，跨地域调用必然失败（HTTP 401 + `invalid_api_key`），且错误信息易被误判为密钥失效；  
- **模型能力差异**：非阿里云直供模型（如三方 DeepSeek、Kimi）在 Responses API 中**Agent 能力受限**，仅支持基础文本生成；  
- **文件配额**：文件存储空间上限为 **10,000 个文件** 或 **100 GB 总大小**，任一达到即拒绝新上传；  
- **Batch 超时**：Batch Chat 最长等待 3600 秒（1 小时），Batch File 任务最长执行 24 小时（`completion_window="24h"`）；  
- **Vision 模型限制**：`QVQ` 模型**仅支持[流式输出](../concepts/streaming.md)**，非流式调用将失败；  
- **Completions 接口地域限制**：文档 5 明确声明该接口**仅适用于华北2（北京）地域**，其他地域调用将报错；  
- **Embeddings 稀疏向量**：[OpenAI 兼容接口](../concepts/openai-compatibility.md)**完全不支持 `output_type=sparse`**，若需稀疏向量，必须切换至 DashScope 原生接口；  
- **测试模型（batch-test-model）**：仅用于链路验证，有严格限制：文件 ≤1 MB、行数 ≤100、并发 ≤2，且不产生费用。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


