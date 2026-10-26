# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等底层组件。该 API 分为两类：面向终端应用调用的 **DashScope 应用网关接口**（使用 API Key 鉴权），以及面向开发者能力扩展的 **百炼 OpenAPI 组件接口**（使用 AccessKey 签名鉴权）。二者在 Base URL、认证方式、错误响应结构上均不兼容，需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 本身不直接暴露模型选型参数，而是通过预置的智能体或工作流应用间接调用底层模型。其核心功能覆盖三类：

- **应用调用**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用的同步/异步调用，提供 `stream` 和 `incremental_output` 等增强交互体验的参数；  
- **Prompt 工程支持**：提供完整的 Prompt 模板生命周期管理（创建、读取、更新、删除、列表），支持变量插值（如 `${theme}`），详见 [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)；  
- **[长期记忆](../concepts/long-term-memory.md)管理**：提供 `Memory`（[长期记忆](../concepts/long-term-memory.md)体）与 `MemoryNode`（记忆片段）两级抽象，支持增删改查及分页列表，适用于需跨会话持久化用户上下文的场景，文档见 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)。

> **注意**：文档中多次提及“长期记忆（旧）”，但未提供“新”长期记忆的说明或替代方案。当前所有 Memory 相关接口（如 [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)）均属此体系，开发者应以该系列接口为准，暂无迁移路径提示。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 所属接口类型 |
|------|------|------|------|--------------|
| `app_id` | string | 是 | 应用唯一标识，从控制台获取。HTTP 调用时需置于 URL 路径中；SDK 调用时作为字段传入。 | 应用调用（DashScope / Responses） |
| `prompt` | string | 是（当未传 `messages` 时） | 用户单轮指令文本。若使用 `messages`，则此项被忽略。 | 应用调用（DashScope） |
| `messages` | array | 是（当替代 `prompt` 时） | 多轮对话消息数组，含 `system`/`user` 角色对象，支持多模态输入（文本+图片）。 | 应用调用（DashScope / Responses） |
| `session_id` | string | 否 | 对话历史标识，启用后自动加载云端存储的上下文（1 小时失效）。与 `messages` 冲突时优先使用 `messages`。 | 应用调用（DashScope） |
| `stream` | boolean | 否（默认 `false`） | 是否启用[流式输出](../concepts/streaming-output.md)。设为 `true` 可降低超时风险，需配合 `X-DashScope-SSE: enable` Header（HTTP）或 `streamCall` 方法（Java SDK）。 | 应用调用（DashScope） |
| `incremental_output` | boolean | 否（默认 `false`） | 仅在 `stream=true` 时生效，控制是否增量返回（`true`）或全量追加返回（`false`）。 | 应用调用（DashScope） |
| `workspaceId` | string | 是（组件类接口必填；应用调用中仅子业务空间/特定地域需显式传） | 业务空间唯一 ID，用于路由请求和权限隔离。获取方式见 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。 | 所有组件类接口（Prompt / Memory / Others） |

## 使用方式

### 1. 认证方式严格分离
- **应用调用接口**（如 `/apps/{app_id}/completion`）：使用 **阿里云百炼 API Key**，通过 `Authorization: Bearer <your-api-key>` 传递；  
- **组件类接口**（如 `/promptTemplates`、`/memories`）：属于阿里云 OpenAPI，必须使用 **AccessKey 签名（ACS3-HMAC-SHA256）**，不支持 `Bearer` 方式。推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成调用代码。

### 2. 接口调用路径
- **应用调用**：统一 Base URL 为 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`（DashScope）或 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/responses`（Responses API）；  
- **组件类接口**：Base URL 为 `https://bailian.{regionId}.aliyuncs.com`，且所有请求路径均需包含 `{workspaceId}` 路径参数（如 `/llm-czal8nvvwb8d4xxx/promptTemplates`）。

### 3. 典型流程示例
- 调用智能体前：在控制台获取 `APP_ID` 和（如需）`Workspace ID` → 配置 API Key → 构造 `POST /api/v1/apps/{APP_ID}/completion` 请求；  
- 管理 Prompt 模板：使用 AccessKey 签名 → 调用 `POST /{workspaceId}/promptTemplates` 创建模板 → 在智能体配置中引用该模板 ID；  
- 启用长期记忆：先调用 `POST /{workspaceId}/memories` 创建 `memoryId` → 在智能体 API 请求中传入 `memoryId` 字段（文档未明确该字段名，但 [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md) 明确指出需“传入该 memoryId”）。

## 限制和注意事项

- **地域限制**：所有 DashScope 应用调用接口（包括新版智能体、工作流、Responses API）当前**仅支持华北2（北京）地域**，其他地域调用将失败；  
- **异步限制**：Responses API 的异步调用（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)（`stream=true`）**，二者互斥；  
- **凭证获取方式**：`APP ID` 和 `Workspace ID` **仅能通过百炼控制台手动复制**，不提供 API 或 CLI 查询能力；  
- **长期记忆限流**：Memory 及 MemoryNode 相关接口有明确限流要求——“两次请求间隔至少 1 秒”，否则可能触发系统限流，需在客户端实现退避重试；  
- **错误处理差异**：应用调用接口返回自定义错误码与 `request_id`；组件类接口遵循阿里云 OpenAPI 统一格式（`Code`/`Message` 字段），详见 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)；  
- **功能演进提示**：`enable_thinking` 参数在文档 7 中被截断，未说明其完整行为与支持模型范围，实际使用前需验证兼容性。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)


