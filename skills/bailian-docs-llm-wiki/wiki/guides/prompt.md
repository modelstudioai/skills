# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持模板化、自动化与反馈驱动的多维度优化能力。开发者可通过结构化提示词控制模型行为、提升输出质量与任务适配性。所有 Prompt 相关功能均依托于百炼统一的推理服务框架，与模型选型和部署方式深度协同。

## 支持的模型/功能

当前 Prompt 功能全面支持百炼平台所有公开可调用的大语言模型（如 Qwen 系列、Baichuan 系列等），且与 [Prompt模板概述](../../raw/application-user-guide/prompt.md) 中定义的模板语法完全兼容。除基础文本提示外，还支持 Prompt 自动优化、反馈优化、样例库检索等高级能力，详见 [Prompt自动优化](../../raw/application-user-guide/prompt.md) 和 [Prompt反馈优化](../../raw/application-user-guide/prompt.md)。> **注意**：部分旧版 SDK（v1.2 以下）未实现对 `system` 角色字段的透传，可能导致自定义系统提示失效，建议升级至 v1.3+ 或直接使用 HTTP API。

## 关键参数

- `prompt_template_id`：模板唯一标识，用于复用预置或已保存的 Prompt 模板；  
- `variables`：JSON 对象，传入模板中 `${key}` 占位符对应的实际值；  
- `optimization_mode`：可选 `"auto"`（启用自动优化）、`"feedback"`（启用反馈优化）或 `null`（禁用）；  
- `max_prompt_tokens`：硬性限制 Prompt 总长度（含模板+变量展开后），超限将触发截断并返回警告。

## 使用方式

1. **模板调用**：通过 `/v1/prompt/render` 接口提交 `prompt_template_id` 与 `variables`，获取渲染后的完整 Prompt 字符串；  
2. **直连推理**：将渲染结果作为 `messages` 数组中的 `user`（或 `system`）内容，传入 `/v1/chat/completions`；  
3. **端到端优化**：在请求中指定 `optimization_mode`，平台将在推理前自动重写 Prompt（需模型支持该能力，参见 [Prompt样例库](../../raw/application-user-guide/prompt.md) 中的兼容性说明）。

## 限制和注意事项

- 单次 Prompt 渲染后总 token 数不得超过所选模型上下文窗口的 80%（例如 Qwen2-7B 最大支持 32768 tokens，则 Prompt 部分上限为 ~26200）；  
- 自动优化功能仅对 `text-generation` 类任务生效，不适用于 embedding 或 rerank 模型；  
- 所有 Prompt 模板存储于租户隔离空间，跨项目不可共享，且不支持导出原始模板 JSON 结构。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


