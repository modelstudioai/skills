# 插件、MCP 与工具框架对比

阿里云百炼为大模型应用提供了三条主流"扩能"路径：**插件（Plug-in）**、**模型上下文协议（MCP）** 与 **工具框架（Toolkits & Frameworks，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)体系）**。三者定位不同——插件偏向平台预置能力的即插即用，MCP 面向跨系统标准化工具接入，工具框架则聚焦于让既有 OpenAI/LangChain 生态无缝迁移到百炼。本页从形态、集成方式、模型支持、调用协议、计费与典型场景等维度做一次横向对比，帮助开发者在技术选型阶段快速定位合适方案。

## 对比背景

- **插件**：百炼原生的工具集合概念，一个插件下挂多个工具（API），可通过智能体应用、工作流应用或 Assistant API 触发。分为官方插件、三方插件、自定义插件三类。
- **MCP**：Anthropic 主导的开源协议，百炼提供官方托管与自定义部署两种服务形态，重点解决"一次接入、多处复用"的工具标准化问题。
- **工具框架 / [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：百炼针对通义千问等模型提供的一整套与 OpenAI 高度兼容的接口（Chat Completions、Responses、Completions、Embedding、Files、Batch、Conversations 等），并可直接对接 LangChain / LangChain4j 等社区框架。

## 关键维度对比

| 维度 | 插件（Plug-in） | 模型上下文协议（MCP） | 工具框架（Toolkits & Frameworks） |
| --- | --- | --- | --- |
| 本质 | 平台内工具集合，扩展模型能力边界 | 大模型与外部工具间的开源标准协议 | OpenAI 兼容 API 与主流框架适配层 |
| 提供形态 | 官方插件 / 三方插件 / 自定义插件 | 官方 MCP 服务 / 自定义 MCP 服务（脚本部署 / AI 网关 / 阿里云 OpenAPI） | Chat Completions、Responses、Completions、Embedding、Files、Batch、Conversations 等接口 |
| 集成入口 | 智能体应用、工作流应用、Assistant API | 智能体应用、工作流应用；也支持外部第三方客户端（Cherry Studio、Cursor 等）与个人项目 SDK | OpenAI SDK / HTTP，直接调用模型；也可被 LangChain 等框架封装 |
| 与模型的交互协议 | 平台内部触发，由模型基于名称与描述判断是否调用工具 | 遵循 MCP 协议（Streamable HTTP，旧版 SSE 已升级） | OpenAI 兼容协议（REST / SSE 流式） |
| 支持模型 | qwen-turbo / qwen-plus / qwen-max / qwen-vl-max / qwen-vl-plus（以控制台实测为准） | 智能体或工作流中使用的模型（推荐千问 3 系列以获得更稳定的工具调用） | Qwen 商业版与开源版、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及 DeepSeek、Kimi、GLM、MiniMax 等三方模型 |
| 每个应用可挂载数量 | 智能体应用最多 **10 个工具** | 单个智能体最多 **5 个 MCP 服务**；工作流单节点仅支持 1 个工具 | 无平台侧数量限制（受模型上下文与开发者代码控制） |
| 典型 API 端点 | 通过 Assistant API 传 `tool_id`（如 `calculator`） | 云端：`https://dashscope.aliyuncs.com/api/v1/mcps/<name>/mcp`；`type` 必须与端点匹配（`sse` → GET `/sse`，`streamableHttp` → POST `/mcp`） | 各地域 `/compatible-mode/v1` 前缀 + 资源路径（`/chat/completions`、`/responses`、`/embeddings`、`/files` 等） |
| 鉴权方式 | 平台内部授权 + 服务关联角色（`AliyunServiceRoleForSFMAccessCloudAPI`）；自定义插件支持 `basic` / `bearer` / `appcode` | `Authorization: Bearer <DASHSCOPE_API_KEY>`；敏感信息可用 KMS 凭据加密 | `api_key` 使用[百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)（`DASHSCOPE_API_KEY`），各地域独立 |
| 是否可直连千问 API | 通过 Assistant API 可直接调用 | **不支持**直连千问 API，必须挂在智能体或工作流内 | 直接调用模型，无需应用层封装 |
| 本地资源访问 | 由自定义插件的后端实现决定 | 托管在函数计算 FC，**不能访问用户本地资源**；如需访问建议在本地部署 MCP Server | 由开发者的应用代码自行处理 |
| 上下文与多轮管理 | 由智能体/工作流内部拼接 | 工具返回内容作为上下文注入模型，会增加 Token 消耗 | Responses + Conversations 可通过 `previous_response_id`（有效期 7 天）自动管理多轮 |
| 计费方式 | 官方插件：多数免费，部分限时免费需申请；三方/自定义按第三方或业务实际计费 | 云部署：限时免部署费，联网搜索超 2000 次后 29 元/千次；自定义部署：基础模式 0.000156 元/秒；极速模式 0.000036 元/秒（部署）+ 0.000156 元/秒（调用） | 按所调用模型的推理 Token 计费；Batch、文件、Embedding 各接口按对应资源计费 |
| 生态兼容性 | 百炼平台专有 | 遵循 MCP 开源标准，可跨支持 MCP 的客户端/项目复用 | 与 OpenAI SDK、LangChain 等生态高度兼容，迁移成本低（改 `api_key`/`base_url`/`model` 三项） |
| 常见错误码 | RAM 授权 140052 等 | `11200044`~`11200060` 系列（连接、超时、鉴权、协议错配 405/404） | 参考 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)的错误规范 |

