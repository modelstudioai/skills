# 智能体开发框架、流程型智能体与托管智能体对比

为帮助开发者在百炼平台上高效选型，本文系统对比三类核心智能体能力：**智能体开发框架（[frameworks](../api/frameworks.md)）**、**流程型智能体（Flow Agent API）** 和 **托管智能体（Managed Agents API）**。三者定位不同——框架面向 *已有应用生态的快速集成*，流程型智能体聚焦 *低代码工作流编排与轻量状态管理*，而托管智能体提供 *全生命周期可编程智能体基础设施*。本对比基于当前平台能力（截至 2024 年 Q3），旨在厘清技术边界、适用约束与演进方向，避免因误用导致开发返工或生产隐患。

## 关键维度对比

| 维度 | 智能体开发框架（[frameworks](../api/frameworks.md)） | 流程型智能体（Flow Agent API） | 托管智能体（Managed Agents API） |
|------|------------------------------|----------------------------------|------------------------------------|
| **本质定位** | 框架适配层：将百炼模型能力注入 LlamaIndex / Spring AI 等主流 SDK | 应用级执行接口 + 组件管理 API：调用已发布智能体/工作流，管理 Prompt 与（旧）[长期记忆](../concepts/long-term-memory.md) | 基础设施级 API：构建、部署、运行和观测可编程智能体实例的完整控制平面 |
| **输入格式** | 标准化框架输入（如 `ChatMessage` 列表、`QueryBundle`）；**仅支持纯文本输入**；不接受 `image`/`audio` | 应用调用接口：JSON 结构化消息体（含 `input` 字符串或 `messages` 数组）；组件接口（如 `CreateMemoryNode`）需传 `content` 字符串（1–200 字符） | JSON 请求体，支持多模态输入（通过 `File` 资源上传后引用）、结构化 `input`、`memory_id`、`session_id` 等上下文参数 |
| **输出格式** | 框架原生返回（如 `ChatResponse` 对象、`StreamEvent` 迭代器）；流式响应需框架自身支持（LlamaIndex 同步流，Spring AI Alibaba 异步 Mono） | 应用调用接口：标准 JSON 响应（含 `output` 字符串或 `messages` 数组），支持 `stream=true` 的 SSE [流式输出](../concepts/streaming-output.md)；组件接口返回资源 ID（如 `memoryId`）及元数据 | 同步：JSON 响应（含 `event_type`、`data`）；异步：通过 Webhook 推送标准化 `Event` 流（如 `tool_called`, `agent_finished`）；支持完整会话事件回溯 |
| **支持模型** | 仅限百炼文本生成模型（`qwen-max`, `qwen-plus` 等）；**明确不支持多模态模型（如 `qwen-vl`）** | 由智能体应用配置决定，API 层**不暴露模型选择参数**；实际可用模型取决于控制台中该应用的部署设置 | 用户在创建 `Agent` 时显式指定模型 ID（如 `qwen-max`）；受平台模型兼容性约束；**支持所有百炼文本与多模态模型**（需模型本身能力匹配） |
| **API 端点与鉴权** | 复用框架默认 endpoint（如 LlamaIndex 使用 `base_url=https://dashscope.aliyuncs.com/compatible-mode/v1`）；Bearer [Token](../concepts/token.md) 认证（`api_key` 或环境变量） | **严格分离两类端点**：<br>• 应用调用：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，Bearer [Token](../concepts/token.md)；<br>• 组件管理（如[长期记忆](../concepts/long-term-memory.md)）：阿里云 OpenAPI 地址，**必须使用 AccessKey 签名（ACS3-HMAC-SHA256）** | 统一 RESTful endpoint（如 `https://dashscope.aliyuncs.com/api/v1/agents`）；**统一 Bearer [Token](../concepts/token.md) 认证**（`Authorization: Bearer <access_token>`） |
| **计费方式** | **按底层模型调用计费**（如 `qwen-max` 的 token 数）；框架层无额外费用 | **按智能体应用调用次数/时长计费**（具体以控制台定价页为准）；[长期记忆](../concepts/long-term-memory.md)组件 API **免费**（但有调用频次限制） | **按 Agent 实例运行时长 + Session 消息处理 + 文件/内存存储量计费**；环境、技能、凭证等管理操作不计费 |
| **会话状态管理** | **不支持跨请求会话状态共享**；状态需由应用自行维护（如 `ChatEngine` 实例内） | 应用调用接口**隐式支持会话上下文**（依赖 `workspaceId` 和应用内部状态）；长期记忆（旧）提供 `memoryId` 显式绑定，但功能受限且已标记为“旧” | **原生强会话支持**：`Session` 是一级资源，支持事件订阅、状态查询（`active`/`timeout`/`finished`）、历史回溯与并发控制（单 Agent 最高 1000 Session） |
| **扩展性与定制能力** | 有限：仅支持框架定义的插件点（如 LlamaIndex 的 `NodePostprocessor`、Spring AI 的 `Tool` 自动发现）；无法修改 Agent 内核逻辑 | 低：面向已发布应用，定制需回到控制台重新配置 Prompt/工作流；组件 API 仅提供基础记忆 CRUD，**不支持自定义工具、技能或运行时逻辑** | 高：支持注册自定义 `Skill`（Python/HTTP 工具）、挂载 `Vault` 密钥、注入 `Credential`、配置 `Webhook` 事件回调、隔离 `Environment` 依赖；可编程控制全生命周期 |
| **典型场景** | • 在 LlamaIndex RAG 应用中无缝替换 LLM 为百炼模型<br>• 在 Spring Boot 微服务中集成百炼 Chat/Embedding 能力 | • 快速上线客服对话机器人（复用控制台配置的工作流）<br>• 为现有业务系统调用一个预置的“合同审核”智能体<br>• （过渡期）使用 `memoryId` 为对话注入静态背景知识 | • 构建企业级 AI 助手（需文件解析、数据库查询、多步骤决策）<br>• 开发带长期记忆与权限隔离的 SaaS 应用后台智能体<br>• 需要实时监控、事件驱动、灰度发布的生产级智能体服务 |

