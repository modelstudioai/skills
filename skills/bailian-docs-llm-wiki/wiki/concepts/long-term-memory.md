# 长期记忆

长期记忆是百炼平台提供的跨会话上下文持久化能力。它自动从对话中提取关键信息并存储，在后续对话中通过语义检索召回相关记忆并注入 Prompt，使智能体能够持续理解用户偏好与历史信息，解决大模型上下文窗口有限、对话结束后信息丢失的问题。

## 核心能力

长期记忆持久化两类内容，二者可独立或组合使用：

- **记忆片段**：从对话中自动提取的关键事件和信息（如"用户每天上午9点需要喝水提醒"），适用于大多数长期记忆场景。支持自动去重、动态更新，也可通过 `custom_content` 直接写入指定内容。
- **用户画像**：基于自定义画像模板从对话中提取的结构化属性（如年龄、职业、偏好等），适用于需要固定属性持久化存储的场景。属性字段应清晰具体，避免"姓名/名称/名字"等同义字段并存，且不应期望一次对话就提取全部信息。

## 接入方式

### API 直连

通过 HTTPS 调用 `https://dashscope.aliyuncs.com/api/v2/apps/memory/*` 系列接口。需在请求 Header 中添加 `Authorization: Bearer $DASHSCOPE_API_KEY`，`Content-Type` 设为 `application/json`。典型流程为：对话结束调用 `AddMemory` 写入记忆 → 调用 `SearchMemory` 语义检索 → 将结果注入 Prompt。

### OpenClaw 记忆插件

OpenClaw Agent 可通过插件实现零侵入的跨会话记忆。插件在 Gateway 内通过 `before_agent_start`（自动召回）和 `agent_end`（自动捕获）两个生命周期钩子与长期记忆 API 交互，所有读写均由百炼服务端完成提炼、[向量化](embedding.md)和语义检索。

```bash
# 安装
openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw

# 验证
openclaw plugins info modelstudio-memory-for-openclaw
openclaw modelstudio-memory stats
openclaw gateway restart
```

> **注意**：OpenClaw 记忆插件为统一配置，所有 Agent 共享同一记忆，暂不支持按 Agent 独立配置；不支持阿里云百炼 Coding Plan 的 API Key。

## 关键接口

| 接口名称 | HTTP 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| AddMemory | POST | `/add` | 添加记忆片段 |
| SearchMemory | POST | `/memory_nodes/search` | 语义搜索记忆片段 |
| ListMemory | GET | `/memory_nodes` | 列出记忆片段 |
| DeleteMemory | DELETE | `/memory_nodes/{memory_node_id}` | 删除记忆片段 |
| UpdateMemory | PATCH | `/memory_nodes/{memory_node_id}` | 更新记忆片段 |
| CreateProfileSchema | POST | `/profile_schemas` | 创建画像模板 |
| ListProfileSchemas | GET | `/profile_schemas` | 获取画像模板列表 |
| GetProfileSchema | GET | `/profile_schemas/{profile_schema_id}` | 获取画像模板详情 |
| UpdateProfileSchema | PATCH | `/profile_schemas/{profile_schema_id}` | 更新画像模板 |
| DeleteProfileSchema | DELETE | `/profile_schemas/{profile_schema_id}` | 删除画像模板 |
| GetUserProfile | GET | `/profile_schemas/{profile_schema_id}/user_profile` | 获取用户画像 |

## AddMemory 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_id` | string | 是 | 记忆实体 ID，用于标识归属对象，最大 64 个字符 |
| `messages` | array | 与 `custom_content` 二选一 | 对话消息列表，每个消息含 `role`（user/assistant）和 `content`，最多 50 条 |
| `custom_content` | string | 与 `messages` 二选一 | 自定义内容，最大 512 个字符，传入后忽略 `messages` |
| `profile_schema` | string | 否 | 画像模板 ID |
| `memory_library_id` | string | 否 | 记忆库 ID，最大 32 个字符，不传则使用默认记忆库 |
| `project_id` | string | 否 | 记忆片段规则 ID，不传则使用指定记忆库的默认规则 |
| `meta_data` | object | 否 | 用户自定义信息 |

返回结果中 `memory_nodes` 数组包含每项的 `memory_node_id`、`content`、`event`（`ADD`/`UPDATE`/`DELETE`）及 `old_content`（仅 `UPDATE` 时有效）。

## 使用示例

```bash
# 写入记忆（从对话自动提取）
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

# 语义检索记忆
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "messages": [{"role": "user", "content": "我需要做什么？"}],
    "top_k": 5
  }'
```

## 使用限制

| 接口 | 限流（阿里云账号级别） |
| --- | --- |
| 全部接口 | 总计不超过 3000 QPM |
| 记忆片段 add 接口 | 120 QPM |
| 记忆片段 search 接口 | 300 QPM |

## 记忆有效期

记忆有效期在不同入口存在差异：通过 API 直写且不指定 `project_id` 时使用默认规则，API 文档指出"生成的记忆片段与用户画像暂无失效日期"；而控制台记忆库的默认规则预置了"默认有效期 180 天"，并支持按规则配置 7/30/180 天或永不过期。以控制台记忆规则配置为准。

## 与应用调用的关系

长期记忆通常与应用调用配合使用。在通过 Responses API 或 DashScope API 调用智能体应用时，可在对话前通过 `SearchMemory` 检索相关记忆注入 Prompt，在对话后通过 `AddMemory` 将新信息写入记忆库，从而实现多轮对话间的上下文连续性。使用 OpenClaw 插件时，这一过程在 Gateway 内自动完成，无需在应用代码中显式调用记忆 API。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [application call](../api/application-call.md)


