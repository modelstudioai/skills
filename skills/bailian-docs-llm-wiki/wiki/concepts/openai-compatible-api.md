# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 RESTful API，严格遵循 OpenAI 官方 API 协议规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/responses` 等），使开发者能**零代码改造**复用现有 OpenAI SDK、LangChain 集成、CLI 工具或框架（如 Cursor、Dify、Cherry Studio），仅需替换 `base_url` 和 `api_key` 即可快速接入百炼的 Qwen 及第三方模型服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用迁移**：已有 OpenAI 应用（如基于 `openai>=1.0` 的 Python 项目）可直接切换 `client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", api_key="sk-xxx")`，无需修改 `chat.completions.create()` 调用逻辑，即支持 `qwen3.8-max`、`deepseek-v4-pro`、`glm-5.2` 等全部兼容模型。  
- **多模态开发**：通过标准 `chat/completions` 接口传入含 `image_url` 或 `image_data` 的 `content` 数组，即可调用 `qwen-vl-plus`、`qwen3-vl-plus` 等视觉模型，完全兼容 OpenAI Vision 规范。  
- **智能体与工具链**：使用 `/v1/responses` 接口（OpenAI 兼容的 Responses 协议），可声明 `tools: [{"type": "web_search"}]` 并自动触发联网搜索、代码解释、文件检索等内置能力，同时支持 `previous_response_id` 实现多轮上下文自动管理。  
- **嵌入与批量处理**：`/v1/embeddings` 接口兼容 `text-embedding-v4`、`qwen3.7-text-embedding`；`/v1/batch`（同步批量）和 `/v1/chat/completions`（流式+批量混合）均支持 OpenAI 协议语义，适用于 RAG 向量构建或高并发推理。  
- **应用集成**：已发布的百炼应用可通过 OpenAI 兼容的 `/v1/chat/completions` 端点调用（`model` 参数填应用 ID），复用[函数调用](function-calling.md)（`function_call`）、RAG 增强、会话状态等能力，与原生 `/api/v1/applications/{app_id}/call` 接口语义一致。

> ⚠️ 注意：Qwen-Audio、QwQ、多模态 Embedding（如 `qwen3-vl-embedding`）**不支持** OpenAI 兼容协议，必须使用 DashScope 原生接口。

## 关键参数和配置

| 参数 | 说明 | 必填 | 示例值 | 注意事项 |
|------|------|------|--------|----------|
| `base_url` | 必须使用地域专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` | 是 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 需从控制台获取；旧域名 `dashscope.aliyuncs.com` 性能较低，不推荐；**API Key 与地域必须严格匹配**（北京 Key 不可调用弗吉尼亚 endpoint） |
| `api_key` | 百炼平台生成的 API Key，按计费方案隔离（[Token](token.md) Plan / Coding Plan / 按量计费） | 是 | `sk-xxx` | [Token](token.md) Plan 个人版 Key 无法用于 Dify；按量计费 Key 必须带 `WorkspaceId` |
| `model` | 模型 ID，需从各接口支持列表中选择 | 是 | `"qwen3.8-max"`、`"qwen-vl-plus"`、`"text-embedding-v4"` | `responses` 接口仅支持特定模型（如 `qwen3.8-max`）；`completions` 接口仅支持 `qwen-coder-turbo` 等代码模型；命名需规范（如 `kimi-k2.6` → `kimi-k2-6`） |
| `stream` | 是否启用流式响应（SSE） | 否 | `true` | 流式响应末尾默认不返回 token 统计，需显式添加 `stream_options={"include_usage": true}` |
| `enable_thinking` | Qwen3 系列专属参数，顶层字段（与 `model` 同级），用于显式开启深度思考模式 | 否 | `true` | 若未设置且模型支持，可能隐式触发思考导致延迟与成本增加；部分客户端（如 `qwen-code`）需在 `extra_body` 中透传 |
| `tools` / `tool_choice` | 仅 `/v1/responses` 和 `/v1/chat/completions` 支持 | 否 | `[{"type": "web_search"}]`, `"auto"` | `responses` 接口支持快捷工具声明（`{"type": "web_search"}`），无需完整 schema；`chat/completions` 需完整 `function` 定义 |

## 面向开发者，简洁实用

- ✅ **快速上手**：安装 `openai` SDK（Python）或 `@anthropic-ai/sdk`（Node.js），初始化时指定 `base_url` 和 `api_key`，其余代码 100% 复用。  
- ✅ **调试友好**：所有请求支持标准 cURL 直调，Header 带 `Authorization: Bearer <api_key>`，Body 为纯 JSON，无额外封装。  
- ✅ **生产就绪**：支持流式、批量、多模态、工具调用、结构化输出（JSON Schema）、显式缓存（`cache_control`）等企业级特性。  
- ❌ **避坑提示**：  
  - 切勿混用地域——`base_url` 地域 ≠ `api_key` 所属地域 → `invalid_api_key`；  
  - `qwen-audio`、`qwq`、`qwen3-vl-embedding` 等模型**不在此协议支持范围内**；  
  - `system` message 在 `qwen3-vl-plus` 中有效，在 `qvq` 中无效，请查阅具体模型文档。  

> 提示：使用 LangChain？优先选用 `langchain_community.chat_models.alibaba_tongyi`（全功能支持），而非 `langchain_openai`（部分高级特性受限）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


