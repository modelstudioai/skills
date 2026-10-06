# 智能体构建范式对比：应用组件、托管智能体与技能

为帮助开发者在百炼平台上高效选型，本文系统对比三种主流智能体构建范式：**应用组件（Application Component）**、**托管智能体（Managed Agents）** 与 **技能（Skill）**。三者定位不同——应用组件面向“快速集成高阶对话能力”，托管智能体聚焦“构建具备记忆与自主性的生产级 Agent”，而技能则专精于“零代码扩展专业任务处理能力”。本对比基于当前稳定版本（v2023-12-29 及 Managed Agents v1），覆盖核心工程维度，旨在为技术决策提供客观、可落地的参考依据。

## 关键维度对比

| 维度 | 应用组件（Application Component） | 托管智能体（Managed Agents） | 技能（Skill） |
|------|----------------------------------|------------------------------|--------------|
| **本质定位** | 封装模型推理+RAG+工具调用的**标准化对话 API**，类“增强版大模型接口” | 提供环境、会话、记忆、技能编排等全生命周期管理的**托管式 Agent 运行时平台** | 可插拔、语义驱动的**原子化任务执行单元**，专注文件/数据处理等具体操作 |
| **输入格式** | `messages` 数组（标准 OpenAI-style 格式），支持 `system`/`user`/`assistant` 角色；可选传入 `tools` 定义数组 | `messages` 数组（同上）；额外支持显式 `session_id`、`files`（引用已上传文件 ID）、`max_steps` 等会话控制参数 | **无直接 API 输入**；通过用户自然语言指令 + 附件（如 `.xlsx`, `.pdf`）触发；由智能体根据 `description` 语义匹配调用 |
| **输出格式** | JSON 响应（非流式）或 SSE 流式响应（含 `delta.content` 和 `delta.tool_calls`）；工具调用结果内联返回 | JSON 响应或 SSE 流式响应；支持事件流订阅（`/events`），可接收 `tool_call_started`、`memory_updated` 等细粒度事件 | **仅输出结构化文件**（如 `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`）；不返回文本流或 JSON 片段；结果需下载或作为后续步骤输入 |
| **支持模型** | `qwen-max`、`qwen-plus`、`qwen-turbo`（默认 `qwen-turbo`）；**不支持 `qwen-vl` / `qwen-audio`** | `qwen-max`、`qwen-plus`、`qwen-turbo`；**仅限百炼托管模型，不支持第三方或自定义权重** | **不直接绑定模型**；作为能力模块被 Qwen 系列模型驱动的智能体调用；自身无模型推理逻辑 |
| **API 端点** | `POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat`（地域化 Endpoint） | 多端点体系：<br>• `POST /v1/agents`（创建 Agent）<br>• `POST /v1/sessions`（启动会话）<br>• `POST /v1/sessions/{id}/chat`（交互）<br>• `GET /v1/sessions/{id}/events`（事件监听） | **无独立 API**；通过智能体配置关联后，由智能体运行时自动调度；开发者不直接调用 Skill 接口 |
| **计费方式** | 按 **API 调用次数 + 模型 token 消耗** 计费（含输入/输出 token）；工具调用不额外计费 | 按 **Agent 实例运行时长 + Session token 消耗 + Memory Store 读写量 + 文件存储量** 综合计费；会话空闲超时自动释放资源 | **按 Skill 执行次数计费**（官方 Skill 免费，自定义 Skill 按次计费）；不消耗模型 token（执行本身不触发新推理） |
| **上下文管理** | 内置多轮对话状态维护；单次请求最大 32768 tokens（含 system prompt） | 全托管 Session 生命周期；支持持久化 Memory Store（向量+结构化混合检索）；单 Session 最大 32k tokens | **无上下文概念**；每次执行完全独立；依赖智能体层传递上下文（如前序步骤生成的 CSV 文件） |
| **工具/能力扩展** | 支持 `tools` 字段声明并调用预注册插件（搜索、DB 查询等），需 RAM 授权 | 支持注册并编排 Skill（Skill 是其子集），还可接入 Vault 凭证、自定义 HTTP endpoints 等更广义“能力” | **即能力本身**；是托管智能体中“Skill”能力的具体实现形式；也可被应用组件间接调用（若组件配置了对应工具） |
| **部署与运维** | 低运维：创建 App 后即可调用；无需管理会话、内存、环境 | 中等运维：需显式管理 Agent、Session、Environment、Memory Store、File 等资源生命周期；支持 TTL 自动清理 | 零运维：上传即用；官方 Skill 自动更新；自定义 Skill 版本需手动切换 |

