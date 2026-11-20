# Flow Agent 与 OpenAI 兼容 Agent API 对比

本文旨在帮助开发者清晰理解百炼平台中两类核心智能体调用能力的定位差异、技术边界与适用场景，为实际项目中的技术选型提供客观、可落地的决策依据。随着智能体应用从单轮问答向多步推理、工具协同、状态持久化演进，百炼平台同步提供了两种不同抽象层级的 API 路径：**Flow Agent API**（面向已发布应用与组件管理）和**OpenAI 兼容 Agent API**（面向标准化、可编程的智能体构建）。二者并非替代关系，而是服务于不同阶段、不同复杂度的开发需求。

---

## 关键维度对比

| 维度 | Flow Agent API | OpenAI 兼容 Agent API |
|------|----------------|------------------------|
| **设计定位** | 应用交付与组件治理接口：聚焦“调用已上线的智能体/工作流”及“管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等基础组件” | 标准化智能体运行时接口：聚焦“按 OpenAI Agents 协议动态创建、配置并执行具备工具调用能力的智能体” |
| **输入格式** | 支持 `prompt`（字符串）或 `messages`（OpenAI 风格消息数组，含 `role: "system"`/`"user"`/`"assistant"`），二者互斥；支持 `session_id` 恢复上下文 | 严格遵循 OpenAI Agents 规范：`model` + `tools`（function schema 数组）+ `tool_choice` + `messages`（必须含 `role: "user"`）；不接受纯 `prompt` 字符串 |
| **输出格式** | 同步响应返回完整 JSON（含 `output.text`、`output.tool_calls` 等）；支持 `stream=true` [流式输出](../concepts/streaming-output.md)（chunk 为 SSE 格式，含 `delta` 或 `incremental_output` 控制增量内容） | **仅支持同步阻塞响应**：返回完整 `Run` 对象（含 `status`、`steps`、`output`、`tool_calls` 等），`stream=true` 参数被忽略；需主动轮询 `/runs/{run_id}` 获取最终结果 |
| **支持模型** | 不直接绑定模型，由后台应用配置决定；兼容新版 Agent 2.0、旧版 Agent 及工作流应用（底层可使用 Qwen 系列全量模型） | **严格限定**：仅支持 `qwen-plus` 和 `qwen-max`；传入其他模型名（如 `qwen-turbo`）将返回 400 错误 |
| **API 端点** | - 应用调用：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（标准模式）<br>- OpenAI 兼容模式（仅限应用调用）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`<br>- 组件管理（Prompt/记忆）：`POST https://bailian.{regionId}.aliyuncs.com/llm-{workspaceId}/...` | - 创建 Agent：`POST https://dashscope.aliyuncs.com/v1/agents`<br>- 运行 Agent：`POST https://dashscope.aliyuncs.com/v1/agents/{agent_id}/runs`<br>- 查询 Run：`GET https://dashscope.aliyuncs.com/v1/agents/{agent_id}/runs/{run_id}` |
| **认证方式** | - 应用调用：`Authorization: Bearer <API_Key>`（百炼平台 API Key）<br>- 组件类接口（Prompt/记忆）：**AccessKey 签名（ACS3-HMAC-SHA256）**，不支持 Bearer | `Authorization: Bearer <API_Key>`（需具备 `agents:read` 和 `agents:execute` 权限） |
| **会话与状态管理** | - `session_id` 用于恢复云端对话历史，有效期 **1 小时**（无请求即失效）<br>- “[长期记忆](../concepts/long-term-memory.md)（旧）” 提供 `Memory`/`MemoryNode` 两级 CRUD，但明确标注为旧版，**不支持用户画像存储** | - `session_id` 用于复用 session，生命周期 **固定 24 小时**（不可配置）<br>- 内置 session-aware state persistence，自动管理多步推理中间状态；支持 `environment_id` 隔离执行沙箱与权限边界 |
| **工具调用（Tool Calling）** | 支持（通过 `messages` 中 `tool_calls` / `tool_responses` 交互），但需在应用配置中预定义工具集；无运行时动态注册能力 | **原生深度支持**：可在每次 `POST /runs` 时动态传入 `tools` 数组（OpenAI function schema），支持 `tool_choice` 精确控制调用策略；函数名需符合 Python 标识符规则 |
| **计费方式** | 按调用次数 + 输出 token 数计费（与 DashScope 应用网关统一计费模型）；Prompt 模板/记忆等组件管理接口**不计费** | 按 `Run` 执行次数 + 输入/输出总 token 数计费（单次 Run 上限 32768 tokens）；Agent 创建（`POST /agents`）本身不计费 |
| **典型场景** | - 快速集成已上线的客服机器人、审批工作流等业务应用<br>- 在低代码平台中嵌入预置智能体能力<br>- 管理企业级 Prompt 模板库与对话记忆归档 | - 构建需动态组合工具链的 AI 应用（如：查天气 + 订机票 + 发邮件）<br>- 迁移现有 OpenAI Agents SDK 项目至百炼<br>- 需要细粒度控制每步推理、调试 tool 调用逻辑的研发场景 |

