# 智能体核心 API 对比：Managed Agents API vs Flow Agent API

本文旨在帮助开发者清晰理解百炼平台两大智能体核心 API 的定位差异、能力边界与适用边界，避免因选型不当导致开发返工、运维复杂度上升或功能缺失。随着百炼平台演进，`Managed Agents API` 侧重**可编程智能体的全生命周期自主编排**，而 `Flow Agent API` 侧重**已发布智能体/工作流的标准化调用与组件化管理**。二者并非替代关系，而是面向不同阶段、不同角色的技术栈：前者服务于需要深度定制 Agent 行为的算法工程师与平台开发者；后者服务于快速集成智能体能力的应用开发者与 SaaS 构建者。

---

## 关键维度对比

| 维度 | Managed Agents API | Flow Agent API |
|------|---------------------|----------------|
| **设计定位** | 可编程智能体（Agent）的基础设施层 API：支持从零构建、调试、部署、隔离运行和状态管理的完整 Agent 运行时环境 | 已发布智能体/工作流的调用网关 + 组件管理 API：聚焦“使用”而非“构建”，提供开箱即用的应用调用能力与 Prompt/记忆等辅助组件管理 |
| **输入格式** | 结构化 JSON 请求体，强约束字段（如 `environment_id`, `model`, `prompt_template`, `skills`）；支持 `Session` 级别多轮消息提交（`POST /v1/sessions/{id}/messages`） | 分两类：<br>• **应用调用（DashScope）**：支持单文本 `prompt` 或标准 `messages` 数组（含 `role: "system"/"user"/"assistant"`）；<br>• **组件管理（OpenAPI）**：RESTful CRUD 请求，需显式携带 `workspaceId` 和资源路径参数 |
| **输出格式** | 统一 JSON 响应体，含 `id`, `status`, `created_at` 等元信息；事件流（SSE）支持细粒度 `agent_step`、`tool_call`、`agent_finish` 等事件类型 | 分两类：<br>• **应用调用**：同步返回 `output.text` / `output.choices[0].message.content`；流式响应为 SSE，含 `delta` 或 `event: message`；异步返回 `task_id`；<br>• **组件管理**：标准阿里云 OpenAPI 响应（含 `RequestId`, `Code`, `Data`） |
| **支持模型** | **不直接绑定模型**；模型由用户在 Agent 配置中指定（如 `"qwen-max"`、`"qwen-plus"`），受环境可用模型白名单约束；支持所有百炼平台已授权的推理模型 | **仅调用已发布的应用**；底层模型由控制台创建应用时选定并固化；API 层不可动态切换模型；新版智能体应用支持 `qwen-max`、`qwen-plus` 等，旧版/工作流取决于发布时配置 |
| **API 端点与认证** | 单一 Base URL（如 `https://dashscope.aliyuncs.com/api/v1`）；**统一 Bearer Token 认证**（24 小时有效期）；所有端点共用同一鉴权体系 | **双认证体系、双 Base URL**：<br>• 应用调用：`https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`，Bearer Token（百炼 API Key）；<br>• 组件管理：`https://bailian.{regionId}.aliyuncs.com`，**ACS3-HMAC-SHA256 签名认证（AccessKey）**，不支持 Bearer |
| **计费方式** | 按 **Agent 实例运行时长 + 调用次数 + 文件/内存存储量** 计费；Environment 级别配额独立；会话、事件、Memory 存储均计入资源消耗 | 按 **应用调用次数 + 输出 token 量** 计费（DashScope 接口）；组件管理类 API（Prompt/记忆）**免费**；[异步任务](../concepts/asynchronous-task.md)按执行时长额外计费；无 Environment 或 Session 级别资源包概念 |
| **典型场景** | • 构建带自定义工具链、多步骤决策逻辑、状态持久化的客服 Agent<br>• 需要 A/B 测试多个 Agent 版本并隔离运行环境<br>• 实现带文件解析、数据库查询、外部系统回调的复合技能编排<br>• 需实时监听每一步推理、工具调用、错误回滚的调试与可观测性场景 | • 在 Web/APP 中嵌入已上线的智能客服、知识问答、营销助手等应用<br>• 快速对接第三方系统（如 CRM、ERP），通过 `messages` 传入上下文完成任务<br>• 批量管理 Prompt 模板（如运营人员更新话术库）<br>• 异步处理长耗时任务（如报告生成、数据汇总）并轮询结果 |
| **会话与状态管理** | 原生支持 `Session` 生命周期管理（默认 24 小时）、结构化 `Memory Store`（TTL 可控）、事件驱动状态追踪；支持 `session_id` 复用与强制终止 | `session_id` 仅作轻量上下文标识（1 小时无请求自动失效），**不保证状态一致性**；[长期记忆](../concepts/long-term-memory.md)（旧）为独立组件，已标记弃用；新版记忆方案未在 Flow Agent API 中暴露；多轮对话依赖客户端维护 `messages` 数组 |
| **扩展性与定制能力** | 高：支持动态注册 Webhook Skill、自定义 Prompt 模板（Jinja2）、环境级配置覆盖、Vault 凭证注入；可构建完全脱离控制台的 CI/CD 流水线 | 低：应用行为完全由控制台发布版本决定；无法在调用时动态修改工具、记忆策略或执行流程；Prompt 模板可管理但不可在单次调用中覆盖；无 Skill 动态绑定能力 |

