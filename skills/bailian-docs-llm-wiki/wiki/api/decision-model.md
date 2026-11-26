# decision model

百炼决策模型（`decision-model`）是一类专为结构化决策任务设计的推理模型，不生成自由文本，而是对输入 `state` 一次性返回多个预定义问题的判定结果（分类、是非、评分）及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高确定性要求的场景。其核心能力基于 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 定义。

## 支持的模型与功能

- **正式版**：`decision-model`，支持文本 + 单图/多图联合输入，上下文上限 268,288 [Token](../concepts/token.md)。
- **预览版**：`decision-model-preview`，仅支持纯文本输入，上下文上限 65,536 [Token](../concepts/token.md)，适合快速验证逻辑。
- **问题类型**：
  - `choice`：多选一（1–255 个选项），返回最可能选项及各选项概率；
  - `noul`：是非判断（yes/no），返回 `P(yes)` 概率值；
  - `score`：有序量表（2–255 级，推荐 3–7 级），返回加权等级索引及各级概率分布。
- 图像输入仅在 `decision-model` 正式版中可用，且需通过 HTTP 直接调用；当前 DashScope Python SDK 2.0.1 的 `client.decision.create` 方法**尚不支持 `images` 参数**，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | 是 | 取值为 `"decision-model"` 或 `"decision-model-preview"` |
| `state` | `String / Object / Array` | 是 | 待决策的业务状态（如工单 JSON、对话文本），对象将被序列化后送入模型 |
| `image` 或 `images` | `Object / Array<Object>` | 否（仅 `decision-model`） | 单图或最多 16 张图（每请求），格式为 `url` 或 `data:image/...;base64,...` |
| `questions` | `Object` | 是 | 键为自定义 question ID，值为含 `type`、`instructions`、`criteria` 的问题对象 |

> **注意**：`questions` 中每个问题的 `criteria` 格式严格依赖 `type` —— `choice` 和 `noul` 使用 `Object` 映射，`score` 使用 `Array` 描述等级顺序。该约束在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确定义，与通用 LLM 接口的 `tools` 或 `function calling` 语义完全不同。

## 使用方式

- **协议与端点**：统一使用 TypeSafe System One 协议，HTTP POST 到 `/compatible-mode/v1/systemone`，Endpoint 需按地域拼接（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`）。
- **认证**：Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需预先配置为环境变量。
- **SDK 调用**：
  - Python：DashScope SDK ≥ 2.0.1，使用 `client.decision.create(...)`；
  - Java：DashScope SDK ≥ 2.23.3，使用 `DecisionModel.call(...)`；
  - 其他语言或自定义客户端：直接构造 JSON 请求体并调用上述 Endpoint。
- **调试建议**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线体验预设场景（如客服对话判断、Agent 完成度核验），可实时观察结果、概率分布与 [Token](../concepts/token.md) 用量变化 —— 此能力在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确推荐。

## 限制和注意事项

- 单次请求最多 16 个问题；问题数增加会导致延迟近似线性上升。
- `choice` 选项数 ≤ 255；`score` 等级数 2–255（强烈建议 3–7 级，确保语义可区分）。
- `decision-model` 上下文上限 268,288 Token；`decision-model-preview` 为 65,536 Token；超长 `state` 将被服务端拒绝。
- 图像输入不支持 SDK 封装（截至 DashScope Python SDK 2.0.1），必须使用原始 HTTP 调用；若混用 `image` 与 `questions`，请确保 `state` 文本明确提示模型关注图像内容（如 `"请看图片内容做判断。"`）。
- 所有响应均为结构化 JSON，无自由文本生成字段；`answers` 中每个 question ID 对应的结果对象包含 `.choice` / `.noul` / `.score` 属性及 `.probabilities` 字段，开发者应直接解析而非正则提取。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


