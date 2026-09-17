# application monitoring

应用监控（Application Monitoring）是百炼平台提供的可观测性能力，用于端到端追踪 LLM 应用的内部执行链路、性能指标与模型行为。它支持对智能体、工作流和高代码三类应用的调用过程进行细粒度观测，覆盖向量生成、知识检索、大模型推理、插件调用等关键节点，并提供延时、[Token](../concepts/token.md) 量、错误状态等分钟级聚合指标。该功能依赖 OpenTelemetry 基础设施，当前仅提供控制台界面，**暂无公开 API** [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：  
  - [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)  
  - [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)  
  - [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)  

- **可观测节点类型**（按应用类型分类）：  
  - 通用节点：`CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`GUARDRAIL`、`TOOL`（插件）、`AGENT`  
  - 工作流专属节点：`START`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`、`END`  
  - 高代码应用限制：`FullCodeApp` 节点仅作为入口展示，**不支持其内部调用链路追踪** —— 此限制在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 的“高代码应用”章节中明确说明。

> **注意**：文档中提及“[通过Assistant API创建的智能体应用](https://help.aliyun.com/zh/model-studio/what-is-assistant-api)”明确**不被支持**，但未说明是否属于 Agent 1.0 范畴；实践中应以控制台实际添加结果为准，避免依赖 Assistant API 创建的应用启用观测。

## 关键参数

| 参数 | 说明 | 来源依据 |
|------|------|----------|
| **Request ID / Trace ID / Span ID** | 用于跨系统定位单次请求全链路，可在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “使用方法 → 查看详情”节 |
| **延时（调用时长）** | 指从请求进入应用到完整响应返回的总耗时（含流式首 [Token](../concepts/token.md) 时间）；LLM 节点延时包含输出生成全过程 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “附录 → 节点类型 → LLM”说明 |
| **[Token](../concepts/token.md) 总量** | = 输入 Token 数 + 输出 Token 数；Embedding 节点 Token 量特指向量化输入的 Token 数 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “附录 → 节点类型”各节点说明 |
| **状态（Status）** | 仅含 `正常` 或 `错误`；错误可进一步按类型细分（如 Guardrail 触发、LLM 调用失败等） | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “使用方法 → 查看详情”节 |

## 使用方式

1. **前提配置（主账号推荐）**：  
   - 单击应用观测页右上角「应用观测配置」，依次完成：  
     - 授权可观测链路 OpenTelemetry 服务角色权限  
     - 开通可观测链路 OpenTelemetry 服务  
     - 初始化 LogStore 存储（主账号操作通常分钟级生效）  
   - 子账号需额外配置 `AliyunBailianFullAccess` + 页面权限 + `CreateServiceLinkedRole` 策略（详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “常见问题”节）

2. **启用观测**：  
   - 进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击「选择被观测的应用添加」  
   - **仅已发布且归属当前业务空间的应用可见**；未发布应用需先通过「管理发布」操作  

3. **数据查看与分析**：  
   - 支持三种 Span 筛选模式：`Root Span`（默认）、`All Span`、`Model Span`  
   - 可基于状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合过滤  
   - 支持按 Request ID/Trace ID/Span ID 搜索，时间范围最长 30 天  
   - 「监控统计」页签提供调用次数、失败率、Token 趋势、平均首 Token 耗时、平均调用时长等图表（支持分钟/小时/天粒度聚合）

4. **高级能力**：  
   - **导出数据**：Trace 列表页右上角支持 JSONL 或 Excel 格式导出  
   - **添加到评测集**：批量选择 Span，映射字段至评测集（最多 50 个字段），支持追加或覆盖  
   - **数据标注**：为 Span 添加布尔值/分类/数字/文本标签，与评测标签体系共享  

## 限制和注意事项

- **功能限制**：  
  - 当前**无开放 API**，所有操作必须通过控制台完成 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)  
  - 不支持通过 Assistant API 创建的智能体应用  
  - 高代码应用仅暴露 `FullCodeApp` 入口节点，**无法观测其内部逻辑**（如自定义 Python 函数、HTTP 调用等）  
  - [长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程**不可观测**  

- **技术限制**：  
  - 数据同步频率为**分钟级**，不适用于毫秒级实时诊断  
  - Embedding/Retriever 默认返回 100 个文本切片，**数量不可配置**  
  - 子账号开通需严格遵循权限清单，缺一不可（尤其 `CreateServiceLinkedRole` 策略易被遗漏）  

- **计费说明**：  
  - 应用监控功能本身**不收费**  
  - 产生的 Trace 数据存储于 OpenTelemetry 服务，按该服务计费规则收取存储与读写费用（参见 [OpenTelemetry 计费说明](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)）  

- **高代码应用特殊要求**：  
  > **注意**：若高代码应用开启观测后无数据上报，需确认两点：① 代码中已集成 AgentScope-AI 的 [`Tracing` 模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing) 并正确埋点；② 部署命令中已添加 `--telemetry enable` 参数 —— 此要求在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “常见问题”末尾明确指出，缺失任一将导致数据丢失。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)


