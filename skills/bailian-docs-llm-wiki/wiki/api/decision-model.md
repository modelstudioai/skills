# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级推理模型，一次前向计算即可同步返回分类、是非判断与有序评分三类结果及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体完成度校验、任务路由等高频、低延迟、强确定性的业务场景。其接口协议兼容 TypeSafe System One，开发者可通过 DashScope SDK 或通用 TypeSafe SDK 快速集成。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`，通过 `POST /compatible-mode/v1/systemone` 接口调用。
- 支持三类结构化问题并行求解：
  - `choice`：多选一分类（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非二元判断（如“是否需升级”），返回 P(yes) 概率值（0–1）；
  - `score`：有序量表打分（如“严重度 1–4 级”），返回概率加权期望分数（可为浮点数，如 `2.25`）、各级概率及置信度。
- 所有结果均附带 `probabilities` 分布与（对 `choice`/`score`）`confidence`，便于下游做阈值过滤或融合决策。详情见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | 是 | 待决策的原始业务上下文（如工单文本、对话 JSON 或结构化对象），将被序列化后送入模型 |
| `questions` | `Object` | 是 | 键为自定义问题 ID，值为问题对象；每个问题对象含 `type`（`choice`/`noul`/`score`）、`instructions`（可选描述）及 `criteria`（按类型要求提供） |
| `criteria`（`choice`） | `Object` | 是（当 `type=choice`） | `"选项名" → "选项描述"` 映射，建议覆盖全部选项并包含 `"other"` 兜底项（上限 255 项） |
| `criteria`（`noul`） | `Object` | 否（可省略） | 可指定 `{"true": "...", "false": "..."}` 描述，增强语义对齐 |
| `criteria`（`score`） | `Array` | 是（当 `type=score`） | 从低到高排列的等级描述数组（如 `["轻微", "中等", "严重"]`），长度 2–255，**推荐 3–7 级**且语义可清晰区分 |

> **注意**：`questions` 中问题总数上限为 16，超出将被拒绝；`state` 上下文长度上限为 65536 token，超长请求直接失败。详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 使用方式

- **SDK 调用（推荐）**：
  - Python：使用 DashScope SDK **≥2.0.1**，调用 `client.decision.create(...)`；旧版本无该接口，会抛 `AttributeError`。安装命令：`pip install -U "dashscope>=2.0.1"`。
  - Java：使用 DashScope SDK **≥2.23.3**，引入 `com.alibaba.dashscope.decision` 包；Maven 坐标：`com.alibaba:dashscope-sdk-java:2.23.3`。
  - SDK 自动拼接 endpoint（基于 `workspace` 和 `region`），无需手动构造 URL。
- **通用 TypeSafe SDK**：安装 `typesafe-sdk`，设置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `client.system_one(...)`。
- **curl 直连**：需手动替换 `{WorkspaceId}` 并指定地域 endpoint，Header 设置 `Authorization: Bearer $DASHSCOPE_API_KEY` 与 `Content-Type: application/json`。完整示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- **性能与容量**：
  - 单次请求最多 16 个问题；延迟随问题数近似线性增长。
  - `choice` 选项数 ≤ 255；`score` 等级数 2–255（强烈建议 3–7 级，过多易导致语义模糊、置信度下降）。
  - 输入 `state` 长度上限 65536 token；超长将直接拒绝，不截断。
- **行为约束**：
  - 模型**不生成任何文本输出**，仅返回结构化答案与概率分布，因此响应延迟与成本与输出长度无关。
  - `noul` 类型仅返回 `noul` 字段（P(yes)），不返回 `true`/`false` 字符串；`score` 返回浮点索引（如 `2.25`），非整数等级。
- **环境依赖**：
  - API Key 必须配置为环境变量 `DASHSCOPE_API_KEY`（DashScope SDK 默认读取）或显式传入。
  - 工作空间 ID（`{WorkspaceId}`）与地域（如 `cn-beijing`）需在初始化 client 或构造 URL 时明确指定，各地域 endpoint 不同。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


