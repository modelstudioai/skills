# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼基于 RAG（检索增强生成）技术为大模型补充私有数据和最新信息的能力：大模型在生成回答前先从知识库检索相关内容，从而提升回答准确性。围绕知识库，平台提供了创建管理、检索服务、知识问答、效果优化、API 集成、日志监控与计费等一整套开发者可消费的功能。

> **注意**：知识库功能仅能在中国站 **华北2（北京）** 地域开通和使用，新加坡、德国（法兰克福）等其他地域均不支持。API 相关能力仅适用于文档搜索类知识库。

## 支持的模型与知识库类型

在 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) 中，支持挂载知识库的预置模型包括千问-QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、千问VL-Max/Plus/Flash/OCR、千问开源版（Qwen3/Qwen2.5/Qwen2 等）以及 DeepSeek-R1/V3.1、Llama3.1、Yi-Large 等第三方模型；自定义（调优后）模型支持千问-Plus/Turbo、千问VL-Max/Plus 及开源版。实际可选模型以创建应用时页面列表为准。

创建知识库时需选择类型，创建后不可更改：

- **文档搜索**：面向企业内部文档、产品手册等非结构化数据，可细分为基础文档问答、图文并茂回复、视觉理解（富文本文档，向量模型强制为 qwen3-vl-embedding）和极速问答（低延迟、仅文本查询）。
- **数据查询（结构化）**：单个 Excel/CSV 文件，支持 NL2SQL。
- **图片问答**、**音视频搜索** 等多模态类型。

## 关键参数与配置

- **相似度阈值**：仅语义相似度高于阈值的切片才会被召回，阈值过高会导致相关切片被全部过滤（例如调到 0.60 可能返回无召回结果）。
- **召回片段数 / 最大召回数量（TopK/K）**：取值范围 1–20。对总结、列举、比较类复杂问题适当增大有助于生成完整答案，但会增加 Token 消耗，推荐使用「按拼装长度」策略。
- **权重**：多知识库召回时按信息源重要性分配，但**权重仅在同类型知识库之间生效**。
- **Meta 信息抽取**：以 key-value 附加到切片，可显著提升检索准确性并降低 Token 消耗；支持常量、变量（file_name/cat_name）、大模型、正则、关键词搜索五种取值方式。**知识库创建后无法再配置 metadata 抽取**。
- **智能切分 / 多轮对话改写**：均在创建知识库时配置；多轮对话改写与知识库绑定，创建时未开启则后续无法补开，除非重建知识库。

## 检索与问答服务

平台在知识库之上提供两类独立服务：

- **知识检索**：见 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。支持多知识库联合检索（最多 15 个），流水线为 Query 改写 → 向量+关键词混合检索 → Rerank 精排 → 加权返回。全局参数含知识库路由、混排模型（qwen3-rerank / qwen3-rerank(hybrid) / qwen3-vl-rerank）、混排模式（问答/相似/自定义）；每个知识库可独立配置初步向量/关键词 TopK（1–100）、排序模型、相似度阈值、标签过滤等。
- **知识问答**：见 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。基于大模型（如 qwen3.6-plus/qwen3.7-plus）结合检索生成自然语言回答，提供**极速**（单轮）与**多轮智能**（Agentic 规划搜索）两种检索模式，支持文件预解析、拒答、防泄漏、多模态回复与引用来源展示。

## 使用方式

1. **控制台**：进入知识库页面 → 选择标准版/旗舰版 → 创建知识库（填写基础信息、选类型、配置数据来源与索引参数）→ 关联到智能体/工作流应用。工作流应用中将「知识库」节点接在开始节点后，用内置变量 `query` 作输入，输出 `result` 传给大模型节点。
2. **API/SDK**：面向外部应用，通过阿里云百炼 SDK 集成检索能力。完整创建流程（申请上传租约 → 上传文件 → AddFile → CreateIndex → SubmitIndexJob → 轮询状态）参见 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。子账号需获取 `AliyunBailianDataFullAccess` 策略并加入业务空间，endpoint 为 `bailian.cn-beijing.aliyuncs.com`。

## 效果优化

RAG 效果由建立索引、检索召回、生成答案三阶段决定。建议先用 [自动评测] 建立至少 100 组问题的评估基线（覆盖事实型/比较型/教程型/分析型），再针对失败用例（大模型打分 < 4）诊断改进：检索无效（补充知识、优化排版、统一实体、开启多轮对话改写）、召回不相关（标签过滤 / 元数据结构化搜索）、切片不完整（智能切分 + 人工修正）、重排不佳（调整相似度阈值与召回片段数）、模型理解有误（更换为参数更多的商业模型）。详见 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 配额与限制

摘自 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)：

- **知识库数量**：使用 RDS 数据源上限 100，其它数据源无限制。
- **存储容量**：旗舰版 9,999 GB，标准版 100 GB（免费平台存储）。
- **文件格式与大小**：pdf/docx/ppt 等 ≤150MB 且 ≤1000 页；txt/markdown/html ≤10MB；图片 ≤20MB；音视频 ≤512MB。
- **切片**：单切片最大 6,000 Token；编辑切片长度 10–6000 字符，删除切片单次最多 10 个。音视频搜索类不支持新增切片。
- **向量模型**：文档/数据查询/音视频类支持 text-embedding-v4/v3（512 维）；图片问答类仅 multimodal-embedding-v1（1024 维），维度不可更改。
- **检索并发**：旗舰版 50–10,000 QPS（可调，对应 1–200 RCU），标准版固定 1 QPS。
- **召回**：单次查询最多召回 20 个切片；单次控制台导入最多 50 个文件（API 批量建议 ≤10,000）。

## 计费

知识库服务自 **2026 年 1 月 4 日** 起正式计费，费用由**规格费用**与**模型调用费用**两部分构成。规格费用按运行时长按小时出账：标准版 0.03 元/知识库/小时，旗舰版 0.2 元/RCU/小时（1 RCU ≈ 50 QPS）。扣费顺序为：免费额度 > 资源包 > 按量付费。平台提供一次性 720 小时免费额度（仅抵扣标准版规格费用，不含模型调用），多个知识库按数量倍数扣减。模型调用费用按输入 Token 计费，其中 Rerank 排序费用取决于**初步召回的总切片数**而非最终返回数量，可通过关闭排序或调低初步 TopK 降低成本。

> **注意**：删除知识库会**永久清除数据且无法恢复**，但也是停止计费的唯一方式。2026 年 1 月 4 日前创建但未开通服务的数据保留至 2026 年 6 月 30 日，逾期永久删除。

## 日志与监控

所有检索调用都会以日志形式投递到日志服务（SLS），用于调用审计、问题排查、用量统计与告警。在知识库列表页右上方「监控配置」中完成 SLS 角色授权、开通日志服务并创建 LogStore 后，检索日志会实时投递（秒级延迟），topic 为 `log_dispatch`。关键索引字段包括 `request_id`、`pipeline_id`（知识库 ID）、`workspace_id`、`path`、`latency`、`response_status_code`、`response_code`（成功为 `Success`）、`request_body`/`response_body`（召回切片在 `data.nodes[]`）。可基于这些字段在 SLS 中做按知识库/业务空间的用量聚合、按 API 路径统计，并搭建调用量趋势、TopN 排名仪表盘及错误率告警。

> **注意**：关闭「检索日志」开关只停止新日志投递，历史日志仍按 SLS 默认配置保留与计费；如需彻底停止计费，需在 SLS 控制台删除对应 LogStore。SLS 存储与流量按其自身标准单独计费。

## 来源文档

- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)


