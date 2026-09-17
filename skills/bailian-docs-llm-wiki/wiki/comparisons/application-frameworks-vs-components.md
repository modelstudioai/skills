# 应用构建方案对比：框架/工具链、应用组件API与托管智能体

本文旨在帮助开发者在阿里云百炼平台上，根据业务需求、技术栈成熟度、运维复杂度及长期演进目标，科学选择最适合的应用构建路径。三类方案分别面向不同抽象层级：**框架/工具链**提供模型能力的“标准化接入层”，适合已有 OpenAI 生态或需快速迁移的场景；**应用组件 API** 提供“能力封装层”，聚焦企业级对话、知识增强与可控推理；**托管智能体（Managed Agents）** 则构建于“工作流编排层”，面向具备[长期记忆](../concepts/long-term-memory.md)、多步工具协同与自主决策需求的复杂智能体应用。本对比从技术实现、使用成本、扩展边界与运维责任等维度展开，为工程化选型提供客观依据。

## 方案核心维度对比

| 维度 | 框架/工具链（[OpenAI 兼容接口](../concepts/openai-compatible-api.md)） | 应用组件 API | 托管智能体（Managed Agents） |
|------|------------------------------|----------------|------------------------------|
| **定位与抽象层级** | 模型能力直连层（Model-as-a-Service） | 预置能力服务层（Capability-as-a-Service） | 智能体工作流层（Agent-as-a-Service） |
| **输入格式** | OpenAI 标准格式：<br>`messages` 数组（含 `role`/`content`）、`model`、`temperature` 等；支持 `previous_response_id` 实现轻量上下文 | 百炼定制 JSON：<br>`input.messages`（同 OpenAI 格式）、`parameters.*` 显式控制生成参数；`session_id` 用于会话管理 | 多阶段结构化输入：<br>1. Agent 创建（`model_id`, `environment_id`）<br>2. Session 启动（`input`, `tools` 列表）<br>3. 工具结果回传（`tool_call_id`, `result`） |
| **输出格式** | OpenAI 兼容响应：<br>`choices[0].message.content`（文本）、`usage`（token 统计）、`id`（用于下轮 `previous_response_id`）；支持 SSE 流式 | 百炼统一响应体：<br>`output.text`（主文本）、`output.choices`（完整选项）、`usage.input_tokens`/`output_tokens`；支持 `stream: true` 的 SSE 流式（字段名一致） | 事件驱动 SSE 流：<br>`event: message`（AI 回复）、`event: tool_call`（工具调用请求）、`event: tool_result`（工具执行结果）、`event: session_end`；需客户端按事件类型分发处理 |
| **支持模型** | 全量百炼模型：<br>• 文本：`qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.3` 等<br>• 多模态：`qwen3-vl-plus`、`qwen-vl-ocr`<br>• Embedding：`text-embedding-v4`、`qwen3.7-text-embedding` | 限定企业级对话模型：<br>`qwen-max`、`qwen-plus`、`qwen-turbo`（均为 Qwen 系列托管版本）；不支持第三方模型或 VL/Embedding 类模型 | 严格限定托管智能体模型：<br>`qwen-max`、`qwen-plus`、`qwen-turbo`（仅此三款）；不支持自定义模型或非 Qwen 系列 |
| **API 端点** | 业务空间专属域名：<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>（推荐）或 `dashscope.aliyuncs.com`（不推荐） | 全局服务端点：<br>`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`<br>（Region 绑定，需匹配 RAM 凭证） | 资源路径化 RESTful 接口：<br>`POST /agents` → `POST /agents/{id}/sessions` → `POST /sessions/{id}/tool_results`<br>端点统一为 `https://dashscope.aliyuncs.com/api/v1` |
| **认证方式** | `Authorization: Bearer <DASHSCOPE_API_KEY>`（DashScope API Key） | `Authorization: Bearer <DASHSCOPE_API_KEY>`（同上），但需 RAM 授权 `dashscope:InvokeApplication` 权限 | `Authorization: Bearer <DASHSCOPE_API_KEY>` + RAM 授权 `dashscope:ManageAgents` 及 `dashscope:InvokeAgent`；Credential 需额外存入 Vault 并授权给 Environment |
| **会话与上下文管理** | • `Responses API` + `previous_response_id`：自动注入上轮 `id`，轻量多轮<br>• `Conversations API`：显式创建/更新会话实体，跨设备同步 | 依赖 `session_id` 字段：服务端自动维护该 ID 下的上下文状态；无内置历史持久化，需应用层保存 `session_id` | 原生 Session 生命周期管理：<br>• `X-Session-ID` 自动绑定/生成<br>• 上下文自动持久化（含工具调用历史、文件引用）<br>• 支持 `DELETE /sessions/{id}` 主动清理 |
| **工具调用（Tool Calling）** | 仅 `Responses API` 支持：<br>• 内置工具（如搜索、计算）由模型自动触发<br>• 不支持自定义函数注册与参数提取 | 支持自定义工具调用：<br>• 在 `input` 中声明 `tools` 列表（JSON Schema 描述）<br>• 模型自动提取参数并返回 `tool_calls` 结构 | 完整工具工作流：<br>• `tool_call` 事件触发 → 应用调用对应 Skill 接口 → `tool_result` 回传 → Agent 继续推理<br>• 内置 `web_search`/`code_interpreter`/`file_read` 等 Skill，支持凭证驱动（Vault） |
| **文件处理能力** | • `Files API`：上传文档（`purpose=file-extract`）用于 OCR/解析<br>• `Batch API`：上传 JSONL 进行异步批量处理 | 仅支持 `input.messages` 中以文本形式嵌入文件内容摘要；**不支持原生文件上传与解析** | 全流程文件支持：<br>• `POST /files` 上传任意二进制文件<br>• 在 `input` 中以 `file://<file_id>` 引用<br>• 文件内容自动送入模型上下文（支持 PDF/DOCX/CSV 等） |
| **批处理能力** | • 同步 Batch：单请求多条 [prompt](../guides/prompt.md)，超时 3600 秒<br>• 异步 Batch：JSONL 文件上传 + 任务调度，费用为实时调用的 50% | **不支持批处理**；每次请求为单次对话/生成 | **不支持批量请求**；每个 Session 为独立工作流实例；高并发需自行调度多个 Session |
| **计费方式** | • 按 token 计费（输入 + 输出）<br>• `enable_thinking=true` 时，思考 token 单独计费<br>• 异步 Batch 享 50% 折扣 | • 按 token 计费（输入 + 输出）<br>• 无思考模式开关，计费逻辑与基础模型一致<br>• 无 Batch 折扣 | • 按 Session 内总 token 计费（含所有工具调用的输入/输出）<br>• 工具调用本身不额外计费，但其输入输出计入 Session 总 token<br>• 无批量折扣，无按调用次数计费选项 |
| **典型场景** | • 将现有 OpenAI 应用零代码迁移至百炼<br>• 构建向量检索服务（Embedding + RAG 后端）<br>• 多模态理解（图像+文本联合分析）<br>• 批量内容生成（营销文案、报告摘要） | • 企业客服机器人（需知识库集成）<br>• 内部智能助手（HR/IT 政策问答）<br>• 结构化数据提取（从邮件/表格中抽取字段）<br>• 需稳定参数控制与统一错误处理的生产 API | • 自动化数据分析 Agent（读取 Excel → 生成图表 → 输出报告）<br>• 研究助理（联网搜索 + 文档解析 + 综述生成）<br>• 客户成功工作流（分析工单 → 查询 CRM → 调用邮件 API 发送跟进）<br>• 需[长期记忆](../concepts/long-term-memory.md)与多步骤协作的 SaaS 集成场景 |

