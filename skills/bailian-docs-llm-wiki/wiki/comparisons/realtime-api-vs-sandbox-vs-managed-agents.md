# 实时API、沙箱环境与托管智能体对比

为帮助开发者在百炼平台上高效选型，本文系统对比三种核心能力：**Qwen-Omni Realtime API（实时API）**、**Sandbox API（沙箱环境）** 与 **Managed Agents API（托管智能体）**。三者定位迥异——实时API聚焦**低延迟多模态语音交互**，沙箱环境专注**安全可控的代码执行**，托管智能体则面向**具备记忆、工具调用与长期会话能力的自主Agent构建**。本对比旨在厘清技术边界、明确适用场景，并提供可落地的选型决策依据。

## 关键维度对比

| 维度 | 实时API（Omni Realtime） | 沙箱环境（Sandbox） | 托管智能体（Managed Agents） |
|------|--------------------------|----------------------|------------------------------|
| **核心定位** | 流式多模态实时人机交互（语音+文本+音频） | 隔离、受限、一次性的代码执行环境 | 具备状态管理、工具编排与[长期记忆](../concepts/long-term-memory.md)的AI Agent托管服务 |
| **输入格式** | WebSocket流式二进制音频（PCM/WAV）、文本事件（`input_text`）、图片（Base64 JPG/JPEG ≤256KB） | RESTful JSON：`code`（字符串）或 `template_id`，含 `runtime`、`timeout` 等配置 | RESTful JSON：用户消息（文本/文件引用）、会话ID；支持上传文件至 `Vault` 后引用 |
| **输出格式** | WebSocket服务端事件流：<br>• `response.text.delta`（流式文本）<br>• `response.audio.delta`（流式PCM音频）<br>• `input_audio_transcription.delta`（实时ASR）<br>• `conversation.item.created`（工具调用/搜索结果） | RESTful JSON响应：<br>• `status`: `"succeeded"`/`"failed"`<br>• `logs`: 执行标准输出/错误日志（字符串）<br>• `exit_code`: 进程退出码 | RESTful JSON响应 + 可选Webhook：<br>• 同步返回 `message` 对象（含 `content`, `role`, `tool_calls`）<br>• 异步触发 `session.completed`、`tool_called` 等事件 |
| **支持模型/运行时** | 专用实时多模态大模型：<br>• `qwen3.5-omni-plus-realtime`<br>• `qwen3.5-omni-flash-realtime`<br>• `qwen3-omni-flash-realtime`<br>• `qwen-omni-turbo-realtime` | 通用轻量级运行时：<br>• Python 3.9–3.12<br>• Node.js 18/20<br>• Shell (bash)<br>（*不支持Java，文档已更新*） | 模型无关（解耦设计）：<br>通过 `Environment` 资源绑定任意百炼支持模型：<br>• `qwen-max`、`qwen-plus`<br>• 自定义微调模型（需已部署） |
| **API 协议与端点** | WebSocket 协议：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime` | RESTful HTTP/HTTPS：<br>`POST https://dashscope.aliyuncs.com/api/v1/sandbox/instances` | RESTful HTTP/HTTPS + Webhook：<br>`POST /v1/sessions/{id}/messages`<br>`POST /v1/webhooks`（注册回调） |
| **计费方式** | 按**实际使用时长（秒）+ 音频处理量（分钟）+ token数**计费：<br>• 连接维持、VAD检测、音频编解码、模型推理均计入时长<br>• 文本/音频输出按 token 或音频分钟单独计费 | 按**实例执行时长（秒）+ 内存占用（MB·秒）** 计费：<br>• 超时或失败仍计费至终止时刻<br>• 内存按 `memory_mb × 实际运行秒数` 计算 | 按**Agent调用次数 + 模型推理token + 工具调用次数 + 存储用量**计费：<br>• `Session` 生命周期内所有推理、工具执行、文件存储均累计计费<br>• Webhook通知免费 |
| **典型场景** | • 智能语音客服（带实时转写与音色复刻）<br>• 多轮语音助手（支持语义VAD打断）<br>• 教育陪练（语音反馈+文本解析）<br>• 实时会议纪要（语音→文本+摘要+行动项） | • AI生成代码的即时验证与沙箱执行<br>• 动态HTTP请求工具（如`curl`模板调用外部API）<br>• 数据清洗脚本安全执行（无网络/受限权限）<br>• 教学实验环境（学生提交代码自动评测） | • 客户支持Agent（记忆历史工单+调用CRM/知识库）<br>• 自动化运营助手（分析报表→生成PPT→邮件发送）<br>• 企业级Copilot（集成内部系统凭证、审批流、文档Vault）<br>• 复杂任务分解Agent（多步骤工具协同+循环推理） |
| **状态与生命周期** | 会话级有状态（`session`），支持 `idle_timeout_ms` 自动引导；连接断开即终止 | 完全无状态、一次性：实例创建→执行→销毁；不可重启、不可重用 | 全生命周期托管：<br>• `Agent`（长期存在、可更新）<br>• `Session`（用户级上下文，TTL可配）<br>• `Vault`（加密密钥/文件持久化）<br>• `Environment`（模型与推理参数快照） |
| **扩展性与集成** | 依赖SDK（Python/Java）实现高级功能（如自定义采样率、VAD策略）；需自行管理WebSocket连接与重连 | 通过预置模板（`template_id`）快速复用；支持企业版启用外网（需报备）；日志可对接SLS | 原生支持：<br>• `Skill`（标准化工具注册）<br>• `Credential`（凭据安全注入）<br>• `Webhook`（事件驱动架构）<br>• `Deployment`（灰度发布） |

