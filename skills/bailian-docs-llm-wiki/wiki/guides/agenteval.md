# agenteval

`agenteval` 是百炼平台提供的面向智能体（Agent）应用的端到端评测与可观测性工具，支持对 Agent 的行为链路、决策逻辑、工具调用及最终结果进行结构化评估。它适用于开发阶段的迭代验证和上线后的持续监控，核心能力覆盖自动化评测、多维指标分析与根因定位。该工具深度集成于百炼 SDK 与控制台，需配合 `qwen-agent` 或兼容框架使用。

## 支持的模型/功能

- 支持基于 Qwen 系列大模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）构建的 Agent 应用评测；  
- 支持自定义评测任务：包括单步动作准确性、多跳推理完整性、工具调用合规性、响应安全性等维度；  
- 提供内置可观测性面板，可追踪 `thought → action → observation → answer` 全链路轨迹，并支持按 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md) 进行分组分析。  
> **注意**：文档中提及的 `qwen-vl` 模型支持仅限视觉-语言联合任务评测，但当前 SDK v2.3.0 版本尚未开放该能力，详见 [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md) 中的兼容性说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `eval_config` | dict | 是 | 指定评测维度（如 `"tool_call_validity": true`）、基准数据集路径及评分规则 |
| `trace_id` | str | 否 | 关联已有观测链路 ID，用于将评测结果注入对应 trace；若未提供则新建 trace |
| `timeout` | int | 否 | 单次评测最大等待时长（秒），默认 120，超时将中断并标记为 `TIMEOUT` 状态 |
| `enable_observability` | bool | 否 | 是否同步采集运行时 trace，默认 `True`；设为 `False` 可降低开销，但将无法使用 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md) 功能 |

## 使用方式

1. 安装最新版百炼 SDK（≥2.2.0）：`pip install alibabacloud-bailian20231227`；  
2. 初始化 `AgentEvalClient`，传入 `app_id` 和 `access_token`；  
3. 调用 `.evaluate()` 方法，传入待测 Agent 实例（需实现标准 `run()` 接口）及 `eval_config`；  
4. 结果返回 `EvaluationResult` 对象，含 `score`、`details`（逐项评分）、`trace_url`（控制台可观测链接）。  
完整示例见 [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)。

## 限制和注意事项

- 单次评测任务最多支持 50 条测试样本，批量评测需分批提交；  
- 所有评测请求均经过百炼服务端统一鉴权与限流（默认 10 QPS / app_id），超出将返回 `429 Too Many Requests`；  
- 评测过程中若 Agent 主动抛出未捕获异常（如 `ToolNotFoundError`），`agenteval` 将终止执行并记录 `ERROR` 状态，**不会自动 fallback 或重试**；  
- 当前不支持跨模型版本混合评测（例如同时对比 `qwen-max-20240601` 与 `qwen-max-20240801`），需分别配置独立评测任务——此限制在 [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md) v2.2.1 中已明确标注。

## 来源文档

- [Evolution](../../raw/application-user-guide/agenteval.md)


