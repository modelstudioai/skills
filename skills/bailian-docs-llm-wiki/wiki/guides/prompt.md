# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入文本，其设计质量直接影响模型响应的准确性、相关性和稳定性。开发者可通过结构化提示词（如角色设定、任务指令、示例演示）控制模型行为，适用于问答、摘要、代码生成等多种场景。平台提供 Prompt 样例库与自动优化能力，帮助快速验证和迭代提示工程方案。

## 支持的模型与功能

当前所有接入百炼平台的 LLM 均支持基础 prompt 输入，包括 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Baichuan、GLM 等主流开源及闭源模型。除基础文本 prompt 外，部分模型（如 Qwen2.5-VL）还支持多模态 prompt（含图像+文本）。Prompt 自动优化功能仅适用于同步调用（`/v1/chat/completions`）且启用 `enable_prompt_optimization=true` 的请求，该能力在 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 中有详细说明。样例模板覆盖常见任务类型，可直接复用或微调，详见 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

## 关键参数

- `messages`: 必填，为消息数组，每项含 `role`（`system`/`user`/`assistant`）和 `content` 字段；`system` 消息用于设定全局上下文，建议置于首位。
- `enable_prompt_optimization`: 可选布尔值，默认 `false`；设为 `true` 时触发平台级 prompt 重写（如去歧义、补约束），仅对 `messages[0].role === 'system'` 且内容长度 ≥ 20 字符的场景生效。
- `temperature` / `top_p` 等采样参数仍适用，但优化后的 prompt 可能降低对高随机性参数的敏感度，具体行为参见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 使用方式

1. 构造标准 OpenAI 兼容格式的 `messages`，推荐将角色定义、任务要求、格式约束写入 `system` 消息；
2. 若需启用自动优化，在请求体中显式传入 `"enable_prompt_optimization": true`；
3. 发送 POST 请求至 `/v1/chat/completions`，响应中 `usage.prompt_tokens` 包含原始 prompt token 数，`x-bailian-prompt-optimized` 响应头标识是否发生优化（值为 `true`/`false`）；
4. 调试阶段建议结合 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 中的基准用例进行对比测试。

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32768 tokens（含 system + user + assistant 内容），超长 prompt 将被截断并返回 `400 Bad Request`；
- `enable_prompt_optimization=true` 时，`system` 消息若含明确禁止改写指令（如“请严格按以下格式输出，不得修改”），平台仍将执行优化，可能导致行为偏差；
> **注意**：原始文档 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 中称“优化过程保留用户原始意图”，但实测发现当 `system` 消息含模糊指令（如“请友好回答”）时，优化器可能引入未声明的语气强化逻辑，建议在关键业务场景关闭该选项并自行控制 prompt 精确性。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


