# 智能体 API 方案对比：托管型、流程型与 OpenAI 兼容型

为帮助开发者在百炼平台上高效选型，本文系统对比三种主流智能体 API 方案：**托管型（Managed Agents API）**、**流程型（Flow Agent API）** 与 **OpenAI 兼容型（OpenAI-Compatible Agents API）**。三者定位不同——托管型聚焦「全生命周期托管」，流程型强调「应用级集成与组件协同」，兼容型侧重「生态平滑迁移与标准协议适配」。本对比基于当前（2024年Q3）平台正式发布能力，所有信息均依据官方文档最新稳定版本验证，不包含灰度或未上线特性。

---

## 关键维度对比表

| 维度 | 托管型（Managed Agents API） | 流程型（Flow Agent API） | OpenAI 兼容型（OpenAI-Compatible Agents API） |
|------|------------------------------|---------------------------|-----------------------------------------------|
| **核心定位** | 声明式 Agent 托管服务：抽象运行时、内存、工具、环境等基础设施 | 应用中心化调用接口 + 平台组件管理接口：面向已发布应用的生产调用与 Prompt/记忆等辅助能力治理 | 标准协议桥接层：100% 兼容 OpenAI `/v1/chat/completions` 接口语义与结构，降低迁移成本 |
| **输入格式** | JSON 对象，含 `model_id`、`system_prompt`、`tools`（百炼专用 schema）、`memory_store_id` 等声明式字段；不支持 OpenAI `messages` 数组 | 分两类：<br>• **应用调用接口**（DashScope/Responses）：支持 `prompt`（字符串）或 `input`（OpenAI 风格 `messages` 数组）<br>• **组件类接口**（Prompt/Memory）：阿里云 OpenAPI 标准请求体（如 `CreatePromptTemplateRequest`） | 严格遵循 OpenAI 格式：`messages`（必填，含 `system`/`user`/`assistant` 角色）、`tools`（OpenAI function calling schema）、`tool_choice`、`model`（仅 `qwen-plus`/`qwen-max`） |
| **输出格式** | 百炼自定义结构：含 `agent_id`、`session_id`、`output`（含 `content` 和 `tool_calls`）、事件 Webhook（如 `session.completed`） | 分两类：<br>• **应用调用接口**：JSON 结构，含 `output.text` / `output.tool_calls` / `request_id`；流式响应为 SSE 格式<br>• **组件类接口**：阿里云 OpenAPI 统一格式（`Code`/`Message`/`Data`） | 完全兼容 OpenAI 响应：`id`、`choices[0].message`（含 `content` 或 `tool_calls`）、`finish_reason`（`"stop"`/`"tool_calls"`）、`usage`；流式响应为标准 OpenAI SSE |
| **支持模型** | 仅 `qwen-max`、`qwen-plus`、`qwen-turbo`（Qwen 系列专属） | 所有已发布应用所绑定的模型（包括 `qwen-*`、`llama-*`、第三方模型等），**由应用配置决定，API 层不直接指定模型** | 仅 `qwen-plus`、`qwen-max`（明确不支持 `qwen-turbo` 及第三方模型） |
| **API 端点** | `https://dashscope.aliyuncs.com/api/v1/agents`（创建）<br>`/sessions`（会话）<br>`/sessions/{id}/messages`（消息） | 分两类：<br>• **应用调用**：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（同步）<br>  `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（异步）<br>• **组件类**：`https://bailian.{region}.aliyuncs.com/{workspaceId}/promptTemplates` 等（多地域） | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`（单一端点） |
| **认证方式** | Bearer Token（OAuth2 Access Token，需通过百炼 OAuth2 流程获取） | 分两类：<br>• **应用调用接口**：Bearer Token（百炼 API Key）<br>• **组件类接口**：AccessKey 签名（ACS3-HMAC-SHA256），**不支持 API Key** | Bearer Token（百炼 API Key，需显式授权 `agents:read` 和 `agents:invoke` 权限） |
| **计费方式** | 按 Agent 实例运行时长（秒） + 会话 token 消耗（输入/输出）计费；Memory Store、Files 等组件单独计费 | 分两类：<br>• **应用调用**：按调用次数 + token 消耗计费（与所选应用计费策略一致）<br>• **组件类接口**：Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等为免费能力（无独立计费项） | 按 token 消耗计费（与 OpenAI 计费模型对齐）；Agent 实例无额外运行时费用；Session 状态跟踪不额外计费 |
| **典型场景** | 需长期运行、强状态管理、多会话共享记忆、高安全隔离（如企业客服 Agent、合规审计助手） | • 快速集成已上线的智能体/工作流应用（如嵌入 CRM 的销售助手）<br>• 需统一管理 Prompt 模板与旧版[长期记忆](../concepts/long-term-memory.md)的中后台系统<br>• 多地域部署（组件类接口）+ 华北2集中调用（应用接口）混合架构 | • 将现有 OpenAI 应用（如 LangChain、LlamaIndex 项目）零代码改造接入百炼<br>• 构建跨平台（OpenAI + 百炼）的统一 Agent 调度网关<br>• 快速 PoC 验证 Qwen 模型能力，无需学习新协议 |

---

## 各方案适用场景建议

