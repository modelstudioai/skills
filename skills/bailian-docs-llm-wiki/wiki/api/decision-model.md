# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，一次前向计算即可同步返回分类（choice）、是非判断（noul）和有序评分（score）三类结果及其概率分布与置信度，**不生成自由文本**。适用于工单分流、内容审核、智能体路由、规则校验等低延迟、高并发的确定性决策场景。其接口协议基于 TypeSafe System One，与传统 LLM 文本生成范式有本质区别。

## 支持的模型与功能

- 当前唯一可用模型为 `decision-model-preview`，通过 `POST /compatible-mode/v1/systemone` 接口调用。
- 支持三类结构化问题并行求解：
  - `choice`：多选一决策（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（0.0–1.0），无置信度字段；
  - `score`：有序量表打分（如严重度 1–4 级），返回加权期望分（可为浮点数，如 `2.25`）、各级概率、等级描述映射（`legend`）及置信度。
- 所有结果均为确定性前向输出，**不依赖采样或解码**，延迟稳定且与输出长度无关。详细能力说明见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | ✅ | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | ✅ | 待决策的原始上下文（工单文本、对话历史或结构化对象），会被序列化后送入模型 |
| `questions` | `Object` | ✅ | 键为自定义问题 ID，值为问题对象；每个问题必须指定 `type`（`choice`/`noul`/`score`） |
| `questions.*.instructions` | `String` | ⚠️ 可选 | 问题语义提示，影响判定边界；建议明确、无歧义 |
| `questions.*.criteria` | `Object / Array` | ⚠️ 视类型而定 | `choice`：选项名→描述映射（建议含 `other` 兜底）；`noul`：可选 `{"true": "...", "false": "..."}`；`score`：从低到高的等级描述数组（建议 3–7 级） |

> **注意**：文档中 `score` 等级数范围在“请求参数”节写为“2–255”，但在“接口限制与建议”节明确建议“3–7 级且每级可清晰区分”。实际部署中应以 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的建议为准——**优先使用 3–7 级**，避免超过 10 级导致判别模糊和置信度下降。

## 使用方式

1. **认证**：配置环境变量 `DASHSCOPE_API_KEY`，Header 中传 `Authorization: Bearer $DASHSCOPE_API_KEY`；
2. **Endpoint**：按地域选择，例如华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`；
3. **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理路径拼接与响应解析，示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)；
4. **批量决策**：单次请求可携带多个问题（建议 ≤16 个），所有问题共享同一 `state`，服务端一次前向完成全部判定。

## 限制和注意事项

- **上下文长度**：最大 65536 token，超长 `state` 将被截断或拒绝，需前置精简；
- **问题规模**：
  - 单 `choice` 问题最多支持 255 个选项；
  - 单 `score` 问题最多支持 255 级（但强烈建议 3–7 级）；
  - `questions` 总数无硬上限，但延迟随问题数近线性增长，生产环境建议 ≤16；
- **无文本生成**：该模型**不输出任何自由文本**，仅返回结构化答案（`choice`/`noul`/`score` + `probabilities` + `confidence`/`legend`），不可用于摘要、改写等任务；
- **错误处理**：失败时返回标准错误码，具体含义参见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


