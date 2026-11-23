# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的**结构化、可检索、跨会话持久化的记忆管理服务**，用于系统性地存储和复用事实信息、技能知识与用户画像等高价值语义单元，而非简单缓存对话历史。它独立于会话生命周期存在，支持按语义意图精准写入、过滤检索与策略化更新，是构建具备持续学习能力与个性化认知的智能体（Agent）的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agents（托管智能体）**：通过 `memory_store_id` 显式绑定长期记忆实例，Agent 在每次 `/sessions/{id}/messages` 调用中自动读取关联记忆库中的相关节点（如用户偏好、历史决策），实现上下文感知的响应生成；Memory Store 默认 TTL 为 7 天，适用于短期任务闭环，**如需永久留存，请使用 `long-term-memory-new` API 管理记忆库**。
  
- **Agent Context（上下文注入）**：在 Agent 运行请求的 `context.memory_library_ids` 字段中传入记忆库 ID（如 `"ml-abc123"`），平台将自动融合该库中匹配 `user_id` 的记忆节点（`observation`/`skill`）作为上下文注入模型提示词，**无需修改 prompt 或业务逻辑**，适用于客服、投顾等需强状态延续的场景。

- **Agent 开发（Sandbox / Flow 模式）**：开发者可通过 `bailian-sdk` 或 RESTful API 直接调用 `AddMemoryAsync` 和 `SearchMemory`，在自定义 `Agent.run()` 中实现记忆驱动的决策链（例如：先查“用户上次投诉原因”，再匹配对应 SOP 技能记忆，最后生成回复）。Sandbox 模式下可完全控制记忆抽取时机、内容结构与更新策略。

- **CLI 工具链**：通过 `bl memory add`（同步）或 `bl memory add-async`（推荐）命令批量写入记忆；使用 `bl memory search --user-id user_001 --memory-types observation,skill` 快速验证记忆可用性，适用于 DevOps 自动化测试与数据管道集成。

- **技能与画像协同**：长期记忆支持三类结构化节点协同：
  - `observation`：记录具体事件（如“用户于2024-09-15退订会员”），用于行为回溯；
  - `skill`：封装可复用流程（如“退订挽留话术”），导出后可被多个 Agent 共享调用；
  - `user_profile`：基于预设模板从对话中抽取结构化属性（如 `age_group: "25-34"`, `preferred_contact: "wechat"`），首次写入后需异步等待画像生成完成，再通过 `GET /profile` 获取。

> ✅ 实践建议：优先选用 `AddMemoryAsync`（而非 `AddMemory`）进行记忆写入——它支持多项目并行、技能抽取与画像联合提取，且不因抽取耗时导致超时；`AddMemory` 仅适用于低延迟、无抽取需求的简单写入场景。

## 关键参数和配置

| 参数 | 说明 | 是否必填 | 典型值 | 注意事项 |
|------|------|----------|--------|----------|
| `user_id` | 子用户唯一标识，用于跨用户记忆隔离与检索 | 所有接口必填 | `"user_001"` | 必须与 Agent 请求中的 `user_id` 一致，否则无法命中 |
| `memory_library_id` | 记忆库 ID；不传则使用默认库 | 可选（默认库） | `"ml-abc123"` | 建议显式指定，便于资源治理与权限控制 |
| `project_ids` | 项目 ID 数组（最多 5 个），用于二级隔离与抽取规则路由 | 写入/检索时可选 | `["proj-sales", "proj-support"]` | 与 `project_id` 互斥；`AddMemoryAsync` 和 `SearchMemory` 支持 |
| `profile_schema` | 用户画像模板 ID，传入后触发画像抽取 | 仅画像写入必填 | `"50edf54eaa5842e891d959ae115205be"` | 需先调用 `POST /profile/schema` 创建模板 |
| `memory_types` | `SearchMemory` 中指定检索类型，默认 `["observation"]` | 可选 | `["observation", "skill"]` | 不支持 `user_profile` 类型直接检索，需用 `GET /profile` |
| `plan_version` | 检索计费策略：`pro`（支持 `min_score`、Rerank）或 `lite`（基础向量搜索） | `SearchMemory` 默认 `pro` | `"pro"` | `pro` 版本需额外计费，但召回精度与可控性显著提升 |
| `top_k` / `min_score` | 检索结果数量上限 / 最小相似度阈值（`pro` 版本） | 可选 | `top_k=5`, `min_score=0.65` | `min_score` 有效过滤噪声，避免低置信度记忆干扰 |

## 面向开发者，简洁实用

- **快速上手**：  
  ```bash
  # 设置环境变量（一次配置，全局生效）
  export DASHSCOPE_API_KEY="sk-xxx"
  export MEMORY_SERVICE_ENDPOINT="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"

  # 异步写入一条事实记忆（推荐）
  curl -X POST "$MEMORY_SERVICE_ENDPOINT/add-async" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "user_id": "user_001",
          "messages": [{"role":"user","content":"我明天10点要开产品评审会"}],
          "project_ids": ["proj-product"]
        }'

  # 语义检索（返回 top 3 观察类记忆，相似度 ≥0.7）
  curl -X POST "$MEMORY_SERVICE_ENDPOINT/memory_nodes/search" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "user_id": "user_001",
          "query": "用户近期会议安排",
          "top_k": 3,
          "min_score": 0.7,
          "memory_types": ["observation"]
        }'
  ```

- **关键约束**：  
  - 所有写入操作受账号级限流保护（具体 QPS 请查阅控制台配额页）；  
  - 记忆节点默认永不过期，但 `managed agents` 中的 `Memory Store` 实例 TTL 固定为 7 天；  
  - `user_profile` 抽取为异步过程，首次 `GET /profile` 可能返回空，建议轮询或监听 Webhook 事件；  
  - 技能记忆需通过专用接口 `GET /skills/export` 导出，不可通过通用 `SearchMemory` 获取完整结构。

- **调试技巧**：  
  - 启用 `X-Bailian-Debug: true` 请求头，查看记忆抽取日志（含 `observation`/`skill` 分类依据、`profile_schema` 匹配详情）；  
  - 使用 `bl memory list --user-id user_001` 快速查看当前用户所有记忆节点 ID 与类型；  
  - 若检索结果为空，优先检查 `user_id` 是否一致、`memory_library_id` 是否正确、`memory_types` 是否遗漏目标类型。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [managed agents api](../api/managed-agents-api.md)
- [agent development](../guides/agent-development.md)
- [agent context](../guides/agent-context.md)
- [capabilities](../guides/capabilities.md)


