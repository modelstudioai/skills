# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心能力模块，提供**可观测性（Observability）** 与**可评测性（Evaluation）** 两大支柱功能。它基于 OpenTelemetry GenAI 标准实现框架中立接入，支持对智能体（Agent 1.0/2.0）和工作流应用的端到端链路追踪、多维监控告警，以及基于评测集、评估器和评测任务的自动化质量评估。开发者可将线上观测数据直接沉淀为评测样本，实现“观测 → 评测 → 优化”的闭环。

## 支持的模型/功能

- **观测能力**：支持智能体应用（Agent 1.0 和 Agent 2.0）及工作流应用的全链路可视化，覆盖 Prompt 解析、大模型调用（含 TTFT、总延时、[Token](../concepts/token.md) 消耗）、工具执行（MCP）、向量检索、记忆读写等环节；**不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持三类评估器：
  - **预置评估器**：按「通用质量」「智能体」「文本匹配」「文本相似度」「格式校验」分类，开箱即用；
  - **LLM 评估器**：使用大模型进行语义评分，支持自定义 Prompt、评分范围（如 0–100）与通过阈值；
  - **Code 评估器**：通过 Python 3.10 脚本实现确定性规则判断（如 JSON Schema 校验、数值计算），无额外 [Token](../concepts/token.md) 成本 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **标签体系**：支持分类、布尔值、数字、文本四类标签，用于人工标注评测数据或线上 Span，支撑多维分析与筛选 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)。

> **注意**：文档 12 (`raw/application-user-guide/agenteval/agenteval-observability.md`) 仅为目录索引页，其内容已被文档 3（`agenteval-observability/agenteval-observation.md`）和文档 4（`agenteval-observability/agenteval-alert-management.md`）完整覆盖，实际使用应以这两篇为准。

## 关键参数

| 参数类别 | 关键参数 | 说明 |
|----------|----------|------|
| **评估器配置** | `评分范围` | 决定打分尺度（如 `0–1` 用于二元判断，`0–100` 用于精细区分）；必须与 Prompt 中的评分指令严格一致 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。 |
| | `通过阈值` | 评分 ≥ 阈值为 Pass，否则为 Fail；建议设为评分范围中位数（如 `0–100` 时设 `50`）。 |
| | `字段映射` | 将评估器变量（如 `query`, `response`, `reference`）精确映射至评测集字段或应用输出；**所有变量必须完成映射，否则无法创建评测任务**。 |
| **告警规则** | `持续时间` / `告警检查周期` | 告警触发需指标连续异常达指定分钟数；检查周期默认 60 秒，最小为 0 秒（即实时检查） [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)。 |
| | `统计周期`（模板级） | 告警模板中指标统计窗口，合法范围 1–10080 分钟（即 1 分钟至 7 天）。 |

## 使用方式

1. **开启观测**：在[应用观测](https://bailian.console.aliyun.com/loop/app-observe)页面授权 OpenTelemetry 角色、开通服务并初始化 LogStore 后，对目标应用点击「开启观测」；数据同步延迟为分钟级 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
2. **构建评测集**：在[评测集](https://bailian.console.aliyun.com/loop/app-evaluate/eval-set)页面创建，**必须发布后才能用于评测任务**；支持从观测 Span 批量导入，实现真实流量→评测样本的转化。
3. **创建评估器**：在[评估器](https://bailian.console.aliyun.com/loop/app-evaluate/grader)页面选择预置模板或自定义 LLM/Code 评估器；LLM 评估器需试运行验证，Code 评估器需确保函数签名与入参一致且返回数值。
4. **发起评测任务**：在[评测任务](https://bailian.console.aliyun.com/loop/app-evaluate/eval-task)页面关联已发布的评测集、应用及评估器（最多 10 个），完成字段映射后提交；任务创建后配置不可修改，但可随时添加人工标签。

## 限制和注意事项

- **观测限制**：应用观测暂无公开 API；仅支持分钟级数据同步，不支持亚秒级实时追踪；关闭观测后历史数据停止同步，重启仅同步新增数据。
- **评测集限制**：单个评测集最多支持 50 个字段映射；文件上传仅支持 `.xls`/`.xlsx`（≤20 MB）；草稿状态评测集不可用于评测任务。
- **评估器限制**：基于评测任务创建的评估器**不支持试运行**，需在真实评测中验证效果；LLM 评估器调用产生 [Token](../concepts/token.md) 费用，Code 评估器无额外费用。
- **权限要求**：首次开通应用观测需使用**主账号**操作权限配置，子账号需主账号预先授予必要权限。
- **兼容性注意**：告警模板中的预置指标（如「QPM 限流大于 6000」）依赖后台分钟级聚合数据，阈值设置需匹配业务实际负载水位。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)


