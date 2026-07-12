# application monitoring

阿里云百炼提供**应用观测**功能，用于端到端查看[业务空间](../concepts/workspace.md)内应用（[智能体应用](../concepts/agent-application.md)、[工作流](../concepts/workflow.md)应用、高代码应用）的处理流程，并获取延时、[Token](../concepts/token.md) 量等关键指标，指标更新频率为分钟级。该功能可帮助开发者追踪应用内部调用链路、查看模型响应延时与思考过程，进而优化运营效果与成本。详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的应用范围

应用观测支持以下三类应用：

- **[智能体应用](../concepts/agent-application.md)**（AgentApp）
- **[工作流](../concepts/workflow.md)应用**（WorkflowApp）
- **高代码应用**（FullCodeApp）

> **注意**：应用观测暂不支持通过 Assistant API 创建的[智能体应用](../concepts/agent-application.md)；对高代码应用，目前不支持追踪其内部调用链路，仅能观测到入口 CHAIN 节点。应用观测本身也没有 API，只能通过控制台操作。

## 前提条件与开通

首次使用需在应用观测页面右上角完成**应用观测配置**，依次执行：授权可观测链路 OpenTelemetry 服务角色权限 → 开通 OpenTelemetry 服务 → 初始化 LogStore。

- 推荐使用**主账号**操作，开通后通常分钟级生效，高峰期可能略有延迟。
- 如需**子账号**开通，主账号需为其配置 `AliyunBailianFullAccess` 全局权限、`应用观测-操作`（或 `管理员`）页面权限，并额外授予 `ram:CreateServiceLinkedRole` 系统策略（用于创建服务关联角色）。

> 子账号权限若未配置完整，开启应用观测时会失败。配置完成后需返回应用观测界面再次尝试开启。

## 使用方式

### 1. 选择被观测的应用

在应用观测页面单击「选择被观测的应用」>「添加」。若列表中看不到已创建的应用，通常是因为该应用尚未发布，或应用不属于当前[业务空间](../concepts/workspace.md)。

### 2. 开始观测

添加完成后，应用会出现在观测列表中。此后所有输入该应用的 Prompt 及相关数据、指标会被自动追踪并以分钟级频率同步。单击「关闭观测」可停止同步，重新添加后仅同步新增数据。

在「查看详情」中可查看最长 30 天内的调用记录，包括 Prompt 内容、输出、延时、调用时间和 [Token](../concepts/token.md) 量，并支持按 Request ID / Trace ID / Span ID 检索和按时间范围筛选。单击节点名称可查看详情、原始数据和标注记录。

> 列表中的 **CHAIN** 节点表示一次完整的应用内部调用追踪，支持展开。状态分为「正常」与「错误」两类。

### 3. 导出数据

在应用详情页的 Trace 列表页签右上角单击「导出数据」，可将当前筛选条件下的数据导出为 **JSONL** 或 **EXCEL** 格式。

### 4. 查看监控统计

「监控统计」页签提供性能监控图表：调用次数（含失败次数与失败率）、[Token](../concepts/token.md) 总量（全部/输入/输出）、平均单次请求 [Token](../concepts/token.md) 量、平均首 [Token](../concepts/token.md) 耗时（流式场景）、平均调用时长。支持按时间范围（最长 30 天）和聚合粒度（分钟/小时/天）查看，每个图表可放大、下载、复制。

## 数据筛选与标注

### Span 筛选模式

- **Root Span**：仅显示根节点（默认）
- **All Span**：平铺展示所有 Span
- **Model Span**：仅显示包含模型调用的 Span

### 过滤器

支持按状态（正常/错误，可按错误类型细分）、Span Name、输入、输出、延时、[Token](../concepts/token.md) 总量、输入 [Token](../concepts/token.md)、输出 [Token](../concepts/token.md)、标签等字段添加多个筛选条件，条件之间组合应用。

### 数据标注

支持对 Span 数据添加标签（布尔值/分类/数字/文本四种类型），标签与应用[评测](../concepts/evaluation.md)的标签管理共享、统一管理。标注内容自动保存，并可在 Span 列表页「标签」列查看。

### 添加到[评测](../concepts/evaluation.md)集

应用观测支持将 Span 数据直接加入[评测](../concepts/evaluation.md)集，将真实线上调用作为评测样本。配置时需选择目标评测集、导入方式（追加数据或全量覆盖）并完成字段映射。每个评测集最多支持 50 个字段映射。

## 节点类型

被观测应用在调用过程中会按操作单元生成不同类型的**节点**，节点之间可形成嵌套关系。仅在被触发或调用时才展示对应节点。完整节点类型与说明见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

### [智能体应用](../concepts/agent-application.md)节点

| 节点 | 说明 |
| --- | --- |
| CHAIN | 连接大模型节点与其他节点，处理复杂任务；作为根节点时名称为 AgentApp 或 WorkflowApp |
| AGENT | 对智能体的调用 |
| RETRIEVER | 检索操作；KnowledgeRetriever 表示在[知识库](../concepts/knowledge-base.md)中检索。子节点名称含 TextRetriever（改进 BM25，默认返回 100 个切片）、VectorRetriever（向量检索，默认返回 100 个切片） |
| REWRITER | 基于会话上下文调整原始 Prompt 以提升检索效果 |
| EMBEDDING | 将 Prompt 转为向量，[Token](../concepts/token.md) 量为本次向量化的 [Token](../concepts/token.md) 数 |
| RERANKER | 计算文本切片相似度分数并降序排列 |
| LLM | 大模型推理/文本生成，[Token](../concepts/token.md) 量 = 输入 + 输出；延时包含输出回复过程 |
| TOOL | 插件调用（官方或自定义） |
| GUARDRAIL | 阿里绿网调用；ManualIntervention 为用户干预规则，SystemIntervention 为系统干预规则 |

> 目前暂不支持观测长期记忆中的检索过程；TextRetriever 与 VectorRetriever 默认返回 100 个切片，暂不支持调整数量。

### [工作流](../concepts/workflow.md)应用节点

除上述 CHAIN、RETRIEVER、REWRITER、EMBEDDING、RERANKER、LLM、GUARDRAIL 外，还包含工作流专属节点：START（开始）、END（结束）、API、CLASSIFIER（意图分类）、TEXT_CONVERTER（文本转换）、SCRIPT（脚本转换）、CONDITION（条件判断）、FUNCTION_COMPUTE（函数计算）、APP_FLOW。

### 高代码应用节点

仅有 CHAIN（FullCodeApp）作为入口节点，目前不支持追踪其内部调用链路。若已开启观测却看不到调用量等统计数据，需排查：代码中是否使用 AgentScope-AI 的 Tracing 模块定义上报信息，以及部署时是否添加 `--telemetry enable` 参数。

## [计费](../concepts/billing.md)说明

应用观测功能本身**不收费**，但观测数据需存储在可观测链路 OpenTelemetry 服务中，相关存储费用由 OpenTelemetry 服务收取。

## 关键指标说明

- **延时（调用时长）**：对 LLM 节点，包含输出回复的完整过程。
- **[Token](../concepts/token.md) 量**：Embedding 节点为本次向量化 [Token](../concepts/token.md) 数；LLM 节点为输入 [Token](../concepts/token.md) + 输出 [Token](../concepts/token.md)。
- **数据时效**：指标更新频率为分钟级，调用记录最长可查 30 天。
- **应用总量 / 平均延时**：用于评估应用运营效果与成本，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)

















