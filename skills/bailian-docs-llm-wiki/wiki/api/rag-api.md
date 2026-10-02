# rag api

RAG API 是百炼平台提供的知识增强型推理服务接口，支持将私有知识库与大模型能力结合，实现精准的[检索增强生成](../concepts/rag.md)。开发者可通过该 API 构建问答、摘要、文档分析等场景应用。所有接口均需通过 API Key 认证，并遵循统一的限流与错误处理规范。

## 支持的模型与功能

RAG API 本身不直接暴露模型选择参数，其底层调用由关联的 Agent 或知识检索配置决定；具体可用模型取决于所绑定的 [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md) 中指定的基础模型。核心功能包括：知识库生命周期管理（创建/删除/更新）、文档上传与解析、语义切片（chunking）控制、异步同步任务调度，以及实时检索增强问答。其中，检索与生成逻辑封装在 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 接口中，支持流式响应和上下文长度控制。

## 关键参数

- `knowledge_base_id`（必填）：目标知识库唯一标识，需提前通过 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md) 接口创建  
- `query`（必填）：用户自然语言查询文本  
- `top_k`（可选，默认 3）：返回最相关切片数量，影响召回精度与延迟  
- `stream`（布尔，默认 false）：启用流式响应时设为 `true`，适用于长回答场景  
- `agent_id`（可选）：若使用 Agent 封装流程，需显式传入，否则默认走基础 RAG 流程  

> **注意**：部分旧版文档中提及 `model` 字段可直接传入模型名，但根据最新 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 规范，该字段已废弃，模型由 `agent_id` 间接指定，直接传入将被忽略。

## 使用方式

1. 创建知识库：调用 `POST /v1/knowledge_bases`，获取 `knowledge_base_id`  
2. 上传文档：使用 `POST /v1/knowledge_bases/{kb_id}/documents` 提交文件或 URL  
3. 触发同步：通过 `POST /v1/knowledge_bases/{kb_id}/sync` 启动解析与切片（或等待自动同步）  
4. 发起问答：向 `POST /v1/knowledge` 提交查询，携带 `knowledge_base_id` 和 `query`  

完整请求示例见 [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md) 中的快速开始章节。

## 限制和注意事项

- 单次请求最大 `query` 长度为 2048 字符；知识库中文档总大小上限为 10 GB（含原始文件与切片索引）  
- 同步任务最长超时时间为 30 分钟，超时后状态置为 `failed`，需检查 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md) 日志  
- 所有接口均受 [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md) 约束，默认配额为 60 次/分钟（按 API Key 统计）  
- 切片内容不可直接修改，如需更新，须重新上传文档并触发同步——详见 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md) 说明

## 来源文档

- [RAG](../../raw/application-api-reference/rag-api.md)


