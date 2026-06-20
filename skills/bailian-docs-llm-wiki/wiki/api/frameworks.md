# frameworks

阿里云百炼提供了与主流 AI 开发框架的集成能力，开发者可以使用熟悉的框架快速接入百炼的大模型服务和数据管理能力。目前官方文档覆盖了两个主要框架：面向 Python 生态的 LlamaIndex 和面向 Java/Spring 生态的 Spring AI Alibaba。

## LlamaIndex（Python）

LlamaIndex 集成适用于需要通过 Python 构建 RAG（[检索增强生成](../concepts/rag.md)）应用的场景，如私域知识问答、客户支持等。百炼提供云端数据管理和大模型推理，LlamaIndex 负责 RAG 编排。

### 核心流程

1. **读取本地文件并构建云端知识库**：通过 `SimpleDirectoryReader` 读取本地 `.txt`、`.docx`、`.pdf` 文件，使用 `DashScopeParse` 解析后上传到百炼应用数据，创建 `DashScopeCloudIndex`。
2. **构建检索引擎**：基于云端知识库构建 `query_engine`，支持设置相似度阈值（`similarity_cutoff`）、返回数量（`similarity_top_k`）以及重排模型（`DashScopeRerank`，使用 `gte-rerank`）。
3. **生成回答**：将用户提问与检索结果合并输入大模型（默认 `qwen-max`），采用 `tree_summarize` 模式生成回答。

### 关键依赖

- Python 3.9+
- `llama_index.indices.managed.dashscope`：云端索引管理
- `llama_index.readers.dashscope`：文档解析
- `llama_index.postprocessor.dashscope_rerank`：检索结果重排

> **注意**：此方案使用云端知识库，采用默认的智能文档切分和官方向量模型，不支持自定义切分方式或嵌入模型。如需本地化部署或自定义嵌入模型，需参考其他方案。

详细步骤和完整代码请参考 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。

## Spring AI Alibaba（Java）

Spring AI Alibaba 面向 Java 开发者，提供了与百炼平台的两种主要集成方式：调用大模型应用和检索知识库。

### 环境要求

- JDK 17+
- Spring Boot 3.x
- Maven 依赖：`spring-ai-alibaba-starter-dashscope`（版本 1.0.0.2）

### 集成大模型应用

通过 `DashScopeAgent` 调用百炼平台上创建的智能体应用或工作流应用，支持非流式和流式两种调用模式。

**配置要点**：

- `application.yml` 中配置 `spring.ai.dashscope.agent.app-id`（应用 ID）和 `spring.ai.dashscope.api-key`
- 子业务空间场景需额外配置 `workspace-id`
- 推荐通过环境变量 `DASHSCOPE_API_KEY` 和 `APP_ID` 注入敏感信息

**调用方式**：

- **非流式**：`agent.call(new Prompt(message, options))` 返回 `ChatResponse`，可从中获取文本内容、文档引用和思考过程
- **流式**：`agent.stream(new Prompt(message, options))` 返回 `Flux<ChatResponse>`，需设置 `withIncrementalOutput(true)`

仅支持集成智能体应用和工作流应用两种类型。详细配置和代码请参考 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。

### 检索知识库

通过 `DashScopeDocumentRetriever` 检索百炼云端知识库，结合 `ChatClient` 实现 RAG 问答。

**核心组件**：

- `DashScopeDocumentRetriever`：按知识库名称检索相关文本切片
- `DocumentRetrievalAdvisor`：将检索结果注入提示词模板作为上下文
- `ChatClient`：调用大模型（默认 `qwen-max`）生成回答

**配置差异**：知识库检索场景推荐使用 `AI_DASHSCOPE_API_KEY` 作为环境变量名（与应用集成场景的 `DASHSCOPE_API_KEY` 不同，但两者功能等价）。

详细代码请参考 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 框架选型参考

| 维度 | LlamaIndex | Spring AI Alibaba |
|------|-----------|-------------------|
| 语言 | Python | Java |
| 适用场景 | RAG 应用构建（含知识库创建） | 大模型应用调用 + 知识库检索 |
| 知识库管理 | 支持从本地文件创建云端知识库 | 需提前在百炼控制台创建知识库 |
| 调用模式 | 同步 | 同步 + 流式 |
| 最低运行时 | Python 3.9 | JDK 17 + Spring Boot 3 |

## 通用前提条件

无论选择哪个框架，都需要：

1. 开通阿里云百炼服务并获取 API Key
2. 将 API Key 配置到环境变量，避免硬编码泄露
3. 确保运行环境可访问公网

## 计费说明

框架集成本身不产生额外费用，费用来自通过框架调用模型时的模型推理计费。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


