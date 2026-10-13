# decision model

decision model 是百炼平台提供的专用结构化决策模型（`decision-model-preview`），通过一次前向推理同步返回多类决策结果（分类、是非判断、量表评分）及其概率分布与置信度，**不生成自由文本**。适用于工单分流、内容审核、智能体任务路由、结果校验等低延迟、高确定性要求的场景。其设计严格遵循 TypeSafe System One 协议，接口语义明确、输出可解析性强，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），无其他变体或微调分支。
- 支持三类结构化问题并行求解：
  - `choice`：多选一分类（如「派单团队」），返回选中项、各选项概率及置信度；
  - `noul`：是非判断（Yes/No），返回 P(yes) 概率值（0.0–1.0）；
  - `score`：有序量表评分（如严重度 1–4 级），返回加权期望分（可为浮点数）、各级概率及置信度。
- 所有结果均基于同一 `state` 输入联合推理，保证逻辑一致性；完整能力说明请参见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✓ | 固定为 `"decision-model-preview"` |
| `state` | string / object / array | ✓ | 待决策的业务上下文；对象会被序列化为字符串送入模型 |
| `questions` | object | ✓ | 键为问题 ID，值为问题定义对象，含 `type`、`instructions`、`criteria`（按类型可选） |
| `type` | string | ✓ | 取值 `"choice"` / `"noul"` / `"score"` |
| `criteria` | object (choice/noul) 或 array (score) | △ | `choice`: 选项名→描述映射（建议含 `"other"`）；`noul`: 可选 `{"true": "...", "false": "..."}`；`score`: 从低到高的等级描述数组（建议 3–7 级） |

> **注意**：文档中 `score` 等级数范围存在表述差异——请求参数节写“2–255 级（建议 3–7）”，而返回示例中 `legend` 的索引为 `"0"`–`"3"`（共 4 级）。实际以运行时 `criteria` 数组长度为准，索引从 `0` 开始；该不一致已在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中统一按数组长度解释，开发者应以 `len(criteria)` 作为等级总数。

## 使用方式

- **协议与端点**：`POST /compatible-mode/v1/systemone`，需替换 `{WorkspaceId}` 并选择对应地域（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`）。
- **认证**：Header 中传 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量（参见 [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）。
- **SDK 推荐**：使用 `typesafe-sdk`（`pip install typesafe-sdk`），自动处理路径拼接与响应解析，示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。
- **调试建议**：首次集成前，务必通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线验证问题定义与结果分布。

## 限制和注意事项

- **性能**：问题数建议 ≤ 16（延迟近线性增长）；`choice` 选项 ≤ 255；`score` 等级建议 3–7 级（清晰区分优先于数量）。
- **上下文**：最大输入长度为 65536 token，超长 `state` 将被截断或拒绝，无自动摘要。
- **输出确定性**：不支持 `temperature` 等采样参数，所有输出为确定性前向结果。
- **错误排查**：失败时返回标准错误码，详细说明见 [错误信息](raw/model-api-reference/preparations/error-code.md)（注意该路径为相对引用，非 `../../raw/` 格式，故不在此处转换为 Wiki 链接）。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


