# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将外部知识检索与大语言模型（LLM）生成能力深度融合的技术范式。它通过在模型推理前动态检索相关知识片段，并将其作为上下文注入 prompt，显著提升生成结果的事实准确性、领域专业性和可解释性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台中不是单一功能，而是贯穿多个层级的**核心增强机制**，具体体现为以下三种协同使用方式：

- **RAG API 独立服务模式**：通过 `/knowledge/search` 和 `/knowledge/chat` 接口直接调用 RAG Agent，适用于需细粒度控制检索策略（如跨库联合检索、多模态重排）的后台服务。支持 `document`/`table`/`image`/`multimedia` 四类知识库类型，配合 `visual_perception_qa` 等场景化配置实现图文音视频混合问答。

- **Agent 内置增强模式**：在 Managed、Flow 或 Sandbox Agent 中，通过「绑定知识库」或 `agent_context` 配置启用 RAG。系统自动完成检索→重排→截断→注入全流程，开发者只需指定 `knowledge_base_id` 和 `rag_top_k`，无需编写检索逻辑。该模式与对话状态管理、工具调用深度集成，适用于客服、智能助手等交互型应用。

- **应用级开箱即用模式**：在网站、微信公众号、企业微信、钉钉等渠道集成时，RAG 作为百炼智能体应用的默认增强能力启用。上传 PDF/Excel/PNG 等文件构建知识库后，在应用配置中开启「必定调用」，即可零代码获得基于私有知识的问答能力，所有渠道复用同一套知识源与检索配置。

> ✅ 关键共识：无论采用哪种模式，RAG 的底层流程一致——**查询向量化 → 向量库相似度检索 → 重排序（可选）→ 上下文拼接 → LLM 生成**，且全程支持流式响应（`stream=true`）与增量输出（`incremental_output=true`）。

## 关键参数和配置

| 参数 | 位置 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `rag_top_k` | Agent 编排 YAML / `agent_context` / RAG API `agent_config` | int | `3` | 检索返回的最相关知识片段数量；增大可提升召回率，但可能引入噪声或超 token 限制 |
| `embeddingModelName` | RAG API 创建知识库时 | string | `text-embedding-v4`（文本）<br>`qwen3-vl-embedding`（多模态） | 显式指定向量模型，影响检索质量；未设置时使用系统默认值 |
| `rerank_top_n` | RAG API `agent_config` | int | `5` | 重排序阶段保留的 Top-N 结果数（重排前检索结果数通常更大） |
| `context_max_tokens` | `agent_context.extra_parameters` | int | `2048` | RAG 注入上下文的整体 token 上限，超出部分按优先级自动截断（RAG > memory > connector） |
| `knowledgeScene` | RAG API 创建知识库时 | string | `basic_document_qa` | 场景标识，决定预置 prompt 模板与处理链路（如 `visual_perception_qa` 启用视觉理解模块） |

⚠️ 注意事项：
- RAG 与 Memory context **不可共存**：若同时配置，系统静默优先采用 RAG，忽略 memory 设置；
- 所有 RAG 请求必须携带有效 `agent_id`（来自已发布的 RAG Agent）；
- 多知识库并行检索时，结果按配置权重融合打分，非简单拼接；
- 文件上传需校验 `MD5`，PDF 后缀必须为小写 `pdf`，否则报错 `140010`。

## 面向开发者，简洁实用

- **快速上手**：控制台 → 数据连接 → 上传文件 → 创建知识库 → 应用管理 → 绑定知识库 → 发布。无需 API 调用即可启用。
- **调试技巧**：在 Playground 测试时，点击回复下方「问题反馈」按钮可提交 `RequestId`，附带原始 query 和检索到的 top-k 片段，便于定位召回或生成问题。
- **性能优化**：  
  - 对长文档，建议启用 ParseX 自动解析（表格转 JSON、PDF 分块优化），提升 chunk 相关性；  
  - 高并发场景下，优先使用 `lite_document_qa` 场景（轻量级 embedding + 快速重排）；  
  - 严格控制 `context_max_tokens ≤ 8192`，为生成留足空间（Qwen 系列推荐最大输入 24K，但 RAG 上下文建议 ≤1/3）。
- **避坑指南**：  
  - 不要硬编码旧模型名（如 `千问-Plus`），统一使用控制台显示的最新命名（如 `Qwen3.5-Plus`）；  
  - 删除文档接口必须传 `index_id`（snake_case），传 `indexId`（camelCase）会触发 `Index.InvalidParameter` 错误；  
  - Sandbox 模式中 RAG 需通过 `extra_parameters.agent_context` 显式传入，不支持可视化绑定。

## 关联主题页

- [rag api](../api/rag-api.md)
- [agent development](../guides/agent-development.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [application support](../guides/application-support.md)


