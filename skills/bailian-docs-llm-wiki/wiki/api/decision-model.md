# decision model

决策模型是百炼平台提供的专用推理服务，基于 System One 协议设计，支持单次前向调用同步返回结构化决策结果（包括分类标签、置信度评分、是非判断及对应概率分布）。该模型适用于风控审核、内容合规判定、策略路由等需明确输出逻辑结论的场景。其接口与行为与通用大模型显著不同，开发者需按专用规范调用。

## 支持的模型/功能

- 当前可用模型标识为 `decision-model-preview`，属于预览阶段模型，能力与稳定性可能随迭代调整，详见 [decision-model-preview 模型信息](../../raw/model-user-guide/get-started-with-models/model-studio-model-list/model-list-decision/decision-model-preview.md)。
- 核心输出包含三项结构化字段：`category`（字符串分类结果）、`score`（0.0–1.0 浮点评分）、`yes_no`（布尔型是非判断），并附带各结果的概率分布与整体置信度。
- 不支持流式响应、多轮对话或文本生成类任务；所有输出均为确定性决策，无自由文本补全。

## 关键参数

- `system_prompt`：必需，用于定义决策规则与输出语义（如“若含违禁词则 category='拒绝'，score<0.3 时 yes_no=false”），格式需严格遵循 System One 协议约束。
- `input`：必需，传入待评估的原始内容（纯文本，最大长度 8192 tokens）。
- `temperature`、`top_p` 等采样参数**无效**，决策模型不启用随机采样。
- 其他参数详见 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 使用方式

1. 通过百炼控制台「模型服务」→「决策模型」开通权限；
2. 调用 `/v1/models/decision-model-preview:predict` 接口（HTTP POST），请求体为 JSON，必须包含 `system_prompt` 和 `input` 字段；
3. 响应体为标准 JSON，含 `category`、`score`、`yes_no` 及 `probabilities` 字段；错误码与重试策略参考 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- 上下文窗口上限为 8192 tokens，超长输入将被截断，不触发自动分块处理；
- 模型不支持图像、音频等多模态输入，仅接受 UTF-8 编码纯文本；
- > **注意**：原始文档中提及“一次前向返回分类、评分与是非判断”，但 [decision-model-preview 模型信息](../../raw/model-user-guide/get-started-with-models/model-studio-model-list/model-list-decision/decision-model-preview.md) 明确说明当前预览版暂不返回 `probabilities` 字段——该字段计划在 GA 版本上线，开发中请以实际响应为准；
- 调用频次受账户级限流约束（默认 5 QPS），超出将返回 `429 Too Many Requests`；
- 模型输出不可微调，不支持 LoRA 或 prompt tuning 等定制方式。

## 来源文档

- [决策模型](../../raw/model-api-reference/decision-model.md)


