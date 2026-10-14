# 智能体相关 API 对比：托管智能体、流程智能体与世界模型

为帮助开发者在百炼平台中高效选型，本文对三类面向不同范式的智能体 API 进行系统性对比分析。随着智能体技术从“单次调用”向“有状态协作”“多步编排”和“环境化推演”演进，百炼平台提供了分层能力支持：**托管智能体（Managed Agents）** 聚焦可编程 Agent 的全生命周期治理；**流程智能体（Flow Agent）** 专注预定义工作流的确定性执行；**世界模型（World Model）** 则面向动态叙事与多模态环境建模。本对比旨在厘清三者在技术定位、能力边界与工程适配性上的本质差异，辅助团队基于业务目标、控制粒度、状态需求与领域特性做出理性技术决策。

## 关键维度对比

| 维度 | 托管智能体（Managed Agents API） | 流程智能体（Flow Agent API） | 世界模型（World Model API） |
|------|----------------------------------|------------------------------|-----------------------------|
| **核心定位** | 可编程智能体的运行时基础设施（Agent as a Service） | 预编排、可复用的多步骤工作流服务（Workflow as a Service） | 动态世界状态建模与因果推演引擎（World Simulation as a Service） |
| **输入格式** | `Session` 级消息流（含 `user_message`, `files`, `session_id`）；支持结构化 `memory_store` 初始化 | 键值对形式的 `inputs` 对象 + `app_id`；支持 `memory_id` 关联长期记忆 | JSON 格式 `scene_state`（描述角色/物品/环境状态） + 文本 `prompt` + 显式 `model` 选择（`adventure`/`directing`/`acting`） |
| **输出格式** | SSE 流式事件（`agent_step`, `tool_call`, `agent_finish`）+ 结构化 `final_output`；支持调试模式返回完整推理链 | 同步 JSON 响应（含 `output`, `trace`, `status`）；启用 `stream=true` 时为 SSE 流（节点级执行事件） | 同步 JSON 响应（含 `result`, `next_scene_state`, `reasoning_trace`（当 `return_trace=true`））；**不支持流式响应** |
| **支持模型** | **不限定模型**：用户自主指定兼容模型（如 `qwen-plus`, `qwen-max`），由 Agent 配置驱动 | **仅限专用架构**：强制使用百炼自研 `flow-agent-v1` 模型，不接受通用 LLM 替换 | **按任务类型划分**：`adventure`（剧情推演）、`directing`（多角色调度）、`acting`（动作-情绪-台词联合生成，需白名单授权） |
| **API 端点示例** | `POST /v1/agents`（创建）<br>`POST /v1/sessions/{session_id}/messages`（交互）<br>`GET /v1/environments/{env_id}`（环境查询） | `POST /v1/flow_agent/applications/{app_id}/call`（主调用入口） | `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`（统一入口） |
| **认证方式** | Bearer [Token](../concepts/token.md)（租户级 Access [Token](../concepts/token.md)） | Bearer [Token](../concepts/token.md)（应用级 API Key） | Bearer Token（模型服务级 API Key） |
| **状态管理** | ✅ 原生支持：<br>• `Session` 级有状态交互（24h 自动清理）<br>• `Memory Store`（TTL 可控的键值存储）<br>• `Environment` 隔离（多版本/多租户） | ⚠️ 有限支持：<br>• 通过 `memory_id` 复用外部记忆服务<br>• **无内置 Session 或环境隔离**，状态需外部维护 | ❌ 无状态设计：<br>• 每次请求必须显式传入完整 `scene_state`<br>• 无会话概念，无自动状态持久化或跨请求上下文继承 |
| **扩展性机制** | ✅ `Skill` 注册（仅 Webhook 类型）<br>✅ `Vault` 安全凭证管理<br>✅ `File` API（支持 PDF/CSV/JSON 等） | ✅ 内置工具自动选择与重试（不可禁用）<br>❌ 不支持自定义技能注册或外部工具绑定 | ❌ 无扩展接口：<br>• 工具能力内置于各子模型中（如 Adventure 的机关触发、Directing 的镜头切换）<br>• 不开放自定义动作或规则注入 |
| **计费方式** | 按 **Agent 实例运行时长** + **Session 消息量** + **文件处理量** 计费；环境、内存、技能调用独立计量 | 按 **单次 Flow 调用次数** 计费；`stream` 模式不额外计费；超时/失败调用仍计费 | 按 **单次模型调用次数** 计费；`adventure`/`directing`/`acting` 分属不同计费单元；`acting` 为邀测专属资费 |
| **典型场景** | • 需长期记忆与多轮对话的客服助手<br>• 需权限隔离与灰度发布的企业内部 Agent<br>• 需集成私有 API 和敏感数据的自动化工作流代理 | • 表单审核→工单创建→通知发送的标准 SOP<br>• 数据清洗→异常检测→报告生成的 ETL 流程<br>• 多条件分支的贷款审批决策链 | • 游戏中的 NPC 行为实时推演与剧情分支生成<br>• 虚拟制片中导演指令到分镜脚本的自动转化<br>• 交互式小说中环境状态演化与角色反应生成 |

## 各方案适用场景建议

