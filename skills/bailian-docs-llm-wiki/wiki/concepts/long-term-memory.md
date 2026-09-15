# 长期记忆

长期记忆是百炼平台提供的结构化、跨会话的用户状态持久化与语义检索能力，用于突破大模型上下文窗口限制，使智能体能在多次交互中持续理解用户偏好、关键事件和结构化属性（如习惯、身份、意图），实现真正连贯、个性化的对话体验。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用调用**：通过 `application call` API 的 `memory_id` 参数一键启用长期记忆。系统自动在会话开始时检索相关记忆片段与用户画像，并在会话结束时将新产生的关键信息（如用户新设定的提醒、确认的偏好）写入记忆库，全程无需开发者手动调用 Add/Search 接口。
  
- **记忆库（Memory Library）直接集成**：开发者可独立调用 `AddMemory` / `SearchMemory` 等原生接口，精细控制记忆生命周期。适用于需自定义提取逻辑、多规则混合检索（如 `project_ids: ["p1", "p2"]`）、或与外部系统（如 CRM）双向同步的场景。

- **OpenClaw 智能体框架**：通过安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，启用 `autoCapture`（自动从对话中提取记忆）与 `autoRecall`（自动在 [prompt](../guides/prompt.md) 中注入高相关性记忆），实现零代码接入，记忆行为完全由钩子驱动。

- **Managed Agents 托管运行时**：虽不直接暴露记忆接口，但其会话状态持久化机制与长期记忆能力正交互补——前者保障单次长任务的中断续接，后者保障跨任务、跨会话的用户认知延续；二者可协同构建“有状态、有记忆”的企业级智能体集群。

- **工作流（Workflow）与高代码应用**：需显式调用记忆 API 实现记忆增强。例如，在工作流的“决策节点”前插入 `SearchMemory` 调用，将检索结果作为上下文输入；或在高代码应用的 `main.py` 中使用 `agentscope-runtime` SDK 主动管理记忆，实现细粒度业务逻辑编排。

## 关键参数和配置

| 参数 | 类型 | 是否必填 | 说明 | 开发建议 |
|------|------|----------|------|----------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），用于隔离记忆空间。同一 `user_id` 下所有记忆共享命名空间。 | 建议与业务系统用户 ID 对齐（如 `"uid_12345"`），避免使用临时会话 ID。 |
| `memory_library_id` | string | 否 | 指定记忆库 ID；不传则使用默认库（不可删除）。生产环境建议显式指定，便于权限与配额管理。 | 控制台创建后获取，ID 格式为 `ml-xxx`。 |
| `project_id` | string | 否 | 记忆片段规则 ID；决定抽取策略与有效期（默认项目为 180 天）。不传则使用默认规则。 | 如需自定义过期策略（如“订单类记忆保留 30 天”），请提前创建专用 Project。 |
| `profile_schema` | string | 否（仅需画像时必填） | 用户画像模板 ID；传入后触发结构化字段（如 `age`, `job`）自动抽取。 | 使用 `CreateProfileSchema` 预定义 schema，字段名需语义清晰、无重叠（如勿同时定义 `name` 和 `full_name`）。 |
| `plan_version` | string | 否 | 检索/写入策略：`pro`（启用 Rerank，质量高）或 `lite`（禁用 Rerank，成本低）。大小写不敏感。 | `SearchMemory` 默认 `pro`；`AddMemory` 默认由 `project_id` 决定。对延迟敏感场景可设为 `lite`。 |
| `top_k` | integer | 否（Search 默认 10） | 最大召回数（1–100）。建议设为 `3–5`，避免噪声干扰 [prompt](../guides/prompt.md)。 | 过高（如 `top_k=50`）易引入低相关性记忆，影响模型推理稳定性。 |
| `min_score` | double | 否（默认 0.3） | 相似度阈值 [0,1]，低于此值的记忆不返回。 | 对精度要求高时（如金融问答），建议设为 `0.5–0.6`；对召回率要求高时（如用户习惯泛查），可降至 `0.2`。 |
| `meta_data` | object | 否 | 自定义键值对（如 `{"source": "app_ios", "category": "health"}`），支持分类、过滤与审计。 | 建议统一约定 key 命名规范（如全小写+下划线），便于后续 `ListMemory` 分页筛选。 |

> ⚠️ 注意：记忆片段与用户画像**无内置自动过期机制**；其生命周期由关联的 `project_id` 规则或开发者主动调用 `DeleteMemory` 控制。请勿依赖“默认过期”，务必按业务需求设计清理策略。

## 面向开发者，简洁实用

- **快速起步**：只需 `user_id` + `DASHSCOPE_API_KEY`，5 行代码即可完成记忆写入与检索（见 [long term memory new](api/long-term-memory-new.md) 中的 Python SDK 示例）。
- **性能优先**：`SearchMemory` 端到端延迟 200–500ms，`AddMemory` 异步执行（不影响主响应流）；高频调用请关注账号级 QPM 限制（Search ≤ 300 QPM，Add ≤ 120 QPM）。
- **策略解耦**：`plan_version` 控制质量/成本权衡，`project_id` 控制数据生命周期，`profile_schema` 控制结构化程度——三者正交，可自由组合。
- **生产就绪**：2026 年 8 月 20 日起正式商业化计费，`pro`/`lite` 版本独立计费，建议在灰度期明确选型并压测成本。
- **避坑提示**：
  - `messages` 中的多模态内容（如图片数组）**仅文本部分参与记忆抽取**，非文本内容被忽略；
  - `user_id` 必须传且稳定，变更将导致记忆断裂；
  - `SearchMemory` 的 `plan_version` 优先级高于 `enable_rerank`，传入 `plan_version` 时后者无效。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)
- [llm application](../guides/llm-application.md)


