# knowledge base

百炼平台的 knowledge base 是面向企业级场景的 RAG（[检索增强生成](../concepts/rag.md)）服务，支持私有文档的自动解析、切片、向量化与索引构建，并提供多路召回检索和基于大模型的流式问答能力。开发者可通过控制台或 API 快速接入，将结构化/非结构化数据转化为可调用的知识服务。该能力深度集成于百炼应用层与 API 层，是构建智能客服、内部知识助手等场景的核心基础设施。

## 支持的模型与功能

- **默认模型**：知识检索与问答均默认使用 `qwen-max` 或 `qwen-plus`（具体以控制台当前配置为准），支持通过 `model_id` 参数显式指定其他已开通的百炼大模型（如 `qwen-turbo`）。  
- **核心功能**：包括文档自动解析（PDF/Word/Excel/TXT/Markdown 等）、语义切片（支持按段落、标题、固定 token 长度等策略）、向量索引（默认使用百炼内置向量引擎）、多路召回（关键词 + 向量 + 重排序）、Agentic 多轮检索（[RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中提及）及流式问答响应。  
- **扩展能力**：支持从 OSS、MySQL、表格文件等多种数据源批量导入（参见 [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)），并可通过 Skill 封装为低代码可复用组件。

## 关键参数

- `knowledge_base_id`：知识库唯一标识，创建后由平台分配，必填。  
- `query`：检索或问答请求中的用户输入文本，最大长度 2048 字符。  
- `top_k`：单次检索返回的最相关切片数，默认 3，取值范围 1–50。  
- `enable_rerank`：是否启用重排序（默认 `true`），影响召回精度与延迟。  
- `stream`：问答接口中控制是否流式返回（`true`/`false`），仅对 `/v1/knowledge_bases/{kb_id}/qa` 生效。  
- `retrieval_strategy`：可选 `hybrid`（默认，混合召回）、`vector_only` 或 `keyword_only`，详见 [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)。

## 使用方式

1. **创建知识库**：在控制台选择「知识库」→「新建」，上传文件或配置数据源，设置解析与切片策略（[创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)）；  
2. **等待构建完成**：状态变为 `active` 后即可调用；  
3. **调用 API**：  
   - 检索：`POST /v1/knowledge_bases/{kb_id}/retrieve`  
   - 问答：`POST /v1/knowledge_bases/{kb_id}/qa`  
   接口定义与示例见 [RAG API 参考](../../raw/application-api-reference/rag-api/rag-api-overview.md)；  
4. **调试验证**：使用控制台 [Playground](../../raw/application-user-guide/knowledge-base/playground.md) 实时测试效果。

## 限制和注意事项

- 单个知识库最大支持 100 万切片；单文档解析后切片数上限为 10,000（超限将截断）；  
- PDF 解析不支持加密文档及扫描版图片型 PDF（需 OCR 预处理）；  
- 向量索引更新非实时：新增/删除文档后，需等待约 1–2 分钟生效；  
- > **注意**：[RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中称“上传后自动完成解析、切片、向量化与索引”，但实际切片策略（如是否启用标题感知切分）需在创建知识库时显式配置，未配置则使用平台默认策略——此细节在 [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md) 中明确说明，前者表述易引发误解；  
- > **注意**：[RAG API 参考](../../raw/application-api-reference/rag-api/rag-api-overview.md) 中部分字段（如 `retrieval_strategy` 的枚举值）与最新控制台实际支持存在滞后，建议以 OpenAPI Spec 返回的 `enum` 值为准；  
- 跨区域知识库调用需确保 API Endpoint 与知识库所在地域一致，否则返回 `404`。

## 来源文档

- [RAG 简介](../../raw/application-user-guide/knowledge-base.md)


