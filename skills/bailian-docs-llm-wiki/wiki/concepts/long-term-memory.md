# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台面向 Agent 应用提供的**结构化、持久化、用户隔离的记忆管理能力**，用于跨会话存储和语义检索用户事实（如提醒、偏好）、技能（如常用操作）及结构化画像（如年龄、兴趣），支撑状态感知型 Agent 的持续演进与个性化服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 运行时上下文（[agent context](../guides/agent-context.md)）**：作为 `context_sources` 中的 `"memory"` 源之一，长期记忆与 RAG、Connector 等协同注入 Agent 输入上下文；但注意：它**不参与单次请求的临时上下文缓存**（那是短期 memory window 的职责），而是通过 `user_id` 显式绑定，在每次调用时按需检索并注入相关记忆节点，实现跨会话状态复用。

- **Agent 开发范式（[agent development](../guides/agent-development.md)）**：  
  - 在 **Managed Agent** 和 **Flow Agent** 中，可通过 YAML 或流程节点配置 `memory: { enabled: true }`，平台自动在 `SearchMemory` 调用后将高分记忆片段注入 prompt；  
  - 在 **Sandbox Agent** 中，开发者需直接调用 `AddMemoryAsync` / `SearchMemory` SDK 工具，自主控制写入时机、检索策略与结果融合逻辑，适用于复杂记忆编排场景（如多项目技能聚合、画像动态更新）。

- **Flow Agent API（组件管理）**：  
  - 新版长期记忆（`long-term-memory-new`）通过 OpenAPI（AccessKey 鉴权）提供完整 CRUD，是当前推荐标准；  
  - 旧版 `Memory` / `MemoryNode` 接口已逐步归档，**不支持用户画像建模，且无语义检索能力**，仅适用于简单键值存储场景，新项目请勿选用。

- **工作流与自动化构建**：常作为工作流的“记忆中枢”，例如：对话中识别用户需求 → 异步写入 `observation` + `skill` → 后续任务触发时按标签/语义检索 → 驱动工具调用或生成个性化响应。

## 关键参数和配置

| 参数 | 说明 | 推荐值 | 注意事项 |
|------|------|--------|----------|
| `user_id` | **必填**，用户级隔离标识，所有读写操作均以此为作用域 | `"user_001"` | 同一 `user_id` 下的记忆可跨 Agent、跨工作流共享 |
| `project_ids` | 可选，业务维度二级隔离（如 `"order"`、`"customer_service"`），最多 5 个 | `["support_v2"]` | 与 `project_id` 互斥；检索时可指定 `project_ids` 精确过滤 |
| `memory_types` | `SearchMemory` 中指定检索范围 | `["observation", "skill"]` | 默认仅查 `observation`；`skill` 类需显式声明才参与检索 |
| `plan_version` | 控制能力等级：`pro`（支持 `min_score`、Rerank、高精度抽取）或 `lite`（基础能力） | `"pro"` | 默认 `pro`；`lite` 仅适用于低资源或测试环境 |
| `extract_mode` | 写入时控制抽取行为 | `"profile_only"` | 仅当传入 `profile_schema` 时生效；若同时含 `messages`，则默认启用全量抽取（observation + skill + profile） |
| `top_k` / `min_score` | `SearchMemory` 检索结果数量与相似度阈值 | `top_k=5`, `min_score=0.45` | `min_score` 仅 `plan_version=pro` 有效；建议生产环境设 `min_score ≥ 0.4` 避免噪声 |

> ⚠️ **重要实践提示**：  
> - **优先使用异步接口**：`AddMemoryAsync` 支持 `intelligent` 模式下的多模态/多项目联合抽取，而同步 `AddMemory` 在 `intelligent` 模式下可能超时；  
> - **画像需预定义 schema**：必须先调用 `CreateProfileSchema` 定义字段（如 `{"age": "integer", "hobby": "string[]"}`），再在写入时传 `profile_schema`，否则不触发属性级抽取；  
> - **多模态输入需项目启用**：`messages[].content` 含 `image_url` 时，仅在开通多模态能力的项目中解析图片内容。

## 面向开发者的快速上手

```python
# 1. 异步写入（推荐）
from agentscope_runtime.tools.modelstudio_memory import AddMemoryAsync
res = await AddMemoryAsync().arun(
    user_id="u123",
    project_ids=["sales"],
    messages=[{"role": "user", "content": "帮我订明天下午3点的会议室"}],
    profile_schema={"meeting_preference": "string"}
)

# 2. 语义检索（带过滤）
from agentscope_runtime.tools.modelstudio_memory import SearchMemory
res = await SearchMemory().arun(
    user_id="u123",
    messages=[{"role": "user", "content": "我最近有什么会议安排？"}],
    memory_types=["observation"],
    project_ids=["sales"],
    top_k=3,
    min_score=0.5
)
for node in res.memory_nodes:
    print(f"[{node.score:.2f}] {node.content} (type: {node.type})")
```

✅ **最佳实践清单**：  
- 初始化阶段：为每个用户调用 `CreateProfileSchema` 一次；  
- 对话中：每轮关键交互后调用 `AddMemoryAsync`，避免高频写入（QPM 限 120）；  
- 推理前：在 `context_sources: ["memory"]` 启用下，`SearchMemory` 结果将自动注入 prompt；  
- 生产监控：关注 `event_id` 轮询失败率与 `SearchMemory` 平均 `score` 分布，低于 0.4 时建议优化 query 或调整 `plan_version`。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent development](../guides/agent-development.md)


