# 记忆能力对比：记忆库与长期记忆

百炼平台为解决大模型跨会话上下文丢失问题提供了完整的记忆能力体系。本文对比「记忆库概览」（guides/memory-library-overview）与「长期记忆（新）API」（api/long-term-memory-new）两个文档，帮助开发者理解两者在定位、覆盖范围和使用方式上的差异，以便在技术选型时快速定位所需信息。

## 对比维度

| 维度 | 记忆库概览（memory-library-overview） | 长期记忆（新）API（long-term-memory-new） |
| --- | --- | --- |
| 文档定位 | 概念指南，介绍记忆库整体架构、核心能力与接入方式 | API 参考手册，详细列出全部 RESTful 接口的端点、参数与返回值 |
| 目标读者 | 做技术选型、架构设计的开发者与产品经理 | 直接调用 API 进行集成的后端开发者 |
| 覆盖范围 | 涵盖 API 直连、OpenClaw 插件、控制台管理、记忆规则配置 | 聚焦于 HTTP API 层面，不涉及 OpenClaw 插件与控制台操作 |
| Base URL | `https://dashscope.aliyuncs.com/api/v2/apps/memory/*`（提及） | `https://dashscope.aliyuncs.com/api/v2/apps/memory/`（完整说明） |
| 认证方式 | `Authorization: Bearer $DASHSCOPE_API_KEY` | `Authorization: Bearer $DASHSCOPE_API_KEY`，并指引 [API Key](../concepts/api-key.md) 获取链接 |
| 核心能力 | 记忆片段 + 用户画像，含自动去重、动态更新 | 记忆片段 + 用户画像，含完整 CRUD 接口 |
| 接入方式 | API 直连 + OpenClaw 记忆插件（零侵入） | 仅 API 直连 |
| 接口列表 | 仅列举 AddMemory、SearchMemory 的关键参数 | 完整列出 11 个接口（增删改查记忆片段 + 画像模板全生命周期） |
| 使用限制 | 未提及 QPM 限制 | 明确标注：总 3000 QPM、add 120 QPM、search 300 QPM |
| 记忆有效期 | 说明差异：API 文档称暂无失效日期，控制台默认 180 天 | 明确标注：生成的记忆片段与用户画像暂无失效日期 |
| 检索高级参数 | 提及 top_k、memory_library_id | 详列 top_k、min_score、enable_rerank、enable_judge、enable_rewrite、project_ids 等 |
| OpenClaw 插件 | 完整覆盖：安装、配置项、生命周期钩子说明 | 不涉及 |
| 控制台管理 | 涉及记忆库与记忆规则管理说明 | 不涉及 |
| 示例代码 | cURL + Python（agentscope-runtime） | cURL 为主，含请求/返回体完整字段说明 |

## 详细差异分析

### 文档定位与覆盖范围

**记忆库概览**是从产品视角出发的入门指南，回答"记忆库是什么、能做什么、怎么接入"的问题。它同时覆盖了三种接入路径——API 直连、OpenClaw 插件、控制台可视化管理——让读者快速建立整体认知。

**长期记忆（新）API**则是从工程视角出发的接口参考，回答"具体调哪个端点、传什么参数、返回什么结构"的问题。它将全部 11 个接口以表格形式列出，并逐一给出 HTTP 方法、路径与说明，适合直接查阅。

### 接口完整度

| 接口能力 | 记忆库概览 | 长期记忆（新）API |
| --- | --- | --- |
| AddMemory（添加记忆） | 有参数说明 | 有完整请求体/返回体说明 |
| SearchMemory（搜索记忆） | 有参数说明 | 有完整请求体/返回体说明 + 高级检索参数 |
| ListMemory（列出记忆） | 提及封装类 | 有独立接口条目 |
| DeleteMemory（删除记忆） | 未涉及 | 有独立接口条目 |
| UpdateMemory（更新记忆） | 未涉及 | 有独立接口条目 |
| CreateProfileSchema（创建画像模板） | 提及封装类 | 有独立接口条目 |
| ListProfileSchemas | 未涉及 | 有独立接口条目 |
| DeleteProfileSchema | 未涉及 | 有独立接口条目 |
| UpdateProfileSchema | 未涉及 | 有独立接口条目 |
| GetProfileSchema | 未涉及 | 有独立接口条目 |
| GetUserProfile | 提及封装类 | 有独立接口条目 |

### 接入方式差异

记忆库概览介绍了两种接入方式：

1. **API 直连**：通过 HTTPS 调用 `memory/*` 系列接口，适合需要灵活控制写入与检索流程的应用。
2. **OpenClaw 记忆插件**：通过 `before_agent_start`（自动召回）和 `agent_end`（自动捕获）两个生命周期钩子实现零侵入接入，适合已使用 OpenClaw Agent 框架的场景。所有读写均由百炼服务端完成提炼、向量化和语义检索。

长期记忆（新）API 文档仅覆盖 API 直连方式，不涉及插件接入，但提供了更完整的接口集（包括记忆片段和画像模板的增删改查全生命周期）。

### 检索能力

在 SearchMemory 接口上，长期记忆（新）API 文档提供了更丰富的高级检索参数：

| 高级参数 | 记忆库概览 | 长期记忆（新）API |
| --- | --- | --- |
| `top_k` | 有（建议 3–10） | 有（取值 1~100，默认 10） |
| `min_score` | 无 | 有（值域 [0,1]，默认 0.3） |
| `enable_rerank` | 无 | 有（搜索结果重排序） |
| `enable_judge` | 无 | 有（意图判别回调） |
| `enable_rewrite` | 无 | 有（query 重写） |
| `project_ids` | 无 | 有（多规则混合检索） |

### 使用限制

长期记忆（新）API 文档明确给出了 QPM 限制：

| 限制项 | 值 |
| --- | --- |
| 全部接口总计 | 3000 QPM |
| 记忆片段 add 接口 | 120 QPM |
| 记忆片段 search 接口 | 300 QPM |

记忆库概览文档未提及这些限制，开发者需参考 API 参考文档了解限流策略。

## 适用场景建议

### 推荐阅读「记忆库概览」的场景

- **技术选型阶段**：需要了解百炼记忆能力整体架构，评估是否满足业务需求
- **选择接入方式**：需要对比 API 直连与 OpenClaw 插件两种方案的优劣
- **配置 OpenClaw 插件**：需要安装、配置记忆插件的详细步骤
- **理解记忆有效期**：需要了解控制台记忆规则与 API 行为的差异
- **控制台管理记忆库**：需要通过可视化界面管理记忆库和规则

### 推荐阅读「长期记忆（新）API」的场景

- **API 集成开发**：需要查阅具体接口的请求体、返回体字段定义
- **实现记忆 CRUD**：需要调用 List/Delete/Update 等概览文档未覆盖的接口
- **画像模板管理**：需要创建、更新、删除画像模板
- **高级检索调优**：需要使用 rerank、judge、rewrite 等高级检索参数
- **容量与限流评估**：需要了解 QPM 限制以做容量规划
- **精确参数查阅**：需要确认 `top_k` 取值范围、`min_score` 默认值等细节

## 总结

两个文档并非竞争关系，而是互补关系。记忆库概览是**入门与选型的起点**，长期记忆（新）API 是**开发与集成的落点**。建议开发者先阅读记忆库概览建立整体认知、选定接入方式，再查阅长期记忆（新）API 获取具体接口实现细节。两者配合使用可以完成从技术评估到工程落地的完整闭环。

## 被对比主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)


