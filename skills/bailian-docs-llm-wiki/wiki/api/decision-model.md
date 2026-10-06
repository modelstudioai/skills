# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，不生成文本，仅输出分类、是非判断、有序评分及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高并发的确定性决策场景。其核心能力基于 TypeSafe System One 协议实现，一次前向计算即可并行响应多个异构问题 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型/功能

- 当前唯一可用模型：`decision-model-preview`（预览版），暂无其他变体或版本别名。
- 支持三类结构化问题：
  - `choice`：多选一判定（如「派单团队」），返回选中项、各选项概率及置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如严重度 1–4 级），返回加权期望分（可为浮点数）、各级概率及置信度。
- 所有问题可**批量提交**（`questions` 为对象字典），模型一次前向完成全部推理，不生成任何自由文本 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | 是 | 待决策的原始上下文，支持纯文本、JSON 对象或数组；对象将被序列化后送入模型 |
| `questions` | `Object` | 是 | 键为自定义 question_id，值为问题对象，含 `type`、`instructions`、`criteria`（按类型可选） |
| `type` | `String` | 是 | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria` | `Object`（choice）<br>`Object`（noul）<br>`Array`（score） | 视 `type` | `choice`：选项名→描述映射（建议含 `"other"` 兜底）；`noul`：可选 `{"true": "...", "false": "..."}`；`score`：从低到高的等级描述数组（建议 3–7 级） |

> **注意**：文档中 `score` 的等级数量限制在“2–255 级”，但实际建议范围明确为“3–7 级且每级可清晰区分”；若使用超 7 级，可能因语义模糊导致置信度下降，此矛盾已在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中体现，以建议值为准。

## 使用方式

- **协议与端点**：HTTP POST 到 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`，其中 `{WorkspaceId}` 和 `{region}` 需按[地域与域名](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)配置。
- **认证**：Header 中传 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量 `DASHSCOPE_API_KEY`。
- **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理路径拼接与响应解析：
  ```python
  from typesafe_sdk import TypeSafeClient
  client = TypeSafeClient(
      api_key=os.environ["DASHSCOPE_API_KEY"],
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode"
  )
  result = client.system_one(model="decision-model-preview", state=..., questions={...})
  ```
- 完整请求示例（含工单分流与是非判断）见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- **问题规模**：单次请求建议 ≤ 16 个问题；延迟随问题数近线性增长。
- **选项与等级**：
  - `choice` 最多支持 255 个选项；
  - `score` 等级数支持 2–255，但**强烈建议 3–7 级**，过多等级易降低判别精度。
- **上下文长度**：最大 65536 token，超长 `state` 将被拒绝或截断。
- **输出特性**：不生成文本，因此无 `output_tokens`、无流式响应、无 `finish_reason` 字段；所有答案均带 `probabilities`，`choice`/`score` 额外带 `confidence`。
- **错误处理**：失败时返回标准错误码，详情参见 `raw/model-api-reference/preparations/error-code.md`（该路径在原始文档中被引用，但未提供完整内容，开发者需自行查阅）。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


