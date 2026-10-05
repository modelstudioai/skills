# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，不生成文本，仅输出分类、是非判断、有序评分及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高并发的确定性决策场景。其核心能力基于 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 定义，调用协议为 TypeSafe System One。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），无其他别名或历史版本。
- 支持三类结构化问题：
  - `choice`：多选一决策（如「派单团队」），返回选中项、各选项概率及置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（0.0–1.0），**不返回置信度**；
  - `score`：有序量表评分（如严重度 1–4 级），返回加权期望分（可为浮点数）、各级概率及置信度。
- 所有类型均返回完整 `probabilities` 分布，便于下游做阈值控制或集成贝叶斯后处理。

> **注意**：文档中未提及 `multi-choice` 或 `ranking` 类型，且 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 明确限定仅支持 `choice`/`noul`/`score` 三种 type，任何扩展类型均属未定义行为。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `"decision-model-preview"` |
| `state` | string / object / array | 是 | 待决策的原始上下文；对象会被 JSON 序列化后送入模型；超长（>65536 token）将被截断或拒绝 |
| `questions` | object | 是 | 键为问题 ID（字符串），值为问题对象；单次请求建议 ≤16 个问题（延迟近线性增长） |
| `questions.*.type` | string | 是 | 取值仅限 `"choice"`、`"noul"`、`"score"` |
| `questions.*.criteria` | object/array | 视 type | `choice`: key-value 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 从低到高的等级描述数组（建议 3–7 级） |

`instructions` 字段为可选，但强烈建议提供清晰评判标准，尤其在 `choice` 和 `score` 场景下直接影响判别一致性 —— 具体约束详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 使用方式

- **协议与端点**：`POST /compatible-mode/v1/systemone`，需替换 `{WorkspaceId}` 并选择对应地域（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`）。
- **认证**：Header 中传 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量（参见[配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）。
- **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理 base_url 拼接与响应解析。示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的 Python 工单分流与是非判断片段。
- **注意事项**：`state` 若为对象，序列化后参与 token 计费；`questions` 中每个问题独立建模，无跨问题依赖。

## 限制和注意事项

- **上下文长度**：硬上限 65536 token；超长 `state` 将被截断（非报错），建议前置摘要或字段筛选。
- **问题规模**：
  - 单次请求问题数无硬上限，但 ≥16 时延迟显著上升；
  - `choice` 选项数 ≤255，`score` 等级数 2–255（建议 3–7 级，避免语义模糊）。
- **输出特性**：
  - 不生成任何文本，因此输出长度不影响延迟或计费；
  - `noul` 类型**不返回 `confidence` 字段**（仅 `choice`/`score` 返回），此为设计约束而非遗漏；
  - `score` 的 `score` 字段为浮点期望值（如 `2.25`），非整数索引。
- **错误处理**：失败响应遵循统一错误码规范，详情参考 [错误信息](raw/model-api-reference/preparations/error-code.md) —— 注意该路径为相对路径，实际引用需按 Wiki 构建规则解析。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


