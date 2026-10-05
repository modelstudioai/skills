# agenteval

`agenteval` 是百炼平台提供的面向智能体（Agent）应用的端到端评测与可观测性工具，支持对 Agent 的任务完成率、响应质量、工具调用准确性等维度进行自动化评估。它可集成于开发流程中，用于迭代验证 Agent 行为一致性与鲁棒性。其能力基于平台统一的评测框架构建，与百炼模型服务深度协同。

## 支持的模型与功能

- 支持所有已接入百炼平台的 **大语言模型**（如 Qwen 系列、Qwen2-Agents）及 **自定义工具函数**（需符合 OpenAPI 3.0 规范）；
- 核心功能包括：**场景化评测任务编排**、**多轮对话轨迹回放与标注**、**自动指标计算（如 success_rate、tool_call_f1）**、**错误归因分析**（如 hallucination、tool misuse）；
- 工具链支持与 [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md) 模块强绑定，评测配置需通过 `eval_config.yaml` 声明，详见 [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md) 文档。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `task_id` | string | 是 | 评测任务唯一标识，需在平台控制台预先创建或通过 API 注册 |
| `model_id` | string | 是 | 百炼模型 ID（如 `qwen2-7b-instruct`），必须为已启用评测权限的模型 |
| `max_turns` | int | 否 | 默认 10，限制单次评测中 Agent 最大交互轮数，超限视为失败 |
| `enable_tracing` | bool | 否 | 默认 `false`，设为 `true` 后启用全链路追踪，数据将同步至 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md) |

> **注意**：`max_turns` 在 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md) 中被误标为“推荐设为 5”，实际行为以运行时配置为准，且平台默认值已在 v2.3.0 起更新为 10。

## 使用方式

1. 在控制台创建评测任务并获取 `task_id`；
2. 构建评测请求体（JSON），包含 `model_id`、输入 `query`、预期 `ground_truth` 及可选参数；
3. 调用 `/v1/agent/evaluate` 接口提交；示例：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/agent/evaluate \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"task_id":"t-abc123","model_id":"qwen2-7b-instruct","query":"查上海今天天气","ground_truth":{"weather":"晴"}}'
   ```
4. 结果可通过 `/v1/agent/evaluate/{eval_id}` 查询，原始日志与 trace 数据可在 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md) 查看。

## 限制和注意事项

- 单次评测请求最大 payload 为 2MB，超长上下文需预截断；
- 不支持跨模型对比评测（即一次请求仅允许指定一个 `model_id`）；
- 评测结果缓存有效期为 7 天，过期后需重新运行；
- 所有评测均受百炼平台配额限制，超出将返回 `429 Too Many Requests`；具体配额策略参见 [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agenteval.md)


