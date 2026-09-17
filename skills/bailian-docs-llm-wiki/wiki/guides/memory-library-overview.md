# memory library [overview](overview.md)

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于解决大模型上下文窗口限制导致的跨会话信息丢失问题。它通过语义驱动的记忆提取、向量化存储与检索机制，使智能体能够持续理解用户偏好、历史事件和结构化属性。该能力以 API 为统一入口，支持开发者在任意应用中集成自动捕获、主动召回与手动管理等完整记忆生命周期操作。

## 支持的模型/功能

- **记忆片段（Memory Nodes）**：从对话消息中自动提取关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、元数据标注、智能去重与动态更新。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（User Profile）**：基于预定义 Schema 从对话中结构化抽取固定属性（如年龄、职业、爱好），支持字段描述引导、初始值设定与多轮增量更新。适用于需强 schema 约束的业务场景。  
- **双模式策略支持**：`Pro`（默认）与 `Lite` 两种记忆处理策略版本，分别对应不同质量与成本权衡（详见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
- **全链路自动化**：OpenClaw 等框架可通过插件实现 `autoCapture`（对话结束自动写入）与 `autoRecall`（对话开始前自动检索注入），无需修改业务逻辑 —— 具体配置见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 1 称“记忆片段默认有效期 180 天”，而文档 3 明确说明“生成的记忆片段与用户画像暂无失效日期”。实际行为以 API 运行时参数为准：`AddMemory` 请求中若显式传入 `expired_in_days` 则按此生效；未传时由关联的 MemoryProject 规则决定（默认规则为 180 天），但系统不强制过期删除，仅影响检索可见性。请以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 中 `expired_in_days` 参数定义为准。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 | 来源 |
|------|------|----------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；同一 `user_id` 下所有记忆可被检索 | 所有 API |
| `memory_library_id` | string | 否 | 指定记忆库 ID；不传则使用默认记忆库 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 指定记忆片段规则 ID；不传则使用默认规则 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `profile_schema` | string | 否 | 用户画像模板 ID；传入后触发画像字段抽取 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `plan_version` | string | 否 | 取值 `"pro"` 或 `"lite"`；`SearchMemory` 中独立控制本次检索策略；`AddMemory` 策略由 `project_id` 对应规则的 `plan_version` 决定 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `top_k` | number | 否 | 检索返回最大条数，默认 `5`（OpenClaw 插件）或 `10`（API 默认） | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |

## 使用方式

1. **准备环境**：设置 `DASHSCOPE_API_KEY` 环境变量（获取方式见[获取 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。  
2. **写入记忆**：调用 `AddMemory` 接口，传入 `messages`（对话历史）或 `custom_content`（直接内容）及 `user_id`。支持指定 `memory_library_id`、`project_id` 和 `profile_schema`。  
3. **检索记忆**：调用 `SearchMemory` 接口，传入 `user_id` 和自然语言查询 `query`（或 `messages`），可选 `top_k`、`plan_version`。  
4. **管理记忆**：使用 `ListMemory`（分页查询）、`UpdateMemory`（PATCH）、`DeleteMemory`（DELETE）进行运维；用户画像需配合 `CreateProfileSchema`、`GetUserProfile` 使用。  
5. **集成框架**：OpenClaw 用户可直接安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，通过 `openclaw.json` 配置 `apiKey` 与 `userId` 即启用全自动捕获与召回 —— 详情见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别限流，总计 ≤3000 QPM；其中 `AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM（见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。  
- **延迟特性**：`AddMemory` 端到端延迟约 500–1000ms，`SearchMemory` 约 200–500ms；自动捕获为异步执行，不影响主流程响应速度。  
- **策略版本一致性**：`AddMemory` 的处理质量由其关联的 MemoryProject 的 `plan_version` 决定；`SearchMemory` 的 `plan_version` 仅影响本次调用，与 project 无关 —— 此设计允许灵活组合（如 lite 写入 + pro 检索）。  
- **画像字段命名**：避免语义近义字段（如“姓名”/“名字”/“名称”）共存，否则影响抽取准确率；建议单次对话聚焦少量字段，通过多轮逐步完善画像（见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 起正式计费，此前为免费试用期（见[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 和 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


