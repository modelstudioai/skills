# 函数调用（Function Calling）

函数调用（Function Calling）是大语言模型与外部工具和服务交互的核心机制。通过该能力，模型可以根据用户输入自主判断是否需要调用预定义的函数，并生成符合函数签名的结构化参数，从而实现信息检索、精确计算、业务操作等大模型本身无法直接完成的任务。

## 在百炼平台中的定位

在阿里云百炼平台中，函数调用是连接大模型与外部能力的桥梁。它贯穿了模型推理、应用编排、插件系统等多个层面：

- **模型推理层**：Qwen 系列主力模型（qwen3.7-max、qwen3.7-plus、qwen3.6-flash 等）以及 DeepSeek 系列均原生支持 Function Calling，开发者可在对话请求中声明可用函数，由模型自动决策调用时机。
- **应用编排层**：智能体应用中的插件工具本质上通过 Function Calling 实现——大模型根据用户意图、工具名称和描述自动选择并调用合适的工具。
- **API 接口层**：百炼的多种 API 协议（OpenAI 兼容 Chat Completions、Responses、Anthropic 兼容 Messages、DashScope 原生接口）均支持 Function Calling，开发者可按已有技术栈选择接入方式。

## 工作原理

函数调用遵循以下流程：

1. **声明函数**：开发者在 API 请求的 `tools` 参数中定义可用函数的名称、描述和参数 schema。
2. **模型决策**：模型根据用户输入内容和函数描述，自主判断是否需要调用函数，以及调用哪个函数。
3. **参数生成**：模型按照函数的参数 schema 生成结构化的 JSON 参数。
4. **应用执行**：应用端接收模型返回的函数调用请求，执行实际的函数逻辑并获取结果。
5. **结果整合**：将函数执行结果回传给模型，模型结合工具返回内容与用户原始问题，生成最终回复。

如果模型判断无需调用任何函数，则直接生成文本回复，不触发调用流程。

## 支持的模型

百炼平台中支持 Function Calling 的主要模型包括：

| 模型 | 文本生成 | 视觉理解 | 备注 |
|------|---------|---------|------|
| qwen3.7-max | 支持 | -- | 旗舰模型，1M 上下文 |
| qwen3.7-plus | 支持 | 支持 | 均衡之选，同时支持视觉 Function Calling |
| qwen3.6-flash | 支持 | 支持 | 低成本，效果接近旗舰 |
| qwen3.5-omni-plus | -- | 支持 | 全模态模型 |
| deepseek-v4-pro | 支持 | -- | 第三方模型 |
| deepseek-v4-flash | 支持 | -- | 第三方模型 |

> 各模型对 Function Calling 的兼容性可能随版本更新变化，以百炼控制台实际执行结果为准。

## 支持的 API 接口

| 接口协议 | Function Calling 支持 | 典型场景 |
|---------|----------------------|---------|
| OpenAI 兼容 Chat Completions | 支持 | 从 OpenAI 生态迁移，标准 function call |
| OpenAI 兼容 Responses | 支持（含内置工具） | 需要联网搜索、代码执行等内置工具 |
| Anthropic 兼容 Messages | 支持（tool use） | 从 Anthropic 生态迁移 |
| DashScope 原生接口 | 支持 | 需要完整功能集和平台特有参数 |

所有接口均通过百炼平台统一鉴权，使用百炼 API Key 访问。

## 关键参数与配置

- **`tools`**：定义可用函数列表，每个函数包含 `name`（函数名）、`description`（功能描述）和 `parameters`（参数 JSON Schema）。
- **`tool_choice`**：控制模型的函数调用行为，可选值通常包括 `auto`（模型自主决定）、`none`（禁止调用）或指定特定函数名（强制调用）。
- 每个智能体应用最多支持添加 10 个工具。

## 与插件系统的关系

百炼平台的插件系统是 Function Calling 在应用层的封装。插件下的每个"工具"本质上对应一个可调用的函数：

- **官方插件**（如 Python 代码解释器、夸克搜索、计算器等）预置了函数定义，无需额外配置。
- **自定义插件**允许开发者定义自己的 API 端点作为可调用函数，支持鉴权配置和参数透传。
- 插件还可发布为 MCP 服务，在智能体应用中以更灵活的方式集成。

调用方式包括智能体应用（模型自主规划）、工作流应用（按编排执行）和 Assistant API（通过 `tools` 参数指定）。

## 开发建议

1. **函数描述要精确**：模型依据函数名和描述来决策是否调用，描述越清晰，调用准确率越高。
2. **参数 schema 要完备**：为每个参数提供类型、描述和约束（如枚举值、必填项），帮助模型生成正确参数。
3. **接口选择**：从 OpenAI 生态迁移优先选 Chat Completions；需要内置工具选 Responses API；需要最完整功能集选 DashScope 原生接口。
4. **思考模式配合**：Qwen3 及以上模型支持思考模式（`enable_thinking`），在复杂的多步函数调用场景中可提升推理质量。

## 来源文档

- [model inference](../guides/model-inference.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [plug in](../guides/plug-in.md)
- toolkits and [frameworks](../api/frameworks.md)
- [more](../api/more.md) about models

## 关联主题页

- [model inference](../guides/model-inference.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