## 各方案适用场景建议

### ✅ 选择 **实时API** 当：
- 你的应用**必须支持语音输入与实时音频输出**（如电话客服、车载助手、无障碍交互）；
- 要求**端到端延迟 <800ms**，且需**语义级语音活动检测（semantic VAD）** 实现自然打断；
- 需要**音色复刻**或**联网搜索**（仅限 `qwen3.5-omni-realtime` 系列）；
- 场景以**单轮强交互、短时会话**为主，无需[长期记忆](../concepts/long-term-memory.md)或跨会话状态。

> ⚠️ 注意：不适用于纯文本问答、批量数据处理、后台任务调度等非实时场景。

### ✅ 选择 **沙箱环境** 当：
- 你需要**安全执行不可信的用户代码或动态脚本**（如AI生成的Python函数）；
- 任务是**轻量、短暂、无状态**的（≤5分钟，≤1GB内存），且**无需调用外部服务或持久化数据**；
- 你希望**绕过模型推理**，直接获得确定性计算结果（如数学运算、JSON转换、正则提取）；
- 作为AI工具链中的“执行层”，配合LLM做**代码生成→沙箱验证→结果反馈**闭环。

> ⚠️ 注意：禁止用于敏感数据处理（沙箱无加密存储）、高频调用（实例创建开销显著）、或需要网络访问的普通场景（需企业版特批）。

### ✅ 选择 **托管智能体** 当：
- 你的Agent需**跨多轮对话保持上下文与记忆**（如客户历史、偏好设置）；
- 必须**编排多个工具并处理复杂依赖**（如“查订单→调物流API→生成摘要→发邮件”）；
- 要求**生产级可靠性**：自动重试、错误降级、Webhook事件通知、灰度发布；
- 需要**集中管理敏感凭据**（数据库密码、API Key）并通过 `Credential` 安全注入；
- 应用属于**企业级AI应用**，需符合审计、权限隔离、资源配额等合规要求。

> ⚠️ 注意：不适用于简单问答、单次API调用、或对延迟极度敏感（如实时语音）的场景；其抽象层级高于实时API，不可替代流式音频能力。

## 技术选型参考指南（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 | 行动建议 |
|----------|-----------|-----------|-----------|
| “我要做一个能听会说的银行语音机器人，支持客户用方言提问并实时播报答案” | ✅ 实时API | 唯一支持双向流式语音、低延迟VAD、音色复刻的方案 | 选用 `qwen3.5-omni-plus-realtime` + `semantic_vad`；集成Python SDK处理PCM音频流 |
| “用户输入一段SQL，我需要安全执行并返回结果，不能访问生产库” | ✅ 沙箱环境 | 提供进程级隔离、资源限制、静态扫描，杜绝越权风险 | 创建 `python` 实例，禁用网络，用 `sqlite3` 内存数据库执行；设置 `timeout=30` |
| “我们想上线一个销售助手Agent，能查CRM、读合同PDF、生成报价单、发起审批流” | ✅ 托管智能体 | 原生支持多工具编排、Vault密钥管理、长期Session、Webhook事件驱动 | 设计 `SalesAgent`，注册 `CRM_Skill`/`PDF_Reader_Skill`/`Approval_Skill`，配置 `Credential` 绑定CRM Token |
| “需要批量处理10万条文本，调用大模型做情感分析” | ❌ 三者均不推荐 → 选用 **Batch Inference API** | 实时API成本高、沙箱不支持LLM、托管智能体过度设计 | 使用 `POST /api/v1/batch/inference` 提交异步任务，按token计费更经济 |
| “想快速测试一个AI提示词效果，看它能否正确解析用户地址” | ✅ 托管智能体（轻量模式） *或* ✅ 实时API（文本模式） | 两者均支持纯文本交互；托管智能体便于后续扩展工具，实时API延迟更低 | 若仅验证[prompt](../guides/prompt.md)：用实时API设 `modalities=["text"]`；若计划加地图API：直接建托管Agent |

> **终极原则**：  
> - **要语音？→ 选实时API**  
> - **要跑代码？→ 选沙箱环境**  
> - **要造Agent？→ 选托管智能体**  
> 三者可组合使用（例如：托管智能体调用沙箱执行用户代码；实时API语音输入触发托管智能体会话），但切勿强行用错场景——这将导致成本飙升、体验劣化或安全风险。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [sandbox api](../api/sandbox-api.md)
- [managed agents api](../api/managed-agents-api.md)


