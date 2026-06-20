# application monitoring

应用观测是阿里云百炼平台提供的端到端可观测能力，用于追踪应用内部调用链路、查看模型响应延时与思考过程，并获取 Token 量等关键指标。该功能基于 OpenTelemetry 实现，数据更新频率为分钟级，支持智能体应用、工作流应用和高代码应用三种应用类型。

> **注意**：应用观测目前暂无 API，且不支持通过 Assistant API 创建的智能体应用。

## 支持的应用类型

根据[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)文档，当前支持以下三类应用：

- **智能体应用** -- 支持完整的调用链路追踪，包括 CHAIN、AGENT、RETRIEVER、LLM、TOOL、GUARDRAIL 等节点类型
- **工作流应用** -- 除智能体应用支持的节点外，还支持 START、END、API、CLASSIFIER、SCRIPT、CONDITION 等工作流特有节点
- **高代码应用** -- 仅显示 FullCodeApp 根节点，目前不支持追踪内部调用链路

## 前提条件与开通

首次使用应用观测需完成以下配置（建议使用主账号操作）：

1. 授权可观测链路 OpenTelemetry 服务角色权限
2. 开通可观测链路 OpenTelemetry 服务
3. 初始化可观测链路 OpenTelemetry 存储 LogStore

开通后通常分钟级生效。如需使用子账号开通，需为其配置 `AliyunBailianFullAccess` 权限、`应用观测-操作`页面权限以及 `ram:CreateServiceLinkedRole` 策略，详细步骤参见[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)中的常见问题部分。

## 核心功能

### 调用链路追踪

添加被观测应用后，所有 Prompt 输入及相应的数据和指标将被自动追踪。每条追踪记录包含：

- **输入/输出内容**：完整的 Prompt 和模型回复
- **延时**：各节点的处理耗时（LLM 节点延时包含输出回复过程）
- **Token 量**：输入 Token 数 + 输出 Token 数
- **调用时间**和**状态**（正常/错误）

支持通过 Request ID、Trace ID 或 Span ID 进行精确搜索，以及按时间范围筛选。

### 节点体系

应用观测将每次调用分解为多种类型的节点（Span），形成嵌套的调用树结构：

| 节点类型 | 说明 |
|---------|------|
| CHAIN | 根节点，串联各子节点；根节点名称为 AgentApp 或 WorkflowApp |
| AGENT | 智能体调用 |
| RETRIEVER | 检索操作，包括 TextRetriever（BM25）和 VectorRetriever |
| REWRITER | 基于上下文自动改写 Prompt 以提升检索效果 |
| EMBEDDING | 将 Prompt 转化为向量 |
| RERANKER | 对检索结果按相似度重排序 |
| LLM | 大模型推理/生成调用 |
| TOOL | 插件调用（官方或自定义） |
| GUARDRAIL | 内容安全检测（阿里绿网） |

### Span 筛选与过滤

提供三种筛选模式：

- **Root Span**：仅显示根节点（默认）
- **All Span**：平铺展示所有 Span
- **Model Span**：仅显示模型调用 Span

过滤器支持按状态、Span Name、输入/输出内容、延时、Token 量（总量/输入/输出）及自定义标签进行多条件筛选。

### 监控统计

在应用详情页的监控统计页签可查看性能数据，包括调用次数、失败率、Token 总量、平均单次请求 Token 量、平均首 Token 耗时和平均调用时长。支持最长 30 天的时间范围，聚合粒度可选分钟、小时或天。

### 数据导出

支持将当前筛选条件下的 Trace 数据导出为 JSONL 或 EXCEL 格式。

### 数据标注

支持对 Span 数据添加自定义标签（布尔值、分类、数字、文本四种类型），标注内容自动保存，与应用评测的标签管理功能共享。

### 添加到评测集

可将 Span 数据批量导入评测集，支持追加数据或全量覆盖两种方式，并通过字段映射将 Span 参数对应到评测集字段（每个评测集最多 50 个字段映射）。这使得真实线上调用数据可直接用于构建评测样本，详见[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 计费说明

应用观测功能本身不收费，但底层依赖的可观测链路 OpenTelemetry 服务会产生存储费用。

## 限制与注意事项

- 应用观测暂无 API 接口
- 不支持通过 Assistant API 创建的智能体应用
- 高代码应用不支持追踪内部调用链路
- 不支持观测长期记忆中的检索过程
- 检索节点（TextRetriever/VectorRetriever）默认返回 100 个文本切片，暂不支持数量调整
- 关闭观测后追踪数据停止同步，重新添加后仅同步新增数据
- 高代码应用需在部署时添加 `--telemetry enable` 参数并在代码中定义上报信息

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)


