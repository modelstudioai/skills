# decision model

decision model 是百炼平台提供的专用结构化决策模型（`decision-model-preview`），专为工单分流、内容审核、智能体路由、结果校验等高频、低延迟、强确定性的结构化判断场景设计。它不生成自由文本，而是对输入 `state` 一次性完成多个 typed 问题（`choice`/`noul`/`score`）的联合推理，返回分类结果、是非概率、有序评分及其置信度与完整概率分布。该能力基于 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 实现，协议兼容 TypeSafe System One。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），无其他变体或微调版本。
- 支持三类结构化问题：
  - `choice`：多选一判定（如“派单团队”），返回选中选项名、各选项概率及整体置信度；
  - `noul`（yes/no/unlikely）：是非二元判断（如“是否需升级”），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如“严重度 1–4 级”），返回概率加权期望分数（可为浮点数，如 `2.43`）、各级概率及置信度。
- 所有类型均返回完整 `probabilities` 分布，便于下游做阈值控制或不确定性分析。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | Body | `String` | ✓ | 固定为 `"decision-model-preview"` |
| `state` | Body | `String` / `Object` / `Array` | ✓ | 待决策的原始业务数据（如工单文本、对话 JSON、结构化对象）；对象将被序列化后送入模型 |
| `questions` | Body | `Object` | ✓ | 键为自定义 question ID，值为问题对象；每个问题必须含 `type` 字段（`choice`/`noul`/`score`）及对应 `criteria`（详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)） |
| `Authorization` | Header | `String` | ✓ | `Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量 `DASHSCOPE_API_KEY` |
| `Content-Type` | Header | `String` | ✓ | `application/json` |

> **注意**：`questions` 中 `choice` 的 `criteria` 必须为 **选项名 → 描述** 的映射（非数组），而 `score` 的 `criteria` 必须为 **从低到高排列的描述数组**；二者格式不可互换，否则模型将拒绝请求。该约束在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的“请求参数”章节明确定义。

## 使用方式

- **推荐 SDK 调用**（自动处理 endpoint 拼接与 region/workspace 映射）：
  - Python：DashScope SDK ≥ `2.0.1`，使用 `client.decision.create()`（旧版本无此接口）；
  - Java：DashScope SDK ≥ `2.23.3`，使用 `com.alibaba.dashscope.decision` 包；
  - 通用 TypeSafe SDK：设置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `client.system_one()`。
- **直接 HTTP 调用**：POST 到 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`，地域与域名需严格匹配 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中列出的 Endpoint 表。
- **调试建议**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线体验，验证问题定义与结果分布是否符合预期。

## 限制和注意事项

- **数量限制**：
  - 单次请求最多 16 个问题（`questions` 对象 key 数）；
  - `choice` 选项数 ≤ 255（建议补 `other` 兜底）；
  - `score` 等级数 2–255（强烈建议 3–7 级，确保语义可区分）；
  - 输入上下文上限 65536 token，超长 `state` 将被拒绝。
- **性能影响**：服务端延迟随问题数近线性增长，建议按业务必要性精简问题集合。
- **错误处理**：SDK 调用失败时，Python 抛 `DashScopeError`，Java 抛 `ApiException`；HTTP 层错误码详见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。
- **模型输出特性**：`score` 类型返回的 `score` 字段为浮点期望值（如 `2.25`），非整数索引；`choice` 和 `score` 类型才返回 `confidence`，`noul` 不提供置信度——这是由模型架构决定的固有行为，非文档遗漏。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


