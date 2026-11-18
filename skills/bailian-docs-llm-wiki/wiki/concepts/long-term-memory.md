# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**结构化、用户级、可检索的持久化记忆服务**，用于跨会话、跨请求地存储和复用关键业务信息，包括事实性事件、可复用技能与结构化用户画像。它独立于模型参数与会话上下文，通过统一 API 管理生命周期，是构建个性化、状态感知型 Agent 的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 推理增强（`agent context`）**：  
  当 `context_config.memory.enabled = true`（默认开启）时，平台自动为当前 `user_id` 检索匹配的长期记忆节点（`observation`/`skill`/`user_profile`），并按相关性注入到模型 prompt 中，作为上下文补充。该过程对开发者透明，无需手动调用检索接口，但需确保记忆已预先写入且 `user_id` 一致。

- **结构化记忆管理（`long term memory new`）**：  
  通过 RESTful API 或 `agentscope-runtime` SDK 主动写入、搜索、更新记忆。典型流程为：  
  - 使用 `AddMemoryAsync` 从对话消息或工具调用中抽取 `observation`（如“用户下周出差”）或 `skill`（如“自动生成会议纪要”）；  
  - 通过 `profile_schema` 定义并写入 `user_profile`（如职业、偏好、设备信息）；  
  - 调用 `/memory_nodes/search` 按 `user_id` + `messages` 语义检索最相关记忆，支持 `top_k` 和 `min_score` 过滤。

- **Flow Agent 开发（`flow agent api`）**：  
  注意区分新旧版本：  
  - **旧版 `Memory` 接口**（OpenAPI 路径含 `/memory`）仅支持基础 `MemoryNode` 增删改查，**不支持用户画像、技能抽取与多模态内容**，已标记为“旧”，不推荐新项目使用；  
  - **新版 `long term memory new`**（独立 endpoint，基于业务空间域名）是当前唯一推荐方案，全面覆盖三类记忆类型与异步抽取能力。

- **Agent 治理与可观测性（`agent governance`）**：  
  所有长期记忆的读写操作（`AddMemory`, `SearchMemory`, `GetUserProfile` 等）均被自动捕获为 Trace 事件，出现在观测面板的 “Memory” 标签页下，包含耗时、返回节点数、`user_id`、`project_id` 等元数据，可用于分析记忆命中率、冷热分布及性能瓶颈。

- **Sandbox/Managed/Flow Agent 开发（`agent development`）**：  
  - Sandbox Agent 可直接调用 `agentscope-runtime` SDK 写入/检索记忆；  
  - Managed Agent 可在 YAML 中配置 `memory_strategy: "summary"` 并结合 `user_id` 实现用户级记忆回溯；  
  - Flow Agent 可在 Python 脚本节点中集成记忆 SDK，实现条件化记忆更新（如仅当用户明确授权时写入敏感画像）。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 场景 |
|------|------|------|------|------|
| `user_id` | string | ✅ | 用户唯一标识，用于隔离不同用户的记忆空间；必须与 `agent context` 调用中的 `user_id` 一致才能生效 | 全部 |
| `project_id` / `project_ids` | string / string[] | ⚠️（技能/事实抽取必需） | 绑定记忆抽取规则：指定后触发 `observation` 或 `skill` 自动抽取；未指定则仅支持 `custom_content` 直接写入 | 写入 |
| `profile_schema` | string | ⚠️（用户画像写入必需） | 用户画像模板 ID；需提前通过 `/profile_schemas` 创建；启用后自动解析 `messages` 中符合 schema 的字段 | 写入 |
| `extract_mode=profile_only` | string | ❌（可选） | 强制仅执行用户画像抽取，忽略 `observation`/`skill`；此时 `messages` 和 `profile_schema` 均为必填 | 写入 |
| `top_k` | integer | ❌（默认 `10`） | 检索返回的最大记忆节点数 | 检索 |
| `min_score` | float | ❌（默认 `0.3`） | 最小相似度阈值；**仅 `plan_version=pro` 时生效** | 检索 |
| `plan_version` | string | ❌（默认 `lite`） | 检索策略：`lite`（基础向量检索）、`pro`（启用 Rerank + `min_score` 过滤） | 检索 |
| `memory_types` | string[] | ❌（默认 `["observation"]`） | 指定检索的记忆类型，如 `["observation", "skill"]` | 检索 |

> **注意**：`user_id` 是长期记忆作用域的唯一锚点，务必在所有相关调用（Agent 推理、记忆写入、检索）中保持一致；跨 `session_id` 的记忆共享天然成立，无需额外配置。

## 面向开发者，简洁实用

- ✅ **首选异步写入**：用 `AddMemoryAsync` 替代 `AddMemory`，避免同步超时；轮询 `GET /events/{event_id}` 获取结果，适合生产环境。
- ✅ **画像先建模再写入**：调用 `/profile_schemas` 创建 schema 后，再在 `AddMemoryAsync` 中传 `profile_schema`，否则画像写入失败。
- ✅ **检索即插即用**：在 `agent context` 中启用 `memory` 即可自动注入；若需精细控制（如只召回技能），请改用 SDK 手动调用 `/memory_nodes/search` 并设置 `memory_types`。
- ⚠️ **鉴权严格分离**：新版 LTM 使用 `DASHSCOPE_API_KEY` + 业务空间 endpoint；旧版 Flow Agent 的 `Memory` 接口使用 AccessKey 签名 —— 切勿混用。
- ⚠️ **容量与限流监控**：单用户长期记忆上限为 1MB；全接口 QPM 总限 3000，其中 `search` ≤ 300 QPM，建议在高并发场景添加重试与降级逻辑。
- 🚀 **快速起步命令**：
  ```bash
  # 设置环境变量（替换为你的 WorkspaceId 和 API Key）
  export MEMORY_ENDPOINT="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"
  export DASHSCOPE_API_KEY="sk-xxxx"

  # 异步写入一条事实记忆
  curl -X POST "$MEMORY_ENDPOINT/add-async" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "user_id": "u123",
          "project_id": "proj-fact-default",
          "messages": [{"role":"user","content":"我明天要去上海开会"}]
        }'

  # 检索该用户的相关记忆
  curl -X POST "$MEMORY_ENDPOINT/memory_nodes/search" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "user_id": "u123",
          "messages": [{"role":"user","content":"帮我安排会议行程"}],
          "top_k": 5,
          "plan_version": "pro",
          "min_score": 0.4
        }'
  ```

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent development](../guides/agent-development.md)
- [agent governance](../guides/agent-governance.md)