## 各方案适用场景建议

- **选择智能体开发框架（[frameworks](../api/frameworks.md)）当且仅当**：  
  ✅ 你已在使用 LlamaIndex 或 Spring AI Alibaba，并希望**最小改动接入百炼模型**；  
  ✅ 你的需求是“增强现有应用的 AI 能力”，而非构建新智能体；  
  ❌ 不适合需要会话状态、多模态、自定义工具链或生产级运维的场景。

- **选择流程型智能体（Flow Agent API）当且仅当**：  
  ✅ 你追求**零代码/低代码交付**，且业务逻辑可被控制台工作流可视化编排覆盖；  
  ✅ 你需要快速对接一个**已发布、经测试的智能体应用**（如“会议纪要生成”）；  
  ⚠️ 注意：若需长期记忆，请确认控制台最新机制（文档明确标注组件 API 中的长期记忆为“旧”，不支持用户画像，新项目应避免依赖）；  
  ❌ 不适合需要深度定制 Agent 行为、集成私有工具、或要求细粒度会话控制的场景。

- **选择托管智能体（Managed Agents API）当且仅当**：  
  ✅ 你需要**完全掌控智能体行为**：从模型选择、工具注册、文件处理到事件监听；  
  ✅ 你的应用有**生产级要求**：环境隔离、会话状态持久化、Webhook 异步通知、灰度发布；  
  ✅ 你正在构建**可复用、可编排、可观测的智能体服务**（如 AI 中台能力）；  
  ❌ 不适合简单一次性调用或无工程资源投入维护的轻量需求。

## 技术选型参考（面向开发者）

| 你的问题 | 推荐方案 | 理由 |
|----------|-----------|------|
| “我用 LlamaIndex 做 RAG，怎么把 OpenAI 替换成百炼？” | frameworks | 直接替换 LLM 实例，5 分钟完成，无需改架构 |
| “我们有个现成的 Spring Boot 后端，想加个百炼聊天接口” | frameworks | 利用 `AlibabaAIClient`，天然融入 Spring 生态，自动管理连接池 |
| “产品让我明天上线一个‘FAQ 问答机器人’，已有知识库” | Flow Agent API | 控制台拖拽配置 Prompt + 知识库，发布后调用 `/v1/chat` 即可，最快路径 |
| “我们需要一个能读 PDF、查数据库、调用内部 API 的销售助手，且要记录每次交互” | Managed Agents API | 唯一支持 `File` 上传解析、`Skill` 注册、`Session` 全事件追踪的方案 |
| “智能体要记住用户偏好（如常用地址），且不同部门数据要隔离” | Managed Agents API | `Environment` 提供权限/配置隔离；`Memory Store` 支持结构化长期记忆（非“旧”API）；`Session` 绑定用户上下文 |
| “调用报错 404，是不是 endpoint 写错了？” | 查鉴权方式：<br>• Bearer Token → frameworks 或 Flow 应用接口<br>• AccessKey 签名 → Flow 组件接口（如长期记忆）<br>• `access_token` → Managed Agents API | 三者鉴权与 endpoint 完全独立，混用必失败；务必先确认调用的是哪类接口 |

> **重要提醒**：  
> - **避免混合使用“旧”长期记忆**：Flow Agent API 中的 `CreateMemory` 等接口已明确标注为“旧”，其能力已被托管智能体的 `Memory Store` 和控制台新记忆机制替代。新项目请直接选用 Managed Agents API 或查阅控制台最新文档。  
> - **模型能力需对齐**：`frameworks` 不支持多模态，若需图像理解，请切换至 `Managed Agents API` 并选用 `qwen-vl` 等模型。  
> - **计费透明化**：所有方案均按实际资源消耗计费，但计量维度不同——请在控制台开通对应服务后，结合 [计费说明](https://help.aliyun.com/zh/model-studio/pricing) 进行成本预估。  

---  
*本文档依据百炼平台 2024 年 Q3 文档版本编写。功能与限制可能随平台迭代更新，请以控制台最新文档及 API 响应为准。*

## 被对比主题页

- [frameworks](../api/frameworks.md)
- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)


