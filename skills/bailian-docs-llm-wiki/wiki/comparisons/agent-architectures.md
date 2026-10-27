# 智能体架构方案对比：Flow Agent、Managed Agents 与 Sandbox

为帮助开发者在百炼平台上高效选型，本文系统对比三种核心智能体架构方案：**Flow Agent**（面向工作流编排与组件化记忆管理）、**Managed Agents**（面向开箱即用、全托管的自主智能体服务）与 **Sandbox**（面向安全隔离、可编程执行环境的底层沙箱能力）。三者定位不同、能力正交，适用于从低代码集成到高定制化AI应用开发的完整技术光谱。本对比基于当前（2024年Q3）百炼平台正式发布的 API 规范与运行约束，聚焦实际工程落地的关键维度。

## 关键维度对比

| 维度 | Flow Agent | Managed Agents | Sandbox |
|------|------------|----------------|---------|
| **核心定位** | 工作流驱动的智能体调用 + 长期记忆组件管理（*组件级能力*） | 全托管、带状态、可扩展的自主智能体服务（*服务级能力*） | 安全隔离、可编程的通用计算环境（*基础设施级能力*） |
| **输入格式** | • 应用调用：`POST /{app_id}`，Body 为任意 JSON 或纯文本<br>• 记忆管理：`POST /memories`，需严格结构化字段（如 `workspaceId`, `memoryId`） | `POST /v1/agents/{agent_id}/chat`，Body 必须含 `"input": "string"` 字段；支持 `files` 数组（文件 ID 列表）、`tools`（启用技能列表） | • 实例创建：JSON 描述资源配置、模版 ID、挂载项等<br>• 运行时交互：通过 `/connect` 获取 token 后，使用 WebSocket 或 HTTP POST `/execute` 发送命令/代码（如 Python 脚本、Shell 命令） |
| **输出格式** | • 应用调用：标准 JSON 响应（含 `output`, `request_id`）<br>• 记忆管理：RESTful CRUD 响应（如 `GetMemory` 返回 memory 对象） | 流式 Server-Sent Events（SSE）或完整 JSON；含 `event` 类型字段（`"message"`, `"tool_use"`, `"error"`, `"file"`），需按事件协议解析 | • 控制面：标准 REST JSON（如创建实例返回 `sandbox_id`, `status`, `endpoint`）<br>• 数据面：执行结果为结构化 JSON（含 `stdout`, `stderr`, `exitCode`, `files` 等） |
| **支持模型** | • 应用调用：不限定模型，取决于已发布的智能体所绑定的模型<br>• 记忆管理：不涉及模型推理 | 仅限百炼托管模型：`qwen-max`、`qwen-plus`、`qwen-turbo`（暂不支持 `qwen2.5-*` 等新系列） | **不提供模型推理能力**；需在沙箱内自行调用模型 API（如 DashScope SDK）或加载本地模型 |
| **API 端点与鉴权** | • 应用调用：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/{app_id}`，`Authorization: Bearer <api-key>`<br>• 记忆管理：阿里云 OpenAPI（如 `https://bailian.cn-shanghai.aliyuncs.com`），**必须使用 AccessKey 签名（ACS3-HMAC-SHA256）** | `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/agents/{agent_id}/chat`，`Authorization: Bearer <access_token>`（OAuth2 Token） | `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox/...`，`Authorization: Bearer <api-key>`（百炼 API Key） |
| **计费方式** | • 应用调用：按调用次数 + 模型 Token 消耗计费（同普通模型 API）<br>• 记忆管理：**长期记忆组件目前免费**（但属维护期功能，不推荐新项目依赖） | 按 Agent 实例运行时长（秒） + 模型 Token 消耗 + 文件存储量（GB·天）综合计费；会话空闲超时后自动释放资源以控成本 | 按沙箱实例运行时长（秒）计费；CPU/内存规格影响单价；文件存储按容量与时长计费（30 天有效期） |
| **典型场景** | • 业务系统集成已发布的工作流应用（如客服工单分派）<br>• 需要手动管理结构化用户记忆片段（如历史订单摘要节点）的轻量级场景（*注意：该能力已标注为“旧”，不建议新项目采用*） | • 构建多轮对话、工具调用、带记忆的 AI 助手（如销售顾问、IT 支持机器人）<br>• 快速上线具备 Skill 编排、凭证安全注入（Vault）、Webhook 回调能力的生产级 Agent | • 代码解释器类应用（运行用户提交的 Python 分析脚本）<br>• 浏览器自动化（如网页数据抓取、表单填写）<br>• [模型微调](../concepts/model-fine-tuning.md)/评估 Pipeline 中的安全代码执行环节 |

