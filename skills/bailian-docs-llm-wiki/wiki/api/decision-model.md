# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级推理模型，一次前向计算即可同步返回分类、是非判断、有序评分及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体完成度校验、任务路由等高频、低延迟、强确定性的业务场景。其接口协议遵循 TypeSafe System One 标准，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），无其他变体或历史版本。
- 支持三类结构化问题并行求解：
  - `choice`：多选一分类（如「派单团队」），返回选中选项名、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非二元判断（如「是否需升级」），返回 P(yes) 概率值（浮点数，0.0–1.0）；
  - `score`：有序量表打分（如「严重度」），返回概率加权等级索引（可为小数）、各级概率、等级描述映射（`legend`）及置信度。
- 所有类型均返回完整概率分布（`probabilities`），便于下游做阈值控制或集成贝叶斯融合。详细能力说明请参见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | 是 | 待决策的原始业务上下文（如工单文本、对话 JSON 或结构化对象），将被序列化后送入模型 |
| `questions` | `Object` | 是 | 键为自定义问题 ID，值为问题对象；每个问题对象含 `type`（`choice`/`noul`/`score`）、`instructions`（可选描述）、`criteria`（按类型要求提供选项映射或等级数组） |

**约束条件**：
- 单次请求最多支持 **16 个问题**；
- `choice` 选项数 ≤ 255（建议补 `other` 兜底）；
- `score` 等级数 2–255（**强烈建议 3–7 级**，确保语义可区分）；
- 输入 `state` 上下文上限 **65536 token**，超长将直接拒绝（不截断）；
- 更多参数细节与示例请参考 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 使用方式

### SDK 调用（推荐）
- **Python**：使用 DashScope SDK ≥ 2.0.1，调用 `client.decision.create()`；旧版本无该接口，会抛 `AttributeError`。
- **Java**：使用 DashScope SDK ≥ 2.23.3，引入 `com.alibaba.dashscope.decision` 包；旧版本不支持。
- SDK 自动拼接 `/compatible-mode/v1/systemone` 端点，并根据 `workspace` 和 `region` 构建完整 URL。

### 通用 TypeSafe SDK
- 安装 `typesafe-sdk`，设置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `client.system_one()`。
- 该方式需手动构造请求体，但兼容性更广。

### curl 直连
- 直接 POST 到对应地域 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），注意设置 `Authorization: Bearer $DASHSCOPE_API_KEY` 与 `Content-Type: application/json`。

> **注意**：所有 SDK 示例中 `{WorkspaceId}` 必须替换为真实业务空间 ID，且各地域 endpoint 域名不同，配置错误将导致 404 或连接失败。具体地域与域名规则见 [地域与域名](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)，该信息亦在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确列出。

## 限制和注意事项

- **无文本生成能力**：模型仅输出结构化答案（`choice`/`noul`/`score` 及其元数据），不产生任何自由文本，因此延迟与成本与输出长度无关。
- **置信度适用范围**：`confidence` 仅对 `choice` 和 `score` 类型有效；`noul` 类型不返回 `confidence`，其 `noul` 值本身即为概率估计。
- **输入格式鲁棒性**：`state` 为对象时会被 JSON 序列化后送入模型，建议避免嵌套过深或含不可序列化字段（如函数、循环引用）。
- **错误处理**：调用失败时，Python SDK 抛 `DashScopeError`，Java SDK 抛 `ApiException`；HTTP 层错误码详见 [错误信息](raw/model-api-reference/preparations/error-code.md)（注意该路径未回溯，属原始文档内部引用，无需调整）。
- **在线调试建议**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 体验预设场景（客服判断、Agent 核验等），实时观察结果、概率分布与 [Token](../concepts/token.md) 消耗，再调整 `instructions` 和 `criteria`。该 Playground 链接在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中已明确标注。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


