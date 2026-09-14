# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持模板化、自动化与反馈驱动的多维度优化能力。开发者可通过结构化提示词控制模型行为、提升输出质量与任务一致性。所有 Prompt 相关功能均需通过 API 或控制台调用，且依赖所选模型对指令的理解能力。

## 支持的模型/功能

当前 Prompt 功能全面支持百炼平台全部主流大模型（如 Qwen 系列、Baichuan、GLM 等），但具体表现受模型原生指令遵循能力影响。核心功能包括：Prompt 模板管理、自定义模板构建、样例库检索与复用、自动优化（基于历史调用数据）及反馈驱动的迭代优化。这些能力在 [Prompt模板概述](../../raw/application-user-guide/prompt.md) 中有整体说明；[自定义Prompt模板](../../raw/application-user-guide/prompt.md) 和 [Prompt样例库](../../raw/application-user-guide/prompt.md) 分别对应模板创建与预置资源调用场景。

## 关键参数

调用 Prompt 相关接口时，关键参数包括：
- `template_id`：模板唯一标识（必填，若使用模板）；
- `variables`：JSON 对象，用于填充模板中的占位符（如 `{{input}}`）；
- `optimize_mode`：可选 `"auto"` 或 `"feedback"`，启用对应优化策略；
- `timeout`：建议设为 30s 以上，因优化流程可能触发多轮模型推理。

> **注意**：`optimize_mode=feedback` 要求已提交至少 5 条有效人工反馈，否则降级为无优化调用——该行为与 [Prompt反馈优化](../../raw/application-user-guide/prompt.md) 文档描述一致，但部分旧版 SDK 示例中未校验反馈数量，需以当前 API 响应为准。

## 使用方式

1. **模板方式**：在控制台创建或选用已有模板，调用 `/v1/prompt/render` 渲染后，再发往 `/v1/chat/completions`；
2. **直调方式**：将完整 prompt 字符串作为 `messages[0].content` 提交，此时不触发任何自动优化；
3. **优化调用**：在请求头添加 `X-Bailian-Prompt-Optimize: true` 并指定 `optimize_mode`，系统将介入重写 prompt（仅限模板路径）。

## 限制和注意事项

- 单次渲染后 prompt 总长度（含变量展开）不得超过 8192 token，超长将被截断并返回警告；
- 自动优化功能仅对 `qwen-max`、`qwen-plus` 及 `qwen-turbo` 生效，其他模型调用时忽略 `optimize_mode` 参数；
- 所有 Prompt 优化操作均不改变原始模型输出逻辑，仅调整输入表述——这一点在 [Prompt自动优化](../../raw/application-user-guide/prompt.md) 中明确强调，但部分用户误认为其会修改模型权重，需特别注意。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


