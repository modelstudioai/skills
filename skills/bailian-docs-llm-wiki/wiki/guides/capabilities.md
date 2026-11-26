# capabilities

`capabilities` 是百炼平台中用于描述模型与系统功能边界的统一抽象层，它定义了各模型支持的调用方式、输入输出约束、扩展能力（如[函数调用](../concepts/function-calling.md)、多模态、流式响应）以及配套基础设施（如 Agent 运行时、微调部署通道）。开发者需依据具体 capability 声明选择适配的模型和参数组合，避免运行时错误。所有 capability 均通过 API 的 `model` 字段隐式绑定，并在 [模型调用](../../raw/cli/capabilities.md) 文档中集中索引。

## 支持的模型与功能

当前平台支持的 capability 类型包括：
- **基础推理**：同步/异步文本生成、流式响应（`stream: true`）、JSON Schema 输出约束；
- **增强能力**：[函数调用](../concepts/function-calling.md)（`tools`）、多模态输入（图像 URL / base64）、长上下文（最高 1M tokens，取决于模型）；
- **Agent 相关**：`agent_loop` 模式、工具执行状态反馈、记忆上下文管理（见 [Agent 基础设施](../../raw/cli/capabilities.md)）；
- **训练与部署**：支持 LoRA 微调、私有模型部署、自定义 tokenizer 配置（详见 [模型训练与部署](../../raw/cli/capabilities.md)）。

> **注意**：部分旧版文档（如 `raw/api/v1/capabilities.md`）仍将 `vision` 能力列为可选布尔字段，但自 v2.3 起已统一为 `input_types: ["text", "image"]` 结构化声明，以兼容多模态扩展，请以 [平台管理与工具](../../raw/cli/capabilities.md) 中的 schema 定义为准。

## 关键参数

调用时需显式或隐式匹配 capability 约束，关键参数包括：
- `model`: 必填，值必须属于某 capability 声明的模型白名单（如 `qwen-vl-plus` 启用 `multimodal` capability）；
- `response_format`: 仅当 capability 声明支持 `json_object` 时可用；
- `tools`: 仅当 capability 包含 `function_calling` 特性时允许非空；
- `max_tokens`: 不得超过该模型在对应 capability 下的硬上限（例如 `qwen-max` 在 `long_context` capability 下上限为 8192）。

## 使用方式

1. 查询模型 capability：调用 `GET /v2/models/{model}` 获取 `capabilities` 数组（如 `["chat", "function_calling", "multimodal"]`）；  
2. 构造请求：确保 `messages`、`tools`、`response_format` 等字段符合所选 capability 的 schema；  
3. 错误处理：若传入不支持的参数（如对无 `function_calling` capability 的模型发送 `tools`），API 返回 `400 Bad Request` 并提示具体缺失 capability。

## 限制和注意事项

- 单次请求的 `input_types` 必须全部被当前 model 的 capability 覆盖（例如含图像则 `multimodal` 必须启用）；  
- `agent_loop` 模式要求模型同时声明 `chat` 和 `function_calling` capability，缺一不可；  
- capability 是模型级静态属性，不随请求参数动态变更；  
- 所有 capability 定义最终以 [模型调用](../../raw/cli/capabilities.md) 中的主索引页为准，子页面（如 `model-invocation.md`）仅作细化说明，不覆盖主索引的约束声明。

## 来源文档

- [能力参考](../../raw/cli/capabilities.md)


