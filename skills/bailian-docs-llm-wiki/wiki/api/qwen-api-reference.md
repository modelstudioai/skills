# qwen api reference

百炼平台提供多种接口用于调用通义千问（Qwen）系列文本生成模型。开发者可根据自身技术栈和业务需求，选择兼容 OpenAI、Anthropic 的标准接口或百炼原生 [DashScope 接口](../concepts/dashscope-api.md)进行集成。

## 支持的接口类型

根据 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)，百炼目前提供以下四种调用方式：

| 接口类型 | 适用场景 | 核心特点 |
|---------|---------|---------|
| OpenAI 兼容 Chat Completions | 迁移现有 OpenAI 应用、接入第三方工具 | 与 OpenAI 客户端库直接兼容，迁移成本最低 |
| OpenAI 兼容 Responses | 需要内置工具能力的场景 | 内置联网搜索、代码解释器、网页内容提取，自动管理对话历史 |
| Anthropic 兼容 Messages | 使用 Anthropic 生态的开发者 | 兼容 Anthropic Messages API，支持思考和工具调用 |
| DashScope | 需要完整功能集的场景 | 百炼原生接口，提供最完整的功能集和参数支持 |

## 接口选择建议

- **已有 OpenAI 代码的项目**：优先选择 OpenAI 兼容 Chat Completions 接口，改动最小。
- **需要内置工具且不想手动维护对话历史**：选择 OpenAI 兼容 Responses 接口。
- **需要使用百炼平台全部能力**：选择 DashScope 原生接口，如 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中所述，该接口提供最完整的功能集和参数支持。

## 使用方式

各接口的详细参数说明和调用示例，请参考对应的官方文档：

- OpenAI 兼容 Chat Completions：https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions
- OpenAI 兼容 Responses：https://help.aliyun.com/zh/model-studio/openai-compatible-responses/
- Anthropic 兼容 Messages：https://help.aliyun.com/zh/model-studio/anthropic-api-messages
- DashScope 原生接口：https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope

## 注意事项

- 不同接口支持的参数范围可能存在差异，[DashScope 接口](../concepts/dashscope-api.md)覆盖面最广。
- OpenAI 兼容 Responses 接口会自动管理对话历史，无需手动维护上下文，但这也意味着对话状态管理逻辑与其他接口不同。
- 如需了解各接口的完整功能对比和参数细节，建议查阅 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中链接的各子文档。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)



