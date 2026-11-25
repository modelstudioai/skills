# 智能体 API 方案对比：托管 Agent、Flow Agent 与 OpenAI 兼容版

为帮助开发者在百炼平台上高效选型，本文系统对比三种主流智能体 API 方案：**托管 Agent（Managed Agents API）**、**Flow Agent（Flow-based Agent API）** 与 **OpenAI 兼容版 Agents API**。三者均面向生产级 AI 应用构建，但在抽象层级、控制粒度、集成方式和适用范式上存在显著差异。本对比聚焦实际开发体验与工程落地约束，不涉及底层模型性能评测，旨在为技术决策提供清晰、可操作的参考依据。

---

## 关键维度对比

| 维度 | 托管 Agent（Managed Agents API） | Flow Agent（Flow-based Agent API） | OpenAI 兼容版 Agents API |
|------|--------------------------------|-------------------------------------|---------------------------|
| **核心定位** | 开箱即用的“黑盒智能体服务”：封装状态管理、记忆、工具编排，以 `Agent`/`Session` 为资源单位统一调度 | “可视化流程引擎”：将智能体行为显式建模为有向图（DAG），支持多节点协同与人工干预 | “协议平移层”：严格对齐 OpenAI Agents API 规范（路径、请求/响应结构、错误格式），降低迁移成本 |
| **输入格式** | JSON 对象，固定结构 `{ "text": "用户输入文本" }`；不支持多模态；文件需预上传获取 `file_id` 后引用 | 强类型 JSON Schema 校验的 `inputs` 对象（如 `{"query": "北京天气", "location_id": 123}`）；字段名与类型必须与流程定义的 `input_schema` 完全匹配 | 兼容 OpenAI 标准格式：`messages` 数组（含 `role`/`content`/`tool_calls` 等）、`tools` 列表（OpenAI Tool Schema）、`tool_choice` 等；支持 `text` 或 `content` 多模态数组（当前仅文本生效） |
| **输出格式** | 同步：完整 JSON 响应，含 `output.text`、`tool_calls`、`session_id`、`memory_store_id`；流式：SSE 事件流（`event: message`, `data: {...}`） | 同步：标准 JSON，含 `status`、`output`（严格匹配 `output_schema` 的结构化对象）、`trace_id`；不支持原生 SSE 流式，但可通过 `enable_tracing=true` 获取分步执行快照 | 同步：OpenAI 兼容格式（`{ "id": "...", "object": "thread.message", "content": [...] }`）；流式：标准 OpenAI SSE（`event: thread.message.delta`, `data: {...}`），与官方 SDK 无缝对接 |
| **支持模型** | `qwen-max`、`qwen-plus`、`qwen-turbo`（仅限百炼托管模型） | `qwen-max`、`qwen-plus`、`qwen-turbo`（仅限百炼托管模型） | `qwen-plus`、`qwen-max`（仅限百炼托管模型；`qwen-turbo` 不支持） |
| **API 端点（典型）** | `POST /v1/agents/{agent_id}/sessions`<br>（创建 Agent → 启动 Session → 发送消息） | `POST /v1/flows/{flow_id}/run`<br>（单次调用即触发完整流程执行） | `POST /v1/agents/{agent_id}/sessions` + `POST /v1/sessions/{session_id}/messages`<br>（遵循 OpenAI 分步交互范式） |
| **计费方式** | 按 **Session 调用次数** + **[Token](../concepts/token.md) 消耗量** 计费（含输入/输出/[工具调用](../concepts/tool-calling.md)上下文）；Memory Store 持久化按存储时长与容量计费 | 按 **流程执行次数** + **总 [Token](../concepts/token.md) 消耗量**（所有节点累计）计费；`enable_tracing=true` 时额外收取轨迹存储费用 | 按 **Message 调用次数** + **[Token](../concepts/token.md) 消耗量** 计费（与 OpenAI 计费模型一致）；Session 生命周期内多次 `messages` 调用共享同一计费上下文 |
| **长期记忆** | ✅ 内置 Memory Store，自动绑定 Session，跨会话持久化（TTL 可配） | ✅ 通过专用 `memory_node` 接入统一 memory 模块（需显式配置） | ✅ 支持 `memory` 配置项，Session 级别自动维护上下文，兼容 Vault 知识片段注入 |
| **[工具调用](../concepts/tool-calling.md)** | ✅ Skills 插件机制：注册自定义工具，运行时动态启用/禁用；支持异步 Webhook 回调 | ✅ HTTP 工具节点：声明式调用外部 API；支持条件分支路由至不同工具；需域名白名单备案 | ✅ OpenAI Tool Calling Schema：完全兼容 `function`/`code_interpreter` 类型；工具需在 Vault 中注册并授权 |
| **典型场景** | 快速上线客服对话机器人、个人助理、知识问答 Bot；强调开箱即用与会话连续性 | 复杂业务流程自动化：工单分派+审批+通知闭环、多源数据聚合分析、合规性人机协同审核 | 现有 OpenAI 生态项目迁移（如 LangChain、LlamaIndex 应用）、需要复用 OpenAI 客户端 SDK 的团队、追求接口标准化与跨平台可移植性 |

