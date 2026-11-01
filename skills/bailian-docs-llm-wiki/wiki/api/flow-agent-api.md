# flow agent api

Flow Agent API 是阿里云百炼平台提供的核心接口体系，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等底层组件。该 API 分为两类：面向终端应用调用的 DashScope 网关接口（使用 API Key 鉴权），以及面向开发者能力扩展的百炼 OpenAPI 组件接口（使用 AccessKey 签名鉴权）。两类接口在 Base URL、认证方式和错误响应格式上均不兼容，需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 本身不直接暴露模型选择能力，而是通过**预发布应用**间接支持模型能力：
- **新版智能体应用（Agent 2.0）**：支持深度思考模型（需启用 `enable_thinking` 参数），详见 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)；
- **旧版智能体与工作流应用**：基于配置的工作流节点自动调度模型，开发者无需指定具体模型 ID；
- **Prompt 模板与[长期记忆](../concepts/long-term-memory.md)（旧）**：作为独立组件能力，通过百炼 OpenAPI 提供完整 CRUD 接口，适用于需要动态注入系统指令或持久化用户上下文的高阶场景，相关文档见 [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md) 和 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)。

> **注意**：文档中多次提及“[长期记忆](../concepts/long-term-memory.md)（旧）”，表明该能力已被标记为历史版本；当前推荐方案应以控制台内置的记忆管理或新版 Agent 内置状态机制为准，OpenAPI 方式仅用于兼容性维护。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 所属接口类型 |
|------|------|------|------|--------------|
| `app_id` | string | 是 | 应用唯一标识，从控制台应用卡片复制获取 | 应用调用（DashScope/API） |
| `prompt` | string | 是（单轮） | 用户输入文本，用于单轮对话 | 应用调用（DashScope/API） |
| `messages` | array | 是（多轮） | 结构化消息数组（含 `system`/`user` 角色），替代 `prompt` 和 `session_id` | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md) |
| `session_id` | string | 否 | 对话会话标识，启用云端历史续写（1 小时失效） | 应用调用（DashScope/API） |
| `workspace` / `X-DashScope-WorkSpace` | string | 否（子空间必需） | 业务空间 ID，仅当应用部署于子业务空间或特定地域（如法兰克福、东京）时必须传入 | 应用调用（DashScope/API） |
| `stream` | boolean | 否（默认 `false`） | 是否启用[流式输出](../concepts/streaming-output.md)；设为 `true` 时需配合 `X-DashScope-SSE: enable` Header | 应用调用（DashScope/API） |
| `incremental_output` | boolean | 否（默认 `false`） | 仅在 `stream=true` 时生效，控制是否增量返回（`true`）或全量追加（`false`） | 应用调用（DashScope/API） |

## 使用方式

### 1. 应用调用（DashScope 网关）
- **Base URL**：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（同步）或 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（OpenAI 兼容模式）  
- **认证**：`Authorization: Bearer <your-api-key>`（API Key 鉴权）  
- **典型流程**：  
  - 获取 APP ID 和 Workspace ID（[获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）；  
  - 构造请求体（`input` 或 `messages` 字段）并设置 `stream`/`incremental_output`；  
  - 调用 `/completion`（DashScope 原生）或 `/responses`（OpenAI 兼容）端点。  
- **异步支持**：OpenAI 兼容模式提供 `background=true` 参数，返回任务 ID 后可轮询结果，避免长耗时超时（[异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。

### 2. 组件类接口（百炼 OpenAPI）
- **Base URL**：`https://bailian.{regionId}.aliyuncs.com`（如 `bailian.cn-beijing.aliyuncs.com`）  
- **认证**：AccessKey 签名（`ACS3-HMAC-SHA256`），**不支持** `Bearer` [Token](../concepts/token.md)  
- **典型操作**：  
  - Prompt 模板：`POST /{workspaceId}/promptTemplates` 创建，`GET /{workspaceId}/promptTemplates/{id}` 查询；  
  - 长期记忆体：`POST /{workspaceId}/memories` 创建记忆体，再通过 `POST /{workspaceId}/memories/{memoryId}/memoryNodes` 添加片段；  
  - 所有组件接口均需显式传入 `workspaceId` 路径参数。

## 限制和注意事项

- **地域限制**：所有 DashScope 应用调用接口（包括新版 Agent、旧版 Agent、Workflow、Responses API）**仅支持华北2（北京）地域**，其他地域调用将失败（见 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md) 和 [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)）；  
- **鉴权隔离**：应用调用接口与组件接口**不可混用凭证**——API Key 无法调用 Prompt 模板 API，AccessKey 也无法调用 `/completion` 接口；  
- **异步与流式互斥**：OpenAI 兼容模式的异步调用（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true`），此限制在 [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md) 中明确声明；  
- **长期记忆限流**：`GetMemory`、`ListMemories` 等长期记忆接口要求两次请求间隔 ≥1 秒，否则触发限流（见 [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)）；  
- **错误处理差异**：应用调用接口错误响应含 `request_id` 字段；组件接口遵循阿里云统一结构，错误字段为 `Code` 和 `Message`（见 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)）。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)


