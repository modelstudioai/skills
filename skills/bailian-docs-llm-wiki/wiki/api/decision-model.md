# decision model

决策模型是百炼平台提供的专用推理服务，遵循 System One 协议，支持单次前向调用同步返回结构化决策结果（包括分类标签、置信度评分、是非判断及对应概率分布）。该模型适用于风控审核、内容合规判定、策略路由等需明确输出决策信号的场景。其设计目标是低延迟、高确定性，不生成自由文本。

## 支持的模型/功能

- 当前正式可用的模型为 `decision-model`（GA 版本），提供标准化的三元决策输出：`label`（字符串分类）、`score`（0–1 浮点置信分）、`is_true`（布尔是非判断）；  
- 同时返回完整概率分布（`probabilities` 字段）与各标签置信度（`confidence` 字段），详见 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md)；  
- 预览模型 `decision-model-preview` 仅用于能力验证，不承诺 SLA，其上下文长度、吞吐限流与定价详见 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input` | string | 是 | 待决策的原始文本输入，最大长度 8192 tokens（超出将被截断） |
| `system_prompt` | string | 否 | 决策任务定义（如“判断是否含欺诈风险”），影响 `label` 和 `is_true` 语义，不可为空字符串 |
| `temperature` | float | 否 | 固定为 `0.0`，模型不支持采样，所有请求 deterministic 输出 |
| `top_p` / `max_tokens` | — | 否 | 不生效，决策模型无 token 生成行为，[决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md) 明确禁用此类参数 |

> **注意**：原始文档中 `decision-model-preview` 的上下文限制标注为“16K”，但 GA 版 `decision-model` 实际限制为 8192 tokens，以 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md) 中 GA 版本说明为准，预览文档存在过时描述。

## 使用方式

1. 通过百炼控制台或 OpenAPI 调用 `/v1/models/decision-model:predict` 端点；  
2. 请求体为 JSON，必须包含 `input` 和非空 `system_prompt`；示例：
   ```json
   {
     "input": "用户申请贷款金额50万元，近3个月逾期2次",
     "system_prompt": "判断该申请是否存在高欺诈风险"
   }
   ```
3. 响应体含 `label`（如 `"HIGH_RISK"`）、`score`（如 `0.92`）、`is_true`（如 `true`）及 `probabilities` 数组，完整字段定义见 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- 输入 `input` 超过 8192 tokens 将被静默截断，不报错；`system_prompt` 超长同样截断，建议 ≤ 512 字符；  
- 不支持 streaming、logprobs、function calling 等通用大模型功能；  
- 模型不接受图像、音频等多模态输入，仅处理纯文本；  
- 若 `system_prompt` 语义模糊（如“请做合理判断”），`label` 可能返回默认值 `"UNKNOWN"`，此时 `score` 通常 < 0.5；  
- 所有调用受百炼统一限流策略约束，具体配额见 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md) 中“GA 版本限流”章节。

## 来源文档

- [决策模型](../../raw/model-api-reference/decision-model.md)


