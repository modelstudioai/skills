# 记忆库与长期记忆对比

百炼平台为解决大模型跨会话上下文丢失的问题，提供了围绕"长期记忆"的完整能力。在文档体系中，这一能力以两种视角呈现：

- **记忆库（Memory Library）**：偏产品与方案视角，强调接入方式（控制台 / HTTP API / OpenClaw 插件）、记忆片段与用户画像两类内容形态，以及记忆规则与有效期等可运营配置。
- **长期记忆（新）API**：偏接口与实现视角，给出 RESTful 端点、请求/响应字段、限流策略和画像模板（Profile Schema）的完整 CRUD。

二者底层共用同一套 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 服务，记忆片段与用户画像的数据模型一致；区别在于"封装层"和"可控粒度"。本文从开发者技术选型角度对两者进行对比。

## 关键维度对比

| 维度 | 记忆库（Memory Library） | 长期记忆（新）API |
| --- | --- | --- |
| 定位 | 上层方案与产品形态：跨会话记忆的整体接入 | 底层 RESTful 接口参考：程序化记忆管理 |
| 文档位置 | 应用使用指南（guides） | 应用 API 参考（api） |
| 接入方式 | 控制台可视化管理 + HTTP API + OpenClaw 插件零侵入 | 直接 HTTPS 调用 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| 记忆内容 | 记忆片段 + 用户画像（两类可独立或组合使用） | 记忆片段 + 用户画像（同一数据模型） |
| 写入输入 | `messages`（自动提取）或 `custom_content`（直写，最大 512 字符），二选一 | 同左，`messages` 最多 50 条对话 |
| 检索能力 | `SearchMemory`，主要参数 `top_k`（建议 3–10） | `SearchMemory`，含 `top_k`（1–100，默认 10）、`min_score`（默认 0.3）、`enable_rerank`/`enable_judge`/`enable_rewrite`、`project_ids` 多规则混合检索 |
| 管理 API | 重点呈现 `AddMemory` / `SearchMemory`（写入与召回） | `AddMemory` / `SearchMemory` / `ListMemory` / `UpdateMemory` / `DeleteMemory` + 画像模板 CRUD + `GetUserProfile` |
| 画像管理 | 通过 `profile_schema` 参数提取画像，模板在记忆库详情页获取 | 提供 `CreateProfileSchema` / `ListProfileSchemas` / `UpdateProfileSchema` / `DeleteProfileSchema` / `GetProfileSchema` 全套接口 |
| 记忆有效期 | 控制台默认规则 180 天，可配 7/30/180 天或永不过期；按规则可编辑 | API 文档标注"生成的记忆片段与用户画像暂无失效日期"（以控制台记忆规则配置为准） |
| 记忆规则 | 每账号自带默认记忆库 + 默认规则（不可删除），可创建新记忆库与规则 | 通过 `memory_library_id`、`project_id` 参数指定记忆库与规则；不传使用默认 |
| 用户隔离 | `user_id` 命名空间隔离，OpenClaw 插件所有 Agent 共享同一记忆 | `user_id` 最大 64 字符，用于标识记忆归属 |
| 限流 | 未单独列出，复用底层 API 限额 | 全部接口合计 ≤ 3000 QPM；`add` 120 QPM；`search` 300 QPM |
| 客户端 SDK | Python `agentscope-runtime`（`AddMemory` / `SearchMemory` 等封装，需 `close()`） | 以 cURL / REST 为主，参数与字段为权威定义 |
| 插件支持 | OpenClaw `modelstudio-memory-for-openclaw`：`before_agent_start` 自动召回 + `agent_end` 自动捕获 | 不直接涉及，插件内部回调此 API |
| 典型场景 | 跨会话个性化、Agent 偏好记忆、控制台运营记忆规则、OpenClaw 零侵入接入 | 程序化记忆 CRUD、画像模板生命周期管理、批量召回与重排序、自建记忆编排 |

## 适用场景建议

### 选择"记忆库（Memory Library）"视角当

- 需要在控制台可视化地创建记忆库、配置记忆片段规则与有效期（7/30/180 天或永不过期）。
- 希望以"产品方案"形式接入，例如通过 OpenClaw 插件实现 `autoCapture` / `autoRecall` 的零侵入跨会话记忆，而不愿手写每轮的写入与检索调用。
- 业务侧关注的是"用户偏好持续化""Agent 跨会话理解"等整体能力，而非单个接口字段。

### 选择"长期记忆（新）API"视角当

- 需要在自研应用中精细控制每一步记忆操作：写入、搜索、列表、更新、删除，以及对画像模板做完整的增删改查。
- 需要使用高级检索参数（`min_score` 阈值、`enable_rerank` 重排序、`enable_judge` 意图判别、`enable_rewrite` query 重写、`project_ids` 多规则混合检索）来调优召回质量。
- 需要依据明确的限流（3000 QPM 总量、add 120 QPM、search 300 QPM）做容量规划与重试策略。
- 需要程序化维护用户画像模板的字段定义，或对接已有用户体系做批量画像写入与读取。

## 技术选型小结

记忆库与长期记忆（新）API 并非二选一的两套系统，而是**同一能力的产品层与接口层**：

- 做方案设计与运营配置时，以"记忆库"文档为准（接入方式、记忆规则、有效期、OpenClaw 插件配置）。
- 做接口对接与字段实现时，以"长期记忆（新）API"文档为准（端点、参数、返回结构、限流、画像模板 CRUD）。

实践建议：先用记忆库视角确定接入形态（控制台 / API / 插件）与记忆规则，再在长期记忆（新）API 中查证具体端点与字段；两者配合即可覆盖从产品方案到代码实现的完整链路。注意记忆有效期以控制台记忆规则配置为准——API 文档的"暂无失效日期"指 API 直写且不指定 `project_id` 时使用默认规则的情形。

## 被对比主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)


