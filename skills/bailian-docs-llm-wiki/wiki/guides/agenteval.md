# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心评测与优化模块，提供可观测性、自动化评测、智能 Prompt 优化三大能力。它支持开发者对智能体/工作流应用的输出质量进行量化评估，并基于真实调用数据、人工反馈与评测结果持续迭代优化，实现“观测 → 评测 → 优化”闭环。

## 支持的模型/功能

- **观测能力**：支持智能体（Agent 1.0 / 2.0）和工作流应用的全链路 Trace 可视化，覆盖 Prompt 解析、模型调用、工具执行、记忆读写等环节，自动捕获延时、[Token](../concepts/token.md) 消耗与异常；但**暂不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置与自定义两类评估器：
  - *预置评估器*：按「通用质量」「智能体」「文本匹配」「文本相似度」「格式校验」分类，开箱即用；
  - *自定义评估器*：支持 LLM 评估器（调用大模型语义评分）和 Code 评估器（Python 脚本规则判断），其中 LLM 评估器支持选择模型并配置评分范围（如 0–100）、通过阈值及系统 Prompt [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持多版本 Prompt 对比调试、基于调试对话与人工反馈的智能优化，以及基于优质评测集或线上 Trace 的 Prompt 迭代 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

> **注意**：文档 1 和文档 2 均将 `agenteval` 描述为 Evolution 的子模块，但文档 2 明确其定位为“一站式 Agent 全生命周期管理 & 智能分析平台”，而文档 1 称其为“Evolution 的各种功能”。实际以平台控制台结构为准——`agenteval` 是 Evolution 控制台内统一入口，非独立产品。

## 关键参数

- **评估器配置**：
  - `评分范围`：决定打分粒度（如 0–1 或 0–100），需与 Prompt 中的评分指令严格一致；
  - `通过阈值`：用于生成 Pass/Fail 判定，默认建议设为评分范围中位数；
  - `字段映射`：必须为评估器所有引用参数（如 `query`, `response`, `reference`）指定明确的数据源（评测集字段或模型输出），映射错误将导致评估失败 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **告警规则**：
  - `持续时间`：指标连续违反阈值的最短分钟数；
  - `告警检查周期`：默认 60 秒，单位为秒，必须为 ≥0 的整数；
  - `统计周期`：告警模板中指标计算的时间窗口（1–10080 分钟）。
- **评测任务**：每个任务最多支持添加 **10 个评估器**，且创建后**不可修改应用、评测集等核心配置**，仅可追加人工标签 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

## 使用方式

1. **观测接入**：  
   首次使用需主账号完成三项授权：开通 OpenTelemetry 服务、授权服务角色、初始化 LogStore；之后在[应用观测](https://bailian.console.aliyun.com/loop/app-observe)页面开启目标应用观测，数据同步延迟约 1 分钟。

2. **评测构建**：  
   - 创建**评测集**（需发布后方可使用）→ 选择或创建**评估器** → 在**评测任务**中关联二者并完成字段映射；
   - “不关联应用”模式适用于纯人工标注场景，此时不触发模型调用。

3. **Prompt 优化**：  
   - 进入应用优化页，可任选以下路径：
     - *多版本对比*：设置基准组与对照组 Prompt，输入问题并对比输出差异，点击“采纳当前组的配置项”更新编辑区；
     - *调试反馈优化*：在调试窗口输入问题 → 选择代表性调试结果 → 填写具体人工反馈（如“遗漏家电类目例外，需完整列出一般规则与特殊品类例外”）→ 点击“开始优化”生成新 Prompt → 采纳后仍需手动发布。

## 限制和注意事项

- **观测限制**：应用观测目前**无公开 API**，仅支持控制台操作；Trace 数据最长保留 30 天，导出格式为 JSONL 或 Excel [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测限制**：评测集文件仅支持 `.xls`/`.xlsx` 格式，最大 20 MB；LLM 评估器调用产生的 [Token](../concepts/token.md) 按标准计费，Code 评估器无额外费用。
- **优化限制**：采纳优化结果**仅更新当前 Prompt 编辑区，不会自动发布应用**；必须重新调试验证（覆盖原问题、正常流程、边界输入）并通过点击“发布”才能生效。
- **权限要求**：开通可观测链路需**主账号操作**；子账号需主账号预先配置 OpenTelemetry 相关权限。
- **数据一致性**：评测集中 `label_score` 字段映射的是评测任务中评估器的输出分数，而非原始评测集字段，此细节易被误用 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)


