# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等底层组件。该 API 分为两类：面向应用调用的 DashScope 网关接口（使用 API Key 鉴权），以及面向组件管理的百炼 OpenAPI（使用 AccessKey 签名鉴权），二者在 Base URL、认证方式和错误响应格式上均不兼容。

## 支持的模型/功能

Flow Agent API 本身不直接绑定特定大模型，而是通过调用已配置好模型的**智能体应用**或**工作流应用**间接使用模型能力。当前支持的应用类型包括：

- **新版智能体应用（Agent 2.0）**：适用于华北2（北京）地域，提供 `stream` 和 `incremental_output` 等高级流式控制能力 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)；
- **旧版智能体应用与工作流应用**：同样限于华北2（北京）地域，支持 `messages` 数组传入多轮对话上下文 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)；
- **Prompt 模板管理**：提供完整的 CRUD 接口（`CreatePromptTemplate`、`GetPromptTemplate` 等），支持变量插值（如 `${theme}`），但暂不支持文生图类 Prompt 模板 [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)；
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：提供 `Memory`（记忆体）与 `MemoryNode`（记忆片段）两级结构的增删改查，用于持久化存储用户相关信息，但文档明确说明“[长期记忆](../concepts/long-term-memory.md)体尚不支持存储与管理用户画像” [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)。

> **注意**：文档中多次强调“本文档仅适用于华北2（北京）地域”，但[获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)指出 Workspace ID 在德国（法兰克福）、新加坡、中国香港、日本（东京）等地域也是必需的，且是 Base URL 的组成部分。这表明组件类接口（如 Prompt 模板、长期记忆）实际支持多地域，而应用调用接口目前仅在北京地域可用。

## 关键参数

### 应用调用类（DashScope API）
- `app_id`（URL 路径参数）：必填，应用唯一标识，通过控制台获取；
- `prompt`（请求体 `input.prompt`）：必填，用户单轮指令文本；
- `session_id`（可选）：用于恢复云端对话历史，1 小时无请求后自动失效；
- `messages`（可选）：替代 `prompt` 和 `session_id` 的多轮对话数组，需按顺序包含 `system` 和 `user` 消息；
- `stream`（布尔，默认 `false`）：启用[流式输出](../concepts/streaming-output.md)，推荐设为 `true`；
- `incremental_output`（布尔，默认 `false`）：仅在 `stream=true` 时生效，控制是否增量返回（即每次只返回新生成内容）；
- `workspace`（Header `X-DashScope-WorkSpace`）：仅调用子业务空间应用时需传入 Workspace ID。

### 组件管理类（OpenAPI）
- `workspaceId`（路径参数）：所有组件接口（Prompt、Memory 等）均需显式传入，是业务空间唯一标识；
- `promptTemplateId` / `memoryId` / `memoryNodeId`（路径参数）：各资源的操作目标 ID；
- `content` / `name` / `description`（请求体）：核心业务字段，均有明确长度与字符集限制（如 `content` ≤200 字符，仅支持中英文、数字及部分符号）。

## 使用方式

### 认证方式分离
- **应用调用接口**（如 `/apps/{APP_ID}/completion`）：使用阿里云百炼 API Key，通过 `Authorization: Bearer <your-api-key>` 传递 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)；
- **组件类接口**（如 `/promptTemplates`、`/memories`）：使用阿里云 AccessKey 进行 `ACS3-HMAC-SHA256` 签名，**不支持** `Bearer` 方式，必须使用 SDK 或 OpenAPI Explorer [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)。

### 调用入口选择
- **同步实时交互**：优先使用 DashScope API（`/api/v1/apps/.../completion`）或 Responses API 同步模式（`/responses`），适用于聊天、问答等低延迟场景；
- **异步长耗时任务**：使用 Responses API 异步模式（`background=true`），立即返回 `task_id`，再通过 `retrieve` 轮询结果，**注意异步任务不支持[流式输出](../concepts/streaming-output.md)** [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)；
- **组件管理**：统一调用百炼 OpenAPI（`bailian.{region}.aliyuncs.com`），Endpoint 格式为 `/{workspaceId}/<resource>`，例如 `POST /{workspaceId}/promptTemplates`。

## 限制和注意事项

- **地域限制**：所有应用调用接口（DashScope API、Responses API）当前仅支持华北2（北京）地域；组件类接口（Prompt、Memory）虽未明示地域限制，但 `workspaceId` 在多地域控制台中均存在，实际支持范围更广；
- **凭证获取方式**：APP ID 和 Workspace ID **仅能通过控制台手动复制**，不支持 API 或 CLI 查询 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)；
- **会话与记忆生命周期**：
  - `session_id` 有效期为 1 小时（无请求即失效）；
  - `Memory` 与 `MemoryNode` 为永久存储，删除操作不可逆；
- **流式与异步互斥**：Responses API 的异步调用模式明确不支持 `stream=true`，若需流式响应，必须使用同步接口；
- **权限要求**：操作子业务空间下的资源（如非默认 Workspace 的 Prompt 或 Memory），调用者需具备对应 `workspaceId` 的 `AliyunBailianFullAccess` 或 `AliyunBailianControlFullAccess` 权限，RAM 子账号需由超级管理员授权 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)


