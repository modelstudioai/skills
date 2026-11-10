# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**结构化、可检索、生命周期可控的记忆管理服务**，用于持久化存储用户事实、可复用技能与结构化画像，并在 Agent 推理过程中按需注入上下文。它不是简单的键值缓存，而是融合语义理解、类型建模与安全治理的生产级记忆基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

| 场景 | 作用方式 | 关键特点 |
|------|----------|----------|
| **新版长期记忆 API（推荐）** | 通过 `AddMemory` / `AddMemoryAsync` 写入，`SearchMemory` 检索；支持 `observation`（事实）、`skill`（流程化能力）、`user_profile`（结构化画像）三类记忆节点 | ✅ 异步优先：`intelligent` 抽取、技能/画像写入必须用 `AddMemoryAsync`<br>✅ 多模态感知：当项目启用多模态时，`image_url` 可参与语义抽取<br>✅ 模型无关：记忆独立于 LLM 存储与更新，所有 Agent 均可复用 |
| **Flow Agent（旧版）** | 作为组件类 OpenAPI 使用，通过 `CreateMemory` 创建记忆体，再以 `memoryId` 注入到 Flow Agent 调用请求中供智能体引用 | ⚠️ 已标记为遗留方案：<br>– 不支持用户画像与技能建模<br>– 内容长度严格限制（1–200 字符）<br>– 鉴权方式为 AccessKey 签名（非 API Key）<br>– 所有接口限流为 ≥1 秒间隔 |
| **Agent Context（运行时上下文）** | 作为 `context_sources` 类型之一（`type: "memory"`），在 Agent 对话时动态加载匹配 `filter`（如 `{"user_id": "{{user_id}}"}`）的记忆片段 | ✅ 自动向量化检索 + 相关性截断<br>✅ 支持 TTL 缓存（`context_ttl_seconds`）<br>✅ 与其他上下文源（RAG/Connector）统一拼接、去重、过滤后送入模型<br>✅ 单次最多 5 个 memory source，超限返回 400 |
| **Agent Governance（治理）** | 记忆读写操作自动上报为 Trace Span，受内容安全策略（默认防护）实时检测；记忆内容变更可触发评测集回溯与优化路径生成 | ✅ 所有 `memory` 类操作（写入/检索/导出）均被可观测性链路捕获<br>✅ 默认开启记忆内容安全扫描（防敏感信息泄露、越权访问等）<br>✅ 记忆质量可纳入轨迹评测（如“是否准确调用历史技能”） |

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 开发建议 |
|------|----------|------|-----------|
| `user_id` | 全场景必填 | 子用户唯一标识，用于跨项目/跨应用隔离记忆 | 始终传入真实业务 ID（如 `uid_12345`），避免使用占位符 |
| `extract_mode` | 新版 API 写入 | 取值：`efficient`（低延迟）、`intelligent`（高精度，需异步）或 `profile_only`（仅画像） | `intelligent` 或含 `profile_schema` 时，**必须用 `AddMemoryAsync`**；否则可能超时或丢失结果 |
| `profile_schema` | 新版 API（画像） | 用户画像模板 ID，需提前创建；传入后才触发画像字段抽取 | 创建模板时明确字段类型（string/number/boolean/array）与是否索引，影响后续检索效率 |
| `plan_version` | 新版 API 检索 | `lite`（基础向量搜索）或 `pro`（启用 Rerank、`min_score` 过滤） | 生产环境推荐 `pro`；`min_score` 建议设为 `0.6`~`0.8`，避免噪声召回 |
| `context_sources.type: "memory"` | Agent Context | 在 YAML/API 中声明 memory 上下文源 | 必须配合 `filter` 使用（如 `{user_id: "{{user_id}}"}`），否则无法定位记忆 |
| `context_ttl_seconds` | Agent Context | memory 类上下文的本地缓存有效期（秒） | 高频会话可设为 `300`（5 分钟）；低频或强一致性场景设为 `0`（禁用缓存） |
| `memoryId` | Flow Agent（旧） | 旧版记忆体唯一 ID，由 `CreateMemory` 返回 | 仅用于兼容旧系统；新项目请勿依赖此 ID，改用新版 `memory_library_id` + `user_id` 组合 |

> 💡 **开发者提示**：  
> - **新项目一律使用新版长期记忆 API**（`/api/v2/apps/memory`），旧版 Flow Agent 记忆接口已停止功能演进；  
> - 技能记忆（`skill`）需显式提供 `skill_name`、`skill_description`、`skill_tags`，便于后续 `GET /skill/export/{id}` 导出与复用；  
> - 检索时若未指定 `memory_types`，默认返回全部类型；建议显式传入 `["observation", "skill"]` 提升精度与性能；  
> - 所有记忆内容均经平台默认安全策略扫描，**禁止在 `custom_content` 或 `messages` 中硬编码密钥、[Token](token.md)、身份证号等敏感字段**。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent context](../guides/agent-context.md)
- [agent governance](../guides/agent-governance.md)