## 适用场景建议

- **优先选择"插件"的场景**
  - 需要"开箱即用"的通用能力：Python 代码解释器、计算器、图片生成、夸克搜索、二维码、GitHub 搜索等。
  - 希望在百炼智能体或工作流中以最低成本让模型具备工具调用能力，且工具形态是较为传统的 REST API。
  - 团队的能力扩展只服务于百炼平台，不需要跨系统标准化。

- **优先选择"MCP"的场景**
  - 已有多个 Agent 客户端（Cursor、Cherry Studio、自研项目）需要**复用同一套工具**，希望走标准协议避免重复接入。
  - 存在需要通过阿里云 OpenAPI 操作 OSS/ECS 等云资源、或将存量 RESTful API 通过 AI 网关升级为标准工具的诉求。
  - 需要在同一个智能体中组合多个高质量官方服务（如 Amap Maps + QuickChart + WebSearch）完成路径规划、数据可视化、联网检索等复合任务。
  - 对调用频次与冷启动敏感时，选择极速模式；对偶发调用敏感时，选择基础模式。

- **优先选择"工具框架 / OpenAI 兼容接口"的场景**
  - 已有基于 OpenAI SDK 或 LangChain / LangChain4j 的成熟应用，希望以最小代价迁移到百炼。
  - 需要直接对模型进行编排、控制多轮上下文、批量推理、文档抽取、代码补全（如 `qwen-coder-turbo`）、文本或多模态 Embedding 等能力。
  - 需要在 Chat Completions 之上使用 **Responses API** 的内置工具（联网搜索、网页抓取、代码解释器、文搜图/图搜图）与 `previous_response_id` 免拼接多轮机制。
  - 关注多地域部署（北京、新加坡、东京、法兰克福、弗吉尼亚），需要业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）。

## 组合使用建议

三者并非互斥关系，实际落地时经常组合出现：

1. **对话入口 = 智能体应用（挂载插件 + MCP）**：让模型可以按对话上下文自动路由至代码解释、地图、联网搜索等能力。
2. **业务后端 = OpenAI 兼容接口**：由业务侧直接调用 `chat/completions`、`responses` 或 `embeddings` 完成结构化生成、向量检索、代码补全等确定性任务。
3. **跨平台复用 = MCP**：将高价值内部工具沉淀为 MCP 服务，同时被百炼智能体、Cursor 等第三方客户端与自研 Agent 共享。

## 技术选型速查

- 只想"给通义千问加几个能力"、又不想写后端 → **插件**（尤其是官方插件）。
- 已经/即将在多个 Agent 客户端之间复用工具，或需要操作阿里云资源 → **MCP**。
- 已有 OpenAI/LangChain 代码或需要 Batch、Embedding、Responses 等原生接口 → **工具框架 / OpenAI 兼容接口**。
- 复杂业务：三者组合，用工具框架承担确定性接口调用，用 MCP 承担跨端标准工具，用插件补齐平台内即用能力。

## 被对比主题页

- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


