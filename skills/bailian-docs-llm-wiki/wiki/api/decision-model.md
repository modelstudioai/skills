# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级前向推理模型，一次调用即可并行返回分类（`choice`）、是非判断（`noul`）和有序评分（`score`）三类结果及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体完成度校验、任务路由等低延迟、高吞吐的确定性决策场景。其接口协议兼容 TypeSafe System One，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），无其他变体或历史版本。
- 支持三种问题类型，可混合出现在同一请求中：
  - `choice`：多选一分类（如“派单团队”），返回选中选项名、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 `P(yes)` 概率值（浮点数，范围 `[0.0, 1.0]`）；
  - `score`：有序量表打分（如严重度 1–4 级），返回概率加权期望等级索引（可为小数，如 `2.25`）、各级概率、等级描述映射（`legend`）及置信度。
- 所有结果均基于单次前向传播生成，输出长度不影响延迟与计费，符合 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 定义的语义契约。

## 关键参数

| 参数 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | `String` | Body | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | Body | 是 | 待决策的原始业务输入（如工单文本、对话 JSON 或结构化对象），将被序列化后送入模型 |
| `questions` | `Object` | Body | 是 | 键为自定义问题 ID，值为问题对象；每个问题对象含 `type`（必填）、`instructions`（可选）、`criteria`（按 type 要求提供） |
| `Authorization` | `String` | Header | 是 | `Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量，参见 [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables) |
| `Content-Type` | `String` | Header | 是 | `application/json` |

> **注意**：`questions.criteria` 的结构严格依赖 `type`：`choice` 要求 `{"key": "desc"}` 映射（建议含 `other` 兜底项），`noul` 可选 `{"true": "...", "false": "..."}`，`score` 要求从低到高的字符串数组（建议 3–7 级）。该约束在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确定义，任何偏离均导致 400 错误。

## 使用方式

### SDK 调用（推荐）
- **Python**：使用 DashScope SDK ≥ 2.0.1，调用 `client.decision.create()`；旧版本无 `decision` 接口，会抛 `AttributeError`（详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)）。
- **Java**：使用 DashScope SDK ≥ 2.23.3，引入 `com.alibaba.dashscope.decision` 包；旧版本不支持。
- SDK 自动拼接 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），无需手动构造 URL。

### 通用 SDK 或 curl
- 可通过 `typesafe-sdk`（`system_one()` 方法）或原生 `curl` 直接调用 `/compatible-mode/v1/systemone`，需显式指定 `base_url` 或完整 endpoint。
- 各地域 endpoint 不同，华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/systemone`（参见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)）。

## 限制和注意事项

- **数量限制**：单次请求最多 16 个问题；`choice` 选项上限 255 项；`score` 等级数 2–255（强烈建议 3–7 级以保障判别清晰性）。
- **上下文长度**：`state` 序列化后总 token 数不得超过 65536，超长将被拒绝（非截断）。
- **延迟特性**：服务端耗时（`latency_ms`）随问题数近线性增长，但与输出长度无关——这是决策模型区别于文本生成模型的核心设计，已在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中强调。
- **错误处理**：Python SDK 抛 `DashScopeError`，Java SDK 抛 `ApiException`；通用错误码参考 `raw/model-api-reference/preparations/error-code.md`。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


