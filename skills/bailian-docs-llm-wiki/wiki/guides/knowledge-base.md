# knowledge base

百炼平台的 knowledge base 是面向企业级场景的 RAG（检索增强生成）服务，支持私有文档的自动解析、切片、向量化与索引构建，并提供多路召回检索与流式大模型问答能力。开发者可通过控制台或 API 快速接入，将结构化/非结构化数据转化为可调用的知识服务。该能力深度集成于百炼模型生态，适用于客服、内部知识助手、合规审查等高精度垂域场景。

## 支持的模型与功能

- **默认模型**：知识检索与问答默认使用 `qwen-max` 或 `qwen-plus`（具体以控制台配置为准），支持通过 `model_id` 参数显式指定其他已授权的大模型；  
- **核心功能**：包括文档自动解析（PDF/Word/Excel/TXT/Markdown 等）、语义切片（支持按段落、标题、固定 token 长度等策略）、双路向量索引（稠密向量 + 关键词倒排）、多路召回（向量+关键词+重排序）、Agentic 多轮检索（[RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中明确提及）及流式问答响应；  
- **扩展能力**：支持与 MCP 协议、Skill 编排、自定义 [Prompt 工程](../concepts/prompt-engineering.md)联动，详见 [应用集成](../../raw/application-user-guide/knowledge-base/integration/channels.md)。

## 关键参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `knowledge_id` | string | 知识库唯一标识，创建后由平台分配 | `kb-abc123xyz` |
| `top_k` | int | 检索返回的最相关切片数（单次请求上限为 50） | `5` |
| `retrieval_strategy` | string | 可选 `hybrid`（默认）、`vector_only`、`keyword_only` | `"hybrid"` |
| `stream` | bool | 是否启用流式问答（仅 `rag-knowledge-qa` 接口支持） | `true` |
| `model_id` | string | 显式指定问答所用大模型 ID，需在当前项目中已开通权限 | `"qwen-plus"` |

> **注意**：`top_k` 在 [RAG API 参考](../../raw/application-api-reference/rag-api/rag-api-overview.md) 中定义为最大 50，但部分旧版 SDK 示例中误写为 100，应以 API 文档为准。

## 使用方式

1. **创建知识库**：通过控制台「知识库」→「新建」或调用 `/v1/knowledge_bases` 接口，选择解析策略与切片规则（参考 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)）；  
2. **上传文档**：支持单文件上传或批量导入（OSS/MySQL/表格等），系统自动触发解析与索引构建；  
3. **发起检索或问答**：  
   - 检索：调用 `/v1/knowledge_bases/{kb_id}/retrieve`，传入 query 与 `top_k`；  
   - 问答：调用 `/v1/knowledge_bases/{kb_id}/chat`，启用 `stream=true` 可获得 SSE 流式响应；  
4. **调试验证**：推荐先使用 [Playground](../../raw/application-user-guide/knowledge-base/playground.md) 实时观察检索质量与问答效果，再集成至生产链路。

## 限制和注意事项

- 单个知识库最多支持 100 万切片（chunk），超限后新增文档将被拒绝；  
- PDF 解析不支持加密文档及扫描件 OCR（需预处理为可选中文本）；  
- 向量化延迟：小规模文档（<100 页）通常在 1–3 分钟内完成索引，大规模批量导入建议异步轮询 `status` 字段；  
- 所有 API 调用均受项目级 QPS 与 [Token](../concepts/token.md) 总量配额约束，详情见配额管理页面；  
- > **注意**：[RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中称“支持 MySQL 数据源”，但当前版本仅支持 MySQL 作为元数据存储（非知识内容源），实际数据接入仍需通过文件或 OSS 导入——该描述存在歧义，应以 [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md) 文档为准。

## 来源文档

- [RAG 简介](../../raw/application-user-guide/knowledge-base.md)


