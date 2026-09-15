# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持模板化、可复用的指令构造方式。开发者可通过预置模板、自定义结构或自动优化流程快速构建高质量 prompt。所有 prompt 操作均通过 API 或控制台界面完成，底层与模型推理服务深度集成。

## 支持的模型/功能

当前 prompt 功能全面支持百炼平台全部公开大模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等），并兼容部分第三方模型接入场景。核心能力包括：静态模板调用、动态变量注入、多轮上下文拼接、基于样例的 prompt 优化，以及用户反馈驱动的迭代改进。详细能力矩阵见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)；针对视觉-语言联合任务的特殊处理逻辑，请参考 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 中的 multimodal 示例章节。

## 关键参数

调用 prompt 时需指定以下关键参数（均通过 `prompt` 字段或 `prompt_template_id` 传入）：
- `variables`: JSON 对象，用于填充模板中的 `{{key}}` 占位符；
- `template_id`: 预注册模板唯一标识（如 `qwen-summarize-v2`）；
- `max_tokens` / `temperature`：若未在模板中锁定，可覆盖模型级默认值；
- `enable_optimization`: 布尔值，启用后触发 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 流程（仅限白名单模型）。

> **注意**：`enable_optimization` 在 v3.2+ 版本中已废弃，实际行为由后端策略控制，前端传参无效——请以 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 文档最新说明为准。

## 使用方式

1. **模板调用**：通过 `/v1/prompt/render` 接口提交 `template_id` 与 `variables`，返回渲染后的完整 prompt 字符串；  
2. **直接推理**：将渲染结果作为 `messages[0].content` 提交至 `/v1/chat/completions`；  
3. **端到端执行**：使用 `/v1/prompt/completion`，平台自动完成渲染 + 推理 + 反馈采集（需配置 `feedback_enabled: true`）。  
完整流程示例见 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md) 的“API 集成”小节。

## 限制和注意事项

- 单次 prompt 渲染后总长度（含变量展开）不得超过模型 context 长度的 90%，否则触发截断且不报错；  
- 模板中禁止嵌套 `{{ }}` 表达式（如 `{{ {{user}} }}`），会导致解析失败；  
- 用户反馈数据仅用于 [Prompt反馈优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) 的离线分析，不参与实时推理；  
- 所有模板 ID 必须通过控制台或 `/v1/prompt/templates` 接口预先注册，硬编码 ID 将导致 404。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


