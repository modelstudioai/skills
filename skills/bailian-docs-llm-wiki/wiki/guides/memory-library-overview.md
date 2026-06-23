# memory library overview

百炼平台的记忆库为智能体提供跨会话的长期记忆能力。大模型受上下文窗口限制，无法在不同会话间保留用户信息，记忆库通过自动从对话中提取关键信息并持久化存储，在后续对话中基于语义检索相关记忆并注入上下文，使智能体能够持续理解用户偏好和历史信息。记忆库提供开放的 API 接口，可接入任意应用，也支持多应用共享同一记忆库。

## 核心概念

记忆库支持两种记忆内容类型：

- **记忆片段**：从对话中自动提取的关键事件和信息（如"用户每天上午9点需要喝水提醒"）。适用于大多数长期记忆场景，支持自动去重和动态更新。
- **用户画像**：基于自定义模板从对话中提取的结构化属性（如年龄、职业、偏好等）。适用于需要持久化存储固定属性的场景。

详细的概念说明和控制台操作指南参见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。

## 使用流程

1. 获取 API Key，创建记忆库或使用默认记忆库（每个账号自带一个默认记忆库）。
2. 每轮对话结束后，调用 `AddMemory` 接口写入记忆。
3. 下次对话前，调用 `SearchMemory` 基于语义检索相关记忆。
4. 将检索结果注入 Prompt，实现个性化回答。

## API 接口

记忆库通过 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 提供完整的记忆管理能力，所有接口的 Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，需在请求头中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。

### 记忆片段操作

**写入记忆（AddMemory）**

传入对话消息，系统自动提取关键信息并存储为记忆片段：

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "messages": [
      {"role": "user", "content": "每天上午9点提醒我喝水"},
      {"role": "assistant", "content": "好的，已记录"}
    ],
    "user_id": "user_001"
  }'
```

也支持通过 `custom_content` 字段直接写入自定义记忆内容，跳过对话提取。

**检索记忆（SearchMemory）**

基于语义检索与当前查询相关的历史记忆：

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "messages": [{"role": "user", "content": "我需要做什么？"}],
    "top_k": 5
  }'
```

**列出/更新/删除记忆**

- `GET /memory_nodes?user_id=xxx&page_size=10&page_num=1` — 分页列出记忆
- `PATCH /memory_nodes/{memory_node_id}` — 更新指定记忆
- `DELETE /memory_nodes/{memory_node_id}` — 删除指定记忆

### 用户画像操作

1. **创建画像模板**（`POST /profile_schemas`）：定义需要提取的属性字段（如年龄、职业、爱好），字段描述应清晰具体，避免语义重复的字段名。
2. **提取画像**：调用 `AddMemory` 时传入 `profile_schema` 参数，系统自动从对话中提取用户属性。
3. **获取画像**（`GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`）：获取完整的用户画像信息。

### 可选参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `user_id` | 是 | 用户标识，用于隔离不同用户的记忆空间 |
| `memory_library_id` | 否 | 记忆库 ID，不填则使用默认记忆库 |
| `project_id` | 否 | 记忆片段规则 ID |
| `profile_schema` | 否 | 用户画像规则 ID |
| `meta_data` | 否 | 自定义元数据，用于分类管理 |

### Python SDK

通过 `agentscope-runtime` 包（`pip install agentscope-runtime`）调用，主要类位于 `agentscope_runtime.tools.modelstudio_memory`，包括 `AddMemory`、`SearchMemory`、`ListMemory`、`CreateProfileSchema`、`GetUserProfile` 等。

## 记忆库管理

在百炼控制台可以创建和管理记忆库，配置记忆规则：

- **记忆片段规则**：定义提取策略（默认或自定义指令）、自动更新开关、过期时间（7天/30天/180天/永不过期）。每个记忆库最多 50 条。
- **用户画像规则**：定义画像字段及描述，支持设置初始值。每个记忆库最多 50 条。
- **检索调试**：支持在控制台调试检索效果，配置意图判别、查询改写、重排序（gte-rerank-v2 模型）和相似度阈值（建议 0.5~0.7）。

## OpenClaw 集成

对于使用 OpenClaw Agent 的场景，百炼提供了 [记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)（`@modelstudio/modelstudio-memory-for-openclaw`），通过 Gateway 的生命周期钩子实现：

- **autoCapture**：对话结束后自动提取并存储记忆
- **autoRecall**：对话开始前自动检索并注入相关记忆

安装步骤：

```bash
openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw
```

在 `~/.openclaw/openclaw.json` 中配置 `apiKey`（必填）和 `userId`（必填），以及可选的 `topK`（默认 5）、`minScore`（默认 0）、`memoryLibraryId`、`profileSchema` 等参数，重启 Gateway 后即可使用。

插件还向 Agent 注册了 `memory_search`、`memory_store`、`memory_list`、`memory_forget` 四个工具，Agent 可在对话中主动调用。

> **注意**：记忆插件为统一配置，所有 Agent 共享同一记忆，暂不支持按 Agent 独立配置。

## 配额与限制

| API 操作 | 速率上限 |
|----------|----------|
| AddMemory（写入） | 120 QPM |
| SearchMemory（查询） | 300 QPM |
| 所有操作合计 | 3000 QPM |

性能参考：SearchMemory 端到端延迟 200-500ms，AddMemory 延迟 500-1000ms。

> **注意**：该功能与 API 调用限时免费。生成的记忆片段与用户画像暂无失效日期（除非配置了记忆过期时间规则）。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)




