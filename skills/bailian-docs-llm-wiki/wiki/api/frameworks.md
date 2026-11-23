# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于简化主流 AI 应用开发框架与百炼模型服务的对接。它通过标准化适配器封装模型调用、流式响应、工具调用等逻辑，降低框架层集成复杂度。当前支持 LlamaIndex 和 Spring AI Alibaba 两大生态，后续将按需扩展。

## 支持的模型/功能

- **LlamaIndex**：支持 `LLM` 接口注入、`ChatEngine` [流式输出](../concepts/streaming.md)、RAG 管道中的 `NodePostprocessor` 集成；兼容百炼全部文本生成类模型（如 `qwen-max`, `qwen-plus`, `qwen-turbo`）及[函数调用](../concepts/function-calling.md)能力。详见 [框架集成](../../raw/application-api-reference/frameworks.md)。
- **Spring AI Alibaba**：提供 `AlibabaAIClient` 实现，支持 `ChatClient`、`EmbeddingClient` 及 `ToolCalling` 场景，自动透传百炼的 `top_p`、`temperature` 等参数。该实现已通过 Spring AI v1.0.0+ 兼容性验证，参考 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

## 关键参数

所有框架适配器均继承百炼通用参数语义：
- `model`: 必填，指定模型 ID（如 `qwen-max`），不支持别名或通配符；
- `stream`: 布尔值，控制是否启用流式响应（LlamaIndex 中对应 `streaming=True`，Spring AI 中为 `chatOptions.stream(true)`）；
- `tools`: JSON Schema 数组，仅当模型支持[函数调用](../concepts/function-calling.md)时生效（如 `qwen-max`）；  
> **注意**：`max_tokens` 在 LlamaIndex 适配器中实际映射为 `max_new_tokens`，而 Spring AI Alibaba 当前仍使用 `maxTokens` 字段名——二者行为一致但字段名不统一，详见 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 与 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 文档差异说明。

## 使用方式

1. **安装依赖**：  
   - LlamaIndex：`pip install llama-index-core llama-index-llms-bailian`  
   - Spring AI Alibaba：`implementation 'org.springframework.ai:spring-ai-alibaba-spring-boot-starter:1.0.0'`  
2. **初始化客户端**：  
   ```python
   # LlamaIndex 示例
   from llama_index.llms.bailian import Bailian
   llm = Bailian(model="qwen-max", api_key="YOUR_API_KEY")
   ```
   ```java
   // Spring AI 示例（application.yml）
   spring:
     ai:
       alibaba:
         base-url: https://dashscope.aliyuncs.com/compatible-mode/v1
         api-key: ${BAI_LIAN_API_KEY}
   ```

## 限制和注意事项

- 所有框架适配器**不支持**跨模型会话状态保持（如 `qwen-max` 的对话历史无法复用于 `qwen-turbo` 调用）；
- 工具调用（`tools`）仅在 `qwen-max` 和 `qwen-plus` 上完全可用，`qwen-turbo` 返回 `400 Unsupported tool call` 错误；
- LlamaIndex 的 `BailianEmbedding` 尚未发布，当前 embedding 功能需直接调用百炼 Embedding API；此限制已在 [框架集成](../../raw/application-api-reference/frameworks.md) 中明确标注。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


