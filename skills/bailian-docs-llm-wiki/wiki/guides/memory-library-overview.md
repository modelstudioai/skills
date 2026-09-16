# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于解决大模型上下文窗口限制导致的跨会话信息丢失问题。它通过语义驱动的记忆提取、向量化存储与检索机制，使智能体能够持续理解用户偏好、历史事件和结构化属性。该能力以 API 服务形式开放，支持直接集成到任意应用或通过 OpenClaw 等框架自动启用。

## 支持的模型/功能

- **记忆片段（Memory Nodes）**：从对话消息中自动提取关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、元数据标注（`meta_data`）、智能去重与动态更新。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（Profile Schema）**：基于预定义模板（如含“年龄”“职业”“爱好”字段）从对话中结构化抽取用户属性，支持初始值设定与多轮增量更新。适用于需固定属性建模的场景。  
- **双模式策略支持**：所有记忆提取与检索操作均支持 `pro`（开启 Rerank，质量更高）和 `lite`（关闭 Rerank，成本更低）两个策略版本，计费与行为分离，详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **自动捕获与召回**：在 OpenClaw 等框架中可通过插件生命周期钩子（`before_agent_start` / `agent_end`）实现零侵入式记忆写入与检索注入，无需修改业务逻辑。

> **注意**：文档 1 称“记忆片段默认有效期 180 天”，而文档 3 明确说明“生成的记忆片段与用户画像暂无失效日期”。实际行为以 API 运行时配置为准——记忆过期时间由创建 MemoryProject 时指定的 `expired_in_days` 参数控制，未显式设置则永不过期。请以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 中的参数定义为准。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离不同用户的记忆空间；同一 `user_id` 下记忆共享命名空间。 |
| `memory_library_id` | string | 否 | 记忆库 ID；不传则使用默认记忆库（不可删除）。可在[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)控制台卡片上获取。 |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用默认规则（预置“默认项目”）。影响 `AddMemory` 的提取策略与计费版本。 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需结构化提取画像时传入。不传则跳过画像提取。 |
| `plan_version` | string | 否（Search 默认 `pro`；Add 由 `project_id` 关联规则决定） | 控制策略版本：`pro`（启用 Rerank，¥0.001/次 Search；¥0.03/次 Add）或 `lite`（禁用 Rerank，¥0.00002/次 Search；¥0.018/次 Add）。Search 的 `plan_version` 优先级高于 `enable_rerank`。 |
| `meta_data` | object | 否 | 自定义键值对，用于分类管理记忆（如 `"category": "reminder"`），支持后续按条件过滤。 |

## 使用方式

1. **准备环境**：配置 `DASHSCOPE_API_KEY` 环境变量，获取方式见 [获取 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
2. **写入记忆**：调用 `AddMemory` 接口，传入 `messages`（对话历史）或 `custom_content`（自定义文本）及 `user_id`。推荐每轮对话结束后立即调用。  
3. **检索记忆**：调用 `SearchMemory` 接口，传入自然语言查询（如 `"我需要做什么？"`）和 `user_id`，返回语义最相关记忆片段列表。建议 `top_k` 设为 `3–10`。  
4. **管理记忆**：使用 `ListMemory`（分页查看）、`UpdateMemory`（PATCH 更新内容）、`DeleteMemory`（DELETE 删除）进行运维；用户画像通过 `CreateProfileSchema` → `AddMemory`（带 `profile_schema`）→ `GetUserProfile` 流程管理。  
5. **框架集成**：OpenClaw 用户可安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，通过 `openclaw.json` 配置 `apiKey` 和 `userId` 即可启用自动捕获与召回，详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别限流，总计 ≤3000 QPM；其中 `AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM。超出将返回 `429 Too Many Requests`。  
- **延迟特性**：`SearchMemory` 端到端延迟约 200–500ms，`AddMemory` 约 500–1000ms；自动捕获为异步执行，不影响主流程响应速度。  
- **策略版本独立性**：`SearchMemory` 的 `plan_version` 与 `MemoryProject` 的 `plan_version` 完全解耦——前者仅影响本次检索，后者仅影响关联 `AddMemory` 调用。二者可混用（如 project 为 `lite`，search 传 `pro`）。  
- **画像字段设计**：避免语义重复字段（如同时定义“姓名”“名字”“名称”），否则影响抽取准确率；单次对话难以覆盖全部画像字段，应通过多轮交互渐进填充。  
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式开始商业化计费，此前为免费试用期。计费细节请参考 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 中的定价说明。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


