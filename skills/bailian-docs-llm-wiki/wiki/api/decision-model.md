# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级前向推理模型，不生成文本，仅输出分类、是非判断、有序评分及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高吞吐的确定性决策场景。其接口基于 TypeSafe System One 协议，一次请求可并行处理多个异构问题 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），无其他变体或版本别名。
- 支持三类结构化问题：
  - `choice`：多选一判定（如“派单团队”），返回选中选项、各选项概率分布及整体置信度；
  - `noul`（no/yes/unlikely）：二元是非判断（如“是否索要退款”），返回 P(yes) 概率值（0–1 浮点数）；
  - `score`：有序量表打分（如“严重度 1–4 级”），返回加权期望分（可非整数）、各级概率分布、等级描述映射（`legend`）及置信度。
- 所有类型均**不生成任何文本输出**，响应内容完全结构化，延迟与输出长度无关 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | 是 | 待决策的原始上下文；对象会被 JSON 序列化后送入模型 |
| `questions` | `Object` | 是 | 键为自定义 question ID，值为问题定义对象 |
| `questions.*.type` | `String` | 是 | 取值：`"choice"` / `"noul"` / `"score"` |
| `questions.*.instructions` | `String` | 否 | 问题语义提示，影响判定边界（建议必填） |
| `questions.*.criteria` | `Object / Array` | 视 type 而定 | `choice`: `{key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 从低到高的等级描述数组（2–255 级，**强烈建议 3–7 级**） |

> **注意**：文档中 `score` 等级数上限标注为 “2–255”，但实际建议范围明确为 “3–7 级且每级可清晰区分”；若使用 >10 级，可能导致概率分布弥散、置信度下降，该限制在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的“接口限制与建议”节已强调，应以建议值为准。

## 使用方式

- **协议与端点**：`POST /compatible-mode/v1/systemone`，需替换 `{WorkspaceId}` 并选择对应地域域名（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`）。
- **认证**：Header 中传 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量 `DASHSCOPE_API_KEY`。
- **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理 endpoint 拼接与响应解析：
  ```python
  from typesafe_sdk import TypeSafeClient
  client = TypeSafeClient(
      api_key=os.environ["DASHSCOPE_API_KEY"],
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode"
  )
  result = client.system_one(model="decision-model-preview", state=..., questions={...})
  ```
- **批量问题**：单次请求支持任意数量问题（建议 ≤16），所有问题并行计算，答案通过 `result.answers[question_id]` 访问。

## 限制和注意事项

- **上下文长度**：最大 65536 token，超长 `state` 将被截断或拒绝，无自动 truncation 策略。
- **问题规模**：
  - 单请求问题数无硬上限，但延迟随问题数近线性增长，**建议 ≤16**；
  - `choice` 选项数 ≤255；
  - `score` 等级数建议 3–7 级（详见上文注意项）。
- **返回结构**：
  - `choice` 和 `score` 类型返回 `confidence`（0–1），`noul` 不返回；
  - `score` 的 `score` 字段为浮点期望值（如 `2.25`），非整数索引；
  - `probabilities` 中 key 类型依问题而异：`choice` 为选项名字符串，`score` 为字符串数字索引（如 `"0"`、`"1"`）。
- **错误排查**：失败时返回标准错误码，详细说明见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


