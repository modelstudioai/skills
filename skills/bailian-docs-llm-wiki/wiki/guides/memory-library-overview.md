# memory library overview

记忆库是阿里云百炼平台提供的长期记忆解决方案，用于解决大模型因上下文窗口限制而无法跨会话保留信息的问题。通过自动从对话中提取关键信息并持久化存储，记忆库使智能体能够在后续对话中基于语义检索相关记忆并注入上下文，实现个性化、连贯的对话体验。记忆库提供开放的 API 接口，可接入任意应用，也支持多应用共享同一记忆库。

## 核心概念

记忆库支持两种记忆内容类型：

- **记忆片段**：从对话中自动提取的关键事件和信息（如"用户每天上午9点需要喝水提醒"）。适用于大多数长期记忆场景。
- **用户画像**：基于自定义模板从对话中提取的结构化用户属性（如年龄、职业、偏好等）。适用于需要持久化存储固定属性的场景。

记忆库的工作机制包括两个核心环节：

- **自动记忆捕获（autoCapture）**：对话结束后自动提取关键信息并存储。
- **自动记忆召回（autoRecall）**：对话开始前自动检索相关记忆并注入上下文。

详细的功能说明请参考 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 和 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 使用方式

### 通过 API 直接调用

长期记忆 API 提供以下核心接口，使用前需配置 `DASHSCOPE_API_KEY` 环境变量：

| 操作 | API | 说明 |
|------|-----|------|
| 写入记忆 | `AddMemory` | 传入对话内容，自动提取记忆片段；也支持 `custom_content` 直接写入指定内容 |
| 检索记忆 | `SearchMemory` | 基于语义检索相关历史记忆，建议 `top_k` 设为 3~10 |
| 列出记忆 | `ListMemory` | 分页列出指定用户的所有记忆条目 |
| 更新记忆 | `UpdateMemory` | 按 `memory_node_id` 更新记忆内容 |
| 删除记忆 | `DeleteMemory` | 按 `memory_node_id` 删除指定记忆 |

写入记忆的基本示例（cURL）：

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

Python SDK 可通过 `agentscope-runtime` 包调用，安装命令：`pip install agentscope-runtime`。完整的 API 参数和代码示例请参见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

### 通过 OpenClaw 插件集成

对于使用 OpenClaw Agent 的场景，百炼提供了 `modelstudio-memory-for-openclaw` 插件，可以零代码实现长期记忆能力。安装和配置流程详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

安装命令：

```bash
openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw
```

插件的核心配置项（在 `~/.openclaw/openclaw.json` 中设置）：

| 配置项 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `apiKey` | string | 是 | DashScope API Key（以 `sk-xxx` 开头） |
| `userId` | string | 是 | 用户标识符，用于隔离记忆空间 |
| `autoCapture` | boolean | 否 | 对话后自动提取并存储记忆，默认 `true` |
| `autoRecall` | boolean | 否 | 对话前自动检索并注入记忆，默认 `true` |
| `topK` | number | 否 | 每次召回返回的记忆条数，默认 `5` |
| `minScore` | number | 否 | 最小相似度阈值（0-100），默认 `0` |

> **注意**：OpenClaw 记忆插件为统一配置，所有 Agent 共享同一记忆，暂不支持按 Agent 独立配置。

插件安装后还会向 Agent 注册四个工具（`memory_search`、`memory_store`、`memory_list`、`memory_forget`），Agent 可在对话中根据语境主动调用。

## 记忆库管理

### 创建与配置

在百炼控制台的[记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)可以创建和管理记忆库。每个账号自带一个默认记忆库，无需额外创建即可直接使用。

记忆规则包括两类，每个记忆库最多可配置 50 条记忆片段规则和 50 条用户画像规则：

- **记忆片段规则**：定义如何从对话中提取关键事件和信息。支持默认规则指令和自定义规则指令，可配置自动更新和记忆过期时间（7 天 / 30 天 / 180 天 / 永不过期）。
- **用户画像规则**：定义需要提取的结构化用户属性字段及其描述。

用户画像通过 API 使用时的流程：`CreateProfileSchema`（创建模板） -> `AddMemory`（传入 `profile_schema` 提取画像） -> `GetUserProfile`（获取画像）。详细操作请参考 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。

### 检索调试

控制台提供记忆检索调试功能，支持配置以下参数优化召回效果：

- **最大召回数量**：每次检索返回的记忆条数（1~100）
- **意图判别召回**：系统自动判断当前对话是否需要召回记忆，建议开启
- **改写**：优化查询语句提升语义检索准确率，口语化提问时建议开启
- **排序**：使用 `gte-rerank-v2` 模型对结果重排，相似度阈值建议设在 0.5~0.7

## 配额与限制

长期记忆 API 存在以下速率限制（阿里云账号级别）：

| API 操作 | 速率上限 |
|----------|----------|
| AddMemory（写入） | 120 次/分钟 |
| SearchMemory（查询） | 300 次/分钟 |
| 所有操作合计 | 3000 次/分钟 |

性能指标参考：

- SearchMemory 端到端延迟：200-500ms
- AddMemory 延迟：500-1000ms
- 自动捕获异步执行，不影响响应速度

> **注意**：该功能与 API 调用限时免费。生成的记忆片段与用户画像暂无失效日期（通过 API 添加时），但通过控制台配置的记忆片段规则可设置过期时间。

## 来源文档

- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


