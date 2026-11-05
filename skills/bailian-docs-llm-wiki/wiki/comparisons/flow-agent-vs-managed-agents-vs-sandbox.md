# Flow Agent、托管 Agent 与 Sandbox 沙箱对比

为帮助开发者在百炼平台中高效选型，本文对三种核心智能体运行范式——**Flow Agent（流程型智能体）**、**托管 Agent（Managed Agent，编排型智能体）** 和 **Sandbox 沙箱（隔离执行环境）** 进行系统性对比。三者定位不同：Flow Agent 侧重**声明式业务流程编排**，托管 Agent 提供**细粒度运行时控制能力**，而 Sandbox 则聚焦于**安全、可控的代码/工具执行沙箱**。理解其差异是构建高可靠、可维护、合规 AI 应用的前提。

---

## 关键维度对比表

| 维度 | Flow Agent | 托管 Agent（Managed Agents API） | Sandbox 沙箱 |
|------|------------|----------------------------------|--------------|
| **本质定位** | 面向业务逻辑的**低代码流程引擎**，以可视化/配置化方式串联 LLM、工具、分支、循环等节点 | 面向工程化的**Agent 全生命周期管理平台**，提供 Agent、Session、Memory、Skill 等资源级 RESTful 控制接口 | 面向安全执行的**隔离计算环境服务**，兼容 E2B 协议，用于运行不可信代码、Python 脚本、CLI 工具等 |
| **输入格式** | JSON 对象（`inputs`），键为流程中预定义的变量名；支持动态注入上下文数据 | 结构化消息体（如 `POST /sessions/{id}/messages` 中的 `content`, `role`, `tool_calls` 等字段）；支持多轮对话上下文与事件驱动输入 | 多样化：创建实例时传入 `templateID`/`timeout` 等配置；连接后通过 `envdAccessToken` + `domain` 发起数据面调用（如 HTTP POST `/run` 执行命令或上传文件） |
| **输出格式** | 同步：JSON 响应含 `status`, `output`, `task_id`；流式（`stream=true`）：SSE 分块（`event: output`/`error`/`done`） | 结构化 JSON 响应，含 `message.id`, `content`, `tool_calls`, `memory_updates`, `events` 等字段；支持 `/events` 端点流式拉取事件日志 | 实例级：返回 `sandboxID`, `status`, `domain`, `envdAccessToken`；执行级：返回命令 `stdout`/`stderr`/`exitCode`、文件读写结果、HTTP 响应体等原始执行产物 |
| **支持模型** | 仅限百炼托管模型：<br>• `qwen-max`<br>• `qwen-plus`<br>• `qwen-turbo`<br>（不支持第三方模型） | **不直接调用模型**；模型选择由绑定的 `Skill` 或下游工具决定（例如某 Skill 内部调用 `qwen-turbo` 或外部 API） | **不涉及模型调用**；沙箱本身无模型概念，仅提供运行环境。模型推理需由沙箱内程序自行发起（如调用百炼 API 或其他服务） |
| **API 端点示例** | `POST https://dashscope.aliyuncs.com/api/v1/agents/{app_id}/run` | `POST /v1/agents/{agent_id}/sessions`<br>`POST /v1/sessions/{session_id}/messages`<br>`GET /v1/sessions/{session_id}/events` | `POST /api/v1/agentstudio/sandbox/sandboxes`<br>`POST /sandboxes/{sandboxID}/connect`<br>`POST /sandboxes/{sandboxID}/run`（数据面） |
| **认证方式** | Bearer [Token](../concepts/token.md)（基于 AK/SK 签名生成的 `access_token`） | Bearer [Token](../concepts/token.md) + `X-App-ID` Header | Bearer [Token](../concepts/token.md)（使用百炼控制台生成的 **API Key**，格式为 `Bearer <your-api-key>`） |
| **计费方式** | 按 **调用量（次）+ 流程执行时长（秒）+ 模型 Token 消耗** 综合计费；流程中工具调用单独计费 | 按 **Agent 实例运行时长（小时）+ Session 数量 + Memory Store 存储量 + Skill 调用次数** 分项计费；部署（Deployment）本身不额外收费 | 按 **沙箱实例运行时长（秒）+ 挂载文件存储量（GB·月）+ 网络出流量（GB）** 计费；模版构建免费，但频繁构建可能触发配额限制 |
| **典型场景** | • 客服工单自动分派与升级流程<br>• 多步骤数据清洗与报告生成流水线<br>• 人机协同审批链（LLM 判断 + 人工确认节点） | • 需要会话状态持久化与跨轮记忆的对话机器人<br>• 多技能组合的复杂 Agent（如“旅行规划 Agent”集成航班查询、酒店比价、行程生成 Skill）<br>• 需审计事件日志与 RBAC 权限管控的企业级 Agent 平台 | • 运行用户上传的 Python 脚本进行数据分析<br>• 安全执行第三方工具（如 `curl`, `jq`, `pandas`）处理敏感数据<br>• 构建 AI 编程助手的“代码执行”插件模块 |

