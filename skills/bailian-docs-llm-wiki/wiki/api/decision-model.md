# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级前向推理模型，一次调用可并行完成多类判断（分类、是非、评分），返回概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高确定性要求的场景。其协议基于 TypeSafe System One，与百炼平台其他模型服务解耦，开发者可通过 DashScope SDK 或通用 TypeSafe SDK 快速集成。

## 支持的模型/功能

- **当前唯一支持模型**：`decision-model-preview`（预览版），无其他变体或历史版本。
- **三类原生问题类型**：
  - `choice`：多选一分类（如“派单团队”），返回选中项、各选项概率及置信度；
  - `noul`：是非判断（yes/no），返回 `P(yes)` 概率值（浮点数，范围 `[0.0, 1.0]`）；
  - `score`：有序量表打分（如严重度 1–4 级），返回概率加权期望等级索引（可为小数）及各等级概率。
- **批量决策能力**：单次请求最多支持 16 个问题，所有问题共享同一 `state` 输入，模型一次前向完成全部推理。
- **在线验证支持**：可通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 直接体验预设场景（客服对话判断、Agent 完成度核验等），详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | Body | `String` | ✓ | 固定为 `"decision-model-preview"` |
| `state` | Body | `String` / `Object` / `Array` | ✓ | 待决策的业务上下文（工单文本、对话记录或结构化对象），超长（>65536 tokens）将被拒绝 |
| `questions` | Body | `Object` | ✓ | 问题字典，key 为自定义 question_id；value 为问题对象，含 `type`、`instructions`、`criteria` 字段 |
| `type` | `questions[xxx]` | `String` | ✓ | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria` | `questions[xxx]` | `Object` / `Array` | ✓（`choice`/`score`）、可选（`noul`） | `choice`：选项名→描述映射（≤255 项，建议含 `"other"`）；`score`：等级描述数组（2–255 级，推荐 3–7 级）；`noul`：可传 `{"true": "...", "false": "..."}` 增强语义 |

> **注意**：`state` 若为对象，SDK 会自动序列化为字符串送入模型；`questions` 中 `instructions` 字段虽为可选，但强烈建议提供明确评判标准以提升一致性——该实践在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的多个示例中已验证有效。

## 使用方式

- **SDK 接入**（推荐）：
  - **Python**：需 `dashscope>=2.0.1`，使用 `client.decision.create()` 方法。旧版本无此接口，调用将抛 `AttributeError`，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。
  - **Java**：需 `dashscope-sdk-java>=2.23.3`，使用 `com.alibaba.dashscope.decision` 包，旧版本无 `DecisionQuestion` 类。
- **TypeSafe SDK**：通用兼容方案，安装 `typesafe-sdk`，调用 `client.system_one()`，需手动指定 `base_url`（指向 `compatible-mode` 子路径）。
- **curl**：直接 POST 到 `/compatible-mode/v1/systemone`，Header 含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。
- **地域与 Endpoint**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/systemone`，`{WorkspaceId}` 需替换为实际业务空间 ID。

## 限制和注意事项

- **QPS 与并发**：未在文档中明确定义硬性限流阈值，但实测高并发下延迟随问题数近线性增长，建议单请求问题数 ≤8 以保障 <100ms 延迟。
- **输入长度**：`state` 上下文上限为 65536 tokens，超长请求将被服务端直接拒绝（HTTP 400），**不触发截断或摘要**。
- **选项与等级约束**：
  - `choice` 选项数 ≤255，`score` 等级数 2–255（但 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 明确建议使用 3–7 级以保证语义可区分）；
  - `noul` 类型不支持自定义 `criteria` 描述（仅 `choice`/`score` 强制要求），若传入会被忽略。
- **错误处理**：Python SDK 抛 `DashScopeError`，Java SDK 抛 `ApiException`；通用错误码参考 [错误信息](../../raw/model-api-reference/preparations/error-code.md)，但决策模型特有错误未单独归类。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


