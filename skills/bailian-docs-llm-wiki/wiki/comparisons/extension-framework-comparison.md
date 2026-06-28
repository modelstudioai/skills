# 框架、工具包与 MCP 对比

阿里云百炼为开发者提供了多种接入与扩展大模型能力的方式，常见的选择包括三类：**开源框架集成**（LlamaIndex、Spring AI Alibaba）、**[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)族与官方 SDK/工具包**（compatible-mode/v1、DashScope SDK、LangChain 适配）、以及**模型上下文协议（MCP）服务**。三者面向的诉求不同——框架侧重在既有编程语言生态中拼装 RAG/[智能体应用](../concepts/agent-application.md)；兼容接口族侧重用最小改动复用 OpenAI 代码与生态；MCP 则侧重让智能体/工作流动态调用外部工具与云资源。本文从接入方式、语言/运行时、能力范围、适用场景、计费与限制等维度做横向对比，供技术选型参考。

## 关键维度对比

| 维度 | 开源框架（LlamaIndex / Spring AI Alibaba） | [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)族与工具包 | MCP 服务（官方 + 自定义） |
| --- | --- | --- | --- |
| 接入方式 | 框架 SDK + 百炼云端[知识库](../concepts/knowledge-base.md) / 应用 ID | 替换 `api_key`、`base_url`、`model` 三参数，复用 OpenAI 路径 | 在智能体/工作流中挂载 MCP 服务，或外部通过 Streamable HTTP 调用 |
| 语言/运行时 | Python 3.9+（LlamaIndex）、Java JDK 17+ / Spring Boot 3.x（Spring AI Alibaba） | 任意支持 OpenAI SDK 的语言；官方同时适配 LangChain、LangChain4j | 语言无关（协议层）；自定义服务可由 npx/uvx/http 部署 |
| 鉴权 | [API Key](../concepts/api-key.md)（`DASHSCOPE_API_KEY` 等环境变量）；子[业务空间](../concepts/workspace.md)需[业务空间](../concepts/workspace.md) ID | [API Key](../concepts/api-key.md)（推荐 `DASHSCOPE_API_KEY`）；新加坡与北京地域 Key 不同 | [API Key](../concepts/api-key.md) + MCP 服务自身鉴权（如 `Authorization` 头）；仅主账号及授权 RAM 用户可访问自定义服务 |
| 主要能力 | 云端[知识库](../concepts/knowledge-base.md)构建、RAG 应用、调用百炼智能体/工作流应用、[知识库](../concepts/knowledge-base.md)检索 | Chat、Responses、Completions、Embedding、Vision、File、Batch、Conversations | 官方工具（地图、联网搜索等）、自定义脚本工具、封装 RESTful API、操作阿里云 OpenAPI（OSS、ECS 等） |
| 知识库/RAG | LlamaIndex 用云端智能切分与官方向量模型，不支持自定义切分/嵌入；Spring AI Alibaba 通过 `DashScopeDocumentRetriever` 检索百炼知识库 | Embeddings 接口做向量化；RAG 需自行在应用层编排 | 不直接提供 RAG；可作为工具被智能体调用，间接参与检索/查询 |
| 模型范围 | LlamaIndex 传 `qwen-max` 等；Spring AI Alibaba 调用智能体/工作流应用（应用背后绑定模型） | Qwen 全系（商业/开源/VL/Coder/Omni/Math）、DeepSeek、Kimi、GLM、MiniMax 等；Responses 支持 qwen3-max/plus/flash、qwen3-coder-plus 等 | 由承载 MCP 的智能体/工作流模型决定；调用准确性依赖提示词，必要时换用千问 3 系列等更强推理模型 |
| 调用形态 | 非流式与流式（Spring AI Alibaba `agent.call` / `agent.stream`） | 流式与非流式；Responses 支持 `previous_response_id` 多轮接续；Batch 异步批量（费用 50%） | 智能体自动判断是否调用；工作流中每节点单工具、手动串联；外部调用走 Streamable HTTP |
| 计费方式 | 按所调用模型/知识库的百炼标准计费 | 按模型 token 计费；Batch/Batch Chat 半价；Responses 上下文关联 7 天 | 云部署 MCP 限时免部署费；联网搜索 2000 次免费后 29 元/千次；自定义基础模式 0.000156 元/秒，极速模式另加 0.000036 元/秒部署时长 |
| 典型场景 | 已使用 Python/Java 生态、希望以框架方式构建 RAG 或集成百炼智能体 | 已有 OpenAI/LangChain 代码、希望低成本迁移或复用生态工具 | 让智能体/工作流动态调用第三方工具或阿里云资源，避免逐个写接口 |

