# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级推理模型，一次前向计算即可同步返回分类、是非判断、有序评分三类结果及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体任务路由、结果校验等高频、低延迟、强确定性的业务场景。其接口协议兼容 TypeSafe System One，开发者可通过 DashScope SDK 或通用 TypeSafe SDK 快速集成。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`，属于预览版，能力稳定但可能随迭代演进。
- 支持三类结构化问题并行求解：
  - `choice`：多选一分类（如“派单团队”），返回选中选项名、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（浮点数，范围 [0,1]）；
  - `score`：有序量表评分（如“严重度”），返回概率加权期望等级索引（可为小数）、各级描述（`legend`）及置信度。
- 所有结果均基于同一前向推理生成，无 token 生成开销，延迟与输出长度无关。详细能力说明见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | 是 | 待决策的原始业务上下文（如工单文本、对话 JSON、结构化对象），将被序列化后送入模型 |
| `questions` | `Object` | 是 | 问题定义集合，key 为自定义 question ID；value 为问题对象，含 `type`（`choice`/`noul`/`score`）、`instructions`（可选）、`criteria`（按类型要求提供） |
| `type=choice` 的 `criteria` | `Object` | 是（当 type=choice） | `"option_key" → "option_desc"` 映射，最多 255 项，建议包含 `"other"` 兜底项 |
| `type=noul` 的 `criteria` | `Object` | 否 | 可选 `{ "true": "...", "false": "..." }` 描述，用于引导判断逻辑 |
| `type=score` 的 `criteria` | `Array<String>` | 是（当 type=score） | 从低到高的等级描述数组，长度 2–255，推荐 3–7 级且语义可区分 |

> **注意**：`questions` 中每个问题的 `criteria` 字段语义和格式严格依赖 `type`，SDK 封装（如 `DecisionQuestion.choice()`）已做类型校验，但原始 HTTP 请求需自行确保一致性。详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中“请求参数”章节。

## 使用方式

- **SDK 推荐**：
  - Python：使用 DashScope SDK ≥ 2.0.1，调用 `client.decision.create(...)`（旧版本无此接口）；
  - Java：使用 DashScope SDK ≥ 2.23.3，引入 `com.alibaba.dashscope.decision` 包；
  - 通用调用：使用 `typesafe-sdk`，调用 `client.system_one(...)`，需手动指定 `base_url` 为业务空间网关的 `compatible-mode` 路径。
- **Endpoint**：固定为 `POST /compatible-mode/v1/systemone`，域名按地域拼接（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`）。
- **认证**：Header 中 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量 `DASHSCOPE_API_KEY`。
- **在线调试**：强烈建议先通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 体验预设场景（客服判断、Agent 完成度核验等），验证逻辑后再编码集成 —— 此功能在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中有完整指引。

## 限制和注意事项

- **数量限制**：
  - 单次请求最多 16 个问题（`questions` 对象 key 数），延迟随问题数近线性增长；
  - `choice` 选项数 ≤ 255，`score` 等级数 2–255（推荐 3–7 级）；
  - 输入 `state` 上下文上限 65536 token，超长将被拒绝。
- **行为约束**：
  - 模型**不生成任何文本输出**，仅返回结构化答案与元信息（`probabilities`, `confidence`, `legend` 等）；
  - `score` 返回值为浮点型期望索引（如 `2.25`），非整数等级，需业务侧按需取整或保留小数；
  - `noul` 结果为 P(yes)，P(no) = 1 − P(yes)，无需额外解析。
- **SDK 兼容性**：DashScope Python SDK < 2.0.1 或 Java SDK < 2.23.3 **不支持**该模型，调用会抛出 `AttributeError`（Python）或 `ClassNotFoundException`（Java），请务必升级。相关版本说明见 [安装 SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


