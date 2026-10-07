# frameworks

`frameworks` 是百炼平台提供的模型集成框架支持模块，用于简化主流 AI 开发框架与百炼 API 的对接。它不直接提供模型推理能力，而是通过标准化适配层，使 LlamaIndex、Spring AI Alibaba 等框架可复用百炼的模型服务、工具调用和 RAG 能力。所有框架适配均基于百炼统一的 `model` 和 `tools` 接口契约。

## 支持的模型/功能

当前支持以下两类框架集成：

- **LlamaIndex**：支持 `LLM`, `Embedding`, `Retriever` 三类组件接入百炼模型（如 `qwen-max`, `qwen-turbo`）及向量库服务；支持 `QueryEngine` 级别流式响应与元数据透传。详情见 [框架](../../raw/application-api-reference/frameworks.md)。
- **Spring AI Alibaba**：提供 `ChatClient` 和 `EmbeddingClient` 的 Spring Boot 自动配置，兼容 `spring-ai-core` 1.0.x 接口规范，支持异步调用与重试策略。该实现已在 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 中完整定义。

> **注意**：原始文档中未列出 LangChain 支持，但部分社区示例代码（如 `langchain-community@0.2.0` 的 `BailianLLM`）已实际可用；该能力尚未纳入官方维护范围，稳定性与接口兼容性请以 [框架](../../raw/application-api-reference/frameworks.md) 的最新声明为准。

## 关键参数

所有框架适配均依赖以下核心参数（环境变量或配置项）：

- `BAI_LIAN_API_KEY`：必填，百炼平台 API Key  
- `BAI_LIAN_BASE_URL`：选填，默认为 `https://dashscope.aliyuncs.com/compatible-mode/v1`  
- `BAI_LIAN_MODEL_NAME`：必填，指定百炼模型 ID（如 `qwen-plus`），需与框架内 `model` 参数一致  
- `BAI_LIAN_TIMEOUT_MS`：选填，HTTP 超时毫秒数（默认 60000）

参数优先级：代码中显式传入 > 配置文件 > 环境变量。

## 使用方式

1. **LlamaIndex**：安装 `llama-index-integrations-llms-bailian` 包，初始化时传入 `BaiLianLLM(model="qwen-turbo")`；Embedding 同理使用 `BaiLianEmbedding` 类。参考 [框架](../../raw/application-api-reference/frameworks.md) 中的代码片段。
2. **Spring AI Alibaba**：在 `pom.xml` 中引入 `spring-ai-alibaba-spring-boot-starter`，配置 `spring.ai.alibaba.model=qwen-max` 即可自动注入 `ChatClient` Bean。

## 限制和注意事项

- 框架层不支持百炼私有模型（如 `custom:xxx`）的直接注册，需通过 `BaiLianLLM(model="custom:xxx", base_url="...")` 手动指定 endpoint。
- LlamaIndex 的 `Settings.llm` 全局设置对 `BaiLianLLM` 实例无效，必须显式传入每个 `ServiceContext` 或 `LLM` 构造函数。
- Spring AI Alibaba 当前仅支持同步 `call()` 方法，`stream()` 返回 `NotImplementedError` —— 此限制已在 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 中明确标注。

## 来源文档

- [框架](../../raw/application-api-reference/frameworks.md)


