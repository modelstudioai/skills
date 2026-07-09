# memory library overview

百炼记忆库（Memory Library）通过长期记忆 API 解决大模型跨会话上下文丢失的问题：自动从对话中提取关键信息并持久化存储，再在后续对话中基于语义检索召回相关记忆注入 Prompt，使智能体能够持续理解用户偏好与历史信息。该能力既可在百炼控制台可视化管理，也提供开放的 HTTP API 接入任意应用，并支持通过 OpenClaw 插件以"自动捕获 / 自动召回"的方式零侵入接入 Agent。详见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)、[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 与 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 核心能力

记忆库提供两类持久化记忆内容，二者可独立或组合使用：

- **记忆片段**：从对话中自动提取的关键事件和信息（如"用户每天上午9点需要喝水提醒"），适用于大多数长期记忆场景。支持自动去重、动态更新，也可通过 `custom_content` 直接写入指定内容。
- **用户画像**：基于自定义画像模板从对话中提取的结构化属性（如年龄、职业、偏好等），适用于需要固定属性持久化存储的场景。属性字段及描述应清晰具体，避免"姓名/名称/名字"等同义字段并存，且不应期望一次对话就提取全部信息。

> **注意**：记忆有效期在不同入口存在差异。[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 文档指出"生成的记忆片段与用户画像暂无失效日期"，而 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 控制台的默认记忆片段规则预置了"默认有效期 180 天"，并支持按规则配置 7/30/180 天或永不过期。以控制台记忆规则配置为准；通过 API 直写且不指定 `project_id` 时使用默认规则。

## 接入方式

### 方式一：API 直连

通过 HTTPS 调用 `https://dashscope.aliyuncs.com/api/v2/apps/memory/*` 系列接口，需在环境变量中配置 `DASHSCOPE_API_KEY`。典型流程为：对话结束调用 `AddMemory` 写入记忆 → 调用 `SearchMemory` 语义检索 → 将结果注入 Prompt。

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

Python 用户可安装 `agentscope-runtime`，使用 `AddMemory`、`SearchMemory`、`ListMemory`、`CreateProfileSchema`、`GetUserProfile` 等封装类（均需在 `finally` 中调用 `close()`）。

### 方式二：OpenClaw 记忆插件

OpenClaw Agent 可通过插件实现零侵入的[跨会话记忆](../concepts/cross-session-memory.md)。插件在 Gateway 内通过 `before_agent_start`（自动召回）和 `agent_end`（自动捕获）两个生命周期钩子与长期记忆 API 交互，所有读写均由百炼服务端完成提炼、向量化和语义检索。

```bash
# 安装
openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw

# 验证
openclaw plugins info modelstudio-memory-for-openclaw
openclaw modelstudio-memory stats
openclaw gateway restart
```

插件配置写入 `~/.openclaw/openclaw.json`，关键项：`slots.memory` 注册为记忆槽位（会自动禁用内置 `memory-core` 和 `memory-lancedb`）；`apiKey` 填 DashScope [API Key](../concepts/api-key.md)；`userId` 用于隔离不同用户记忆空间。

> **注意**：OpenClaw 记忆插件为统一配置，所有 Agent 共享同一记忆，暂不支持按 Agent 独立配置；不支持阿里云百炼 Coding Plan 的 [API Key](../concepts/api-key.md)。

## 关键参数

### AddMemory 请求参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `messages` | 与 `custom_content` 二选一 | 对话内容，系统自动从中提取记忆片段 |
| `custom_content` | 与 `messages` 二选一 | 直接指定要存入的记忆内容，不经过对话提炼 |
| `user_id` | 是 | 记忆空间用户标识，同 `user_id` 共享命名空间，不同 `user_id` 完全隔离 |
| `memory_library_id` | 否 | 记忆库 ID，不填使用默认记忆库 |
| `project_id` | 否 | 记忆片段规则 ID，不填使用默认规则 |
| `profile_schema` | 否 | 用户画像规则 ID，传入后同时提取画像 |
| `meta_data` | 否 | 自定义元数据，用于分类管理 |

### SearchMemory 请求参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `user_id` | 是 | 记忆空间用户标识 |
| `messages` | 是 | 查询对话内容 |
| `memory_library_id` | 否 | 限定检索的记忆库 |
| `top_k` | 否 | 返回记忆条数，建议 3–10 |

### OpenClaw 插件配置项

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `apiKey` | string | - | 必填，以 `sk-` 开头 |
| `userId` | string | - | 必填，记忆空间用户标识 |
| `autoCapture` | boolean | `true` | 对话后自动提取并存储记忆 |
| `autoRecall` | boolean | `true` | 对话前自动检索并注入记忆 |
| `topK` | number | `5` | 每次召回返回的记忆条数 |
| `minScore` | number | `0` | 最小相似度阈值（0–100） |
| `profileSchema` | string | - | 用户画像 ID |
| `memoryLibraryId` | string | - | 记忆库 ID |
| `projectId` | string | - | 记忆片段规则 ID |

## 记忆库与记忆规则管理

每个账号自带一个无法删除的默认记忆库，预置一条"默认项目"记忆片段规则（默认有效期 180 天，可编辑但不可删除）。可按业务场景创建新记忆库并配置记忆规则，每个记忆库最多 50 条记忆片段规则和 50 条用户画像规则。

- **记忆片段规则**：定义从对话中提取关键事件和信息的策略，可选择默认或自定义规则指令，支持自动更新和过期时间（7/30/180 天或永不过期）。
- **用户画像规则**：定义画像字段名称、描述和初始值。当用户尚未通过对话提供信息时，系统使用初始值作为属性值。

控制台记忆检索页支持配置最大召回数量（1–100）、意图判别召回（建议开启）、查询改写（口语化提问时开启）和排序（使用 `gte-rerank-v2` 模型，相似度阈值建议 0.5–0.7）。

## OpenClaw 插件工具

除自动捕获/召回外，插件向 Agent 注册四个可主动调用的工具：

- **memory_search**：语义检索记忆库，返回相似度最高的记忆列表，适用于"之前讨论过什么"等回顾性问题。
- **memory_store**：直接写入记忆，不经过对话提炼，适用于"记住我的服务器 IP 是 192.168.1.x"等显式记忆请求。
- **memory_list**：分页列出当前 `userId` 下所有记忆条目。
- **memory_forget**：按记忆 ID 删除指定记忆，通常先 `memory_search` 定位再删除。

CLI 等效：`openclaw modelstudio-memory search|list|stats`。

## 配额与限制

长期记忆 API 速率限制（阿里云账号级别）：

| API 操作 | 速率上限 |
| --- | --- |
| AddMemory（写入） | 120 次/分钟 |
| SearchMemory（查询） | 300 次/分钟 |
| 所有操作合计 | 3000 次/分钟 |

性能指标：SearchMemory 端到端延迟 200–500ms；AddMemory 延迟 500–1000ms；自动捕获异步执行，不影响响应速度。该功能与 API 调用限时免费。

## 排错要点

- **OpenClaw 插件重启后状态为 not loaded**：检查 `openclaw.json` 中 `plugins.entries.modelstudio-memory-for-openclaw.enabled` 是否为 `true`，以及 `plugins.slots.memory` 是否指向该插件，修正后重新 `openclaw gateway restart`。
- **日志出现 InvalidApiKey**：DashScope [API Key](../concepts/api-key.md) 无效或过期，到百炼控制台确认状态或重新创建；若用环境变量引用，确认 `DASHSCOPE_API_KEY` 已设置且 Gateway 进程可读取。
- **查看插件日志**：日志按日期存储在系统临时目录，文件名 `openclaw-YYYY-MM-DD.log`，可用 `grep modelstudio-memory` 过滤。

> **注意**：[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 为新版本，相比旧版长期记忆 API 在延迟、自动提取、语义检索准确性和用户画像能力上均有改进，建议新接入直接使用新版接口。

## 来源文档

- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)














