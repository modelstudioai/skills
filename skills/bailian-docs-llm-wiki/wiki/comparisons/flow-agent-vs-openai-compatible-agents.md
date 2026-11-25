# Flow Agent 与 OpenAI 兼容 Agent API 对比

本文旨在帮助开发者在百炼平台内进行智能体（Agent）技术选型时，清晰理解 **Flow Agent API** 与 **OpenAI 兼容 Agent API** 的核心差异、能力边界与适用场景。二者虽同属百炼平台的 Agent 类服务，但设计哲学、抽象层级、集成方式和目标用户存在显著区别：  
- **Flow Agent** 面向**业务流程编排者**，强调**可视化建模 + 确定性执行**，适合需要强逻辑控制、多系统协同、可审计可复用的生产级工作流；  
- **OpenAI 兼容 Agent API** 面向**LLM 应用开发者**，强调**协议兼容 + 快速迁移 + 灵活交互**，适合已有 OpenAI 生态代码、需轻量级工具调用与会话状态管理的对话式智能体场景。  

以下从关键维度展开对比分析，所有信息均基于百炼平台当前（v202409）正式发布能力。

## 关键维度对比

| 维度 | Flow Agent API | OpenAI 兼容 Agent API |
|------|----------------|--------------------------|
| **设计定位** | 流程即服务（Flow-as-a-Service）：以预定义、可发布的 Flow 为单元，强调结构化、可复用、可治理的业务流程 | 协议即接口（Protocol-as-an-API）：以 OpenAI `chat.completions` 兼容接口为契约，强调开发友好、生态平滑、会话级智能体行为 |
| **输入格式** | JSON 对象，严格匹配 Flow 定义中的 `input_schema`（如 `{"query": "订单号 OD2024001..."}`）；不支持消息历史数组 | OpenAI 标准 `messages` 数组（含 `user`/`assistant`/`tool` 角色），支持多轮上下文显式传递（如 `[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]`） |
| **输出格式** | 同步返回完整 `outputs` 对象（JSON），含流程最终结果、各节点执行摘要、错误详情；流式模式（`stream=true`）返回 SSE，每条事件为 `data: {"event":"node_executed","payload":{...}}` | 完全兼容 OpenAI 响应结构：含 `choices[0].message`（含 `tool_calls`）、`usage`、`session_id` 等字段；流式响应为标准 OpenAI SSE 格式（`data: {"id":"...","choices":[{"delta":{"role":"assistant",...}}]}`） |
| **支持模型** | `qwen-max`、`qwen-plus`、`qwen-turbo`（三者均支持） | 仅 `qwen-plus`、`qwen-max`（v202409+ 版本）；`qwen-turbo` 不支持工具调用能力栈 |
| **API 端点** | `POST https://dashscope.aliyuncs.com/api/v1/flows/run` | `POST https://dashscope.aliyuncs.com/compatible-mode/v1/agents/chat/completions` |
| **核心编排能力** | ✅ 内置流程图引擎：顺序、并行、条件分支（if-else）、循环（有限次）、失败重试、人工审核节点<br>❌ 不支持运行时动态决定工具调用（工具选择由节点配置固化） | ✅ 运行时动态工具调用：模型自主决策是否调用工具、调用哪个工具（`tool_choice=auto`）<br>❌ 不支持显式条件分支或并行执行；逻辑需通过 `messages` 历史或工具返回内容间接引导 |
| **状态与上下文** | 上下文仅限单次 Flow 执行生命周期内传递（通过 `inputs` → 节点变量 → `outputs`）；无跨请求会话状态 | 支持 `session_id` 维持长期会话状态（默认 24 小时），自动累积 `messages` 历史、工具执行记录、环境变量；支持跨多次请求的上下文延续 |
| **工具集成方式** | 工具作为“内置节点”在 Flow 编辑器中配置（如 HTTP 请求节点、知识库检索节点），参数通过变量注入；无需函数 schema 定义 | 工具通过 OpenAI 标准 `tools` 数组声明（`type: "function"` + `parameters` JSON Schema），由模型解析并生成 `tool_calls`；支持 Vault 安全凭证注入 |
| **执行环境** | 统一后端执行环境，无用户可控沙箱；工具调用由平台托管服务完成 | 支持指定 `environment_id`，启用隔离沙箱（Python/Shell），工具代码在受控环境中执行，支持自定义依赖与临时文件 |
| **计费方式** | 按 **Flow 执行次数** + **所用模型 Token** 计费（`qwen-turbo` 成本最低，`qwen-max` 最高）；节点内多次模型调用累计 Token | 按 **API 调用次数** + **模型输入/输出 Token** 计费（与 OpenAI 模式一致）；Session 生命周期内多次调用独立计费 |
| **典型场景** | • 客服工单自动分派（判断类型→查知识库→转人工/自动回复）<br>• 多源数据聚合报告（并行调用数据库/API/Excel→清洗→生成 PPT）<br>• 合规审批流程（条件分支：金额>10万→触发风控模型→人工复核） | • 智能客服助手（多轮问答+天气/订单查询工具）<br>• 个人助理（日程管理+邮件发送+网页搜索）<br>• 快速原型验证（复用 OpenAI 示例代码，替换 endpoint 即可运行） |

