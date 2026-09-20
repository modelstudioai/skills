# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持模板化、自动化优化与人工反馈迭代。开发者可通过结构化 Prompt 控制模型行为、提升输出质量与任务一致性。所有 Prompt 相关能力均基于百炼统一的推理服务层实现，与底层模型解耦。

## 支持的模型/功能

当前所有接入百炼平台的模型（包括 Qwen 系列、Baichuan、GLM 及第三方 API 模型）均支持基础 Prompt 输入；高级功能如 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 和 [Prompt反馈优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) 仅对 Qwen-1.5 及以上版本、且启用 `enable_prompt_optimization: true` 的实例生效。模板语法兼容 Jinja2 子集，详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

## 关键参数

- `prompt_template`: 字符串或对象，指定模板内容或引用 ID（如 `"qa-v2"`）  
- `variables`: JSON 对象，传入模板变量（如 `{"question": "如何重置密码？", "context": "..."}`）  
- `enable_prompt_optimization`: 布尔值，启用后触发自动优化流程（默认 `false`）  
- `feedback_score`: 数值型反馈分（0–5），仅在调用 [Prompt反馈优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) 时必需  

> **注意**：`prompt_template` 若为字符串，将跳过模板校验；若为对象（含 `id` 字段），则强制校验模板存在性与权限，该行为与 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md) 文档描述一致，但部分旧版 SDK 默认忽略校验，建议显式配置。

## 使用方式

1. **直接传入**：在 `/v1/chat/completions` 请求体中以 `messages[0].content` 传原始 Prompt 字符串  
2. **模板引用**：通过 `prompt_template` + `variables` 组合调用预注册模板（需提前在控制台或 API 注册）  
3. **优化闭环**：首次请求启用 `enable_prompt_optimization: true` 获取优化建议；后续结合用户反馈调用 [Prompt反馈优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) 接口固化改进  

## 限制和注意事项

- 单次 Prompt 总长度（含变量渲染后）不得超过 32768 token，超限将返回 `400 Bad Request`  
- 模板中禁止使用 `{% include %}` 或外部文件加载语法，仅支持内联变量渲染与简单条件判断  
- 自动优化功能依赖历史调用数据，新应用首次调用可能返回空优化结果；建议先积累 ≥50 次有效请求再启用  
- 所有 Prompt 操作受项目级 Token 配额与速率限制约束，详情参见 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 中的性能基准章节

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


