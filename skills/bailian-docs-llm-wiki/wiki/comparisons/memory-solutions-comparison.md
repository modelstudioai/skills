# 长期记忆方案对比：Long-term Memory vs Memory Library

为帮助开发者在百炼平台中科学选型长期记忆能力，本文对两种主流方案——**Long-term Memory（新架构版）** 与 **Memory Library（记忆库）** 进行系统性对比。二者均面向跨会话、结构化、语义驱动的[记忆管理](../concepts/memory.md)，但在设计哲学、集成方式、模型耦合度、运维粒度及商业化路径上存在本质差异。本对比基于截至 2024 年 Q3 的正式发布版本（`long-term-memory-new` v1.2 / `memory-library` v2.0），旨在为智能体（Agent）、个性化助手、企业服务类应用提供可落地的技术决策依据。

## 关键维度对比

| 维度 | Long-term Memory（新架构） | Memory Library（记忆库） |
|------|-----------------------------|---------------------------|
| **定位与设计目标** | 模型原生增强型记忆：作为大模型推理链的**深度集成组件**，强调与 LLM 推理生命周期强协同（自动注入、schema 驱动提取） | 平台级通用记忆服务：作为**解耦的后端中间件**，提供标准化 Add/Search API，与前端所用模型完全无关 |
| **输入格式** | - 写入：JSON 对象（需显式指定 `memory_type`, `key`, `value`, `ttl_seconds` 等）<br>- 注入：通过 `messages` 中 `memory_context` 字段声明加载类型（如 `["fragment", "profile"]`） | - 写入：`POST /add`，传入 `user_id` + `messages` 数组（自动解析对话内容）<br>- 检索：`POST /memory_nodes/search`，传入 `user_id` + 当前 `messages`（生成查询向量） |
| **输出格式** | - 写入响应：轻量 JSON（仅含 `id`, `status`）<br>- 检索结果：自动注入至 `messages` 上下文，**不返回原始记忆数据**；调试需调用 `/v1/memory/debug` | - 写入响应：返回结构化 `memory_node_id` 及提取详情（含字段、置信度、过期时间）<br>- 检索响应：标准 JSON 数组，每项含 `id`, `content`, `score`, `type`, `expire_at`, `metadata` 等完整字段 |
| **支持模型** | 严格限定：仅 `qwen-max`、`qwen-plus` 及明确标注 `ltm-enabled` 的模型；`qwen-turbo`、`qwen-14b-chat` 等**不支持** | **模型无关**：所有百炼支持的模型（包括 `qwen-turbo`、`qwen-14b-chat`、`qwen-vl` 等）均可调用其 API；记忆能力由平台统一服务提供 |
| **API 端点** | - 写入：`POST /v1/memory/fragments` / `PUT /v1/memory/profiles/{id}`<br>- 注入：隐式（通过 `memory_context` 触发）<br>- 调试：`GET /v1/memory/debug` | - 写入：`POST /v1/add`（默认库）或 `POST /v1/{memory_library_id}/add`<br>- 检索：`POST /v1/memory_nodes/search`（支持多库路由）<br>- 管理：`GET /v1/memory_nodes/list`, `DELETE /v1/memory_nodes/{id}` 等完整 CRUD |
| **计费方式** | 按调用次数计费（写入 + 检索），**未公开详细单价**；当前处于灰度阶段，费用计入应用整体账单，无独立计量项 | **精细化分项计费**（2026年8月20日起正式商用）：<br>- 存储：¥0.002 / 万条 / 小时<br>- 写入（Add）：Lite ¥0.00001/次，Pro ¥0.0005/次<br>- 检索（Search）：Lite ¥0.00002/次，Pro ¥0.001/次<br>- 用户画像提取：额外按字段数计费 |
| **典型场景** | - 高保真事实管理（如用户认证邮箱、合同编号等强一致性要求）<br>- 模型驱动的自动化记忆维护（`auto_extract: true` 场景）<br>- 需与 `qwen-max` 等高阶模型深度协同的金融/法律类 Agent | - 多模型混合部署场景（如 Turbo 做快速响应 + Max 做深度分析，共用同一记忆源）<br>- 快速上线的个性化助手（开箱即用默认库 + 控制台规则配置）<br>- 需要人工审核、批量管理、跨应用共享记忆的 SaaS 类产品 |
| **隔离与多租户** | 以 `namespace`（默认为应用 ID）隔离；不同 namespace 记忆不可见；**不原生支持跨应用共享** | 以 `user_id` 为第一隔离维度；同一 `user_id` 的记忆可在多个应用间共享（需权限配置）；支持创建多个独立 `memory_library_id` 实现业务域隔离 |
| **Schema 管理** | 必须在应用配置中预定义 `memory_schema`（JSON Schema），写入时强校验；`fragment` key 全局唯一且字符受限（`[a-zA-Z0-9_-]`） | 用户画像需先调用 `CreateProfileSchema` 创建模板；事实记忆通过“记忆规则”配置抽取逻辑（正则/LLM 指令），**无需预定义全局 schema**；key 由系统自动生成 |
| **TTL 与生命周期** | `ttl_seconds` 对 `fragment` 有效（默认 1 年）；`profile` 类型**实际不受 TTL 控制**，仅靠显式 `PUT` 更新 | 支持四级过期策略：7天 / 30天 / 180天 / 永不过期；所有类型（事实/画像）均严格遵循配置的过期时间 |
| **异步行为说明** | 所有写入均为**异步落库**；`200 OK` 仅表示入队成功，不保证立即可查 | `Add` 为同步返回提取结果（但后台异步持久化）；用户画像提取为**明确异步任务**，首次 `GetUserProfile` 可能为空，需业务侧轮询 |

