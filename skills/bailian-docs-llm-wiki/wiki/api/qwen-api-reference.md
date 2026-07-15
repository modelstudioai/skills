# qwen api reference

百炼平台为文本生成模型提供了多种调用接口，开发者可根据迁移成本、功能完整度和生态兼容性选择合适的入口。当前共有四类接口：OpenAI 兼容 Chat Completions、OpenAI 兼容 Responses、Anthropic 兼容 Messages 以及百炼原生的 DashScope 接口。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 支持的接口

百炼针对不同的接入场景提供了以下四种接口，功能定位各有侧重：

- **OpenAI 兼容 Chat Completions**：与 OpenAI 客户端库直接兼容，迁移现有应用或接入第三方工具的成本最低。适合已经基于 OpenAI SDK 构建的应用平滑迁移。
- **OpenAI 兼容 Responses**：内置联网搜索、代码解释器和网页内容提取工具，并自动管理对话历史，无需手动维护上下文。
- **Anthropic 兼容 Messages**：兼容 Anthropic Messages API，支持思考（thinking）和工具调用（tool use）。适合基于 Anthropic 生态构建的应用接入。
- **DashScope**：百炼原生接口，提供最完整的功能集和参数支持，是需要使用平台全部能力时的首选。

以上接口的完整清单与说明参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 如何选择

- 追求**最低迁移成本**、已有 OpenAI 应用：选择 OpenAI 兼容 Chat Completions。
- 需要**内置工具（联网搜索/代码解释器/网页提取）与自动对话管理**：选择 OpenAI 兼容 Responses。
- 处于 **Anthropic 生态**、需要思考与工具调用：选择 Anthropic 兼容 Messages。
- 需要**最完整的功能与参数**、使用平台全部能力：选择 DashScope 原生接口。

## 使用方式与注意事项

- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)可直接复用官方 OpenAI 客户端库，仅需替换 base URL 和 API Key，改动量小。
- 若依赖联网搜索、代码解释器等内置工具，需使用 Responses 接口，而非普通的 Chat Completions。
- 不同接口在参数集合和功能覆盖上存在差异：DashScope 参数最全，OpenAI/Anthropic 兼容接口以对应生态的字段约定为准，跨接口迁移时需核对参数映射。

> **注意**：本页仅为文本生成模型各接口的入口索引，具体的请求参数、字段格式与调用示例请查阅对应接口的专属文档；随着平台迭代，接口能力可能变化，请以 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 为准。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)



