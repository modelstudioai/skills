# 长期记忆 API 与记忆库对比

百炼平台围绕"跨会话记忆"提供了两个层次的文档视角：**长期记忆（新）API** 是底层 RESTful 接口规范，定义了记忆片段与用户画像的完整 CRUD 操作；**记忆库（Memory Library）** 则是面向用户的产品能力概述，涵盖控制台管理、API 接入和 OpenClaw 插件三种使用方式。二者本质上是同一套后端服务的不同入口——记忆库的 API 直连方式即为长期记忆（新）API。本文从开发者技术选型角度，对比两种接入路径的能力边界与适用场景。

## 关键维度对比

| 维度 | 长期记忆（新）API 直连 | 记忆库 + OpenClaw 插件 |
| --- | --- | --- |
| 接入方式 | HTTPS RESTful 调用，任意语言/框架 | OpenClaw 插件一键安装，零代码接入 |
| API 端点 | `https://dashscope.aliyuncs.com/api/v2/apps/memory/*`（11 个接口） | 插件内部封装同一组 API，无需直接调用 |
| 认证方式 | Header `Authorization: Bearer $DASHSCOPE_API_KEY` | 插件配置文件中填写 `apiKey`（`sk-` 开头） |
| 输入格式 | `messages`（对话列表，最多 50 条）或 `custom_content`（≤512 字符），二者互斥 | 由插件自动采集对话内容，无需手动构造 |
| 输出格式 | JSON：`memory_nodes` 数组（含 `memory_node_id`、`content`、`event`） | 自动注入 Agent 上下文，开发者无感知 |
| 记忆写入 | 手动调用 `AddMemory`，支持自动提取与自定义内容两种模式 | `autoCapture`（默认开启），对话结束自动提取存储 |
| 记忆召回 | 手动调用 `SearchMemory`，支持 `top_k`（1–100）、`min_score`、重排序、意图判别、query 重写 | `autoRecall`（默认开启），对话前自动检索注入，`topK` 默认 5 |
| 用户画像 | 支持完整生命周期：创建/更新/删除/查询画像模板 + 获取用户画像 | 通过 `profileSchema` 配置项关联画像模板 |
| 记忆库管理 | 通过 `memory_library_id` 指定目标记忆库 | 共享统一配置，所有 Agent 共用同一记忆空间 |
| 记忆规则 | 通过 `project_id` 指定片段规则（有效期、提取策略） | 使用默认记忆库的默认规则 |
| 多用户隔离 | `user_id` 字段（≤64 字符），不同 `user_id` 完全隔离 | 配置文件中 `userId` 字段，全局唯一 |
| 限流 | 全接口合计 3000 QPM；add 120 QPM；search 300 QPM（账号级） | 受同一账号级限流约束 |
| 有效期 | API 文档标注"暂无失效日期" | 控制台默认规则预置 180 天，可配置 7/30/180 天或永不过期 |
| SDK 支持 | Python `agentscope-runtime` 封装类（`AddMemory`、`SearchMemory` 等） | OpenClaw CLI 命令（`plugins install`、`modelstudio-memory stats`） |
| 控制台可视化 | 无（纯 API） | 支持在百炼控制台查看/管理记忆库与规则 |

## 适用场景建议

### 选择 API 直连的场景

- **自定义应用集成**：需要在自有后端服务中精确控制记忆的写入时机、检索策略和 Prompt 注入逻辑。
- **高级检索需求**：需要启用重排序（`enable_rerank`）、意图判别（`enable_judge`）、query 重写（`enable_rewrite`）等高级参数。
- **多记忆库/多规则管理**：业务上需要为不同场景创建独立记忆库和提取规则（如客服记忆与营销记忆分离）。
- **用户画像深度使用**：需要动态创建/更新画像模板，或在业务逻辑中直接消费结构化画像数据。
- **高吞吐写入**：需要批量或高频写入记忆（注意 add 接口限流 120 QPM）。

### 选择 OpenClaw 插件的场景

- **OpenClaw Agent 快速接入**：已有 OpenClaw 框架的 Agent，希望零代码获得跨会话记忆能力。
- **原型验证**：快速验证长期记忆对 Agent 效果的提升，无需编写集成代码。
- **统一记忆管理**：单用户或少量用户场景，所有 Agent 共享记忆空间即可满足需求。

### 注意事项

1. **有效期差异**：API 直写且不指定 `project_id` 时使用默认规则；控制台默认规则有 180 天有效期。如需永久记忆，应在控制台将规则有效期设为"永不过期"，或创建自定义规则并在 API 调用时指定 `project_id`。
2. **插件限制**：OpenClaw 插件为统一配置，不支持按 Agent 独立配置记忆空间；不支持百炼 Coding Plan 的 [API Key](../concepts/api-key.md)。
3. **混合使用**：两种方式操作的是同一后端存储，可以先用插件快速接入，后续再迁移到 API 直连做精细化控制，已有记忆数据不会丢失。

## 选型决策速查

| 决策因素 | 推荐方案 |
| --- | --- |
| 需要精细控制写入/检索逻辑 | API 直连 |
| 使用 OpenClaw 框架且无定制需求 | OpenClaw 插件 |
| 需要多记忆库隔离 | API 直连 |
| 需要控制台可视化管理 | 记忆库控制台 + API 直连 |
| 快速 MVP 验证 | OpenClaw 插件 |
| 需要用户画像完整 CRUD | API 直连 |

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)



