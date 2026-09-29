# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级模型，一次前向推理即可同步输出分类、是非判断、有序评分及其概率分布与置信度，**不生成自由文本**。适用于工单分流、内容审核、智能体路由、规则校验等低延迟、高并发的确定性决策场景。其接口协议为 TypeSafe System One，通过 `POST /compatible-mode/v1/systemone` 调用，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），暂无其他别名或历史版本。
- 支持三类结构化问题：
  - `choice`：多选一决策（如“派单团队”），返回选中项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非二元判断，返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如严重度 1–4 级），返回加权期望分（可为浮点数）、各级概率及置信度。
- 所有问题可批量提交（单次请求支持多个 `questions`），模型统一前向计算并原子化返回全部结果，避免多次调用开销。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | ✅ | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | ✅ | 待决策的原始上下文，将被序列化后送入模型；超长（>65536 token）会被截断或拒绝 |
| `questions` | `Object` | ✅ | 键为自定义 question ID，值为问题对象；每个问题必须含 `type` 字段 |
| `questions.*.type` | `String` | ✅ | 取值为 `"choice"` / `"noul"` / `"score"` |
| `questions.*.criteria` | `Object` / `Array` | ⚠️ 条件必填 | `choice`: 选项名→描述映射（建议含 `"other"` 兜底）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 从低到高的等级描述数组（2–255 项，推荐 3–7 级） |

> **注意**：文档中 `score` 等级数量限制在“2–255”与“2–10”两处表述不一致（见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) “接口限制与建议”节），实际服务端校验上限为 **255**，但业务推荐使用 3–7 级以保障判别清晰性。

## 使用方式

1. **认证**：设置环境变量 `DASHSCOPE_API_KEY`，Header 中传 `Authorization: Bearer $DASHSCOPE_API_KEY`；
2. **Endpoint**：按地域选择对应域名，例如华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`；
3. **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理路径拼接与响应解析，示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)；
4. **关键实践**：
   - `state` 建议结构化（如 JSON 对象），比纯文本更易对齐语义；
   - `choice` 的 `criteria` 应覆盖常见选项，避免模型被迫归入 `other` 降低准确率；
   - 单次请求问题数建议 ≤16，延迟随问题数近线性增长。

## 限制和注意事项

- **上下文长度**：硬上限 65536 token，超长 `state` 将被截断或直接报错（HTTP 400）；
- **问题规模**：
  - 单个 `choice` 问题最多支持 255 个选项；
  - 单个 `score` 问题最多支持 255 级（但推荐 3–7 级）；
  - `questions` 总数无硬限制，但 ≥16 时延迟显著上升；
- **输出特性**：严格不生成任何文本（无 `text` / `output` 字段），仅返回结构化答案（`answers`）、`confidence`、`probabilities` 等；
- **错误排查**：失败时返回标准错误码，详细说明请查阅 [错误信息](../../raw/model-api-reference/preparations/error-code.md)；
- **地域一致性**：`base_url` 域名中的地域必须与 Workspace 所属地域一致，否则返回 403 或 404 —— 此约束在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中未显式强调，但实测验证必需。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


