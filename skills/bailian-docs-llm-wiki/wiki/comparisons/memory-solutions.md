# 长期记忆与记忆库对比

百炼平台为解决大模型跨会话上下文丢失的问题，提供了长期记忆能力。该能力以"长期记忆（新）API"和"记忆库"两种形态对外服务：前者是一组 RESTful 接口，开发者可自行编排写入与检索流程；后者在 API 之外还提供控制台可视化管理与 OpenClaw 插件零侵入接入。本文从输入格式、接入方式、API 端点、[计费](../concepts/billing.md)、典型场景等维度进行对比，帮助开发者在技术选型时做出合适选择。

## 关键维度对比

| 维度 | 长期记忆（新）API | 记忆库（Memory Library） |
| --- | --- | --- |
| 定位 | 纯接口层，提供记忆片段与用户画像的 CRUD | 能力集合 + 管理入口，包含 API、控制台、OpenClaw 插件三种接入 |
| 接入方式 | HTTPS 直调 `https://dashscope.aliyuncs.com/api/v2/apps/memory/*` | API 直连（同左）、控制台可视化管理、OpenClaw 插件零侵入 |
| 认证方式 | `Authorization: Bearer $DASHSCOPE_API_KEY` | 同 API；OpenClaw 插件在 `openclaw.json` 配置 `apiKey` |
| 输入格式 | `messages`（对话数组，最多 50 条）或 `custom_content`（自定义文本，最大 512 字符），二者互斥 | 同 API；OpenClaw 插件通过生命周期钩子自动捕获，无需手动传参 |
| 输出格式 | 返回 `memory_nodes`（含 `memory_node_id` / `content` / `event` / `old_content`）与 `request_id` | API 返回同左；控制台提供可视化列表；插件自动注入 Prompt |
| 核心接口 | AddMemory、SearchMemory、ListMemory、DeleteMemory、UpdateMemory、CreateProfileSchema、ListProfileSchemas、DeleteProfileSchema、UpdateProfileSchema、GetProfileSchema、GetUserProfile | 包含上述全部接口；额外提供控制台记忆规则管理与插件配置 |
| 记忆片段有效期 | 暂无失效日期 | 控制台默认规则预置 180 天有效期，支持按规则配置 7/30/180 天或永不过期；API 直写不指定 `project_id` 时使用默认规则 |
| 用户画像 | 通过 `profile_schema` 传入画像模板 ID，API 自动提取结构化属性 | 同 API；控制台可可视化管理画像模板 |
| 检索能力 | 语义相似度搜索，支持 `top_k`、`min_score`、`enable_rerank`、`enable_judge`、`enable_rewrite`、`project_ids` 混合检索 | API 检索同左；OpenClaw 插件通过 `topK`、`minScore`、`autoRecall` 配置自动召回 |
| 限流 | 全部接口合计 3000 QPM；AddMemory 120 QPM；SearchMemory 300 QPM | 同 API 限流规则 |
| [计费](../concepts/billing.md)方式 | 按 API 调用计量 | 同 API；OpenClaw 插件底层仍调用同一组接口 |
| 管理界面 | 无，纯接口 | 控制台记忆库详情页，可管理记忆片段规则、画像模板、查看记忆内容 |
| OpenClaw 支持 | 需自行对接 | 原生支持 `@modelstudio/modelstudio-memory-for-openclaw` 插件，`before_agent_start` 自动召回、`agent_end` 自动捕获 |
| 多 Agent 隔离 | 通过 `user_id` 隔离不同用户记忆空间 | OpenClaw 插件为统一配置，所有 Agent 共享同一记忆，暂不支持按 Agent 独立配置 |
| 语言 SDK | 原生 HTTP；Python 可用 `agentscope-runtime` 封装类 | 同 API；OpenClaw 提供独立插件 CLI |

## 适用场景建议

### 选择长期记忆（新）API 的场景

- **需要精细控制写入与检索流程**：开发者希望在对话结束后自行决定何时调用 `AddMemory`、何时调用 `SearchMemory`，并将召回结果以自定义方式注入 Prompt。
- **已有自研 Agent 框架**：不依赖 OpenClaw 生态，希望以纯 HTTP 方式集成到现有 Python / Java / Go 服务中。
- **需要混合检索与高级参数**：如开启重排序（`enable_rerank`）、意图判别（`enable_judge`）、query 重写（`enable_rewrite`）、多规则检索（`project_ids`）等。
- **需要自定义 `custom_content` 直写**：跳过对话提炼，直接写入指定文本。

### 选择记忆库（Memory Library）的场景

- **需要控制台可视化管理**：希望在百炼控制台直接查看、管理记忆片段规则、画像模板和已存储的记忆内容，而不仅通过 API。
- **使用 OpenClaw Agent 并希望零侵入接入**：通过插件实现自动捕获 / 自动召回，无需在业务代码中手动调用记忆接口。
- **需要灵活配置记忆有效期**：控制台规则支持 7/30/180 天或永不过期，适合对记忆保留周期有明确要求的业务。
- **快速原型验证**：控制台 + 插件组合可最快跑通"写入 → 检索 → 注入"闭环，降低初期集成成本。

### 二者组合使用

记忆库的 API 直连方式与长期记忆（新）API 面向同一组后端接口，二者并非互斥。常见组合是：生产环境用长期记忆（新）API 做精细控制，同时用控制台做运营管理与规则调优；若部分 Agent 基于 OpenClaw 构建，则这些 Agent 走插件通道，其余自研服务走 API。

## 技术选型参考

| 选型要点 | 推荐 |
| --- | --- |
| 自研框架、需要全链路控制 | 长期记忆（新）API |
| 基于 OpenClaw 的 Agent、希望最少代码改动 | 记忆库 + OpenClaw 插件 |
| 需要可视化管理记忆规则与内容 | 记忆库（控制台） |
| 对记忆有效期有差异化要求 | 记忆库（控制台规则配置） |
| 需要重排序、意图判别、query 重写等高级检索 | 长期记忆（新）API |
| 多用户、需要 `user_id` 隔离 | 两者均支持，按接入方式选择 |

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


