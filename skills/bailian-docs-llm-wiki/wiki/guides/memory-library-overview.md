# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话[长期记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储，解决大模型上下文窗口限制导致的“每次对话从零开始”问题。它支持两种核心记忆类型（事实记忆与用户画像），提供开放 API 与控制台管理能力，并可被多个应用共享。商业化计费将于 2026 年 8 月 20 日 10:00（北京时间）起正式生效，详见[计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。

## 支持的模型/功能

- **事实记忆**：自动从对话消息中提取动态事件信息（如“用户每天上午 9 点需要喝水提醒”），适用于偏好变更、待办事项等时效性较强的内容。  
- **用户画像**：基于预定义模板提取结构化用户属性（如年龄、职业、爱好），适用于固定且长期稳定的用户特征。两者可同时使用，协同增强个性化能力。  
- **自动捕获与召回**：在 OpenClaw 等工作流中，可通过插件实现 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索注入）[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。  
- **集成路径**：支持两种接入方式——**Agent Harness**（面向百炼智能体的零代码配置）和**插件**（面向工作流的 SDK/CLI 集成）[集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。

> **注意**：文档 4 中提出的“记忆片段（MemoryNode）”与“记忆变量”概念，与文档 1/3/6 定义的“事实记忆”和“用户画像”存在术语不一致。当前官方统一采用 **事实记忆**（对应 MemoryNode）和 **用户画像**（对应结构化 Profile）作为标准术语，所有 API、控制台及新文档均以此为准；文档 4 属于旧版[长期记忆](../concepts/memory.md)功能描述，其“记忆变量”实际等价于用户画像字段，“记忆片段”即事实记忆节点。

## 关键参数

| 参数 | 说明 | 取值/范围 | 备注 |
|------|------|-----------|------|
| `user_id` | 记忆实体隔离维度，必填 | 字符串 | 不同 `user_id` 的记忆完全隔离；默认用于控制台筛选与 API 路径 |
| `plan_version` | 控制 Add/Search 调用策略版本 | `"Pro"` 或 `"Lite"` | `Add` 版本由记忆规则配置决定；`Search` 版本由请求参数独立控制，默认 `"Pro"` [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md) |
| `min_score` | 相似度阈值，过滤低相关性结果 | `0.0`–`1.0` | 建议 `0.5`–`0.7`；过低引入噪声，过高漏召 [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md) |
| `top_k` | 单次检索最大返回条数 | `1`–`100` | 默认 `10`；需结合业务精度与 Token 成本权衡 |
| `profile_schema` | 用户画像模板 ID | 字符串 | 调用 `AddMemory` 时传入才触发画像提取；未传则仅生成事实记忆 |

## 使用方式

1. **开通与准备**：首次使用需在[百炼控制台记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)点击**立即开通**，并获取 `DASHSCOPE_API_KEY`。  
2. **写入记忆**：调用 `AddMemory` 接口，传入 `messages`（对话历史）和 `user_id`；若需提取画像，额外传入 `profile_schema`。示例见[快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)。  
3. **检索记忆**：调用 `SearchMemory` 接口，传入 `user_id` 和当前 `query`（或 `messages`），指定 `top_k` 与 `min_score`；检索结果需手动注入 Prompt。  
4. **管理与调试**：  
   - 控制台：在**记忆详情**页按 `user_id` 查看/编辑记忆；在**记忆检索**页实时调试参数效果。  
   - API：使用 `ListMemory`、`UpdateMemory`、`DeleteMemory` 进行全生命周期管理。  

## 限制和注意事项

- **限流**：全部接口总计 ≤ 3000 QPM（阿里云账号级别）；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM。超限返回 HTTP `429`，需实现退避重试 [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。  
- **存储与过期**：默认记忆库不可删除；自定义记忆库删除后数据**不可恢复**；事实记忆有效期可在规则中配置（7/30/180 天或永不过期），用户画像无默认过期机制。  
- **异步行为**：用户画像提取为异步过程，调用 `AddMemory` 后需等待约 3 秒再调用 `GetUserProfile` 获取结果 [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。  
- **计费影响**：`SearchMemory` 返回的记忆内容将作为上下文注入大模型，产生额外 Token 消耗，该部分费用**不包含在记忆库计费中**，需单独计算模型调用成本。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/memory.md)
- [长期记忆](../../raw/application-user-guide/memory-library-overview/memory/long-term-memory.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)


