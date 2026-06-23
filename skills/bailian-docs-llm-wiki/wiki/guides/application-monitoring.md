# application monitoring

应用观测是阿里云百炼平台提供的端到端应用调用链路追踪与性能监控功能。通过该功能，开发者可以查看[业务空间](../concepts/workspace.md)内百炼应用的完整处理流程（包括向量生成、向量检索和大模型调用等环节），并获取延时、Token 用量等关键指标。该功能基于可观测链路 OpenTelemetry 服务，数据更新频率为分钟级。

## 支持的应用类型

应用观测支持以下三种应用类型：

- **智能体应用**
- **工作流应用**
- **高代码应用**

> **注意**：通过 Assistant API 创建的智能体应用暂不支持应用观测。

详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 原始文档。

## 前提条件

首次使用应用观测前，需要完成以下初始化步骤：

1. 授权可观测链路 OpenTelemetry 服务角色权限
2. 开通可观测链路 OpenTelemetry 服务
3. 初始化可观测链路 OpenTelemetry 存储 LogStore

> **注意**：建议使用主账号操作。开通后通常分钟级生效，高峰期可能稍有延迟。子账号开通需主账号预先配置必要权限（包括 `AliyunBailianFullAccess` 权限、页面权限和创建服务关联角色的系统策略）。

## 使用流程

### 1. 选择被观测的应用

访问应用观测页面，点击"选择被观测的应用"并添加目标应用。如果列表中找不到已创建的应用，可能原因包括：

- 应用尚未发布
- 应用不属于当前[业务空间](../concepts/workspace.md)

### 2. 查看观测数据

添加应用后，所有在该应用中输入的 Prompt 及相应数据将被自动追踪，并同步至应用观测。可查看的信息包括：

- **Prompt 内容与输出**
- **延时与调用时间**
- **Token 用量**

支持通过 Request ID、Trace ID 或 Span ID 进行搜索，以及按时间范围筛选。关闭观测后数据停止同步，重新添加后仅同步新增数据。

### 3. 导出数据

在应用详情页的 Trace 列表中，可将当前筛选条件下的数据导出为 JSONL 或 EXCEL 格式。

### 4. 监控统计

监控统计页签提供以下性能指标：

| 指标 | 说明 |
|------|------|
| 调用次数 | 应用调用次数趋势 |
| 失败次数与失败率 | 调用失败统计 |
| Token 总量 | 全部、输入和输出 Token 总量趋势 |
| 平均单次请求 Token 量 | 每次请求的平均输入和输出 Token 量 |
| 平均首 Token 耗时 | 流式调用场景下的首 Token 响应时间 |
| 平均调用时长 | 应用调用的平均延时 |

支持按时间范围（最长 30 天）和聚合粒度（按分钟/小时/天）查看数据。

## Span 筛选与过滤

应用观测提供三种 Span 筛选模式：

- **Root Span**：仅显示根节点（默认模式）
- **All Span**：显示所有 Span，平铺展示
- **Model Span**：仅显示包含模型调用的 Span

还可通过过滤器添加筛选条件，支持按状态、Span Name、输入/输出关键词、延时、Token 总量、输入/输出 Token、标签等维度过滤。具体用法参见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 文档。

## 节点类型

应用观测中的"节点"是被追踪的操作单元，节点之间可形成嵌套关系。主要节点类型包括：

**通用节点**：

| 节点 | 说明 |
|------|------|
| CHAIN | 将大模型节点与其他节点相连接，实现复杂任务处理。根节点时名称为 AgentApp 或 WorkflowApp |
| LLM | 调用大模型进行推理或文本生成，Token 量 = 输入 + 输出 |
| RETRIEVER | 执行检索操作，包括 TextRetriever（BM25 文本检索）和 VectorRetriever（向量检索） |
| EMBEDDING | 将输入 Prompt 转化为数值化向量 |
| RERANKER | 按相似度分数对文本切片降序排列 |
| REWRITER | 基于上下文调整 Prompt 以提升检索效果 |
| GUARDRAIL | 调用阿里绿网进行内容安全检测 |
| TOOL | 调用插件（官方或自定义） |

**工作流专有节点**：START、END、API、CLASSIFIER、TEXT_CONVERTER、SCRIPT、CONDITION、FUNCTION_COMPUTE、APP_FLOW 等。

**高代码应用**：目前仅支持追踪到 FullCodeApp 级别，不支持其内部调用链路追踪。高代码应用需在代码中使用 AgentScope-AI 的 Tracing 模块定义上报信息，并在部署时添加 `--telemetry enable` 参数。

## 数据标注与评测集

应用观测支持两项数据管理功能：

- **数据标注**：对 Span 数据添加自定义标签（布尔值、分类、数字、文本），与应用评测的标签管理功能共享
- **添加到评测集**：将线上调用的 Span 数据批量导入评测集，支持追加或全量覆盖，可自定义字段映射（最多 50 个字段）

详细操作步骤参见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 原始文档。

## 计费说明

应用观测功能本身不收费。但观测数据存储在可观测链路 OpenTelemetry 服务中，需支付该服务的存储费用。

> **注意**：应用观测目前暂无 API 接口，仅支持控制台操作。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)




