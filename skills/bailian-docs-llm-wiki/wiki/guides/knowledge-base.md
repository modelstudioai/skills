# knowledge base

阿里云百炼知识库基于 RAG（[检索增强生成](../concepts/rag.md)）技术，为大模型补充私有数据与最新信息，使应用能够准确回答特定领域问题。知识库仅能在中国站华北2（北京）地域开通和使用，提供标准版与旗舰版两种规格，并配套日志监控、API、效果优化与计费体系。

## 支持的模型与功能

知识库支持对私有数据或文件进行语义检索，可找出语义相同或相近的内容，即使关键词匹配度极低甚至为零。支持挂载到[智能体应用](../concepts/agent-application.md)、工作流应用以及通过 SDK 集成到外部应用。

支持的模型范围如下（以应用管理页面实际可选为准）：

- 预置模型：千问-QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、千问VL-Max/Plus/Flash/OCR、千问开源版（Qwen3、Qwen2.5、Qwen2 等）、第三方文本生成模型（DeepSeek-R1、DeepSeek-V3.1、abab6.5s、Llama3.1、Yi-Large 等）。
- 自定义模型：基于千问-Plus/Turbo、千问VL-Max/Plus、千问开源版等调优后的自定义模型。

知识库类型分为文档搜索、数据查询、图片问答、音视频搜索四类，单一知识库不支持同时选择多个类型。文档搜索类还细分为基础文档问答、图文并茂回复、视觉理解（富文本文档）、极速问答四种使用场景，详情可参见 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 关键参数

### 规格与并发

| 规格 | 最高检索并发 | 平台存储空间 | 价格 |
| --- | --- | --- | --- |
| 标准版 | 1 QPS（固定，不可调） | ≤ 100 GB | 0.03 元/知识库/小时 |
| 旗舰版 | 50–10,000 QPS（可调，对应 1–200 RCU） | ≤ 9,999 GB | 0.2 元/RCU/小时 |

RCU（Retrieval Compute Unit）是检索并发能力度量单位，1 RCU 约支撑最高 50 QPS。所需 RCU = 向上取整（检索峰值 QPS ÷ 50）。变配按发生时间分段计费，同一知识库 1 个自然日内最多变配 1 次。

### 向量与切片

- 向量模型：文档搜索、数据查询、音视频搜索类支持 text-embedding-v4、text-embedding-v3（均为 512 维）；图片问答类仅支持 multimodal-embedding-v1（1024 维）。向量维度不支持更改。
- 文本切片长度上限：单个切片 6,000 [Token](../concepts/token.md)；编辑切片（UpdateChunk）长度限制为 10–6,000 字符；删除切片（DeleteChunk）单次最多 10 个。
- 召回文本切片数量：单次查询最多召回 20 个切片。

### 检索参数

- 相似度阈值：仅语义相似度高于此阈值的文本切片才会被召回，阈值过高会丢弃相关切片。
- 召回片段数（K 值）：取值范围 1–20，调大可提升完整性但增加 [Token](../concepts/token.md) 消耗。
- 初步向量检索 TopK / 初步关键词检索 TopK：默认 50，取值范围 10–100，影响送入排序模型的切片数量与成本。
- 权重：仅在**同类型知识库之间生效**，用于干预多知识库召回顺序。

## 使用方式

### 创建知识库

1. 在知识库页面点击创建知识库，选择规格（标准版或旗舰版）。
2. 填写基础信息并选择知识库类型与使用场景（创建后不可更改）。
3. 配置数据来源（本地上传或从 OSS/数据连接器导入）与解析方式（电子文档解析、文档智能解析、大模型文档解析、Qwen VL 解析、音视频解析）。
4. 设置索引参数：Meta 信息抽取、Excel 表头拼装、切片方式（智能切分或按长度切分）。

> **注意**：知识库一旦创建，无法再配置 metadata 抽取，也无法更改文档切分 chunk。请在创建时一次性规划好元数据与切片策略。

完整创建流程与参数说明参见 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

### 集成到应用

- [智能体应用](../concepts/agent-application.md)：在应用配置页文档知识库右侧点击 + 添加知识库，可设置相似度阈值与权重。
- 工作流应用：将知识库节点拖入画布，配置输入变量（query）、选择固定知识库或动态引入、设置 TopK。
- 外部应用：通过阿里云百炼 SDK 调用检索能力，集成步骤参见 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

### API 调用

