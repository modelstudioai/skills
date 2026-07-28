# 框架与工具包对比

阿里云百炼提供两条不同的框架与工具包集成路径：一条是通过 **LlamaIndex / Spring AI Alibaba** 等原生框架深度集成百炼的云端知识库与智能体应用能力；另一条是通过 **OpenAI 兼容接口**体系，以最小改动迁移已有 OpenAI 应用或接入 LangChain 等主流框架。本文从集成方式、语言生态、核心能力、适用场景等维度对两条路径进行对比，帮助开发者根据自身技术栈和业务需求做出选型。

## 关键维度对比

| 维度 | [frameworks](../api/frameworks.md)（原生框架集成） | toolkits-and-[frameworks](../api/frameworks.md)（OpenAI 兼容接口） |
| --- | --- | --- |
| **集成方式** | 使用框架原生 SDK 深度对接百炼云端知识库、智能体应用、工作流 | 替换 `api_key`、`base_url`、`model` 三项即可迁移已有 OpenAI 应用 |
| **语言/生态** | Python（LlamaIndex）、Java（Spring AI Alibaba，JDK 17+） | 任意支持 OpenAI SDK 的语言；可直接接入 LangChain / LangChain4j |
| **核心能力** | 云端知识库构建、RAG 检索引擎、智能体应用调用（流式/非流式）、工作流应用调用 | Chat Completions、Responses、Completions、Embedding、文件上传、Batch 批量推理、Conversations 会话管理、Vision 视觉理解 |
| **知识库** | 支持将本地文件上传到百炼构建云端知识库，使用默认智能切分与官方向量模型；Spring AI Alibaba 可检索百炼知识库 | 不直接提供知识库构建能力，但可通过 Embedding 接口自行实现向量检索 |
| **文档切分/嵌入模型** | 云端方案不支持自定义切分与嵌入模型；需本地知识库方案方可灵活控制 | 可自由选择嵌入模型（text-embedding-v1~v4），v3/v4 支持自定义向量维度 |
| **智能体/工作流** | Spring AI Alibaba 直接调用百炼智能体应用与工作流应用，获取思考过程、文档引用等元数据 | Responses API 提供内置联网搜索、网页抓取、代码解释器等工具，通过 `previous_response_id` 自动管理多轮上下文 |
| **API 端点** | 通过框架 SDK 封装调用百炼原生接口 | 统一使用 `/compatible-mode/v1` 路径，HTTP 调用追加具体资源路径 |
| **鉴权** | API Key 配置到环境变量（`DASHSCOPE_API_KEY` 等） | API Key 配置到环境变量 `DASHSCOPE_API_KEY`；各地域 API Key 不同，切换地域需同步更换 |
| **多地域支持** | 主要面向百炼主站 | 支持华北2（北京）、新加坡、日本（东京）、德国（法兰克福）、美国（弗吉尼亚）等多地域，含[业务空间](../concepts/workspace.md)专属域名 |
| **迁移成本** | 需按框架文档搭建工程、配置依赖、编写集成代码 | 已有 OpenAI 应用通常零代码改动，仅改配置即可完成迁移 |
| **典型场景** | 从零构建 RAG 应用、集成百炼智能体/工作流到 Java/Python 工程 | 迁移已有 OpenAI 应用、多语言接入、使用 LangChain 生态、批量推理、代码补全 |

## 适用场景建议

### 选择 [frameworks](../api/frameworks.md)（原生框架集成）的情况

- **需要使用百炼云端知识库**：希望将本地文档上传到百炼、由平台托管知识库并完成智能切分与向量索引，无需自建向量数据库。
- **需要调用百炼智能体应用或工作流应用**：已在百炼控制台创建了智能体或工作流，希望在 Java 后端通过 Spring AI Alibaba 集成，获取[流式输出](../concepts/streaming.md)、思考过程等结构化结果。
- **使用 Python 构建 RAG**：技术栈为 Python，希望用 LlamaIndex 快速搭建[检索增强生成](../concepts/rag.md)应用，复用百炼的向量模型与重排能力。

### 选择 toolkits-and-frameworks（OpenAI 兼容接口）的情况

- **已有 OpenAI 应用需要迁移**：应用已使用 OpenAI SDK，希望以最低成本切换到百炼通义千问等模型，不改动业务逻辑。
- **多语言或 LangChain 生态**：使用的语言或框架不在原生框架覆盖范围内（如 Go、Node.js、LangChain/LangChain4j），通过 OpenAI 兼容接口可无缝接入。
- **需要多地域部署**：业务需要在中国内地、新加坡、日本、德国、美国等多地域调用模型，通过切换 `base_url` 即可实现。
- **需要批量推理或代码补全**：有大规模批量推理需求（Batch 接口）或代码补全场景（Completions 接口，支持 `qwen-coder-turbo`）。
- **需要 Responses API 的高级能力**：希望使用内置联网搜索、网页抓取、代码解释器等工具，以及通过 `previous_response_id` 自动管理多轮上下文。

### 两者结合使用

在实际项目中，两条路径并非互斥。常见的组合方式是：使用 **toolkits-and-frameworks** 的 OpenAI 兼容接口完成模型调用（Chat Completions、Embedding 等），同时使用 **frameworks** 的 LlamaIndex 或 Spring AI Alibaba 对接百炼云端知识库与智能体应用，兼顾迁移便利性与平台原生能力。

## 被对比主题页

- [frameworks](../api/frameworks.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


