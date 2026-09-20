# agenteval

`agenteval` 是百炼平台提供的面向智能体（Agent）应用的端到端评测与可观测性工具，支持对 Agent 的行为逻辑、工具调用、响应质量及链路耗时等维度进行自动化评估。它不依赖人工标注，可基于预设场景和黄金标准输出进行多维打分，并与百炼监控体系深度集成。该能力主要服务于开发者在 Agent 开发迭代周期中快速验证效果、定位瓶颈。

## 支持的模型与功能

- **模型兼容性**：支持所有已在百炼平台部署并启用 `agent` 类型的模型服务（如 Qwen-Agent 系列），但不支持纯文本生成模型（如 `qwen-max` 未开启 agent 模式）直接接入评测流程。  
- **核心功能**：  
  - 场景化评测（Scenario-based Evaluation）：基于用户定义的输入-期望输出对执行自动比对；  
  - 工具调用合规性检查：验证 Agent 是否按预期调用指定工具、参数是否合法；  
  - 链路可观测性：完整追踪 LLM 调用、Tool 调用、Parser 解析、Fallback 触发等环节耗时与状态；  
  - 标签驱动分析：支持通过 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md) 对评测结果按业务维度（如“登录流程”“客服意图”）聚合分析。  

> **注意**：文档 [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md) 中提及“支持任意 HTTP 接口封装的外部 Agent”，但当前版本（v2.3.0+）仅支持百炼原生托管的 Agent 实例；该描述已过时，请以 [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md) 中的接入方式为准。

## 关键参数

评测任务配置需在 `eval_config.yaml` 中声明，关键字段包括：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `scenario_id` | string | 是 | 场景唯一标识，需提前在控制台创建，对应 [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md) 中定义的测试集 |
| `timeout_ms` | integer | 否 | 单次评测超时，默认 `120000`（2 分钟），不可低于 `5000` |
| `max_retries` | integer | 否 | 失败重试次数，默认 `1`，设为 `0` 表示不重试 |
| `enable_observability` | boolean | 否 | 是否采集全链路 trace，默认 `true` |

## 使用方式

1. 在控制台「Agent 应用」页选择目标实例，进入「评测」Tab；  
2. 点击「新建评测任务」，上传或引用已配置的 `scenario_id`（参见 [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)）；  
3. 提交后，系统异步执行并生成报告，支持按 `status`（success/partial_failure/failed）、`latency_p95`、`tool_call_accuracy` 等指标筛选；  
4. 结果数据可通过 OpenAPI `/v1/evaluations/{id}/results` 获取原始 JSON，用于 CI/CD 集成。

## 限制和注意事项

- 单次评测任务最多包含 1000 个测试样本，超量需拆分任务；  
- 工具调用日志仅保留最近 7 天，历史 trace 不可回溯；  
- 若 Agent 返回非 JSON 格式响应且未配置自定义 parser，评测将标记为 `parse_error` 并终止后续校验；  
- 所有评测流量计入项目配额，不享受免费额度（详见 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md) 的计费说明）。

## 来源文档

- [Evolution](../../raw/application-user-guide/agenteval.md)


