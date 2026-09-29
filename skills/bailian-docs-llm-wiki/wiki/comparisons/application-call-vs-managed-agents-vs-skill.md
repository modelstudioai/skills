# 应用调用、托管智能体与技能（Skill）架构对比

本文旨在帮助开发者清晰理解百炼平台中三种核心能力——**应用调用（Application Call）**、**托管智能体（Managed Agents API）** 和 **技能（Skill）** 的定位差异、能力边界与技术约束，从而在构建 AI 应用时做出合理、可扩展、可维护的技术选型。三者并非互斥替代关系，而是分层协作的架构组件：Skill 是能力单元，托管智能体是运行时载体，应用调用是面向生产环境的标准化接入方式。

---

## 关键维度对比

| 维度 | 应用调用（Application Call） | 托管智能体（Managed Agents API） | 技能（Skill） |
|------|------------------------------|-----------------------------------|----------------|
| **本质定位** | **生产级 API 接入层**：调用已发布应用（Agent/Workflow）的标准协议封装 | **全托管 Agent 运行时服务**：提供开箱即用的会话管理、记忆、工具编排等基础设施 | **可插拔任务能力单元**：语义驱动的原子化功能模块，用于扩展智能体处理能力 |
| **输入格式** | • DashScope API：`prompt`（单轮）或 `messages`（多轮/多模态）<br>• Responses API：`input`（支持字符串、消息数组、含 `imageList`/`file_ids` 的对象） | `input` 对象：必含 `text` 字段（字符串），可选 `files` 数组（含 `file_id`）；不支持原生 `messages` 结构 | 无独立 API 输入；通过自然语言指令 + 上下文（含附件）触发；依赖 `description` 语义匹配用户意图 |
| **输出格式** | • 同步：JSON 响应（含 `output`、`thoughts`、`rag_results` 等字段）<br>• 流式：SSE 或 chunked JSON（`incremental_output=true`） | • 同步：JSON（含 `output`、`events`、`session_id`）<br>• 流式：SSE 事件流（`event: step` / `event: final_output`） | 无直接输出；执行结果以结构化数据（如解析后的 JSON 表格）、文件（如生成的 `.xlsx`）、或文本摘要形式，**透传回所属智能体的最终响应中** |
| **支持模型** | • 新版智能体：`qwen-max`/`qwen-plus`/`qwen-turbo`/`qwen-vl` 等全系模型<br>• 工作流：按节点配置任意支持模型（含自定义模型）<br>• 旧版智能体：限定模型列表 | 仅限平台托管模型：`qwen-max`、`qwen-plus`、`qwen-turbo`（**不支持 VL、自定义模型或外部模型**） | 无模型概念；由宿主智能体（调用它的 Agent 或 Workflow）所用模型执行推理并触发 Skill，Skill 本身不运行模型 |
| **API 端点** | • DashScope 原生：`POST /api/v1/apps/{APP_ID}/completion`<br>• OpenAI 兼容：`POST /api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | 统一 RESTful：`POST /v1/agents/{agent_id}/run`（创建、配置等其他端点见 `/v1/agents`） | **无独立 API**；通过控制台添加至智能体后，由平台在推理过程中自动调度，开发者不可直调 |
| **计费方式** | 按调用次数 + 模型 Token 消耗计费（含输入/输出、RAG 检索、图像解析等所有 token） | 按 `agent.run` 调用次数 + 模型 Token 消耗计费；`max_steps` 超限不额外计费，但可能失败 | **不单独计费**；Skill 使用成本计入其宿主智能体的调用费用中（如调用 PDF Skill 产生的 OCR token、模型推理 token） |
| **[长期记忆](../concepts/long-term-memory.md)** | • 智能体应用：支持 `memory_id` 参数启用（需配置）<br>• 工作流/旧版智能体：支持，但新版智能体 API 不支持 | 原生支持：通过 `session_id` 自动关联 `Memory Store`，默认保留 7 天；支持结构化读写（Key-Value） | 不具备记忆能力；状态需由宿主智能体或外部系统维护 |
| **RAG 检索** | • 智能体应用：支持 `rag_options`（指定 `pipeline_ids`/`file_ids`）<br>• 工作流/旧版智能体：支持<br>• 新版智能体 API：**不支持** | **不支持原生 RAG 集成**；需将知识库预加载为 `Memory Store` 条目或通过自定义 Skill 封装检索逻辑 | 可作为 RAG 的“执行器”（如自定义 Skill 调用企业内网搜索 API），但不提供 RAG 框架能力 |
| **多模态支持** | • 图像：支持（需 VL 模型 + `imageList` 参数）<br>• 文件：支持（PDF/DOCX/XLSX 等，需配置文件处理方式） | • 图像：**不支持**（`input.files` 仅支持上传，不触发图像理解）<br>• 文件：支持上传与引用（文本提取由宿主模型完成） | • 官方 Skill：部分支持（如 `pdf`、`xlsx` 支持内容提取）<br>• 自定义 Skill：可实现图像处理（需在 ZIP 中集成模型），但平台不提供 VL 运行环境 |
| **流式响应** | 支持（`stream=true` + `incremental_output=true`） | 支持（`stream=true`，SSE 事件流） | 不适用（无独立响应通道） |
| **调试方式** | 控制台“API 调试”页在线测试；支持 SDK（DashScope/OpenAI） | 控制台 Session 事件查询（`/v1/sessions/{session_id}/events`）；支持 Webhook 订阅 | 控制台对话窗格实时测试；依赖 Skill `description` 质量与上下文匹配度 |

---

## 适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|----------|-----------|
| **快速上线一个客服问答机器人，需对接知识库、支持历史会话、兼容现有 OpenAI 代码** | ✅ 应用调用（Responses API） | 利用 OpenAI 兼容模式零改造迁移；通过 `rag_options` 和 `session_id` 快速集成 RAG 与短期记忆；控制台调试便捷。 |
| **构建一个需要长期用户画像沉淀、多步骤决策（如信贷审批）、且需统一管控凭证与密钥的企业级 Agent** | ✅ 托管智能体（Managed Agents API） | 原生 `Memory Store` 支持结构化[长期记忆](../concepts/long-term-memory.md)；`Credential API` 和 `Vault` 提供安全凭证分发；`Deployment` 支持灰度发布与版本回滚，满足企业治理要求。 |
| **为已有智能体增加“自动解析发票 PDF 并提取金额”能力，且不希望修改智能体核心逻辑** | ✅ 技能（Skill） | 官方 `pdf` Skill 开箱即用；或上传自定义 Skill 封装行业专用解析逻辑；无需改动智能体配置，平台自动语义匹配触发。 |
| **需要严格控制模型选型（如必须用自定义微调模型）、或需在工作流中混合调用多个异构模型（Qwen + GLM + 本地模型）** | ✅ 应用调用（DashScope 原生 API + 工作流） | 工作流节点可自由绑定任意百炼支持模型（含自定义模型）；通过 `biz_params` 精确传递参数；是唯一支持多模型协同编排的方案。 |
| **开发一个轻量级工具类 Bot（如会议纪要生成器），功能单一、无需复杂状态管理** | ⚠️ 应用调用（新版智能体） 或 ✅ 技能（若能力已存在） | 若仅需单次文本处理，新版智能体调用简洁高效；若官方已有 `docx`/`meeting-notes` Skill，直接复用更省资源。 |
| **需要跨多个 Skill 协同完成任务（如先 OCR 扫描件 → 再结构化合同条款 → 最后生成风险报告）** | ❌ 技能（不支持） → ✅ 托管智能体 或 ✅ 应用调用（工作流） | Skill 间无编排能力；必须由上层 Agent 或 Workflow 显式串联调用，托管智能体可通过 `skills` 配置声明依赖，工作流可通过节点连接实现精确编排。 |

---

## 技术选型参考指南（面向开发者）

请按以下顺序进行决策：

1. **明确能力粒度需求**  
   - 若需**扩展单一原子能力**（如“解析 Excel”“调用天气 API”），优先评估 **Skill** —— 降低开发与维护成本，享受平台自动升级与安全审查。  
   - 若需**构建完整业务 Agent**（含记忆、多步、工具链），则跳过 Skill，进入下一步。

2. **评估运行时治理要求**  
   - 若需**企业级运维能力**（灰度发布、密钥 Vault、会话审计、SLA 保障），选择 **托管智能体**。  
   - 若追求**最大灵活性与模型自由度**（自定义模型、VL 多模态、RAG 深度定制、工作流可视化编排），选择 **应用调用（工作流/旧版智能体）**。  
   - 若仅需**快速验证 MVP 或对接标准 API**，且接受平台托管限制，**应用调用（新版智能体 + Responses API）** 是最快路径。

3. **检查关键能力是否被满足**  
   - ✅ 必须支持图像理解？→ 排除托管智能体，选应用调用（VL 模型 + `imageList`）。  
   - ✅ 必须长期保存用户画像（>7天）？→ 托管智能体默认 7 天，应用调用需自行实现外部存储；二者均需额外设计。  
   - ✅ 必须调用私有 API 或处理敏感数据？→ 托管智能体的 `Credential API` 和 `Environment API` 提供隔离环境；自定义 Skill 需确保 ZIP 包符合安全规范。

4. **成本与团队技能匹配**  
   - 初创团队/前端主导项目 → 优先应用调用（OpenAI 兼容）降低学习成本。  
   - AI 工程师主导/复杂 Agent 构建 → 托管智能体提供更清晰的抽象（Session/Event/Memory），减少胶水代码。  
   - 数据工程团队存在 → 技能是复用数据处理能力的理想接口。

> **重要提醒**：三者可组合使用。典型架构为：**工作流（应用调用）→ 编排核心逻辑**，**托管智能体（Managed Agents）→ 运行高 SLA 关键 Agent**，**Skill → 为两者注入通用或垂直领域能力**。避免将 Skill 作为唯一架构，因其不具备状态、编排与可观测性能力。

---  
*最后更新：2024年6月*

## 被对比主题页

- [application call](../api/application-call.md)
- [managed agents api](../api/managed-agents-api.md)
- [skill](../guides/skill.md)


