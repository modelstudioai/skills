# 智能体架构方案对比：托管型、流程型与沙箱型

为帮助开发者在百炼平台上高效选型，本文系统对比三种核心智能体架构方案：**托管型（Managed Agents）**、**流程型（Flow Agent）** 与 **沙箱型（Sandbox）**。三者定位互补——托管型面向“开箱即用的生产级 Agent 全生命周期管理”，流程型聚焦“已发布应用的轻量调用与 Prompt/记忆组件编排”，沙箱型则专精于“安全隔离的代码执行环境供给”。本对比基于当前（2024年Q3）平台正式能力，旨在为技术决策提供客观、可落地的参考依据。

## 关键维度对比表

| 维度 | 托管型（Managed Agents API） | 流程型（Flow Agent API） | 沙箱型（Sandbox API） |
|------|-----------------------------|---------------------------|------------------------|
| **核心定位** | 托管式 Agent 运行时：内置状态管理、[长期记忆](../concepts/long-term-memory.md)、工具调用、环境隔离的完整 Agent 框架 | 应用网关 + 组件管理双模接口：调用已发布智能体/工作流，并管理 Prompt 模板、旧版[长期记忆](../concepts/long-term-memory.md)等辅助资源 | 隔离式代码执行沙箱：提供容器化、可配置、带网络/文件能力的运行时环境，不直接提供 LLM 推理 |
| **输入格式** | `POST /sessions/{id}/messages`，请求体为结构化 `messages` 数组（含 `role`/`content`/`tool_calls`），支持 `tool_choice` 显式控制 | **应用调用类**：`messages`（多轮）或 `prompt`（单轮）；**组件类**：JSON 格式资源定义（如 `CreatePromptTemplate`） | 无语义化输入；通过 `/sandboxes/{id}/connect` 建立连接后，使用 E2B 协议发送 `execute`、`uploadFile`、`browse` 等指令 |
| **输出格式** | 同步 JSON 响应，含 `output`（文本/工具调用结果）、`tool_calls`、`usage`（token 消耗）、`trace_id`；支持 `debug: true` 返回完整推理链路 | **应用调用类**：标准 DashScope Completion 响应（含 `output.text`、`usage`、`request_id`）；**组件类**：阿里云 OpenAPI 标准 `Result<T>` 结构 | E2B 协议兼容响应：`execute` 返回 `stdout`/`stderr`/`exitCode`；`browse` 返回 HTML 截图或 DOM 文本；无 LLM 生成内容 |
| **支持模型** | 仅限百炼托管 Qwen 系列：`qwen-max`、`qwen-plus`、`qwen-turbo`；**不支持自定义模型或第三方模型** | 调用侧透明：取决于所部署的智能体应用本身使用的模型（控制台配置）；API 层不暴露模型选择能力 | **不提供模型服务**；沙箱是纯执行环境，模型调用需由外部 Agent（如托管型或流程型）发起并传入指令 |
| **API 端点与鉴权** | RESTful，统一 Base URL；使用 `X-DashScope-Access-Token`（24小时有效期） | **双端点体系**：<br>• 应用调用：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，`Authorization: Bearer <api-key>`<br>• 组件管理：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/{workspaceId}/...`，ACS3 签名鉴权（AccessKey） | 工作空间专属 Endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`；`Authorization: Bearer <api-key>` |
| **计费方式** | 按 **Agent 实例运行时长 + Token 消耗 + 文件存储** 计费；Environment、Memory Store 等资源按小时计费 | **应用调用类**：按调用次数 + Token 消耗计费（同 DashScope 模型 API）；**组件类**（Prompt/Memory）：免费额度内不计费，超出按量计费 | 按 **沙箱实例运行时长（秒） + 存储容量（GB·月）** 计费；文件上传、模版构建不额外收费 |
| **典型场景** | 构建客服对话机器人（需[长期记忆](../concepts/long-term-memory.md)+多轮工具调用）、自动化数据处理 Agent（需环境隔离+文件处理+凭证注入）、企业级 RAG 助手（需 Memory Store + Skill 封装） | 快速集成已上线的智能体应用到前端（如 Web App 调用客服 Bot）；批量管理 Prompt 模板（A/B 测试）；维护遗留系统的长期记忆数据（旧版 Memory API） | Agent 的工具执行后端（如 Python 数据分析、网页爬取、代码解释）、需要临时计算资源的插件（如 Excel 处理、PDF 解析）、安全敏感的代码沙盒验证 |
| **状态与会话管理** | 内置强会话（`session_id`）与环境（`environment_id`）隔离；Memory Store 提供持久化长期记忆；Session 上下文上限 32KB | 会话依赖 `session_id`（云端维护，1小时失效）；“长期记忆（旧）”为独立资源，需手动 CRUD；**无原生环境隔离概念** | 无会话/记忆概念；每个沙箱实例为独立容器，生命周期由 `timeout`/`autoPause` 控制；文件挂载实现“状态传递”，但非语义化记忆 |

## 各方案适用场景建议

