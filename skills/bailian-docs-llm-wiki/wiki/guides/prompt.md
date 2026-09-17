# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持模板化、可复用、可优化的文本指令构造方式。开发者可通过声明式模板语法定义变量、约束和上下文，结合平台提供的自动优化与反馈闭环能力提升效果稳定性。所有 prompt 相关功能均通过 API 或控制台配置生效，无需修改模型权重。

## 支持的模型/功能

当前所有百炼托管的 LLM（包括 Qwen 系列、Baichuan、GLM 等）均原生支持 prompt 输入，但仅部分模型支持 `system` 角色字段（如 Qwen2.5-72B、Qwen3-72B），其余模型会将 system 内容合并至 user 消息前。模板渲染、变量注入、多轮上下文拼接等功能在 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中详细说明；自动优化与人工反馈驱动的迭代能力见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 和 [Prompt反馈优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

- `prompt_template`: 字符串模板，支持 Jinja2 语法（如 `{{ input }}`、`{% if condition %}...{% endif %}`），最大长度 8192 字符  
- `variables`: JSON 对象，键需与模板中变量名严格一致，值将被转义后注入  
- `system_prompt`: 可选字符串，仅对明确标注支持 system 角色的模型生效；不支持时平台静默降级为前置 user 消息  
- `enable_optimization`: 布尔值，默认 `false`；设为 `true` 时触发 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 流程（需已开启对应应用的优化开关）

> **注意**：`system_prompt` 参数在部分旧版 SDK 文档中被错误描述为“全模型通用”，实际行为以 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中的模型兼容性表格为准。

## 使用方式

1. 在控制台「应用配置 → Prompt 设置」中编辑模板并保存，或通过 `/v1/applications/{app_id}/prompt` API 更新  
2. 调用模型 API 时，在请求体中传入 `variables` 对象（如 `{"query": "天气如何", "location": "杭州"}`）  
3. 若启用优化，首次调用将返回带 `optimization_id` 的响应，后续可通过该 ID 查询优化进度  

完整样例与调试技巧参见 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

## 限制和注意事项

- 单次请求中 `prompt_template + 渲染后变量内容` 总长度不得超过 32768 token（按模型 tokenizer 计算）  
- 模板中禁止使用未声明的变量，否则渲染失败并返回 HTTP 400  
- 启用 `enable_optimization` 后，首次响应延迟增加约 200–500ms，且不保证每次调用都触发新优化（平台按流量阈值与效果衰减策略决策）  
- 自定义模板若含敏感逻辑（如条件分支嵌套超 5 层），可能因渲染引擎限制导致截断，建议优先使用 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md) 中验证过的结构模式

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


