# 智能体开发框架对比：Flow Agent、Managed Agents 与 Sandbox

为帮助开发者在百炼平台上高效选型，本文对三种核心智能体开发支持能力——**Flow Agent API**、**Managed Agents API** 和 **Sandbox API**——进行系统性对比分析。三者定位不同：Flow Agent 侧重**低代码工作流编排与[长期记忆](../concepts/long-term-memory.md)集成**，Managed Agents 聚焦**可编程、有状态、可扩展的生产级智能体全生命周期管理**，而 Sandbox 则提供**底层隔离计算环境**，用于安全执行任意代码或自定义推理逻辑。明确其差异是构建可靠、可维护、可演进智能体系统的前提。

## 关键维度对比

| 维度 | Flow Agent | Managed Agents | Sandbox |
|------|------------|----------------|---------|
| **核心定位** | 工作流驱动的智能体调用与[长期记忆](../concepts/long-term-memory.md)组件管理平台 | 可编程、会话感知、技能可插拔的智能体运行时基础设施 | 隔离、按需、短时存活的轻量级容器化计算沙箱 |
| **输入格式** | • 应用调用类：JSON（含 `input` 字段，结构由 Flow 定义）<br>• 组件类（如 `CreateMemoryNode`）：JSON（`content` 字段限 1–200 字符，仅支持基础符号） | JSON（标准 REST 请求体），支持结构化 `messages` 数组、`session_id`、`environment_id`、`skills` 列表等字段；支持流式请求头（`Accept: text/event-stream`） | JSON（实例配置），含 `template_id`/`image`、`timeout_seconds`、`resources`、`mounts` 等；不处理语义化用户输入，仅传递启动参数与挂载配置 |
| **输出格式** | • 应用调用类：标准 DashScope 响应（含 `output.text`、`request_id`、`usage`）<br>• 组件类：OpenAPI 标准响应（含 `Code`/`Message`，无 `usage` 字段） | JSON（同步响应）或 SSE 流式事件（`event: agent_step` / `event: agent_finish`）；含 `output`、`status`、`events`、`memory_store` 快照等；支持完整 token 使用统计（`usage.input_tokens`/`output_tokens`） | JSON（实例元数据，如 `id`、`status`、`endpoint`、`created_at`）；日志通过独立 `/logs` 接口以 chunked HTTP 流返回；**无模型推理结果封装** |
| **支持模型** | 间接支持：依赖 DashScope 应用网关中已发布的智能体所绑定的模型（如 `qwen-max`），**自身不暴露模型选择接口** | 直接支持：创建 Agent 时通过 `model` 字段指定（如 `"qwen-plus"`），受平台模型白名单约束；支持多模型混用（不同 Agent 实例可配不同模型） | **不直接支持大模型推理**；但可通过预置镜像（如 `llm-inference-gpu`）或自定义 Dockerfile 部署私有模型服务，由用户完全控制模型加载与调用逻辑 |
| **API 端点** | • 应用调用：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`<br>• 组件管理（[长期记忆](../concepts/long-term-memory.md)）：`https://bailian.{regionId}.aliyuncs.com/{workspaceId}/...` | 统一端点：`https://dashscope.aliyuncs.com/api/v1/managed-agents`（所有子资源路径均以此为前缀，如 `/agents`, `/sessions`） | 统一端点：`https://dashscope.aliyuncs.com/api/v1/sandbox/instances`（及 `/templates`, `/instances/{id}/logs` 等） |
| **认证方式** | **双认证体系**：<br>• 应用调用：`Authorization: Bearer <dashscope_api_key>`<br>• 组件管理：阿里云 AccessKey 签名（ACS3-HMAC-SHA256），**不支持 Bearer** | 统一 Bearer [Token](../concepts/token.md) 认证：<br>`Authorization: Bearer <token>`（[Token](../concepts/token.md) 通过百炼平台 OAuth2 或临时凭证获取） | 统一 Bearer [Token](../concepts/token.md) 认证：<br>`Authorization: Bearer <token>`（同 Managed Agents） |
| **计费方式** | • 应用调用类：按调用次数 + 模型 token 用量计费（归属 DashScope 应用计费体系）<br>• 组件管理类（长期记忆）：**当前免费**（文档未提及计费项，属平台基础能力） | 按 Agent 实例运行时长（秒） + 模型 token 用量 + 技能调用次数综合计费；Environment、Skill、Vault 等资源创建不额外计费 | 按实例实际运行时长（秒）计费，与 CPU/GPU 规格强相关；文件挂载（OSS）、网络流量等按阿里云通用产品计费；**与模型无关** |
| **典型场景** | • 快速上线基于可视化 Flow 编排的客服/导购机器人<br>• 需复用已有长期记忆（如产品知识库、用户历史交互摘要）的轻量级应用<br>• 控制台发布后，由业务系统通过 API 触发固定流程 | • 构建具备复杂状态管理（如多轮对话上下文、任务进度跟踪）的智能体<br>• 需动态绑定/解绑技能（如根据用户意图切换 KB 检索、工单创建、支付验证）<br>• 要求细粒度权限隔离（多租户 Environment）、敏感凭证安全托管（Vault） | • 安全执行用户上传的 Python 脚本（如数据清洗、报告生成）<br>• 部署私有微调模型或非百炼原生模型（如 Llama 3、Phi-3）进行推理<br>• 运行需 GPU 加速的自定义算法（如图像生成、语音转写后处理） |

