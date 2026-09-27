# 模型部署方式对比：托管Agent、模型推理、模型部署索引

本文旨在帮助开发者清晰理解百炼平台三大核心能力层的定位差异与技术边界：**托管 Agent（Managed Agents）** 侧重于构建具备记忆、工具调用与环境感知的完整 AI 应用；**模型推理（Model High-Speed Inference）** 聚焦于底层大模型的高性能、低延迟服务交付；**模型部署索引（Model Deployment Index）** 则提供面向生产环境的多维度模型部署与资源编排能力。三者并非互斥，而是分层协作的关系——托管 Agent 可调用已部署的推理服务（如 PTU/DTU 模型），而模型推理与部署索引共同构成模型服务能力的基础设施底座。本对比聚焦于**使用目的、技术接口形态与适用阶段**，为架构设计与技术选型提供客观依据。

## 关键维度对比

| 维度 | 托管 Agent（Managed Agents API） | 模型推理（High-Speed Inference） | 模型部署索引（Model Deployment Index） |
|------|----------------------------------|-----------------------------------|------------------------------------------|
| **本质定位** | **AI 应用层抽象**：封装 Agent 生命周期（会话、记忆、技能、环境）的托管服务 | **性能加速通道**：对标准模型 API 的吞吐/延迟优化方案（非独立部署） | **模型服务层编排**：面向生产环境的模型实例化、资源隔离与计费模式管理 |
| **输入格式** | JSON 结构化请求体，含 `input`（用户消息）、`file_ids`（上下文文件）、`session_id`（可选）、`stream`（流式开关）等语义化字段 | 标准 OpenAI/DashScope 兼容格式（`messages`, `model`, `max_tokens` 等），无会话/记忆/技能概念 | 部署创建时为 JSON 配置（如 `input_tpm`, `deploy_spec`）；调用时为标准推理请求（同“模型推理”） |
| **输出格式** | SSE 流式事件（`message`, `tool_call`, `step`, `memory_written`）或 JSON 同步响应，含 `trace_id`、`session_id`、`event_type` 等应用级元数据 | 标准 OpenAI/DashScope 响应（`choices[0].message.content`, `usage`），含 `reasoning_tokens`（Prime）、`cached_tokens`（PTU）等性能指标 | 完全复用模型推理的输出格式；部署 API 返回 `model_code`、`status`、`endpoint` 等服务元信息 |
| **支持模型** | 仅限百炼托管模型：`qwen-max`、`qwen-plus`、`qwen-turbo`（不支持自定义/第三方模型） | 吞吐预留：Qwen3.x、GLM-5.x、DeepSeek-v4、Kimi-K2.6 等；Prime：`glm-5.2-fast-preview`、`wan3.0-video-prime` 等特定加速模型 | PTU：Qwen/DeepSeek/GLM/千问VL 等主流模型；DTU/MU：支持 LoRA/全参微调模型及自定义模型；[Token](../concepts/token.md) 按量：仅 LoRA 微调模型（如 `qwen3-8b-ft-*`） |
| **API 端点** | `/v1/agents`, `/v1/sessions`, `/v1/memory`, `/v1/files`（专属 RESTful 接口） | 复用标准推理端点（如 `/v1/chat/completions`），但需：<br>• 吞吐预留：替换 `model` 为专属 code（`tpm-reserved-xxx`）<br>• Prime：使用专属域名（`{workspace_id}.cn-beijing.maas.aliyuncs.com`） | 部署管理：`/api/v1/deployments`（创建/查询/删除）<br>服务调用：复用标准推理端点（`/v1/chat/completions`），`model` 参数填部署生成的 `model_code` 或 `auto-model-xxxx`（智能路由） |
| **计费方式** | 按 **会话调用次数 + 文件存储 + 记忆容量** 计费（项目配额制），无 TPM/token 显式计量 | 吞吐预留：预付费锁定 TPM 容量（按小时/天计费）；Prime：按量计费（TPS 提升不额外收费，用量计入标准模型账单） | PTU：预付费 TPM 容量；DTU/MU：预付费或后付费（按 TPM 或模型单元数）；[Token](../concepts/token.md) 按量：按实际输入/输出 token 数实时计费；智能路由：按实际执行模型的 token 用量计费 |
| **典型场景** | 构建客服助手、数据分析助理、自动化工作流等需长期记忆、多步骤决策、工具集成的应用 | 高并发在线服务（如 App 后端）、实时内容生成、对首字延迟（TTFT）和整体延迟（E2E）敏感的业务 | 需要稳定 SLA 的企业级 SaaS 服务、私有化模型交付、A/B 测试多版本模型、成本敏感的效果验证与灰度发布 |

## 各方案适用场景建议