---

## 适用场景建议

### ✅ 推荐选用 **Flow Agent API** 当：
- 你已在百炼控制台完成智能体或工作流的可视化编排与发布，目标是**快速调用现成能力**；
- 你需要在应用层统一管理 Prompt 模板（如 A/B 测试不同系统提示词）、或需对对话历史做结构化持久化（如存入自定义记忆节点）；
- 项目对响应延迟敏感，需启用 `stream=true` 实现低延迟[流式输出](../concepts/streaming-output.md)（如实时客服对话）；
- 团队以业务人员或低代码开发者为主，偏好通过 `app_id` 直接对接，避免复杂 agent 生命周期管理。

### ✅ 推荐选用 **OpenAI 兼容 Agent API** 当：
- 你需要**完全掌控智能体的行为逻辑**：动态注册工具、指定 `tool_choice`、逐 step 分析执行轨迹；
- 项目已基于 OpenAI Agents SDK 开发，希望最小成本迁移至百炼（代码只需修改 endpoint 和 API Key）；
- 场景涉及多步骤、强状态依赖的任务（如数据分析 pipeline、跨系统事务协调），需利用内置 session state 与 environment sandbox 保障一致性与安全性；
- 工具函数需注入密钥（vault-backed secrets），且要求参数名与 secret key 严格一致（大小写敏感）。

### ⚠️ 注意规避以下误用：
- 试图用 Flow Agent API 的 `compatible-mode/v1/responses` 端点实现 OpenAI Agents 的完整功能（该端点仅为协议适配，**不支持动态 tools 注册、不支持 run 状态轮询、无 environment 隔离**）；
- 在 OpenAI 兼容 Agent API 中尝试传入 `stream=true` 或期望获得流式响应（服务端强制忽略，必须轮询）；
- 使用 Flow Agent 的组件类接口（如 `CreatePromptTemplate`）时误用 Bearer Token 认证（必须用 AccessKey 签名）；
- 在非华北2（北京）地域调用 Flow Agent 的应用接口（DashScope 网关）而未确认 workspace 映射与 endpoint 合法性。

---

## 技术选型参考总结

| 决策维度 | 优先选择 Flow Agent API | 优先选择 OpenAI 兼容 Agent API |
|----------|--------------------------|----------------------------------|
| **开发成熟度** | 已上线应用 → “开箱即用” | 从零构建智能体 → “代码即配置” |
| **协议兼容性** | DashScope 自有协议（兼容部分 OpenAI message 格式） | 100% 对齐 OpenAI Agents v1 协议语义 |
| **运维复杂度** | 低（无需管理 agent/run 生命周期） | 中（需处理 session 失效、run 轮询、timeout 重试） |
| **扩展灵活性** | 低（工具集需预配置于应用中） | 高（每次 run 可动态声明 tools 与环境） |
| **可观测性** | 基础日志 + `request_id` 追踪 | 完整 `Run` 对象包含每步 `step` 详情、tool 调用耗时、错误上下文 |

> 💡 **一句话选型口诀**：  
> **“调现成的，选 Flow；造灵活的，选 OpenAI 兼容。”**  
> 若项目同时存在两类需求（如：主流程调用预置工作流 + 子任务动态调用工具），可**混合使用**——用 Flow Agent API 调用主应用，在其内部通过 OpenAI 兼容 Agent API 启动子智能体，实现能力分层解耦。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)


