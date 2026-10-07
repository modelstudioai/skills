# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持模板化、可复用的指令构造方式。开发者可通过结构化 Prompt 控制模型行为、格式、角色设定及任务边界。所有 Prompt 功能均通过 API 或控制台配置生效，适用于推理调用与工作流编排。

## 支持的模型/功能

当前所有百炼托管模型（包括 Qwen 系列、Baichuan、GLM 等）均支持标准 Prompt 输入；部分模型（如 Qwen2.5-72B-Instruct）额外支持系统提示词（`system` role）和多轮对话上下文注入。Prompt 模板功能已在 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中定义，支持变量插值、条件分支与 JSON Schema 校验；自动优化能力依赖 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)，需启用 `enable_optimization: true` 参数并提供至少 3 条人工标注样本。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `prompt` | string | 是 | 原始 Prompt 字符串，若使用模板则传入已渲染后的完整文本 |
| `template_id` | string | 否 | 模板唯一标识，对应 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md) 中注册的 ID |
| `variables` | object | 否 | 模板变量映射（如 `{ "topic": "AI安全", "length": 200 }`），仅当 `template_id` 存在时生效 |
| `enable_optimization` | boolean | 否 | 默认 `false`；设为 `true` 时触发基于反馈的 Prompt 微调，详见 [Prompt反馈优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) |

> **注意**：`system` 字段在 v3.2+ API 中已统一归入 `messages` 数组首项（role=system），旧版 `system_prompt` 参数已被废弃——请以 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中的最新消息格式为准。

## 使用方式

1. **直接传入**：将完整 Prompt 字符串赋值给 `prompt` 字段，适用于简单场景；  
2. **模板调用**：指定 `template_id` + `variables`，平台自动渲染后提交；  
3. **样例驱动优化**：上传高质量输入-输出对至 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，再通过 `enable_optimization=true` 触发在线优化。

## 限制和注意事项

- 单次请求 Prompt 文本长度上限为 8192 token（含变量展开后）；  
- 模板变量名仅支持 ASCII 字母、数字和下划线，且不能以数字开头；  
- 自动优化功能仅对已部署的在线服务生效，离线批量调用不触发；  
- 所有 Prompt 内容经平台清洗后才送入模型，禁止包含 `<script>`、`{{exec}}` 等执行类语法——该规则在 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中明确约束。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


