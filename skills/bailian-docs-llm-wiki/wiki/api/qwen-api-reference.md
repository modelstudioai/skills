# qwen api reference

百炼平台提供多种 API 接口用于调用通义千问（Qwen）系列文本生成模型。开发者可根据已有技术栈和业务需求，选择最合适的接口协议进行集成。各接口在兼容性、功能覆盖度和内置工具支持上各有侧重，详见[文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 支持的接口协议

百炼为文本生成模型提供以下四种调用方式：

### OpenAI 兼容 Chat Completions

与 OpenAI 客户端库直接兼容，适合从 OpenAI 生态迁移现有应用或接入第三方工具。迁移成本最低，开发者可复用已有的 OpenAI SDK 代码，仅需更换 API endpoint 和密钥即可完成接入。

### OpenAI 兼容 Responses

在 Chat Completions 基础上进一步扩展，内置联网搜索、代码解释器和网页内容提取等工具能力。该接口可自动管理对话历史，无需开发者手动维护上下文，适合需要工具调用的复杂场景。

### Anthropic 兼容 Messages

兼容 Anthropic Messages API 协议，支持思考（thinking）和工具调用（tool use）功能。适合已在使用 Anthropic SDK 的开发者快速接入百炼平台模型。

### DashScope 原生接口

百炼平台的原生接口，提供最完整的功能集和参数支持。如需使用百炼平台的全部能力（包括平台特有的高级参数和功能），推荐使用 DashScope 接口。

## 接口选择建议

| 场景 | 推荐接口 |
|------|----------|
| 从 OpenAI 迁移现有应用 | OpenAI 兼容 Chat Completions |
| 需要内置工具（搜索、代码执行等） | OpenAI 兼容 Responses |
| 从 Anthropic 生态迁移 | Anthropic 兼容 Messages |
| 需要完整功能集和最大灵活性 | DashScope 原生接口 |

## 关键信息

- 所有接口均通过百炼平台统一鉴权，需使用百炼 API Key。
- 各接口的具体参数说明和请求示例，请参考[文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)中列出的各协议文档链接。
- 选择接口时需权衡兼容性与功能完整度：第三方兼容接口便于迁移，DashScope 原生接口则覆盖最全的平台能力，具体差异可在[文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)中查看各接口说明。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)




