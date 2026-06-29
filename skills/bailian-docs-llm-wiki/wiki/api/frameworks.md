# frameworks

阿里云百炼支持通过主流开源框架集成其大模型应用与云端[知识库](../concepts/knowledge-base.md)能力。当前官方文档覆盖两类框架：基于 Python 的 LlamaIndex，用于构建 RAG 应用；以及基于 Java 的 Spring AI Alibaba，用于集成百炼智能体/工作流应用并检索百炼[知识库](../concepts/knowledge-base.md)。两者均以 [API Key](../concepts/api-key.md) 鉴权，复用百炼的数据管理与模型推理能力。

## 支持的框架与功能

| 框架 | 语言 | 主要能力 |
| --- | --- | --- |
| LlamaIndex | Python 3.9+ | 读取本地文件上传到百炼应用数据、构建云端[知识库](../concepts/knowledge-base.md)、构建检索引擎与 RAG 应用 |
| Spring AI Alibaba | Java（Spring Boot 3.x，JDK 17+） | 调用百炼[智能体应用](../concepts/agent-application.md)/工作流应用（流式与非流式）、检索百炼知识库 |

- LlamaIndex 路线将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持**自定义文档切分方式或自定义嵌入模型。如需本地知识库或灵活切分，应改用本地知识库方案，详见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- Spring AI Alibaba 的应用集成**仅支持**[智能体应用](../concepts/agent-application.md)与工作流应用两类，需提前在百炼控制台创建并获取应用 ID。

## 前提条件

