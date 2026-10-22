# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，不生成文本，仅输出分类、是非判断、有序评分及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、任务完成度校验等低延迟、高并发的确定性决策场景。其核心能力基于 TypeSafe System One 协议实现，一次前向计算即可并行响应多个异构问题 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），暂无其他变体或版本别名。
- 支持三类结构化问题：
  - `choice`：多选一判定（如「派单团队」），返回选中选项、各选项概率及整体置信度；
  - `noul`（no/yes/unknown/likely）：是非二元判断（如「是否索要退款？」），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如「严重度 1–4 级」），返回加权期望得分（可为浮点数）、各级概率及置信度。
- 所有类型均**不生成任何自由文本**，输出严格受限于 `questions` 中定义的 schema，确保结果可解析、可审计 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✓ | 固定为 `"decision-model-preview"` |
| `state` | string / object / array | ✓ | 待决策的原始业务上下文；若为对象，将被 JSON 序列化后送入模型 |
| `questions` | object | ✓ | 键为问题 ID（调用方自定义），值为问题对象；最多支持 **16 个问题** |
| `questions.*.type` | string | ✓ | 取值 `"choice"` / `"noul"` / `"score"` |
| `questions.*.instructions` | string | ✗ | 问题语义提示，影响判断逻辑，建议明确简洁 |
| `questions.*.criteria` | object / array | ✓（`choice`/`score`）<br>✗（`noul`） | `choice`：选项名 → 描述映射（≤255 项，建议含 `"other"` 兜底）；`score`：等级描述数组（2–255 级，**强烈建议 3–7 级**，每级语义需可区分） |

> **注意**：文档中 `noul` 类型虽在 `criteria` 字段注明“可选 `{"true":…, "false":…}`”，但实际调用中该字段对 `noul` 无效，模型仅依据 `instructions` 和 `state` 推理 P(yes)；此为文档冗余描述，以 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中请求示例和返回结构为准。

## 使用方式

- **协议与端点**：HTTP POST 到 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`（如华北2：`cn-beijing`）。
- **认证**：Header `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。
- **推荐 SDK**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理 endpoint 拼接、请求序列化与响应解析：
  ```python
  from typesafe_sdk import TypeSafeClient
  client = TypeSafeClient(
      api_key=os.environ["DASHSCOPE_API_KEY"],
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode"
  )
  result = client.system_one(model="decision-model-preview", state=..., questions={...})
  ```
- **在线调试**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 选择预设场景（如「客服对话判断」「Agent 完成度核验」）快速验证逻辑与输出格式。

## 限制和注意事项

- **上下文长度**：`state` 序列化后总 token 数 ≤ 65536；超长将直接拒绝，不截断。
- **问题规模**：
  - 单次请求最多 16 个 `questions`，延迟随问题数近似线性增长；
  - `choice` 选项数 ≤ 255，`score` 等级数 2–255（但 3–7 级为最佳实践，过多等级易导致概率分散、置信度下降）。
- **输出确定性**：模型不生成文本，所有输出字段（`choice`/`noul`/`score`/`probabilities`/`confidence`）均严格按 schema 返回，无额外字段或自由文本。
- **地域与 WorkspaceId**：Endpoint 中 `{WorkspaceId}` 为必填业务空间 ID，不可省略；地域域名需与控制台开通区域一致，否则返回 403。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


