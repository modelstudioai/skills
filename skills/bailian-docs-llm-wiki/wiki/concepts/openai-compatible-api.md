# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 API 协议，完全遵循 OpenAI REST API 的请求/响应格式（包括路径、HTTP 方法、JSON 结构、字段命名与语义），使开发者能直接复用 OpenAI SDK（如 `openai==1.0+`）、现有代码库或第三方工具链，零改造接入百炼的千问系列及主流第三方模型能力。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一 API，而是一组按能力分层的协议实现，覆盖模型调用、向量计算、重排序、文件处理与应用编排等核心场景：

- **模型推理**：通过 `/v1/chat/completions`（标准对话）和 `/v1/responses`（增强型响应）两个端点调用文本、多模态（VL 系列）及第三方模型。其中 `responses` 接口内置联网搜索、网页抓取、代码解释器、文搜图、知识库检索等工具，支持自动工具选择与调用闭环。
- **向量化与排序**：提供 `/v1/embeddings`（文本/多模态向量）和 `/v1/reranks`（文本/跨模态重排序）端点，参数结构与 OpenAI 官方一致（如 `input`, `model`, `dimensions`, `query` + `documents`），可直接替换 OpenAI `text-embedding-3-small` 或 `gpt-4o-rerank` 调用。
- **文件操作**：支持 `/v1/files` 上传、列表与删除，配合 `purpose=file-extract` 可触发文档智能解析（PDF/DOCX 结构化提取），为 RAG 流程提供标准化输入。
- **应用集成**：新版智能体（Agent 2.0）与工作流（Workflow）均支持通过 OpenAI 兼容 `responses` 接口同步/异步调用，复用 `messages`、`stream`、`tool_choice` 等字段，并扩展 `memory_id`（[长期记忆](long-term-memory.md)）、`rag_options`（知识库精准检索）等百炼特有能力。
- **框架与工具链**：LlamaIndex、Spring AI Alibaba、Dify、Cursor、Qwen Code 等主流框架与 IDE 插件，仅需配置 `base_url=https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` 和对应 API Key，即可无缝对接，无需修改业务逻辑。

> ⚠️ 注意：Qwen-Audio 模型、QwQ/QVQ 特定行为模型、万相（WanX）文生图/视频模型**不支持 OpenAI 兼容协议**，必须使用 DashScope 原生 API；`qwen-coder` 仅支持 `completions` 接口，不支持 `chat/completions`。

## 关键参数和配置

所有 OpenAI 兼容接口共用以下核心配置，开发者需严格遵循：

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `base_url` | string | 是 | **必须使用业务空间专属域名**，格式为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。旧域名 `dashscope.aliyuncs.com` 已不推荐，性能与稳定性较低。 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | string | 是 | 方案专属密钥：按量计费用 `sk-xxx`，[Token](token.md) Plan 用 `tp-xxx`，**不可混用**。 | `sk-1234567890abcdef` |
| `model` | string | 是 | 模型 ID，必须严格匹配文档支持列表（如 `qwen3.8-max`, `qwen3-vl-plus`, `text-embedding-v4`, `qwen3-rerank`）。三方模型需先在控制台开通权限。 | `qwen3.7-plus` |
| `stream` | boolean | 否 | 是否启用 SSE 流式响应，默认 `false`。流式时客户端需按行解析 `data: {...}` 事件。 | `true` |

**场景特有关键参数**：

- **Chat / Responses**：  
  - `messages`: 标准 `[{"role": "user", "content": "..."}]` 数组；`responses` 还支持 `input_file`、`function_call_output` 等扩展类型。  
  - `previous_response_id`: `responses` 多轮对话必需，传入上一轮响应的顶层 `id`（UUID），用于上下文自动注入。  
  - `enable_thinking`: `qwen3.5+` 系列模型必需显式设置为 `true` 才启用深度思考模式（影响计费与效果）。  

- **Embeddings / Rerank**：  
  - `input`（向量）或 `query` + `documents`（排序）：均为顶层字段，**不嵌套在 `parameters` 或 `input` 对象内**。  
  - `dimensions`: 向量维度（如 `1024`, `2048`），部分模型支持可选配置。  
  - `instruct`: 排序模型任务指令（英文），用于控制语义对齐策略。  

- **Files**：  
  - `purpose`: 文件用途，取值 `file-extract`（解析）、`batch`（批量任务）、`fine-tune`（微调数据集）。  

## 面向开发者，简洁实用

- ✅ **快速迁移**：用 OpenAI Python SDK，仅需两行替换：
  ```python
  from openai import OpenAI
  client = OpenAI(api_key="sk-xxx", base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
  response = client.chat.completions.create(model="qwen3.8-max", messages=[{"role": "user", "content": "你好"}])
  ```

- ✅ **调试建议**：  
  - 首选 `curl` 验证基础连通性：  
    ```bash
    curl -X POST "https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
      -H "Authorization: Bearer sk-xxx" \
      -H "Content-Type: application/json" \
      -d '{"model":"qwen3.8-max","messages":[{"role":"user","content":"你好"}]}'
    ```  
  - 查看响应中的 `x-dashscope-usage` Header 获取实际 token 消耗与模型版本。  

- ✅ **避坑清单**：  
  - 不要将 `enable_thinking` 放在 `extra_body` 中——它必须是请求 JSON 的顶层字段；  
  - `previous_response_id` 必须是上一轮响应的 `id`（非 `output[0].id`）；  
  - `qwen3-rerank` 的 `query` 和 `documents` 是并列顶层字段，而非嵌套在 `input` 下；  
  - [Token](token.md) Plan 用户无法调用多模态模型（Qwen-VL/Omni）或按量计费专属模型（如 WanX），请确认方案权限。  

- 📌 **一句话总结**：OpenAI 兼容接口 = 标准协议 + 百炼能力 + 零迁移成本。用你熟悉的 OpenAI 方式，调用百炼最全、最强、最新的 AI 模型与服务。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [vector and sort](../api/vector-and-sort.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [frameworks](../api/frameworks.md)


