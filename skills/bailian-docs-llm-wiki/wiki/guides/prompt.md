# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持模板化、自动化与反馈驱动的多种优化方式。开发者可通过结构化提示词控制模型行为、提升输出质量与稳定性。所有 Prompt 相关能力均依托于百炼统一的推理服务框架，与模型选型和部署配置深度协同。

## 支持的模型/功能

当前所有接入百炼平台的 LLM（包括 Qwen 系列、Baichuan、GLM 等）均原生支持 Prompt 输入，但**仅部分模型支持 Prompt 自动优化与反馈优化功能**，具体以 [Prompt自动优化](https://help.aliyun.com/zh/model-studio/optimize-prompt) 文档所列支持列表为准。模板功能（如变量占位、上下文注入）在全部模型上可用，详见 [Prompt模板概述](https://help.aliyun.com/zh/model-studio/prompt-template)。> **注意**：[Prompt样例库](https://help.aliyun.com/zh/model-studio/prompt-sample-optimization) 中部分示例基于旧版 Qwen-1.5，对 Qwen2/Qwen3 模型需手动验证 token 截断与角色标记兼容性。

## 关键参数

调用时通过 `prompt_template` 字段传入模板字符串，支持 Jinja2 语法（如 `{{ input }}`、`{% if condition %}...{% endif %}`）；若启用自动优化，需额外设置 `enable_prompt_optimization: true`。参数 `prompt_version` 可指定模板版本（默认 latest），该字段在 [自定义Prompt模板](https://help.aliyun.com/zh/model-studio/prompt-custom-template) 中有明确定义。

## 使用方式

1. 在控制台创建 Prompt 模板，或直接在 API 请求体中内联 `prompt_template`；
2. 若需运行时变量替换，确保请求 payload 包含对应 `variables` 对象（如 `{"input": "xxx", "context": [...]}`）；
3. 启用自动优化需在请求头或参数中显式声明，且模型必须在 [Prompt自动优化](https://help.aliyun.com/zh/model-studio/optimize-prompt) 支持列表内。

## 限制和注意事项

- 单次 Prompt 模板长度上限为 8192 token（含变量展开后），超长将触发截断并返回 warning；
- 自动优化功能仅对同步调用生效，流式响应（stream=true）下不触发优化；
- 所有 Prompt 操作均受项目级配额限制，详情参见 [Prompt反馈优化](https://help.aliyun.com/zh/model-studio/prompt-feedback-optimization) 中的速率控制说明。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