### ✅ 选择 **托管型（Managed Agents）** 当：
- 你需要从零构建一个具备**完整 AI Agent 能力**（工具调用、长期记忆、多轮对话、环境隔离、凭证安全注入）的生产服务；
- 你希望**完全免运维**：无需管理模型部署、推理服务扩缩容、会话状态持久化、工具函数注册等底层细节；
- 你的业务对**安全性与合规性要求高**（如金融、政务），需利用 Vault 注入密钥、Environment 网络策略、Memory Store 权限控制等企业级能力；
- 你计划将 Agent 封装为可复用的 Skill，并在多个业务线中共享调用。

> ⚠️ 注意：若需使用非 Qwen 模型（如 Llama、Claude），或需深度定制推理逻辑（如自定义 LoRA 加载、特定 tokenizer），托管型不适用。

### ✅ 选择 **流程型（Flow Agent）** 当：
- 你已有在百炼控制台**发布完成的智能体或工作流应用**，只需在自有系统中快速调用其能力（如嵌入客服页面、集成进 CRM）；
- 你需要**批量管理 Prompt 模板**（例如为不同客户群配置差异化提示词），或需程序化维护一套遗留的长期记忆数据（注意：此为“旧版”能力，新项目请优先考虑托管型 Memory Store）；
- 你追求**最低接入成本与最快上线速度**，且对 Agent 内部状态管理、工具执行环境无定制需求；
- 你的调用方是前端应用或低代码平台，偏好简单 REST 调用而非复杂 SDK。

> ⚠️ 注意：地域限制严格（仅北京），且应用调用与组件管理必须使用**两套完全不同的鉴权机制与 Endpoint**，需在工程中明确分离。

### ✅ 选择 **沙箱型（Sandbox）** 当：
- 你的智能体需要**安全、隔离地执行任意代码**（Python 脚本、Shell 命令、浏览器自动化），且该代码可能访问网络、读写文件或消耗大量 CPU；
- 你正在构建一个**工具调用（Tool Calling）的后端执行引擎**，例如：将 `python_interpreter`、`web_browser`、`file_analyzer` 等工具映射为沙箱实例；
- 你需要**高度可复现的执行环境**（通过模版固化镜像、CPU/内存、挂载文件、网络策略），满足审计或测试要求；
- 你已有一个成熟的 Agent 框架（如 LangChain、LlamaIndex），仅需百炼提供可靠的沙箱作为其 `Tool` 的执行载体。

> ⚠️ 注意：沙箱本身**不生成文本、不理解 Prompt、不管理会话**；它是一个“哑”执行单元，必须由上层 Agent（如托管型或自研框架）负责调度、输入构造与结果解析。

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| “我要做一个能查订单、改地址、发短信的电商客服 Bot，要记住用户历史偏好” | **托管型** | 内置 Session + Memory Store + Tool（短信/订单系统 API）+ Vault（短信密钥）一体化支持，无需自行串联各模块 |
| “我们已在控制台发布了‘合同审核助手’，现在要嵌入到内部 OA 系统里调用” | **流程型（应用调用类）** | 直接 `POST /apps/{APP_ID}/completion`，最简路径；`stream=true` 支持流式返回提升用户体验 |
| “我用 LangChain 开发了一个 Agent，其中 `code_interpreter` 工具需要安全执行 Python” | **沙箱型** | 提供 `code-interpreter-v1` 镜像、文件挂载、超时控制，完美匹配 LangChain `Tool` 接口契约 |
| “我们需要为销售团队 A/B 测试 5 个不同版本的销售话术 Prompt” | **流程型（组件类）** | 使用 `CreatePromptTemplate` / `UpdatePromptTemplate` 批量管理，调用时动态指定 `prompt_template_id` |
| “我们要构建一个能自动抓取竞品网页、分析 PDF 报告、生成 PPT 的研究助理” | **托管型 + 沙箱型 组合** | 托管型作为主 Agent（协调流程、调用工具、维护记忆），沙箱型作为 `web_crawler` / `pdf_analyzer` / `ppt_generator` 工具的执行后端 |
| “我们的 Agent 需要调用私有 API，且该 API 需要 VPC 内网访问” | **托管型（Environment 网络配置）** 或 **沙箱型（networkConfig）** | 托管型 Environment 支持绑定 VPC；沙箱 `networkConfig` 可配置安全组与路由，二者均优于流程型（无网络控制能力） |

> 💡 **终极建议**：  
> - **新项目首选托管型**：它是百炼当前主推的、面向 Agent 原生开发的现代化架构，能力最全、演进最快、企业特性最完善。  
> - **存量集成选流程型**：适用于“调用已有资产”的轻量场景，避免重复开发。  
> - **代码执行必选沙箱型**：任何涉及 `exec`、`browse`、`run_script` 的需求，沙箱是唯一符合安全与隔离要求的官方方案。  
> - **复杂系统采用组合模式**：生产级 Agent 往往是“托管型（大脑） + 沙箱型（手脚） + 流程型（调用已发布能力）”的混合架构。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)
- [sandbox api](../api/sandbox-api.md)