---

## 各方案适用场景建议

### ✅ 选择 **Managed Agents API** 当：
- 你需要**从零开始构建一个具备复杂逻辑、多工具协同、状态感知能力的智能体**，而非简单调用已有应用；
- 你要求**环境隔离、版本灰度、细粒度可观测性（如每一步 agent_step 日志）和运行时干预能力（如终止异常会话）**；
- 你的业务涉及**敏感凭证管理（如数据库密码、API Key）**，需通过 `Vault` 安全注入；
- 你正在搭建内部 Agent 平台、低代码编排引擎，或需要将 Agent 能力深度集成至自有 DevOps 体系；
- 你对成本模型有明确预期，且愿意为运行时资源（CPU/内存/存储）付费，换取最大控制权。

### ✅ 选择 **Flow Agent API** 当：
- 你已通过百炼控制台**发布了一个成熟、稳定、经过测试的智能体或工作流应用**，目标是快速将其能力接入业务系统；
- 你的集成场景强调**简单、标准、兼容性好**（如 OpenAI 兼容的 `/v1/responses` 接口）；
- 你需要**批量管理 Prompt 模板**（如运营团队更新 100+ 个客服话术），或为多租户应用配置独立 Workspace；
- 你接受**会话状态由客户端维护**，且无需监听中间执行步骤，只关注最终输出或流式文本片段；
- 你希望最小化运维负担，**不关心底层 Agent 如何运行，只关注“调得通、结果准、费用明”**。

> ⚠️ 注意：二者**不可混用**。例如，不能用 Flow Agent API 调用一个通过 Managed Agents API 创建的 Agent 实例；反之，Managed Agents API 也无法操作控制台发布的 Flow 类应用。它们分别对应百炼平台中两个正交的智能体范式：*可编程 Agent* 与 *可发布应用*。

---

## 技术选型参考（致开发者）

| 你的需求 | 推荐方案 | 理由简述 |
|----------|-----------|-----------|
| “我要做一个能查订单、改地址、发短信的电商客服 Agent，还要支持上传发票 PDF 自动识别” | ✅ Managed Agents API | 需要文件上传（`/v1/files`）、自定义 Webhook Skill（对接订单/短信系统）、结构化 Memory 存储用户会话状态、Jinja2 Prompt 动态渲染 |
| “我们已有控制台发布的‘HR 政策问答机器人’，现在要嵌入钉钉群聊，支持 @ 提问” | ✅ Flow Agent API（DashScope） | 直接调用 `apps/{app_id}/completion`，传入 `messages` 数组即可；无需关心其内部实现；天然支持流式回复适配 IM 场景 |
| “我们需要为 50 家客户部署不同 Prompt 和工具集的专属 Agent，并做 A/B 测试” | ✅ Managed Agents API | 利用 `Environment` 实现客户级隔离；通过 `POST /v1/agents` 批量创建不同配置实例；`status` 查询与事件流便于自动化监控 |
| “运营同学要每周更新 20 个销售话术模板，技术不想每次发版” | ✅ Flow Agent API（OpenAPI） | 使用 `CreatePromptTemplate` / `UpdatePromptTemplate` 等接口，配合阿里云 SDK 实现模板后台管理系统 |
| “我们要做异步报告生成（耗时 5–10 分钟），前端轮询结果，不阻塞用户” | ✅ Flow Agent API（Responses 异步模式） | `background=true` 返回 `task_id`，后续 `GET /tasks/{id}` 获取结果；Managed Agents API 无原生[异步任务](../concepts/asynchronous-task.md)抽象 |
| “我需要在 Agent 执行中实时展示思考链（Thought Process），供 QA 团队审计” | ✅ Managed Agents API | `GET /v1/sessions/{id}/events?stream=true` 提供 `agent_step`、`tool_input`、`tool_output` 等精确事件，粒度远超 Flow 的 `delta` 流 |

---

📌 **最后提醒**：  
- 新项目请优先评估 **Managed Agents API** —— 它代表百炼平台对“智能体即服务（AaaS）”的下一代抽象，能力更完整、演进更活跃；  
- 若已有大量 Flow 类应用沉淀，或团队无 Agent 工程化经验，**Flow Agent API 是更安全、更低门槛的起点**；  
- 两种 API 均需通过百炼控制台申请对应权限（如 `AliyunBailianFullAccess` 或精细化 RAM 策略），请根据实际调用范围配置最小必要权限。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)


