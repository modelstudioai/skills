# frameworks

百炼平台支持通过第三方开发框架集成其大模型服务和知识库能力，目前主要覆盖 LlamaIndex（Python）和 Spring AI Alibaba（Java）两个生态。开发者可以利用这些框架快速构建 RAG 应用、检索知识库或调用百炼大模型应用，而无需直接对接底层 API。以下按框架分别介绍其集成方式、适用场景和关键参数。

## LlamaIndex 集成

LlamaIndex 提供了基于 Python 的 RAG 应用构建框架，百炼通过 `DashScopeCloudIndex` 等组件与之对接，详细用法参见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。

### 适用场景

- 私域知识问答、客户支持等需要[检索增强生成](../concepts/rag.md)的场景
- 已熟悉 LlamaIndex API 的 Python 开发者

### 前提条件

- Python 3.9 及以上
- 已开通百炼服务并获取 API Key，配置到环境变量

### 核心流程

1. **构建云端知识库**：使用 `SimpleDirectoryReader` 读取本地 `.txt`、`.docx`、`.pdf` 文件，通过 `DashScopeParse` 解析后上传至百炼应用数据，调用 `DashScopeCloudIndex.from_documents()` 创建知识库。
2. **构建检索引擎**：通过 `index.as_query_engine()` 创建检索引擎，支持配置相似度阈值（`similarity_cutoff`）、Top-K 数量（`similarity_top_k`）和重排模型（`DashScopeRerank`，默认 `gte-rerank`）。
3. **交互问答**：引擎接收用户提问，从云端知识库检索相关片段，合并后送入大模型（默认 `qwen-max`）生成回答。

### 关键参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `model_name` | 生成回答使用的大模型 | `qwen-max` |
| `similarity_top_k` | 检索返回的最高相似度结果数 | 5 |
| `similarity_cutoff` | 最低相似度过滤阈值 | 0.4 |
| `top_n`（Rerank） | 重排后返回的结果数 | 1 |

### 限制

- 云端知识库方案使用默认的智能文档切分和官方向量模型，不支持自定义切分方式或自定义嵌入模型
- 仅支持非结构化数据文件（`.txt`、`.docx`、`.pdf` 等）

## Spring AI Alibaba 集成

Spring AI Alibaba 面向 Java 生态，提供了检索百炼知识库和调用百炼大模型应用两种集成方式。

### 环境要求

- JDK 17 或更高版本
- Spring Boot 3.x

### 检索百炼知识库

通过 `DashScopeDocumentRetriever` 检索百炼云端知识库中的文本切片，结合 `ChatClient` 生成回答。具体步骤参见[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

核心配置：

```yaml
spring:
  ai:
    dashscope:
      api-key: ${AI_DASHSCOPE_API_KEY}
      # workspace-id: ${AI_DASHSCOPE_WORKSPACE_ID}  # 子业务空间时需要
```

关键组件：

- `DashScopeDocumentRetriever`：根据知识库名称检索相关文本切片
- `DocumentRetrievalAdvisor`：将检索结果作为上下文注入提示词
- `ChatClient`：调用大模型生成回答，默认使用 `qwen-max`

### 集成百炼大模型应用

通过 `DashScopeAgent` 调用百炼平台创建的智能体应用或工作流应用，支持非流式和流式两种调用方式。详细步骤参见[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。

核心配置：

```yaml
spring:
  ai:
    dashscope:
      agent:
        app-id: ${APP_ID}
      api-key: ${DASHSCOPE_API_KEY}
```

关键组件：

- `DashScopeAgent`：封装百炼应用调用，支持 `call()`（非流式）和 `stream()`（流式）
- `DashScopeAgentOptions`：配置应用 ID、会话 ID、增量输出等参数

Maven 依赖：

```xml
<dependency>
    <groupId>com.alibaba.cloud.ai</groupId>
    <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
    <version>1.0.0.2</version>
</dependency>
```

> **注意**：集成百炼大模型应用仅支持智能体应用和工作流应用两种类型，不支持其他应用类型。

## 框架对比

| 维度 | LlamaIndex | Spring AI Alibaba |
|------|-----------|-------------------|
| 语言 | Python | Java |
| 最低运行时 | Python 3.9 | JDK 17 + Spring Boot 3.x |
| 知识库集成 | 支持（云端构建 + 检索） | 支持（检索已有知识库） |
| 应用调用 | 不涉及 | 支持（智能体/工作流应用） |
| [流式输出](../concepts/streaming.md) | 未提及 | 支持 |

## 计费说明

框架本身不收取费用。通过框架调用百炼模型时会产生模型推理费用，知识库检索也可能产生相关费用。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)




