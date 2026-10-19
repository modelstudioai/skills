# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于将大模型能力快速嵌入主流开发框架（如 LlamaIndex、Spring AI 等），降低工程接入门槛。该能力通过标准化适配器封装模型调用、流式响应、工具调用等逻辑，使开发者无需重复实现底层协议对接。所有集成均基于百炼统一的 `v1/chat/completions` 接口语义。

## 支持的模型/功能

当前支持以下框架的开箱即用集成：
- **LlamaIndex**：提供 `LlamaIndexLLM` 类，兼容 `llama-index-core>=0.10.35`，支持同步/异步调用、自定义 system prompt、tool calling（需模型启用 `tools` 能力）及 streaming；详细用法见 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **Spring AI Alibaba**：提供 `AlibabaAISpringAiChatClient`，适配 Spring AI 1.0+ 的 `ChatClient` SPI，支持自动注入百炼 endpoint、API Key 及 model id；配置说明详见 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

> **注意**：原始文档中未明确列出支持的百炼模型列表，但根据 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 中示例所用 `qwen-max` 和 `qwen-plus`，可确认至少支持 Qwen 系列全量模型；其他模型（如 `qwen2-72b`）需自行验证 tool calling 兼容性。

## 关键参数

所有框架集成均继承百炼基础参数，关键可配置项包括：
- `model`: 必填，模型 ID（如 `qwen-max`, `qwen-plus`）
- `api_key`: 百炼平台 API Key（优先从环境变量 `QWEN_API_KEY` 读取）
- `base_url`: 可选，自定义 endpoint（默认为 `https://dashscope.aliyuncs.com/compatible-mode/v1`）
- `stream`: 布尔值，控制是否启用流式响应（部分框架如 Spring AI 需显式启用 `StreamingChatClient`）

## 使用方式

1. 安装对应框架的百炼适配器包（如 `pip install llama-index-llms-bailian` 或 `spring-ai-alibaba-starter`）  
2. 初始化客户端时传入百炼认证与模型信息（参见 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 中的 Python 示例）  
3. 在框架原生 API 中直接使用（例如 LlamaIndex 的 `llm.complete()` 或 Spring AI 的 `chatClient.call()`）

## 限制和注意事项

- 不支持跨框架混用（如在 LlamaIndex 中调用 Spring AI 的 `Message` 类型）  
- 工具调用（function calling）仅在模型本身支持且请求中传入 `tools` 字段时生效；[Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 文档未说明 tools 透传机制，实际使用需验证  
- 流式响应的 chunk 解析逻辑由各框架适配器实现，若遇到解析异常，请优先检查 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 中标注的 `StreamingResponse` 版本兼容性要求

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