## 各方案适用场景建议

### ✅ 推荐选用 **Long-term Memory（新架构）** 当：
- 应用已确定使用 `qwen-max` 或 `qwen-plus`，且追求**模型与记忆的零摩擦协同**；
- 业务对关键事实（如用户身份标识、订单号、合规条款）有**强一致性、强可追溯性**要求，需精确控制 `key`、显式更新、严格 schema 校验；
- 开发团队具备较强工程能力，愿意承担 schema 定义、namespace 管理、调试接口集成等额外开发成本；
- 场景以**单应用、单模型、高精度事实管理**为主，暂无跨模型/跨应用共享需求。

### ✅ 推荐选用 **Memory Library（记忆库）** 当：
- 应用需**兼容多种模型**（例如前端用 `qwen-turbo` 做轻量交互，后台用 `qwen-max` 做深度分析），且希望记忆层统一；
- 追求**快速上线**：利用默认记忆库 + 控制台可视化配置规则，5 分钟完成基础记忆能力接入；
- 需要**灵活的运营能力**：如人工审核记忆、批量导出/删除、按用户维度查看全量记忆快照、配置差异化过期策略；
- 构建**多租户 SaaS 或企业级平台**，要求同一 `user_id` 的记忆在客服、销售、BI 等多个子系统间安全共享；
- 对成本敏感且调用量大：可选用 Lite 版本降低 Search/Add 成本，或通过 `top_k`/`min_score` 精细调控召回质量与 [Token](../concepts/token.md) 开销。

## 技术选型参考指南（面向开发者）

| 选型考量因素 | Long-term Memory | Memory Library | 建议动作 |
|--------------|------------------|----------------|----------|
| **模型锁定风险** | ⚠️ 高：绑定特定高阶模型，迁移成本高 | ✅ 低：完全解耦，模型升级不影响记忆服务 | 若未来可能切换模型（如从 Max 降级到 Plus/Turbo），优先 Memory Library |
| **开发效率** | ⚠️ 中高：需配置 schema、处理 namespace、调试隐式注入 | ✅ 高：API 直观、文档完善、控制台友好、SDK/CLI 开箱即用 | MVP 验证或交付周期紧，首选 Memory Library |
| **数据治理能力** | ⚠️ 基础：仅支持按 namespace 隔离，无批量操作、审计日志、导出功能 | ✅ 强：支持控制台全量管理、权限分级、操作审计、CSV 导出 | 涉及金融、医疗等强监管场景，Memory Library 提供更完备治理工具链 |
| **成本可控性** | ❓ 不透明：当前无独立计费项，长期成本难预估 | ✅ 高：分项明细计费，支持 Lite/Pro 切换、`top_k` 限流、存储压缩 | 预算敏感型项目，务必使用 Memory Library 并启用 Lite 策略 |
| **未来演进方向** | 定位为「模型原生记忆」，将随 Qwen 系列模型迭代持续增强语义理解能力 | 定位为「平台标准记忆中间件」，将扩展向量数据库对接、RAG 增强、跨云同步等企业级特性 | 长期战略规划中，Memory Library 具备更广的生态兼容性与扩展边界 |

> **重要提示**：二者**非互斥关系，可组合使用**。典型混合模式：  
> - 使用 **Memory Library** 作为统一记忆底座，管理用户画像与通用事实；  
> - 在 `qwen-max` 驱动的关键会话中，启用 **Long-term Memory** 的 `auto_extract` 能力，对高价值片段（如合同条款、审批意见）做二次强化校验与精准写入；  
> - 通过 `namespace` 与 `user_id` 映射，实现双通道记忆的协同与去重。  
>   
> 最终选型请结合您的模型栈、交付节奏、合规要求与成本模型综合决策。建议在 POC 阶段并行接入两个方案，用真实对话数据验证召回准确率、延迟与成本表现。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


