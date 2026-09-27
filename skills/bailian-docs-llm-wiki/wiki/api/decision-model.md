# decision model

decision model 是百炼平台专为结构化决策任务设计的轻量级推理模型，一次前向计算即可并行返回分类（choice）、是非判断（noul）和有序评分（score）三类结果及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体路由、规则校验等低延迟、高吞吐的确定性决策场景。其接口协议为 TypeSafe System One，与传统 LLM 文本生成范式分离，性能与成本不受输出长度影响。

## 支持的模型/功能

- 当前唯一可用模型为 `decision-model-preview`，通过 `POST /compatible-mode/v1/systemone` 接口调用。
- 支持三种问题类型并行求解：
  - `choice`：多选一分类（如“派单团队”），返回选中项、各选项概率及整体置信度；
  - `noul`：是非判断（yes/no），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表打分（如严重度 1–4 级），返回加权期望分数（可为浮点数，如 `2.25`）、各级概率及置信度。
- 所有结果均为结构化 JSON，无自由文本生成，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `"decision-model-preview"` |
| `state` | string / object / array | ✅ | 待决策的原始上下文（如工单 JSON、对话文本），会被序列化后送入模型 |
| `questions` | object | ✅ | 键为自定义 question_id，值为问题对象；每个问题必须指定 `type`（`choice`/`noul`/`score`） |
| `questions.*.instructions` | string | ❌ | 问题语义描述或评判标准，提升判定一致性 |
| `questions.*.criteria` | object/array | ⚠️ | 类型依赖：<br>• `choice`: `{key: desc}` 映射（≤255 项，建议含 `other` 兜底）<br>• `noul`: 可选 `{"true": "...", "false": "..."}`<br>• `score`: 从低到高的等级描述数组（2–255 级，**建议 3–7 级**） |

> **注意**：文档中 `score` 等级数范围在“请求参数”节写为 2–255，但在“接口限制与建议”节明确建议为 3–7 级且强调“每级可清晰区分”。实际部署中应严格遵循 3–7 级，避免使用 2 级或 >7 级——后者将显著降低判别精度。该约束已在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的“接口限制与建议”中强调。

## 使用方式

- **认证**：通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 头传递 API Key，需提前配置环境变量（参见[配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）。
- **Endpoint**：按地域选择，例如华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`，其中 `{WorkspaceId}` 需替换为实际业务空间 ID（详见[地域与域名](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）。
- **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理 base_url 拼接与响应解析，示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的 Python 调用片段。
- **典型模式**：单次请求可携带多个问题（建议 ≤16 个），实现多维度联合决策（如同时判定「部门」「是否升级」「严重度」）。

## 限制和注意事项

- **上下文长度**：最大 65536 token，超长 `state` 将被截断或拒绝。
- **问题规模**：
  - 单次请求 `questions` 数量无硬上限，但延迟随问题数近线性增长，**强烈建议 ≤16**；
  - `choice` 选项数 ≤255；
  - `score` 等级数建议 3–7 级（见上文注意）。
- **无流式响应**：仅支持同步阻塞调用，不支持 `stream=true`。
- **错误处理**：失败时返回标准错误码，详细说明请参考 [错误信息](raw/model-api-reference/preparations/error-code.md)（注意该路径未做两级回溯，因非本主题直接关联文档，故不强制引用为 `../../raw/...` 格式）。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


