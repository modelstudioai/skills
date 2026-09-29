# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话[长期记忆](../concepts/long-term-memory.md)服务，通过自动从对话中提取关键信息并持久化存储，解决大模型上下文窗口限制导致的会话状态丢失问题。它支持两种核心记忆类型（事实记忆与用户画像），提供开放 API 与控制台管理能力，并可被多个应用共享。所有调用均通过 DashScope 网关鉴权，服务地址为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`。

## 支持的模型/功能

- **事实记忆**：自动从对话消息中提取动态事件信息（如“每天上午9点提醒我喝水”），适用于行为、偏好、待办等时效性较强的内容。提取逻辑由预置或自定义的**事实记忆规则**驱动，每条规则可独立配置过期时间（7/30/180天或永不过期）和策略版本（Pro/Lite）[配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)。
- **用户画像**：基于结构化模板（`ProfileSchema`）提取固定用户属性（如年龄、职业、爱好），需显式传入 `profile_schema` 参数调用 `AddMemory` 才触发提取 [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。
- **多集成路径**：支持 Agent Harness（零代码控制台配置）与插件模式（如 OpenClaw 工作流集成），后者通过生命周期钩子（`before_agent_start`/`agent_end`）实现自动捕获与召回 [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。

> **注意**：文档 11 明确指出“生成的事实记忆与用户画像暂无失效日期（除非在创建记忆库时配置了记忆过期时间）”，但文档 1 和 5 均强调默认记忆库预置规则的“默认有效期 180 天”。实际行为以**规则级配置为准**，即未显式设置过期时间的规则将按默认值（180天）生效；若规则设为“永不过期”，则对应记忆不自动过期。

## 关键参数

| 参数 | 说明 | 取值/范围 | 备注 |
|------|------|-----------|------|
| `user_id` | 记忆实体 ID，用于跨会话隔离用户数据 | 字符串 | 必填，所有读写操作的基础维度 |
| `plan_version` | 控制 Pro/Lite 策略版本 | `"Pro"` 或 `"Lite"` | **Add 调用**由记忆规则配置决定；**Search 调用**由请求参数独立控制，默认 `"Pro"` [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md) |
| `top_k` | 检索返回的最大记忆条数 | 1–100 | 默认值未明确，建议显式设置（如 `10`） |
| `min_score` | 相似度阈值，过滤低相关性结果 | `0.0`–`1.0` | Pro 版本生效，建议 `0.5`–`0.7`；Lite 版本忽略此参数 |
| `profile_schema` | 用户画像模板 ID | 字符串 | 调用 `AddMemory` 时传入才触发画像提取 |

## 使用方式

1. **初始化**：开通服务后获取 `DASHSCOPE_API_KEY`，服务地址固定为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`。
2. **写入记忆**：调用 `POST /add`，传入 `messages`（对话历史）和 `user_id`；若需提取画像，额外传入 `profile_schema`。
3. **检索记忆**：调用 `POST /memory_nodes/search`，传入 `user_id` 和当前 `messages`（用于语义匹配），可选 `top_k`、`min_score`、`plan_version`。
4. **管理记忆**：支持 `GET /memory_nodes`（列表）、`GET /memory_nodes/{id}`（详情）、`PATCH /memory_nodes/{id}`（更新）、`DELETE /memory_nodes/{id}`（删除）。

示例（cURL 检索）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --data '{
    "user_id": "user_001",
    "messages": [{"role": "user", "content": "我需要做什么？"}],
    "top_k": 10,
    "min_score": 0.6,
    "plan_version": "Lite"
  }'
```

## 限制和注意事项

- **限流**：阿里云账号级别总计 ≤ 3000 QPM；`/add` 接口 ≤ 120 QPM；`/memory_nodes/search` 接口 ≤ 300 QPM。超限返回 HTTP `429`，需实现退避重试 [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。
- **异步行为**：用户画像提取为异步过程，首次 `GetUserProfile` 可能返回空值，需按业务逻辑重试（文档 8 建议 `await asyncio.sleep(3)` 后查询）。
- **默认记忆库**：每个账号自带一个不可删除的默认记忆库，已预置“默认项目”事实记忆规则（有效期 180 天），但可编辑其名称、描述及规则 [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)。
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式开始计费，Add/Search 调用区分 Pro/Lite 版本，免费额度自该日起 3 个月内有效 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)


