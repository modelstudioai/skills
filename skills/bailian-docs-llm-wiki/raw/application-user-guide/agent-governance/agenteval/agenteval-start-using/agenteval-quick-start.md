# 快速开始

快速了解 Evolution 的各种功能

按当前任务选择观测、评测或优化，它们可以独立使用，不要求依次完成三个阶段。

## 选择要体验的能力

[

**观测执行过程**

配置观测与数据上报，查看 Trace、监控和限流指标。

](#h-agenteval-qs-observation)[

**评测输出与轨迹**

用已发布的评测集与评估器查看评分。

](#h-agenteval-qs-evaluation)[

**优化应用 Prompt**

基于调试、反馈或评测数据比较优化结果。

](#h-agenteval-qs-optimization)

## 前置准备

1.  访问[Evolution](https://bailian.console.aliyun.com/loop/quick-start)，点击右上角的**登录**。
2.  使用阿里云账号登录。
3.  如尚未注册阿里云账号，先注册并完成登录。

## 观测

Evolution 为开发者提供全链路执行过程的可视化观测能力，完整记录从输入到输出的每个处理环节，同时支持监控统计、限流统计、配置告警规则。

**最小准备**：选择当前业务空间内已发布的受支持应用。应用观测支持 Agent 1.0、Agent 2.0 和工作流应用，暂不支持通过 Assistant API 创建的智能体。首次使用先在**应用观测配置**中授权 OpenTelemetry 服务角色、开通服务并初始化 LogStore，详见[观测前提条件](https://help.aliyun.com/zh/model-studio/agenteval-observation#h-agenteval-obs-prereq)。使用主账号操作；子账号需主账号配置必要权限。

在应用列表中对目标应用点击**开启观测**，输入一条测试问题产生追踪数据，再进入详情页的 **Trace 列表**核对输入、输出与节点。数据同步以该应用已开启观测为前提。

1.  上报&查看 调用链轨迹与模型/工具事件。
2.  观察请求数、Tokens、模型、工具调用等监控指标。
3.  查看应用 QPM、限流次数等限流指标。
4.  基于告警模板配置告警规则，查看告警历史。

**说明**在 Trace 列表中找到本次问题，并查看对应节点、模型或工具事件，即可核对观测数据已上报。监控统计、限流统计与告警历史用于进一步排查运行情况。

更多详细说明，参考[应用观测](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)与[告警管理](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)。

## 评测

Evolution 为开发者提供系统化的评测能力，能够对应用的输出、Agent 执行轨迹与多模态内容进行评测。可以通过分析实验结果，深入研究异常案例，并进行有针对性的优化。

**最小准备**：准备输入样本与期望结果、对应评测集和评分维度。评测集必须[发布后再使用](https://help.aliyun.com/zh/model-studio/agenteval-evaluation-set#h-agenteval-set-publish)，草稿不能用于评测。任务中选择评测集的已发布版本与目标应用；为评估器的所有变量配置映射，变量与评测集字段或应用输出的数据类型须一致，详见[评估器映射](https://help.aliyun.com/zh/model-studio/agenteval-evaluation-task#h-agenteval-task-create-grader)。

1.  创建和管理评测集，整理输入样本与期望结果。
2.  创建或选择评估器，配置规则或模型评分维度。
3.  创建评测任务&查看评测结果，批量运行并生成评分，分析得分分布与回归对比。

**说明**任务完成后，在数据明细中核对样本、应用输出与评估器评分，再查看指标统计中的得分汇总。评分和分布用于定位异常样本；回归对比需选择可比较的评测结果。

更多详细说明，参考[评测任务](raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

## 优化

Evolution 为开发者提供系统化的评测与优化闭环，能够基于调试结果、评测集数据与线上 Trace 反馈，对应用 Prompt 进行智能优化与人工调试。支持多版本效果对比与一键采纳，持续提升应用输出质量。

**最小准备**：准备要优化的应用当前 Prompt，以及能暴露问题的测试问题。建议确认应用已创建并发布，见[使用前准备](https://help.aliyun.com/zh/model-studio/agenteval-optimization#h-agenteval-opt-prereq)。选择调试反馈路径时，先发送测试问题，选择对应调试结果，填写具体问题与期望改进方向，再点击**开始优化**。选择评测数据路径时，准备所选评测集版本或已完成的评测任务结果；线上 Trace 路径需要已有的观测反馈。

1.  多版本效果对比调试优化应用 Prompt。
2.  基于调试结果&反馈优化应用 Prompt。
3.  基于优质评测集 & 评测任务结果，优化应用 Prompt。

**说明**查看生成的 Prompt 与当前 Prompt 的对比，用同一测试问题复核回复差异，再决定是否采纳。采纳会更新当前编辑中的 Prompt，不会自动发布应用。

更多详细说明，参考[应用优化](raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。

## 下一步

[

**接入观测并排查告警**

按完整指南配置追踪与监控，结合告警历史排查问题。

](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)[

**创建评测任务**

配置评测集版本、评估器与字段映射。

](raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)[

**调试与优化 Prompt**

比较版本，选择反馈并审查优化结果。

](raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
