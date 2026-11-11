# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的推理模型，一次前向计算即可同步返回分类（choice）、是非判断（noul）和有序评分（score）三类结果及其概率分布与置信度，**不生成自由文本**。适用于工单分流、内容审核、智能体任务路由、完成度校验等低延迟、高确定性要求的业务场景。其协议基于 TypeSafe System One，接口路径为 `POST /compatible-mode/v1/systemone`。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)）。
- 支持三类结构化问题并行求解：
  - `choice`：多选一分类（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如严重度 1–4 级），返回概率加权期望分数（可为浮点数，如 `2.25`）、各级概率及置信度。
- 所有结果均附带 `probabilities` 分布与 `usage.input_tokens`、`latency_ms` 等可观测字段，便于质量监控与成本核算。

## 关键参数

| 参数 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | `String` | Body | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | Body | 是 | 待决策的原始输入（如工单文本、对话 JSON 或结构化对象），将被序列化后送入模型 |
| `questions` | `Object` | Body | 是 | 问题集合，key 为自定义 question_id；value 为含 `type`、`instructions`、`criteria` 的对象（详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)） |
| `Authorization` | `String` | Header | 是 | `Bearer $DASHSCOPE_API_KEY` |
| `Content-Type` | `String` | Header | 是 | `application/json` |

> **注意**：`questions` 中每个问题的 `criteria` 字段格式严格依赖 `type`：`choice` 要求 `Map<String, String>`，`noul` 可选 `{"true": "...", "false": "..."}`，`score` 要求 `String[]`（升序排列）。未按规范提供将导致 400 错误 —— 此约束在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确列出，但部分旧版 SDK 示例曾省略 `criteria`，请以该文档为准。

## 使用方式

### SDK 调用（推荐）

- **Python**：需 `dashscope>=2.0.1`，使用 `client.decision.create()` 方法（[安装 SDK](../../raw/model-api-reference/preparations/install-sdk.md)）。
- **Java**：需 `dashscope-sdk-java>=2.23.3`，使用 `DecisionModel` 类（[错误信息](../../raw/model-api-reference/preparations/error-code.md) 文档中亦提及 Java 版本兼容性要求）。
- SDK 自动拼接 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），无需手动构造 URL。

### 通用 HTTP 调用

- 直接调用 `POST /compatible-mode/v1/systemone`，需显式指定 `base_url`（含 `{WorkspaceId}` 和地域域名）。
- 支持 `typesafe-sdk`（`pip install typesafe-sdk`），通过 `client.system_one()` 调用，自动解析响应结构。

## 限制和注意事项

- **数量限制**：单次请求最多 16 个问题；`choice` 选项数 ≤ 255；`score` 等级数 2–255（**强烈建议 3–7 级**，确保语义可区分）。
- **上下文长度**：`state` 序列化后总 token 数上限为 65536，超长将直接拒绝（非截断）。
- **延迟特性**：延迟随问题数近线性增长，与输出长度无关（因无文本生成）。
- **环境依赖**：API Key 必须通过环境变量 `DASHSCOPE_API_KEY` 提供（或显式传入 SDK），否则调用失败。
- **地域 Endpoint**：华北2（北京）与新加坡等地域 endpoint 域名不同，需按 [地域与域名](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain) 配置，不可混用。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


