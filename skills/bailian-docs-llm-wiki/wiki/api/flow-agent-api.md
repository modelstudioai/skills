# flow agent api

Flow Agent API 是阿里云百炼平台提供的核心接口体系，用于调用智能体（Agent）与工作流应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。API 分为两类：面向终端应用调用的 **应用调用接口**（通过 DashScope 应用网关），以及面向平台能力集成的 **组件类接口**（基于阿里云 OpenAPI）。两类接口在鉴权、Endpoint、错误格式上均存在差异，开发者需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 支持以下核心能力：

- **应用调用**：调用已发布的**新版智能体应用（Agent 2.0）**、**旧版智能体应用**及**工作流应用**，支持同步/异步、流式/非[流式输出](../concepts/streaming.md)；  
- **Prompt 工程组件**：提供完整的 Prompt 模板生命周期管理（创建、查询、更新、删除、列表），详见 [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)；  
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：支持记忆体（Memory）与记忆片段（MemoryNode）的增删改查，适用于需跨会话持久化用户上下文的场景；  
- **其他辅助能力**：包括支付宝打赏状态查询、临时文件上传许可申请等，详见 [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)。

> **注意**：文档中多次提及“[长期记忆](../concepts/long-term-memory.md)（旧）”，表明该能力已被标记为遗留方案，新项目应优先评估平台当前推荐的记忆方案（如新版智能体内置记忆机制），具体演进路径请参考最新版[智能体开发指南](raw/application-user-guide/agent-development/llm-application/new-single-agent-application.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 所属接口类型 |
|--------|------|------|------|--------------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取 | 应用调用（DashScope / Responses） |
| `workspace_id` | string | 条件必填 | 仅当应用位于**子业务空间**或部署在**德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）** 地域时必需；也是组件类接口 URL 路径中的必要路径参数 | 全局（应用调用 & 组件类） |
| `prompt` 或 `input` | string/array | 是 | 用户输入指令；`input` 可为字符串或符合 OpenAI 格式的 `messages` 数组（含 `system`/`user` 角色） | 应用调用（DashScope / Responses） |
| `session_id` | string | 否 | 用于恢复云端存储的对话历史；1 小时无请求后自动失效 | 应用调用（DashScope） |
| `stream` | boolean | 否 | 是否启用流式响应（默认 `false`）；启用时需设置 Header `X-DashScope-SSE: enable` | 应用调用（DashScope） |
| `incremental_output` | boolean | 否 | 仅在 `stream=true` 时生效，控制是否增量输出（推荐 `true`） | 应用调用（DashScope） |
| `background` | boolean | 否 | Responses API 异步调用标志（设为 `true` 返回任务 ID） | 应用调用（Responses） |

## 使用方式

### 1. 鉴权方式（关键区别）
- **应用调用接口**（如 `/apps/{APP_ID}/completion`）：使用 **百炼 API Key**，Header 中传 `Authorization: Bearer <your-api-key>`；  
- **组件类接口**（如 Prompt 模板、长期记忆）：使用 **AccessKey 签名（ACS3-HMAC-SHA256）**，不支持 `Bearer` 方式，必须通过阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 调用。

### 2. Endpoint 与 Base URL
- **应用调用**（DashScope）：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（同步）或 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（Responses 同步）；  
- **组件类接口**：Base URL 为 `https://bailian.{regionId}.aliyuncs.com`，路径含 `{workspaceId}`，例如 `POST /{workspaceId}/promptTemplates`；  
- **地域限制**：所有应用调用接口（DashScope / Responses）目前**仅支持华北2（北京）地域**，此限制在多份文档中反复强调，如 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md) 和 [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)。

### 3. 典型调用流程
- **获取凭证**：通过控制台手动获取 `APP_ID` 和（如需）`WORKSPACE_ID`，API Key 或 AccessKey；  
- **选择协议**：实时交互选 DashScope 同步/流式，长耗时任务选 Responses 异步（`background=true`）；  
- **构造请求**：按接口类型设置对应鉴权 Header、URL 路径及请求体（注意 `prompt`/`input`/`messages` 的嵌套层级差异）；  
- **处理响应**：应用调用返回标准 JSON；组件类接口遵循阿里云 OpenAPI 统一结构（含 `Code`/`Message` 字段）。

## 限制和注意事项

- **地域硬限制**：应用调用类接口（DashScope / Responses）**仅限华北2（北京）地域**，尝试在其他地域调用将失败；组件类接口虽支持多地域，但 `workspaceId` 必须与目标地域匹配；  
- **凭证获取方式**：`APP_ID` 和 `WORKSPACE_ID` **仅支持控制台手动复制**，不提供 API 或 CLI 查询能力，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)；  
- **错误处理差异**：应用调用接口返回 `request_id` 便于问题追踪；组件类接口返回 `Code`/`Message` 字段，且 HTTP 状态码语义需结合文档理解（如 404 表示资源不存在，见 [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)）；  
- **异步限制**：Responses API 的异步调用 **不支持[流式输出](../concepts/streaming.md)（`stream=true` 无效）**；  
- **长期记忆限流**：所有长期记忆相关接口（如 `CreateMemory`）要求两次请求间隔 ≥1 秒，否则可能触发限流；  
- **幂等性说明**：`GetMemory`、`UpdateMemory`、`DeleteMemory`、`ListMemories` 等接口明确声明具有幂等性，而 `CreateMemory` 不具备幂等性，重复调用将创建多个资源。

## 来源文档

- [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)


