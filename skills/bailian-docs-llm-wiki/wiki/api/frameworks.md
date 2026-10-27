# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于将大模型能力无缝嵌入主流开发框架（如 LlamaIndex、Spring AI 等），降低工程接入门槛。它不提供独立 API，而是通过适配器模式封装百炼的底层模型调用与工具调用逻辑。开发者需结合具体框架文档和百炼模型服务配置使用。

## 支持的模型/功能

当前支持以下两类框架集成：
- **LlamaIndex**：提供 `LlamaIndex` 专用的 `LLM` 和 `Embedding` 接口实现，兼容 `llama-index-core>=0.10.0`，支持同步/异步调用、流式响应及自定义参数透传。详细用法见 [框架集成 (raw/application-api-reference/frameworks.md)](../../raw/application-api-reference/frameworks.md)。
- **Spring AI Alibaba**：为 Spring Boot 应用提供 `ChatClient` 和 `EmbeddingClient` 的自动配置支持，兼容 Spring AI 0.8.x+，支持 `spring.ai.alibaba.*` 配置项。该集成已在 [框架集成 (raw/application-api-reference/frameworks.md)](../../raw/application-api-reference/frameworks.md) 中明确列出。

> **注意**：原始文档中未说明对 LangChain 的官方支持；若在社区示例中见到 LangChain 集成，应以 [框架集成 (raw/application-api-reference/frameworks.md)](../../raw/application-api-reference/frameworks.md) 为准，当前版本不承诺兼容性或维护保障。

## 关键参数

所有框架集成均依赖以下核心参数（通过环境变量或框架配置注入）：
- `QWEN_API_KEY`：百炼平台 API Key（必填）
- `QWEN_BASE_URL`：默认为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（可选，仅当使用私有部署时覆盖）
- `QWEN_MODEL`：指定模型 ID，如 `qwen-max`、`qwen-plus`（必填，部分框架默认值可能过时，请以实际运行时显式设置为准）

## 使用方式

1. 安装对应框架适配包（如 `pip install llama-index-llms-qwen` 或 `spring-ai-alibaba-spring-boot-starter`）  
2. 配置上述关键参数（推荐通过 `.env` 或 `application.yml` 注入）  
3. 在代码中按框架规范初始化客户端（例如 LlamaIndex 中使用 `QwenLLM(model="qwen-max")`）  
4. 调用框架原生接口（如 `index.query()` 或 `chatClient.call()`），底层自动路由至百炼服务  

## 限制和注意事项

- 单次请求最大 token 数受所选模型限制（如 `qwen-max` 上限为 32768），超出将触发 `400 Bad Request`  
- 流式响应需框架本身支持（如 LlamaIndex v0.10.3+、Spring AI 0.8.2+），旧版本可能静默降级为非流式  
- 不支持跨模型会话状态管理（如 `qwen-max` 与 `qwen-turbo` 的 `chat_history` 不互通）  
- 所有集成均**不支持**自定义 HTTP 客户端拦截器（如添加全局重试逻辑），如需高级控制，请直接调用百炼 REST API

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


