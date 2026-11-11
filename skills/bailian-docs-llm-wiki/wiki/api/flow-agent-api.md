# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体与工作流应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。API 分为两类：**应用调用接口**（通过 DashScope 应用网关）和**组件类接口**（通过阿里云 OpenAPI），二者在鉴权方式、Endpoint 和功能边界上存在明确划分。开发者需根据使用场景选择对应路径并严格遵循其认证与参数规范。

## 支持的模型/功能

Flow Agent API 本身不直接暴露底层大模型选型，而是通过预配置的智能体（Agent）或工作流（Workflow）应用间接调用模型能力。当前支持的应用类型包括：

- **新版智能体应用（Agent 2.0）**：支持深度思考（`enable_thinking`）、[流式输出](../concepts/streaming-output.md)（`stream`）与增量输出（`incremental_output`）等高级能力，详见[新版智能体应用 API 参考](raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)；
- **旧版智能体与工作流应用**：适用于华北2（北京）地域，支持 `session_id` 对话状态管理和 `messages` 多轮上下文输入，但不支持 `enable_thinking` 参数；
- **Prompt 模板管理**：提供完整的 CRUD 接口（如 [CreatePromptTemplate](raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)、[ListPromptTemplates](raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)），支持变量插值（如 `${theme}`）；
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：提供 `Memory`（[长期记忆](../concepts/long-term-memory.md)体）与 `MemoryNode`（记忆片段）两级结构的增删改查能力，用于持久化用户偏好或对话关键信息，详见[长期记忆（旧）](raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)；
- **其他辅助能力**：包括支付宝打赏状态查询、临时文件上传许可申请等，详见[其他](raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)。

> **注意**：文档中多次提及“长期记忆（旧）”，表明该能力已被标记为遗留方案；新项目应优先评估平台是否已推出替代的长期记忆 V2 或统一记忆服务，避免技术债累积。

## 关键参数

### 应用调用类（DashScope / Responses API）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取。HTTP 调用时需填入 URL 路径，SDK 中为 `appId`。 |
| `prompt` | string | 是（当未传 `messages` 时） | 单轮用户指令文本。若同时传 `messages`，则 `prompt` 被忽略。 |
| `messages` | array | 否（替代 `prompt`） | 多轮对话消息数组，含 `system` 和 `user` 角色对象；使用时必须完整传递历史，暂不支持基于 `conversation_id` 的上下文自动补全。 |
| `session_id` | string | 否 | 云端维护的会话 ID，启用后自动加载历史对话；1 小时无请求即失效；与 `messages` 冲突时以 `messages` 为准。 |
| `workspace` | string | 否（仅子业务空间） | 业务空间 ID，仅在调用子业务空间下的应用时需通过 Header `X-DashScope-WorkSpace` 传递。 |
| `stream` | boolean | 否（默认 `false`） | 是否启用流式响应。推荐设为 `true`，需配合 `X-DashScope-SSE: enable` Header 使用。 |
| `incremental_output` | boolean | 否（默认 `false`） | 仅在 `stream=true` 时生效，控制输出为全量累计（`false`）或增量分片（`true`）。 |

### 组件类（OpenAPI）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspaceId` | string | 是 | 业务空间 ID，所有组件类接口（Prompt、Memory 等）均需在路径中显式指定。 |
| `name` / `content`（Prompt） | string | 是（创建时） | Prompt 模板名称与模板内容，`content` 支持 `${variable}` 插值语法。 |
| `memoryId` / `memoryNodeId` | string | 是（操作时） | 长期记忆体与记忆片段的唯一 ID，由 `CreateMemory` 或 `CreateMemoryNode` 返回，后续操作必需。 |

## 使用方式

### 1. 认证方式
- **应用调用接口**（DashScope / Responses）：使用百炼 API Key，Header 中携带 `Authorization: Bearer <your-api-key>`；
- **组件类接口**（Prompt、Memory 等）：使用阿里云 AccessKey 进行 `ACS3-HMAC-SHA256` 签名，**不支持** `Bearer` 方式；推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成代码。

### 2. Endpoint 与调用路径
- **应用调用**：
  - DashScope API：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - Responses API（OpenAI 兼容）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **组件类**：
  - Prompt 模板：`POST /{workspaceId}/promptTemplates`（[CreatePromptTemplate](raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)）
  - 长期记忆：`POST /{workspaceId}/memories`（[CreateMemory](raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)）

### 3. 地域与 Workspace 限制
- 所有应用调用接口（DashScope / Responses）**仅支持华北2（北京）地域**；
- `Workspace ID` 在以下场景为必需：
  - 调用子业务空间下的应用；
  - 调用德国（法兰克福）、新加坡、中国香港、日本（东京）等非北京地域的模型（此时 `Workspace ID` 构成 Base URL 的一部分）；
  - 所有组件类接口（Prompt、Memory 等）均强制要求 `workspaceId` 路径参数。

## 限制和注意事项

- **地域强约束**：文档 7、8、10、11 均明确标注“本文档仅适用于华北2（北京）地域”，跨地域调用将失败，且错误码不提示地域问题，仅返回 404 或 403。
- **Session 时效性**：`session_id` 在连续 1 小时无请求后自动失效，不可续期；若需长期会话，建议自行维护 `messages` 并每次完整提交。
- **流式与异步互斥**：Responses API 的异步调用（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true`），二者不可同时启用。
- **权限最小化原则**：组件类接口需精确授权 RAM 权限（如 `sfm:CreatePromptTemplate`），而非泛化的 `AliyunBailianFullAccess`；主账号或超级管理员才可访问全部业务空间列表。
- **幂等性差异**：`CreateMemory` 不具备幂等性，重复调用将创建多个记忆体；而 `GetMemory`、`ListMemories`、`UpdateMemory` 等均为幂等操作。
- **错误处理统一性**：应用调用接口返回 `request_id` 便于排查；组件类接口遵循阿里云 OpenAPI 标准，错误信息在 `Code`/`Message` 字段中，详见[错误码](raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)