## 各方案适用场景建议

- **选择 Flow Agent 当且仅当**：  
  ✅ 业务逻辑高度结构化、流程固定（如“用户提问 → 检索知识库 → 生成回答 → 记录日志”）；  
  ✅ 团队以低代码/无代码为主，依赖百炼控制台完成 Flow 设计与发布；  
  ✅ 需要快速集成平台提供的长期记忆能力，且记忆内容简单（如 FAQ 条目、产品参数摘要）；  
  ❌ 不适合需要动态决策、技能热插拔、复杂会话状态管理或自定义模型部署的场景。

- **选择 Managed Agents 当且仅当**：  
  ✅ 需要构建生产级、可运维、可监控的智能体服务（如企业级客服中台、AI 助手 SDK 后端）；  
  ✅ 要求完整的会话生命周期管理（`session_id` 隔离、事件流订阅、超时保活）；  
  ✅ 业务涉及多源技能集成（Webhook 调用内部系统、调用百炼内置工具、安全访问 Vault 凭证）；  
  ✅ 开发团队具备较强工程能力，接受基于 RESTful API 的编程模型；  
  ❌ 不适合仅需单次简单调用、或对底层计算环境有特殊定制需求（如特定 Linux 内核模块、CUDA 版本）的场景。

- **选择 Sandbox 当且仅当**：  
  ✅ 核心需求是**安全、隔离、可控的代码执行环境**，而非开箱即用的智能体能力；  
  ✅ 需部署百炼平台未预置的模型、框架或二进制程序（如 PyTorch 自定义算子、Rust 编写的推理服务）；  
  ✅ 任务具有明确起止时间（≤1 小时），且可接受实例销毁后状态清零；  
  ✅ 需要直接操作文件系统、挂载 OSS 数据、或进行网络调试（受限于内网访问策略）；  
  ❌ 不适合构建需要持久化会话状态、长期记忆、自然语言理解/生成抽象能力的智能体——它提供的是“土壤”，而非“植物”。

## 技术选型参考（面向开发者）

| 你的关键需求 | 推荐方案 | 理由简述 |
|--------------|----------|----------|
| “我只想用一个 API 调用已发布的 Flow，不关心底层” | ✅ Flow Agent（应用调用类） | 最简路径，无需管理环境、会话、技能，直连 DashScope 网关 |
| “我要让智能体记住用户上次咨询的订单号，并在本次对话中自动关联” | ✅ Managed Agents（+ Memory Store） | `Memory Store` 支持带 TTL 的键值存储，天然适配会话级上下文；Flow Agent 的长期记忆为全局共享、更新成本高、不支持会话粒度 |
| “我有一套自研的 RAG 引擎，想把它包装成智能体技能供其他 Agent 调用” | ✅ Managed Agents（Skill + Webhook） | Skill 机制专为此设计，支持注册 Webhook URL，由平台统一调度与错误重试 |
| “客户要求我们使用他们私有的 Llama 3 模型，且不能离开其 VPC” | ✅ Sandbox | 可构建专属镜像，在客户 VPC 内部署模型服务，通过 Sandbox 实例暴露 API 端点，再由 Managed Agents 的 Skill 调用 |
| “我需要跑一个耗时 5 分钟的数据分析脚本，结果返回 Excel” | ✅ Sandbox | 短时、计算密集、IO 密集，Sandbox 提供资源隔离与 OSS 挂载，比长期运行 Agent 更经济安全 |
| “我想在 Flow 中嵌入一段 Python 代码做条件判断，但 Flow 编辑器不支持” | ⚠️ 组合方案：Sandbox + Flow Agent | 将 Python 逻辑封装为 Sandbox 实例，Flow 中通过 HTTP 调用其结果，实现低代码与代码能力的混合编排 |

> **重要提醒**：  
> - **不要混淆层级**：Sandbox 是基础设施层，Managed Agents 是智能体平台层，Flow Agent 是应用封装层。三者可组合使用（如 Managed Agents 的 Skill 调用 Sandbox 实例），但不可互相替代。  
> - **关注演进状态**：Flow Agent 的长期记忆文档标注为“（旧）”，新项目建议优先评估 Managed Agents 的 `Memory Store` 是否满足需求；Sandbox 的 WebSocket 日志功能尚未上线，当前仅支持 HTTP chunked 流。  
> - **认证是第一道门槛**：Flow Agent 的双认证体系易出错，务必严格区分 `Bearer`（调用）与 `AccessKey`（管理）；Managed Agents 与 Sandbox 共享统一 Bearer Token，开发体验更一致。  

选型的本质是匹配技术能力与业务抽象层级。从 Flow Agent 的“所见即所得”，到 Managed Agents 的“所编即所运”，再到 Sandbox 的“所控即所为”，百炼平台提供了覆盖全栈智能体开发的弹性能力矩阵。请基于你的团队能力、交付周期、长期维护成本与架构演进规划，做出审慎决策。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [sandbox api](../api/sandbox-api.md)


