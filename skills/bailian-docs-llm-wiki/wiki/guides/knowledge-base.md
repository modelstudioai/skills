# [knowledge](../api/knowledge.md) base

阿里云百炼知识库基于 RAG（[检索增强生成](../concepts/rag.md)）技术，为大模型补充私有数据与最新信息，提升特定领域问答的准确性。它覆盖知识库创建、数据导入、检索召回、问答生成、日志监控与计费计量的完整链路，支持文档搜索、数据查询、图片问答、音视频搜索等[多模态](../concepts/multimodal.md)场景，并可经控制台或开放 API 接入业务系统。

## 支持的模型与知识库类型

知识库功能仅能在中国站 **华北2（北京）** 地域开通和使用，其他地域均不支持。

可挂载知识库的模型范围以应用管理页面实际可选项为准，预置模型涵盖千问 QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、千问 VL 系列、千问开源版（Qwen3、Qwen2.5、Qwen2 等）以及第三方文本生成模型（DeepSeek-R1、DeepSeek-V3.1、abab6.5s、Llama3.1、Yi-Large 等）；自定义模型支持基于千问 Plus/Turbo、千问 VL-Max/Plus、千问开源版调优后的版本。详见 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

知识库类型在创建时选定且不可更改，主要包括：

- **文档搜索类**：用于企业内部文档、产品手册等非结构化数据，支持基础文档问答、图文并茂回复、视觉理解（富文本文档）、极速问答等子场景。
- **数据查询类**：结构化知识库，单个知识库仅支持 1 篇 Excel/CSV 文件，可用 NL2SQL 查询。
- **图片问答类**：仅支持 `multimodal-embedding-v1`（1024 维）向量模型。
- **音视频搜索类**：对语音做识别、对视频做帧提取与剧情解析，按时间轴结构化对齐。

向量模型方面，文档搜索、数据查询、音视频搜索类支持 `text-embedding-v4` 或 `text-embedding-v3`（均为 512 维），维度不可更改；视觉理解场景会自动切换为 `qwen3-vl-embedding`（qwen3 [多模态](../concepts/multimodal.md)向量）。详见 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

## 创建与数据导入

