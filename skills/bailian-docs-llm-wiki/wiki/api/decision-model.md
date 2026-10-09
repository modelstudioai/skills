# decision model

决策模型（`decision-model-preview`）是百炼平台专为结构化决策场景设计的轻量级推理模型，一次前向计算即可同步返回分类、是非判断、有序评分三类结果及其概率分布与置信度，**不生成自由文本**。适用于工单分流、内容审核、智能体任务路由、完成度校验等低延迟、高确定性要求的业务场景。其接口协议为 TypeSafe System One，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），无其他变体或版本别名。
- 支持三类结构化问题类型：
  - `choice`：多选一判定（如“派单团队”），返回选中项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非二元判断（如“是否需升级”），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如“严重度 1–4 级”），返回加权期望分（可为小数）、各级概率及置信度。
- 所有类型均返回完整 `probabilities` 分布，便于下游做阈值控制或不确定性回退。该能力在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确定义。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | Body | `String` | ✓ | 固定为 `"decision-model-preview"` |
| `state` | Body | `String` / `Object` / `Array` | ✓ | 待决策的原始输入；结构化对象将被序列化后送入模型 |
| `questions` | Body | `Object` | ✓ | 键为自定义 question ID，值为含 `type`、`instructions`、`criteria` 的问题对象 |
| `type` | `questions.*` | `String` | ✓ | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria` | `questions.*` | `Object` / `Array` | ✓（`choice`/`score`），可选（`noul`） | `choice`：选项名→描述映射（建议含 `"other"`）；`score`：等级描述数组（2–255 项，推荐 3–7 级）；`noul`：可提供 `{"true": "...", "false": "..."}` 辅助理解 |
| `Authorization` | Header | `String` | ✓ | `Bearer $DASHSCOPE_API_KEY` |

> **注意**：文档中 `score` 等级数上限标注为“2–255”，但实际建议范围明确为“3–7 级且每级可清晰区分”；若使用超 10 级，可能因语义模糊导致置信度下降——此约束在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的“接口限制与建议”章节中强调，开发者应优先遵循建议值。

## 使用方式

- **Endpoint**：`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`  
  地域支持：`cn-beijing`（华北2）、`ap-southeast-1`（新加坡）等，详见[地域与域名](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
- **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理路径拼接与响应解析：
  ```python
  from typesafe_sdk import TypeSafeClient
  client = TypeSafeClient(
      api_key=os.environ["DASHSCOPE_API_KEY"],
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode"
  )
  result = client.system_one(model="decision-model-preview", state=..., questions={...})
  ```
- **调试建议**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线体验，选择预设场景快速验证逻辑与输出格式。

## 限制和注意事项

- **上下文长度**：最大 65536 token；超长 `state` 将被拒绝或截断，需业务侧预处理。
- **问题规模**：单次请求 `questions` 数量无硬上限，但**建议 ≤ 16**；实测延迟随问题数近线性增长。
- **选项与等级限制**：
  - `choice` 最多支持 255 个选项；
  - `score` 等级数 2–255，但强烈建议 3–7 级（见上文注意项）。
- **无文本生成**：模型严格输出结构化答案，不返回任何解释性文本或 reasoning trace，因此输出成本与长度无关。
- **错误排查**：失败响应含标准错误码，详细说明请参阅 [错误信息](raw/model-api-reference/preparations/error-code.md) —— 注意该路径为相对路径，实际引用时需补全为 `../../raw/model-api-reference/preparations/error-code.md`。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


