# 托管智能体与大模型调用对比

为帮助开发者在百炼平台上高效构建 AI 应用，本文对两类核心能力——**托管智能体（Managed Agents API）** 与 **大模型直调 API（Qwen 系列模型 API）** 进行系统性对比。二者定位不同：前者面向**高阶自主行为建模**，提供开箱即用的 Agent 生命周期管理、状态持久化与安全工具编排能力；后者面向**灵活可控的模型推理层调用**，强调低延迟、细粒度参数控制与多协议兼容性。本对比旨在厘清技术边界，辅助团队基于业务复杂度、运维成本、功能需求与长期演进路径做出理性选型。

## 关键维度对比

| 维度 | 托管智能体（Managed Agents API） | 大模型调用（Qwen API） |
|------|----------------------------------|--------------------------|
| **输入格式** | 结构化会话消息（`POST /v1/sessions/{session_id}/messages`），支持纯文本或带 `metadata` 的 JSON；需先创建 `Agent` 和 `Session`，上下文由平台自动维护 | 标准对话数组 `messages: [{role, content}]`（OpenAI/DashScope）或 `messages` + `system`（Anthropic）；所有上下文需客户端显式传入 |
| **输出格式** | SSE 流式事件（`step_started`, `tool_call`, `message`, `step_finished` 等），含执行轨迹、工具调用详情与最终响应；支持结构化 `message.content` 或 `message.tool_results` | 按协议返回：<br>• OpenAI 兼容：`choices[0].message.content` 或 `delta.content`（流式）<br>• DashScope：`output.text` 或 `output.choices[0].message.content`<br>• Anthropic：`content` 数组（含 `text`/`tool_use` 类型块）；**无内置执行步骤日志** |
| **支持模型** | 仅限平台托管的 `qwen-max`、`qwen-plus`、`qwen-turbo`；不支持 BYOM 或外部模型端点 | 同样支持 `qwen-max`、`qwen-plus`、`qwen-turbo`；但通过 DashScope 接口可扩展接入其他百炼托管模型（如未来新增的 `qwen2-72b`） |
| **API 端点** | 专属资源化端点：<br>• `POST /v1/agents`（创建 Agent）<br>• `POST /v1/sessions`（启动会话）<br>• `POST /v1/sessions/{id}/messages`（发送消息） | 协议标准化端点：<br>• DashScope：`POST /api/v1/services/aigc/text-generation`<br>• OpenAI 兼容：`POST /compatible-mode/v1/chat/completions`<br>• Anthropic 兼容：`POST /anthropic/v1/messages` |
| **计费方式** | 按 **Agent 实例运行时长 + 工具调用次数 + token 消耗** 综合计费；会话空闲超时（默认 30 分钟）后自动释放资源，停止计费；长期 Memory Store 持久化单独计费 | 按 **实际请求的输入/输出 token 总量** 计费（模型级单价）；无运行时长或会话管理费用；工具调用本身不额外计费（但触发的子请求 token 会计入） |
| **状态与记忆** | 内置 `Memory Store`（向量检索+持久化），自动关联会话历史、长期知识与用户偏好；支持跨会话记忆复用 | **无服务端状态管理**；对话历史需客户端完整维护并每次传入；Anthropic Messages 接口支持有限轮次缓存（非持久化），DashScope/OpenAI 完全无状态 |
| **工具调用能力** | 原生深度集成：`Skill` 作为声明式资源注册，Agent 自动规划→调用→解析→反思；支持沙箱环境（Python/Node.js）安全执行代码类工具 | 仅 DashScope 和 Anthropic 接口原生支持 `tools` + `tool_choice`；[OpenAI 兼容接口](../concepts/openai-compatible-api.md)需客户端自行解析 `function_call` 并调用工具，再拼接结果重发；**无沙箱执行环境** |
| **安全与凭证管理** | 提供 `Vault` + `Credential` 机制，敏感凭据动态注入 Skill，避免硬编码；Environment 隔离执行上下文 | 凭据完全由客户端管理（如 API Key 存于后端配置）；工具调用所需密钥需自行注入请求体或 Header，无平台级凭证托管 |
| **典型场景** | • 客户自助服务 Agent（多轮问答+查订单+改地址+发工单）<br>• 数据分析助手（上传文件→理解结构→生成 SQL→执行→可视化）<br>• IT 运维巡检 Agent（调用监控 API + 解析日志 + 自动修复脚本） | • 实时聊天机器人（轻量级客服应答）<br>• 文档摘要/翻译/润色等单步生成任务<br>• 集成至已有系统（如 CRM 插件）做即时内容增强<br>• 需要严格控制采样参数（top_p/repetition_penalty）的创意生成 |

