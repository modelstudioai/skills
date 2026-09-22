# rag api

RAG API 是百炼平台提供的[检索增强生成](../concepts/rag.md)服务接口，支持开发者将自有知识库接入大模型应用，实现基于私有数据的精准问答与内容生成。该 API 提供知识库管理、文档处理、向量切片、同步任务及检索问答等完整能力链路，适用于构建智能客服、企业知识助手等场景。所有请求需通过标准 HTTP 接口调用，并遵循统一的认证与限流机制。

## 支持的模型/功能

- 支持的知识库类型包括结构化数据（如数据库表）和非结构化文档（PDF、Word、TXT 等），具体格式与预处理规则详见 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md) 和 [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md) 文档。
- 检索与问答能力基于百炼内置的多模态嵌入模型（默认 `text-embedding-v3`）和 LLM（默认 `qwen-max`），支持自定义 embedding 模型与 LLM，配置方式见 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)。
- > **注意**：原始文档中 [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md) 提到“Agent 可直接绑定 RAG 知识源”，但当前 API 实际不支持运行时动态切换知识库 ID；该能力尚在灰度阶段，生产环境请以 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 中的 `knowledge_base_id` 显式传参为准。

## 关键参数

- `knowledge_base_id`（必填）：目标知识库唯一标识，需提前通过 `/v1/knowledge_bases` 创建并获取。
- `query`（必填）：用户自然语言问题，长度上限 2048 字符。
- `top_k`（可选，默认 3）：返回最相关切片数量，取值范围 1–10。
- `enable_rerank`（可选，默认 false）：启用重排序（cross-encoder），显著提升相关性但增加延迟。
- 其他高级参数（如 `filter`, `chunk_size`, `rerank_model`）详见 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)。

## 使用方式

1. 使用 API Key 进行 Bearer [Token](../concepts/token.md) 认证，参考 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)；
2. 向 `POST /v1/knowledge_bases/{kb_id}/retrieve_and_answer` 发起请求（检索+生成一体化）或 `POST /v1/knowledge_bases/{kb_id}/retrieve`（仅检索）；
3. 响应包含 `retrieved_chunks`（原始切片列表）和 `answer`（LLM 生成结果），结构与错误处理逻辑见 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 限制和注意事项

- 单次请求最大响应时间 60 秒；超时将返回 `504 Gateway Timeout`；
- 知识库内单文档大小上限 100 MB，切片后总 chunk 数建议不超过 100 万（[切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)）；
- 同步任务（如文档解析、向量化）受 [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md) 约束，高频提交可能触发 `429 Too Many Requests`；
- > **注意**：[数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md) 文档中提及“支持 CSV 直接映射字段”，但实际仅支持 CSV 作为纯文本导入（字段映射功能尚未上线），请优先使用 JSONL 或结构化 API 导入。

## 来源文档

- [RAG](../../raw/application-api-reference/rag-api.md)


