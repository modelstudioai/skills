# 长期记忆

长期记忆是百炼平台提供的结构化、可检索、跨会话持久化的用户与对话上下文存储服务，用于在 Agent 全生命周期中持续积累和复用事实性信息、技能知识与用户画像，支撑更连贯、个性化、具备“成长性”的智能交互。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 开发（Flow/Sandbox）**：作为核心上下文源，通过 `agent_context` 机制按需注入记忆片段（如“用户偏好咖啡因”“曾使用过报销流程”），替代手动维护 session history；Sandbox 中可调用 SDK 主动读写，Flow Agent 中可通过 Memory 节点或 `extra_parameters.agent_context` 声明式加载。
- **新版智能体（Agent 2.0）**：深度集成于推理 Runtime，自动触发记忆抽取（observation/skill/profile）与语义检索，无需显式调用 API；记忆写入由 `/add` 或 `/add-async` 接口驱动，检索结果经 Rerank 后自动注入 prompt 上下文。
- **RAG 增强场景**：与知识库协同工作——知识库承载静态领域知识，长期记忆承载动态用户专属事实（如“张三的工号是 A1024”），二者通过 `context_type="memory"` 显式区分，且不可同时启用（RAG 优先级更高）。
- **用户画像构建**：需先定义 `profile_schema`（如含 `age`, `job_title`, `preferred_language` 字段），再在记忆写入时传入该 schema ID，系统将从对话中结构化提取并持久化为可查询的 `user_profile` 实体。
- **治理与可观测性**：所有记忆写入/检索操作均生成完整 Trace（含 `memory_node_id`, `extract_mode`, `score` 等字段），可在 Agent Governance 控制台中追踪耗时、失败原因及 Token 消耗，支持基于记忆行为的评测集构建（如验证“是否正确复用历史决策”）。

> ⚠️ 注意：旧版 Flow Agent API 中的 `Memory` / `MemoryNode` 接口已被标记为 legacy（目录含时间戳 `2023-12-29`），新项目**必须使用 `/api/v2/apps/memory` 下的新版长期记忆 API**（即 `long-term-memory-new`），二者不兼容。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | 所有请求体 | string | ✓ | 子用户唯一标识，用于跨用户记忆隔离；建议与业务系统用户 ID 对齐。 |
| `project_id` 或 `project_ids` | `/add`, `/add-async`, `/search` | string / string[] | ✗ | 二级隔离维度；`project_ids` 最多 5 个，与 `project_id` 互斥；常用于多租户 SaaS 场景。 |
| `messages` | `/add`, `/add-async`, `/search` | array | ✓（二选一） | OpenAI 格式消息数组，触发模型抽取（observation/skill）或作为语义搜索 query；若仅存原始内容，改用 `custom_content`。 |
| `custom_content` | `/add`, `/add-async` | string/object | ✓（二选一） | 直接写入原始结构化内容（如 JSON），跳过抽取；适用于已清洗的技能文档或画像数据。 |
| `profile_schema` | `/add`, `/add-async` | string | ✗ | 用户画像模板 ID；传入后自动触发 profile 抽取，否则仅生成 observation/skill。 |
| `extract_mode` | `/add`, `/add-async` | string | ✗ | 可选 `"profile_only"`（仅抽画像）、`"all"`（默认，全类型）；不传则按 `messages` 内容自动判断。 |
| `top_k` | `/search` | int | ✗ | 最大召回数，默认 `10`，范围 `1–100`。 |
| `min_score` | `/search` | float | ✗ | 最小相似度阈值，默认 `0.3`；**仅 `plan_version="pro"` 时生效**。 |
| `memory_types` | `/search` | string[] | ✗ | 指定检索类型，默认 `["observation"]`；支持 `["skill"]`, `["observation","skill"]`, `["user_profile"]`。 |
| `plan_version` | `/search`, `/add` | string | ✗ | `"pro"`（启用 Rerank、支持 `min_score`）或 `"lite"`（基础向量检索）；不区分大小写。 |

## 面向开发者，简洁实用

- ✅ **快速上手**：  
  ```bash
  # 设置环境变量（一次配置，全局复用）
  export DASHSCOPE_API_KEY="sk-xxx"
  export MEMORY_SERVICE_ENDPOINT="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"

  # 同步写入一条事实记忆（低延迟场景）
  curl -X POST "$MEMORY_SERVICE_ENDPOINT/add" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "user_id": "u123",
          "messages": [{"role":"user","content":"我明天要参加杭州的客户会议"}],
          "project_id": "proj-crm"
        }'

  # 语义搜索（带过滤）
  curl -X POST "$MEMORY_SERVICE_ENDPOINT/memory_nodes/search" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "user_id": "u123",
          "messages": [{"role":"user","content":"客户会议安排"}],
          "memory_types": ["observation"],
          "top_k": 3,
          "plan_version": "pro"
        }'
  ```

- ✅ **SDK 推荐**：优先使用 `agentscope-runtime`（v0.8.0+），自动处理认证、重试、异步轮询与错误分类：
  ```python
  from agentscope.runtime import LongTermMemoryClient

  client = LongTermMemoryClient(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      endpoint=os.getenv("MEMORY_SERVICE_ENDPOINT")
  )

  # 异步写入（推荐高吞吐/复杂抽取）
  event = client.add_async(
      user_id="u123",
      messages=[{"role":"user","content":"整理会议纪要的步骤是..."}],
      project_id="proj-crm",
      profile_schema="ps-abc"  # 同时抽画像
  )
  result = client.wait_for_event(event.event_id)  # 自动轮询，超时抛异常

  # 检索
  nodes = client.search(
      user_id="u123",
      query="会议纪要",
      memory_types=["skill"],
      top_k=5,
      plan_version="pro"
  )
  ```

- ⚠️ **避坑指南**：
  - 同步 `/add` 在 `intelligent` 模式下可能超时（尤其含图片或多轮消息），SLA 敏感场景请改用 `/add-async`；
  - `min_score` 仅对 `plan_version="pro"` 生效，`lite` 版本忽略该参数；
  - 多模态抽取需确保项目已开通多模态能力，否则 `image_url` 将被静默跳过；
  - 记忆写入与检索均受账号级限流（总 3000 QPM），`/add` 单接口限 120 QPM，生产环境需做好降级（如本地缓存 fallback）。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent development](../guides/agent-development.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent context](../guides/agent-context.md)
- [agent governance](../guides/agent-governance.md)


