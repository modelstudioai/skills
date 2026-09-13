# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持模板化、自动化优化与人工反馈迭代。开发者可通过结构化文本明确任务目标、上下文约束和格式要求，从而提升模型响应的准确性与一致性。所有 Prompt 操作均需通过 API 或控制台调用，底层由百炼统一的推理服务调度执行。

## 支持的模型与功能

当前所有接入百炼平台的模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方托管模型）均支持基础 Prompt 输入。高级功能如 Prompt 自动优化、模板版本管理、多轮上下文注入等，仅对 [Prompt自动优化](../../raw/application-user-guide/prompt.md) 和 [Prompt模板概述](../../raw/application-user-guide/prompt.md) 中声明的模型生效（如 qwen-max、qwen-plus）。非标模型或自定义部署实例可能不支持模板变量解析（如 `{{input}}`）与条件块语法。

## 关键参数

- `prompt`：必需字符串，可为纯文本或含 Jinja2 语法的模板（如 `{{system}}\n{{user}}`），最大长度 32768 字符  
- `variables`：可选对象，用于运行时填充模板变量（如 `{"input": "杭州天气如何？"}`）  
- `enable_optimization`：布尔值，默认 `false`；设为 `true` 时触发 [Prompt自动优化](../../raw/application-user-guide/prompt.md) 流程（仅限白名单模型）  
- `template_id`：可选字符串，引用已发布的模板 ID（需提前在控制台创建）

> **注意**：文档中提及的 `prompt_feedback_optimization` 参数在 v3.2+ SDK 中已弃用，实际应使用 `/v3/prompt/feedback` 独立接口提交反馈，详见 [Prompt反馈优化](../../raw/application-user-guide/prompt.md) 的最新说明。

## 使用方式

1. **直接传入**：适用于简单场景，`prompt` 字段填入完整指令（如 `"请用中文总结以下文本：{text}"`）  
2. **模板复用**：调用前通过控制台创建模板并获取 `template_id`，API 请求中指定该 ID 与 `variables`  
3. **自动优化启用**：在请求中设置 `enable_optimization: true`，系统将基于历史效果数据重写 Prompt（需模型支持且账户开通权限）  

所有方式均通过 `POST /v3/services/{service_id}/call` 接口提交，响应中 `optimized_prompt` 字段仅在启用优化且成功时返回。

## 限制和注意事项

- 单次请求中 `prompt` + `variables` 渲染后总长度不得超过模型 context 长度（如 qwen-max 为 32K tokens）  
- Jinja2 模板中禁止使用 `{% include %}`、`{% from %}` 等可能引入外部依赖的语句，否则触发安全拦截  
- 启用 `enable_optimization` 后，首次调用延迟增加 200–500ms，且不保证每次优化结果可复现（依赖在线学习策略）  
- 模板变量名不可与保留字段冲突（如 `system`、`history`、`tools`），否则行为未定义  

如需调试模板渲染结果，建议先调用 `/v3/prompt/render` 接口预览输出，避免因变量缺失导致空渲染。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


