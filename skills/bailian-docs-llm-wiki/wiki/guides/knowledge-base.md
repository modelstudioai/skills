# [knowledge](../api/knowledge.md) base

知识库（Knowledge Base）是阿里云百炼平台基于 RAG（检索增强生成）技术为大模型补充私有数据和最新信息的能力。大模型在生成回答前先从知识库中检索语义相关的内容，从而显著提升在特定领域问题上的准确性。围绕知识库，平台还提供了知识检索、知识问答、API 集成、日志监控与计费等一整套配套能力。

> **注意**：知识库功能仅能在中国站 **华北2（北京）** 地域开通和使用，新加坡、德国（法兰克福）等其他地域均不支持。

## 支持的模型与知识库类型

预置模型（千问-QwQ/Long/Max/Plus/Turbo/Coder、千问VL 系列、Qwen 开源版，以及 DeepSeek-R1/V3.1、Llama3.1 等第三方文本生成模型）和部分调优后的自定义模型均可挂载知识库。具体可选模型以[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面创建应用时实际可选项为准。

创建知识库时按场景选择类型（创建后不可更改）：

- **文档搜索**：企业内部文档、产品手册等非结构化数据检索。可细分为基础文档问答、图文并茂回复、视觉理解（富文本文档）、极速问答四种使用场景。选择视觉理解后向量模型自动切换为 qwen3 多模态向量（qwen3-vl-embedding），不可更改。
- **数据查询（表格库）**：结构化 Excel/CSV，单库仅支持 1 篇。
- **图片问答类**：仅支持 multimodal-embedding-v1 向量模型。
- **音视频搜索类**：支持语音识别、视频帧提取与剧情解析。

不同解析方式（电子文档解析、文档智能解析、大模型文档解析、Qwen VL 解析、音视频解析）在速度与图表理解能力上有明显差异，详见[知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 关键参数

知识库的检索效果主要由以下参数决定，在命中测试、检索服务和问答服务中可反复调优：

- **相似度阈值（0.01~1.0）**：仅语义相似度高于阈值的切片会被召回。阈值过高会导致相关切片被全部丢弃（例如调至 0.60 可能返回无召回结果）。
- **初步向量检索 TopK / 初步关键词检索 TopK（1~100，默认各 50）**：控制初步召回的切片数量，直接影响送入 Rerank 模型的 Token 量与成本。
- **最大召回数量 / 召回片段数（1~20）**：即多路召回的 K 值，最终提供给大模型的切片数。对总结、列举、比较类复杂问题应适当调大。
- **权重**：多知识库联合召回时用于干预排序，但**仅在同类型知识库之间生效**。
- **排序模型（Rerank）**：纯文本可选 qwen3-rerank、qwen3-rerank(hybrid)；多模态可选 qwen3-vl-rerank。支持问答模式与相似模式。
- **Meta 信息抽取与标签过滤**：通过元数据（常量/变量/大模型/正则/关键词方式提取）和标签在向量检索前做结构化筛选，精准定位目标文件。注意元数据只能在创建时配置，创建后无法再开启。

## 使用方式

**控制台快速构建**：进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)选择规格后，按"填写基础信息 → 配置数据来源 → 设置索引参数"三步完成创建，随后可关联到智能体应用、工作流应用或外部应用。工作流应用需将知识库节点接在开始节点之后、大模型节点之前，并在大模型提示词中引用 `result` 变量。

**知识检索服务**：面向多知识库联合检索（最多 15 个），提供 Query 改写、混合检索（向量+关键词）、Rerank 排序的流水线，支持知识库路由、混排模型模式等全局与单库独立参数配置，详见[知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

**知识问答服务**：在检索基础上由大模型（如 qwen3.6-plus）生成自然语言回答，提供**极速模式**（单轮检索+生成）和**多轮智能模式**（Agentic 多轮规划搜索），并支持文件预解析、拒答、防泄漏、多模态回复、引用来源等生成控制。

**API/SDK 集成**：通过[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)调用，典型创建流程为：申请上传租约（ApplyFileUploadLease）→ 上传文件 → AddFile → CreateIndex → SubmitIndexJob → 轮询 GetIndexJobStatus。子账号需先获取 AliyunBailianDataFullAccess 策略并加入业务空间，详见[知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 效果优化

RAG 效果由建立索引、检索召回、生成答案三个阶段决定。优化前建议用[自动评测](https://help.aliyun.com/zh/model-studio/application-auto-evaluation)建立至少 100 组用例的评估基线，再针对失败用例（打分 < 4）诊断改进：

- **检索无效（没找到）**：补充知识、优化源文件排版（推荐转 Markdown、移除水印、避免复杂表格）、统一实体表述、启用多轮对话改写。
- **召回不相关**：使用标签过滤或元数据做结构化搜索。
- **切片不完整**：采用"智能切分"（基于语义自适应切分），并人工检查修正异常切片。
- **重排不佳**：调整相似度阈值与召回片段数，在漏召回与噪声之间平衡。

## 日志与监控

所有检索调用都会以日志形式投递到日志服务（SLS），topic 为 `log_dispatch`，包含 `request_id`、`pipeline_id`（知识库 ID）、`workspace_id`、`latency`、`response_status_code`、`response_code`、`request_body`、`response_body` 等索引字段，可用于调用审计、用量统计、慢查询与错误率监控。首次使用需在知识库列表页的**监控配置**中授权 SLS 角色、开通日志服务并创建 LogStore。SLS 存储与流量单独计费，关闭检索日志开关只停止新投递，历史日志仍保留计费，需彻底停止请到 SLS 删除对应 LogStore。

## 限制与配额

| 类别 | 上限 |
| --- | --- |
| 知识库数量 | RDS 数据源 100，其它数据源无限制 |
| 存储容量 | 旗舰版 9,999 GB / 标准版 100 GB |
| 单个文档搜索类知识库文件数 | 无硬性上限（数据查询类仅 1 篇） |
| 单次控制台导入文件数 | 50（API 批量建议单次 ≤ 10,000） |
| 单文件标签数 | 32 |
| 文本切片长度 | 6,000 Token |
| 召回文本切片数量 | 20 |
| 检索并发 | 旗舰版 50-10,000 QPS（1-200 RCU）/ 标准版 1 QPS 固定 |

文件格式限制：pdf/docx/ppt 等最大 150MB 且页数 ≤ 1,000；txt/markdown/html 最大 10MB；图片最大 20MB；音视频最大 512MB。向量模型仅支持 text-embedding-v3/v4（512 维）与 multimodal-embedding-v1（1024 维），维度不可更改。完整清单见[知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

## 计费注意事项

知识库服务自 **2026 年 1 月 4 日**起正式计费，总费用由**规格费用**（运行时长）和**模型调用费用**（向量化 + Rerank）两部分构成，扣费顺序为免费额度 > 资源包 > 按量付费。

- 规格费用：标准版 0.03 元/知识库/小时；旗舰版 0.2 元/RCU/小时（1 RCU ≈ 50 QPS）。
- 模型调用费用独立计费，公式为 `(输入 Token 总数 / 1000) × 模型单价`。**Rerank 费用取决于初步召回的总切片数，而非最终返回数**，因此降低初步 TopK 或关闭排序可显著省钱。
- 应用挂载多个知识库时，模型 Token 消耗按知识库数量倍增（N 个库则 × N）。
- 平台提供一次性 720 小时免费额度（仅抵扣标准版规格费用，不含模型调用费）。删除知识库以停止计费，但删除会**永久清除数据且无法恢复**。

> **注意**：免费额度有效期存在新老用户差异——老用户统一截至 2026 年 2 月 3 日 23:59，新用户自开通起 30 天内有效，逾期作废。此外《知识库计费说明》以 2026 年计费规则描述，而《知识库》文档仍按旧的即时计费口径（0.03/0.2 元/小时）介绍创建流程，接入时以[知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)为准。

## 来源文档

- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)


