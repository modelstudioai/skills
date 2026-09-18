# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、结构化或非结构化数据，从而提升其在垂直领域回答的准确性与可靠性。它支持文档搜索、数据查询、图片问答、音视频搜索等多种知识类型，并可通过智能体应用、工作流应用或外部 SDK 集成调用。知识库功能目前仅在中国站华北2（北京）地域可用，国际站仅支持新加坡地域 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 支持的模型与功能

### 支持的模型
以下模型可直接用于知识库问答或[检索增强生成](../concepts/rag.md)：
- **预置模型**：千问-QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、千问VL-Max/Plus/Flash/OCR、千问-开源版（Qwen3、Qwen2.5、Qwen2等）；
- **第三方模型**：DeepSeek-R1、DeepSeek-V3.1、abab6.5s、Llama3.1、Yi-Large 等；
- **自定义模型**：基于千问-Plus/Turbo、千问VL-Max/Plus 或 Qwen 系列开源模型调优后的模型。

> **注意**：文档 1 中列出的“千问-Plus/Turbo”等模型在“自定义模型”小节中重复出现，但未说明是否需额外开通权限；而文档 5 明确指出 API 调用仅支持**文档搜索类知识库**，且对模型无额外限制。实际开发中请以控制台创建应用时可选模型为准 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

### 核心功能
- **多知识库联合检索**：单次请求最多支持 15 个知识库并行检索，支持权重配置与路由判断；
- **多模态支持**：视觉理解（富文本文档）、图片问答、音视频搜索（语音识别+帧提取+剧情解析）；
- **智能检索增强**：支持 Query 改写、混合检索（向量 + 关键词）、Rerank 排序、标签/元数据/结构化字段过滤；
- **生成控制能力**：拒答策略、防泄漏保护、引用溯源、多模态图文回复、文件预解析（对话中上传即用）；
- **两种问答模式**：极速模式（单轮检索→生成）适用于低延迟场景；多轮智能模式（Agentic 规划）适用于复杂意图理解与跨库综合推理 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **全局检索** | 最大召回数量 | 1–20 | 混排后最终返回的切片总数（所有知识库合并后） |
| | 知识库路由 | 开/关 | 开启后调用 `qwen-plus` 判断应检索哪些知识库，产生额外模型费用 |
| **单知识库独立配置** | 初步向量检索 TopK | 1–100 | 向量语义召回的初始切片数（默认 50） |
| | 初步关键词检索 TopK | 1–100 | 关键词精确匹配召回的初始切片数（默认 50） |
| | 相似度阈值 | 0.01–1.0 | 过滤排序后得分低于该值的切片；过高易漏召，过低引入噪声 |
| | 权重 | 任意正整数 | 多知识库场景下，影响混排时各库结果的相对优先级（仅同类型知识库间生效） |
| | 标签过滤 | 自定义字符串 | 按 `tags` 字段筛选文档，实现业务维度精准过滤 |
| **索引构建** | Meta信息抽取 | — | 创建知识库时配置，支持从文件中自动提取 `date`、`filename`、`author` 等元数据，用于结构化检索 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |

> **注意**：文档 7 中“召回文本切片数量”上限为 20，与文档 8/9 中“最大召回数量”取值范围（1–20）一致，但文档 6 的计费说明强调“**Rerank 费用取决于初步召回总切片数**”，而非最终返回数——这意味着即使设置 `最大召回数量=5`，若 `TopK=100`，仍按 100 个切片计费。开发者需权衡效果与成本。

## 使用方式

### 控制台集成（零代码）
- **智能体应用**：在应用配置页 → “文档知识库” → 点击 `+` 添加知识库，可设置相似度阈值与权重；
- **工作流应用**：拖入“知识库”节点 → 配置输入（如 `query`）、选择知识库（固定或动态）、设置 `TopK` → 连接下游大模型节点 → 在提示词中插入 `{知识库1/result}` 变量；
- **知识检索/问答服务**：在知识库页面切换至对应标签页 → 创建服务 → 绑定知识库 → 配置参数 → 发布 → 直接测试。

### API/SDK 集成
- 适用场景：自动化知识库生命周期管理（创建、上传、索引、检索）、嵌入自有系统；
- 前置条件：子账号需授予 `AliyunBailianDataFullAccess` 权限并加入业务空间；配置 `ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET` 和 `WORKSPACE_ID` 环境变量；
- 核心流程：申请上传租约 → 上传文件 → 添加文件到类目 → 创建索引 → 提交索引任务 → 等待完成；
- 注意事项：API 仅支持**文档搜索类知识库**；同步规则、日志监控等功能暂无对应 API [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

### 定时数据同步（免运维）
通过“数据连接器”配置同步规则，支持 OSS、飞书、钉钉、语雀、SharePoint 五类源，按分钟/小时/天周期自动拉取新增/更新文件。同步文件作为独立副本存储，源文件删除不影响百炼副本；OSS 同步需为目标 Bucket 添加 `bailian-datahub-access` 标签 [知识库定时数据同步指南 (raw/application-user-guide/knowledge-base/data-sync-guide.md)](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能仅在中国站**华北2（北京）**地域开通；国际站仅支持**新加坡**地域（文档 1 与文档 5 表述存在差异，以文档 5 的国际站支持说明为准）；
- **配额限制**：
  - 单知识库平台存储：标准版 ≤100 GB，旗舰版 ≤9,999 GB；
  - 单次导入文件数：控制台上限 50 个（API 无此限制）；
  - 单文件大小：PDF/DOCX 最大 150 MB，图片最大 20 MB，音视频最大 512 MB；
  - 文本切片长度：单切片 ≤6,000 Token；
- **关键不可变项**：知识库类型（文档搜索/数据查询/图片问答等）创建后不可更改；Meta信息抽取必须在创建时配置，后续无法追加；
- **计费要点**：
  - 规格费用：标准版 0.03 元/小时，旗舰版按 RCU 计费（1 RCU ≈ 50 QPS）；
  - 模型费用：独立于规格费，包括向量化（`text-embedding-v4` 等）、Rerank（`qwen3-rerank`）、路由（`qwen-plus`）、问答生成（如 `qwen3.7-plus`）三类调用，均按输入 Token 计费；
  - **重要**：Rerank 费用 = `初步召回总切片数 × 平均切片Token数 × 单价`，与最终返回数无关；
- **调试建议**：
  - 使用[命中测试](raw/application-user-guide/knowledge-base/rag-optimization.md)验证召回质量；
  - 开通[SLS 日志监控](raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)，通过 `request_id` 和 `response_body.data.nodes[]` 审计召回切片与元数据；
  - 对于多轮对话场景，启用“多轮对话改写”功能（创建知识库时开启），避免指代歧义导致召回失败。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)


