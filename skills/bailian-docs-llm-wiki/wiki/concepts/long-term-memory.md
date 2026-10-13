# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、跨会话、可检索的记忆管理能力，用于持久化存储用户事实性行为片段（Observation/Skill）与结构化画像（Profile），支撑 Agent 的个性化响应、上下文延续与技能复用。它独立于单次推理请求生命周期，通过统一 DashScope API 网关提供写入、语义搜索、更新与导出能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 开发（Managed / Flow / Sandbox）**：作为上下文增强的核心组件，Agent 可在运行时主动调用长期记忆 API（如 `SearchMemory`）注入相关事实或用户画像，替代冗长的 prompt 注入，显著提升响应准确性与个性化水平。例如，Flow Agent 在处理用户咨询前，先根据 `user_id` 检索其历史偏好与技能标签，动态拼接至 LLM 输入；Sandbox 中可通过 `agentscope_runtime.tools.modelstudio_memory` SDK 直接集成，实现“记忆感知”的自定义逻辑。

- **Flow Agent API 调用**：通过请求体中的 `memory_id` 参数（推荐 UUID v4 格式）显式关联一次会话与长期记忆实例，使多次调用可共享同一记忆上下文。该 `memory_id` 本身不存储数据，而是作为业务侧标识，用于组织 `user_id` + `project_ids` 维度下的记忆查询与写入，实现会话级状态延续（注意：旧版基于 session ID 的记忆机制已废弃，必须使用新长期记忆 API）。

- **记忆建模与运营**：开发者可分离构建两类记忆：
  - **事实记忆（Fragments）**：以 `observation`（如“用户三次询问退款流程”）或 `skill`（如“自动填写退货单”执行模板）形式存入，支持语义搜索与批量导出，用于行为分析与自动化流程沉淀；
  - **用户画像（Profiles）**：基于预定义 schema（如 `basic_info`, `purchase_preference`）从对话消息中自动抽取结构化属性，需在 `AddMemory` 请求中显式传入 `profile_schema` 才能触发抽取，后续通过 `GetUserProfile` 接口获取标准化结果。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | Query / Body | string | 是 | 唯一标识记忆归属主体，所有读写操作均强制隔离，建议使用业务系统用户 ID（如 `uid_123456`） |
| `memory_library_id` | Query / Body | string | 否 | 指定记忆库，不传则写入/检索默认库；可用于多租户或环境隔离（如 `prod-memory-lib`, `test-memory-lib`） |
| `project_ids` | Body | array of string | 否 | 项目级二级隔离，最多 5 个字符串，与 `custom_content` 互斥；适用于同一用户在不同业务线（如电商/客服）的记忆分区 |
| `plan_version` | Body | string | 否 | 检索策略版本：`pro`（支持 `min_score` 过滤、高精度向量搜索）或 `lite`（基础 BM25+向量混合）；默认 `pro` |
| `min_score` | Body | number | 否 | 仅 `plan_version=pro` 生效，语义搜索相关性阈值（0.0–1.0），默认 `0.3`；低于此值的结果将被过滤 |
| `extract_mode` | Body | string | 否 | 抽取控制：`profile_only` 表示仅执行画像提取（需同时传 `profile_schema` 和 `messages`），跳过事实记忆写入 |

> ⚠️ 注意：`profile_schema` 是触发用户画像抽取的**隐式必填项**——若在 `AddMemory` 中未传该字段，即使 `messages` 包含足够信息，画像也不会生成。务必在首次写入含画像意图的数据时显式指定。

## 面向开发者，简洁实用

- **快速上手**：优先使用 `agentscope_runtime.tools.modelstudio_memory` SDK（已封装鉴权、重试、错误分类），避免手动构造 HTTP 请求；
- **写入建议**：
  - 高实时性场景（如对话中即时记录）→ 用同步 `/add`；
  - 批量导入、含 Skill/Profile 多类型抽取 → 用异步 `/add-async`，轮询 `/events/{event_id}` 获取结果；
- **检索建议**：`SearchMemory` 请求中 `messages` 字段应为自然语言查询句（如“用户最近投诉过什么？”），而非原始日志；`top_k` 建议设为 `3–10`，避免噪声干扰；
- **限流应对**：账号级总限流 3000 QPM，`/add` 单独限流 120 QPM；遇 `429` 错误请按 1s → 2s → 4s 指数退避重试；
- **调试技巧**：结合 `enable_tracing=true` 调用 Flow Agent，检查 `SearchMemory` 工具调用的输入/输出与耗时，验证记忆召回质量。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent development](../guides/agent-development.md)
- [flow agent api](../api/flow-agent-api.md)