### ✅ 推荐选择 **托管智能体（Managed Agents API）** 当：
- 你需要构建**具备记忆、会话、环境隔离与技能生态**的生产级智能体；
- 业务逻辑复杂且需**细粒度控制 Agent 生命周期**（如启动/暂停/终止/回滚）；
- 必须集成**自有后端服务（Webhook）** 并保障凭证安全（`Vault`）；
- 场景涉及**多文件解析（PDF/CSV）** 或需要结构化记忆（如用户偏好、历史订单）；
- 团队具备较强工程能力，愿承担 Session 管理、SSE 解析、错误重试等客户端开发成本。

### ✅ 推荐选择 **流程智能体（Flow Agent API）** 当：
- 你已将业务逻辑抽象为**稳定、可复用、低变更频次的工作流**（如审批流、数据处理链）；
- 追求**开箱即用的确定性执行**，无需自行实现工具路由、重试策略或状态同步；
- 输入输出结构清晰，**无需长期会话上下文**，每次调用可视为独立事务；
- 团队希望快速上线、低运维负担，且能接受平台对执行过程的黑盒封装；
- 需要轻量级跨会话状态复用（通过 `memory_id` 关联统一记忆服务）。

### ✅ 推荐选择 **世界模型（World Model API）** 当：
- 你的应用本质是**动态环境模拟与因果推演**（非通用问答或任务执行）；
- 领域强依赖**空间关系、角色状态、时间演进与多模态反馈**（如游戏、影视、教育仿真）；
- 你能精确建模并序列化 `scene_state`（JSON Schema 严格约束），且接受**每次请求全量传入**；
- 需要专业级叙事能力（Adventure）、镜头语言生成（Directing）或角色表演合成（Acting）；
- 项目处于原型验证或垂直领域深度定制阶段，可配合白名单申请高级模型权限。

## 技术选型参考指南（面向开发者）

| 选型考量因素 | 托管智能体 | 流程智能体 | 世界模型 | 建议动作 |
|--------------|------------|------------|----------|----------|
| **是否需要自定义大模型？** | ✅ 支持任意兼容模型（`qwen-*` 系列） | ❌ 仅限 `flow-agent-v1` | ✅ 按任务选子模型（非通用 LLM） | 若需微调/私有模型 → 选托管智能体 |
| **是否要求会话级状态保持？** | ✅ 原生 `Session` + `Memory Store` | ⚠️ 仅通过 `memory_id` 外部关联 | ❌ 完全无状态，需手动维护 `scene_state` | 若需多轮自然对话 → 优先托管智能体；若仅需跨调用轻量记忆 → 流程智能体 |
| **是否需集成自有系统？** | ✅ Webhook Skill + Vault 凭证管理 | ❌ 仅支持平台内置工具（自动选择） | ❌ 无扩展能力，纯模型服务 | 若需调用企业 ERP/CRM → 必选托管智能体 |
| **是否追求零配置快速上线？** | ❌ 需创建 Environment/Skill/Agent 多步初始化 | ✅ 控制台发布 Flow App 后，1 个 API 即可调用 | ✅ 统一端点 + 明确参数，5 分钟可跑通 demo | 若 MVP 验证或低代码场景 → 选流程智能体或世界模型 |
| **是否处理非文本数据？** | ✅ 支持 PDF/CSV/JSON 文件上传与解析 | ❌ 仅支持文本输入（≤32KB） | ⚠️ `scene_state` 支持结构化数据，但**不直接处理原始文件**（需前置解析） | 若需文档理解 → 托管智能体；若已结构化 → 三者皆可，按语义匹配选 |
| **是否涉及三维/时空/角色建模？** | ❌ 无原生支持 | ❌ 无原生支持 | ✅ `scene_state` 专为角色、位置、物品、情绪等建模设计 | 游戏/影视/AI 教育 → 世界模型是唯一正解 |

> **重要提醒**：  
> - **不要混合滥用**：托管智能体 ≠ 流程智能体的“高级版”，二者范式不同——前者是 *Agent 运行时*，后者是 *Workflow 编排器*。强行用托管智能体实现固定流程，将增加不必要的运维复杂度；反之，用流程智能体实现长周期对话，将丧失状态一致性。  
> - **世界模型不是通用 LLM 接口**：它不回答“今天天气如何”，而是推演“当主角踏入密室，门锁解除后，守卫巡逻路径将如何变化”。请严格对照 `scene_state` Schema 设计输入。  
> - **计费敏感场景请实测**：托管智能体的 Session 时长计费、流程智能体的失败调用计费、世界模型的 `acting` 高单价，均需在压测中验证成本模型。  

如需进一步评估，建议：  
1. 使用 [托管智能体 Quickstart](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 完成一个带 Memory 的客服 Demo；  
2. 在控制台创建一个三节点 Flow（输入→调用知识库→格式化输出），测试其稳定性；  
3. 调用 `adventure` 模型，传入简单 `scene_state`（如 `{"characters":[{"id":"player","x":0,"y":0}]}`）和 `prompt`（如 `"向右移动"`），观察 `next_scene_state` 演化。  
通过三者最小可行实验，可最真实地锚定技术选型。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)
- [world model api reference](../api/world-model-api-reference.md)


