# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，不生成文本，仅输出分类、是非判断、有序评分及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高并发的确定性决策场景。其接口基于 TypeSafe System One 协议，一次前向即可并行响应多个问题，延迟与输出长度无关 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），暂无其他变体或版本。
- 支持三类结构化问题：
  - `choice`：多选一决策（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非判断，返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表评分（如严重度 1–4 级），返回加权期望分值（可为小数）、各级概率及置信度。
- 所有答案均附带 `probabilities` 字段（归一化概率分布），便于下游做阈值过滤或集成决策 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `model` | string | 是 | 固定为 `"decision-model-preview"` |
| `state` | string / object / array | 是 | 待决策的原始上下文，支持文本、JSON 对象或数组；对象将被序列化后送入模型 |
| `questions` | object | 是 | 键为自定义 question_id，值为问题定义对象，含 `type`、`instructions` 和 `criteria`（按类型要求） |
| `type` | string | 是（在 `questions.*` 中） | 取值 `"choice"`、`"noul"` 或 `"score"` |
| `criteria` | object / array | 视 `type` 而定 | `choice`: `{key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 从低到高的等级描述数组（建议 3–7 级，2–255 级有效） |

> **注意**：文档中 `score` 的等级数量限制在“接口限制与建议”中写为“2–255”，但在“问题对象属性”说明中又注明“2–10 级”，二者矛盾。实际服务端校验以 `2–255` 为准（实测 12 级可成功提交），建议遵循 3–7 级以保障判别清晰度 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 使用方式

- **协议与端点**：`POST /compatible-mode/v1/systemone`，需替换 `{WorkspaceId}` 并选择对应地域域名（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`）。
- **认证**：Header 中传 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量 `DASHSCOPE_API_KEY`。
- **推荐 SDK**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理 endpoint 拼接与响应解析，示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的 Python 片段。
- **典型调用模式**：单次请求可并行提交 ≤16 个问题（超量将显著增加延迟），例如同时完成工单的「部门归属」`choice`、「是否升级」`noul`、「严重度」`score` 三项判定。

## 限制和注意事项

- **上下文长度**：最大 65536 token，超长 `state` 将被截断或拒绝，建议预处理压缩关键信息。
- **问题规模**：
  - 单次请求建议 ≤16 个问题（延迟近线性增长）；
  - `choice` 选项数 ≤255；
  - `score` 等级数 2–255（但语义区分难度随等级数上升，强烈建议 3–7 级）。
- **无文本生成**：该模型**不输出任何自由文本**，仅返回结构化答案字段（`choice`/`noul`/`score`/`probabilities`/`confidence` 等），因此不适用需要解释、摘要或生成式反馈的场景。
- **错误排查**：失败时返回标准错误码，详细说明请参考 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


