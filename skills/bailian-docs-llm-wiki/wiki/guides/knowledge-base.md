# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大模型注入私有数据和最新业务信息，提升回答的准确性与领域专业性。其工作流程涵盖知识索引、语义检索与生成增强三个阶段，支持文档搜索、图片问答、音视频搜索等多种知识类型。知识库功能仅在中国站华北2（北京）地域可用，国际站仅支持新加坡地域 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 支持的模型与功能

知识库支持与多种预置及自定义模型协同工作：
- **预置模型**：千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2）、第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）；
- **自定义模型**：基于千问-Plus/Turbo、VL-Max/Plus 或开源版调优后的模型。

功能上，知识库提供三类核心服务：
- **知识检索**：支持单库/多库联合检索（最多 15 个），具备 Query 改写、混合检索（向量+关键词）、Rerank 排序能力 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)；
- **知识问答**：绑定知识库后，自动完成检索+生成，支持极速模式（单轮）与多轮智能模式（Agentic 规划），并可启用文件预解析、拒答、防泄漏、引用溯源等生成控制 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)；
- **定时数据同步**：通过规则自动从 OSS、飞书、钉钉、语雀、SharePoint 同步更新文件，支持分钟级至日级同步周期，确保知识实时性 [知识库定时数据同步指南 (raw/application-user-guide/knowledge-base/data-sync-guide.md)](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

> **注意**：文档 1 和文档 8 对地域支持的描述存在差异——文档 1 明确限定“仅华北2（北京）”，而文档 8 补充说明“国际站仅支持新加坡”。该差异非矛盾，而是分别针对中国站与国际站的独立约束，实际使用需严格按所在站点选择对应地域。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **检索控制** | 相似度阈值 | 0.01–1.0 | 过滤排序后低分切片；值过高易漏召回，过低引入噪声。建议通过[命中测试](raw/application-user-guide/knowledge-base/rag-optimization.md)调优 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |
| | 初步向量检索 TopK | 1–100（默认 50） | 控制向量召回切片数；增大可提升召回完整性，但增加 Rerank 模型 Token 消耗 |
| | 最大召回数量 | 1–20 | 最终返回给大模型的切片数；影响输入 Token 与回答质量平衡 |
| **知识库配置** | 权重 | 数值型（无固定上限） | 多知识库场景下，权重决定同分切片的优先级顺序；**仅在同类型知识库间生效**（如文档搜索类之间） |
| | 标签过滤 / Meta 信息 | 自定义字符串 | 用于结构化过滤：标签实现文件级筛选，Meta（如 `filename`, `date`）实现切片级上下文增强，显著提升精准召回 |

## 使用方式

### 控制台集成
- **智能体应用**：在应用配置页点击“文档知识库”旁的 `+`，添加知识库并设置相似度阈值与权重；
- **工作流应用**：拖入“知识库”节点，配置 `query` 输入变量、TopK 及知识库选择方式（固定或动态），再连接大模型节点并在提示词中引用 `{result}`；
- **外部应用**：通过 SDK 调用知识库 API，需完成权限配置、AccessKey 设置及地域指定（`bailian.cn-beijing.aliyuncs.com`）。

### API 集成
- 适用场景：自动化知识库创建、批量文件上传、检索服务编排；
- 前置要求：子账号需授予 `AliyunBailianDataFullAccess` 策略，并加入目标业务空间；
- 关键流程：申请上传租约 → 上传文件 → 添加文件到类目 → 创建索引 → 提交索引任务 → 轮询状态 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能仅在中国站华北2（北京）及国际站新加坡地域可用，其他地域（如德国法兰克福）不支持；
- **配额限制**：标准版知识库并发为固定 1 QPS，旗舰版为 50–10,000 QPS（可调）；单次查询最多召回 20 个切片；单个知识库文件数无硬上限，但业务空间总文件数上限为 100,000；
- **文件限制**：PDF/DOCX 等文档最大 150 MB 且不超过 1,000 页；Excel 表格禁止合并单元格表头，首行必须为纯字段名；
- **计费要点**：费用 = **规格费用**（按小时计费，标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时） + **模型调用费用**（向量化、Rerank、路由、问答生成均独立计费，按 Token 计）；
- **关键注意事项**：
  - 知识库类型（如“文档搜索”或“视觉理解”）创建后不可更改；
  - Meta 信息抽取必须在创建知识库时配置，后续无法追加；
  - 同步规则导入的文件为独立副本，源文件删除不影响百炼平台内数据；
  - 删除知识库将**永久清除所有数据且不可恢复**，操作前务必确认。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)


