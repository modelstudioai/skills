# 跨会话记忆

跨会话记忆是指将对话中提取的关键信息和用户画像持久化存储，并在后续会话中通过语义检索召回并注入 Prompt 的能力，用于解决大模型上下文窗口无法跨会话延续的问题。百炼平台通过「记忆库（Memory Library）」与「长期记忆 API」提供该能力。

## 在百炼平台中的使用场景

跨会话记忆在以下场景中发挥作用：

- **个性化智能体**：在多轮对话之间保留用户偏好、习惯和重要事件（如「每天上午 9 点提醒我喝水」），让智能体在新会话中仍然理解用户历史。
- **长期用户画像**：通过自定义画像模板提取结构化属性（年龄、职业、偏好等），在后续对话中以固定字段持久化注入，适用于需要稳定属性支撑的业务。
- **Agent 自动捕获/召回**：OpenClaw Agent 通过记忆插件在 `before_agent_start`（自动召回）和 `agent_end`（自动捕获）两个生命周期钩子中与长期记忆 API 交互，实现零侵入的跨会话记忆。
- **应用观测中的记忆追踪**：在应用观测的调用链路中，记忆的写入与检索会作为 RETRIEVER、EMBEDDING 等节点出现，便于开发者定位记忆相关调用的延时与 Token 消耗。

## 接入方式

### 方式一：API 直连

通过 HTTPS 调用 `https://dashscope.aliyuncs.com/api/v2/apps/memory/*` 系列接口，请求 Header 携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。典型流程为：对话结束调用 `AddMemory` 写入记忆 → 下次对话调用 `SearchMemory` 语义检索 → 将结果注入 Prompt。

```bash
# 写入记忆（自动从对话提取）
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "messages": [
      {"role": "user", "content": "每天上午9点提醒我喝水"},
      {"role": "assistant", "content": "好的，已记录"}
    ],
    "user_id": "user_001"
  }'

# 语义检索记忆
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "user_id": "user_001",
    "messages": [{"role": "user", "content": "我需要做什么？"}],
    "top_k": 5
  }'
```

Python 用户可安装 `agentscope-runtime`，使用 `AddMemory`、`SearchMemory`、`ListMemory`、`CreateProfileSchema`、`GetUserProfile` 等封装类（均需在 `finally` 中调用 `close()`）。

### 方式二：OpenClaw 记忆插件

```bash
openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw
openclaw plugins info modelstudio-memory-for-openclaw
openclaw modelstudio-memory stats
openclaw gateway restart
```

插件配置写入 `~/.openclaw/openclaw.json`，关键项：`slots.memory` 注册为记忆槽位（会自动禁用内置 `memory-core` 和 `memory-lancedb`）；`apiKey` 填 DashScope API Key；`userId` 用于隔离不同用户记忆空间。所有读写均由百炼服务端完成提炼、向量化和语义检索。

## 记忆内容类型

记忆库提供两类持久化内容，可独立或组合使用：

- **记忆片段**：从对话中自动提取的关键事件和信息，支持自动去重、动态更新，也可通过 `custom_content` 直接写入指定内容。适用于大多数长期记忆场景。
- **用户画像**：基于画像模板（profile schema）从对话中提取的结构化属性，适用于需要固定属性持久化存储的场景。属性字段应清晰具体，避免「姓名/名称/名字」等同义字段并存，且不应期望一次对话就提取全部信息。

## 关键参数

### AddMemory 请求参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `user_id` | 是 | 记忆实体 ID，用于标识归属对象，最大 64 个字符 |
| `messages` | 与 `custom_content` 二选一 | 对话消息列表，每个消息含 `role`（user/assistant）和 `content`，最多 50 条 |
| `custom_content` | 与 `messages` 二选一 | 自定义内容，最大 512 个字符，传入后忽略 `messages` |
| `profile_schema` | 否 | 画像模板 ID，在记忆库详情页获取 |
| `memory_library_id` | 否 | 记忆库 ID，最大 32 个字符，不传则使用默认记忆库 |
| `project_id` | 否 | 记忆片段规则 ID，不传则使用指定记忆库的默认规则 |
| `meta_data` | 否 | 用户自定义信息 |

### SearchMemory 请求参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `user_id` | 是 | 用户 ID，用于隔离记忆空间 |
| `messages` | 是 | 查询对话内容，系统据此做语义检索 |
| `top_k` | 否 | 返回的记忆片段数量 |

## 使用限制

| 项目 | 限制 |
| --- | --- |
| 全部接口总计 | 3000 QPM（阿里云账号级别） |
| 记忆片段 add 接口 | 120 QPM |
| 记忆片段 search 接口 | 300 QPM |

## 有效期说明

记忆有效期在不同入口存在差异：长期记忆 API 文档指出「生成的记忆片段与用户画像暂无失效日期」，而控制台默认记忆片段规则预置了「默认有效期 180 天」，并支持按规则配置 7/30/180 天或永不过期。以控制台记忆规则配置为准；通过 API 直写且不指定 `project_id` 时使用默认规则。

## 注意事项

- OpenClaw 记忆插件为统一配置，所有 Agent 共享同一记忆，暂不支持按 Agent 独立配置；不支持阿里云百炼 Coding Plan 的 API Key。
- 应用观测暂不支持通过 Assistant API 创建的智能体应用；对高代码应用，仅能观测到入口 CHAIN 节点，不支持追踪其内部调用链路。
- 记忆的写入与检索在应用观测中会体现为 RETRIEVER、EMBEDDING 等节点，可用于定位记忆相关调用的延时与 Token 消耗。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [application monitoring](../guides/application-monitoring.md)


