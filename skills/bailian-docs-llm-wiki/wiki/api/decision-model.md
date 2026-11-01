# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级推理模型，一次前向计算即可同步返回分类、是非判断、有序评分三类结果及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体完成度校验、任务路由等高频、低延迟、需可解释输出的场景。其协议兼容 TypeSafe System One，通过 `/compatible-mode/v1/systemone` 接口调用，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），无其他变体或版本别名。
- 支持三类结构化问题并行求解：
  - `choice`：多选一分类（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（浮点数，范围 [0,1]）；
  - `score`：有序量表评分（如严重度 1–4 级），返回概率加权期望等级索引（可为小数）及各级概率分布。
- 所有结果均附带 `probabilities` 字段（归一化概率分布）和 `latency_ms` / `usage.input_tokens` 等可观测指标，便于监控与成本分析。完整能力说明请参考 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 参数 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | `String` | Body | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | Body | 是 | 待决策的原始业务上下文（如工单文本、对话 JSON 或结构化对象），将被序列化后送入模型 |
| `questions` | `Object` | Body | 是 | 问题定义集合，key 为自定义 question_id；value 为含 `type`、`instructions`、`criteria` 的对象 |
| `type` | `String` | `questions[question_id]` 内 | 是 | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria` | `Object` / `Array` | `questions[question_id]` 内 | 视 `type` 而定 | `choice`: `{option_key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 等级描述数组（2–255 项，推荐 3–7 级） |

> **注意**：`questions` 中每个问题的 `criteria` 字段在 `noul` 类型下为**可选**，但若提供，必须是 `{"true": ..., "false": ...}` 形式；未提供时模型仍可执行判断，但判据由内部默认逻辑决定——该行为与部分旧文档中“`noul` 必须提供 `criteria`”的描述存在矛盾，以 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 为准。

## 使用方式

- **SDK 调用（推荐）**：
  - Python：使用 `dashscope>=2.0.1`，调用 `client.decision.create(...)`；
  - Java：使用 `dashscope-sdk-java>=2.23.3`，调用 `DecisionModel.call(...)`；
  - 均自动拼接 endpoint（基于 `workspace` + `region`），无需手动构造 URL。
- **通用 TypeSafe SDK**：使用 `typesafe-sdk`，设置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `client.system_one(...)`。
- **curl 直连**：直接 POST 到 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`，需手动设置 `Authorization` 和 `Content-Type` 头。
- 所有方式均要求配置环境变量 `DASHSCOPE_API_KEY`，详细配置方法见 [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。SDK 安装指引参见 [安装 SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

## 限制和注意事项

- **请求限制**：
  - 单次请求最多 16 个问题（`questions` 对象 key 数），延迟随问题数近线性增长；
  - `choice` 选项数 ≤ 255，`score` 等级数 2–255（强烈建议 3–7 级，确保语义可区分）；
  - 输入 `state` 上下文上限 65536 token，超长将被拒绝。
- **模型行为**：
  - **不生成任何文本输出**，仅返回结构化答案，因此响应延迟与输出长度无关；
  - `score` 类型返回的是概率加权等级索引（如 `2.25`），非整数等级，需按业务逻辑四舍五入或分段映射；
  - `confidence` 仅对 `choice` 和 `score` 类型返回，`noul` 类型无此字段。
- **错误处理**：
  - Python SDK 抛出 `DashScopeError`，Java SDK 抛出 `ApiException`；
  - 全量错误码及排查指南见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


