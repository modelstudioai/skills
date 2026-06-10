# Application Monitoring

应用观测是阿里云百炼平台提供的端到端可观测能力，用于追踪应用内部调用链路、查看模型响应延时与思考过程，并获取 Token 量等关键指标。该功能基于可观测链路 OpenTelemetry 服务，数据更新频率为分钟级，目前暂无 API 接口。

## 支持的应用类型

根据[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)文档，当前支持以下三类应用：

- **智能体应用**
- **工作流应用**
- **高代码应用**

> **注意**：通过 Assistant API 创建的智能体应用目前不支持应用观测。

## 前提条件

首次使用前需完成以下初始化步骤（建议使用主账号操作，开通后通常分钟级生效）：

1. 授权可观测链路 OpenTelemetry 服务角色权限
2. 开通可观测链路 OpenTelemetry 服务
3. 初始化可观测链路 OpenTelemetry 存储 LogStore

如需使用子账号开通，需为其配置 `AliyunBailianFullAccess` 权限、`应用观测-操作`页面权限，以及 `ram:CreateServiceLinkedRole` 系统策略。

## 核心功能

### 调用链路追踪

在[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)页面添加被观测应用后，所有输入的 Prompt 及相应数据会被自动追踪。列表中的 **CHAIN** 节点表示一次完整的应用内部调用，支持展开查看子节点。

支持通过 **Request ID**、**Trace ID** 或 **Span ID** 进行搜索，以及按时间范围筛选。

### Span 筛选模式

| 模式 | 说明 |
|------|------|
| **Root Span** | 仅显示根节点（默认模式） |
| **All Span** | 显示所有 Span，平铺展示 |
| **Model Span** | 仅显示包含模型调用的 Span |

### 过滤器

支持按以下条件组合筛选：

- **状态**：正常、错误（属于/不属于）
- **Span Name**、**输入**、**输出**：关键词匹配（包含/不包含）
- **延时**（毫秒）、**Token 总量**、**输入/输出 Token**：数值比较
- **标签**：根据标签类型支持不同比较方式

### 监控统计

应用详情页的**监控统计**页签提供以下指标（最长 30 天，支持按分钟/小时/天聚合）：

- 调用次数、失败次数与失败率
- Token 总量（全部/输入/输出）
- 平均单次请求 Token 量
- 平均首 Token 耗时（流式调用场景）
- 平均调用时长

### 数据导出

支持将当前筛选条件下的 Trace 数据导出为 JSONL 或 EXCEL 格式。

### 数据标注

支持对 Span 数据添加自定义标签（布尔值、分类、数字、文本），标签与应用评测的标签管理共享，标注内容自动保存。

### 添加到评测集

支持将 Span 数据批量添加到评测集，可选择追加或全量覆盖，每个评测集最多支持 50 个字段映射。

## 支持的节点类型

节点仅在被触发时展示。以下为主要节点类型，详细说明参见[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)原文附录。

| 节点类型 | 说明 | 适用应用 |
|----------|------|----------|
| **CHAIN** | 连接多个节点实现复杂任务处理，根节点名称为 AgentApp 或 WorkflowApp | 智能体、工作流 |
| **AGENT** | 智能体调用 | 智能体 |
| **LLM** | 大模型推理/文本生成，Token 量 = 输入 + 输出，延时包含输出过程 | 智能体、工作流 |
| **RETRIEVER** | 检索操作，子节点含 TextRetriever（BM25）和 VectorRetriever | 智能体、工作流 |
| **EMBEDDING** | 将 Prompt 转化为向量 | 智能体、工作流 |
| **RERANKER** | 按相似度分数对文本切片降序排列 | 智能体、工作流 |
| **REWRITER** | 基于上下文调整 Prompt 以提升检索效果 | 智能体、工作流 |
| **TOOL** | 插件调用（官方/自定义） | 智能体 |
| **GUARDRAIL** | 阿里绿网内容安全检测 | 智能体、工作流 |
| **API / CLASSIFIER / SCRIPT / CONDITION** 等 | 工作流专属节点 | 工作流 |

> **注意**：高代码应用目前仅支持观测 FullCodeApp 触发记录，不支持追踪其内部调用链路。

## 计费说明

- 应用观测功能本身**不收费**
- 数据存储依赖可观测链路 OpenTelemetry 服务，需支付该服务的存储费用

## 限制与注意事项

- 应用观测目前暂无 API
- 不支持观测长期记忆中的检索过程
- TextRetriever 和 VectorRetriever 默认返回 100 个文本切片，暂不支持数量调整
- 关闭观测后数据停止同步，重新添加仅同步新增数据
- 高代码应用需在代码中定义上报信息（可使用 AgentScope-AI 的 Tracing 模块），并在部署时添加 `--telemetry enable` 参数

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)





