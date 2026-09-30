# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）与工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 与 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming.md)、多模态输入、[长期记忆](../concepts/memory.md)、RAG 检索等高级功能，适用于从轻量级对话到复杂多步骤任务的全场景集成。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）及工作流（Workflow）三类应用，但不同 API 路径和参数支持存在差异。
- **多模态能力**：支持图像（`image_list` / `input_image`）与文件（`file_list` / `input_file`）输入，需在应用中选用通义千问 VL 系列模型或配置对应文件处理方式 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。
- **增强功能**：
  - [长期记忆](../concepts/memory.md)（`memory_id`）：仅智能体应用支持，需在应用内开启开关并发布 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)；
  - RAG 检索（`rag_options`）：仅智能体应用支持，可指定知识库 ID（`pipeline_ids`）、文档 ID（`file_ids`）及元数据过滤条件；
  - 插件调用与自定义参数（`biz_params`）：支持通过 `user_prompt_params`、`user_defined_params` 等子字段传递提示词变量、插件参数及用户级鉴权信息。

> **注意**：`rag_options` 和 `memory_id` 在 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 中未被提及，仅在 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 中明确定义，开发者调用新版智能体时若需使用这些功能，应以后者文档为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属 API |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取 | 全部 |
| `prompt` | string | 是（DashScope） | 单轮文本输入指令 | DashScope API |
| `input` | string/array | 是（Responses） | 支持纯文本或 Messages 数组（含 system/user/assistant 角色）；多模态输入需为 content 数组 | Responses API |
| `session_id` | string | 否 | 对话历史标识，1 小时无请求自动失效；与 `messages` 冲突时优先使用 `messages` | DashScope API |
| `messages` | array | 否（DashScope） | 多轮对话上下文，替代 `prompt` + `session_id` | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming.md)（默认 `false`）；Responses API 中 `background=true` 时不可用 | 全部 |
| `workspace` | string | 否 | 子业务空间 ID，仅调用子空间应用或特定地域（如法兰克福、北京、新加坡等）模型时必需，通过 Header `X-DashScope-WorkSpace` 传递 | 全部 |
| `biz_params` | object | 否 | 传递自定义变量、插件参数及用户鉴权信息，结构复杂，详见文档 | DashScope & Responses API |

## 使用方式

- **DashScope 原生 API**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  推荐用于需要最大灵活性与性能的场景，支持完整参数集（如 `rag_options`, `memory_id`, `flow_stream_mode`）。SDK 调用需注意版本要求（如 Java SDK ≥ 2.22.23）[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。

- **OpenAI 兼容 Responses API**  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上 endpoint，请求体中设置 `"background": true`  
  适用于复用现有 OpenAI 生态代码的场景，简化迁移成本。注意：异步模式不支持 `stream=true`，且 `messages` 格式与 DashScope 的 `input.messages` 不完全等价。

- **调试与验证**  
  所有应用均支持控制台「发布 → API 调试」在线调试，无需编码即可验证参数组合与响应结构。

## 限制和注意事项

- **地域限制**：所有文档明确指出，当前 DashScope API 与 Responses API 均**仅支持华北2（北京）地域**，跨地域调用将失败。
- **凭证获取**：APP ID 和 Workspace ID **仅可通过控制台手动获取**，不支持 API 或 CLI 查询 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本强依赖**：多个参数（如 `incremental_output`, `flow_stream_mode`, `rag_options`）对 SDK 版本有最低要求（如 Python ≥ 1.24.7，Java ≥ 2.22.23），低版本将静默忽略或报错。
- **参数冲突规则**：当同时传入 `session_id` 和 `messages` 时，DashScope API 优先使用 `messages`；当 `background=true` 时，Responses API 忽略 `stream` 参数。
- **工作流流式模式弃用警告**：`flow_stream_mode=full_thoughts` 已被标记为“不推荐新业务使用”，应优先选用 `message_format` 或 `message_format_plus` [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


