# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级前向推理模型，一次调用可并行完成多类判断（分类、是非、评分），返回概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体任务路由、结果校验等低延迟、高确定性要求的场景。其协议基于 TypeSafe System One，通过 `POST /compatible-mode/v1/systemone` 接口调用，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），无其他变体或历史版本。
- 支持三类结构化问题并行求解：
  - `choice`：多选一分类（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如严重度 1–4 级），返回概率加权期望分数（可为浮点数，如 `2.43`）、各级概率及置信度。
- 所有输出均为确定性结构化数据，**无自由文本生成**，因此响应延迟与输出长度无关，适合高频调用。该特性在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确强调。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | 是 | 待决策的原始业务上下文（如工单文本、对话 JSON 或结构化对象）；对象将被序列化后送入模型 |
| `questions` | `Object` | 是 | 键为自定义 question ID，值为问题对象；单次最多 16 个问题 |
| `questions.*.type` | `String` | 是 | 取值：`"choice"` / `"noul"` / `"score"` |
| `questions.*.instructions` | `String` | 否 | 问题语义描述或评判标准（建议提供，提升准确性） |
| `questions.*.criteria` | `Object` / `Array` | 视类型而定 | `choice`：选项名→描述映射（≤255 项，建议含 `"other"`）；`noul`：可选 `{"true": "...", "false": "..."}`；`score`：等级描述数组（2–255 级，**强烈建议 3–7 级**，且每级语义需可区分） |

> **注意**：`state` 超过 65536 token 将被拒绝，此限制在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确定义，但部分旧版 SDK 文档未同步更新该阈值，请以本页为准。

## 使用方式

- **SDK 调用（推荐）**：
  - Python：需 `dashscope>=2.0.1`，使用 `client.decision.create(...)`；
  - Java：需 `dashscope-sdk-java>=2.23.3`，使用 `DecisionModel.call(...)`；
  - 两者均自动拼接 `/compatible-mode/v1/systemone` 端点，并从环境变量 `DASHSCOPE_API_KEY` 读取密钥。
- **通用 TypeSafe SDK**：安装 `typesafe-sdk`，设置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `client.system_one(...)`。
- **curl 直连**：需手动构造完整 endpoint（含 `{WorkspaceId}` 和地域域名），Header 设置 `Authorization: Bearer $DASHSCOPE_API_KEY` 与 `Content-Type: application/json`。

所有方式均遵循同一请求/响应 Schema，示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- **并发与规模限制**：
  - 单次请求最多 16 个 `questions`（延迟随问题数近线性增长）；
  - `choice` 选项数 ≤ 255，`score` 等级数 2–255（生产环境建议 3–7 级）；
  - `state` 上下文上限 65536 token，超长将直接拒收。
- **行为约束**：
  - 不支持流式响应（`stream: true` 无效）；
  - 不支持 `system` / `user` / `assistant` 消息角色划分，仅接受扁平 `state` 输入；
  - `noul` 类型不返回置信度（仅 `choice` 和 `score` 返回 `confidence` 字段）。
- **调试建议**：
  - 开发阶段务必先通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线验证逻辑与输出分布；
  - 错误排查优先检查 `request_id` 与 `latency_ms`，错误码参考 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


