# knowledge base

阿里云百炼知识库基于 RAG（[检索增强生成](../concepts/rag.md)）技术，为大模型补充私有数据和最新信息，使其在生成回答前先从知识库中检索相关内容，从而提升回答的准确性。知识库支持文档搜索、数据查询、图片问答、音视频搜索等多种类型，可集成到智能体应用、工作流应用或外部应用中。

## 支持的模型

知识库支持多种预置模型和自定义模型：

- **预置模型**：千问-QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research，千问VL-Max/Plus/Flash/OCR，千问开源版（Qwen3、Qwen2.5 等），第三方文本生成模型（DeepSeek-R1、DeepSeek-V3.1 等）
- **自定义模型**：基于千问-Plus/Turbo、千问VL-Max/Plus、千问开源版调优后的模型

详细的模型列表和配置方式请参见 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 知识库类型与规格

### 知识库类型

创建知识库时需选择类型（创建后不可更改）：

- **文档搜索**：适用于企业内部文档、产品手册等非结构化数据的检索。包含基础文档问答、图文并茂回复、视觉理解（富文本文档）、极速问答四种使用场景
- **数据查询**：适用于结构化数据（单个 Excel 或 CSV 文件）
- **图片问答**：支持 multimodal-embedding-v1 模型
- **音视频搜索**：支持音视频文件的语音识别、视频帧提取和剧情解析

### 规格对比

| 规格 | 最高并发 | 存储空间 | 价格 |
|------|---------|---------|------|
| 标准版 | 1 QPS（固定） | 平台存储 ≤ 100 GB | 0.03 元/知识库/小时 |
| 旗舰版 | 50-10,000 QPS（1-200 RCU） | 平台存储 ≤ 9,999 GB | 0.2 元/RCU/小时 |

标准版适用于个人/小规模和 PoC 环境，旗舰版适用于高并发生产级环境。完整计费规则请参见 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 创建与配置

### 快速开始

1. 进入知识库页面，选择规格后创建知识库
2. 填写名称和描述，上传文件
3. 将知识库关联到智能体应用、工作流应用或通过 SDK 集成到外部应用

### 关键索引配置

创建知识库时需配置以下索引参数（创建后不可更改）：

- **切片方式**：推荐使用**智能切分**，系统会基于语义相关性自适应选择切片点，保持语义完整性。也支持按长度切分
- **Meta 信息抽取**：为文本切片附加元数据（key-value 键值对），支持常量、变量、大模型、正则、关键词搜索五种取值方法，可显著提升检索精准度
- **向量模型**：文档搜索类支持 text-embedding-v4 和 text-embedding-v3；图片问答类支持 multimodal-embedding-v1
- **向量存储**：可使用平台存储或自购 ADB-PG

### 检索参数调优

- **相似度阈值**：仅语义相似度高于此阈值的文本才会被召回，设置过高可能导致相关内容被过滤
- **召回片段数（TopK）**：控制最终返回的文本切片数量（取值 1-20），对于需要总结或比较的复杂问题建议适当增大
- **权重**：关联多个知识库时，可按重要程度分配权重影响召回顺序

## RAG 效果优化

当出现知识召回不完整或内容不准确时，可按以下诊断方向进行优化。详细策略请参见 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

### 检索阶段

- **检索无效（无结果）**：补充知识库内容、优化源文件排版（优先使用 Markdown）、消除实体歧义、启用多轮对话改写
- **检索无效（结果不相关）**：为文件添加标签进行过滤、定义元数据进行结构化搜索
- **切片不完整**：采用智能切分策略、人工检查和修正切片内容

### 排序与生成阶段

- **重排不佳**：调整相似度阈值、增加召回片段数、使用"按拼装长度"策略
- **模型理解有误**：更换更强的生成模型（如通义千问 Max）、优化提示词模板（添加输出限定、Few-Shot 示例、内容分隔标记）

> **注意**：建议在优化前建立评估基线，创建至少 100 组问题的评测集，覆盖事实型、比较型、教程型、分析型问题，以客观衡量优化效果。

## 配额与限制

主要限制如下（完整限制请参见 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)）：

| 类别 | 上限 |
|------|------|
| 文件数量（每业务空间） | 100,000 |
| 单文件大小（PDF/DOCX） | 150 MB，≤ 1,000 页 |
| 单文件大小（TXT/MD/HTML） | 10 MB |
| 文本切片长度 | 6,000 Token |
| 单次召回切片数 | 20 |
| 标准版并发 | 1 QPS |
| 旗舰版并发 | 50-10,000 QPS |

## 计费说明

知识库总费用由**规格费用**（运行时长）和**模型调用费用**（向量化 + 排序）两部分构成：

- **规格费用**：标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时。新用户享 720 小时免费额度（30 天内有效，仅限标准版）
- **模型调用费用**：创建/更新时调用向量模型，检索时调用向量模型和排序模型。关联 N 个知识库时，Token 消耗量按 N 倍计算
- **费用优化**：可关闭排序功能或降低初步召回参数（初步向量检索 TopK 和初步关键词检索 TopK）以减少排序模型的 Token 消耗

预付费资源包可进一步降低成本，具体规格和价格请参见 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 日志与监控

知识库所有检索调用均会以日志形式投递到日志服务（SLS），支持调用审计、问题排查和用量统计。主要字段包括 `request_id`、`pipeline_id`（知识库 ID）、`latency`（耗时）、`response_code`（业务响应码）、`request_body` 和 `response_body` 等。详细的字段说明和使用场景请参见 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## API 集成

通过阿里云百炼 SDK 可实现知识库的程序化操作，主要流程：

1. 安装百炼 SDK，配置 AccessKey 和业务空间 ID
2. 申请文件上传租约 → 上传文件 → 添加到类目
3. 等待文件解析完成 → 初始化知识库 → 提交索引任务
4. 通过 Retrieve API 进行检索

> **注意**：API 操作仅适用于文档搜索类知识库。子账号需获取 AliyunBailianDataFullAccess 策略权限。

完整的示例代码（Python/Java）和接口说明请参见 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)


