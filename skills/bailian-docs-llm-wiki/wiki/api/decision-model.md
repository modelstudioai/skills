# decision model

decision model 是百炼平台提供的专用结构化决策模型（`decision-model-preview`），通过一次前向推理同步返回分类、是非判断、有序评分及其概率分布与置信度，**不生成自由文本**。适用于工单分流、内容审核、智能体任务路由、结果校验等低延迟、高确定性要求的决策场景。其设计基于 TypeSafe System One 协议，与传统大模型文本生成范式有本质区别，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），无其他别名或历史版本。
- 支持三类结构化问题：
  - `choice`：多选一判定（如「派单团队」），返回选中项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非二元判断（如「是否需升级」），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如「严重度 1–4 级」），返回加权期望分（可为小数）、各级概率及置信度。
- 所有问题共享同一 `state` 输入，一次请求可并发处理多个问题（建议 ≤16 个），显著降低端到端延迟。该能力在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确定义。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✓ | 固定为 `"decision-model-preview"` |
| `state` | string / object / array | ✓ | 待决策的业务上下文；对象会被序列化为字符串送入模型 |
| `questions` | object | ✓ | 键为自定义 question_id，值为问题对象，含 `type`、`instructions`、`criteria` |
| `type` | string | ✓ | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria` | object (choice/noul) 或 array (score) | ✓（对 choice/score）<br>○（对 noul） | `choice`：选项名→描述映射（≤255 项，建议含 `"other"`）；`score`：等级描述数组（2–255 级，**强烈建议 3–7 级**，见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)） |

> **注意**：文档中 `score` 等级数量上限标注为“2–255”，但正文示例与最佳实践均强调“建议 3–7 级且每级可清晰区分”。实际部署中若使用 >10 级，可能导致概率分布弥散、置信度下降，应以示例中的工程建议为准。

## 使用方式

- **协议与端点**：`POST /compatible-mode/v1/systemone`，地域相关 Endpoint（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`）。
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
- **调试建议**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线验证逻辑，选择预设场景快速观察输出结构与概率行为。

## 限制和注意事项

- **上下文长度**：最大 65536 token，超长 `state` 将被拒绝或截断（非静默截断）。
- **问题规模**：单请求问题数无硬上限，但延迟随问题数近线性增长，**生产环境建议 ≤16**。
- **输出特性**：严格不生成文本，因此无 `output_tokens`、无 `text` 字段、无流式响应；所有答案均为结构化 JSON。
- **错误排查**：失败时返回标准错误码，详细说明见 [错误信息](../../raw/model-api-reference/preparations/error-code.md) —— 注意该文档路径为 `preparations/` 下，与本模型文档同属 `model-api-reference` 分类。
- **模型演进**：当前仅提供 `decision-model-preview`，暂无 GA 版本计划；后续变更将通过 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 同步更新。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


