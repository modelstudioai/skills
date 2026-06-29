# 记忆能力对比（长期记忆 vs 记忆库）

百炼平台提供两种面向"跨会话上下文持久化"的记忆能力描述入口：一是 **长期记忆（新）**（API 参考视角，`api/long-term-memory-new.md`），二是 **记忆库（Memory Library）**（用户指南视角，`guides/memory-library-overview.md`）。两者本质指向同一套底层长期记忆 API（`https://dashscope.aliyuncs.com/api/v2/apps/memory/*`），但在文档定位、接入方式、管理入口和适用对象上存在差异。本页从技术选型角度对二者进行对比，帮助开发者快速判断应参考哪一份文档、采用哪种接入路径。

## 关键维度对比

| 维度 | 长期记忆（新）（API 参考） | 记忆库（Memory Library）（用户指南） |
| --- | --- | --- |
| 文档定位 | RESTful API 接口参考，逐接口说明请求/响应字段 | 能力总览与接入指南，含概念、控制台管理与插件接入 |
| 受众 | 直接调用 HTTP API 的后端/服务端开发者 | 需要端到端方案选型、含控制台与零侵入接入的开发者 |
| Base URL | `https://dashscope.aliyuncs.com/api/v2/apps/memory/` | 同上（`https://dashscope.aliyuncs.com/api/v2/apps/memory/*`） |
| 认证方式 | Header `Authorization: Bearer $DASHSCOPE_API_KEY` | 环境变量 `DASHSCOPE_API_KEY`，同样以 `Bearer` 方式携带 |
| 接口覆盖 | AddMemory / SearchMemory / ListMemory / DeleteMemory / UpdateMemory / CreateProfileSchema / ListProfileSchemas / DeleteProfileSchema / UpdateProfileSchema / GetProfileSchema / GetUserProfile 共 11 个 | 重点讲 AddMemory / SearchMemory，并补充 ListMemory、CreateProfileSchema、GetUserProfile 等封装类 |
| SDK 支持 | 以 cURL 示例为主 | 额外提供 Python `agentscope-runtime` 封装类，需在 `finally` 调 `close()` |
| 零侵入接入 | 未涉及 | 提供 OpenClaw 记忆插件，`before_agent_start`/`agent_end` 钩子自动召回/捕获 |
| 控制台管理 | 未涉及 | 支持控制台可视化管理记忆库、记忆规则、默认有效期 |
| 记忆有效期 | 明确"生成的记忆片段与用户画像暂无失效日期" | 控制台默认规则 180 天，可配置 7/30/180 天或永不过期；以控制台规则为准 |
| 限流说明 | 给出账号级 QPM：全局 3000、add 120、search 300 | 未在总览中给出 QPM 数字 |
| 检索增强参数 | 列出 `top_k`/`min_score`/`enable_rerank`/`enable_judge`/`enable_rewrite` | 仅点出 `top_k`、`minScore`（插件）等关键参数 |
| 画像能力 | 完整的 Profile Schema CRUD 与 GetUserProfile 接口 | 介绍画像模板概念与 `profileSchema` 配置项，接口细节指向 API 参考 |
| [计费](../concepts/billing.md)方式 | 未在本页说明 | 未在本页说明（统一走 DashScope [计费](../concepts/billing.md)） |
| 典型场景 | 需要精细控制记忆 CRUD、画像模板、检索召回参数的服务端集成 | 需要快速接入、可视化运维或让 OpenClaw Agent 自动具备记忆 |

## 适用场景建议

- **参考"长期记忆（新）"文档的情况**：你需要直接对接 HTTP API，关心每个接口的请求体、响应字段、`event` 事件类型（ADD/UPDATE/DELETE）、画像模板的完整 CRUD，或需要按 `enable_rerank`/`enable_judge`/`enable_rewrite` 等参数精细调优检索召回；适合自研 Agent 后端、需要严格接口契约的服务端开发者。
- **参考"记忆库"文档的情况**：你希望先从业务视角理解"记忆片段 vs 用户画像"两类持久化内容的差异与组合用法，或希望通过控制台创建/编辑记忆库与记忆规则、配置有效期，又或者你的 Agent 运行在 OpenClaw 之上，希望以插件方式零侵入获得"自动捕获/自动召回"能力；适合做整体方案选型与低代码运维的团队。
- **二者结合使用**：多数生产落地建议先读"记忆库"理解概念与管理入口，再用"长期记忆（新）"对照接口字段落地代码；OpenClaw 用户可仅依赖插件配置项即可跑通，深定制时再回查 API 参考。

## 技术选型参考

1. 接入路径：纯后端 HTTP 调用 → 选 API 直连（两份文档均适用，接口细节以"长期记忆（新）"为准）；OpenClaw Agent → 选记忆插件（仅"记忆库"文档覆盖）。
2. 有效期策略：若需记忆按天失效，务必以控制台记忆规则配置为准（默认 180 天）；API 直写且不指定 `project_id` 时走默认规则，"暂无失效日期"的说法仅适用于不经过规则提炼的直写场景。
3. 命名空间隔离：两份文档均强调 `user_id` 为记忆空间隔离维度，不同 `user_id` 完全隔离；OpenClaw 插件目前所有 Agent 共享同一记忆，暂不支持按 Agent 独立配置，也不支持百炼 Coding Plan 的 API Key。
4. 检索质量：需要重排序、意图判别、query 重写等高级召回能力时，参考"长期记忆（新）"的 SearchMemory 参数；插件场景受 `topK`/`minScore` 配置项约束。
5. 画像存储：需要固定结构化属性（年龄、职业、偏好等）持久化时使用用户画像，字段命名应清晰具体、避免同义并存；接口细节走"长期记忆（新）"的 Profile Schema 系列。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