## 适用场景建议

### ✅ 选择 **托管智能体** 当：
- 业务逻辑涉及 **3 步以上多跳推理**（例如：“查我上月账单→对比套餐资费→推荐更优方案→生成办理链接”）；
- 需要 **长期记忆能力**（如记住用户偏好、历史交互、组织知识库）并支持向量检索；
- 工具调用场景复杂，要求 **沙箱安全执行 Python/Node.js 代码**（如数据清洗、图表生成、API 调试）；
- 团队希望 **降低工程复杂度**，避免自行实现状态管理、会话路由、错误恢复、凭证轮转等基础设施；
- 对 **可审计性与可解释性** 有强要求，需完整记录每一步决策依据（`tool_call` 参数、执行结果、反思过程）。

### ✅ 选择 **大模型直调 API** 当：
- 场景简单、低延迟敏感（如毫秒级响应的搜索补全、实时弹幕互动）；
- 已有成熟对话状态管理框架（如自研 Session Store + Redis 缓存），无需平台托管记忆；
- 需要 **极致参数控制**（如精确控制 logprobs、stop tokens、JSON Schema 强约束输出）；
- 技术栈已深度适配 OpenAI/Anthropic 协议，追求 **零改造迁移**；
- 成本敏感且流量高度波动，希望按 token 精确计费，避免 Agent 实例的固定保底开销。

## 技术选型参考（面向开发者）

| 评估项 | 托管智能体 | 大模型直调 |
|--------|-------------|--------------|
| **开发效率** | ⭐⭐⭐⭐☆（声明式配置，减少胶水代码） | ⭐⭐⭐☆☆（需自行封装重试、流式解析、上下文拼接） |
| **运维负担** | ⭐⭐⭐⭐☆（平台托管扩缩容、监控、日志、故障隔离） | ⭐⭐☆☆☆（需自建限流、熔断、配额告警、token 统计） |
| **功能上限** | ⭐⭐⭐⭐☆（内置多步规划、沙箱、记忆、凭证） | ⭐⭐⭐☆☆（依赖客户端能力补足工具链与状态） |
| **灵活性** | ⭐⭐☆☆☆（模型/环境/技能绑定较固定，定制化需提工单） | ⭐⭐⭐⭐☆（任意组合参数、协议、前端渲染逻辑） |
| **学习成本** | ⭐⭐⭐☆☆（需理解 Agent/Session/Memory/Skill 概念模型） | ⭐⭐☆☆☆（标准 LLM API，文档即上手） |
| **生产就绪度** | ⭐⭐⭐⭐☆（内置超时、最大步数、并发限流、凭证安全） | ⭐⭐⭐☆☆（需自行实现健壮性保障） |

> **混合架构提示**：实践中常采用分层策略——使用 **托管智能体** 构建核心业务 Agent（如“财务顾问”），其内部 Skill 可调用 **Qwen 直调 API** 完成特定子任务（如“用 qwen-turbo 快速生成报表摘要”），兼顾能力深度与调度灵活性。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [qwen api reference](../api/qwen-api-reference.md)


