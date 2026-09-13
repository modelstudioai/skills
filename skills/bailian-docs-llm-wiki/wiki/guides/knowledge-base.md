# knowledge base

知识库（Knowledge Base）是百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，支持将私有文档注入模型上下文，实现基于领域知识的精准问答与内容生成。它通过向量检索与大模型协同工作，无需微调即可提升模型在垂直场景下的专业性与准确性。所有功能均通过 API 或控制台统一管理，适用于企业级知识管理、客服助手、内部文档智能查询等场景。

## 支持的模型/功能

- **支持模型**：当前知识库功能默认绑定百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 系统模型；自定义部署的 `Qwen2` 系列模型需确保已启用 RAG 插件并完成向量模型对齐配置。  
- **核心功能**：包括文档上传与解析（支持 PDF/Word/Excel/TXT/Markdown）、自动分块与向量化、多路召回（关键词+向量+重排序）、混合检索（语义+结构化元数据过滤）、以及端到端问答（[知识问答](https://help.aliyun.com/zh/model-studio/rag-knowledge-qa)）。  
- **高级能力**：支持定时数据同步（[知识库定时数据同步指南](https://help.aliyun.com/zh/model-studio/data-sync-guide)）、细粒度权限控制、以及日志追踪与效果分析（[知识库日志与监控](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-log-monitoring)）。  
> **注意**：原始文档中未明确说明是否支持第三方开源模型（如 Llama 3）直接接入知识库 pipeline；实际使用时请以 [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md) 中最新 API 兼容列表为准，避免依赖过时文档描述。

## 关键参数

- `top_k`：控制检索返回的文档片段数量，默认为 3，最大支持 10；过高可能引入噪声，影响生成质量。  
- `score_threshold`：向量相似度阈值（0.0–1.0），低于该值的片段将被过滤；建议初始设为 0.35，结合 [知识库效果优化](https://help.aliyun.com/zh/model-studio/rag-optimization) 中的 A/B 测试方法调优。  
- `enable_hybrid_search`：启用混合检索（默认 `true`），同时触发关键词匹配与向量检索，显著提升长尾 query 召回率。  
- `retrieval_mode`：可选 `single`（单次检索）或 `multi`（多跳检索），后者适用于复杂推理类问题，但延迟增加约 40% —— 具体行为详见 [知识检索](https://help.aliyun.com/zh/model-studio/rag-knowledge-retrieval)。

## 使用方式

1. **控制台流程**：进入「知识库」模块 → 创建知识库 → 上传文件 → 启动构建（自动完成解析、分块、向量化）→ 发布后调用 `/v1/knowledge_base/query` 接口。  
2. **API 调用**：使用 `POST /v1/knowledge_base/query`，请求体需包含 `knowledge_base_id`、`query` 及可选参数（如 `top_k`、`score_threshold`）；认证方式与百炼通用 API 一致（`Authorization: Bearer <api_key>`）。完整规范见 [知识库API指南](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-api-guide)。  
3. **调试建议**：首次集成时，务必通过 [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md) 提供的控制台「测试问答」功能验证分块逻辑与检索相关性，避免因文档格式异常导致静默失败。

## 限制和注意事项

- **配额限制**：单知识库最大文档数 10,000 份，总原始文本容量上限 10 GB；超出需拆分知识库或启用 [知识库配额与限制](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-specifications) 中的升级流程。  
- **文件限制**：PDF 文件需为可复制文本（非扫描图），否则 OCR 能力暂未开放；单文件大小上限 100 MB。  
- **时效性**：知识库更新后，新文档需等待 2–5 分钟完成向量化生效；实时性要求高的场景应结合 [知识库定时数据同步指南](https://help.aliyun.com/zh/model-studio/data-sync-guide) 配置 Webhook 回调。  
- **计费说明**：按调用量（每次 `/query` 请求）与存储量（GB/月）分别计费，详情参见 [知识库计费说明](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base)；注意免费额度不覆盖 API 调用频次。  
> **注意**：原始文档中多处链接指向 help.aliyun.com 的旧版帮助页，部分页面已迁移至新版控制台文档体系；开发者应优先参考 [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md) 中的最新链接锚点，避免点击失效 URL。

## 来源文档

- [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md)