### ✅ 推荐选择 **托管型（Managed Agents API）** 当：
- 你需要**从零构建一个具备完整生命周期管理能力的 Agent**，而非调用已有应用；
- 业务要求**跨会话持久化上下文**（如用户历史偏好、对话摘要），且需精细控制 Memory TTL、存储位置与访问策略；
- 对**安全合规性要求极高**：需显式绑定 Environment（网络隔离）、Vault（凭证加密存储）、文件沙箱（`file_search` 工具仅接受预上传 `file_id`）；
- 团队倾向于**声明式配置**（如通过 YAML 定义 Agent 行为），并希望平台自动处理重试、超时、错误恢复等运维细节。

> ⚠️ 注意：不适用于快速迁移 OpenAI 项目，也不适合调用控制台已发布的“应用”（如工作流应用）。

### ✅ 推荐选择 **流程型（Flow Agent API）** 当：
- 你的核心需求是**调用已在百炼控制台发布并经过测试的智能体或工作流应用**（例如：已上线的合同审核 Agent、多步骤报销审批工作流）；
- 需要**同时管理 Prompt 模板版本、A/B 测试不同提示词**，或需复用遗留的“[长期记忆](../concepts/long-term-memory.md)（旧）”数据；
- 架构涉及**多地域部署**（如德国法兰克福用户访问本地 Prompt 服务），且能接受应用调用必须走华北2（北京）网关的约束；
- 你正在构建一个**统一的百炼能力集成平台**，需同时对接应用调用、Prompt 管理、记忆服务等多类能力。

> ⚠️ 注意：应用调用接口**强制限定华北2地域**；组件类接口需手动管理 `workspace_id` 与地域匹配；`APP_ID` 和 `WORKSPACE_ID` **无法通过 API 获取**，必须人工复制。

### ✅ 推荐选择 **OpenAI 兼容型（OpenAI-Compatible Agents API）** 当：
- 你拥有**现成的 OpenAI 生态代码库**（如 LangChain 的 `ChatOpenAI`、LlamaIndex 的 `OpenAIEmbedding`），希望最小改动接入百炼；
- 项目处于**快速验证阶段**，需用标准 `curl` 或 Python `openai` SDK 直接发起请求，避免学习百炼特有参数（如 `environment_id`、`memory_store_id`）；
- 你追求**协议一致性**：希望同一套客户端逻辑可无缝切换 OpenAI / 百炼 / 其他兼容平台；
- 你只需要**轻量级会话状态**（`enable_session=true`），不依赖跨会话全局 Memory Store 或复杂工具链编排。

> ⚠️ 注意：不支持 `qwen-turbo`；`temperature`/`top_p` 等采样参数对 `qwen-plus` 无效；不支持 `response_format`（如 JSON mode）。

---

## 技术选型决策参考（面向开发者）

| 你的关键诉求 | 推荐方案 | 理由简述 |
|--------------|----------|----------|
| “我要把公司现有的 LangChain 应用从 OpenAI 切到百炼，一周内上线” | ✅ OpenAI 兼容型 | 仅需替换 `base_url` 和 `api_key`，无需重构 Agent 初始化、Tool 注册、Stream 处理逻辑 |
| “我需要开发一个银行理财顾问 Agent，必须记住客户风险测评结果、持仓历史，并隔离访问内部数据库” | ✅ 托管型 | 唯一支持显式 Environment（VPC 网络策略）、Vault（加密存储数据库凭据）、Memory Store（7天 TTL 可调）的方案 |
| “我们已在控制台发布了 20+ 个智能体应用，现在要给销售 SaaS 系统集成‘客户画像生成’和‘竞品分析’两个应用” | ✅ 流程型（应用调用接口） | 直接使用 `APP_ID` 调用，无需重新部署 Agent；可复用控制台的发布、灰度、监控能力 |
| “我们需要统一管理 50+ Prompt 模板，并支持运营人员在 Web 端 A/B 测试不同版本” | ✅ 流程型（组件类接口） | 唯一提供完整 Prompt 模板 CRUD API 的方案，且与百炼控制台 Prompt 管理功能实时同步 |
| “我想用百炼跑一个临时实验：测试 qwen-max 在工具调用中的表现，不关心长期维护” | ✅ OpenAI 兼容型 或 ✅ 托管型（快速创建） | 兼容型：`curl` 一行命令即可；托管型：`POST /agents` 创建后立即 `POST /sessions/xxx/messages`，适合调试 |
| “我们的 Agent 需要调用 15 个内部 API 工具，且部分工具需串行执行（B 依赖 A 结果）” | ✅ 托管型 | 支持最多 10 个工具绑定（注意限制），且内置多步推理调度器；兼容型虽支持并行/串行，但工具编排逻辑需客户端实现 |

> 💡 **终极建议**：  
> - **新项目起步**：优先评估 **托管型** —— 它代表百炼对下一代 Agent 架构的设计理念，提供最完整的自主可控能力；  
> - **存量应用集成**：若已发布应用，选 **流程型（应用调用）**；若需 Prompt/记忆治理，叠加 **流程型（组件类）**；  
> - **生态迁移与快速验证**：坚定选择 **OpenAI 兼容型** —— 它是百炼拥抱开放标准的关键桥梁，也是未来多模型、多平台调度的基础。  

所有方案均支持流式响应与错误码标准化，开发者可根据团队技术栈、交付节奏与长期演进目标组合使用。建议在真实业务场景中，用最小可行请求（如单次 `curl`）交叉验证三者行为差异，再做最终决策。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)