## 适用场景建议

### 选择 Flow Agent API 当：
- 你的业务逻辑具有**明确、稳定、可图形化表达的步骤与分支**（例如：电商售后流程、金融风控链路）；
- 需要**跨多个异构系统（CRM、ERP、数据库、第三方 API）协调执行**，且对每个环节的输入输出、超时、重试、错误处理有强管控需求；
- 团队包含**非开发角色（如业务分析师、运营）**，需通过低代码界面协作设计、调试、发布流程；
- 要求**全流程可追溯、可审计、可版本化管理**（Flow 有发布历史、灰度开关、执行日志明细）；
- 对成本敏感且流程中大量使用 `qwen-turbo` 进行轻量推理（如文本分类、简单提取）。

### 选择 OpenAI 兼容 Agent API 当：
- 你已拥有基于 OpenAI `chat.completions` + `tools` 的代码库，希望**最小改造迁移到百炼**；
- 应用本质是**对话式智能体**，核心价值在于模型的自主规划（Reasoning）与工具调用（Acting）能力，而非固定流程；
- 需要**维护用户级长会话状态**（如连续多轮任务协作、个性化记忆）；
- 工具逻辑较复杂，需**在隔离沙箱中执行自定义 Python/Shell 脚本**（如数据处理、本地文件操作）；
- 开发团队熟悉 OpenAI 生态，追求**快速迭代、A/B 测试不同提示词与工具组合**。

## 技术选型参考指南

| 选型考量 | Flow Agent API | OpenAI 兼容 Agent API | 建议动作 |
|----------|----------------|--------------------------|-----------|
| **已有 OpenAI 代码，想快速上线？** | ❌ 需重构为 Flow 设计 | ✅ 直接替换 endpoint 和 model 参数 | 优先选 OpenAI 兼容 API |
| **流程需人工介入（如审批、确认）？** | ✅ 原生支持“人工节点”，可对接钉钉/企微通知 | ❌ 无内置人工环节，需应用层兜底实现 | 选 Flow Agent |
| **工具需访问企业内网服务（如内部 API）？** | ✅ 可配置白名单内网代理节点 | ⚠️ 沙箱环境默认不可达内网，需额外申请网络策略 | Flow Agent 更稳妥 |
| **需对单次请求做细粒度超时控制（如某节点≤5秒）？** | ✅ 支持节点级 timeout 配置 | ❌ 仅全局请求 timeout（通过 HTTP client 设置） | Flow Agent 更精确 |
| **希望模型自主决定调用 10+ 个工具中的任意组合？** | ❌ 工具调用由流程图静态绑定 | ✅ `tool_choice=auto` + 动态 `tools` 列表完美支持 | OpenAI 兼容 API 更灵活 |
| **要求每次调用都生成可归档的执行报告（含耗时、Token、节点状态）？** | ✅ 输出含完整执行轨迹（`execution_trace`） | ❌ 仅返回最终 message，需自行记录 `messages` 历史 | Flow Agent 更合规 |

> **重要提醒**：二者并非互斥关系。在复杂系统中，可采用**混合架构**——例如：用 Flow Agent 作为顶层业务编排器（处理路由、权限、审计），在其“工具节点”中调用 OpenAI 兼容 Agent API 实现某个子任务的智能对话（如“生成营销文案”子流程）。这种组合能兼顾流程确定性与模型灵活性。

---  
*最后更新：2024年9月*  
*本文档依据百炼平台 v202409 版本 API 行为编写，具体能力请以控制台实时文档及 OpenAPI Schema 为准。*

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)


