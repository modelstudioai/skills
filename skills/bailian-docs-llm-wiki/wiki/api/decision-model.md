# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级模型，一次前向推理即可同步输出分类、是非判断、有序评分及其概率分布与置信度，**不生成文本**，适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高并发场景。其核心能力聚焦于确定性决策输出，与通用大模型的生成式范式有本质区别。详细协议与行为定义见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），暂无其他别名或历史版本。
- 支持三类结构化问题：
  - `choice`：多选一决策（如「派单团队」），返回选中项、各选项概率及整体置信度；
  - `noul`（yes/no/unlikely）：二元是非判断（如「是否需升级」），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如「严重度 1–4 级」），返回加权期望分（可为小数）、各级概率及置信度。
- 所有问题可**批量提交**（同一请求中多个 `questions`），模型一次前向完成全部判定，避免多次调用开销。

> **注意**：文档中未提及 `decision-model-v1` 或任何 GA 版本，所有生产使用必须指定 `model: "decision-model-preview"`；若其他内部文档声称存在 `decision-model`（无 `-preview` 后缀），以本 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 为准。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | ✅ | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | ✅ | 待决策的原始上下文，支持文本、JSON 对象或数组；对象将被序列化后送入模型 |
| `questions` | `Object` | ✅ | 键为自定义 question_id，值为问题定义对象 |
| `questions.*.type` | `String` | ✅ | 取值 `"choice"` / `"noul"` / `"score"` |
| `questions.*.instructions` | `String` | ⚠️推荐 | 清晰的问题描述或评判标准，显著影响判定质量 |
| `questions.*.criteria` | `Object / Array` | ⚠️按类型必填 | `choice`: `{key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 描述数组（2–255 级，**强烈建议 3–7 级**） |

- 上下文长度上限：65536 token，超长 `state` 将被截断或拒绝。
- 问题总数无硬性上限，但**建议 ≤ 16**，延迟随问题数近线性增长。

## 使用方式

1. **认证**：通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头传入 API Key（需提前配置环境变量）；
2. **Endpoint**：根据地域选择对应域名，例如华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`；
3. **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理路径拼接与响应解析，示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)；
4. **原生调用**：发送 `POST` 请求，`Content-Type: application/json`，Body 包含 `model`、`state`、`questions`。

## 限制和注意事项

- **无文本生成**：该模型严格输出结构化决策结果，不返回任何自由文本（如解释、理由），不可用于问答或摘要场景。
- **置信度覆盖范围**：仅 `choice` 和 `score` 类型返回 `confidence` 字段；`noul` 仅返回 `noul`（即 P(yes)）。
- **`score` 的 `legend` 字段索引为字符串**：返回体中 `legend` 的 key 为 `"0"`、`"1"` 等字符串，而非整数，解析时需注意类型（参见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 返回示例）。
- **错误处理**：失败响应遵循统一错误码规范，详见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


