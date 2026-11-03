# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在各类任务上的性能表现。它支持自动化指标计算、人工标注验证及多维度横向对比，帮助开发者快速定位模型优劣并指导迭代优化。该功能面向所有已部署或待选型的模型，覆盖从单次推理到批量任务的全场景评测需求。

## 支持的模型/功能

- 支持对百炼平台托管的全部 LLM（含通义千问系列、第三方接入模型）进行评测；  
- 提供三大评测维度：[大模型评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-llm.md)（基于预设 [prompt](prompt.md) 的自动打分）、[规则评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-rule.md)（正则/关键词/逻辑校验）、[人工评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-manual.md)（支持多人标注与一致性分析）；  
- 支持创建自定义评测任务和基线评测任务，便于 A/B 对比与版本回溯。

## 关键参数

- `dataset_id`：必填，指定评测数据集（需提前上传并结构化为 JSONL 格式，每行含 `input` 和 `reference` 字段）；  
- `model_id` 或 `endpoint`：指定被测模型，支持平台内模型 ID 或自定义 API endpoint；  
- `metrics`：可选列表，如 `["accuracy", "bleu", "rouge-l", "custom_rule"]`，具体取值需与所选评测维度匹配；  
- `evaluation_dimension`：必填，取值为 `"llm"`、`"rule"` 或 `"manual"`，决定底层执行逻辑；  
- `timeout`：单条样本最大处理时长（秒），默认 60，规则评估中不可超 10 秒。

## 使用方式

1. 通过控制台「模型评测」入口新建任务，或调用 `/v1/evaluations` REST API 提交评测请求；  
2. 选择数据集、目标模型、评测维度及指标组合；  
3. 启动后系统自动调度执行，结果可通过 [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md) 页面实时追踪；  
4. 人工标注类任务需额外配置标注员角色与质检规则，详见 [人工标注评测](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-manual-annotation.md)。

## 限制和注意事项

- 单次评测任务最多支持 10,000 条样本；超过需分批提交；  
- 规则评估不支持动态上下文依赖（如跨轮对话状态判断），仅适用于单轮静态输出校验；  
- > **注意**：文档中提及的 [排行榜](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-leaderboard.md) 功能当前仅对平台公开榜单开放，私有任务暂不支持自动入榜——该说明与控制台最新 UI 不一致，以实际接口返回字段 `leaderboard_enabled: false` 为准；  
- 所有评测任务默认保留 90 天，过期后原始日志与中间结果将被清理，建议及时导出关键指标。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


