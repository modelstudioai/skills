# qwen api reference

百炼平台提供多种 API 接口用于调用通义千问（Qwen）系列文本生成模型，涵盖 OpenAI 兼容、Anthropic 兼容以及百炼原生 DashScope 接口。开发者可根据已有技术栈和功能需求选择最合适的接入方式，实现低成本迁移或深度集成。详细参数与调用方式请参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 支持的接口类型

百炼为文本生成模型提供了四种 API 接口，各有侧重：

### OpenAI 兼容 Chat Completions

与 OpenAI 客户端库直接兼容，适用于从 OpenAI 迁移现有应用或接入第三方工具的场景。该方式迁移成本最低，只需更换 API 端点和密钥即可完成切换。

### OpenAI 兼容 Responses

在 Chat Completions 基础上进一步增强，内置联网搜索、代码解释器和网页内容提取工具，并可自动管理对话历史，无需手动维护上下文。适合需要快速搭建具备工具调用能力的应用场景。

### Anthropic 兼容 Messages

兼容 Anthropic Messages API 规范，支持思考（thinking）和工具调用（tool use）能力。适合已有 Anthropic 技术栈的开发者无缝接入百炼平台。

### DashScope 原生接口

百炼平台原生接口，提供最完整的功能集和参数支持。如需使用百炼独有的高级功能或最新特性，推荐使用此接口。

## 接口选择建议

| 场景 | 推荐接口 |
|------|----------|
| 从 OpenAI 迁移现有应用 | OpenAI 兼容 Chat Completions |
| 需要内置工具（搜索、代码执行） | OpenAI 兼容 Responses |
| 从 Anthropic 迁移或需要 thinking 能力 | Anthropic 兼容 Messages |
| 需要最完整的功能集和参数控制 | DashScope 原生接口 |

## 使用方式

无论选择哪种接口，基本接入流程一致：

1. 在百炼控制台获取 API Key
2. 根据所选接口安装对应的客户端 SDK（OpenAI SDK、Anthropic SDK 或 [DashScope SDK](../concepts/dashscope-sdk.md)）
3. 配置 API 端点指向百炼服务
4. 按接口规范构造请求并调用

各接口的具体参数、请求格式和响应结构详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中对应章节的外部链接。

## 注意事项

- 不同接口支持的功能范围有所差异，DashScope 原生接口功能最全。选型前建议查阅 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 确认目标接口是否支持所需特性。
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)虽然与 OpenAI SDK 直接兼容，但部分 OpenAI 独有参数可能不被支持，需以百炼文档为准。
- 各接口的计费方式和限流策略相同，均基于百炼平台统一的 Token 计量体系。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


