# 百炼应用调用与模型API直调对比

## 📖 背景与目的
在阿里云百炼平台的开发实践中，开发者通常面临两种服务接入路径：基于可视化控制台构建的**应用层调用**（面向 Agent/Workflow），以及面向底层基础大模型的**API 直调**。本文档旨在对比两者在接口协议、上下文管理、能力边界、计费策略及集成复杂度等核心维度的差异，帮助开发者在系统架构设计、生态迁移或业务迭代阶段，做出符合项目需求的技术选型。

## 📊 核心维度对比

| 对比维度 | 百炼应用调用 (Application Calling) | 模型 API 直调 (Model API Direct) |
|:---|:---|:---|
| **API 端点 / 协议** | 统一基于 DashScope 规范：<br>`POST /api/v1/apps/{APP_ID}/completion` | 支持多协议并行：<br>OpenAI 兼容、Anthropic 兼容、DashScope 原生网关 |
| **输入格式** | `app_id` (必填) + `input.[[prompt|prompt]]` 或 `input.messages` + 可选 `input.session_id` + `input.biz_params`（插件透传） | `model` (必填) + `messages`/`input` + 生成参数（`temperature`, `max_tokens` 等）+ `tools`/`tool_choice` |
| **输出格式** | 标准 JSON 响应，业务结果集中位于 `output.text`，Token 统计在 `usage.models` | 同步 JSON 或 SSE 流式响应，需解析 `choices[0].delta`，包含 `finish_reason` 及完整用量明细 |
| **支持模型 / 能力边界** | 聚焦[[智能体应用]]与[[工作流应用]]编排；内置插件自动路由、节点控制、业务参数动态注入 | 覆盖全量文本模型（如 `qwen-turbo`, `qwen-max` 等）；支持 Function Calling、深度思考(Thinking)、联网搜索、代码解释器 |
| **上下文/状态管理** | **双模式可选**：<br>1. 云端托管：通过 `session_id` 自动拉取缓存（1小时/50轮）<br>2. 客户端维护：显式传入 `messages`（优先级高于云端缓存） | **默认客户端显式维护**（需拼接完整历史）<br>*注：OpenAI Responses 协议内置上下文自动管理；超出窗口需业务层实现滑动压缩* |
| **计费方式** | 按应用实际消耗的输入/输出 Token 阶梯计费（统计口径以 `usage.models` 为准） | 严格按实际消耗 Token 阶梯计费；Thinking 思考过程产生的中间 Token **计入输出侧** |
| **限流与配额** | 共享账户全局配额，地域当前仅支持**中国大陆（北京）**；高频调用建议配置指数退避重试 | 按模型规格独立设定 RPM/TPM 上限；支持控制台或工单申请[[rate-limit]]弹性扩容 |
| **典型场景** | 客服工单流、知识库问答、多步骤自动化审批、需快速对接内部业务系统的 AI 中台 | 独立 C 端对话产品、代码辅助插件、多协议生态平滑迁移、需深度定制 Prompt 与流式渲染的底层服务 |

## 🎯 各方案适用场景建议

### ✅ 推荐使用：百炼应用调用
* **低代码/快迭代需求**：业务逻辑涉及多步推理、外部工具链组合或人工审核节点，适合在控制台通过[[工作流应用]]可视化拖拽编排，避免硬编码复杂控制逻辑。
* **轻量化上下文管理**：希望将多轮对话状态交由云端自动缓存，降低自身数据库/Redis 的存储与同步成本，直接通过 `session_id` 复用历史。
* **业务系统无缝对接**：需将 ERP/CRM 等业务参数动态注入 AI 流程，可通过 `biz_params.user_defined_params` 实现标准化透传，结合[[自定义插件]]完成数据闭环。

### ✅ 推荐使用：模型 API 直调
* **生态迁移与协议兼容**：现有项目已深度绑定 OpenAI 或 Anthropic 技术栈，采用对应兼容协议可实现 `base_url` 与 SDK 替换的最低成本迁移，无需重构提示词结构。
* **极致上下文与流式控制**：对首字延迟(TTFT)、Token 截断策略、流式分块渲染有严格要求；或需自行实现长上下文摘要压缩、向量检索融合等高级逻辑。
* **深度定制与高级特性**：需精细化控制采样参数（`top_p`, `temperature`）、启用模型内置的[[parameter-validation]]、深度思考(Thinking)能力或动态 Function Calling。

## 🛠️ 开发者技术选型 Checklist
| 决策考量 | 选择建议 |
|:---|:---|
| **是否希望平台托管多轮会话状态？** | 是 → 应用调用(`session_id`) 或 Responses协议；否 → 直调(自主维护) |
| **业务是否依赖复杂可视化流程/节点控制？** | 是 → 应用调用(工作流)；否 → 直调 |
| **现有代码库是否基于 OpenAI/Anthropic SDK？** | 是 → 直调(对应兼容协议)；否 → 均可 |
| **是否需要对思考过程 Token 或上下文窗口做精细预算？** | 是 → 直调；否 → 应用调用 |
| **目标部署地域是否仅限中国大陆？** | 仅大陆 → 两者均可；需海外 Region → 当前直调支持更广（应用调用暂未开放） |

> **💡 最佳实践提示**：在实际架构中，两者并非互斥。常见组合模式为：使用**百炼应用调用**处理核心业务编排与插件路由，在关键节点（如复杂内容生成、特定格式结构化输出）通过工作流的**代码节点**或[[自定义插件]]内部发起**模型 API 直调**，以兼顾开发效率与底层控制力。详细调用规范请参考[[dashscope-sdk]]文档与各协议对应指南。

## 被对比主题页

- [[bailian-application-calling|bailian [[application-call|application call]]ing]] — `../guides/bailian-application-calling.md`
- [[qwen-api-reference|qwen api reference]] — `../api/qwen-api-reference.md`

