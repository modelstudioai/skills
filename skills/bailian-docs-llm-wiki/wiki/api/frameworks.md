# frameworks

`frameworks` 是百炼平台提供的标准化集成层，用于将大模型能力无缝嵌入主流 AI 开发框架中，降低工程接入成本。当前支持 LlamaIndex 和 Spring AI Alibaba 两大框架，通过统一的适配器封装模型调用、流式响应、工具调用等能力。所有集成均基于百炼 v3.2+ API 规范实现，需配合对应 SDK 版本使用。

## 支持的模型与功能

- **LlamaIndex**：支持 `llm`, `embed_model`, `retriever` 等核心组件注入，兼容 `SimpleDirectoryReader`、`VectorStoreIndex` 等常用模块；完整支持 RAG 流程中的异步查询、元数据过滤与自定义 prompt 模板。详见 [框架集成 (raw/application-api-reference/frameworks.md)](../../raw/application-api-reference/frameworks.md)。
- **Spring AI Alibaba**：提供 `AlibabaAIClient` 实现 `ChatClient` 和 `EmbeddingClient` 接口，支持 `StreamingChatClient`、`RetryTemplate` 集成及 Spring Boot 自动配置；已验证兼容 Spring AI 0.8.1+ 和 Spring Boot 3.2+。该实现细节见 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 百炼模型 ID（如 `qwen-max`, `qwen-plus`），必须为当前框架支持的模型列表内项 |
| `api_key` | string | 否 | 若未通过环境变量 `QWEN_API_KEY` 设置，则需显式传入；优先级高于环境变量 |
| `base_url` | string | 否 | 默认为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；若使用私有部署实例，需覆盖此值 |
| `stream` | boolean | 否 | 仅 LlamaIndex 的 `LLM` 组件生效；设为 `true` 时启用逐 token [流式输出](../concepts/streaming-output.md)（[LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md)） |

> **注意**：Spring AI Alibaba 的 `temperature` 参数默认值为 `0.8`，而 LlamaIndex 适配器中同名参数默认为 `0.1`，二者行为不一致，建议在业务代码中显式指定以避免非预期采样差异。

## 使用方式

1. 安装对应框架 SDK 及百炼适配器：
   ```bash
   # LlamaIndex 场景
   pip install llama-index-core llama-index-llms-qwen
   # Spring AI Alibaba 场景
   ./gradlew dependencies --include spring-ai-alibaba-spring-boot-starter
   ```
2. 初始化客户端并注入框架：
   - LlamaIndex：`QwenLLM(model="qwen-max", api_key="...")`
   - Spring AI Alibaba：在 `application.yml` 中配置 `spring.ai.alibaba.base-url` 和 `spring.ai.alibaba.api-key`
3. 调用框架原生接口（如 `index.as_query_engine().query("...")` 或 `chatClient.call(...)`）

## 限制和注意事项

- 单次请求最大上下文长度受所选模型限制（如 `qwen-max` 为 32768 tokens），超出将触发 `400 Bad Request`；框架层不自动截断或分块。
- LlamaIndex 的 `ToolRetriever` 尚未支持百炼[函数调用](../concepts/function-calling.md)（Function Calling）协议，仅支持传统 `QueryEngine` 流程；相关能力计划在 Q3 发布，当前请参考 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 的已知限制章节。
- 所有框架集成均**不支持**跨 Region 调用（例如华东1 区应用调用华北2 区部署的百炼实例），`base_url` 必须与实际部署区域严格匹配。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


