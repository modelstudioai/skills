# [长期记忆](../concepts/memory.md)与记忆库方案对比

为帮助开发者清晰理解百炼平台中两类核心[长期记忆](../concepts/memory.md)能力的定位、差异与演进关系，本文档对 **“[长期记忆](../concepts/memory.md)（Long Term Memory）新 API”** 与 **“记忆库（Memory Library）”** 进行系统性对比分析。需特别说明：根据官方文档指引（`memory library overview` 中明确指出“与之前的长期记忆功能相比，记忆库是全面升级版”，且“旧版‘长期记忆’功能已下线”），**二者并非并存方案，而是同一服务在不同阶段的命名与能力演进体现**。当前（2024年起）百炼平台统一提供的是 **记忆库（Memory Library）服务**，其 API、控制台、文档体系及商业化路径均已全面收敛至此。所谓“长期记忆 new”实为记忆库服务的底层 API 接口层描述，而“记忆库”则是面向用户的产品化命名与集成抽象。

本对比旨在厘清技术细节一致性、接口行为差异及最佳实践建议，避免因术语混用导致选型偏差，为开发者提供可落地的技术决策依据。

## 关键维度对比

| 维度 | 长期记忆（Long Term Memory new） | 记忆库（Memory Library） |
|------|----------------------------------|---------------------------|
| **本质定位** | 记忆库服务的底层 REST API 规范描述，聚焦接口契约与参数语义 | 百炼平台统一提供的长期记忆产品名称，涵盖 API、控制台、规则引擎、Agent 集成等完整能力层 |
| **输入格式** | `POST /add` 或 `/add-async`：支持 `messages`（对话数组）或 `custom_content`（结构化片段，含 `skill_name`/`skill_description` 等）；必填 `user_id`；可选 `profile_schema`、`memory_library_id`、`plan_version` 等 | `POST /api/v2/apps/memory/add`：统一接收 `messages` 数组 + `user_id`；画像提取需显式传入 `profile_schema` ID；支持多模态内容（图像/音频等）扩展字段（通过 `attachments`） |
| **输出格式** | 同步 `/add` 返回 `memory_node_id` 及基础元信息；异步 `/add-async` 返回 `event_id`，需轮询 `/events/{event_id}` 获取最终 `result`（含 `memory_nodes`）；检索 `/memory_nodes/search` 返回带 `score` 的 `memory_nodes` 列表 | `Add` 接口返回标准化响应体（含 `event_id` 或直接 `memory_nodes`）；`Search` 接口返回结构一致的 `memory_nodes` 数组，每项含 `id`、`content`、`type`、`score`、`meta_data`；支持 `min_score` 过滤后结果 |
| **支持模型/能力** | 明确区分 `observation`（事件性事实）、`skill`（技能流程）、`profile`（用户画像）三类；`skill` 需手动构造 `custom_content`；画像提取依赖模板配置 | 统一抽象为“事实记忆”与“用户画像”，但底层兼容 `observation`/`skill`/`profile`；**新增多模态记忆支持**（图像/音频特征提取）；**技能记忆可通过规则自动识别**（无需手动构造 `custom_content`） |
| **API 端点** | `/add`, `/add-async`, `/memory_nodes/search`, `/profile_schemas/{id}/user_profile`, `/events/{event_id}` 等（路径较细粒度） | `/api/v2/apps/memory/add`, `/api/v2/apps/memory/memory_nodes/search`, `/api/v2/apps/memory/profile_schemas/{id}/user_profile` 等（路径统一归入 `/api/v2/apps/memory/` 命名空间） |
| **计费方式** | 按 `plan_version="pro"` 或 `"lite"` 分档计费：Pro 版含 Rerank、`min_score` 过滤、高精度抽取；Lite 版无 Rerank，相似度计算更轻量；存储按小时计费；2026年8月20日起商业化 | **完全一致**：Add/Search 调用按 Pro/Lite 版本计费；存储按小时计费；免费额度（1500次 Add + 5000次 Search）自商业化日起3个月内有效；计费策略与长期记忆 new 完全对齐 |
| **典型场景** | - 需精细控制 `skill` 写入（如预定义工作流步骤）<br>- 对异步任务状态有强感知需求（需主动轮询 event）<br>- 已深度集成旧版 long-term-memory 接口逻辑的应用迁移 | - 快速构建个性化智能体（Agent Harness 一键接入）<br>- 多模态交互场景（图文/音视频上下文记忆）<br>- 基于规则自动提取技能与事实（减少人工构造 `custom_content`）<br>- 工作流插件集成（如 OpenClaw） |
| **限流策略** | 账号级总限流 3000 QPM；`/add` ≤ 120 QPM；`/memory_nodes/search` ≤ 300 QPM；429 错误需指数退避重试 | **完全一致**：账号级总限流 3000 QPM；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM；错误处理规范相同 |
| **控制台支持** | 无独立控制台入口；依赖 API 调用与日志排查 | 提供完整控制台页面（`/memory/list`），支持：<br>- 记忆库创建/管理<br>- 记忆规则配置（提取时机、类型、模板绑定）<br>- 默认项目规则（180天有效期）预置与编辑<br>- 实时记忆浏览与调试 |

