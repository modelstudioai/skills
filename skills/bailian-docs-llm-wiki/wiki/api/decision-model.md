# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级前向推理模型，一次调用即可并行返回多类判定结果（分类、是非、评分）及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体完成度校验、任务路由等低延迟、高确定性要求的场景。其接口协议兼容 TypeSafe System One，开发者可通过 DashScope SDK 或通用 TypeSafe SDK 快速集成。

## 支持的模型/功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），通过 `POST /compatible-mode/v1/systemone` 接口调用。
- 支持三类结构化问题并行求解：
  - `choice`：多选一分类（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`：是非判断（Yes/No），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表评分（如严重度 1–4 级），返回概率加权期望分数（可为浮点数，如 `2.25`）、各级概率及置信度。
- 所有判定均基于输入 `state` 一次性前向完成，无 token 生成开销，延迟与输出长度无关。详细能力说明见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | `String` | Body | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | Body | 是 | 待决策的业务上下文（如工单文本、对话 JSON 或结构化对象）；对象将被序列化后送入模型 |
| `questions` | `Object` | Body | 是 | 问题字典，key 为自定义 question_id；value 为含 `type`、`instructions`、`criteria` 的问题对象 |
| `type` | `String` | `questions[xxx]` | 是 | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria` | `Object` / `Array` | `questions[xxx]` | 视类型 | `choice`: `{option_key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 等级描述数组（2–255 项，推荐 3–7 级） |

> **注意**：`questions` 中每个问题的 `criteria` 字段在 `noul` 类型下为**可选**，但若提供，必须为 `{"true": ..., "false": ...}` 格式；未提供时模型仍可执行基础是非判断，但语义边界可能弱于显式定义。该行为与 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中“`noul`：可选 `{"true":…, "false":…}` 描述”的说明一致，无矛盾。

## 使用方式

- **SDK 调用（推荐）**：
  - Python：使用 DashScope SDK ≥2.0.1，调用 `client.decision.create(...)`；安装命令：`pip install -U "dashscope>=2.0.1"`。详见 [安装 SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
  - Java：使用 DashScope SDK ≥2.23.3，引入 `com.alibaba:dashscope-sdk-java:2.23.3`，调用 `DecisionModel.call(...)`。
  - 两者均自动拼接 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），无需手动构造 URL。
- **通用 TypeSafe SDK**：安装 `typesafe-sdk`，设置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `client.system_one(...)`。
- **curl**：直接 POST 到对应地域 endpoint，需手动设置 `Authorization` 和 `Content-Type` 头。完整示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- **数量限制**：单次请求最多 16 个问题；`choice` 选项 ≤255 个；`score` 等级数 2–255（强烈建议 3–7 级以保障区分度）。
- **上下文长度**：`state` 序列化后总 token 数上限为 65536；超长将被拒绝，不截断。
- **延迟特性**：服务端耗时（`latency_ms`）随问题数近线性增长，建议按需聚合问题而非拆分为多次调用。
- **错误处理**：调用失败时，Python SDK 抛出 `DashScopeError`，Java SDK 抛出 `ApiException`；具体错误码含义参见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。
- **环境依赖**：API Key 必须配置为环境变量 `DASHSCOPE_API_KEY`（SDK 默认读取），或显式传入 `api_key` 参数。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


