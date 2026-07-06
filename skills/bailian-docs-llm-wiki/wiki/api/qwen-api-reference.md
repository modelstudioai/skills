# qwen api reference

百炼平台为文本生成模型（Qwen 系列）提供多种调用接口，开发者可根据兼容性需求选择 OpenAI 兼容、Anthropic 兼容或百炼原生 DashScope 接口。每种接口在功能完整度、迁移成本和工具能力上各有侧重，详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 支持的接口

| 接口 | 兼容协议 | 主要特点 |
| --- | --- | --- |
| OpenAI 兼容 Chat Completions | OpenAI Chat Completions | 与 OpenAI 客户端库直接兼容，迁移成本最低，适合接入第三方工具 |
| OpenAI 兼容 Responses | OpenAI Responses | 内置联网搜索、代码解释器、网页内容提取，自动管理对话历史 |
| Anthropic 兼容 Messages | Anthropic Messages | 兼容 Anthropic Messages API，支持思考（thinking）与工具调用 |
| DashScope | 百炼原生 | 功能集最完整，参数支持最丰富 |

## 关键参数与使用方式

- **模型选择**：各接口均通过请求体中的 `model` 字段指定 Qwen 系列具体模型名。
- **兼容性映射**：OpenAI / Anthropic 兼容接口在协议层做了一一映射，请求/响应字段与对应官方客户端保持一致，可直接复用现有 SDK 与示例代码。
- **对话历史**：OpenAI 兼容 Responses 接口由平台自动管理对话历史，无需在请求中手动拼接 `messages`；其余接口需由调用方维护上下文。
- **工具能力**：仅 OpenAI 兼容 Responses 接口内置联网搜索、代码解释器和网页内容提取三类工具，开箱即用；其他接口如需工具调用，需按各自协议自行定义工具。

更多接口级参数与字段说明请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 限制和注意事项

- **功能完整度**：兼容接口为保证协议一致性，可能不暴露百炼原生的全部参数；如需使用最全的采样参数、插件或业务字段，建议改用 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中介绍的 DashScope 原生接口。
- **工具能力差异**：联网搜索、代码解释器、网页内容提取为 Responses 接口专属内置能力，OpenAI Chat Completions 与 Anthropic Messages 接口不内置这些工具，需自行实现或通过工具调用协议接入。
- **对话历史管理**：仅 Responses 接口自动维护历史，迁移到其他接口时需自行管理上下文长度与轮次，避免超出模型[上下文窗口](../concepts/context-window.md)。
- **迁移评估**：从 OpenAI / Anthropic 迁移时，应先确认目标 Qwen 模型在对应兼容接口下是否支持所需参数（如 `temperature`、`tools`、`stream` 等），再决定接口选型。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)











