# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级推理模型，一次前向计算即可返回分类、是非判断与有序评分三类结果及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体任务路由、完成度校验等高频、低延迟、强确定性的业务场景。其接口协议兼容 TypeSafe System One，开发者可通过 DashScope SDK 或通用 TypeSafe SDK 快速集成。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`，属于预览版（preview），能力稳定但可能随迭代演进。
- 支持三类结构化问题：
  - `choice`：多选一分类（如“派单团队”），返回选中选项名、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非二元判断（如“是否需升级”），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如“严重度 1–4 级”），返回概率加权期望等级索引（可为浮点数，如 `2.43`）、各级概率及置信度。
- 所有类型均返回完整 `probabilities` 分布，便于下游做阈值过滤或不确定性分析。

该模型能力定义与语义规范详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 文档。

## 关键参数

| 字段 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | 是 | 待决策的原始业务上下文，支持文本、JSON 对象或数组；对象将被序列化后送入模型 |
| `questions` | `Object` | 是 | 键为自定义问题 ID，值为问题对象；每个问题必须指定 `type`（`choice`/`noul`/`score`） |
| `questions.*.instructions` | `String` | 否 | 问题描述或评判标准，用于引导模型理解意图 |
| `questions.*.criteria` | `Object` / `Array` | 视 `type` 而定 | `choice`：选项名→描述映射（建议含 `other` 兜底）；`noul`：可选 `{"true": "...", "false": "..."}`；`score`：从低到高排列的等级描述数组（建议 3–7 级） |

> **注意**：`questions` 中 `choice` 选项数上限为 255，`score` 等级数范围为 2–255，但文档明确建议使用 3–7 级以保证语义区分度——此约束在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中多次强调，实际部署时应严格遵循。

## 使用方式

### SDK 集成（推荐）

- **Python**：需 `dashscope>=2.0.1`，调用 `client.decision.create(...)`  
- **Java**：需 `dashscope-sdk-java>=2.23.3`，使用 `com.alibaba.dashscope.decision` 包  
- SDK 自动拼接 `/compatible-mode/v1/systemone` 端点，并根据 `workspace` 和 `region` 构造地域化域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`）

### 通用 TypeSafe SDK

安装 `typesafe-sdk`，手动指定 `base_url` 为业务空间网关的 `compatible-mode` 路径（不含 `/v1/systemone`），调用 `client.system_one(...)` 即可。

### 原生 HTTP（curl）

直接 POST 到对应地域 endpoint（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），Header 需含 `Authorization: Bearer $DASHSCOPE_API_KEY` 与 `Content-Type: application/json`。

所有调用方式均需提前配置 `DASHSCOPE_API_KEY` 环境变量，配置方法见 [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。更多细节请参考 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- **请求限制**：单次最多 16 个问题；`state` 上下文长度上限为 65536 token，超长将被拒绝。
- **延迟特性**：服务端耗时（`latency_ms`）随问题数量近似线性增长，不随输出长度变化（因无文本生成）。
- **SDK 版本强依赖**：旧版 DashScope SDK 不支持 `decision` 接口，调用将抛出 `AttributeError`（Python）或 `ClassNotFoundException`（Java）；务必核对版本要求。
- **地域与域名**：Endpoint 中 `{WorkspaceId}` 必须替换为真实业务空间 ID，且需匹配所选地域（如北京、新加坡），否则返回 404 或鉴权失败。
- **错误处理**：失败时 Python SDK 抛 `DashScopeError`，Java SDK 抛 `ApiException`；完整错误码列表见 [错误信息](raw/model-api-reference/preparations/error-code.md) —— 注意该路径为相对引用，实际文档位于 `../../raw/model-api-reference/preparations/error-code.md`。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


