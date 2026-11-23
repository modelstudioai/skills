# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的**结构化、用户级、跨会话持久化**的记忆管理服务，用于存储和检索与用户身份强绑定的稳定知识，包括事实性信息（如偏好、日程）、可复用技能（如工具调用流程）及结构化用户画像。它独立于单次会话生命周期，通过 `user_id` 实现严格隔离，是构建个性化、有状态、可进化的 Agent 的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 上下文（Agent Context）中作为 User Memory 使用**：  
  当在 `context_config.memory` 中配置 `"type": "user"` 并传入 `user_id` 时，平台自动从长期记忆服务中检索匹配该用户的 `observation` 和 `skill` 类型记忆节点，并将其注入模型 prompt。若未提供 `user_id`，则退化为仅使用会话级短期记忆（Session Memory），长期记忆不生效。

- **Agent 开发中作为状态增强能力**：  
  在 Managed/Flow/Sandbox Agent 中，可通过 SDK（如 `agentscope-runtime`）或直接调用 Long Term Memory API 主动写入或查询记忆。例如：在用户完成一次订单后，调用 `/add-async` 写入 `observation` 类型记忆（“用户偏好无糖饮品”）；后续对话中，Agent 可基于该记忆主动推荐相关商品。

- **Skill 与 MCP 能力协同中承载上下文依据**：  
  技能（Skill）执行结果（如解析 PDF 得到的用户合同条款）可被结构化为 `skill` 或 `observation` 记忆写入长期记忆；后续 MCP 服务（如“生成续签提醒”）可基于这些记忆触发精准动作，实现“记忆驱动的行为闭环”。

- **Agent 治理中作为可观测与评测的数据源**：  
  所有长期记忆的读写操作（`/add`, `/add-async`, `/search` 等）均被统一采集至 Trace 链路，可在「应用观测」中查看记忆检索耗时、命中率、`min_score` 过滤效果等指标；记忆内容本身也可作为评测集输入，用于评估 Agent 对历史信息的回忆准确性与一致性。

- **Agent Store 中支撑 Skill 的个性化执行**：  
  自定义 Skill（如“生成个性化周报”）可在执行时主动查询长期记忆中的 `user_profile`，动态填充姓名、部门、KPI 目标等字段，实现真正意义上的“千人千面”输出。

## 关键参数和配置

| 参数 | 说明 | 必填性 | 典型值 | 注意事项 |
|------|------|--------|--------|----------|
| `user_id` | **全局必需**，用于唯一标识用户并隔离记忆空间 | 所有接口必填 | `"u_123456"` | 若缺失，写入失败或检索返回空；Agent Context 中未传则不启用长期记忆 |
| `memory_types` | 检索/写入时指定记忆类型，支持 `["observation", "skill", "user_profile"]` | `search` 接口可选（默认 `["observation"]`） | `["observation", "skill"]` | 类型决定语义向量建模方式与检索策略，不可混用 |
| `extract_mode` | 控制记忆抽取行为：`efficient`（低延迟，适合实时写入）、`intelligent`（高精度，需异步） | 条件必填（启用画像或高精度抽取时） | `"intelligent"` | 同步接口 `/add` **仅支持 `efficient` 模式**；`intelligent` 模式必须用 `/add-async` |
| `profile_schema` | 用户画像模板 ID，用于触发 `user_profile` 类型抽取与结构化存储 | 仅当写入/更新画像时必填 | `"50edf54eaa5842e891d959ae115205be"` | 需先通过 `CreateProfileSchema` 创建，支持动态增删字段 |
| `plan_version` | 决定能力等级与计费：`pro`（支持 `min_score`、Rerank、高级过滤）、`lite`（基础向量检索） | `search` / `profile_schema` 相关接口可选，默认 `pro` | `"pro"` | `min_score` 仅在 `plan_version=pro` 下生效；`lite` 不支持该参数 |
| `top_k` / `min_score` | 检索参数：最大召回数（默认 10）、最小相似度阈值（默认 `0.3`） | 均为可选 | `top_k=5`, `min_score=0.6` | `min_score` 是 `pro` 版本关键过滤手段，可显著提升结果相关性 |
| `project_id` / `project_ids` | 项目级隔离标识，用于多业务线/多 Agent 共享同一 `user_id` 时的二级分组 | 可选（影响记忆可见范围） | `["proj-crm", "proj-support"]` | `project_ids` 最多 5 个，与 `project_id` 互斥；不传则归属默认项目 |

## 面向开发者，简洁实用

- ✅ **默认首选异步写入**：生产环境一律使用 `/add-async`，避免同步超时风险；轮询 `/events/{event_id}` 获取结果，超时建议设为 30s。
- ✅ **画像必须先建模**：使用 `user_profile` 前，务必调用 `POST /profile_schemas` 创建 schema，否则写入失败。
- ✅ **检索务必加过滤**：`search` 接口默认只查 `observation`，如需技能或画像，请显式传 `memory_types`。
- ✅ **`user_id` 是生命线**：确保所有调用（API / SDK / Agent Context）中 `user_id` 一致且稳定（推荐使用业务系统 UID，而非临时 session ID）。
- ⚠️ **避免滥用 `project_id`**：除非明确需要多项目隔离，否则不传以降低复杂度；`project_id` 不参与语义检索，仅作逻辑分组。
- ⚠️ **`min_score` 不是越高越好**：设为 `0.8+` 可能导致零召回；建议从 `0.5` 起调优，结合业务场景平衡精度与覆盖率。
- 🛠️ **调试技巧**：用 `GET /memory_nodes?user_id=xxx&memory_type=observation` 快速浏览用户当前记忆快照，验证写入是否成功。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [agent governance](../guides/agent-governance.md)
- [agent development](../guides/agent-development.md)
- [agent store](../guides/agent-store.md)


