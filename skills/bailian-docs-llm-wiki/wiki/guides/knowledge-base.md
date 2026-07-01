# knowledge base

百炼知识库基于 RAG（[检索增强生成](../concepts/rag.md)）技术，为大模型补充私有数据和最新信息。大模型在生成回答前会先从知识库中检索相关内容，从而提升回答的准确性。知识库功能仅在中国站华北2（北京）地域可用。

## 知识库规格

百炼提供两种知识库规格：

| 规格 | 最高并发 | 存储空间 | 价格 |
|------|---------|---------|------|
| 标准版 | 1 QPS（固定） | 平台存储 100 GB | 0.03 元/知识库/小时 |
| 旗舰版 | 50-10,000 QPS（1-200 RCU） | 平台存储 9,999 GB | 0.2 元/RCU/小时 |

新用户享有一次性 720 小时免费额度（仅适用于标准版），自开通之日起 30 天内有效。详细[计费](../concepts/billing.md)规则参见[知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 知识库类型

创建知识库时需选择类型（创建后不可更改）：

- **文档搜索**：适用于非结构化数据（文档、图片等）的语义检索，支持四种使用场景：基础文档问答、图文并茂回复、视觉理解（富文本文档）、极速问答
- **数据查询**：适用于结构化数据（单个 Excel/CSV 文件），支持 NL2SQL 查询
- **图片问答**：适用于图片类知识库
- **音视频搜索**：适用于音视频内容检索

## 支持的模型

知识库支持以下模型接入：

- 千问系列：QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research
- 千问VL：Max/Plus/Flash/OCR
- 千问开源版：Qwen3、Qwen2.5、Qwen2 等
- 第三方模型：DeepSeek-R1、DeepSeek-V3.1、Llama3.1、Yi-Large 等
- 调优后的自定义模型（基于千问-Plus/Turbo/VL/开源版调优）

## 创建与使用

### 构建知识库

1. 在知识库页面选择规格（标准版/旗舰版），点击创建
2. 填写基础信息并选择知识库类型
3. 配置数据来源（本地上传或 OSS 导入）
4. 设置索引参数（切片方式、向量模型、Meta 信息抽取等）

支持的文件格式包括 PDF、DOCX、TXT、Markdown、HTML、XLSX、图片、音视频等，具体限制参见[知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

### 集成方式

知识库创建后可通过以下方式集成：

- **智能体应用**：在应用配置中添加文档知识库，设置相似度阈值和权重
- **工作流应用**：将知识库节点拖入画布，配置输入变量和 TopK 参数
- **外部应用**：通过百炼 SDK 调用知识库检索能力，详见[知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)

### 知识检索服务

知识检索服务支持多知识库联合检索（最多 15 个），提供完整的检索流水线：

1. Query 改写（可选）
2. 向量检索 + 关键词检索（混合检索）
3. 排序模型（Rerank）精排
4. 加权返回最终结果

可选排序模型包括 qwen3-rerank、qwen3-rerank(hybrid)、qwen3-vl-rerank（[多模态](../concepts/multimodal.md)）。

### 知识问答服务

知识问答服务结合大模型与知识检索，支持两种检索模式：

- **极速模式**：单轮检索后直接生成回答，低延时
- **多轮智能模式**：基于 Agent 的多轮规划搜索（Agentic），自动进行意图识别和 Query 改写

支持文件预解析、拒答策略、防泄漏保护、[多模态](../concepts/multimodal.md)回复和引用来源展示等生成控制能力。

## 关键配置参数

### 索引配置

| 参数 | 说明 |
|------|------|
| 切片方式 | 推荐"智能切分"（基于语义相关性自适应切分） |
| 向量模型 | text-embedding-v4（512维）或 multimodal-embedding-v1（1024维） |
| Meta 信息抽取 | 为文本切片附加元数据（常量/变量/大模型/正则），提升检索精度 |
| 多轮对话改写 | 根据历史对话自动补全用户查询（创建后不可开启） |

### 检索配置

| 参数 | 说明 |
|------|------|
| 相似度阈值 | 仅语义相似度高于此值的切片被召回，需反复调试 |
| 初步向量检索 TopK | 向量检索阶段初步召回数量（1-100，默认 50） |
| 初步关键词检索 TopK | 关键词检索阶段初步召回数量（1-100，默认 50） |
| 最大召回数量 | 最终返回的切片数量（1-20） |
| 标签过滤 | 根据文档标签筛选检索范围 |

## RAG 效果优化

当知识召回不完整或不准确时，可按以下方向优化：

1. **检索无效（未找到相关知识）**：补充知识库内容、优化源文件排版、消除实体歧义、启用多轮对话改写
2. **召回不相关**：为文件添加标签进行过滤、定义 Meta 元数据实现结构化搜索
3. **切片不完整**：采用智能切分策略、人工检查修正切片内容
4. **重排不佳**：调低相似度阈值、增加召回片段数
5. **模型理解有误**：更换参数更多或专业能力更强的大模型

> **注意**：优化前建议先通过自动评测功能建立量化评估基线（至少 100 组测试用例），以客观衡量改进效果。

## 日志与监控

知识库检索调用日志投递到日志服务（SLS），支持调用审计、问题排查、用量统计与告警监控。首次使用需在知识库列表页开通监控配置，授权 SLS 角色权限。关键日志字段包括 request_id、pipeline_id、latency、response_code 等，详见[知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 配额与限制

| 类别 | 上限 |
|------|------|
| 知识库数量 | RDS 数据源 100 个，其他无限制 |
| 单知识库存储 | 标准版 100 GB / 旗舰版 9,999 GB |
| 文件数量 | 每[业务空间](../concepts/workspace.md) 100,000 个 |
| 检索并发 | 标准版 1 QPS / 旗舰版 50-10,000 QPS |
| 文本切片长度 | 最大 6,000 [Token](../concepts/token.md) |
| 单次召回切片数 | 最大 20 个 |

## 费用优化建议

- 关闭排序模型（Rerank）可消除排序费用，适用于精度要求不高的场景
- 降低初步召回 TopK 值可减少送入排序模型的 [Token](../concepts/token.md) 量
- 挂载多个知识库时 [Token](../concepts/token.md) 消耗按知识库数量倍增，建议精简绑定数量
- 不再使用的知识库应及时删除以停止[计费](../concepts/billing.md)

## 来源文档

- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)


