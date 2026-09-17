# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、领域专属或时效性强的结构化与非结构化数据。其工作原理是在模型生成回答前，先从向量化索引中语义检索相关知识片段，并将其作为上下文输入模型，从而显著提升回答的准确性、专业性与事实一致性。该功能仅在中国站华北2（北京）地域可用，国际站仅支持新加坡地域 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作：
- **预置模型**：千问全系（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research）、千问VL系列（Max/Plus/Flash/OCR）、Qwen3/Qwen2.5/Qwen2等开源版本，以及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large等）。
- **自定义模型**：基于上述基础模型调优后的版本，包括千问-Plus/Turbo、千问VL-Max/Plus 及 Qwen 系列开源模型 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

知识库提供三大核心服务形态：
- **知识检索**：面向多知识库联合查询场景，支持混合检索（向量+关键词）、Query 改写与 Rerank 排序，可配置独立参数并返回原始切片 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **知识问答**：在检索基础上集成大模型生成能力，支持极速单轮与 Agentic 多轮智能模式，具备拒答、防泄漏、引用溯源、文件预解析等生产级控制能力 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。
- **定时数据同步**：通过 OSS、飞书、钉钉、语雀、SharePoint 等连接器实现外部知识源的自动化增量同步，支持分钟级至日级周期配置 [知识库定时数据同步指南 (raw/application-user-guide/knowledge-base/data-sync-guide.md)](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

> **注意**：文档 1 与文档 4 在地域支持上存在矛盾。文档 1 明确指出知识库“仅能在中国站华北2（北京）地域开通和使用”，而文档 4 则称“在国际站仅支持新加坡地域开通和使用”。该差异需以控制台实际开通入口为准；当前控制台 UI 仅在北京地域显示知识库入口，故应以文档 1 的描述为权威依据。

## 关键参数

| 参数类别 | 参数名 | 说明 | 典型取值/范围 |
|----------|--------|------|----------------|
| **检索控制** | `相似度阈值` | 过滤排序后得分低于该值的切片，值越高结果越精准但可能漏召 | 0.01–1.0（默认建议 0.3–0.5） |
| | `TopK`（初步召回） | 向量/关键词检索阶段初步召回的切片数，直接影响 Rerank 模型费用 | 向量 TopK：1–100（默认 50）；关键词 TopK：1–100（默认 50） |
| | `最大召回数量` | 最终返回给下游（模型或用户）的切片总数 | 1–20（默认 5） |
| **知识库路由** | `权重` | 多知识库场景下，决定各库召回切片在最终排序中的相对优先级 | 数值越大，权重越高（仅同类型知识库间生效） |
| | `知识库路由开关` | 开启后由 qwen-plus 自动判断应查询哪些知识库，产生额外模型调用费用 | 开/关 |
| **内容过滤** | `标签过滤` | 基于上传时设置的标签进行前置筛选，提升检索精度与效率 | 支持单标签、多标签“或”/“与”逻辑 |
| | `元数据（metadata）` | 在切片中嵌入结构化属性（如 `filename`, `date`, `author`），用于精准过滤与上下文增强 | 创建知识库时配置，创建后不可修改 |

## 使用方式

### 控制台集成
- **智能体应用**：在应用配置页点击“文档知识库”旁的 `+`，选择知识库并设置相似度阈值与权重；支持调试界面实时启用标签过滤。
- **工作流应用**：拖入“知识库”节点，配置 `content` 输入为 `query`，选择固定知识库或动态 `CodeList` 变量；下游大模型节点提示词中通过 `{知识库1/result}` 引用检索结果。
- **外部应用**：通过百炼 SDK 调用 `Retrieve` API 实现检索能力集成，需完成子账号权限配置、AccessKey 设置及业务空间 ID 注入 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

### 高级能力启用
- **多轮对话改写**：在创建知识库的“索引设置”步骤中开启，可自动补全历史上下文，提升模糊查询召回率（创建后不可更改）。
- **视觉理解场景**：选择“文档搜索”类型下的“视觉理解（富文本文档）”使用场景，系统自动切换为 `qwen3-vl-embedding` 向量模型，保留 PDF/图片版面信息。
- **日志监控**：在知识库列表页点击“监控配置”，授权 SLS 角色后即可查看 `request_id`、`latency`、`response_code` 等字段，用于审计、排障与用量分析 [知识库日志与监控 (raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域限制**：知识库功能仅在中国站华北2（北京）地域可用，其他地域（含国际站）不支持开通 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **规格与配额**：
  - 单知识库文件数无硬上限（非结构化类），但单次控制台导入上限为 50 个文件；
  - 文本切片长度上限为 6,000 [Token](../concepts/token.md)，切片数量无限制；
  - 标准版并发为固定 1 QPS，旗舰版为 50–10,000 QPS（按 RCU 计费）；
  - 单次检索最多召回 20 个切片。
- **计费要点**：
  - 规格费用（按小时）与模型调用费用（按 [Token](../concepts/token.md)）分离计费；
  - Rerank 排序费用取决于**初步召回总切片数**（而非最终返回数），增大 TopK 将显著增加成本；
  - 多知识库绑定时，Query 向量化与 Rerank 费用按知识库数量线性叠加。
- **关键操作约束**：
  - 知识库类型（文档搜索/数据查询/图片问答）创建后不可更改；
  - Meta 信息抽取配置必须在创建知识库时完成，后续无法追加；
  - 文件同步为独立副本存储，源文件删除不影响百炼平台内副本，需手动清理。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)


