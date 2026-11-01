# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**结构化、可检索、跨会话持久化的用户与业务知识管理服务**，用于在 Agent 运行过程中持续积累、组织和复用事实性信息（如用户偏好、历史决策）与能力型知识（如操作流程、领域技能），从而支撑个性化、连贯且具备“成长性”的智能体行为。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 上下文（[agent context](../guides/agent-context.md)）中作为核心模块启用**：通过 `memory.enabled: true` 开启会话级（`session`）或用户级（`user`）记忆回溯，系统自动将对话历史向量化并存入默认记忆库，在每次调用时按语义相似度检索最近 10 轮相关上下文注入 prompt，无需开发者手动拼接历史。
  
- **独立记忆服务（[long term memory new](../api/long-term-memory-new.md)）中作为底层能力直接调用**：支持细粒度控制——可写入 `observation`（事实记忆，如“用户姓李，忌口花生”）、`skill`（技能记忆，如“能生成周报PPT”），并结合 `profile_schema` 自动抽取用户画像字段；适用于需强一致性、多项目隔离（`project_ids`）、异步批量处理或导出为可复用技能模块的高阶场景。

- **Flow Agent 与 Sandbox 模式中作为状态扩展能力集成**：虽 Flow Agent API 中“长期记忆（旧）”已被标记为历史版本，但新版推荐方式是通过 `context.memory` 字段传入 `session_id` 或 `user_id`，由平台统一调度；Sandbox 模式下则可直接调用 LTM SDK（如 `MemoryClient.add()` / `.search()`）实现自定义记忆生命周期管理。

- **不用于 Managed Agent 的显式配置**：Managed Agent 仅隐式依赖内置记忆机制维持单次会话连贯性，不开放 LTM 的读写接口或参数配置，开发者无法干预其存储结构或检索逻辑。

> ✅ 最佳实践建议：  
> - 简单个性化 → 启用 `agent context` 中的 `memory.enabled`；  
> - 多业务域/强数据治理 → 直接调用 `long term memory new` API，配合 `project_ids` 和 `plan_version=pro` 实现精准过滤与重排序；  
> - 需混合外部状态（如数据库+记忆）→ 在 Sandbox 中组合使用 LTM SDK 与自定义 I/O。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 注意事项 |
|------|----------|------|----------|
| `memory.enabled` | [agent context](../guides/agent-context.md) | 启用记忆回溯开关 | 必须同时指定 `memory.type: session` 或 `user`；默认不启用 |
| `memory.session_id` / `memory.user_id` | [agent context](../guides/agent-context.md) API 请求体 | 标识会话或用户维度 | `session_id` 有效期 1 小时；`user_id` 需业务侧稳定生成（如登录 ID） |
| `user_id` | [long term memory new](../api/long-term-memory-new.md) API | 用户级隔离主键 | 所有写入/检索接口必填；同一 `user_id` 下记忆默认不可跨项目访问 |
| `project_ids` | [long term memory new](../api/long-term-memory-new.md) API | 业务项目分组标识（数组，最多 5 个） | 与 `project_id`（单值）互斥；用于隔离不同 Agent 应用的记忆空间 |
| `plan_version` | long term memory new API | 计费与能力策略（`pro` / `lite`） | `pro` 支持 `min_score` 过滤与 Rerank；`lite` 版本忽略 `min_score` 参数 |
| `memory_types` | `/memory_nodes/search` 接口 | 指定检索类型（`["observation", "skill"]`） | 可组合过滤，提升检索精度；默认返回全部类型 |
| `top_k` | `/memory_nodes/search` 接口 | 返回最相关记忆节点数 | 默认 5，最大支持 20；注意与模型上下文长度协同控制 |

> ⚠️ 重要限制：  
> - 单次 `search` 最多返回 20 条记忆，`add-async` 批量写入单次上限 100 条；  
> - `user_id` + `project_ids` 组合构成唯一命名空间，未指定 `project_ids` 时记忆归属默认项目；  
> - 删除操作（`DELETE /memory_nodes/{id}`）不可逆，请务必校验 `id` 后再执行。

## 面向开发者，简洁实用

- **快速启用**：在 `agent_config.yaml` 中添加  
  ```yaml
  memory:
    enabled: true
    type: user
  ```
  并在 API 调用时传入 `"memory": {"user_id": "u_123"}` —— 即刻获得用户级记忆回溯能力。

- **精准检索**：调用 LTM Search API 时，用自然语言提问作为 `messages` 输入，并限定类型与阈值：
  ```bash
  curl -X POST https://<workspace-id>.cn-beijing.maas.aliyuncs.com/api/v2/memory_nodes/search \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d '{
          "user_id": "u_123",
          "project_ids": ["proj-crm"],
          "messages": [{"role":"user","content":"他上次订的是什么咖啡？"}],
          "memory_types": ["observation"],
          "top_k": 3,
          "min_score": 0.75
        }'
  ```

- **避免踩坑**：  
  - ❌ 不要混用 `project_id` 和 `project_ids`；  
  - ❌ 不要在 `lite` 版本中依赖 `min_score` 过滤；  
  - ✅ 所有 LTM 接口均需 `DASHSCOPE_API_KEY` 鉴权，**不支持 AccessKey**；  
  - ✅ Sandbox 中推荐使用 `agentscope-runtime` SDK 封装调用，自动处理重试与错误码映射。

- **调试提示**：若记忆未被检索到，优先检查 `user_id` 是否一致、`project_ids` 是否匹配、`plan_version` 是否为 `pro`，以及查询 `messages` 内容是否足够具象（避免“之前的事”等模糊表述）。

## 关联主题页

- [agent context](../guides/agent-context.md)
- [long term memory new](../api/long-term-memory-new.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent development](../guides/agent-development.md)
- [application support](../guides/application-support.md)


