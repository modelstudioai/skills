# rag api

RAG API 是百炼平台提供的[检索增强生成](../concepts/rag.md)（Retrieval-Augmented Generation）能力接口，支持将私有知识库与大模型推理深度集成，实现基于上下文的精准问答与内容生成。该 API 以 RESTful 形式提供，覆盖知识入库、切片管理、异步同步、检索调用等全链路能力。开发者需通过标准认证方式访问，并遵守平台限流与配额策略。

## 支持的模型/功能

- 支持与百炼平台托管的多种大语言模型（如 Qwen 系列、Qwen2 系列）协同工作，具体兼容模型列表见 [RAG](../../raw/application-api-reference/rag-api.md) 文档首页的“模型支持”章节（实际内容位于子页面 `rag-api-overview.md`）。
- 核心功能包括：知识库生命周期管理、文档上传与解析、自动切片（chunking）、向量化索引构建、同步任务调度，以及面向终端用户的 `knowledge` 检索问答接口。
- Agent 相关能力（如多跳检索、工具调用编排）已整合进 RAG API，但需注意其依赖独立的 [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md) 接口配置；> **注意**：`rag-api-agents.md` 中描述的 `agent_id` 绑定逻辑与 `knowledge.md` 中的 `agent_mode` 参数行为存在不一致，建议优先以 `knowledge.md` 的 `agent_mode=true` 调用为准，该模式下无需显式传入 `agent_id`。

## 关键参数

- `knowledge_id`：必填，标识目标知识库，需通过 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md) 接口创建后获取。
- `query`：检索请求中的用户问题文本，长度限制为 2048 字符。
- `top_k`：控制返回最相关切片数量，默认为 3，取值范围 1–10。
- `enable_rerank`：布尔值，启用重排序可提升相关性，但增加延迟；默认 `false`，详见 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)。
- `stream`：仅在 `/v1/knowledge/query` 接口生效，设为 `true` 时返回 SSE 流式响应。

## 使用方式

1. **前置准备**：调用 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md) 创建知识库 → 上传文档至 [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md) → 触发 [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md) 完成切片与向量化。
2. **发起检索**：对已就绪的知识库，向 `POST /v1/knowledge/query` 发送请求，携带 `knowledge_id` 和 `query`。
3. **认证**：使用 Bearer [Token](../concepts/token.md) 认证，[Token](../concepts/token.md) 需通过 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md) 获取，不支持 API Key 直接调用。

## 限制和注意事项

- 单次请求最大响应体为 8MB；若 `stream=true`，单条 SSE event payload 不得超过 1MB。
- 知识库内单个文档原始大小上限为 50MB（PDF/Word 等格式），超限将被截断并返回警告；该限制在 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md) 页面明确说明。
- 同步任务（sync job）最长执行时间为 30 分钟，超时后状态置为 `failed`，需检查 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md) 中的错误日志。
- > **注意**：[限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md) 中标注的“每秒 5 QPS”为账户级全局限流，但实测中 `/v1/knowledge/query` 接口受更严格的路径级限流（2 QPS），请以 `rag-api-rate-limits.md` 的“接口粒度”表格为准。

## 来源文档

- [RAG](../../raw/application-api-reference/rag-api.md)


