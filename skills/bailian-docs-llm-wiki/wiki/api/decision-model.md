# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级推理模型，一次前向计算即可返回分类、是非判断、有序评分及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体完成度校验、任务路由等低延迟、高并发的确定性决策场景。其输出为纯结构化结果，延迟与成本与输出长度无关，与 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 定义的 TypeSafe System One 协议严格对齐。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），仅支持通过 `POST /compatible-mode/v1/systemone` 接口调用。
- 支持三类结构化问题：
  - `choice`：多选一分类（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非判断（如“是否需升级”），返回 `P(yes)` 概率值（0.0–1.0）；
  - `score`：有序量表评分（如“严重度 1–4 级”），返回加权得分索引、各级概率分布及置信度。
- 所有结果均附带概率分布与置信度（`confidence` 字段），便于下游做阈值过滤或融合决策。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | 是 | 待决策的原始业务上下文（如工单 JSON、对话文本），最大 65536 token；超长将被拒绝 |
| `questions` | `Object` | 是 | 键为问题 ID（字符串），值为问题对象；最多支持 **16 个问题** |
| `questions.*.type` | `String` | 是 | 取值 `"choice"` / `"noul"` / `"score"` |
| `questions.*.instructions` | `String` | 否 | 问题语义描述或评判标准，影响判断准确性 |
| `questions.*.criteria` | `Object` 或 `Array` | 视类型而定 | `choice`: `{key: desc}` 映射（≤255 项）；`noul`: 可选 `{true: "...", false: "..."}`；`score`: 从低到高的等级描述数组（2–255 级，**强烈建议 3–7 级**） |

> **注意**：文档中明确要求 `score` 等级数范围为 2–255，但 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的“接口限制与建议”部分强调“建议 3–7 级且每级可清晰区分”，实践中使用 2 级（如 `[low, high]`）可能导致判别粒度不足，应优先遵循该建议。

## 使用方式

- **SDK 调用（推荐）**：
  - Python：DashScope SDK ≥ `2.0.1`，使用 `client.decision.create()` 方法（[决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中已提供完整示例）；
  - Java：DashScope SDK ≥ `2.23.3`，使用 `com.alibaba.dashscope.decision` 包；
  - TypeSafe SDK：通用 `typesafe-sdk`（`system_one()` 方法），需手动指定 `base_url` 为业务空间网关地址（含 `/compatible-mode` 路径）。
- **HTTP 直连**：构造 `POST` 请求至对应地域 Endpoint（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），Header 包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。
- **在线调试**：可通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 快速验证，支持预设场景（客服判断、Agent 核验、工单分流等），详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的“在线体验”说明。

## 限制和注意事项

- **QPS 与配额**：受百炼平台统一配额管控，具体额度请在控制台查看，未单独开放决策模型专属限流配置。
- **上下文长度**：`state` 输入上限为 **65536 token**，超长请求将直接被拒绝（非截断）。
- **问题规模**：单次请求最多 16 个 `questions`，延迟随问题数近线性增长；`choice` 选项数 ≤ 255，`score` 等级数 2–255（但实际建议 3–7 级）。
- **无文本生成**：该模型**不输出任何自由文本**，仅返回结构化判定结果（`answers` 对象），因此不可用于摘要、改写等生成类任务。
- **环境依赖**：API Key 必须通过环境变量 `DASHSCOPE_API_KEY` 配置（SDK 默认读取），或显式传入；未配置时调用将失败。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