子账号需获取 AliyunBailianDataFullAccess 策略并加入[业务空间](../concepts/workspace.md)后才能操作知识库；主账号可操作所有[业务空间](../concepts/workspace.md)下的知识库。创建流程为：申请上传租约 → 上传文件 → 添加文件到类目 → 轮询文件解析状态（INIT/PARSING/PARSE_SUCCESS）→ 初始化知识库 → 提交索引任务 → 轮询任务状态直至 COMPLETED。

### 日志监控

检索日志由日志服务（SLS）承载，首次使用需授权角色 AliyunServiceRoleForSFMAccessSLS 并创建 LogStore。每条日志 topic 为 `log_dispatch`，包含 request_id、pipeline_id、workspace_id、latency、response_status_code、response_code 等字段。建议搭建调用量趋势、TopN 知识库排名、业务错误率与 HTTP 5xx 错误率等监控。详见 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 效果优化

当出现知识召回不完整或内容不准确时，建议先建立评测基线（至少 100 组问题，覆盖事实型/比较型/教程型/分析型），再按失败用例诊断改进。优化策略围绕 RAG 三阶段展开：

1. 建立索引：优化源文件排版（优先 Markdown、移除水印、避免复杂表格）、统一实体表述、启用多轮对话改写（创建时开启，后续无法补开）。
2. 检索召回：为文件添加标签过滤、配置元数据做结构化搜索、采用智能切分保留语义完整性、调整相似度阈值与召回片段数。
3. 生成答案：更换为能力更强的商业模型（如通义千问 Max/Plus/QwQ）、优化提示词模板（限定输出、少样本提示、内容分隔标记且 `${documents}` 只出现一次）。

> **注意**：相似度阈值过高（如 0.60）可能导致无召回结果；召回片段数并非越大越好，拼装后总长度超出大模型输入限制会被截断，推荐选择按拼装长度策略。

## 限制和注意事项

### 配额

- 知识库数量：使用 RDS 数据源上限 100，其它数据源无限制。
- 存储容量：旗舰版 9,999 GB，标准版 100 GB。
- 类目数量：每个[业务空间](../concepts/workspace.md) 500；文件数量：每个业务空间 100,000；数据表数量：每个业务空间 1,000。
- 单次导入文件数量：控制台 50（API 批量导入建议不超过 10,000）；单个文件标签数量上限 32。
- ADB-PG 向量存储单表最大行数 10,000,000，单行最大 100 KB。

### 文件格式

| 知识库类型 | 支持格式 | 限制 |
| --- | --- | --- |
| 文档搜索 | pdf/docx/doc/wps/pptx/ppt | 最大 150MB，页数 ≤ 1,000 |
| 文档搜索 | txt/markdown/html | 最大 10MB |
| 文档搜索 | xlsx/xls | 最大 10MB，10 万行以内 |
| 文档搜索 | png/jpg/jpeg/bmp/gif | 最大 20MB，短边 > 15px，长边 < 8,192px，长短边比 < 50 |
| 数据查询/图片问答 | xlsx/xls | 最大 100,000 行，列数 ≤ 100 |
| 音视频搜索 | aac/amr/flac/flv/m4a/mp3/mpeg/ogg/opus/wav/webm/wma/mp4/mkv/avi/mov/wmv | 最大 512MB |

完整配额与限制参见 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

### 计费

知识库自 2026 年 1 月 4 日起正式计费，费用由规格费用与模型调用费用两部分构成。扣费顺序为免费额度 > 资源包 > 按量付费。

- 规格费用：按运行时长累计，按小时出账。所有用户有一次 720 小时免费额度（仅抵扣标准版规格费用）；老用户免费额度截至 2026 年 2 月 3 日 23:59，新用户自开通起 30 天内有效。
- 模型调用费用：创建/更新时按新增内容 [Token](../concepts/token.md) 计费；检索时按 Query 向量化 Token + Rerank 排序 Token 计费，排序费用取决于初步召回总切片数而非最终返回数量。多知识库检索时 Token 消耗按知识库数量倍数增加。

> **注意**：2026 年 1 月 4 日前创建但未开通服务的知识库数据将保留至 2026 年 6 月 30 日，逾期未开通将被永久删除。欠费后平台存储保留 14 天、自购 ADB-PG 保留 7 天，超期数据永久删除无法恢复。

成本优化可关闭 Rerank 排序（降低精度）或调低初步向量/关键词检索 TopK（取值 10–100）。计费规则与示例详见 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 来源文档

- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)


