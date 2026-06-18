# knowledge base

百炼知识库基于 RAG（检索增强生成）技术，为大模型补充私有数据和最新信息。大模型在生成回答前会先从知识库中检索相关内容，从而提升回答的准确性。知识库提供标准版和旗舰版两种规格，支持文档搜索、数据查询、图片问答、音视频搜索等多种类型。

## 支持的模型

知识库支持以下模型接入：

- **预置模型**：千问 QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、千问VL-Max/Plus/Flash/OCR、千问开源版（Qwen3、Qwen2.5、Qwen2 等）、第三方文本生成模型（DeepSeek-R1、DeepSeek-V3.1 等）
- **自定义模型**：基于千问 Plus/Turbo、千问VL-Max/Plus、千问开源版等模型调优后的自定义模型

> **注意**：以上列表随时可能更新，请以控制台应用管理页面实际可选的模型为准。

## 知识库类型与使用场景

创建知识库时需选择知识库类型，创建后不可更改。详见[知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

| 类型 | 适用场景 |
|------|---------|
| **文档搜索 — 基础文档问答** | 纯文本文档的语义检索 |
| **文档搜索 — 图文并茂回复** | 需要返回图文混排内容 |
| **文档搜索 — 视觉理解（富文本文档）** | 含复杂排版、图表、公式的 PDF/图片，使用 qwen3 多模态向量模型 |
| **文档搜索 — 极速问答** | 高度结构化或简单文档（FAQ、产品参数表等），低延时优化 |
| **数据查询** | 结构化数据（单个 Excel/CSV），最多 1 篇文件 |
| **图片问答** | 图片类数据，使用 multimodal-embedding-v1 向量模型 |
| **音视频搜索** | 音视频文件，支持语音识别、视频帧提取和剧情解析 |

## 索引配置

索引配置决定数据的处理与存储方式，直接影响检索效果。核心配置项包括：

### Meta 信息抽取

为文本切片附加元数据（key-value 键值对），显著提升检索准确性。支持常量、变量（file_name/cat_name）、大模型提取、正则匹配、关键词搜索五种取值方式。元数据可配置是否参与检索和模型回复。

> **注意**：知识库创建后无法再配置 metadata 抽取，需在创建时决定。

### 切片方式

- **智能切分（推荐）**：基于语义相关性自适应切分，大多数文件可获得最佳检索效果
- **按长度切分**：适合对 Token 数量有严格要求的场景，需设置最大分段长度和重叠字符数

> **注意**：知识库创建后无法更改切片方式。

### 向量模型

| 知识库类型 | 支持的向量模型 | 向量维度 |
|-----------|--------------|---------|
| 文档搜索/数据查询/音视频搜索 | text-embedding-v4、text-embedding-v3 | 512 维 |
| 图片问答 | multimodal-embedding-v1 | 1024 维 |

## 集成方式

知识库创建后，可通过以下方式集成到业务中：

1. **智能体应用**：在应用配置中添加文档知识库，设置相似度阈值和权重
2. **工作流应用**：将知识库节点拖入画布，配置输入变量和 TopK 参数
3. **外部应用（API）**：通过百炼 SDK 调用知识库检索能力，详见[知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)

### API 调用前置条件

- 子账号需获取 AliyunBailianDataFullAccess 策略并加入[业务空间](../concepts/workspace.md)
- 安装最新版百炼 SDK
- 配置 `ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET` 和 `WORKSPACE_ID` 环境变量

## RAG 效果优化

当出现知识召回不完整或内容不准确时，可针对 RAG 三个核心阶段进行优化。详见[RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

### 检索无效：未找到相关知识

- 补充知识库中缺失的相关知识
- 优化源文件内容与排版（推荐 Markdown 格式，避免复杂表格，移除水印）
- 保持提示词与源文件语言一致
- 消除实体歧义，统一表述
- 启用"多轮对话改写"，根据历史对话自动补全用户查询

### 检索无效：召回不相关

- **标签过滤**：为文件添加标签，检索前根据标签筛选文件
- **元数据提取**：将产品名称等标识信息作为元数据嵌入切片，实现结构化搜索前置过滤

### 切片质量问题

切片过短导致语义缺失、过长导致主题干扰、语义截断导致内容不完整。建议采用智能切分策略，并在导入后人工检查和修正切片内容。

### 重排与召回参数调整

- **相似度阈值**：过高会丢弃相关切片，建议通过命中测试反复调试
- **召回片段数（TopK）**：对列举、总结、比较类问题适当增大（如 K=20），或选择"按拼装长度"策略
- **模型选择**：简单查询用千问 Flash/Turbo，复杂推理用千问 Max/QwQ，长文档用千问 Long/Plus

### 提示词优化

- 在提示词中限定输出格式和行为（如禁止编造答案）
- 使用少样本提示（Few-Shot Prompting）提供问答示例
- 将 `${documents}` 变量与提示词明确分隔，且只出现一次

## 配额与限制

关键配额如下，完整列表见[知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

| 项目 | 限制 |
|------|------|
| 知识库数量（RDS 数据源） | 每账号 100 个 |
| 标准版存储 | 100 GB |
| 旗舰版存储 | 9,999 GB |
| 每[业务空间](../concepts/workspace.md)文件数 | 100,000 |
| 每[业务空间](../concepts/workspace.md)类目数 | 500 |
| 单文本切片长度 | 最大 6,000 Token |
| 单次召回切片数 | 最多 20 个 |
| 标准版检索并发 | 1 QPS（固定） |
| 旗舰版检索并发 | 50–10,000 QPS（1–200 RCU） |

### 支持的文件格式

- **文档搜索**：PDF/DOCX/DOC/WPS/PPTX/PPT（最大 150MB，1000 页）、TXT/Markdown/HTML（最大 10MB）、XLSX/XLS（最大 10MB，10 万行）、图片（最大 20MB）
- **音视频搜索**：AAC/MP3/MP4/MKV/AVI 等（最大 512MB）
- **数据查询/图片问答**：XLSX/XLS（最大 10 万行，100 列）

## 计费说明

知识库费用由**规格费用**和**模型调用费用**两部分构成。详见[知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

### 规格费用

| 规格 | 最高并发 | 存储空间 | 价格 |
|------|---------|---------|------|
| 标准版 | 1 QPS | 100 GB | 0.03 元/知识库/小时 |
| 旗舰版 | 50–10,000 QPS | 9,999 GB | 0.2 元/RCU/小时 |

- **免费额度**：所有用户一次性 720 小时标准版免费额度（新用户 30 天有效）
- **资源包**：支持预付费资源包，标准版最低 20 元/月，旗舰版最低 139 元/月

### 模型调用费用

- **创建/更新**：调用向量模型对内容向量化，按新增 Token 数计费
- **检索**：Query 向量化 + Rerank 排序费用，排序费用取决于初步召回总切片数
- **多知识库检索**：Token 消耗按知识库数量倍增

费用优化建议：关闭不必要的排序功能，或降低初步向量/关键词检索 TopK 值。

### 欠费处理

- 平台存储：欠费后 14 天内补缴可恢复，第 15 天数据永久删除
- 自购 ADB-PG：欠费后 7 天内补缴可恢复，第 8 天数据永久删除

## 日志与监控

知识库检索调用以日志形式投递到日志服务（SLS），支持调用审计、问题排查和用量统计。详见[知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

核心日志字段包括 `request_id`（请求 ID）、`pipeline_id`（知识库 ID）、`latency`（耗时毫秒）、`response_status_code`（HTTP 状态码）、`response_code`（业务响应码）、`request_body` 和 `response_body`（请求/响应体 JSON）。

开通方式：在知识库列表页右上方点击"监控配置"，完成日志服务授权和 LogStore 创建即可。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)


