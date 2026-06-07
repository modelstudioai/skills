# memory library overview

记忆库是百炼平台提供的长期记忆解决方案，通过自动从对话中提取关键信息并持久化存储，使智能体能够跨会话持续引用用户偏好和历史信息。记忆库提供开放的 API 接口，可接入任意应用，也支持多应用共享同一记忆库。该功能与 API 调用目前限时免费。

## 核心功能

记忆库支持两种记忆内容类型：

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **记忆片段** | 从对话中自动提取的关键事件和信息，如"用户每天上午9点需要喝水提醒" | 大多数长期记忆场景 |
| **用户画像** | 基于自定义模板从对话中提取的结构化属性，如年龄、职业、偏好等 | 需要持久化存储固定属性的场景 |

根据 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 文档，相比旧版 API 的改进包括：

- 更低延迟、更高的记忆检索召回效果
- 支持从对话中自动提取关键信息并自动去重
- 新增语义检索能力，检索准确性显著提升
- 新增完整的用户画像提取和管理能力

> **注意**：[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 文档中提到记忆过期时间可选 7 天、30 天、180 天、永不过期；而 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 文档中则表述为"生成的记忆片段与用户画像暂无失效日期"。实际行为以控制台配置的记忆规则为准。

## 使用流程

1. 获取 API Key，创建或使用默认记忆库
2. 每轮对话结束后，调用 `AddMemory` 写入记忆
3. 在控制台查看和检索记忆，或调用 `SearchMemory` 在应用中检索
4. 将检索结果注入 Prompt，实现个性化回答

## 主要 API 接口

| 接口 | 功能 |
|------|------|
| `AddMemory` | 写入对话或自定义内容至记忆库 |
| `SearchMemory` | 基于语义检索相关历史记忆 |
| `ListMemory` | 分页列出记忆片段 |
| `UpdateMemory` | 更新指定记忆片段内容 |
| `DeleteMemory` | 删除指定记忆片段 |
| `CreateProfileSchema` | 创建用户画像模板 |
| `GetUserProfile` | 获取完整的用户画像 |

### 关键参数

**AddMemory 参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `user_id` | 是 | 记忆实体的用户标识 |
| `messages` | 与 `custom_content` 二选一 | 对话消息列表 |
| `custom_content` | 与 `messages` 二选一 | 直接指定要存入的记忆内容 |
| `memory_library_id` | 否 | 记忆库 ID，不填则使用默认记忆库 |
| `project_id` | 否 | 记忆片段规则 ID |
| `profile_schema` | 否 | 用户画像规则 ID |
| `meta_data` | 否 | 自定义元数据，用于分类管理 |

**SearchMemory 参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `user_id` | 是 | 用户标识 |
| `messages` | 是 | 查询消息 |
| `top_k` | 否 | 返回的记忆条数，建议 3~10 |
| `memory_library_id` | 否 | 记忆库 ID |

### 基本示例

```bash
# 写入记忆
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

# 检索记忆
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "messages": [{"role": "user", "content": "我需要做什么？"}],
    "top_k": 5
  }'
```

Python SDK 需安装 `agentscope-runtime`（`pip install agentscope-runtime`），详细代码示例请参见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 文档。

## 记忆规则配置

在控制台创建记忆库后可配置记忆规则，每个记忆库最多支持：

- 50 条记忆片段规则
- 50 条用户画像规则

**记忆片段规则参数：**
- 规则名称：唯一标识
- 规则指令：定义抽取策略（默认或自定义）
- 自动更新：开启后模型自动更新记忆内容
- 记忆过期时间：7 天 / 30 天 / 180 天 / 永不过期

**用户画像最佳实践：**
- 画像字段及描述应清晰、具体，避免过于抽象
- 属性名称应保证语义唯一（如"姓名"和"名字"不应同时出现）
- 不应期望一次对话就能提取所有信息，应通过多轮对话收集

## 集成方式

除直接调用 API 外，记忆库还支持通过插件集成到第三方 Agent 框架。例如 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 文档介绍了如何通过生命周期钩子实现自动记忆捕获和召回，无需手动调用 API。

插件核心机制：
- **autoCapture**：对话结束后自动提取关键信息存储
- **autoRecall**：对话开始前自动检索相关记忆注入上下文

## 配额与限制

| API 操作 | 速率上限 |
|----------|----------|
| AddMemory（写入） | 120 次/分钟 |
| SearchMemory（查询） | 300 次/分钟 |
| 所有操作合计 | 3000 次/分钟 |

**性能指标：**
- SearchMemory 端到端延迟：200–500ms
- AddMemory 延迟：500–1000ms

**其他限制：**
- 记忆库为账号级别资源，每个账号自带一个默认记忆库（不可删除）
- 检索时建议将 `top_k` 设置在 3~10 之间以平衡性能和效果
- 排序模型目前仅支持 gte-rerank-v2
- 相似度阈值建议设置在 0.5~0.7 之间

> **注意**：SearchMemory 的 API 端点在不同文档中存在差异：记忆库文档使用 `/api/v2/apps/memory/search`，长期记忆 API 文档使用 `/api/v2/apps/memory/memory_nodes/search`。请以 API 参考文档为准。

## 环境变量

| 环境变量 | 必需 | 说明 |
|----------|------|------|
| `DASHSCOPE_API_KEY` | 是 | 百炼 API 密钥 |

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



