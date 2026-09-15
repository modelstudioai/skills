# [knowledge](../api/knowledge.md) base

知识库（Knowledge Base）是百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）能力核心组件，支持将私有文档注入大模型上下文，实现基于自有数据的精准问答与推理。它通过向量化存储、语义检索与提示工程协同工作，适用于客服知识问答、内部文档助手、合规审查等场景。开发者可通过控制台或 API 快速接入，无需自行搭建向量数据库或微调模型。

## 支持的模型与功能

- **模型支持**：当前知识库检索与问答功能默认绑定 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型；其他模型暂不支持直接启用知识库增强（详见 [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md)）。  
- **核心功能**：包括文档上传与解析（PDF/Word/Excel/TXT/Markdown）、自动分块与向量化、语义检索（支持关键词+向量混合检索）、多轮对话上下文感知问答、以及结果溯源（返回匹配原文片段）。  
- **高级能力**：支持定时数据同步（[知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)）、自定义检索策略（如 top_k、score_threshold）、以及细粒度权限控制（按知识库实例隔离）。

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `top_k` | integer | `3` | 检索返回的最相关文档片段数，取值范围 1–10 |
| `score_threshold` | float | `0.3` | 向量相似度阈值（余弦相似度），低于此值的片段被过滤；设为 `0` 表示关闭阈值过滤 |
| `enable_hybrid_search` | boolean | `true` | 是否启用关键词+向量混合检索；设为 `false` 则仅使用向量检索 |
| `retrieval_mode` | string | `"auto"` | 可选 `"auto"` / `"vector_only"` / `"keyword_only"`；注意 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md) 中部分旧版 SDK 仍默认 `vector_only`，需显式覆盖 |

> **注意**：`retrieval_mode=auto` 在 v2.3.0+ 版本生效，v2.2.x 及更早版本中该参数无效，实际行为等同于 `vector_only` —— 请确认 SDK 版本兼容性，详见 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 使用方式

1. **控制台快速启动**：进入「知识库」模块 → 创建新知识库 → 上传文件 → 等待状态变为 `active`（通常 1–5 分钟）→ 在「测试问答」面板输入问题验证效果。  
2. **API 集成**：调用 `/v1/knowledge_bases/{kb_id}/query` 接口，请求体需包含 `query` 字段及可选参数（如 `top_k`, `score_threshold`）；完整字段定义与错误码见 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
3. **嵌入应用**：推荐使用 `BailianSDK` 的 `KnowledgeBaseClient` 类封装调用逻辑，支持自动重试、超时控制与日志透传；初始化时需传入 `kb_id` 与 `access_token`。

## 限制和注意事项

- **文档限制**：单文件最大 100 MB；总知识库容量上限由配额决定（免费版 1 GB，企业版按合同配置），详见 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **格式支持**：PDF 解析依赖文本层提取，扫描版 PDF（无 OCR）无法处理；Excel 仅支持 `.xlsx`，且仅读取首 Sheet。  
- **安全与合规**：所有文档内容在向量化前经脱敏预处理（移除文件元数据、隐藏属性）；但用户需自行确保上传内容不包含敏感信息，平台不提供运行时内容审计。  
- **调试建议**：若检索结果不理想，优先检查分块策略（默认 512 token + 128 重叠）与 `score_threshold` 设置，并参考 [知识库效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) 中的常见调优路径。

## 来源文档

- [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md)


