# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级推理模型，一次前向计算即可返回分类、是非判断与有序评分三类结果及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体任务路由、完成度校验等高频、低延迟、强确定性的业务场景。其接口协议遵循 TypeSafe System One 规范，与百炼平台其他模型保持一致的调用体验。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），对应 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 文档中定义的能力。
- 支持三类结构化问题：
  - `choice`：多选一分类（如“派单团队”），返回选中选项名、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（浮点数，范围 [0,1]）；
  - `score`：有序量表评分（如严重度 1–4 级），返回概率加权期望等级索引（可为小数）、各级概率及置信度。
- 所有类型均返回完整 `probabilities` 分布，便于下游做阈值控制或集成 Ensemble 决策逻辑。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | 是 | 待决策的原始输入（如工单文本、对话 JSON、结构化事件对象），会被序列化后送入模型 |
| `questions` | `Object` | 是 | 键为问题 ID（字符串），值为问题对象；每个问题对象含 `type`（`choice`/`noul`/`score`）、`instructions`（可选描述）、`criteria`（按类型要求提供选项映射或等级数组） |
| `questions.*.criteria` | `Object`（`choice`）、`Object`（`noul`）、`Array`（`score`） | 视 `type` 而定 | `choice`：选项名 → 描述映射（建议补 `other` 兜底）；`noul`：可选 `{"true": "...", "false": "..."}`；`score`：从低到高排列的等级描述数组（建议 3–7 级） |

> **注意**：`questions` 中每个问题的 `criteria` 字段在 `noul` 类型下文档未强制要求，但实践中若缺失可能导致语义模糊；建议始终提供 `{"true": "...", "false": "..."}`，以对齐 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中“可选”的说明与实际稳定性需求。

## 使用方式

- **推荐 SDK 方式**（自动处理 endpoint 拼接、认证与响应解析）：
  - Python：使用 DashScope SDK ≥ 2.0.1，调用 `client.decision.create(...)`；
  - Java：使用 DashScope SDK ≥ 2.23.3，调用 `DecisionModel.call(...)`；
  - 通用 SDK：`typesafe-sdk`（`TypeSafeClient.system_one(...)`），需手动指定 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`。
- **Endpoint**：`POST /compatible-mode/v1/systemone`，地域相关，例如华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`。
- **认证**：Header 中 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量 `DASHSCOPE_API_KEY`（详见 [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）。
- **在线调试**：强烈建议先通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 试运行，验证问题设计与结果合理性——该能力在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中有明确指引。

## 限制和注意事项

- **请求限制**：
  - 单次最多 16 个问题（延迟近线性增长）；
  - `choice` 选项数 ≤ 255，`score` 等级数 2–255（官方建议 3–7 级）；
  - 输入 `state` 上下文上限 65536 token，超长将被拒绝。
- **行为约束**：
  - 模型**不生成任何文本输出**，仅返回结构化答案与概率，因此延迟与成本与输出长度无关；
  - `choice` 和 `score` 类型返回 `confidence`，`noul` 类型不返回（因其本质即为概率）；
  - `score` 的 `score` 字段为浮点数（如 `2.25`），表示概率加权后的等级索引，非整数等级。
- **SDK 兼容性**：
  - Python SDK < 2.0.1 或 Java SDK < 2.23.3 **不支持** `decision` 接口，调用将报 `AttributeError` 或 `ClassNotFoundException`；
  - 旧版 SDK 用户必须升级，此要求已在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确标注。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


