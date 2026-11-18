# decision model

decision model 是百炼平台提供的专用结构化决策模型（`decision-model-preview`），用于在工单分流、内容审核、智能体路由、结果校验等高频决策场景中，一次性返回分类、是非判断、有序评分及其概率分布与置信度。该模型不生成自由文本，仅输出结构化判定结果，因此推理延迟与成本与输出长度无关，适合低延迟、高确定性要求的业务系统集成。

## 支持的模型/功能

- 当前唯一支持的模型为 `decision-model-preview`，通过 TypeSafe System One 协议调用（`POST /compatible-mode/v1/systemone`）。
- 支持三类结构化问题：
  - `choice`：多选一决策（如“派单团队”），返回选中项、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（0–1 浮点数）；
  - `score`：有序量表评分（如严重度 1–4 级），返回概率加权期望分数（可为小数）、各级概率及置信度。
- 所有判定均基于输入 `state`（文本、JSON 对象或数组）进行联合推理，一次请求最多支持 16 个问题，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | 是 | 待决策的原始业务上下文；对象将被序列化后送入模型 |
| `questions` | `Object` | 是 | 键为自定义 question_id，值为问题对象，含 `type`、`instructions` 和 `criteria`（类型相关） |
| `type` | `String` | 是 | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria` | `Object` 或 `Array` | 视 type | `choice`: `{key: desc}` 映射（≤255 项）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 从低到高的等级描述数组（2–255 级，**建议 3–7 级**） |

> **注意**：`score` 的 `criteria` 数组索引即为等级序号（0-based），返回的 `score` 字段是概率加权期望值（如 `2.25`），而非整数等级；此行为与部分旧文档中“返回整数等级”的描述矛盾，请以 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的返回示例为准。

## 使用方式

- **SDK 调用（推荐）**：
  - Python：需 DashScope SDK ≥ `2.0.1`，使用 `client.decision.create()` 方法；
  - Java：需 DashScope SDK ≥ `2.23.3`，使用 `com.alibaba.dashscope.decision` 包；
  - SDK 自动拼接 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），无需手动构造 URL。
- **通用 TypeSafe SDK**：安装 `typesafe-sdk`，设置 `base_url` 为业务空间网关的 `compatible-mode` 路径，调用 `client.system_one()`。
- **curl 直连**：需手动替换 `{WorkspaceId}` 并指定地域 endpoint，参见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的完整示例。

## 限制和注意事项

- **QPS 与配额**：受百炼平台统一配额管控，具体限流策略请参考控制台配额管理页。
- **上下文长度**：最大支持 65536 token，超长 `state` 将直接拒绝（HTTP 400）。
- **问题规模限制**：
  - 单次请求最多 16 个 `questions`（延迟近似线性增长）；
  - `choice` 选项数 ≤ 255；
  - `score` 等级数 2–255（但实际建议设为 3–7 级，确保语义可区分且模型判别稳定）。
- **环境依赖**：API Key 必须通过环境变量 `DASHSCOPE_API_KEY` 提供，或显式传入 SDK 构造函数；未配置将导致认证失败。
- **调试建议**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线验证逻辑与输出格式，避免因 `criteria` 描述模糊导致置信度偏低。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


