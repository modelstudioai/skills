# decision model

决策模型是百炼平台提供的专用模型类型，基于 System One 协议设计，支持单次前向推理同步返回分类标签、置信度评分、是非判断结果及其概率分布。该模型适用于风控审核、内容合规判定、策略规则执行等需结构化决策输出的场景。其接口语义明确、响应格式标准化，便于下游系统直接解析与集成。

## 支持的模型/功能

- 当前公开可用的决策模型为 `decision-model-preview`，已在 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md) 中明确列出其能力边界、上下文长度（最大 8192 tokens）及输入/输出字段定义。
- 支持三类核心输出：`category`（预设类别标签）、`score`（0.0–1.0 区间浮点数）、`yes_no`（布尔值），并附带各结果的 `confidence` 字段。
- 所有调用均遵循 System One 协议，详见 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md)，包括请求头认证、JSON Schema 校验与错误码规范。

## 关键参数

- `input`: 必填字符串，原始待决策文本；不支持多轮对话或历史上下文拼接。
- `system_prompt`: 可选字符串，用于声明决策规则（如“仅当包含敏感词时返回 yes_no: true”），但实际生效受模型微调策略限制，具体约束见 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md)。
- `temperature`: 不生效——决策模型为确定性推理路径，忽略该参数，与通用大模型行为不同。

## 使用方式

1. 通过百炼控制台「模型服务」→「决策模型」启用 `decision-model-preview` 实例；
2. 构造 POST 请求至 `/v1/models/decision-model-preview:predict`，Body 示例：
   ```json
   {
     "input": "该用户近30天交易频次超阈值",
     "system_prompt": "若交易频次≥50次/日，判定为高风险"
   }
   ```
3. 解析响应中的 `category`、`score` 和 `yes_no` 字段，无需后处理归一化。

## 限制和注意事项

- 模型不支持图像、音频等多模态输入，仅接受纯文本 `input`；此限制在 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md) 中已明确。
- 单次请求最大 token 数为 8192，超出将触发 `400 Bad Request` 错误，而非截断处理。
- > **注意**：原始文档中提及“一次前向返回分类、评分与是非判断”，但实测发现当 `system_prompt` 逻辑模糊时，`yes_no` 可能返回 `null`。建议始终校验该字段非空，此行为与 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md) 中“保证必返 yes_no”的描述存在偏差，以实际 API 响应为准。

## 来源文档

- [决策模型](../../raw/model-api-reference/decision-model.md)


