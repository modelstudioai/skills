# decision model

决策模型（`decision-model-preview`）是百炼平台专为结构化决策场景设计的轻量级推理模型，一次前向计算即可同步返回多类判定结果（分类、是非、评分）及其概率分布与置信度，**不生成自由文本**。适用于工单分流、内容审核、智能体任务路由、完成度校验等低延迟、高确定性要求的业务场景。其接口协议基于 TypeSafe System One，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），无其他变体或版本别名。
- 支持三类结构化问题：
  - `choice`：多选一判定（如「派单团队」），返回选中项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非判断（如「是否需升级」），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如「严重度」），返回加权期望分（可为浮点数，如 `2.43`）、等级描述映射（`legend`）及各等级概率。
- 所有问题并行处理，一次请求可携带多个问题（建议 ≤16 个），模型统一前向、统一返回，避免多次调用开销。该能力在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确定义。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `"decision-model-preview"` |
| `state` | string / object / array | 是 | 待决策的原始业务上下文；对象会被序列化为字符串送入模型 |
| `questions` | object | 是 | 键为问题 ID，值为问题定义对象，含 `type`、`instructions`、`criteria` 等字段 |
| `type` | string | 是 | 取值为 `"choice"` / `"noul"` / `"score"` |
| `criteria` | object 或 array | 视 type 而定 | `choice`: `{key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 从低到高的等级描述数组（建议 3–7 级） |

> **注意**：文档中 `score` 的等级数量限制存在表述差异——正文称“2–255 级”，但示例与最佳实践均强调“建议 3–7 级且每级可清晰区分”。实际部署应以 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的建议为准，避免使用超宽量表（如 20 级），否则概率分布易趋平、置信度下降。

## 使用方式

- **协议与端点**：HTTP POST 至 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`（如华北2：`cn-beijing`）。
- **认证**：Header 中传 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量。
- **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理路径拼接与响应解析，示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。
- **调试建议**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线验证问题定义与输出效果，支持预设场景快速试跑。

## 限制和注意事项

- **上下文长度**：最大 65536 token；超长 `state` 将被拒绝或截断，不触发静默降级。
- **性能影响**：延迟随问题数量近似线性增长，单次请求建议 ≤16 个问题；`choice` 选项数超过 50 时，概率分布收敛速度可能下降。
- **输出确定性**：模型不生成文本，因此无 `output_tokens` 字段，`usage` 仅含 `input_tokens`。
- **错误处理**：失败时返回标准错误码，详细说明参见 `raw/model-api-reference/preparations/error-code.md`（该路径未在当前原始文档中展开，需查阅对应原始文件）。
- **地域约束**：Endpoint 必须与 Workspace 所属地域严格匹配，跨地域调用将失败。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