---

## 适用场景建议

### ✅ 推荐选用 **Flow Agent** 当：
- 业务逻辑清晰、步骤固定，且需快速上线（如订单履约、FAQ 自动归类）；
- 团队以产品/业务人员为主，希望最小化编码依赖，通过拖拽或 YAML 定义流程；
- 需要统一入口暴露给前端或第三方系统，且对响应延迟敏感（同步调用默认 <3s）；
- 不需要深度干预 Agent 内部状态，也不涉及复杂会话管理或多用户并发隔离。

> ⚠️ 注意：不适合需动态加载新工具、实时修改流程结构或强会话状态管理的场景。

---

### ✅ 推荐选用 **托管 Agent** 当：
- 开发者需完全掌控 Agent 行为：自定义会话超时、精细控制 memory 生命周期、按事件类型订阅回调；
- 应用需支持多租户、多版本 Agent 并行部署（如 `environment=prod` / `staging`）；
- 技能（Skill）复用率高，且需统一凭证管理（Credential）、权限校验（RBAC）与可观测性（Event 日志）；
- 计划构建 Agent 开发平台、低代码 Agent Studio 或集成至内部 DevOps 流水线。

> ⚠️ 注意：学习成本较高，需理解 `Session`、`Deployment`、`Memory Store` 等抽象概念；不适用于纯代码执行类需求。

---

### ✅ 推荐选用 **Sandbox 沙箱** 当：
- 必须执行不可信代码（如用户提交的 `.py` 文件）、第三方 CLI 工具或需操作系统级能力（网络、文件系统）的任务；
- 对安全性与隔离性有硬性要求（如金融、政务场景），需防止内存泄漏、无限循环、恶意外连；
- 需要挂载定制化环境（预装库、私有模型权重、配置文件）并复用模版（Template）快速启停；
- 作为 Agent 的“执行臂”（Executor），与 Flow Agent 或托管 Agent 协同工作（例如：Agent 决策 → Sandbox 执行 → 返回结果）。

> ⚠️ 注意：沙箱本身不提供 LLM 能力，所有 AI 推理需由沙箱内程序主动调用；不适用于纯文本对话或轻量逻辑编排。

---

## 技术选型参考指南（面向开发者）

| 你的需求 | 推荐方案 | 理由简述 |
|----------|----------|-----------|
| “我只想把几个 API 串起来，做成一个自动填表流程” | ✅ Flow Agent | 最快上手，无需管理会话/内存/部署，5 分钟完成流程发布 |
| “我要做一个支持 10 万用户同时对话、带历史回溯和敏感词过滤的客服机器人” | ✅ 托管 Agent | 原生支持 Session 管理、Memory Store 分片、Webhook 事件通知，满足高并发与合规审计 |
| “我要让用户上传 Python 脚本，自动跑出分析图表并返回 PNG” | ✅ Sandbox 沙箱 | 唯一提供 OS 级隔离与文件系统访问能力的方案，保障代码执行安全 |
| “我的 Agent 需要先调用 LLM 做决策，再调用数据库，最后在沙箱里跑一段数据处理脚本” | 🔁 **组合使用**：<br>Flow Agent 或 托管 Agent + Sandbox | Flow/托管 Agent 负责编排与决策，Sandbox 负责安全执行；通过 `task_id` 或 `sandboxID` 串联异步结果 |
| “我需要调试 Agent 每一步的中间输出（比如某个工具调用的原始 JSON）” | ✅ Flow Agent（节点日志）<br>✅ 托管 Agent（`/events` 流式日志） | 两者均支持细粒度日志回溯；Sandbox 仅提供最终 stdout/stderr，无中间推理痕迹 |
| “我已有大量 Python 工程经验，想用 SDK 写 Agent 逻辑” | ✅ 托管 Agent（官方 Python SDK 支持完整 CRUD）<br>✅ Sandbox（兼容 E2B SDK，适配简单） | Flow Agent 主推低代码，SDK 支持有限；后两者提供完备的编程接口 |

> 💡 **最佳实践提示**：  
> - **不要用 Sandbox 替代 Agent**：沙箱无对话管理、无记忆、无工具发现能力，不能独立完成 Agent 任务。  
> - **不要用 Flow Agent 做复杂状态管理**：[长期记忆](../concepts/long-term-memory.md)已迁移至向量存储服务，Flow Agent 本身不维护会话状态。  
> - **生产环境务必启用异步模式**：Flow Agent 与托管 Agent 的[异步调用](../concepts/asynchronous-invocation.md)（`async=true` 或 `deployment`）可避免请求超时，提升可用性。  
> - **Sandbox 实例需主动释放**：忘记调用 `DELETE /sandboxes/{sandboxID}` 将持续计费，建议结合 `maxRunningTimeout` 自动兜底。

--- 

*本文档依据百炼平台 v2.4 版本 API 规范编写，更新日期：2024年6月。请以控制台最新文档与 OpenAPI Schema 为准。*

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [sandbox api](../api/sandbox-api.md)


