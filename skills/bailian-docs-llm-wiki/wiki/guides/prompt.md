# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持模板化、可复用、可优化的文本指令构造。开发者可通过结构化方式定义角色、任务、约束和示例，显著提升模型响应的准确性与一致性。所有 prompt 操作均通过 API 或控制台 Prompt 编辑器完成，底层与模型推理服务深度集成。

## 支持的模型/功能

当前 prompt 功能完整支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Baichuan2、GLM4 等百炼托管模型；部分第三方模型（如 Llama3-70B）仅支持基础 prompt 输入，不支持变量插值与自动优化。模板能力（含变量占位符 `{{variable}}` 和条件块 `{% if %}`）需配合 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中定义的语法规范使用。自动优化与反馈优化功能仅对启用「Prompt 实验室」的项目开放，详见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 关键参数

调用 `/v1/chat/completions` 时，prompt 相关行为由以下参数控制：
- `prompt_template_id`: 指定已发布的模板 ID（必填，若使用模板）；
- `variables`: JSON 对象，用于填充模板中的变量（如 `{"query": "天气如何", "lang": "zh"}`）；
- `enable_optimization`: 布尔值，启用后触发基于历史反馈的 prompt 微调（仅当项目开通优化权限且存在有效反馈数据时生效），参考 [Prompt反馈优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)；
- `max_prompt_tokens`: 显式限制 prompt 总长度（含模板渲染后内容），超限将截断并返回警告。

> **注意**：`enable_optimization` 在 v3.2.0+ 版本中已替代旧版 `optimize_level` 参数；若原始文档中仍出现后者，以 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 的最新说明为准。

## 使用方式

1. **模板创建**：在控制台「Prompt 实验室」中新建模板，支持 Markdown 格式编写，并引用预置变量或自定义字段；  
2. **API 调用**：POST 请求体中传入 `prompt_template_id` 与 `variables`，平台自动渲染并注入系统提示词；  
3. **调试验证**：使用「预览渲染结果」功能查看实际发送至模型的 prompt 文本，避免变量未解析或语法错误；  
4. **迭代优化**：部署后收集用户点击“不满意”反馈，系统自动触发 A/B 测试与 prompt 微调，流程见 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

## 限制和注意事项

- 单个 prompt 模板最大长度为 8192 字符（渲染前），渲染后总 token 数不得超过所选模型的 context 长度上限；  
- 变量插值不支持嵌套表达式（如 `{{items[0].name}}` 不合法），仅支持一级键访问（`{{item_name}}`）；  
- 自定义模板若引用了已下线的内置函数（如 `now_utc()`），将导致渲染失败，需同步更新至 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md) 所列的当前可用函数列表；  
- 启用 `enable_optimization` 后，首次优化需至少 50 条有效反馈，且优化版本默认仅对新请求生效，旧会话不受影响。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


