# memory library overview

记忆库旨在突破大语言模型上下文窗口的物理限制，解决跨会话信息丢失导致的对话割裂问题。系统通过在交互过程中自动提取关键事件与用户属性，并将其持久化存储为向量索引，使应用能够在后续会话中精准召回历史上下文。平台提供标准化 API 与管理控制台，支持多应用共享同一记忆空间以实现全局个性化体验。

## 支持的模型/功能
- **记忆片段（Memory Fragment）**：自动从历史对话中提炼非结构化关键信息，支持基于语义的动态更新与检索。适用于通用业务场景的长期上下文保持。详细抽取与配置逻辑见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。
- **结构化用户画像（User Profile）**：基于预定义的 Schema 模板，从多轮对话中抽取并维护固定属性（如年龄、职业、偏好）。支持初始值设定与增量更新，适用于强规则依赖的个性化业务。
- **自动化插件集成**：提供 `modelstudio-memory-for-openclaw` 插件，通过生命周期钩子实现对话前后自动捕获与召回。架构与部署指南详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 关键参数
| 参数名 | 类型 | 说明 |
|:---|:---|:---|
| `user_id` | `string` | 用户唯一标识。用于隔离不同用户的记忆命名空间（必填）。 |
| `memory_library_id` | `string` | 目标记忆库 ID。未传参时默认调用系统内置的 [[default-memory-library]]。 |
| `project_id` | `string` | 记忆片段规则 ID，控制自动更新策略、过期时间与抽取指令。 |
| `profile_schema` | `string` | 用户画像模板 ID。传入后 `AddMemory` 将触发结构化属性抽取。 |
| `top_k` / `min_score` | `int` / `float` | 控制检索返回条数与向量相似度阈值。推荐 `top_k: 3~10`，`min_score: 0.5~0.7`。 |
| `auto_capture` / `auto_recall` | `bool` | 插件级开关，分别控制会话结束后的写入与会话开始前的检索注入（默认 `true`）。 |
| `meta_data` | `object` | 自定义键值对元数据。支持按业务维度（如优先级、模块）对记忆进行分类过滤。 |

## 使用方式
1. **鉴权准备**：配置环境变量 `[[DASHSCOPE_API_KEY]]`，获取方式参考 [[get-api-key]]。
2. **写入记忆**：在每轮对话结束后调用 `AddMemory` 接口。支持传入完整 `messages` 数组供模型自动提炼，或通过 `custom_content` 直接写入指定内容。
3. **检索与注入**：在新会话发起前调用 `SearchMemory`，传入当前用户 Query。将返回的高相关性记忆片段拼接至 System Prompt 或上下文窗口，再发送至 [[llm-model]]。
4. **生命周期管理**：通过 `ListMemory` 分页浏览，`UpdateMemory` 修正错误信息，`DeleteMemory` 清除过期或敏感数据。
5. **完整接口规范**：请求体结构、分页参数与错误码处理请参考 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 中的最新定义。

## 限制和注意事项
- **速率限制（QPM）**：单阿里云账号级别限制如下：`AddMemory` 120 次/分，`SearchMemory` 300 次/分，所有接口合计上限 3000 次/分。高频写入需实现指数退避重试。
- **性能延迟**：`SearchMemory` 端到端延迟约 200–500ms，`AddMemory` 约 500–1000ms。画像提取为异步任务，建议调用后设置 3 秒缓冲再查询结果。
- **规则上限**：单个记忆库最多允许配置 50 条记忆片段规则与 50 条用户画像规则，超出将拒绝创建。
> **注意**：不同文档对检索接口路径的表述存在版本差异（如 `/memory/search` 与 `/memory/memory_nodes/search`）。实际集成请以官方控制台提供的 SDK 或最新 API Reference 为准，避免路径路由错误。
> **注意**：原文档间关于记忆有效期存在矛盾。控制台默认预置规则标注有效期为 180 天，但 API 概览文档声明“生成的记忆片段与用户画像暂无失效日期”。生产环境建议依赖 `meta_data` 结合业务逻辑自行实现 TTL 清理策略。
- **插件共享机制**：OpenClaw 插件采用全局统一配置，所有 Agent 实例共享同一记忆空间，当前暂不支持按 Agent ID 独立隔离配置。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)

