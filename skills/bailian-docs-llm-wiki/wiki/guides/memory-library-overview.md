# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力组件，用于解决大模型受上下文窗口限制、无法跨会话保留信息的问题。它通过自动从对话中提取关键事件（记忆片段）和结构化属性（用户画像），并持久化存储与语义检索，使智能体具备跨会话的个性化理解与连贯交互能力。该能力以开放 API 形式提供，支持任意应用接入及多应用共享同一记忆库。

## 支持的模型/功能

- **记忆片段（Memory Nodes）**：从对话消息中自动提取关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、语义检索、更新与删除。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。
- **用户画像（Profile Schema）**：基于预定义模板从对话中结构化抽取固定属性（如年龄、职业、爱好），支持创建、更新、获取完整画像。适用于需强 schema 约束的用户建模场景。
- **双模式策略支持**：AddMemory 和 SearchMemory 均支持 `pro`（开启 Rerank，质量更高）与 `lite`（关闭 Rerank，成本更低）两种策略版本，计费与行为分离，详见[长期记忆 API](raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

> **注意**：文档 1 中称“用户画像规则默认有效期 180 天”，而文档 3 明确说明“生成的记忆片段与用户画像暂无失效日期”。此处以文档 3 的权威表述为准，即**用户画像本身无内置过期机制**；记忆片段的过期由关联的 Memory Project 规则控制，非画像模板自身属性。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；同一 `user_id` 下所有记忆共享命名空间。 |
| `memory_library_id` | string | 否 | 指定记忆库 ID；不传时使用默认记忆库（不可删除）。参见[记忆库](raw/application-user-guide/memory-library-overview/memory-library.md)。 |
| `project_id` | string | 否 | 记忆片段规则 ID；不传时使用默认项目规则（预置，180 天有效期）。 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需触发画像提取时必传。 |
| `meta_data` | object | 否 | 自定义元数据，用于分类管理（如 `"location_name": "北京"`）。 |
| `plan_version` | string | 否（Search 默认 `pro`；Add 由 project 决定） | 控制策略版本：`pro`（启用 Rerank）或 `lite`（禁用 Rerank）。Search 的 `plan_version` 优先级高于 `enable_rerank`，且独立于 Memory Project 的 `plan_version`。 |

## 使用方式

1. **准备环境**：配置 `DASHSCOPE_API_KEY` 环境变量（获取方式见[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)）。
2. **写入记忆**：
   - 调用 `AddMemory` 接口，传入 `messages`（对话历史）或 `custom_content`（直接写入内容），指定 `user_id` 及可选的 `project_id` / `profile_schema`。
   - 示例：`curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add ...`
3. **检索记忆**：
   - 调用 `SearchMemory` 接口，传入 `user_id` 和自然语言查询 `query`（或 `messages`），设置 `top_k`（建议 3–10）和 `plan_version`。
   - 示例：`curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search ...`
4. **管理记忆**：
   - 列出：`ListMemory`（分页查询 `memory_nodes`）
   - 更新：`UpdateMemory`（PATCH `/memory_nodes/{id}`）
   - 删除：`DeleteMemory`（DELETE `/memory_nodes/{id}`）
   - 画像管理：`CreateProfileSchema` → `AddMemory`（带 `profile_schema`）→ `GetUserProfile`

OpenClaw 用户可直接安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，通过 `autoCapture`/`autoRecall` 钩子实现全自动记忆捕获与召回，详情见[为 OpenClaw 配置长期记忆插件](raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **配额限制**（阿里云账号级别）：
  - 总调用量：≤ 3000 QPM
  - `AddMemory`：≤ 120 QPM
  - `SearchMemory`：≤ 300 QPM
- **延迟参考**：`SearchMemory` 端到端延迟 200–500ms；`AddMemory` 延迟 500–1000ms（自动捕获为异步，不影响主响应流）。
- **策略版本兼容性**：`plan_version` 不区分大小写（`"pro"`/`"PRO"` 等效）；非法值将返回报错；修改 Memory Project 的 `plan_version` 仅影响后续新增记忆，存量记忆不受影响。
- **画像字段设计**：避免语义重叠字段（如同时定义“姓名”“名字”“名称”），否则影响抽取效果；单次对话难以提取全部画像字段，建议通过多轮对话渐进收集。
- **商业化提示**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式开始商业化计费，Pro/Lite 版本计费标准详见[长期记忆 API](raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


