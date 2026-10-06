# agenteval

`agenteval` 是 Evolution 平台中面向 AI Agent 全生命周期质量保障的核心模块，提供可观测性、自动化评测与 Prompt 智能优化三位一体的能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路接入，支持从线上 Trace 沉淀评测数据、多维自动评分、人工反馈驱动的 Prompt 迭代，形成“观测 → 评测 → 优化”闭环。

## 支持的模型/功能

- **观测能力**：支持智能体应用（Agent 1.0 / 2.0）和工作流应用的全链路追踪，覆盖 Prompt 解析、大模型调用（含 TTFT、耗时、[Token](../concepts/token.md)）、工具执行（MCP）、向量检索、记忆读写等节点；但**暂不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置评估器（通用质量、智能体、文本匹配、格式校验等）与自定义评估器（LLM 或 Code 类型），支持多维度自动评分（如相关性、正确性、合规性、工具调用准确性）；同时支持人工标签体系，涵盖分类、布尔值、数字、文本四类标签，用于主观或复合维度补充 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持两种 Prompt 优化路径：① 多版本对比调试（基准组 vs 对照组），② 基于调试对话 + 人工反馈的智能生成；优化结果需手动采纳至编辑区，并经验证后发布，**采纳操作不会自动发布应用** [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

> **注意**：文档 4 明确指出“应用观测目前暂无 API”，但文档 1 中“全流程可观测”描述未作此限定；实际开发中应以文档 4 为准，当前观测能力仅限控制台交互，不可编程调用。

## 关键参数

- **评估器配置**：
  - `评分范围`（必填）：决定打分粒度（如 `0-100` 用于精细区分，`1-5` 用于快速分类），影响系统提示词生成与阈值判断。
  - `通过阈值`（必填）：评分 ≥ 阈值为 Pass，否则为 Fail；建议设为评分范围中位数。
  - `参数映射`（强约束）：所有评估器变量（如 `query`, `response`, `reference`）必须完成字段映射，否则无法保存评测任务 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **评测集字段**：预置评估器对字段有明确要求（如「问答相关性」需 `query` 和 `response` 字段），构建评测集前须按评估器文档规划表结构 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **告警规则**：`持续时间`（分钟）、`告警检查周期`（秒，默认 60）、`统计周期`（分钟，1–10080）为关键阈值触发参数，直接影响告警灵敏度与噪声水平 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)。

## 使用方式

1. **观测接入**：主账号完成三步开通（授权 OTel 角色 → 开通 OTel 服务 → 初始化 LogStore），再在控制台开启目标应用观测；开启后数据分钟级同步，支持按 `Request ID`/`Trace ID` 搜索、导出 JSONL/EXCEL [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
2. **评测构建**：
   - 创建评测集（类型选「智能体」或「工作流」，并关联具体应用及版本），发布后方可使用；
   - 创建评测任务时，选择已发布评测集、目标应用，并添加 ≤10 个评估器（推荐 3–5 个组合，如 LLM 相关性 + Code 格式校验）；
   - “不关联应用”模式仅用于纯人工标注场景，不触发自动调用 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
3. **Prompt 优化**：
   - 进入「应用优化」页面，选择待优化应用；
   - 可选路径一（对比）：设置基准组与对照组 Prompt，输入问题批量调试，采纳最优组配置；
   - 可选路径二（反馈）：选取代表性调试结果，填写具体人工反馈（如“遗漏家电类目例外；请完整列出一般规则、适用条件和特殊品类例外”），生成并采纳优化 Prompt；
   - **必须重新调试验证原问题、正常流程与边界场景，确认无退化后才可发布** [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

## 限制和注意事项

- **权限与开通**：应用观测首次使用需主账号操作开通 OTel 服务，子账号需被授予对应权限；高峰期开通可能延迟 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **数据时效与范围**：观测数据最长保留 30 天，监控指标聚合粒度支持分钟/小时/天；评测任务创建后**不可修改应用、评测集或评估器配置**，仅支持追加人工标签 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **评估器限制**：基于评测任务创建的评估器**不支持试运行**，需在真实评测任务中验证效果；Code 评估器要求 Python 3.10，函数签名必须严格匹配入参，且返回数值类型结果 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **成本提示**：评测任务调用 LLM 评估器产生的 [Token](../concepts/token.md) 按标准计费，可在评测任务列表页查看消耗量；Code 评估器无额外费用 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)