## 各方案的适用场景建议

- ✅ **优先选用「记忆库（Memory Library）」方案**  
  适用于**所有新项目开发与存量应用升级**。其优势在于：
  - **产品化成熟**：控制台可视化配置、规则引擎、多模态支持、Agent Harness 与插件双路径集成；
  - **开发效率高**：无需手动构造 `skill` 结构，规则可自动识别技能意图；默认记忆库开箱即用；
  - **架构统一**：API 命名空间规整（`/api/v2/apps/memory/`），文档与 SDK 全面覆盖；
  - **长期演进保障**：作为百炼平台唯一维护的长期记忆服务，将持续获得新特性（如向量模型升级、RAG 增强、隐私合规增强）。

- ⚠️ **仅在以下情况参考「长期记忆 new」API 文档**  
  - 进行**底层协议调试或问题排查**（如分析 `request_id` 日志、理解 `event` 状态机）；
  - **存量系统尚未完成迁移**，需临时适配旧接口路径（注意：该路径实际指向记忆库服务后端，非独立服务）；
  - 开发**高度定制化中间件**，需精确控制异步任务生命周期（如自定义轮询策略、事件聚合）。

> 📌 **重要提醒**：不存在“两个独立服务供选择”的技术现实。所谓“长期记忆 new”是记忆库服务的 API 层技术规格说明，而非竞品方案。开发者不应在二者间做二选一决策，而应将“记忆库”作为标准方案，将“长期记忆 new 文档”视为其权威 API 参考手册。

## 面向开发者的技术选型参考

| 选型考量 | 推荐动作 | 说明 |
|----------|----------|------|
| **新项目启动** | 直接使用 **记忆库（Memory Library）** 控制台 + `/api/v2/apps/memory/` API | 从开通、配置规则、调用 Add/Search 到调试画像，全程有图形界面引导与示例代码，降低接入门槛 |
| **Agent 智能体开发** | 优先启用 **Agent Harness 集成模式** | 在百炼控制台智能体配置页勾选“启用记忆库”，系统自动注入检索结果至 Prompt，无需修改业务代码 |
| **工作流/插件集成** | 使用 **OpenClaw 等官方插件** | 插件已封装 Add/Search 调用、错误重试、`min_score` 自适应等逻辑，符合生产环境健壮性要求 |
| **需要多模态记忆** | 必选记忆库方案 | “长期记忆 new”文档未提及多模态支持，而记忆库明确支持 `attachments` 字段上传图像/音频并提取特征 |
| **对技能记忆有强结构化需求** | 配置**记忆规则 + 技能模板**，而非手动构造 `custom_content` | 记忆库规则引擎可基于关键词、正则、LLM 分类器自动识别“设置提醒”“生成报告”等技能意图，并关联预设模板，比手动构造更可靠、可维护 |
| **性能敏感场景（低延迟写入）** | 同步调用 `/api/v2/apps/memory/add`，并设置 `plan_version="lite"` | Lite 版本跳过 Rerank，响应更快；若需更高精度，可异步调用后监听 `event_id`，平衡延迟与质量 |

**总结一句话选型原则**：  
> **以「记忆库」为唯一产品入口，以「长期记忆 new」文档为 API 实现参考——不选方案，只用服务；不比功能，只看集成效率与演进可持续性。**

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


