# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话[长期记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储，解决大模型上下文窗口限制导致的会话间信息丢失问题。它支持事实记忆与用户画像两类结构化记忆形式，并提供开放 API 供开发者集成到各类智能体和工作流中。所有功能均基于 DashScope 网关统一鉴权与调用。

## 支持的模型/功能

- **两类核心记忆类型**：  
  - **事实记忆**：自动从对话中提取动态事件信息（如“每天上午9点提醒我喝水”），适用于行为、偏好、临时状态等可变信息；  
  - **用户画像**：基于预定义模板提取结构化静态属性（如年龄、职业、爱好），需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中传入 `profile_schema` 参数触发提取。  
  两者可共存使用，分别覆盖不同语义场景，详见[核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)。

- **两种集成路径**：  
  - **Agent Harness**：面向百炼原生智能体，通过控制台配置即可启用跨会话记忆，无需编码；  
  - **插件方式**：面向 OpenClaw 等工作流框架，通过 `@modelstudio/modelstudio-memory-for-openclaw` 插件实现自动捕获（`autoCapture`）与自动召回（`autoRecall`），支持 `memory_search`、`memory_store` 等工具调用，具体实践参见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 13 中插件默认使用 `memoryLibraryId` 和 `projectId` 的自动 fallback 行为（如不传则选默认记忆库及默认规则），但文档 7 明确指出“默认项目”规则不可删除、仅可编辑——这意味着插件在未显式指定 `projectId` 时的行为强依赖该默认规则的可用性与配置一致性，生产环境建议显式传入稳定 ID。

## 关键参数

| 参数 | 说明 | 取值/范围 | 默认值 | 备注 |
|------|------|-----------|--------|------|
| `user_id` | 记忆实体隔离维度，必填 | 字符串 | — | 不同 `user_id` 完全隔离；同一 `user_id` 下所有记忆共享命名空间 |
| `plan_version` | 控制 Pro/Lite 策略版本 | `"Pro"` 或 `"Lite"` | `"Pro"` | **Add 调用**由记忆规则配置决定；**Search 调用**由请求参数独立控制（与规则无关）；详见[计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md) |
| `top_k` | 检索最大返回条数 | 1–100 | `10`（API） / `5`（插件） | 过高易引入噪声，建议按业务需求设为 3–10 |
| `min_score` | 相似度阈值（过滤低相关结果） | `0.0`–`1.0` | `0.3`（API） / `0`（插件） | 推荐 `0.5–0.7` 平衡召回率与精度；插件文档中 `minScore` 单位为 `0–100`（整数），需注意单位转换 |
| `memory_library_id` | 指定目标记忆库 | 字符串 | 默认记忆库 | 可在控制台记忆库卡片上获取 ID |
| `profile_schema` | 用户画像模板 ID | 字符串 | — | `AddMemory` 中必须传入才触发画像提取；提取为异步过程，首次 `GetUserProfile` 可能为空，需重试 |

## 使用方式

1. **快速验证（3 步）**：  
   - 调用 `AddMemory` 写入对话（含 `user_id` 和 `messages`）；  
   - 通过控制台「记忆详情」页或 `ListMemory` API 查看写入结果；  
   - 调用 `SearchMemory`（传 `user_id` + 当前 `messages`）检索历史记忆，将返回的 `memory_nodes` 注入 Prompt 即可。完整示例见[快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)。

2. **自定义规则（推荐生产使用）**：  
   - 在控制台创建新记忆库（或复用默认库）；  
   - 进入「记忆规则」标签页，配置最多 50 条事实记忆规则（含过期时间、`plan_version`）和 50 条用户画像规则（含字段定义与初始值）；  
   - 规则生效后，后续 `AddMemory` 自动按规则抽取，`SearchMemory` 可指定 `project_id` 精准召回。

3. **高级操作**：  
   - 更新/删除单条记忆：使用 `UpdateMemory`（PATCH `/memory_nodes/{id}`）或 `DeleteMemory`（DELETE `/memory_nodes/{id}`）；  
   - 批量管理：结合 `meta_data` 字段添加业务标签，提升后续检索精度；  
   - 异步写入：对高吞吐场景，可用 `AddMemoryAsync` 提交任务，再轮询 `GetEvent` 获取状态。

## 限制和注意事项

- **限流策略**（阿里云账号级别）：  
  - 全部接口合计 ≤ 3000 QPM；  
  - `AddMemory` ≤ 120 QPM；  
  - `SearchMemory` ≤ 300 QPM；  
  超出返回 HTTP `429`，需实现退避重试。详细限流规则见[限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。

- **商业化与免费额度**：  
  - **2026 年 8 月 20 日 10:00（北京时间）起正式计费**；  
  - 商业化后赠送 1,500 次 Add（分 6 类规格）和 5,000 次 Search（分 2 类规格），3 个月内有效；存储 10,000 条永久免费；  
  - Pro/Lite 版本单价差异显著（如 Search Pro ¥0.001/次 vs Lite ¥0.00002/次），需根据准确率要求与成本预算权衡选择。

- **关键注意事项**：  
  - 默认记忆库**不可删除**，仅可编辑名称、描述与规则；  
  - 记忆内容无全局失效机制（除非规则中配置了过期时间），需主动调用 `DeleteMemory` 或控制台删除；  
  - 用户画像提取为异步过程，`AddMemory` 返回成功不代表画像已就绪，`GetUserProfile` 需等待并重试；  
  - 检索结果注入 Prompt 后，将额外增加大模型 [Token](../concepts/token.md) 消耗，此部分费用**不包含在记忆库计费中**，需单独核算。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)