1. 开通阿里云百炼服务并[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
2. 将 [API Key](../concepts/api-key.md) 配置到环境变量，避免硬编码泄露：
   - LlamaIndex：按百炼通用约定配置。
   - Spring AI Alibaba 应用集成：推荐变量名 `DASHSCOPE_API_KEY`，应用 ID 用 `APP_ID`，子[业务空间](../concepts/workspace.md)用 `WORKSPACE_ID`。
   - Spring AI Alibaba 知识库检索：推荐变量名 `AI_DASHSCOPE_API_KEY`，子[业务空间](../concepts/workspace.md)用 `AI_DASHSCOPE_WORKSPACE_ID`。
3. 若应用或知识库创建在子[业务空间](../concepts/workspace.md)，需额外获取业务空间 ID 并配置对应环境变量。

> **注意**：Spring AI Alibaba 两篇文档对 [API Key](../concepts/api-key.md) 环境变量名约定不一致（应用集成用 `DASHSCOPE_API_KEY`，知识库检索用 `AI_DASHSCOPE_API_KEY`）。两者均为约定俗成，可按工程实际统一，关键是 `application.yml` 中 `${...}` 占位符与实际变量名一致。

## LlamaIndex：构建 RAG 应用

### 方案概览

1. 读取本地文件（`.txt`、`.docx`、`.pdf` 等非结构化数据）并上传到云端，构建云端知识库。
2. 基于云端知识库构建检索引擎，接收用户提问、检索相关文本片段，与提问合并后送入大模型生成回答；检索不到相关内容时返回报错信息。

完整流程与示例代码参见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。

### 关键参数

构建检索引擎时需手动调整以下参数：

- `Settings.llm = DashScope(model_name="qwen-max")`：生成回答时调用的大模型，可传 `qwen-max` 等模型名称。
- `similarity_top_k`：相似度最高的检索结果数（示例为 5）。
- `similarity_cutoff`：过滤检索结果的最低相似度阈值（示例为 0.4）。
- `top_n`：重排后返回语义相关度最高的结果数（示例为 1）。

检索引擎默认结果可能不满足需求，可通过 `node_postprocessors` 做后处理：
- `SimilarityPostprocessor(similarity_cutoff=...)`：过滤低于阈值的检索结果。
- `DashScopeRerank(top_n=..., model="gte-rerank")`：对检索结果重排，返回最相关结果。
- `response_mode="tree_summarize"`：响应聚合方式。

### 使用方式

1. 下载示例包 `llamaindex_cloud_rag.zip` 并解压，`docs/` 内为示例业务文件（可替换），`create_cloud_index.py` 用于建库，`rag.py` 用于运行 RAG 应用。
2. `pip install -r requirements.txt` 安装依赖。
3. `python create_cloud_index.py`：将 `docs/` 文件上传到百炼应用数据并创建云端知识库（示例知识库名 `my_first_index`）。
4. `python rag.py`：读取已创建的云端知识库，启动本地交互式 RAG 应用；输入问题回车得到回答，输入 `q` 退出。

> **注意**：本方案使用百炼云端智能文档切分与官方向量模型，不支持自定义切分与嵌入模型；如需灵活控制请改用本地知识库方案。

## Spring AI Alibaba：集成大模型应用

### 环境要求

- Spring Boot 3.x
- JDK 17 或更高版本

### 依赖与配置

在 `pom.xml` 中添加 `spring-ai-alibaba-starter-dashscope`（示例版本 `1.0.0.2`）及 `spring-boot-starter-web` 等依赖。`application.yml` 配置示例：

```yaml
spring:
  ai:
    dashscope:
      agent:
        app-id: ${APP_ID}
      api-key: ${DASHSCOPE_API_KEY}
      # workspace-id: ${WORKSPACE_ID}  # 子业务空间时启用
```

### 调用方式

通过 `DashScopeAgent` 调用百炼大模型应用，支持两种模式：

- **非流式调用**：`agent.call(new Prompt(message, DashScopeAgentOptions.builder().withAppId(appId).build()))`，返回 `ChatResponse`，可从 `output` 元数据中取出 `docReferences`（文档引用）与 `thoughts`（思考过程）。
- **流式调用**：`agent.stream(...)` 返回 `Flux<String>`，构造 `DashScopeAgent` 时可设置 `sessionId`、`incrementalOutput`（增量输出）、`hasThoughts`（返回思考）等选项，接口 `produces="text/event-stream"`。

工程入口为标准 `@SpringBootApplication`，启动后可用 Postman 等工具访问 `/ai/bailian/agent/call` 或 `/ai/bailian/agent/stream` 测试。完整代码与示例工程参见[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。

## Spring AI Alibaba：检索百炼知识库

### 环境要求

- JDK 17 或更高版本
- Spring Boot 3 GA 或更高版本

### 使用方式

1. 从 Spring AI Alibaba examples 仓库下载 `bailian-rag-knowledge` 示例（需整个 examples 目录以保证结构与依赖完整）。
2. 配置 `AI_DASHSCOPE_API_KEY`（及可选的 `AI_DASHSCOPE_WORKSPACE_ID`）。
3. 通过 `DashScopeDocumentRetriever` 检索百炼知识库：

```java
DocumentRetriever retriever = new DashScopeDocumentRetriever(dashscopeApi,
    DashScopeDocumentRetrieverOptions.builder().withIndexName(INDEX_NAME).build());

this.chatClient = builder
    .defaultAdvisors(new DocumentRetrievalAdvisor(retriever, retrievalSystemTemplate))
    .build();
```

- `INDEX_NAME` 为待检索知识库名称，**需提前在百炼控制台创建**。
- 检索到的文本切片与原始问题一并提交给大模型生成回答，默认模型 `qwen-max`，可通过 `DashScopeChatOptions.builder().withModel("qwen-plus").build()` 切换。
- 建议使用系统提示词模板约束模型"仅依据上下文回答，答案不在上下文中则告知无法回答"。

详情参见[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## [计费](../concepts/billing.md)与错误处理

- 百炼应用本身不收费，但通过应用调用模型会产生模型推理（调用）费用。
- 通用错误码参见百炼[错误信息](https://help.aliyun.com/zh/model-studio/error-code)文档。

## 限制与注意事项

- LlamaIndex 云端方案不支持自定义文档切分与嵌入模型；本地需可访问公网，文件上传与生成回答均需等待。
- Spring AI Alibaba 应用集成仅支持[智能体应用](../concepts/agent-application.md)与工作流应用，其他应用类型不在支持范围。
- 知识库检索需提前创建好知识库并获取其名称；检索默认业务空间知识库无需配置 `workspace-id`。
- 子业务空间场景必须配置对应的业务空间 ID 环境变量，否则会鉴权或定位失败。
- API Key 一律通过环境变量注入，切勿硬编码到源码或配置文件中。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)



