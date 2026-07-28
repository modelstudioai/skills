# 框架与工具包对比

百炼平台为开发者提供了两条主要的框架集成路径：一是通过官方适配的开源框架（LlamaIndex、Spring AI Alibaba）直接调用百炼云端能力，二是通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)将已有应用迁移至百炼并接入 LangChain 等主流框架。两者在定位、语言生态、功能范围和迁移成本上存在显著差异。本页面帮助开发者根据技术栈和业务需求选择合适的集成方案。

## 关键维度对比

| 维度 | LlamaIndex + Spring AI Alibaba（官方框架适配） | [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) + LangChain（兼容迁移路线） |
| --- | --- | --- |
| 定位 | 深度集成百炼云端知识库、智能体与工作流 | 以 OpenAI 兼容协议接入百炼模型推理能力 |
| 支持语言 | Python（LlamaIndex）、Java（Spring AI Alibaba） | 多语言（Python/Node.js/Go 等任意支持 OpenAI SDK 的语言） |
| 核心能力 | 云端知识库构建、RAG 应用、智能体/工作流调用、知识库检索 | Chat Completions、Responses、Completions、Embedding、Vision、文件、Batch、Conversations |
| 知识库支持 | 原生支持云端知识库（智能切分 + 官方向量模型） | 通过 Embedding 接口 + 文件接口可自建知识库管线 |
| 自定义切分/嵌入 | LlamaIndex 云端方案不支持；需改用本地知识库方案 | 完全可控，可自定义切分策略与嵌入模型 |
| 模型范围 | LlamaIndex：qwen-max 等对话模型；Spring AI Alibaba：智能体/工作流应用 | Qwen 全系列（含 VL/Coder/Omni/Math）、DeepSeek、Kimi、GLM、MiniMax 等三方模型 |
| [流式输出](../concepts/streaming.md) | Spring AI Alibaba 支持流式（`Flux<String>`，`text/event-stream`） | Chat Completions 支持 `stream=True`；Responses 支持流式 |
| 迁移成本 | 需学习百炼专用 SDK 与配置方式 | 已有 OpenAI 应用仅需替换 `api_key`、`base_url`、`model` 三项 |
| 鉴权方式 | [API Key](../concepts/api-key.md)（环境变量 `DASHSCOPE_API_KEY` 等） | [API Key](../concepts/api-key.md)（环境变量 `DASHSCOPE_API_KEY`） |
| 地域支持 | LlamaIndex 按百炼通用约定；Spring AI Alibaba 需配置[业务空间](../concepts/workspace.md) ID | 北京、新加坡、东京、法兰克福、弗吉尼亚等多地域，各地域 [API Key](../concepts/api-key.md) 不同 |
| 典型场景 | 企业级 RAG 应用、Java/Spring 生态集成百炼智能体 | OpenAI 应用迁移、多模型统一调用、代码补全、批量推理、视觉理解 |

## 各方案适用场景建议

### LlamaIndex（Python）

适合使用 Python 技术栈、希望快速搭建 RAG 应用的开发者。核心优势是将本地文件上传至百炼云端自动构建知识库，无需自行管理切分与向量模型。但云端方案不支持自定义切分和嵌入模型，对切分粒度有精细控制需求时应改用本地知识库方案。

### Spring AI Alibaba（Java）

适合 Java/Spring Boot 生态的企业应用，需要直接调用百炼控制台中已创建的智能体应用或工作流应用。支持流式与非流式调用，可获取文档引用与思考过程元数据。也支持检索百炼知识库。前提是 JDK 17+ 与 Spring Boot 3.x，并需提前在控制台创建应用获取 App ID。

### [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) + LangChain

适合已有 OpenAI 应用希望低成本迁移到百炼的场景，或需要使用多语言 SDK 的项目。通过替换三项配置即可完成迁移，同时支持 LangChain/LangChain4j 等主流框架。该路线覆盖能力最广（对话、补全、嵌入、视觉、文件、批量），但不提供百炼云端知识库的托管能力，知识库需自行构建。

## 选型建议

- **已有 OpenAI 应用或使用 LangChain 生态**：优先选择 OpenAI 兼容接口路线，迁移成本最低，模型覆盖最广。
- **Python 新项目、需要云端托管知识库**：选择 LlamaIndex，快速构建 RAG 应用，无需运维基础设施。
- **Java/Spring 企业应用、需要调用百炼智能体或工作流**：选择 Spring AI Alibaba，与 Spring 生态无缝集成。
- **需要自定义文档切分或嵌入模型**：OpenAI 兼容接口 + 自建知识库管线，或 LlamaIndex 本地知识库方案。

## 被对比主题页

- [frameworks](../api/frameworks.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


