# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，不生成文本，仅输出分类、是非判断、有序评分及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高并发的确定性决策场景。其核心能力基于 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 定义，调用方式统一为 `POST /compatible-mode/v1/systemone`。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），无其他别名或历史版本。
- 支持三类结构化问题：
  - `choice`：多选一判定（如“派单团队”），返回选中项、各选项概率及置信度；
  - `noul`：是非判断（yes/no），返回 `P(yes)` 概率值（浮点数，0.0–1.0）；
  - `score`：有序量表评分（如严重度 1–4 级），返回加权期望分（可为小数）、各级概率及置信度。
- 所有类型均**不生成任何自由文本**，输出严格结构化，延迟与成本与输出长度无关，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | Body | `String` | ✓ | 固定为 `"decision-model-preview"` |
| `state` | Body | `String` / `Object` / `Array` | ✓ | 待决策的原始上下文（如工单 JSON、对话文本），超长（>65536 token）将被截断或拒绝 |
| `questions` | Body | `Object` | ✓ | 键为自定义 question_id，值为问题对象；支持 ≤16 个问题（建议值，见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)） |
| `type`（question 内） | Body | `String` | ✓ | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria`（question 内） | Body | `Object` / `Array` | 条件必填 | `choice`: `{key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 描述数组（2–255 级，**强烈建议 3–7 级**） |

> **注意**：文档中 `score` 等级上限标注为“2–255”，但实际性能与可解释性在 3–7 级时最优；超出 7 级易导致概率分布扁平、置信度下降，该建议来自 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的实践指引，非硬性限制。

## 使用方式

- **协议与端点**：`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`  
  地域支持：华北2（北京）、新加坡（具体域名见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)）。
- **认证**：Header 中 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量。
- **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理路径拼接与响应解析：
  ```python
  from typesafe_sdk import TypeSafeClient
  client = TypeSafeClient(
      api_key=os.environ["DASHSCOPE_API_KEY"],
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode"
  )
  result = client.system_one(model="decision-model-preview", state=..., questions={...})
  ```

## 限制和注意事项

- **上下文长度**：最大 65536 token，超长 `state` 将被截断（非报错），影响决策准确性。
- **问题规模**：单次请求建议 ≤16 个问题；实测延迟随问题数近线性增长。
- **选项与等级约束**：
  - `choice` 最多 255 个选项；
  - `score` 等级数建议 3–7 级（文档明确提示“建议 3–7 级且每级可清晰区分”）；
- **无流式响应**：仅支持同步一次性返回，不支持 `stream=true`。
- **错误处理**：失败时返回标准错误码，详细说明见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)（该路径为 raw 文档引用，非本文档维护）。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