---

## 适用场景建议

### ✅ 选择 **托管 Agent（Managed Agents API）** 当：
- 你希望**最小化开发与运维负担**，聚焦业务逻辑而非 Agent 底层调度；
- 应用以**自然语言多轮对话**为核心（如客服、教育陪练、虚拟助手），且对上下文连贯性、长期记忆有强需求；
- 需要快速验证 MVP，或团队缺乏复杂流程编排经验；
- 你接受百炼平台对模型、环境、工具的统一管控，无需深度定制推理链路。

### ✅ 选择 **Flow Agent（Flow-based Agent API）** 当：
- 你的业务逻辑天然具备**明确步骤、条件分支与人工介入点**（如“用户投诉→自动分类→高危升级→人工审核→生成报告→邮件通知”）；
- 需要**可视化调试与灰度发布能力**，或要求每个环节输入/输出可审计、可校验；
- 多个异构系统（数据库、CRM、内部 API）需被编排进同一智能工作流；
- 你已具备流程图设计能力，或团队习惯使用低代码/可视化工具构建业务逻辑。

### ✅ 选择 **OpenAI 兼容版 Agents API** 当：
- 你正在**将现有基于 OpenAI Agents 的应用迁移到百炼平台**，希望零改造或极小改造（如仅修改 `base_url` 和 API Key）；
- 团队已深度使用 LangChain、LlamaIndex、OpenAI Python SDK 等生态工具，依赖其 Agent 抽象（`AgentExecutor`、`create_openai_tools_agent`）；
- 项目对**接口标准化、文档一致性、社区工具链兼容性**有硬性要求；
- 你愿意为协议兼容性接受一定功能限制（如暂不支持 `temperature` 调优、`qwen-turbo` 不可用）。

---

## 技术选型参考指南（面向开发者）

| 你的关键诉求 | 推荐方案 | 理由说明 |
|--------------|----------|----------|
| **“我要今天就跑通一个能记住上次聊天内容的问答机器人”** | 托管 Agent | 创建 Agent 仅需 3 行 JSON 配置，Session 自动绑定 Memory，5 分钟完成端到端联调。 |
| **“我需要把客户咨询自动分派给销售/技术支持，并在超时未响应时触发升级流程”** | Flow Agent | 条件判断节点（if-else）、并行节点（fork/join）、人工审核节点、超时控制（`timeout`/`node_timeout`）全部原生支持，流程图一目了然。 |
| **“我们用 LangChain 构建了智能投研助手，现在要切换到百炼，但不想重写 Agent 编排代码”** | OpenAI 兼容版 | 直接替换 `openai.OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")`，其余代码（包括 `tools` 定义、`AgentExecutor` 调用）几乎无需修改。 |
| **“我需要精细控制每个 LLM 调用的采样参数（temperature/top_p）”** | ❌ 三者均不支持 | 当前所有方案均采用平台固定解码策略保障确定性；如需动态采样，请使用百炼基础 `chat/completions` API 自行构建 Agent。 |
| **“我要接入自己的私有模型或非 Qwen 系列模型”** | ❌ 三者均不支持 | 百炼当前所有 Agent 方案仅开放 `qwen-*` 系列托管模型；自定义模型需通过 `chat/completions` 或 `functions` API 手动集成。 |
| **“我需要处理图片/PDF 等多模态输入”** | ❌ 三者当前均不支持（文本-only） | 文件需预上传为 `file_id` 后在文本中引用描述；原生多模态（`content` 数组含 `image_url`）暂未开放。 |

> **重要提醒**：  
> - 所有方案均**强制使用百炼统一认证体系（Bearer Token）**，权限需在控制台精确授予（如 `agents:read`、`flows:execute`）。  
> - **速率限制与并发数**是高频瓶颈点：托管 Agent 单 Agent 并发 Session ≤ 100，Flow Agent 单次执行最大耗时 600 秒，OpenAI 兼容版 Session 生命周期严格限定为 24 小时且不可跨地域。企业级需求请提前申请配额提升。  
> - **错误处理必须遵循各自规范**：托管 Agent 返回 `X-RateLimit-Remaining` 头；Flow Agent 使用 `code: INVALID_INPUT` 等自定义码；OpenAI 兼容版返回 `error.type`（如 `"invalid_request_error"`），切勿混用解析逻辑。

---  
*最后更新：2024年6月 | 文档版本：v2.4*

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)