## 适用场景建议

- **选择 Flow Agent 当且仅当**：  
  ✅ 你已有在百炼控制台发布的成熟工作流应用，只需在业务系统中调用它；  
  ✅ 你明确需要对**极少量、高度结构化的长期记忆片段**进行细粒度 CRUD 操作（如为 VIP 用户单独维护一个“偏好标签”节点）；  
  ❌ **不建议用于新项目**：其长期记忆组件已进入维护期，文档明确提示“不支持用户画像管理”，且存在 1 秒限流、无幂等性等工程约束，扩展性与稳定性不足。

- **选择 Managed Agents 当且仅当**：  
  ✅ 你需要快速构建一个**开箱即用、自带会话状态、记忆、工具链和安全上下文**的智能体，且接受平台对模型、运行时的统一管控；  
  ✅ 你的场景强调**端到端可观测性**（如审计每一步 tool use）、**企业级安全**（Vault 注入凭证、Skill 权限隔离）、**低运维负担**（自动扩缩容、故障恢复）；  
  ❌ 不适合：需深度定制模型推理逻辑、要求非 Qwen 系列模型、或需在 Agent 内部执行不受控的任意系统命令。

- **选择 Sandbox 当且仅当**：  
  ✅ 你的核心需求是**安全、隔离、可控的代码执行环境**，而非预置的智能体逻辑；  
  ✅ 你需要运行**未经审核的用户代码**（如 Jupyter Notebook 单元格）、**调用外部网络服务**（开启 `allow_internet_access`）、或**加载自定义二进制依赖**（通过挂载 `.whl` 或编译产物）；  
  ❌ 不适合：直接构建对话式 AI 应用（需自行实现 LLM 调用、RAG、Tool Calling 等全套逻辑）；或对延迟极度敏感（沙箱启动有数百毫秒冷启开销）。

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| “我有一个现成的百炼工作流，想在 ERP 系统里一键调用它” | ✅ Flow Agent（应用调用部分） | 最轻量、最直接，无需改造现有资产，API 简洁，Token 计费透明。 |
| “我要做一个能查数据库、读 Excel、发邮件的销售助手，希望一周内上线，团队无 infra 经验” | ✅ Managed Agents | 全托管：内置 Memory Store 自动维护对话历史，Skill 系统封装数据库/邮件等能力，Vault 解决密码安全，OAuth2 鉴权符合企业 SSO 要求。 |
| “我要做一个 AI 编程助手，允许用户粘贴 Python 代码并安全执行，显示图表和错误堆栈” | ✅ Sandbox | 唯一满足代码沙箱化执行、文件 I/O（上传 `.py`/`.csv`）、图形渲染（`matplotlib` 输出 PNG）、网络访问（`pip install`）等硬性安全要求的方案。 |
| “我想用 Qwen2.5-72B 做 RAG，自己写召回+重排+LLM 调用逻辑，并精细控制每个 Token 的生成” | ❌ 三者均不直接适用 → 建议：**直接调用 DashScope 模型 API + 自建向量库 + 百炼 Knowledge Base** | Flow Agent 和 Managed Agents 模型受限；Sandbox 需自行部署大模型（显存/延迟不可控）。此场景应绕过智能体抽象层，直连基础模型能力。 |
| “我需要为每个用户保存完整的对话历史、用户画像、偏好设置，并做复杂关联查询” | ⚠️ **不推荐任一方案** → 建议：**使用百炼 Knowledge Base + 自建业务数据库** | Flow Agent 记忆组件能力弱且已过时；Managed Agents Memory Store 仅为会话级缓存（默认 100 条），非持久化用户档案；Sandbox 无内置存储。用户数据应由业务系统自主管理。 |

> **重要提醒**：  
> - **不要混用鉴权方式**：Flow Agent 的组件管理接口（OpenAPI）与 Managed Agents / Sandbox 的 Bearer Token 接口**绝不兼容**，错误鉴权将导致 `401 Unauthorized`；  
> - **地域强约束**：Sandbox 与 Managed Agents 当前**仅支持 `cn-beijing` 地域**，Flow Agent 应用调用也需匹配 workspace 所在地域；  
> - **演进趋势**：百炼平台正推动能力收敛——Managed Agents 是当前主推的智能体服务形态；Flow Agent 的组件能力逐步被 Managed Agents 的 `memory_config` 和控制台功能替代；Sandbox 作为底层基座，将持续增强与 Managed Agents 的集成（如未来支持 Skill 直接调度沙箱）。新项目请优先评估 Managed Agents。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [sandbox api](../api/sandbox-api.md)


