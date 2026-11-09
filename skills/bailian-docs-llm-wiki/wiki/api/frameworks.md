# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于简化主流 AI 应用开发框架与百炼模型服务的对接。它通过标准化适配器封装模型调用、流式响应、工具调用等逻辑，降低框架层集成复杂度。当前支持 LlamaIndex 和 Spring AI Alibaba 两大生态，后续将按需扩展。

## 支持的模型/功能

- **LlamaIndex**：支持 `LLM` 接口注入、`ChatEngine` [流式输出](../concepts/streaming-output.md)、RAG 管道中的 `NodePostprocessor` 集成；兼容百炼全部文本生成类模型（如 `qwen-max`, `qwen-plus`），但不支持多模态模型输入 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **Spring AI Alibaba**：提供 `AlibabaAIClient` 实现，支持 `ChatClient`、`EmbeddingClient` 及 `Tool` 自动发现机制；仅限 Spring Boot 3.2+ 与 Spring AI 1.0.0-M5 及以上版本 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。  
- 所有框架均支持同步/异步调用、自定义 `system_prompt` 注入及请求级 `top_p`、`temperature` 覆盖，但**不支持跨框架共享会话状态**。

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `model` | string | `qwen-plus` | 必填，指定百炼模型 ID；需与框架所选模型能力匹配（如 LlamaIndex 不支持 `qwen-vl`） |
| `api_key` | string | — | 可选，若未配置全局凭证，则需显式传入；优先级高于环境变量 `BAILIAN_API_KEY` |
| `base_url` | string | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 仅当使用私有部署实例时需覆盖；注意该地址与 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 文档中示例一致 |

> **注意**：`base_url` 在 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 文档中误标为 `https://dashscope.aliyuncs.com/api/v1`（已过时），实际应以本页为准，否则将返回 404。

## 使用方式

1. **安装依赖**：  
   - LlamaIndex：`pip install llama-index-llms-bailian`  
   - Spring AI Alibaba：`implementation 'com.alibaba.cloud:spring-ai-alibaba-spring-boot-starter:1.0.0-M5'`  

2. **初始化客户端**（以 LlamaIndex 为例）：  
   ```python
   from llama_index.llms.bailian import Bailian
   llm = Bailian(model="qwen-max", api_key="sk-xxx")
   ```

3. **注入框架组件**：  
   - LlamaIndex：直接传入 `llm` 至 `Settings.llm` 或 `ChatEngine.from_defaults()`  
   - Spring AI Alibaba：通过 `@Bean` 声明 `ChatClient`，自动绑定 `AlibabaAIClient`

## 限制和注意事项

- 单次请求最大 token 数受底层模型限制（如 `qwen-max` 为 32768），框架层不额外截断；超长输入需由应用自行分块。  
- 工具调用（Function Calling）仅在 `qwen-max` 和 `qwen-plus` 上可用，且 LlamaIndex 的 `ToolSelection` 需手动启用 `enable_tool_choice=True` [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- 所有框架均**不支持**百炼的 `audio` 或 `image` 输入类型，尝试传入非文本内容将触发 `ValidationError`。  
- 异步调用在 Spring AI Alibaba 中需显式使用 `Mono<ChatResponse>`，而 LlamaIndex 当前仅支持同步 `stream_chat()`；此差异已在 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 文档中明确标注。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


