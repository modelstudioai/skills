# application monitoring

应用观测提供端到端的调用链路追踪与性能分析能力，帮助开发者实时掌握 AI 应用内部处理流程（如向量化、知识检索、大模型推理）及核心运行时指标。数据以分钟级频率异步同步至控制台，支持可视化查看 Prompt 内容、节点延时、Token 消耗及全链路拓扑结构。

## 支持的功能与应用类型
- **接入范围**：全面支持 [[agent-application]]、[[workflow-application]] 与 [[high-code-application]]。
- **核心能力**：
  - **链路追踪**：自动记录 `CHAIN`、`LLM`、`RETRIEVER`、`TOOL`、`GUARDRAIL` 等标准节点的调用关系与嵌套结构。详细节点类型定义与数据字典可参考 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 附录说明。
  - **数据分析**：支持流式场景下的首 Token 耗时统计、Token 输入/输出拆分计量，以及原始请求/响应数据的留存与导出。
  - **数据流转**：支持将线上真实调用 Span 数据批量导入至 [[evaluation-dataset]]，用于构建贴近生产环境的评测基准。
- **暂不支持**：通过 [[assistant-api]] 创建的应用实例无法接入本观测模块。

## 关键参数
- **性能指标**：调用次数、失败次数/失败率、Token 总量与平均单次请求量、平均首 Token 耗时、平均调用时长。
- **视图模式**：`Root Span`（默认仅显示调用入口）、`All Span`（全量平铺）、`Model Span`（仅含大模型调用节点）。
- **筛选维度**：支持基于 Request ID、Trace ID、Span ID 精确检索；支持按状态（正常/错误）、延时（ms）、Token 阈值、输入/输出关键词及自定义标签组合过滤。
- **导出格式**：JSONL（结构化流式数据）或 EXCEL（表格化统计）。

## 使用方式
1. **服务初始化**：首次访问观测控制台需完成角色授权、[[opentelemetry]] 服务开通及 LogStore 初始化。界面交互与配置步骤详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。
2. **应用接入**：点击“添加”选择目标应用。应用必须处于已发布状态且归属当前业务空间。添加后系统自动开始采集，关闭后将停止同步，重新添加仅采集后续新数据。
3. **日常运维**：
   - 在 Span 列表页通过节点名称展开查看 `详情`、`原始数据` 及下游子节点。
   - 使用表头编辑器自定义展示字段，利用过滤器快速定位异常或高延迟调用。
   - 对典型 Span 进行数据标注（布尔/分类/数值/文本），标注结果实时保存并共享至全局标签管理体系。

## 限制与注意事项
- **计费说明**：应用观测控制台功能免费，但底层依赖的可观测链路存储服务按量计费，具体计费标准请参考云厂商账单。
- **高代码应用埋点**：[[high-code-application]] 默认仅暴露 `FullCodeApp` 根节点。若需观测内部链路，必须在业务代码中集成 `agentscope-runtime` Tracing 模块，并在容器部署参数中显式添加 `--telemetry enable`。
> **注意**：部分历史指引提及“长期记忆检索过程可被观测”，但当前版本暂不支持捕获该环节的底层调用；此外，`TextRetriever` 与 `VectorRetriever` 默认返回 100 个切片且控制台不支持动态调参，架构设计时需考虑上下文窗口限制。关于子账号权限配置冲突排查（如缺少 `ram:CreateServiceLinkedRole` 策略导致初始化卡死），完整解决方案可查阅 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)

