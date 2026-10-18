# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体与工作流应用，并管理 Prompt 模板、长期记忆等底层组件。该 API 分为两类：**应用调用接口**（通过 DashScope 应用网关）和**组件类接口**（通过百炼 OpenAPI），二者在鉴权方式、Endpoint 和功能定位上存在根本差异。开发者需根据使用场景严格区分调用路径与凭证类型。

## 支持的模型/功能

Flow Agent API 支持调用三类核心能力：

- **新版智能体应用（Agent 2.0）**：通过 DashScope API 调用，支持 `stream` [流式输出](../concepts/streaming-output.md)与 `incremental_output` 增量流式响应，适用于实时交互场景。其 API 文档明确标注“仅适用于华北2（北京）地域”[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)。
- **旧版智能体与工作流应用**：同样通过 DashScope API 调用，但支持更丰富的上下文参数（如 `messages` 数组），可用于多轮对话或结构化输入。该接口也限定于华北2（北京）地域[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)。
- **组件类能力**：包括 Prompt 模板管理（创建、更新、查询等）、长期记忆（旧）管理（含记忆体与记忆片段的全生命周期操作），以及支付宝打赏、临时文件上传等辅助功能。这些均属于百炼 OpenAPI，需使用 AccessKey 签名认证。

> **注意**：文档中多次提及“长期记忆（旧）”，表明该能力已被标记为历史方案；当前推荐方案未在原始文档中体现，开发者应关注控制台或后续文档中关于“长期记忆（新）”的演进说明。

## 关键参数

### 应用调用接口（DashScope API）
- `app_id`（URL 路径参数）：必填，应用唯一标识，从控制台应用卡片复制。
- `prompt` 或 `messages`（请求体）：二选一。`prompt` 用于单轮指令；`messages` 为数组，支持 system/user 多角色消息，启用时自动忽略 `prompt` 和 `session_id`。
- `session_id`（可选）：用于恢复云端存储的对话历史，1 小时无请求后失效。
- `workspace`（Header 中 `X-DashScope-WorkSpace`）：仅当调用子业务空间下的应用时必需。
- `stream`（布尔，默认 `false`）：是否启用流式响应；设为 `true` 时需在 Header 中添加 `X-DashScope-SSE: enable`。
- `incremental_output`（布尔，默认 `false`）：仅在 `stream=true` 时生效，控制[流式输出](../concepts/streaming-output.md)是否为增量模式（推荐设为 `true`）。

### 组件类接口（百炼 OpenAPI）
- `workspaceId`（路径参数）：所有组件接口（如 Prompt 模板、长期记忆）均需显式传入，对应业务空间 ID。
- `promptTemplateId` / `memoryId` / `memoryNodeId`（路径参数）：各资源的唯一标识，由创建接口返回。
- `content`, `name`, `description`（请求体）：分别为 Prompt 模板内容、名称，或记忆片段/记忆体的描述信息，均有长度与字符集限制（如 `content` 长度上限 200 字符）。

## 使用方式

### 认证方式
- **应用调用接口**：使用百炼 API Key，通过 `Authorization: Bearer <your-api-key>` Header 传递。API Key 在[控制台密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)获取[认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)。
- **组件类接口**：使用阿里云 AccessKey（AK/SK），采用 `ACS3-HMAC-SHA256` 签名机制，**不支持** `Bearer` 方式。强烈推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动处理签名。

### Endpoint 与调用路径
- **应用调用**：Base URL 为 `https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（同步）或 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（OpenAI 兼容模式）。
- **组件类接口**：Base URL 为 `https://bailian.{regionId}.aliyuncs.com`，具体路径包含 `/{workspaceId}/promptTemplates` 或 `/{workspaceId}/memories` 等。

### 开发建议
- 对于耗时较长的任务（如复杂报告生成），优先选用 Responses API 的异步模式（`background=true`），避免 HTTP 请求超时[异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- 使用 SDK 可大幅降低集成复杂度：DashScope SDK 已预置正确 endpoint；OpenAPI SDK 可自动完成签名。

## 限制和注意事项

- **地域限制**：所有 DashScope API（新版智能体、旧版智能体、工作流、Responses API）均**仅支持华北2（北京）地域**，其他地域调用将失败。
- **凭证获取方式**：APP ID 和 Workspace ID **仅能通过控制台手动获取**，不支持 API 或 CLI 查询[获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。
- **长期记忆（旧）限流**：CreateMemory、UpdateMemory 等接口要求两次请求间隔 ≥1 秒，否则可能触发限流。
- **错误处理**：两类接口错误码体系不同——应用调用接口返回自定义 `code`/`message` 并附带 `request_id`；组件类接口遵循阿里云 OpenAPI 标准，返回 `Code`/`Message` 字段[错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。
- **流式与异步互斥**：Responses API 的[异步调用](../concepts/asynchronous-invocation.md)（`background=true`）**不支持 `stream=true`**，二者不可同时启用。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)


