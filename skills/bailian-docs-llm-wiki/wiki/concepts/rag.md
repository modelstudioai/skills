# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其作为提示（Prompt）的一部分输入模型，从而显著提升回答的事实准确性、领域专业性和私有知识覆盖能力，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一功能模块，而是贯穿多个产品层级的**核心架构模式**，具体体现为以下三类典型应用方式：

- **知识库问答（KB-QA）**：通过控制台或 RAG API 创建结构化/非结构化知识库（支持 `document`、`table`、`image`、`multimedia` 类型），上传 PDF/DOCX/Excel/图片/音视频等文件，平台自动完成解析、切片、向量化与索引构建；调用 `/api/v2/apps/knowledge/chat` 等接口时，系统自动执行“检索 → 重排 → 注入 → 生成”全流程，实现基于私有知识的流式问答。

- **多端智能助手集成**：在网站、微信公众号、企业微信、钉钉等渠道部署 AI 助手时，底层统一依赖 RAG 架构——AppFlow 将用户消息路由至已绑定知识库的百炼智能体应用，确保所有终端共享同一套知识资产与检索逻辑，实现“一次配置、多端复用”。

- **开发者自定义 RAG 应用**：支持通过 LlamaIndex 等开源框架对接百炼知识库服务（如 `DashScopeParse` 文档解析 + 百炼向量索引），或在 Assistant API 中显式启用多知识库并行检索（按配置策略聚合 TopN 结果），满足复杂业务场景下的混合检索、跨模态召回等高级需求。

## 关键参数和配置

RAG 效果高度依赖以下可调参数，开发者应在创建知识库、发起查询或配置智能体应用时重点关注：

| 参数名 | 所属层级 | 说明 | 推荐值 | 注意事项 |
|--------|----------|------|--------|----------|
| `top_k` | 检索层 | 检索阶段返回的最相关文本片段数量 | `3–5` | 过大会引入噪声，过小可能导致信息缺失；需与模型上下文窗口匹配 |
| `similarity_threshold` | 检索层 | 过滤低相似度检索结果的阈值（0–1） | `0.3–0.7` | 默认为 `0`（不过滤）；设为 `0.5` 可显著提升答案精准度，但可能漏检边缘相关项 |
| `rerankTopN` / `rerankModelName` | 检索层 | 重排模型返回的最终排序结果数及模型名（如 `qwen3-rerank`） | `rerankTopN=3`, `rerankModelName=qwen3-rerank` | 重排为可选步骤，对长尾问题和语义歧义场景效果提升明显 |
| `embeddingModelName` | 索引层 | 知识库向量化所用嵌入模型（如 `text-embedding-v4`） | 根据数据类型选择：文本用 `text-embedding-v4`，图文用 `qwen3-vl-embedding` | 多模态场景下 `multimodalEmbeddingModelName` 为必填 |
| `knowledgeScene` | 索引层 | 知识库适用场景枚举（如 `basic_document_qa`, `visual_perception_qa`, `basic_table_qa`） | 严格匹配控制台或 `create_index` 接口文档所列有效值 | 已废弃值（如 `visual_document_qa`）将导致创建失败 |

> ⚠️ 注意：参数命名存在风格混用（`snake_case` 与 `camelCase` 并存），请务必以对应接口文档为准；时间戳类参数需传**秒级 Unix 时间戳字符串**，文件大小类参数（如 `sizeBytes`）必须为字符串格式。

## 面向开发者，简洁实用

- ✅ **快速启动**：优先使用控制台「标准版知识库」+「智能体应用」组合，5 分钟完成私有知识问答闭环；调试时善用界面右上角「问题反馈」按钮提交 `RequestId`，加速问题定位。
- ✅ **性能调优**：若响应延迟高，先检查 `top_k` 是否过大（建议 ≤5）、重排是否冗余（可临时关闭 `rerankModelName` 测试）；若准确率低，优先调高 `similarity_threshold` 并验证嵌入模型与 `knowledgeScene` 匹配性。
- ✅ **生产注意**：单业务空间默认上限 10 万文档，超限时需提交工单扩容；PDF 文件后缀必须为小写 `pdf`，否则返回错误码 `140010`；所有 RAG 请求必须携带 `Authorization: Bearer <API-Key>` Header。
- ✅ **避坑指南**：不要硬编码已废弃的 `knowledgeScene` 值；避免在 `create_index` 接口误传 `file_ids`（实际应为 `docIds`）；[流式输出](streaming-output.md)需显式设置 `incremental_output=True` 才能获得增量 token，否则会重复返回历史内容。

## 关联主题页

- [rag api](../api/rag-api.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)
- [use cases](../guides/use-cases.md)


