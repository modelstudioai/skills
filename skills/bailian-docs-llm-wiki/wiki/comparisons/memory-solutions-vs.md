# 长期记忆与记忆库对比

百炼平台提供两套紧密关联但定位不同的记忆能力：「长期记忆（新）API」和「记忆库（Memory Library）」。前者是一组 RESTful 接口，聚焦于记忆片段与用户画像的增删改查；后者是更高层的产品概念，涵盖记忆库管理、记忆规则配置以及多种接入方式（API 直连、OpenClaw 插件、控制台可视化管理）。本文从开发者技术选型角度对两者进行对比，帮助你快速判断应使用哪一套能力。

## 关键维度对比

| 维度 | 长期记忆（新）API | 记忆库（Memory Library） |
| --- | --- | --- |
| 定位 | 底层 RESTful API 集合，提供记忆片段与用户画像的 CRUD 操作 | 产品级概念，包含记忆库、记忆规则、接入方式与控制台管理的完整体系 |
| 文档归属 | API 参考（application-api-reference） | 用户指南（application-user-guide） |
| Base URL | `https://dashscope.aliyuncs.com/api/v2/apps/memory/` | 同上（API 直连时使用相同端点） |
| 认证方式 | Header `Authorization: Bearer $DASHSCOPE_API_KEY` | 同左（API 直连）；OpenClaw 插件在配置中填 `apiKey` |
| 接入方式 | 仅 HTTP API 直连 | API 直连 + OpenClaw 记忆插件（零侵入）+ 控制台可视化管理 |
| 记忆类型 | 记忆片段（自动提取）+ 用户画像（profile schema） | 记忆片段 + 用户画像（同左，但额外支持记忆规则配置） |
| 记忆有效期 | 生成的记忆片段与用户画像暂无失效日期 | 控制台默认规则预置 180 天有效期，可配置 7/30/180 天或永不过期；API 直写且不指定 `project_id` 时使用默认规则 |
| 核心接口 | AddMemory、SearchMemory、ListMemory、DeleteMemory、UpdateMemory、CreateProfileSchema、ListProfileSchemas、GetUserProfile 等 | 复用长期记忆 API 全部接口，并叠加记忆库 / 记忆规则管理能力 |
| 限流 | 全部接口合计 3000 QPM；AddMemory 120 QPM；SearchMemory 300 QPM | 同左（底层共用同一 API 网关） |
| 编程语言支持 | cURL / 任意 HTTP 客户端 | cURL + Python `agentscope-runtime` 封装类 + OpenClaw 插件 |
| OpenClaw 集成 | 不直接提供 | 提供 `@modelstudio/modelstudio-memory-for-openclaw` 插件，通过 `before_agent_start` / `agent_end` 钩子实现自动捕获与召回 |
| 控制台管理 | 不涉及 | 支持在百炼控制台可视化管理记忆库、记忆规则与记忆内容 |
| 记忆库隔离 | 通过 `memory_library_id` 参数区分，不传则使用默认记忆库 | 每个账号自带一个不可删除的默认记忆库，可创建多个自定义记忆库 |
| 记忆规则 | 通过 `project_id` 指定规则，不传使用默认 | 支持自定义记忆片段规则（有效期、提取策略等），预置默认项目规则 |

## 适用场景建议

### 选择长期记忆（新）API 的场景

- **已有自有 Agent 框架**，只需调用 HTTP 接口完成记忆存取，不需要控制台可视化管理。
- **需要对记忆片段做精细 CRUD**，例如单独 Update、Delete 某条记忆，或管理画像模板的完整生命周期。
- **需要自定义记忆有效期**为永不过期，且通过 API 直写而不依赖控制台规则配置。
- **对限流有明确预期**，需要按 120/300 QPM 的接口级限流做容量规划。

### 选择记忆库（Memory Library）的场景

- **希望零侵入接入**，使用 OpenClaw Agent 且不愿手动编排记忆读写逻辑——安装插件后自动完成捕获与召回。
- **需要在控制台可视化管理**记忆库与记忆规则，包括调整有效期（7/30/180 天或永不过期）、查看记忆内容、配置提取策略。
- **使用 Python 开发**，希望用 `agentscope-runtime` 封装类简化调用，而非手写 HTTP 请求。
- **需要多记忆库隔离**，希望按业务线或场景创建不同记忆库并分别配置规则。
- **团队协作场景**，需要非开发人员通过控制台查看和管理记忆数据。

## 技术选型建议

两套能力并非互斥，而是分层关系：记忆库是产品层概念，长期记忆 API 是其底层接口层。实际开发中常见的做法是：

1. **快速验证阶段**：先用 API 直连方式（即长期记忆 API）跑通 AddMemory → SearchMemory 的核心链路，验证记忆提取与召回效果。
2. **生产化阶段**：在控制台创建专属记忆库并配置记忆规则（有效期、提取策略），通过 `memory_library_id` 和 `project_id` 参数将 API 调用绑定到对应规则。
3. **OpenClaw 场景**：如果 Agent 基于 OpenClaw 构建，直接安装记忆插件即可获得完整的自动捕获/召回能力，无需手动编排 API 调用时序。

无论选择哪种路径，底层的记忆存储、语义检索和画像提取引擎是同一套，差异仅在接入方式和管理粒度上。根据团队技术栈和运维需求选择即可。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


