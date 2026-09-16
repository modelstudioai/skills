# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪 LLM 应用内部执行链路、分析性能瓶颈并采集关键指标（如延时、Token 量、状态码等）。该功能面向已发布的智能体、工作流及高代码应用，数据同步频率为分钟级，不提供实时 API 接口。所有观测数据依赖可观测链路 OpenTelemetry 服务进行采集与存储。

## 支持的模型/功能

- **支持的应用类型**：  
  - [智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md)  
  - [工作流应用](raw/application-user-guide/llm-application/workflow-application.md)  
  - [高代码应用](raw/application-user-guide/llm-application/rich-code-application.md)  

- **核心可观测能力**：  
  - 调用链路追踪（Root Span / All Span / Model Span 三种视图）  
  - 节点级指标采集（延时、输入/输出 Token、状态、Request ID / Trace ID / Span ID）  
  - 交互式节点展开与原始数据查看  
  - 数据标注（布尔值、分类、数字、文本四类标签）  
  - Span 数据一键导出（JSONL / Excel）及批量导入评测集  
  - 监控统计看板（调用次数、失败率、Token 趋势、首 Token 耗时、平均调用时长）  

> **注意**：应用观测目前暂不支持[通过Assistant API创建的智能体应用](https://help.aliyun.com/zh/model-studio/what-is-assistant-api)，该限制在[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)中明确说明。

## 关键参数

| 参数 | 说明 | 来源上下文 |
|------|------|------------|
| `Request ID` / `Trace ID` / `Span ID` | 用于精准定位单次调用或子链路，可在节点详情页点击「查看 ID」获取 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `延时（调用时长）` | LLM 节点延时包含完整响应生成过程；首 Token 耗时仅适用于流式调用 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `Token 总量` | = 输入 Token + 输出 Token；Embedding 节点 Token 量仅指向量化输入长度 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `Span Name` | 如 `AgentApp`、`WorkflowApp`、`FullCodeApp`、`LLM`、`RETRIEVER` 等，标识节点语义角色 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

### 前置配置（必需）
1. 使用**主账号**（或已授权子账号）访问[应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角「应用观测配置」完成：  
   - 授权可观测链路 OpenTelemetry 服务角色权限  
   - 开通可观测链路 OpenTelemetry 服务  
   - 初始化 LogStore 存储  
   > 子账号需额外配置 `AliyunBailianFullAccess`、页面权限及 `CreateServiceLinkedRole` 策略（详见[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)常见问题章节）

### 启用观测
1. 在应用观测页点击「选择被观测的应用添加」，**仅已发布且归属当前业务空间的应用可见**；  
2. 添加后，所有新 Prompt 请求将自动追踪（分钟级同步），关闭观测即停止数据采集；  
3. 单击「查看详情」进入 Span 列表页，支持按时间范围（最长30天）、ID、关键词、延时、Token 量、标签等多维筛选；  
4. 在监控统计页签可查看聚合图表（支持按分钟/小时/天粒度切换）；  
5. 支持将 Span 批量添加至评测集（字段映射最多50个），或添加结构化标注用于后续分析。

## 限制和注意事项

- **无 API 接口**：应用观测目前不提供编程接口，所有操作均通过控制台完成；  
- **高代码应用限制**：`FullCodeApp` 类型节点仅作为根节点上报，**不支持其内部调用链路追踪**（需自行集成 AgentScope-AI Tracing 模块并启用 `--telemetry enable`）；  
- **知识库检索限制**：仅支持观测知识库（RAG）中的 `TextRetriever` 和 `VectorRetriever`，**不支持[长期记忆](../concepts/long-term-memory.md)中的检索过程**；  
- **计费说明**：功能本身免费，但底层依赖 OpenTelemetry 服务，相关日志存储与分析费用需单独承担；  
- **数据时效性**：指标更新延迟约 1–3 分钟，不适用于毫秒级诊断场景。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)