### ✅ 选择 **托管 Agent**
- 你的需求是构建一个**完整的 AI 应用**，而非单纯调用模型；
- 必须支持**跨会话记忆**（如记住用户偏好、历史订单）；
- 需要**安全调用外部系统**（数据库、CRM、天气 API），且凭证需加密托管（Vault）；
- 业务逻辑涉及**多步骤自主规划**（如“分析报表 → 生成摘要 → 发送邮件”），需 Agent 自动编排；
- 团队缺乏运维 Agent 运行时（[sandbox](../guides/sandbox.md)、状态管理、事件总线）的能力与意愿。

> ⚠️ 注意：不适用于需要自定义模型、超低延迟（<200ms）或高频批量推理（>100 QPS）的纯文本生成任务。

### ✅ 选择 **模型推理（吞吐预留 / Prime）**
- 你已有一个成熟模型服务，但面临**流量高峰导致延迟飙升或 429 错误**；
- 对**首字延迟（TTFT）或整体响应时间（E2E）有严格 SLA 要求**（如金融风控、实时游戏 NPC）；
- 希望在**不修改现有代码**的前提下，通过更换 `model` 或域名快速获得性能提升；
- 需要**确定性容量保障**（吞吐预留）或**极致性价比的按量加速**（Prime）。

> ⚠️ 注意：这不是一种“部署”，而是对已有模型 API 的性能增强通道；无法提供会话管理、记忆、工具调用等应用层能力。

### ✅ 选择 **模型部署索引**
- 你需要将模型作为**独立、可管理、可计量的服务资产**交付给业务方；
- 要求**物理/逻辑资源隔离**（如避免 A 业务影响 B 业务的推理延迟）；
- 需要**灵活的成本模型**：预付费保底（PTU/DTU）、按需即用（[Token](../concepts/token.md) 按量）、或多模型自动选优（智能路由）；
- 计划进行**模型版本灰度、AB 测试、或私有化部署**（DTU/MU 支持 OSS 导入自定义模型）；
- 服务需满足**企业级可观测性**（细粒度 TPM 监控、缓存命中率、故障自动切换）。

> ⚠️ 注意：部署后仍需通过标准推理 API 调用，其本身不提供应用逻辑封装；若需在此基础上构建 Agent，应将部署生成的 `model_code` 作为托管 Agent 的 `model` 参数传入。

## 技术选型参考指南（面向开发者）

| 你的核心诉求 | 推荐首选方案 | 补充说明 |
|--------------|----------------|-----------|
| “我要做一个能查订单、记会议、发邮件的智能助手” | **托管 Agent** | 直接使用 `/v1/agents` 创建，配置 `skills` 和 `vault` 即可，无需自行实现会话状态机与工具调度器。 |
| “我的 App 用户暴涨，现在 API 延迟从 300ms 升到 2s，经常超时” | **吞吐预留（TPM Reservation）** | 申请 2x 输入 TPM 预留，将 `model` 替换为专属 code，5 分钟内生效，SLA 可保障 99.9% 请求 <800ms。 |
| “我需要跑一个自研的 LoRA 模型做内部测试，只用几天，不想预付费” | **模型部署索引 → Token 按量** | 部署 `qwen3-8b-ft-mytest`，按实际 token 付费，停用即停止计费，适合 PoC 验证。 |
| “我们是 SaaS 厂商，要为每个客户部署独立模型实例，保证资源不抢占” | **模型部署索引 → DTU/MU** | 为客户 A 部署 `dtu-qwen3.8-max-custA`，设置专属 TPM 与 `rpm_limit`，完全隔离。 |
| “我想让模型自动选效果最好、价格最低的那个来回答问题” | **模型部署索引 → 智能路由** | 创建 `auto-model-routing-prod`，配置备选模型集与 `COST_FIRST` 策略，调用时只需指定 `model=auto-model-xxxx`。 |
| “我已有托管 Agent，但发现它调用的 `qwen-plus` 响应太慢，想加速” | **组合使用：托管 Agent + 模型部署索引** | 先用模型部署索引为 `qwen-plus` 创建 PTU 服务（如 `ptu-qwen-plus-highspeed`），再在托管 Agent 创建时，将 `model` 设为该 `model_code`。 |

> 💡 **关键原则**：  
> - **分层解耦**：Agent 层负责“做什么”（What），部署层负责“怎么做快/稳/省”（How）；  
> - **避免重复建设**：勿用 DTU 部署一个模型再手动写代码实现 Agent 功能——直接用托管 Agent 调用该 DTU 模型；  
> - **成本透明优先**：Token 按量适合验证，PTU/DTU 适合长期稳定服务，Prime 适合突发流量缓冲；  
> - **安全合规兜底**：涉及敏感数据时，托管 Agent 的 `Environment` 隔离 + `Vault` 凭证加密，比直连第三方 API 更可控。  

如需进一步评估具体场景的架构方案，可参考《百炼生产环境部署最佳实践》或联系技术支持获取定制化建议。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment index](../guides/model-deployment-index.md)


