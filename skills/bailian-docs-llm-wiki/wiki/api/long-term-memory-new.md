# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户状态存储与语义检索能力，支持从对话中自动抽取关键事实并持久化为记忆片段，同时提供画像模板管理、多策略搜索与分页管理等核心功能。该能力通过 RESTful API 和 `agentscope-runtime` SDK 两种方式接入，适用于需要跨会话维持上下文、构建个性化服务的场景。所有接口均需使用 DashScope API Key 进行认证。

## 支持的模型/功能

- **记忆抽取模型**：Add 接口支持 `pro` 与 `lite` 两个质量版本（对应不同抽取精度），由 `profile_schema` 或隐式策略决定；Search 接口通过 `plan_version`（`pro`/`lite`）控制是否启用 Rerank 模块，详见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **核心功能**：
  - `AddMemory`：从 `messages`（最多 50 条）或 `custom_content`（≤512 字符）中提取结构化记忆；
  - `SearchMemory`：基于语义相似度召回，并支持 `top_k`、`min_score`、`enable_rerank`、`enable_rewrite` 等精细控制；
  - `ListMemory` / `DeleteMemory` / `UpdateMemory`：对记忆片段进行 CRUD 管理；
  - `ProfileSchema` 系列接口：定义、查询、更新用户画像模板，用于驱动画像提取（需在 Add 时显式传入 `profile_schema`）。

> **注意**：文档中 `AddMemory` 的 `messages` 字段说明称“一问一答算 2 条”，但未明确定义“问答对”的边界（如连续多轮 user/assistant 是否必须严格交替）。实际调用应确保 `role` 值合法且顺序合理，避免因格式异常导致抽取失败。该细节在 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中未进一步澄清，建议以实际请求返回的 `memory_nodes` 数量为准进行调试。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | body/query | string | 是 | 记忆归属实体 ID（≤64 字符），所有接口均需提供 |
| `memory_library_id` | body/query | string | 否 | 记忆库 ID（≤32 字符），不传则使用默认库；[获取方式见控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) |
| `messages` / `custom_content` | body | array / string | 互斥 | `messages` 为 role-content 对数组（最多 50 条）；`custom_content` 为纯文本（≤512 字符），优先级更高 |
| `profile_schema` | body | string | 否 | 画像模板 ID，传入后触发用户画像提取；ID 需从 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 所述记忆库详情页获取 |
| `top_k`, `min_score`, `plan_version` | body | int / double / string | 否 | Search 接口专用：`top_k∈[1,100]`（默认 10），`min_score∈[0,1]`（默认 0.3），`plan_version` 优先级高于 `enable_rerank` |

## 使用方式

- **HTTP 调用**：Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，Header 必须包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。
- **SDK 调用**：推荐使用 `agentscope-runtime>=1.1.5`，已封装全部接口类（如 `AddMemory`, `SearchMemory`），示例见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 Python 片段。
- **典型流程**：
  1. 创建记忆库并获取 `memory_library_id`；
  2. （可选）调用 `CreateProfileSchema` 定义画像模板；
  3. 调用 `AddMemory` 写入记忆（传 `profile_schema` 启用画像）；
  4. 调用 `SearchMemory` 检索相关记忆，结合 `top_k` 与 `min_score` 控制召回质量；
  5. 使用 `ListMemory` 分页查看或 `DeleteMemory`/`UpdateMemory` 维护数据。

## 限制和注意事项

- **限流**：阿里云账号级别总计 ≤3000 QPM；其中 `AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM。
- **计费节点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化计费，Add 和 Search 均按 `pro`/`lite` 版本区分定价，详情参见 [记忆库计费标准](https://help.aliyun.com/zh/model-studio/memory-library#h3-pricing)。
- **数据时效性**：当前生成的记忆片段与用户画像**无自动失效机制**，需业务侧自行管理生命周期。
- **字段约束**：`user_id`、`memory_library_id`、`memory_node_id` 等 ID 类字段长度均有明确上限，超长将导致 400 错误；`custom_content` 与 `messages` 互斥，若同时提供，后者被忽略。
- **时间戳**：`UpdateMemory` 的 `timestamp` 为秒级 Unix 时间戳（非毫秒），默认使用当前时间。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)


