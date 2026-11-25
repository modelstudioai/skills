# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级前向推理模型，一次调用即可并行返回多个分类、是非判断或有序评分结果及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体完成度校验、任务路由等低延迟、高吞吐的确定性决策场景。其能力在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中完整定义。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），通过 `POST /compatible-mode/v1/systemone` 接口调用。
- 支持三类问题类型：
  - `choice`：多选一判定（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非判断，返回 `P(yes)` 概率值（0.0–1.0），语义上等价于二分类；
  - `score`：有序量表打分（如严重度 1–4 级），返回加权得分索引、各级概率分布及置信度。
- 所有结果均为结构化 JSON，无自由文本输出，因此推理延迟与成本与输出长度无关，仅受输入 token 数与问题数量影响。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | 是 | 待决策的业务上下文（如工单 JSON、对话文本），最大 65536 tokens；超长将被拒绝 |
| `questions` | `Object` | 是 | 键为问题 ID（自定义字符串），值为问题对象，含 `type`、`instructions` 和 `criteria` 字段 |

问题对象字段说明：
- `type`：必填，取值 `"choice"` / `"noul"` / `"score"`；
- `instructions`：可选，自然语言描述问题或评判标准；
- `criteria`：按类型可选：
  - `choice`：`{ "key": "description", ... }` 映射（1–255 项，建议包含 `"other"` 兜底）；
  - `noul`：可选 `{ "true": "...", "false": "..." }` 描述（非必需，模型可自主理解）；
  - `score`：`["等级1描述", "等级2描述", ...]` 数组（2–255 级，**强烈建议 3–7 级**，且每级语义需清晰可区分）。

> **注意**：文档中明确要求 `score` 等级数为 2–255，但 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的“接口限制与建议”部分强调“建议 3–7 级且每级可清晰区分”，实践中使用 2 级易导致置信度偏低、区分度不足，应优先遵循该建议。

## 使用方式

支持三种调用路径，均需配置 `DASHSCOPE_API_KEY` 环境变量（参见 [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）：

- **DashScope SDK（推荐）**：
  - Python：`dashscope>=2.0.1`，使用 `client.decision.create(...)`（[决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 提供完整示例）；
  - Java：`dashscope-sdk-java>=2.23.3`，使用 `DecisionModel.call(...)`；
- **TypeSafe SDK**：通用协议兼容，`base_url` 指向 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `system_one(...)`；
- **原生 HTTP/curl**：直接 POST 至对应地域 endpoint（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`）。

所有方式均需替换 `{WorkspaceId}` 为实际业务空间 ID，并确保地域匹配（Endpoint 域名由地域决定）。SDK 会自动拼接路径与处理鉴权，无需手动构造 URL。

## 限制和注意事项

- **并发与规模限制**：
  - 单次请求最多 16 个问题（延迟随问题数近线性增长）；
  - `choice` 选项上限 255 个；
  - `score` 等级上限 255 级，但 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 明确建议 3–7 级；
  - 输入 `state` 上下文上限 65536 tokens，超限将返回 400 错误。
- **行为约束**：
  - 不支持流式响应（`stream: true` 无效）；
  - 不支持 `system` / `messages` 等聊天式参数，仅接受 `state` + `questions` 结构；
  - `noul` 问题不返回 `P(no)`，仅返回 `P(yes)`（`1.0 - P(yes)` 即为 `P(no)`）；
- **调试建议**：
  - 开发阶段务必先使用 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线验证逻辑与效果（选择预设场景快速试跑）；
  - 关注 `result.usage.input_tokens` 与 `result.latency_ms` 监控性能；
  - 对模糊边界 case，可通过调整 `instructions` 或细化 `criteria` 描述提升一致性。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


