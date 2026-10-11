# memory library [overview](overview.md)

记忆库是为大模型提供跨会话长期记忆的 API 服务，通过自动从对话中提取关键信息并持久化存储为事实记忆与用户画像，在后续对话中基于语义检索相关记忆并注入上下文，从而突破上下文窗口限制，实现个性化、连贯的智能体交互。它支持多应用共享、灵活规则配置，并提供完整的开放接口体系。

## 支持的模型/功能

- **两类核心记忆类型**：  
  - **事实记忆**：自动从对话中提取动态事件信息（如“用户每天上午9点需要喝水提醒”），适用于临时性、时效性场景；  
  - **用户画像**：基于自定义模板提取结构化用户属性（如年龄、职业、爱好），适用于固定属性的持久化管理。二者可独立或协同使用。  
- **双策略版本支持**：Add 和 Search 操作均支持 `Pro`（开启 Rerank，检索质量更高）与 `Lite`（关闭 Rerank，成本更低）两种策略版本，满足不同精度与成本诉求 [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)。  
- **集成路径**：支持 **Agent Harness**（百炼智能体一键配置）和 **插件**（如 OpenClaw 工作流集成）两种方式，覆盖低代码与代码化场景 [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。  
- **异步能力**：提供 `AddMemoryAsync` 接口用于高吞吐写入场景，配合 `GetEvent` 查询任务状态 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

> **注意**：文档 1 和文档 3 均声明商业化计费起始时间为 **2026 年 8 月 20 日 10:00（北京时间）**，但文档 15 的计费说明中明确该时间点为“正式开始商业化计费”，而文档 1 的警告语句未加“正式”二字，属表述冗余，以文档 15 为准。

## 关键参数

| 参数 | 说明 | 取值/范围 | 备注 |
|------|------|-----------|------|
| `user_id` | 记忆实体唯一标识，用于隔离不同用户数据 | 字符串 | 必填，所有读写操作均以此为维度 |
| `plan_version` | 控制 Add/Search 策略版本 | `"Pro"` / `"Lite"` | Add 版本由记忆规则配置决定；Search 版本由请求参数独立控制，不传默认 `Pro` [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md) |
| `top_k` | 检索最大返回条数 | `1–100` | 默认值未显式声明，建议按需设置（如 `5` 或 `10`） |
| `min_score` | 相似度阈值，过滤低相关性结果 | `0.0–1.0` | Pro 版本生效，默认 `0.3`；建议调优至 `0.5–0.7` [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md) |
| `memory_library_id` | 指定目标记忆库 ID | 字符串 | 非必填；不传时使用默认记忆库 |
| `profile_schema` | 用户画像模板 ID | 字符串 | 调用 `AddMemory` 时传入方可触发画像提取 [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md) |

## 使用方式

1. **开通与准备**：在[百炼控制台记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)点击**立即开通**，并获取有效的 `DASHSCOPE_API_KEY`。  
2. **写入记忆**：调用 `POST /add`，传入 `messages`（对话历史）和 `user_id`；若需提取画像，额外传入 `profile_schema`。示例见[快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)。  
3. **检索记忆**：调用 `POST /memory_nodes/search`，传入 `user_id` 和当前 `messages`，可选 `top_k`、`min_score`、`plan_version`。  
4. **管理记忆**：通过 `GET /memory_nodes` 列表查看，`PATCH /memory_nodes/{id}` 更新，`DELETE /memory_nodes/{id}` 删除；用户画像需先创建模板（`POST /profile_schemas`），再调用 `GET /profile_schemas/{id}/user_profile` 获取。  
5. **控制台调试**：在记忆库详情页的**记忆检索**标签页可实时调试参数效果，支持开启“意图判别召回”“改写”“排序”等增强选项。

## 限制和注意事项

- **限流策略**（阿里云账号级别）：  
  - 全部接口总计 ≤ 3000 QPM；  
  - `AddMemory` ≤ 120 QPM；  
  - `SearchMemory` ≤ 300 QPM；  
  超出返回 HTTP `429`，需实现退避重试 [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。  
- **默认记忆库不可删除**，仅可编辑名称、描述及规则；自定义记忆库删除后数据不可恢复。  
- **用户画像提取为异步过程**：`AddMemory` 返回成功不代表画像已就绪，首次 `GetUserProfile` 可能为空，需按业务逻辑重试（如等待 3 秒后查询）[使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。  
- **存储有效期**：事实记忆/画像默认永不过期，除非在记忆规则中显式配置过期时间（如 7/30/180 天）；免费额度中的 10,000 条存储长期有效，其余存储按 ¥0.002/万条/小时计费 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **策略版本切换影响范围**：更新记忆规则的 `plan_version` 后，**仅新写入的记忆**遵循新策略，历史记忆不受影响；Search 的 `plan_version` 参数对每次请求独立生效。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)


