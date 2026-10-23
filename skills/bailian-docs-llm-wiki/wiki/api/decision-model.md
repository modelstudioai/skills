# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，不生成文本，仅输出分类、是非判断、有序评分及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、任务完成度校验等低延迟、高并发的确定性决策场景。其核心能力基于 TypeSafe System One 协议实现一次前向即返回多问题答案，响应延迟与输出长度无关 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一可用模型：`decision-model-preview`（预览版），通过 `POST /compatible-mode/v1/systemone` 接口调用。
- 支持三类结构化问题：
  - `choice`：多选一决策（如「派单团队」），返回选中选项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非判断（如「是否需升级」），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表评分（如「严重度 1–4 级」），返回加权期望分（可为浮点数）、各级概率及置信度。
- 所有类型均返回完整 `probabilities` 分布，便于下游做阈值控制或不确定性分析 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✓ | 固定为 `"decision-model-preview"` |
| `state` | string / object / array | ✓ | 待决策的业务上下文；对象会被序列化为字符串送入模型 |
| `questions` | object | ✓ | 键为问题 ID，值为问题定义对象；最多支持 **16 个问题** |
| `questions.*.type` | string | ✓ | 取值 `"choice"` / `"noul"` / `"score"` |
| `questions.*.instructions` | string | ✗ | 问题语义描述，影响判断准确性，建议明确简洁 |
| `questions.*.criteria` | object / array | ✓（`choice`/`score`）<br>✗（`noul`） | `choice`：选项名→描述映射（≤255 项，建议含 `"other"`）；`score`：等级描述数组（2–255 级，**强烈建议 3–7 级**且语义可区分） |

> **注意**：文档中 `noul` 类型未要求 `criteria`，但实际使用中若提供 `{"true": "...", "false": "..."}` 可提升语义对齐效果；该行为在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中未明确定义，属隐式推荐实践。

## 使用方式

- **协议与端点**：使用 `POST` 请求 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`，其中 `{WorkspaceId}` 为业务空间 ID，`{region}` 如 `cn-beijing` 或 `ap-southeast-1`。
- **认证**：Header 中传 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量。
- **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理 endpoint 拼接与响应解析，示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的 Python 调用片段。
- **调试建议**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线体验，选择预设场景快速验证逻辑与结果分布。

## 限制和注意事项

- **请求限制**：
  - 单次最多 16 个问题（延迟近线性增长）；
  - `choice` 选项数 ≤ 255，`score` 等级数 2–255（但 3–7 级为最佳实践）；
  - 输入 `state` 上下文上限 **65536 token**，超长将被拒绝（无截断）。
- **输出特性**：
  - 不生成任何自由文本，仅返回结构化答案（`answers` 对象）；
  - `choice` 和 `score` 类型返回 `confidence`（0.0–1.0），`noul` 仅返回 `noul`（P(yes)）；
  - `score` 的 `score` 字段为浮点期望值（如 `2.25`），非整数索引。
- **其他**：
  - 返回中 `usage.input_tokens` 为实际消耗输入 token 数，可用于成本监控；
  - 错误排查请参考统一错误码文档，详见 [错误信息](raw/model-api-reference/preparations/error-code.md)（注意路径为 raw 下相对路径）。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


