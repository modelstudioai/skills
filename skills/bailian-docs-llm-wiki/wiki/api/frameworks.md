# frameworks

本文档汇总阿里云百炼平台支持的主流开发框架集成方案，涵盖基于 Python 与 Java 生态的标准化接入路径。开发者可通过 LlamaIndex 快速构建云端检索增强生成（RAG）应用，或利用 Spring AI Alibaba 集成智能体与工作流服务。框架提供开箱即用的工具链与检索引擎封装，有效降低大模型应用开发与集成门槛。

## 支持的模型与功能
- **模型支持**：默认对接 `qwen-max`，支持通过配置参数无缝切换至其他千问系列开源版或商业版[[文本生成模型]]。
- **核心能力**：
  - **云端知识库构建**：支持 `.txt`、`.docx`、`.pdf` 格式文件的自动解析、向量化与索引创建。
  - **检索与重排**：内置相似度阈值过滤、Top-K 向量召回与 Rerank 模型（如 `gte-rerank`）二次排序。
  - **应用类型集成**：完整支持 [[智能体应用]] 与 [[工作流应用]] 的同步/流式调用，标准化返回问答内容、中间推理过程（Thoughts）及关联文档引用。

## 核心框架与使用方式
### LlamaIndex (Python)
适用于快速搭建 Python 侧的云端 RAG 问答系统。核心流程包括本地文件解析、云端知识库创建、检索引擎配置及交互式问答启动。完整实现步骤与代码模板请参考 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **环境要求**：Python 3.9 及以上版本。
- **调用链路**：`DashScopeParse` 解析本地文件 -> `DashScopeCloudIndex.from_documents` 构建云端知识库 -> 配置 `Settings.llm` 与 `node_postprocessors` -> 实例化 Query Engine 启动服务。

### Spring AI Alibaba (Java)
适用于基于 Spring Boot 的企业级 Java 应用开发，提供对百炼应用与知识库的标准化 Client 封装。应用集成与知识库检索的详细指南请分别查阅 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 与 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。
- **环境要求**：JDK 17 及以上版本，Spring Boot 3.x。
- **应用调用**：通过 `DashScopeAgent` 注入 `DashScopeAgentApi`，支持 `agent.call()`（非流式）与 `agent.stream()`（流式 `Flux`）。
- **知识库检索**：通过 `DashScopeDocumentRetriever` 结合 `DocumentRetrievalAdvisor` 注入 `ChatClient.Builder`，框架自动完成上下文拼接与大模型 Prompt 组装。

## 关键参数与配置
开发过程中需重点关注以下核心配置项，建议根据业务场景调优：

| 框架/组件 | 关键参数 | 说明与示例值 |
|---|---|---|
| `LlamaIndex` | `model_name` | 指定生成模型，如 `"qwen-max"`, `"qwen-plus"` |
| | `similarity_top_k` | 初始向量召回数量，推荐值 `5` |
| | `similarity_cutoff` | 相似度过滤阈值，低于此值的片段将被丢弃（如 `0.4`） |
| | `DashScopeRerank` | 语义重排配置，`model="gte-rerank"`，`top_n=1` |
| `Spring AI Alibaba` | `spring.ai.dashscope.api-key` | 平台鉴权密钥（对应 [[API Key 配置]]） |
| | `app-id` / `index-name` | 智能体/工作流应用 ID，或云端知识库名称 |
| | `incrementalOutput` | 流式调用时是否开启增量输出模式，建议 `true` |
| | `hasThoughts` | 是否返回智能体中间推理过程，默认 `true` |
| | `retrievalSystemTemplate` | RAG 系统提示词模板，控制知识库未命中时的兜底回复逻辑 |

## 限制与注意事项
- **云端知识库能力边界**：LlamaIndex 云端集成方案依赖百炼默认的智能文档切分与官方向量模型，当前**不支持**自定义文档切分策略或替换自定义 Embedding 模型。若需在本地实现灵活控制或选择第三方嵌入模型，请切换至本地知识库部署方案。
> **注意：** 官方示例文档中推荐的环境变量命名存在不一致。智能体应用示例使用 `DASHSCOPE_API_KEY`，而知识库检索示例使用 `AI_DASHSCOPE_API_KEY`。请在实际项目中统一变量名，并确保 `application.yml` 或脚本中的 `${...}` 占位符与实际配置严格对应，避免鉴权失败。
- **子业务空间隔离**：若知识库或大模型应用创建于子业务空间，必须显式配置 `workspace-id`（Java 侧对应 `spring.ai.dashscope.workspace-id`），否则请求将默认路由至主账号空间，导致索引找不到或权限报错。
- **网络与计费**：所有框架调用均依赖公网访问百炼云端网关。框架本身免费，实际费用仅由底层大模型推理调用（Token 计费）与云端知识库存储/检索操作产生，详细规则请参考 [[平台计费说明]]。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)

