# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、结构化提取参数，并按约定协议触发外部工具或服务执行的关键能力。它不是简单的 API 转发，而是由大模型在推理过程中自主决策“何时调用、调用哪个、传什么参数”，再将结果注入后续生成流程，实现模型能力的动态扩展。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口，而是贯穿多个能力层的统一语义机制，具体体现为以下三类实践路径：

- **Assistant API 场景（推荐首选）**：通过 `tools` 数组注册函数定义（含 `tool_id`、`description`、`parameters`），模型自动解析用户输入、生成符合 OpenAPI Schema 的参数对象，并返回 `tool_calls` 字段；开发者需按 `tool_call.id` 和 `function.name` 执行对应逻辑，再将结果以 `tool_results` 形式回传给 `/v1/threads/runs` 继续执行。适用于智能体编排、RAG+工具混合调度等复杂工作流。

- **Managed Agents（托管智能体）场景**：底层封装为 `Skill` 能力，通过 `/v1/agents/{agent_id}/skills` 注册自定义工具后，在运行时由 `qwen-max` 等托管模型触发 `tool_call` 事件；响应需通过 `POST /v1/agents/{agent_id}/sessions/{session_id}/tool_results` 提交，平台自动处理上下文注入与多步编排。优势在于免运维状态管理与跨 Session Memory 持久化。

- **插件（Plug-in）场景**：面向控制台快速集成，本质是预置的函数调用封装。官方插件（如 `calculator`、`quark_search`）和自定义插件均需配置 `tool_id` 与参数契约，调用时模型输出 `tool_calls` 后，平台自动透传 `biz_params` 并注入 `Authorization` header（唯一支持透传的 header），无需开发者手动发起 HTTP 请求。

> ⚠️ 注意：所有场景下，函数调用均由模型自主触发，**不支持客户端强制指定调用**；模型是否触发、触发哪个工具，取决于其对 `description` 和 `parameters` 的理解质量，建议保持描述简洁精准、参数类型明确（避免嵌套过深）。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `tool_id` | `tools[].tool_id`（Assistant API）、`skills[].id`（Managed Agents）、插件配置页 | string | 工具唯一标识，必须与注册时完全一致；大小写敏感，不可含空格 |
| `parameters` | `tools[].parameters`（OpenAPI 3.0 JSON Schema） | object | 定义输入参数结构，**必需包含 `type` 和 `description`**；GET 类型插件不支持 `object` 类型入参（报错 `130022`） |
| `biz_params` | Assistant API 请求体 `input.biz_params` 或 Managed Agents `input` 中 | object | 业务透传参数（如用户 ID、会话上下文），仅当插件配置为“业务透传”模式时生效 |
| `stream` | 请求体顶层参数 | boolean | 启用后，函数调用过程中的 `tool_call`、`tool_result` 等事件将以 SSE 流式返回，便于前端实时渲染中间状态 |
| `Authorization` | 请求 header | string | **唯一允许透传的 header**，用于携带 Bearer [Token](token.md) 或 AppCode，其他自定义 header 将被平台过滤 |

## 面向开发者，简洁实用

- ✅ **必做**：所有函数定义必须提供完整、无歧义的 `description` 和 `parameters` Schema；缺失 `description` 将导致发布失败（错误码 `130040`）。  
- ✅ **推荐**：优先使用 Assistant API 进行开发——它提供最标准的 [OpenAI 兼容接口](openai-compatible-api.md)、最灵活的工具注册方式，且 SDK（Python/Java）已内置 `tool_calls` 解析与 `tool_results` 回传逻辑。  
- ⚠️ **避坑**：  
  - 不要尝试在 `GET` 请求中传递复杂对象参数；改用 `POST` + `application/json`；  
  - 不要依赖模型自动填充未声明的参数字段；所有需传参字段必须显式定义在 `parameters` 中；  
  - 自定义插件调试阶段务必完成“测试成功→发布”闭环，草稿状态无法被模型调用；  
  - 文件类工具（如 `text_to_image`）需单独申请开通，且限时免费，勿用于生产环境长期调用。  
- 🚀 **进阶提示**：结合 RAG 使用时，可将知识库检索结果作为 `biz_params` 注入函数调用，实现“先查知识，再调工具”的确定性编排；Managed Agents 的 `Memory Store` 可自动缓存历史 `tool_result`，供后续 Session 复用。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)
- [managed agents api](../api/managed-agents-api.md)


