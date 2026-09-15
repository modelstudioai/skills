# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、结构化或非结构化数据，从而提升其在垂直领域回答的准确性与可靠性。它支持文档搜索、数据查询、图片问答、音视频搜索等多种知识类型，并可通过智能体、工作流或 API 方式集成到业务系统中。知识库功能目前仅在中国站华北2（北京）地域可用，国际站仅新加坡地域支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 支持的模型与功能

### 模型支持
以下模型可直接用于知识库问答场景（即作为最终生成模型）：
- **预置模型**：千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research）、千问VL系列（Max/Plus/Flash/OCR）、Qwen3/Qwen2.5/Qwen2 等开源版；
- **第三方模型**：DeepSeek-R1、DeepSeek-V3.1、abab6.5s、Llama3.1、Yi-Large 等；
- **自定义模型**：基于上述基础模型调优后的文本生成模型（如千问-Plus/Turbo、Qwen3 等）[知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

> **注意**：文档1中“支持的模型”列表末尾注明“上述列表随时可能更新”，且明确要求“以应用管理页面实际可选模型为准”。而文档9中知识问答服务的模型选项示例为 `qwen3.6-plus`、`qwen3.7-plus`，与文档1中列出的 `qwen3` 版本命名不一致；文档7的计费说明中亦出现 `qwen3.7-plus`。建议开发者以控制台实时下拉菜单为准，避免硬编码模型名称。

### 核心功能类型
| 类型 | 适用场景 | 关键能力 |
|------|----------|----------|
| **文档搜索** | PDF/DOCX/Markdown 等非结构化文档 | 支持基础问答、视觉理解（富文本文档）、极速问答三种子场景；支持元数据抽取、标签过滤、多轮对话改写 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |
| **数据查询** | Excel/CSV 表格类结构化数据 | 支持 NL2SQL 查询；单知识库仅限 1 个文件；不支持合并单元格表头 |
| **图片问答** | PNG/JPG 等图像文件 | 多模态向量化（`qwen3-vl-embedding`），支持图文理解与问答 |
| **音视频搜索** | MP4/MP3/FLV 等音视频文件 | 先语音识别/帧提取/剧情解析为文本，再进行文本向量化与检索 |

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **全局检索** | 最大召回数量 | 1–20 | 混排后最终返回的切片总数（知识检索服务）或单知识库最终返回数（知识问答服务） |
| | 知识库路由 | 开/关 | 开启后调用 `qwen-plus` 判断应检索哪些知识库，产生额外模型费用 |
| **单知识库** | 初步向量检索 TopK | 1–100 | 向量检索阶段初步召回的切片数（默认 50）；影响 Rerank 费用（见计费说明） |
| | 初步关键词检索 TopK | 1–100 | 关键词检索阶段初步召回的切片数（默认 50） |
| | 相似度阈值 | 0.01–1.0 | 过滤排序后分数低于该值的切片；过高易漏召，过低引入噪声 |
| | 权重 | 数值（无固定上限） | 仅同类型知识库间生效；多路召回时，加权得分 = 相似度 × 权重，决定优先级 |
| **高级控制** | 标签过滤 | 自定义字符串 | 用于精准限定检索范围，支持单标签、多标签“或”/“与”逻辑 |
| | 结构化字段过滤 | 键值对 | 仅表格类知识库支持，按列名和值过滤 |

> **注意**：文档6明确指出“权重仅在同类型知识库之间生效”，而文档1中描述为“当智能体应用同时关联多个知识库时……系统将优先返回权重更高的知识库中的文本切片”，未强调类型限制。以文档6为准，跨类型（如文档搜索 vs 数据查询）知识库的权重配置无效。

## 使用方式

### 控制台集成（零代码）
- **智能体应用**：在应用配置页 → “文档知识库” → 点击 `+` 添加知识库，设置相似度阈值与权重；
- **工作流应用**：拖入“知识库”节点 → 配置输入（如 `query`）、选择知识库（固定或动态）、设置 `TopK` → 连接至大模型节点 → 在提示词中引用 `{知识库1/result}`；
- **知识检索/问答服务**：独立服务形态，支持多知识库联合检索与问答，通过控制台创建并发布后即可调试 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

### API 集成（代码接入）
- 适用于外部系统调用知识库检索能力；
- 必须使用华北2（北京）或新加坡地域 endpoint；
- 前置步骤：子账号需 `AliyunBailianDataFullAccess` 权限、加入业务空间、配置 AccessKey 与 `WORKSPACE_ID`；
- 核心流程：申请上传租约 → 上传文件 → 添加文件 → 创建索引 → 提交索引任务 → 等待完成 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

### 定时同步（自动化运维）
- 通过“数据连接器”配置同步规则，自动从 OSS/飞书/钉钉/语雀/SharePoint 同步文件；
- 同步周期可选：1分钟（高实时性，高配额消耗）、1小时（推荐默认）、1天（低频更新）；
- 同步文件为独立副本，源文件删除不影响百炼中已同步内容 [知识库定时数据同步指南 (raw/application-user-guide/knowledge-base/data-sync-guide.md)](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

## 限制和注意事项

### 地域与配额限制
- **地域限制**：知识库功能仅在中国站华北2（北京）及国际站新加坡地域可用；其他地域（如德国法兰克福）不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)；
- **知识库数量**：主账号无硬性上限（除 RDS 数据源为 100 个）；
- **单知识库存储**：标准版 ≤100 GB，旗舰版 ≤9,999 GB；
- **单次导入文件数**：控制台最多 50 个；API 无此限制，但建议单次 ≤500；
- **单文件大小**：PDF/DOCX 最大 150 MB（≤1000 页），图片最大 20 MB，音视频最大 512 MB。

### 计费关键点
- **规格费用**：按小时计费（标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时），RCU 决定并发能力（1 RCU ≈ 50 QPS）；
- **模型调用费用**（独立于规格费）：
  - **向量化**：按新增内容 Token 计费（`text-embedding-v4` 或 `qwen3-vl-embedding`）；
  - **Rerank 排序**：费用 = `初步召回总切片数 × 平均切片 Token 数 × 单价`，**与最终返回数无关**；
  - **多知识库场景**：Query 向量化与 Rerank 费用按知识库数量线性叠加（N 个库 → N 倍费用）；
- **免费额度**：仅抵扣标准版规格费，720 小时一次性额度，老用户有效期至 2026-02-03。

### 技术注意事项
- **元数据配置不可逆**：知识库创建后无法再开启 Meta 信息抽取，务必在创建时完成配置；
- **多轮对话改写不可追加**：若创建知识库时未启用该功能，则后续无法为该库开启；
- **切片编辑局限性**：音视频搜索类知识库不支持新增切片；
- **日志监控**：检索日志投递至 SLS，需手动开通并授权角色 `AliyunServiceRoleForSFMAccessSLS`，关闭开关仅停止新日志投递，历史日志仍计费。

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