## 适用场景建议

- **选开源框架（LlamaIndex / Spring AI Alibaba）**：团队以 Python 或 Java/Spring 为主技术栈，希望以框架抽象快速搭建 RAG 应用或集成百炼智能体/工作流应用，且可接受云端智能切分与官方向量模型（LlamaIndex）或预先在控制台创建应用/知识库（Spring AI Alibaba）。若需要完全自定义文档切分与嵌入模型，LlamaIndex 路线并不适合，应改用本地知识库方案。
- **选 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)族与工具包**：已有基于 OpenAI SDK 或 LangChain/LangChain4j 的存量代码，希望以最小改动（`api_key`/`base_url`/`model`）迁移到百炼，或需要使用 Completions（FIM 代码补全）、Batch（半价批量推理）、Responses（智能体原生能力、内置工具、多轮接续）等专项接口。适合追求协议兼容、跨语言复用与生态工具接入的团队。
- **选 MCP 服务**：核心诉求是让百炼智能体或工作流在运行时动态调用外部工具（地图、联网搜索、自建脚本、RESTful API、阿里云 OSS/ECS 等），而非固定编写接口。适合需要多工具协同、逐步推理、或把已有业务 API 快速封装给模型使用的场景。注意 MCP 只能在智能体/工作流应用中使用，不能在直接调用千问 API 时接入；且会因工具返回内容进上下文而增加 token 消耗。

## 技术选型参考

1. **先明确诉求边界**：是"迁移/复用现有 OpenAI 代码"（走兼容接口族）、"用框架拼装 RAG/[智能体应用](../concepts/agent-application.md)"（走开源框架），还是"让运行时智能体动态调用外部工具"（走 MCP）。三者并非互斥，常组合使用——例如用兼容接口族做模型调用，同时用 MCP 扩展工具能力。
2. **地域与鉴权一致性**：兼容接口族需按[业务空间](../concepts/workspace.md)专属域名拼装 `base_url`，弗吉尼亚地域使用固定域名且不带 `{WorkspaceId}`；Spring AI Alibaba 应用集成与知识库检索对 API Key 变量名约定不同（`DASHSCOPE_API_KEY` vs `AI_DASHSCOPE_API_KEY`），关键是 `application.yml` 占位符与实际变量名一致；子业务空间一律需要业务空间 ID。
3. **能力限制与成本**：LlamaIndex 云端方案不支持自定义切分/嵌入；Completions 仅限北京地域；MCP 单智能体最多 5 个服务、工作流每节点单工具、自定义服务托管在 FC 无固定出口公网 IP（访问云资源需配白名单或打通 VPC）。批量推理与 Batch Chat 可享 50% 费用优惠；MCP 联网搜索有免费额度与 QPS 限制，自定义服务按响应速度分基础/极速两种计费。
4. **协议演进**：MCP 已从旧版 SSE 升级为 Streamable HTTP，已开通用户需"取消开通"后重新"立即开通"完成升级；Responses API 旧版路径即将停用，应使用 `/compatible-mode/v1/responses`，且 `previous_response_id` 传顶层 `id`（UUID，有效期 7 天）。

## 被对比主题页

- [frameworks](../api/frameworks.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model context protocol](../guides/model-context-protocol.md)


