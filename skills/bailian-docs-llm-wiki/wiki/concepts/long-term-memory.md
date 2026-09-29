# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、跨会话持久化记忆管理能力，用于突破大模型单次推理的上下文长度限制，将用户关键信息（如行为偏好、待办事项、结构化画像）自动提取、语义化存储并按需召回，支撑个性化、连续性 AI 交互。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）与工作流应用调用**：通过 `application call` API 的 `memory_id` 参数启用，使智能体在每次运行时自动从指定记忆库中检索相关事实记忆或用户画像，并注入提示词上下文，实现“记住用户说过什么、做过什么、想要什么”。该能力仅在工作流与旧版智能体 API 中原生支持（新版智能体 API 不支持此参数）。

- **记忆库（Memory Library）独立服务**：作为独立模块提供 RESTful API，支持开发者直接调用 `/add`（写入）、`/memory_nodes/search`（语义检索）、`/profile_schemas`（画像模板管理）等接口。适用于需要精细控制记忆生命周期、多应用共享记忆、或与自定义 Agent 框架（如 OpenClaw）深度集成的场景。

- **Managed Agents 环境挂载**：在 Managed Agents 的 Session 配置中，可将记忆库作为 `resources` 挂载至 `/mnt/memory/` 路径。此时智能体可通过内置 `read`/`write` 工具直接读写结构化记忆文件（如 JSON 格式的技能记录或用户摘要），实现基于文件系统的轻量级长期状态复用，与 API 模式互补。

- **RAG 场景协同**：长期记忆不替代知识库（Knowledge Base），但可与之协同——知识库承载企业静态文档知识，长期记忆承载动态用户个体数据。例如：RAG 检索出产品文档后，长期记忆可补充“该用户上周咨询过同类问题且偏好技术细节”，辅助模型生成更精准回复。

> 注意：所有长期记忆操作均基于 `user_id` 隔离，确保多用户数据严格分离；默认记忆库已预置规则，开箱即用，无需额外创建即可调用。

## 关键参数和配置

| 参数 | 作用 | 必填 | 常用值/范围 | 说明 |
|------|------|------|-------------|------|
| `user_id` | 记忆归属标识，所有读写操作的基础维度 | ✅ | 字符串（如 `"u_123"`） | 同一 `user_id` 下的记忆自动聚合、隔离；不可为空或空字符串 |
| `memory_library_id` | 指定目标记忆库 ID | ❌ | 字符串 | 不传则使用账号默认记忆库（不可删除） |
| `project_id` / `project_ids` | 二级业务隔离维度（如不同 App 或渠道） | ❌ | 单个字符串 或 最多 5 个字符串数组 | 与 `project_id` 互斥；用于精细化权限与统计 |
| `plan_version` | 控制检索/抽取策略版本 | ❌ | `"pro"`（默认） 或 `"lite"` | `"pro"` 支持 `min_score` 过滤与更高精度；`"lite"` 仅基础语义匹配 |
| `min_score` | 相似度阈值（仅 `plan_version=pro` 生效） | ❌ | `0.0`–`1.0`，建议 `0.5`–`0.7` | 低于此值的记忆条目不返回；默认 `0.3` |
| `top_k` | 检索返回最大条数 | ❌ | `1`–`100`，建议显式设为 `10` | 默认值未明确定义，生产环境务必显式设置 |
| `profile_schema` | 用户画像模板 ID | ❌（仅触发画像时必填） | 字符串 | 调用 `/add` 时传入，才启动结构化画像抽取 |
| `extract_mode` | 写入模式控制 | ❌ | `"profile_only"`（仅抽画像） 或 `"all"`（默认，抽事实+画像） | 用于降低非必要抽取开销 |

- **事实记忆有效期**：由**记忆规则（Memory Rule）** 级别配置，非全局或单条记忆设置。预置规则默认 180 天，可选 7/30/180 天或永不过期。未显式配置的规则继承默认值。
- **异步写入推荐**：对稳定性要求高的场景（尤其含图片等多模态内容），优先使用 `/add-async` 接口，通过 `event_id` 轮询获取结果，避免同步超时风险。

## 面向开发者，简洁实用

- ✅ **快速上手**：开通服务后，只需 `DASHSCOPE_API_KEY` + 固定地址 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，无需部署任何后端。
- ✅ **零配置启动**：默认记忆库已就绪，直接调用 `/add`（带 `user_id` 和 `messages`）即可开始积累事实记忆。
- ✅ **精准召回**：检索时传入当前对话 `messages`（如 `[{ "role": "user", "content": "我上次说要订机票" }]`），系统自动语义匹配历史记忆，无需手动构造关键词。
- ⚠️ **注意异步延迟**：用户画像抽取为异步过程，首次 `GET /profile_schemas/{id}/user_profile?user_id=xxx` 可能返回空，建议重试间隔 ≥3 秒。
- ⚠️ **限流硬约束**：账号级总 QPM ≤3000；`/add` ≤120 QPM；`/memory_nodes/search` ≤300 QPM。务必实现指数退避重试（HTTP 429 响应）。
- ⚠️ **删除不可逆**：`DELETE /memory_nodes/{id}` 立即生效且无回收站，请校验 `memory_node_id` 后再执行。

示例：检索用户近期待办（Pro 版本，高相关性过滤）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role": "user", "content": "我有什么待办？"}],
    "top_k": 5,
    "min_score": 0.6,
    "plan_version": "pro"
  }'
```

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [application call](../api/application-call.md)
- [managed agents](../guides/managed-agents.md)
- [knowledge base](../guides/knowledge-base.md)


