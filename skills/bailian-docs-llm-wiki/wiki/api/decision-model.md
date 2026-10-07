# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，不生成文本，仅输出分类、是非判断、有序评分及其概率分布与置信度。适用于工单分流、内容审核、智能体路由、结果校验等低延迟、高并发的确定性决策场景。其核心优势在于输出长度无关的稳定延迟与成本，且支持单次请求并行处理多类问题。

## 支持的模型/功能

- 当前唯一可用模型为 `decision-model-preview`，通过 `POST /compatible-mode/v1/systemone` 接口调用，属于 TypeSafe System One 协议体系 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。
- 支持三类结构化问题：
  - `choice`：多选一决策（如「派单团队」），返回选中选项、各选项概率分布及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如严重度 1–4 级），返回加权期望分数（可为浮点数）、每级概率及置信度。
- 所有问题在一次前向计算中并行完成，**不生成任何文本输出**，因此响应时间与输出长度无关。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `String` | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | 是 | 待决策的业务上下文，将被序列化后送入模型；超长（>65536 token）会被截断或拒绝 |
| `questions` | `Object` | 是 | 键为自定义 question_id，值为问题对象；详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中“问题对象属性”定义 |

问题对象内关键子字段：
- `type`：必须为 `"choice"` / `"noul"` / `"score"`；
- `instructions`：可选，用于明确评判意图；
- `criteria`：按类型提供结构化标准（`choice`: `{"opt1": "desc"}`；`noul`: `{"true": "...", "false": "..."}`；`score`: `["level0 desc", "level1 desc", ...]`）。

> **注意**：文档中 `score` 等级数量描述存在不一致——正文称“2–255 级（建议 3–7 级）”，但示例与返回结构均以 0-based 索引呈现（如 `"legend": {"0": "...", "1": "...", "2": "...", "3": "..."}`）。实际使用应以返回 `legend` 的 key 类型（字符串数字）为准，且 `criteria` 数组长度即为等级总数，索引从 `0` 开始。该细节已在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的“返回示例”中明确体现。

## 使用方式

- **认证**：通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 头传递 API Key，需提前配置环境变量 `DASHSCOPE_API_KEY`（配置方法见[配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）。
- **Endpoint**：按地域选择，例如华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`，其中 `{WorkspaceId}` 需替换为实际业务空间 ID（参见[地域与域名](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）。
- **推荐 SDK**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理 base_url 拼接与响应解析。示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的 Python 调用片段。

## 限制和注意事项

- **问题规模**：单次请求建议 ≤ 16 个问题；延迟随问题数近线性增长。
- **选项/等级上限**：
  - `choice` 最多 255 个选项；
  - `score` 等级数建议 3–7 级（最小 2 级，最大 255 级），但需确保各级语义可清晰区分。
- **上下文长度**：`state` 输入上限为 65536 token；超长内容将被截断，可能影响决策质量。
- **无流式响应**：该模型仅支持同步阻塞式调用，不支持 `stream=true`。
- **错误处理**：失败时返回标准错误码，详细说明请参考 [错误信息](raw/model-api-reference/preparations/error-code.md)（注意路径未带 `../../raw/` 前缀，此为原始文档内部引用，无需调整）。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


