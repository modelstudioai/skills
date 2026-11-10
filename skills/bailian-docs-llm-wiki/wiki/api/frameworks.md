# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于简化主流 AI 应用开发框架与百炼模型服务的对接。它通过标准化适配器封装模型调用、流式响应、[工具调用](../concepts/tool-calling.md)等逻辑，降低框架层集成复杂度。当前支持 LlamaIndex 和 Spring AI Alibaba 两大生态，后续将按需扩展。

## 支持的模型/功能

- **LlamaIndex**：支持 `LLM` 接口注入、`ChatEngine` [流式输出](../concepts/streaming-output.md)、RAG 管道中的 `NodePostprocessor` 集成；兼容百炼全部文本生成类模型（如 `qwen-max`, `qwen-plus`, `qwen-turbo`）及[函数调用](../concepts/function-calling.md)能力。详见 [框架集成](../../raw/application-api-reference/frameworks.md)。
- **Spring AI Alibaba**：提供 `AlibabaAIClient` 实现，支持 `ChatClient`、`EmbeddingClient` 及 `ToolCalling` 场景，自动透传百炼的 `top_p`、`temperature` 等参数。该实现已通过 Spring AI v1.0.0+ 兼容性验证，参考 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

## 关键参数

所有框架适配器均继承百炼通用参数语义：
- `model`: 必填，指定模型 ID（如 `qwen-max`），不支持别名或通配符；
- `stream`: 布尔值，控制是否启用流式响应（LlamaIndex 默认 `false`，Spring AI Alibaba 默认 `true`）；
- `tools`: 工具定义数组，仅当模型支持[函数调用](../concepts/function-calling.md)时生效（如 `qwen-max`）；  
- `max_tokens`、`temperature`、`top_p` 等参数直接透传至底层 API，行为与 [框架集成](../../raw/application-api-reference/frameworks.md) 中描述一致。

> **注意**：LlamaIndex 文档中提及的 `QwenLLM` 类已废弃，应统一使用 `QwenModel`（见 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md)），旧类在 v0.10.35+ 版本中不再维护。

## 使用方式

1. **安装依赖**：  
   - LlamaIndex：`pip install llama-index-llms-bailian`  
   - Spring AI Alibaba：`implementation 'org.springframework.ai:spring-ai-alibaba-spring-boot-starter:1.0.0'`  
2. **初始化客户端**：  
   ```python
   # LlamaIndex 示例
   from llama_index.llms.bailian import QwenModel
   llm = QwenModel(model="qwen-max", api_key="YOUR_API_KEY")
   ```
   ```java
   // Spring AI 示例（application.yml）
   spring:
     ai:
       alibaba:
         endpoint: https://dashscope.aliyuncs.com/compatible-mode/v1
         api-key: ${BAI_LIAN_API_KEY}
   ```

## 限制和注意事项

- 不支持跨框架混用（例如在 Spring AI 中调用 LlamaIndex 的 `ServiceContext`）；
- [工具调用](../concepts/tool-calling.md)返回的 `tool_calls` 字段结构与 OpenAI 兼容，但 `id` 字段为百炼内部生成，不可用于幂等重试；
- 所有框架适配器均**不缓存**请求/响应，需由上层应用自行实现缓存策略；
- LlamaIndex 的 `AsyncLLM` 接口暂未实现异步流式支持，同步调用是唯一稳定路径（参见 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md)）。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


