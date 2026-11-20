# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等底层组件。该 API 分为两类：面向终端应用调用的 **应用调用接口**（通过 DashScope 应用网关），以及面向开发者能力集成的 **组件类接口**（通过百炼 OpenAPI）。二者在鉴权方式、Base URL 和错误响应格式上均存在差异，需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 支持以下核心能力：

- **应用调用**：同步/[异步调用](../concepts/asynchronous-invocation.md)新版智能体（Agent 2.0）、旧版智能体及工作流应用，支持多轮对话（`messages`）、会话上下文（`session_id`）、[流式输出](../concepts/streaming-output.md)（`stream=true`）和增量流式（`incremental_output=true`）[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)。
- **Prompt 工程**：全生命周期管理 Prompt 模板，包括创建、获取、更新、删除及列表查询，支持变量占位符（如 `${theme}`）和类型区分（`System`/`Custom`）[CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)。
- **[长期记忆](../concepts/long-term-memory.md)（Memory）**：提供 `Memory`（[长期记忆](../concepts/long-term-memory.md)体）与 `MemoryNode`（记忆片段）两级抽象，支持 CRUD 及分页查询；注意文档中明确说明“长期记忆体尚不支持存储与管理用户画像”，相关操作需通过控制台完成 [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)。
- **其他扩展能力**：包括支付宝打赏状态查询、临时文件上传许可申请等，主要面向高代码或特定业务场景。

> **注意**：文档 1 中提及“长期记忆（旧）”属于历史遗留描述，而文档 31 的目录结构与文档 19–26 的实际接口命名（如 `CreateMemory`）完全一致，表明当前所有长期记忆接口均为现行有效版本。“旧”字仅为路径标识，不代表功能过时或即将下线。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 所属接口类型 |
|--------|------|------|------|--------------|
| `app_id` | string | 是 | 应用唯一标识，从控制台应用卡片复制获取 | 应用调用（DashScope / Responses） |
| `workspaceId` | string | 条件必填 | 子业务空间 ID；调用子空间应用或德国/北京/新加坡/香港/东京地域模型时必需 | 所有组件类接口（Prompt/Memory）及部分应用调用场景 |
| `prompt` | string | 是（部分场景） | 用户指令文本；当使用 `messages` 时可省略 | DashScope 应用调用 |
| `messages` | array | 可选（替代 prompt） | 多轮消息数组，含 `system`/`user` 角色，支持多模态内容结构 | DashScope 应用调用 |
| `session_id` | string | 否 | 对话历史标识，启用后自动加载云端会话上下文（1 小时有效期） | DashScope 应用调用 |
| `stream` | boolean | 否（默认 false） | 是否启用流式响应；设为 `true` 时需配合 `X-DashScope-SSE: enable` Header | DashScope 应用调用 |
| `incremental_output` | boolean | 否（默认 false） | 仅在 `stream=true` 时生效，控制是否返回增量内容（`true`）或全量累积内容（`false`） | DashScope 应用调用 |
| `background` | boolean | 否（默认 false） | Responses API 异步模式开关；设为 `true` 则立即返回任务 ID | Responses API（异步） |

## 使用方式

### 1. 鉴权方式（必须区分）
- **应用调用接口**（DashScope / Responses）：使用 **百炼 API Key**，Header 中传 `Authorization: Bearer <your-api-key>`。
- **组件类接口**（Prompt / Memory / Others）：使用 **阿里云 AccessKey** 签名（`ACS3-HMAC-SHA256`），不支持 `Bearer` 方式；推荐直接使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 免签名调试。

### 2. Base URL 与 Endpoint
- **应用调用**：
  - DashScope API：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - Responses API（同步）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **组件类接口**：统一为百炼 OpenAPI 域名 `https://bailian.{region}.aliyuncs.com`，路径含 `{workspaceId}`，例如 Prompt 创建：`POST /{workspaceId}/promptTemplates`

### 3. 地域限制
- 所有应用调用类文档（文档 8、9、32、16）均明确标注 **“仅适用于华北2（北京）地域”**；若需在其他地域（如德国法兰克福）调用，必须使用对应地域的 `workspaceId` 构造 Base URL（见文档 4），且仅限子业务空间场景。

## 限制和注意事项

- **凭证获取方式受限**：APP ID 和 Workspace ID **仅支持控制台手动复制**，不提供 API 或 CLI 查询能力 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。
- **[异步调用](../concepts/asynchronous-invocation.md)约束**：Responses API 的异步模式（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true` 会被忽略），且需自行实现轮询逻辑获取最终结果。
- **长期记忆限流**：所有 Memory 相关接口（`CreateMemory`/`ListMemories` 等）均有 **1 秒最小请求间隔** 要求，否则触发限流；建议在客户端添加退避重试。
- **错误处理差异**：
  - 应用调用接口：错误响应含 `request_id`，错误码与信息字段名依具体接口而定；
  - 组件类接口：严格遵循阿里云 OpenAPI 标准，错误时返回 `Code` 与 `Message` 字段。
- **Prompt 模板限制**：`CreatePromptTemplate` 接口 **暂不支持文生图 Prompt 模板创建**，仅适用于文本生成类模板。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)