在 [知识库控制台](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 选择 **标准版** 或 **旗舰版** 后创建，三步完成：基础信息与类型 → 数据来源 → 索引参数。

**规格差异**：标准版 0.03 元/小时、1 QPS、平台存储 ≤ 100 GB；旗舰版 0.2 元/RCU/小时、50–10,000 QPS（对应 1–200 RCU）、平台存储 ≤ 9,999 GB。RCU（Retrieval Compute Unit）按"向上取整（峰值 QPS ÷ 50）"估算。

**解析方式**（文档搜索类）：

- 电子文档解析：最快，不支持插图与图表。
- 文档智能解析：对插图做 OCR 与摘要，速度较快。
- 大模型文档解析：用千问 VL 深度理解插图与图表，耗时较长。
- Qwen VL 解析：专用于图片文件，可指定 Prompt 引导识别。
- 音视频解析：含录音文件识别、视频帧提取与剧情解析（手动开启）。

**索引配置**：含 Meta 信息抽取、切片方式、多轮对话改写等。注意：

- Meta 抽取在知识库创建后**无法再配置**，需在创建时一次性设好。
- 多轮对话改写与知识库绑定，创建时未开启则后续无法开启，除非重建。
- 切片方式推荐 **智能切分**，基于语义相关性自适应选择切片点；单切片 [Token](../concepts/token.md) 上限 6,000。

## 检索与问答

阿里云百炼提供两条独立服务线，均支持绑定最多 15 个知识库：

- **知识检索服务**：仅返回检索切片，不生成回答。流程为 Query 改写 → 向量 + 关键词混合检索 → Rerank 排序 → 加权返回。详见 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **知识问答服务**：在检索基础上叠加生成模型（如 qwen3.6-plus、qwen3.7-plus），支持极速模式（单轮检索 + 生成）和多轮智能模式（Agentic 多轮规划搜索）。详见 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

关键检索参数：

| 参数 | 取值 | 说明 |
| --- | --- | --- |
| 初步向量检索 TopK | 1–100（默认 50） | 向量语义召回切片数 |
| 初步关键词检索 TopK | 1–100（默认 50） | 关键词匹配召回切片数 |
| 排序模型 | qwen3-rerank / qwen3-rerank(hybrid) / qwen3-vl-rerank | [多模态](../concepts/multimodal.md)库只能选 vl-rerank |
| 排序模式 | 问答 / 相似 / 自定义高级 | 问答模式按 QA 匹配度，相似模式按语义相似度 |
| 相似度阈值 | 0.01–1.0 | 过滤排序后低分切片，过高会丢弃全部结果 |
| 最大召回数量 | 1–20 | 最终返回切片数 |

**权重**：多知识库召回时，相似度相同的切片优先返回权重高的库；权重**仅在同类型知识库之间生效**。

## 优化与诊断

如遇召回不完整或内容不准确，建议先建立评估基线（至少 100 组覆盖事实/比较/教程/分析型的评测用例），再按失败类型针对性改进，详见 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

常见诊断方向：

- **没有相关知识**：补充知识库内容，优化源文件排版（移除水印、避免合并/跨页单元格、优先 Markdown），统一实体表述，启用多轮对话改写。
- **召回不相关**：为文件添加标签做前置过滤，或为文件配置 Meta 元数据做结构化筛选（如按产品名、日期过滤）。
- **切片不完整**：改用智能切分；人工检查并修正异常切片（编辑后原内容失效）。
- **重排不佳**：通过命中测试反复调整相似度阈值与召回片段数（K 值 1–20）；对"列举/总结/比较"类问题适当提高 K，并优先选 **按拼装长度** 避免超长截断。
- **模型理解有误**：更换为商业模型（如通义千问 Max、Plus），简单查询可用 Flash/Turbo。

## API 集成

知识库提供开放 API，便于自动化操作与外部接入。注意 **API 指南仅适用于文档搜索类知识库**。

前置步骤：子账号需获取 `AliyunBailianDataFullAccess` 策略并加入[业务空间](../concepts/workspace.md)；安装阿里云百炼 SDK（`alibabacloud_bailian20231229`）；配置 `ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`、`WORKSPACE_ID` 环境变量。接入地址示例：`bailian.cn-beijing.aliyuncs.com`。

典型流程：申请上传租约（ApplyFileUploadLease）→ 上传文件到预签名 URL → 添加文件（AddFile）→ 查询解析状态（DescribeFile）→ 创建索引（CreateIndex）→ 提交索引任务（SubmitIndexJob）→ 查询任务状态（GetIndexJobStatus）→ 检索（Retrieve）。详见 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 日志与监控

所有检索调用均以日志形式投递到日志服务（SLS），可用于调用审计、问题排查、用量统计与告警。在知识库列表页 **监控配置** 面板首次开通，会自动创建固定 Project/LogStore（按 SLS 存储与流量计费）。

每条日志 `topic = log_dispatch`，关键字段：`request_id`、`pipeline_id`（知识库 ID）、`workspace_id`、`user_id`、`path`、`latency`、`response_status_code`、`response_code`（成功为 `Success`，失败为点分错误码如 `Index.IndexNotExist`）、`request_body`、`response_body`（召回切片在 `data.nodes[]`，含 `score`、`text`、`metadata`）。

> **注意**：关闭 **检索日志** 开关只停止新日志投递，历史日志仍按 SLS 默认配置保留与计费；如需彻底停止计费，请到 SLS 控制台删除对应 LogStore。详见 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 配额与限制

| 类别 | 上限 |
| --- | --- |
| 知识库数量（RDS 数据源） | 100 |
| 知识库数量（其他数据源） | 无限制 |
| 平台存储容量 | 标准版 100 GB / 旗舰版 9,999 GB |
| 类目数量（每[业务空间](../concepts/workspace.md)） | 500 |
| 文件数量（每[业务空间](../concepts/workspace.md)） | 100,000 |
| 单知识库文件数 | 非结构化无硬性上限 / 结构化 1 篇 |
| 数据表数量 | 1,000 |
| ADB-PG 单表行数 / 单行大小 | 10,000,000 / 100 KB |
| 单文件标签数 | 32 |
| 控制台单次导入文件数 | 50（API 建议单次 ≤ 10,000） |
| 单切片 [Token](../concepts/token.md) | 6,000 |
| 单次检索召回切片数 | 20 |
| 检索并发 | 标准版 1 QPS（固定）/ 旗舰版 50–10,000 QPS（1–200 RCU） |

文件格式限制要点：pdf/docx/wps/pptx 等最大 150 MB 且 ≤ 1,000 页；txt/markdown/html 最大 10 MB；xlsx/xls 最大 10 MB 且 ≤ 10 万行；图片最大 20 MB、短边 > 15px、长边 < 8,192px；音视频最大 512 MB。切片操作方面，编辑切片（UpdateChunk）长度限制 10–6,000 字符，删除切片（DeleteChunk）单次最多 10 个；音视频搜索类**不支持新增切片**。

## 计费

自 2026 年 1 月 4 日起正式计费，计费起点为成功创建知识库，按小时出账。费用 = **规格费用** + **模型调用费用**。

**规格费用**：标准版 0.03 元/小时；旗舰版 0.2 元/RCU/小时。变配按发生时间分段计费，同一知识库 1 个自然日最多变配 1 次。删除知识库会永久清除数据且不可恢复，用以停止计费。

**免费额度**：所有用户一次性 720 小时，仅抵扣标准版规格费用。老用户（2026-01-04 前开通）额度有效期至 2026-02-03 23:59；新用户自开通起 30 天内有效，过期作废。模型调用费用不在免费额度内。

**模型调用费用**：独立计费项，按输入 [Token](../concepts/token.md) 计费，遵循模型广场定价。

- 创建/更新：按新增内容 [Token](../concepts/token.md) 数计费，删除文件不产生费用。
- 检索：Query 向量化按输入 [Token](../concepts/token.md) 计费；Rerank 费用 = **初步召回总切片数 × 平均切片 [Token](../concepts/token.md) × 模型单价**，与最终返回切片数无关。
- 多知识库：N 个知识库 Token 消耗 × N。

**优化建议**：对精度要求不高的场景可关闭排序（消除 Rerank 费用，但降低相关性）；或调低初步向量/关键词检索 TopK（取值 10–100）减少送入 Rerank 的 Token 量。详见 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

> **注意**：免费额度仅适用于标准版；旗舰版规格费用需通过资源包或按量付费承担，且 2026-01-04 前创建但未开通服务的知识库数据将保留至 2026-06-30，逾期未开通将被永久删除。

## 使用要点

- [业务空间](../concepts/workspace.md)隔离：子账号只能操作已加入[业务空间](../concepts/workspace.md)中的知识库，主账号可操作所有[业务空间](../concepts/workspace.md)下的知识库。
- 知识库 ID：每个知识库卡片上的 `ID` 字段，用于 API 调用。
- 删除文件不退模型调用费，但删除知识库可停止规格计费。
- 命中测试会产生向量模型与排序模型的调用计费。
- 检索结果优先级：`models/` > `raw/` > `wiki/`，本文为 wiki 合成页，遇具体数值请以控制台与最新官方文档为准。

## 来源文档

- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)