## 适用场景建议

- **选择应用组件（Application Component）当：**  
  ✅ 快速构建轻量级对话应用（如 FAQ 助手、简单知识问答）；  
  ✅ 已有成熟后端服务，仅需嵌入一个“智能回复模块”；  
  ✅ 对会话状态要求不高，无需[长期记忆](../concepts/memory.md)或复杂工作流；  
  ❌ 不适合需要跨会话记忆、多步自主决策或深度文件分析的场景。

- **选择托管智能体（Managed Agents）当：**  
  ✅ 构建生产级自主 Agent（如客服坐席助手、自动化数据分析员）；  
  ✅ 需要强会话隔离、敏感信息安全注入（Vault）、持久化记忆检索；  
  ✅ 业务流程涉及多步骤工具调用、条件分支、循环重试（`max_steps` 控制）；  
  ✅ 需实时监控执行过程（通过 Events 流）或对接企业 Webhook 系统；  
  ❌ 不适合极简集成或对资源成本极度敏感的 PoC 场景（因管理开销更高）。

- **选择技能（Skill）当：**  
  ✅ 需让智能体“开箱即用”处理特定文件/数据任务（如 PDF 表格提取、Excel 汇总、CSV 清洗）；  
  ✅ 团队无开发资源，但业务人员可精准描述需求（通过优化 `description` 字段）；  
  ✅ 需复用行业专用能力（如金融报文解析、医疗文档结构化），且希望沙箱安全执行；  
  ❌ 不适合需要模型生成文本、进行逻辑推理或返回非文件结果的任务；  
  ❌ 不适合需动态修改执行逻辑的场景（Skill 行为由 `SKILL.md` 静态定义）。

## 技术选型参考指南

面向开发者，请按以下路径决策：

1. **明确核心诉求**：  
   - 若目标是“**调用一个 API 得到智能回复**” → 优先评估 **应用组件**；  
   - 若目标是“**部署一个能记住用户、调用多个工具、自主完成任务的 Agent**” → 选择 **托管智能体**；  
   - 若目标是“**让现有智能体立刻支持处理 Excel/PDF 等文件**” → 直接添加 **技能**（无论底层用应用组件或托管智能体）。

2. **评估工程成熟度**：  
   - 初创团队/快速验证：从 **应用组件** 入手，最小成本验证效果；  
   - 成熟业务系统集成：采用 **托管智能体**，利用其 Environment 隔离、Memory Store 和事件机制保障稳定性与可观测性；  
   - 产品化交付：组合使用 —— 用 **托管智能体** 构建主干 Agent，通过 **技能** 扩展垂直能力，必要时用 **应用组件** 作为轻量备用通道。

3. **注意关键约束**：  
   - 模型限制：三者均**不支持 `qwen-vl`/`qwen-audio`**，多模态需求需单独调用对应 API；  
   - 文件处理：仅 **技能** 和 **托管智能体**（通过 `/files` 上传）原生支持文件输入；应用组件需自行预处理为文本；  
   - 成本控制：高频简单问答选应用组件；长会话、多步骤 Agent 选托管智能体（注意 `max_steps` 与 Memory Store 读写成本）；批量文件处理优先走技能（按次计费通常优于 token 计费）。

> **最佳实践提示**：在托管智能体中启用 Skill 是当前最灵活的架构——它既获得 Agent 的自主性与记忆能力，又通过 Skill 实现零代码专业任务扩展。应用组件可作为该架构的降级方案（当 Agent 服务不可用时，切至组件 API 维持基础对话）。

## 被对比主题页

- [application component api reference](../api/application-component-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [skill](../guides/skill.md)


