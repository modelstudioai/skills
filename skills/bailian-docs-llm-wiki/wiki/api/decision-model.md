# decision model

decision model 是百炼平台提供的专用结构化决策模型（`decision-model-preview`），专为工单分流、内容审核、智能体路由、结果校验等高频、低延迟、强确定性的结构化判断场景设计。它不生成自由文本，而是对输入 `state` 一次性完成多个 typed 问题（`choice`/`noul`/`score`）的联合推理，返回分类结果、是非概率、有序评分及其置信度与完整概率分布。该能力基于 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 实现，协议兼容 TypeSafe System One。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），无其他变体或微调版本。
- 支持三类结构化问题：
  - `choice`：多选一判定（如“派单团队”），返回选中选项名、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（浮点数，范围 [0,1]）；
  - `score`：有序量表打分（如严重度 1–4 级），返回概率加权期望得分（可为小数）、各级概率及置信度。
- 所有类型均返回完整 `probabilities` 分布，便于下游做阈值控制或不确定性分析。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | 是 | 待决策的原始业务上下文（如工单文本、对话 JSON 或结构化对象）；对象将被序列化后送入模型 |
| `questions` | `Object` | 是 | 键为自定义 question ID，值为问题对象；每个问题必须指定 `type` 及对应 `criteria`（详见下表） |

**问题对象 (`questions[key]`) 的关键字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `String` | 必填，取值 `"choice"` / `"noul"` / `"score"` |
| `instructions` | `String` | 可选，用于明确评判标准（如 `"是否需要立即通知值班人员？"`） |
| `criteria` | `Object` 或 `Array` | **按 type 区分**：<br>• `choice`：`{"option_key": "描述"}` 映射（建议含 `"other"` 兜底项，≤255 项）<br>• `noul`：可选 `{"true": "...", "false": "..."}` 描述（非必需，但推荐提供以提升一致性）<br>• `score`：从低到高排列的等级描述数组（建议 3–7 级，2–255 级合法） |

> **注意**：文档中 `noul` 的 `criteria` 字段标注为“可选”，但实测表明，若完全省略 `criteria`（即空对象或 null），部分 SDK 版本可能触发解析异常；建议始终显式传入 `{"true": "...", "false": "..."}`。详情参见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中“问题对象属性”章节。

## 使用方式

### SDK 调用（推荐）

- **Python**：需 DashScope SDK ≥ `2.0.1`，使用 `client.decision.create()` 方法。安装命令：`pip install -U "dashscope>=2.0.1"`。SDK 自动拼接 endpoint 并处理序列化，[安装 SDK](../../raw/model-api-reference/preparations/install-sdk.md) 文档已同步更新。
- **Java**：需 DashScope SDK ≥ `2.23.3`，使用 `com.alibaba.dashscope.decision` 包。Maven 坐标：`com.alibaba:dashscope-sdk-java:2.23.3`。
- **通用 TypeSafe SDK**：支持 `typesafe-sdk`（`pip install typesafe-sdk`），通过 `client.system_one()` 调用，需手动指定 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`。

### 直接 HTTP 调用

- **Endpoint**：`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`
- **Headers**：`Authorization: Bearer $DASHSCOPE_API_KEY`，`Content-Type: application/json`
- **Body**：JSON 格式，包含 `model`、`state`、`questions` 字段（示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)）。

## 限制和注意事项

- **请求限制**：
  - 单次请求最多 16 个问题（`questions` 对象 key 数），延迟随问题数近线性增长；
  - `choice` 选项数 ≤ 255，`score` 等级数 2–255（强烈建议 3–7 级，确保语义可区分）；
  - 输入 `state` 上下文上限 65536 token，超长将直接拒绝（不截断）。
- **环境依赖**：
  - 必须配置 `DASHSCOPE_API_KEY` 环境变量（或显式传入），否则 SDK 报错；
  - Workspace ID 与地域需匹配，Endpoint 域名规则详见 [地域与域名](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
- **行为约束**：
  - 模型**不生成任何文本输出**，仅返回结构化答案，因此响应延迟与输出长度无关；
  - 返回中的 `confidence` 仅对 `choice` 和 `score` 类型有效，`noul` 类型无此字段；
  - `score` 的 `score` 字段为浮点数（如 `2.25`），表示概率加权索引，非整数等级。

> **注意**：原始文档中 Java SDK 示例使用 `DecisionQuestion.noul("...")` 构造器，但其底层未透出 `criteria` 参数；而 Python SDK 和 curl 示例均支持显式传入 `criteria`。为保证跨语言行为一致，**所有 `noul` 问题均应通过 `criteria` 显式定义 true/false 语义**，避免因 SDK 差异导致判断偏差。该实践已在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的“是非判断示例”中体现。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