## 适用场景建议

- **选择「框架/工具链」当您：**  
  ✅ 已有基于 OpenAI SDK 的成熟应用，追求最小改造成本；  
  ✅ 需要灵活调用百炼全量模型（尤其是多模态、Embedding、第三方模型）；  
  ✅ 业务以“单次推理”为主，或可通过 `previous_response_id`/`Conversations API` 满足轻量会话需求；  
  ❌ 不适合需要深度工具编排、长期上下文沉淀或企业级权限隔离的场景。

- **选择「应用组件 API」当您：**  
  ✅ 构建标准企业对话应用，且明确只需 `qwen-max`/`plus`/`turbo` 等托管模型；  
  ✅ 需要开箱即用的知识库增强问答（KnowledgeBase ID 直接集成）；  
  ✅ 要求简单可控的工具调用（如调用一个内部 HTTP 接口获取数据），无需复杂事件流处理；  
  ✅ 追求低延迟、高吞吐的 API 服务，且可接受应用层管理 `session_id`；  
  ❌ 不适合需要多步工具循环、文件深度解析、或自动化工作流编排的场景。

- **选择「托管智能体」当您：**  
  ✅ 构建真正意义上的 AI Agent：具备自主规划、工具选择、结果验证与迭代推理能力；  
  ✅ 业务流程天然包含多个异构步骤（如“查资料→写代码→运行测试→生成报告”）；  
  ✅ 需要安全、隔离的凭证管理（Vault）与沙箱化执行环境（Environment）；  
  ✅ 接受更高抽象层级带来的学习成本，并愿意按 Session 生命周期设计系统架构；  
  ❌ 不适合简单问答、单次生成或对延迟极度敏感（如毫秒级响应）的场景；也不适合预算受限且无复杂工作流需求的项目。

## 技术选型参考指南（面向开发者）

| 选型考量因素 | 推荐方案 | 关键理由 |
|--------------|----------|----------|
| **迁移成本最低** | 框架/工具链 | 100% OpenAI SDK 兼容，仅需替换 `base_url` 和 `model`，零逻辑修改 |
| **模型选择最广** | 框架/工具链 | 唯一支持 VL 模型、Embedding、第三方模型（DeepSeek/GLM/Kimi）的方案 |
| **知识库集成最便捷** | 应用组件 API | `knowledge_base_id` 参数直连，无需自行实现 RAG 检索逻辑 |
| **工具调用最灵活** | 托管智能体 | 唯一支持事件驱动、多轮工具交互、凭证安全注入与结果校验的方案 |
| **文件处理最完整** | 托管智能体 | 唯一支持原生文件上传、格式解析、内容自动注入上下文的方案 |
| **运维负担最轻** | 应用组件 API | 无 Environment/Skill/Vault 等概念，权限模型最简（仅 RAM 授权） |
| **长期演进潜力最大** | 托管智能体 | 百炼平台持续投入 Agent 生态（Skill 商店、可视化编排、监控告警），是下一代智能应用基座 |

> **重要提醒**：三类方案**并非互斥**。推荐采用组合策略——例如，用「框架/工具链」调用 `text-embedding-v4` 生成向量，存入向量库；再用「应用组件 API」构建知识增强对话；对于高阶任务（如“分析本周销售报告并生成 PPT”），则交由「托管智能体」调度多个子任务完成。百炼平台的设计哲学正是通过分层抽象，让开发者在合适层级做合适的事。

## 被对比主题页

- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application component api reference](../api/application-component-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)


