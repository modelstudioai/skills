# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、领域专属或时效性强的结构化与非结构化数据，从而提升回答的准确性、专业性和事实一致性。其本质是将用户自有数据（文档、表格、音视频等）经解析、切片、向量化后构建可语义检索的索引，并在模型生成前动态注入相关上下文。

## 支持的模型/功能

知识库支持两类模型调用：**向量/排序模型**（用于检索流程）和**问答生成模型**（用于最终回答）。  
- **向量模型**：`text-embedding-v4`（文档/音视频搜索类）、`qwen3-vl-embedding`（图片问答类及「视觉理解」场景）；  
- **排序模型**：`qwen3-rerank`（文本类）、`qwen3-vl-rerank`（[多模态](../concepts/multimodal.md)类）；  
- **问答生成模型**：所有支持 RAG 的预置与自定义模型，包括千问全系（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research）、千问VL系列、Qwen3/Qwen2.5/Qwen2 开源版，以及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）[配置千问使用知识库教程](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  

功能上，知识库支持**文档搜索**（含基础问答、视觉理解、极速问答三类场景）、**数据查询**（结构化表格）、**图片问答**和**音视频搜索**四类知识库类型，并提供**知识检索服务**（多库联合检索）与**知识问答服务**（端到端问答）两种封装形态 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

## 关键参数

| 参数类别 | 参数名 | 说明 | 取值范围/默认值 |
|----------|--------|------|-----------------|
| **检索控制** | 初步向量检索 TopK | 向量召回切片数（影响 Rerank 费用） | 1–100，默认 50 |
| | 初步关键词检索 TopK | 关键词召回切片数 | 1–100，默认 50 |
| | 相似度阈值 | 过滤重排后低分切片 | 0.01–1.0，默认 0.3 |
| | 最大召回数量 | 单次查询返回的最终切片数 | 1–20，默认 5 |
| **高级能力** | 多轮对话改写 | 基于历史会话自动补全 Query | 创建时启用，后续不可修改 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |
| | 标签过滤 / Meta 信息 | 结构化过滤，提升召回精度 | 标签最多 32 个/文件；Meta 需创建知识库时配置，不可追加 |

> **注意**：文档 7 中“召回文本切片数量”上限为 20，但文档 8 和文档 9 明确允许将“最大召回数量”设为 1–20，且文档 1 的工作原理图示及实测案例均基于该参数生效。因此以文档 8/9 的 1–20 为准，文档 7 的“20”应理解为单次请求的硬性上限，而非配置项限制。

## 使用方式

知识库可通过三种方式集成：  
1. **控制台零代码集成**：在[应用管理](https://bailian.console.aliyun.com/#/app-center)中为智能体或工作流应用添加「文档知识库」节点，配置相似度阈值、权重及 TopK；工作流中需显式连接知识库节点与大模型节点，并在提示词中引用 `{result}` 变量 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
2. **API 调用**：通过 `bailian20231229` SDK 调用 `CreateIndex`、`SubmitIndexJob`、`Retrieve` 等接口实现自动化知识库生命周期管理与检索，适用于外部系统对接 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
3. **定时同步**：通过「数据连接器」配置 OSS/飞书/钉钉等来源的同步规则，按分钟/小时/天自动拉取更新文件，确保知识库内容实时性 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能仅在中国站**华北2（北京）**和国际站**新加坡**地域可用，其他地域（如德国法兰克福）不支持 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **配额限制**：单账号最多创建 100 个知识库（若使用 RDS 数据源）；标准版知识库存储上限 100 GB，旗舰版 9,999 GB；单次导入文件数上限 50 个（API 批量无此限）[知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **计费要点**：费用 = **规格费**（标准版 0.03 元/小时，旗舰版按 RCU 计费） + **模型调用费**（向量化、Rerank、问答生成独立计费，[Token](../concepts/token.md) 按实际用量计算）；多个知识库并行检索时，模型费用线性叠加 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。  
- **关键约束**：知识库类型（文档搜索/数据查询等）创建后不可更改；Meta 信息抽取必须在创建时配置，无法事后补充；权重仅在同类型知识库间生效（如文档搜索类之间），跨类型无效。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)


