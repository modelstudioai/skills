# frameworks

阿里云百炼平台支持通过主流开发框架集成大模型服务和数据管理能力，目前主要支持 **LlamaIndex**（Python）和 **Spring AI Alibaba**（Java）两大框架。开发者可以基于这些框架快速构建 RAG 应用、知识库检索服务以及智能体应用。

## 支持的框架与适用场景

| 框架 | 语言 | 适用场景 | 环境要求 |
|------|------|---------|---------|
| LlamaIndex | Python | 构建云端 RAG 应用（知识库问答、客户支持） | Python 3.9+ |
| Spring AI Alibaba | Java | 知识库检索、智能体应用、工作流应用集成 | JDK 17+，Spring Boot 3.x |

## LlamaIndex 集成

根据 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)，LlamaIndex 方案将知识库部署在云端，提供从本地文件读取到云端知识库构建，再到检索引擎和 RAG 应用搭建的完整流程。

### 核心组件

- **`DashScopeParse`**：解析 `.txt`、`.docx`、`.pdf` 等非结构化文件
- **`DashScopeCloudIndex`**：创建和管理云端知识库
- **`DashScopeRerank`**：对检索结果进行语义重排

### 关键参数

```python
Settings.llm = DashScope(model_name="qwen-max")  # 生成回答使用的模型
similarity_top_k = 5       # 检索返回的最大结果数
similarity_cutoff = 0.4    # 最低相似度阈值
top_n = 1                  # 重排后返回的结果数
```

`model_name` 支持 `qwen-max` 等千问系列模型。

> **注意**：该方案使用默认的智能文档切分与官方向量模型，不支持自定义文档切分方式或自定义嵌入模型。如需灵活控制，可考虑基于本地知识库构建 RAG 应用。

## Spring AI Alibaba 集成

Spring AI Alibaba 支持两种集成方式：知识库检索和大模型应用调用。

### 知识库检索

参见 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)，通过 `DashScopeDocumentRetriever` 检索百炼知识库中的相关文本切片，结合大模型生成回答。

核心配置：

```yaml
spring:
  ai:
    dashscope:
      api-key: ${AI_DASHSCOPE_API_KEY}
      # workspace-id: ${AI_DASHSCOPE_WORKSPACE_ID}  # 子业务空间时需要
```

关键代码：

```java
DocumentRetriever retriever = new DashScopeDocumentRetriever(dashscopeApi,
    DashScopeDocumentRetrieverOptions.builder().withIndexName(INDEX_NAME).build());

this.chatClient = builder
    .defaultAdvisors(new DocumentRetrievalAdvisor(retriever, retrievalSystemTemplate))
    .build();
```

知识库需提前在百炼控制台创建，`INDEX_NAME` 设置为知识库名称。默认使用 `qwen-max` 模型，可通过 `DashScopeChatOptions` 切换其他模型。

### 大模型应用调用

参见 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)，通过 `DashScopeAgent` 调用百炼平台上的智能体应用和工作流应用，支持非流式和流式两种调用方式。

配置示例：

```yaml
spring:
  ai:
    dashscope:
      agent:
        app-id: ${APP_ID}
      api-key: ${DASHSCOPE_API_KEY}
```

流式调用时可配置增量输出和思考过程：

```java
DashScopeAgentOptions.builder()
    .withSessionId("current_session_id")
    .withIncrementalOutput(true)
    .withHasThoughts(true)
    .build();
```

> **注意**：仅支持集成智能体应用和工作流应用，不支持其他类型的百炼应用。

## API Key 配置

所有框架均需配置百炼 API Key，但环境变量命名存在差异：

| 框架/场景 | 推荐环境变量名 |
|-----------|---------------|
| LlamaIndex | 通过 `配置API Key到环境变量` 文档设置 |
| Spring AI Alibaba（知识库检索） | `AI_DASHSCOPE_API_KEY` |
| Spring AI Alibaba（应用调用） | `DASHSCOPE_API_KEY` |

> **注意**：两篇 Spring AI Alibaba 文档中推荐的 API Key 环境变量名不一致（`AI_DASHSCOPE_API_KEY` vs `DASHSCOPE_API_KEY`），[业务空间](../concepts/workspace.md) ID 的环境变量名也不同（`AI_DASHSCOPE_WORKSPACE_ID` vs `WORKSPACE_ID`）。请以各自示例项目的 `application.yml` 中的配置为准。

## 限制与注意事项

- **LlamaIndex**：仅支持非结构化数据文件（`.txt`、`.docx`、`.pdf`），文件上传和模型推理均需公网访问。
- **Spring AI Alibaba**：依赖版本为 `spring-ai-alibaba-starter-dashscope:1.0.0.2`，需确保 Spring Boot 3.x 兼容性。
- **计费**：框架本身不收费，但调用模型会产生推理费用。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)













