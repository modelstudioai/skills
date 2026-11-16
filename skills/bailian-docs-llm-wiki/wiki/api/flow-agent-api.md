# flow agent api

Flow Agent API 是阿里云百炼平台提供的核心接口体系，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。该 API 分为两类：**应用调用接口**（通过 DashScope 应用网关）和**组件类接口**（通过百炼 OpenAPI），二者在鉴权方式、Endpoint 和功能边界上存在明确区分。

## 支持的模型/功能

Flow Agent API 本身不直接暴露底层大模型，而是面向已部署的**应用实例**提供调用能力。支持的应用类型包括：
- **新版智能体应用（Agent 2.0）**：基于 DashScope API 调用，支持 `stream`、`incremental_output`、`enable_thinking` 等高级参数 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)；
- **工作流应用与旧版智能体应用**：同样通过 DashScope API，但参数结构略有差异，例如支持 `messages` 数组实现多轮对话 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)；
- **OpenAI 兼容模式（Responses API）**：提供同步与异步两种调用方式，便于复用现有 OpenAI 生态代码 [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)。

此外，组件类接口支持：
- **Prompt 模板管理**：创建、更新、查询、删除模板，支持变量插值（如 `${theme}`）[CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)；
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：以 Memory 为单位组织记忆片段（MemoryNode），支持 CRUD 操作，适用于需跨会话持久化用户上下文的场景；
- **其他辅助能力**：如支付宝打赏状态查询、临时文件上传许可申请等（详见 [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)）。

> **注意**：文档中多次提及“[长期记忆](../concepts/long-term-memory.md)（旧）”，表明该能力已被标记为遗留方案；当前推荐使用新版智能体内置的记忆机制或工作流节点状态管理，避免依赖此组件类接口。

## 关键参数

### 应用调用类（DashScope / Responses API）
- `app_id`（必选）：应用唯一标识，从控制台应用卡片复制；
- `prompt`（必选，DashScope）或 `input`（必选，Responses）：用户输入文本或消息数组；
- `session_id`（可选）：用于恢复云端存储的对话历史，1 小时无请求后自动失效；
- `messages`（可选，DashScope）：替代 `prompt` + `session_id` 的多轮对话格式，需 SDK ≥ Python 2.0.1 / Java 2.17.0；
- `stream`（可选，默认 `false`）：启用[流式输出](../concepts/streaming-output.md)，需配合 `X-DashScope-SSE: enable` Header；
- `incremental_output`（可选，默认 `false`）：仅在 `stream=true` 时生效，控制是否增量返回 token；
- `workspace`（可选，DashScope）或 `X-DashScope-WorkSpace` Header：子业务空间 ID，仅在非默认空间调用时必需。

### 组件类（Prompt / Memory）
- `workspaceId`（必选）：所有组件接口均需显式传入，作为路径参数；
- `promptTemplateId` / `memoryId` / `memoryNodeId`（必选）：资源唯一标识，由对应创建接口返回；
- `content`（必选）：Prompt 模板内容或记忆片段正文，长度与字符集受严格限制（如 MemoryNode 内容限 1–200 字符）。

## 使用方式

### 认证方式
- **应用调用接口**（DashScope / Responses）：使用百炼 API Key，Header 中传递 `Authorization: Bearer <your-api-key>`；
- **组件类接口**（Prompt / Memory）：使用阿里云 AccessKey 签名（`ACS3-HMAC-SHA256`），**不支持** `Bearer` 方式，必须通过 SDK 或 OpenAPI Explorer 调用 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)。

### Endpoint 与调用路径
- **应用调用**：
  - DashScope：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - Responses（同步）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **组件类**：
  - Prompt：`POST /{workspaceId}/promptTemplates`（需替换为实际 `workspaceId`）
  - Memory：`POST /{workspaceId}/memories`（同上）

### 开发建议
- 优先使用官方 SDK（DashScope SDK / OpenAI Python SDK），避免手动签名；
- 对于耗时任务（如报告生成），务必选用 Responses API 的异步模式，避免 HTTP 超时；
- `session_id` 与 `messages` 不可混用：若同时传入，系统将忽略 `session_id` 和 `prompt`，仅使用 `messages`。

## 限制和注意事项

- **地域限制**：所有应用调用类文档（DashScope / Responses）均明确标注“仅适用于华北2（北京）地域”，跨地域调用将失败；
- **凭证获取**：APP ID 和 Workspace ID **仅支持控制台手动获取**，不提供 API 或 CLI 查询方式 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)；
- **长期记忆限流**：CreateMemory 等接口要求两次请求间隔 ≥ 1 秒，否则触发限流；
- **异步限制**：Responses API 异步调用不支持 `stream=true`；
- **错误处理**：应用调用接口返回 `request_id` 便于问题定位；组件类接口遵循阿里云 OpenAPI 统一结构（`Code`/`Message` 字段）[Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)；
- **权限要求**：操作业务空间（如 `ListMemories`）需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号，普通子账号无法访问“业务空间管理”页面。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)


