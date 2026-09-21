# rag api

RAG API 是百炼平台提供的知识增强型推理服务接口，支持将私有知识库与大模型能力结合，实现精准的[检索增强生成](../concepts/rag.md)。开发者可通过该 API 构建问答、摘要、知识验证等场景应用。所有接口均需通过 API Key 认证，并遵循统一的限流与错误处理规范。

## 支持的模型与功能

- 当前 RAG API **不直接暴露底层大模型选型**，而是以“知识检索与问答”为统一能力入口，由平台根据知识库配置与查询意图自动调度最优模型（详见 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)）。
- 核心功能包括：知识库生命周期管理、文档上传与解析、语义切片控制、异步同步任务调度、以及基于检索结果的结构化问答响应。
- Agent 管理能力（如多跳推理、工具调用编排）已集成至 RAG 流程中，但需通过 [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md) 接口单独配置，不可在 `/knowledge` 主路径中直接启用。

## 关键参数

- `knowledge_base_id`（必填）：标识目标知识库，需提前通过 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md) 接口创建并获取。
- `query`（必填）：用户自然语言问题，长度 ≤ 2048 字符；过长将被截断且不报错。
- `top_k`（可选，默认 3）：返回最相关切片数量，取值范围 1–10；超出范围将被静默修正为默认值。
- `enable_citation`（可选，默认 false）：设为 `true` 时，响应中包含来源文档 ID 与切片位置信息，便于溯源。

## 使用方式

1. 创建知识库：调用 `POST /v1/knowledge_bases`（参考 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)）  
2. 上传文档：使用 `POST /v1/knowledge_bases/{kb_id}/documents` 提交文件或 URL（见 [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)）  
3. 触发同步：文档上传后需显式调用 `POST /v1/knowledge_bases/{kb_id}/sync` 启动解析与索引（[同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)）  
4. 发起问答：`POST /v1/knowledge`，传入 `knowledge_base_id` 与 `query` 即可获得答案及（可选）引用信息  

> **注意**：部分旧版文档示例中仍展示 `/v1/rag/query` 路径，该路径已于 v2.3 版本废弃；请统一使用 `/v1/knowledge`（参见 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)），否则返回 404。

## 限制和注意事项

- 单次请求最大响应体为 8 MB；若答案过长，系统将截断并返回 `truncated: true` 字段。
- 知识库内单文档大小上限为 100 MB（PDF/Word/Excel），纯文本无此限制；超限文档上传将失败并返回 `400 InvalidDocumentSize`（见 [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)）。
- 切片（chunk）最小粒度为句子级，不可人工指定固定字数切分；自定义切片逻辑需通过 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md) 接口在同步前预设规则，而非请求时传参。
- 所有 API 均受 [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md) 约束，突发流量可能触发 `429 Too Many Requests`；建议客户端实现指数退避重试。

## 来源文档

- [RAG](../../raw/application-api-reference/rag-api.md)


