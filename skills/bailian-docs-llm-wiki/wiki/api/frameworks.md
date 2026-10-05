# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于简化大模型应用开发中与主流开源框架（如 LlamaIndex、Spring AI）的对接。它通过标准化接口封装底层模型调用、提示工程和工具编排逻辑，使开发者可复用已有框架生态快速构建 RAG、Agent 等应用。该能力需配合 `application-api` 使用，不直接暴露原始模型 API。

## 支持的模型/功能

当前支持以下两类框架集成：

- **LlamaIndex**：提供 `llamaindex` 适配器，支持 `VectorStoreIndex`、`SummaryIndex` 及自定义 `QueryEngine` 的无缝接入，自动将百炼模型（如 `qwen-max`、`qwen-plus`）注入 `LLM` 和 `Embedding` 组件。详细用法见 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **Spring AI Alibaba**：提供 Spring Boot Starter `spring-ai-alibaba-spring-boot-starter`，兼容 Spring AI 标准接口，支持 `ChatClient`、`EmbeddingClient` 及 `AiResponse` 流式解析。具体配置项参见 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

> **注意**：原始文档中未明确说明是否支持 LangChain；[LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 文档提及“暂不提供 LangChain 官方适配器”，但部分社区示例存在非官方封装，建议以该文档为准。

## 关键参数

使用任一框架适配器时，均需在初始化阶段传入以下必选参数：

- `api_key`：百炼平台项目级 API Key（非个人 AccessKey）
- `base_url`：固定为 `https://dashscope.aliyuncs.com/compatible-mode/v1`
- `model`：指定模型 ID（如 `qwen-max`），必须与所选框架支持的模型类型匹配（例如 LlamaIndex 要求模型支持 `chat` 和 `embedding` 双能力）

部分框架额外要求：
- LlamaIndex 需显式设置 `embed_model` 参数指向百炼 embedding 模型（如 `text-embedding-v3`）
- Spring AI Alibaba 中 `spring.ai.alibaba.model` 配置项必须与 `spring.ai.alibaba.chat.options.model` 保持一致，否则请求将失败

## 使用方式

1. **添加依赖**  
   - LlamaIndex：安装 `llamaindex` ≥ 0.10.52，并引入 `llamaindex-llms-dashscope` 包  
   - Spring AI Alibaba：在 `pom.xml` 中添加 `spring-ai-alibaba-spring-boot-starter`（版本 ≥ 0.1.0-M2）

2. **初始化客户端**  
   按照对应框架文档完成配置，例如 LlamaIndex 示例需调用 `DashScopeLLM(...)` 和 `DashScopeEmbedding(...)` 构造器。

3. **发起调用**  
   后续调用完全遵循原框架语法（如 `index.as_query_engine().query("...")`），无需修改业务逻辑。

完整代码示例请参考 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 和 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 文档中的 Quick Start 章节。

## 限制和注意事项

- 单次请求最大 token 数受所选模型自身限制（如 `qwen-max` 上限为 32768），框架层不额外截断
- 不支持跨模型混合调用（例如在同一个 `QueryEngine` 中混用百炼模型与 OpenAI 模型）
- LlamaIndex 的 `retriever` 默认启用 `similarity_top_k=2`，若需调整，必须在创建 `VectorStoreIndex` 前显式传入 `service_context`
- 所有框架适配器均**不支持**百炼私有部署版（即 `dashscope-enterprise` 环境），仅适用于公有云百炼服务

## 来源文档

- [框架](../../raw/application-api-reference/frameworks.md)


