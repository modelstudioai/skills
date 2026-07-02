# knowledge base

百炼知识库基于 RAG（检索增强生成）技术，为大模型补充私有数据和最新信息。大模型在生成回答前先从知识库中检索语义相关的内容，从而提升回答准确性。知识库支持文档搜索、数据查询、图片问答、音视频搜索四种类型，提供标准版（0.03 元/小时）和旗舰版（0.2 元/RCU/小时）两种规格。

> **注意**：知识库功能仅能在中国站**华北2（北京）**地域开通和使用，其他地域不支持。

## 支持的模型

知识库可关联以下模型使用：

- **预置模型**：千问-QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、千问VL-Max/Plus/Flash/OCR、千问开源版（Qwen3、Qwen2.5、Qwen2 等）、第三方文本生成模型（DeepSeek-R1、DeepSeek-V3.1 等）
- **自定义模型**（基于千问-Plus/Turbo、千问VL-Max/Plus、千问开源版调优后的模型）

模型列表随时可能更新，以控制台应用管理页面实际可选的模型为准。详见[知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 知识库类型与使用场景

创建知识库时需选择类型，创建后不可更改：

| 类型 | 适用场景 | 数据来源 |
|------|---------|---------|
| 文档搜索（基础文档问答） | 纯文本文档的语义检索 | 本地上传 / OSS 导入 |
| 文档搜索（图文并茂回复） | 需要返回图文混排内容 | 本地上传 / OSS 导入 |
| 文档搜索（视觉理解） | 含复杂排版、图表、公式的 PDF/图片，使用[多模态](../concepts/multimodal.md)向量模型 | 本地上传 / OSS 导入 |
| 文档搜索（极速问答） | FAQ、产品参数表等高度结构化文档，低延时 | 本地上传 / OSS 导入 |
| 数据查询 | 结构化数据（单个 Excel/CSV） | 单文件 |
| 图片问答 | 图片内容理解 | Excel/图片 |
| 音视频搜索 | 音视频内容检索 | 音视频文件 |

## 集成方式

知识库创建后，可通过三种方式集成到业务中：

**[智能体应用](../concepts/agent-application.md)**：在应用配置页添加知识库，设置相似度阈值和权重。多知识库场景下，权重仅在同类型知识库之间生效。

**工作流应用**：将知识库节点拖入画布，配置输入变量和 TopK 参数，连接大模型节点。支持固定知识库或通过 `CodeList` 变量动态引入。

**外部应用（API）**：通过百炼 SDK 调用知识库检索能力。需先获取 AccessKey 和[业务空间](../concepts/workspace.md) ID，安装最新版 SDK。子账号需获取 `AliyunBailianDataFullAccess` 策略权限。完整对接步骤参见[知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 知识检索与知识问答服务

除了通过应用集成，百炼还提供独立的检索和问答服务：

**知识检索服务**支持单知识库或多知识库联合检索（最多 15 个），提供 Query 改写、混合检索（向量 + 关键词）与排序模型的完整流水线。每个知识库可独立配置向量召回数、排序模型、相似度阈值等参数。详见[知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

**知识问答服务**基于大模型结合知识检索生成自然语言回答，提供两种检索模式：
- **极速模式**：单轮检索后直接生成，适合简单明确的问题
- **多轮智能模式**（Agentic）：自动进行意图识别、Query 改写、知识库路由，适合复杂问题

## 索引配置

创建知识库时的索引配置直接影响检索效果：

**文档解析方式**：电子文档解析（最快，不支持插图）、文档智能解析（识别插图生成文本摘要）、大模型文档解析（深度理解图表，耗时较长）、Qwen VL 解析（专用于图片）、音视频解析（语音识别 + 视频帧提取 + 剧情解析）。

**切片方式**：推荐使用**智能切分**，基于语义相关性自适应切分，避免固定长度切分导致的语义截断。单个切片最大 6,000 [Token](../concepts/token.md)。

**向量模型**：文档搜索/数据查询/音视频搜索类支持 text-embedding-v4（512 维）和 text-embedding-v3（512 维）；图片问答类仅支持 multimodal-embedding-v1（1024 维）。视觉理解场景自动使用 qwen3 [多模态](../concepts/multimodal.md)向量模型。

**Meta 信息抽取**：为文本切片附加元数据（key-value），提升检索精准度。支持常量、变量（file_name/cat_name）、大模型抽取、正则抽取四种方式。知识库创建后无法再配置此项。

**多轮对话改写**：根据历史对话自动补全用户查询，需在创建知识库时开启，创建后无法追加。

## RAG 效果优化

当知识召回不完整或不准确时，可按以下方向排查和优化。详见[RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

**检索无效（未找到相关知识）**：
- 补充知识库中缺失的相关内容
- 优化源文件排版（层次分明、去水印、避免复杂表格、优先 Markdown）
- 使提示词语言与源文件语言一致
- 统一实体表述，消除歧义
- 启用多轮对话改写

**召回知识不相关**：
- 使用**标签过滤**按文件类别筛选
- 使用**元数据**进行结构化搜索，精准定位目标文件

**切片不完整**：
- 采用智能切分策略
- 人工检查并修正异常切片

**重排不佳**：
- 适当降低相似度阈值，避免丢弃相关切片
- 增大召回片段数（K 值），或选择"按拼装长度"策略

**模型理解有误**：
- 更换参数更多或专业能力更强的模型（如从开源版换到千问 Max/Plus）
- 优化系统提示词

## 配额与限制

| 资源 | 限制 |
|------|------|
| 知识库数量（RDS 数据源） | 每主账号 100 个 |
| 知识库存储（标准版/旗舰版） | 100 GB / 9,999 GB |
| 每[业务空间](../concepts/workspace.md)类目数 | 500 |
| 每[业务空间](../concepts/workspace.md)文件数 | 100,000 |
| 单次控制台导入文件数 | 50 |
| 单文件标签数 | 32 |
| 单切片最大 [Token](../concepts/token.md) | 6,000 |
| 单次检索最大召回切片 | 20 |
| 检索并发（标准版/旗舰版） | 1 QPS / 50-10,000 QPS |

支持的文件格式：PDF/DOCX/DOC/WPS/PPTX/PPT（最大 150 MB，1000 页内）、TXT/Markdown/HTML（最大 10 MB）、XLSX/XLS（最大 10 MB，10 万行内）、图片 PNG/JPG/BMP/GIF（最大 20 MB）、音视频（最大 512 MB）。

完整配额信息参见[知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

## [计费](../concepts/billing.md)说明

知识库总费用 = 规格费用 + 模型调用费用。

**规格费用**按运行时长[计费](../concepts/billing.md)，按小时出账：标准版 0.03 元/知识库/小时，旗舰版 0.2 元/RCU/小时（1 RCU 约支撑 50 QPS）。新用户有 720 小时免费额度（仅限标准版，开通后 30 天内有效）。也可购买预付费资源包降低成本。

**模型调用费用**包含向量化和 Rerank 排序两部分。排序费用取决于**初步召回的总切片数**而非最终返回数量，是检索费用的主要部分。挂载 N 个知识库时，[Token](../concepts/token.md) 消耗按 N 倍计算。

**费用优化建议**：对精度要求不高的场景可关闭排序；降低初步检索 TopK 值可减少排序 Token 消耗。详见[知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 日志与监控

知识库的检索调用日志投递到日志服务（SLS），支持调用审计、问题排查和用量统计。首次使用需在知识库列表页开启监控配置，授权 SLS 角色权限并创建 LogStore。

关键日志字段：`request_id`（请求 ID）、`pipeline_id`（知识库 ID）、`latency`（耗时毫秒）、`response_code`（业务响应码）、`request_body` / `response_body`（请求/响应 JSON）。

建议搭建调用量趋势、TopN 知识库排名等仪表盘，并对业务错误率和 HTTP 5xx 错误率设置告警。详见[知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)


