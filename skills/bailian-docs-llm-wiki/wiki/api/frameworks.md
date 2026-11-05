# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于简化主流 AI 应用开发框架（如 LlamaIndex、Spring AI）与百炼模型服务的对接。它通过标准化适配层屏蔽底层 API 差异，使开发者可复用原有框架代码快速接入百炼模型。该能力不提供独立 API 接口，而是以 SDK 集成和配置驱动方式生效。

## 支持的模型/功能

当前支持以下两类框架集成：
- **LlamaIndex**：支持 `LLM`、`Embedding`、`Retriever` 等核心组件对接，兼容 `llama-index-core>=0.10.0`；支持同步/[异步调用](../concepts/asynchronous-invocation.md)及流式响应透传。详细用法见 [框架集成](../../raw/application-api-reference/frameworks.md)。
- **Spring AI Alibaba**：提供 `AlibabaAIClient` 实现，兼容 Spring AI 1.0+ 的 `ChatClient` 和 `EmbeddingClient` 抽象；支持自动注入百炼模型配置（如 `qwen-max`、`qwen-plus`）。具体配置项参考 [框架集成](../../raw/application-api-reference/frameworks.md)。

> **注意**：原始文档中未明确说明对 LangChain 的官方支持。尽管部分用户通过自定义 `LLM` 类实现接入，但该路径未被 [框架集成](../../raw/application-api-reference/frameworks.md) 文档覆盖，也不在 SDK 的 `@alibaba/bailian-frameworks` 包中声明，建议优先选用已文档化的框架。

## 关键参数

所有集成均依赖以下基础参数（通过环境变量或框架配置注入）：
- `BAI_LIAN_API_KEY`：必填，百炼平台生成的 API Key；
- `BAI_LIAN_ENDPOINT`：可选，默认为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；
- `BAI_LIAN_MODEL_NAME`：必填，指定模型 ID（如 `qwen-max`），需与所选框架的模型类型匹配（例如 LlamaIndex 要求 `model_name` 字段，Spring AI 要求 `spring.ai.alibaba.model`）。

## 使用方式

1. 安装对应框架的百炼适配包：
   - LlamaIndex：`pip install llama-index-llms-bailian`
   - Spring AI Alibaba：`implementation 'com.alibaba.bailian:spring-ai-alibaba-starter:1.0.0'`
2. 按框架规范配置参数（详见 [框架集成](../../raw/application-api-reference/frameworks.md) 中各子文档）；
3. 在业务代码中直接使用原生框架接口（如 `llm.complete("...")` 或 `chatClient.call(...)`），无需修改逻辑。

## 限制和注意事项

- 不支持跨框架混用（例如在 LlamaIndex 中嵌入 Spring AI 的 `ChatClient` 实例）；
- 流式响应仅在框架原生支持且百炼模型本身支持流式（如 `qwen-max`）时可用；
- 所有请求受百炼平台通用限流策略约束（默认 QPS=5/Key），超出将返回 `429 Too Many Requests`；
- 错误码映射遵循百炼统一规范，但部分框架（如旧版 Spring AI）可能忽略 `x-bailian-error-code` 响应头，建议启用 SDK 的 `debug` 日志确认实际返回。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


