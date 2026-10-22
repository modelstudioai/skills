# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体与工作流应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。该 API 分为两类：面向应用调用的 DashScope 网关接口（Bearer Token 鉴权），以及面向组件管理的阿里云 OpenAPI（AccessKey 签名鉴权），二者在 Base URL、认证方式和错误响应格式上均不兼容。

## 支持的模型/功能

Flow Agent API 支持以下三类核心能力：

- **应用调用**：调用新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，覆盖同步、流式、增量输出与[异步任务](../concepts/asynchronous-task.md)模式。其中，[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)明确仅支持华北2（北京）地域；而[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)同样限定于该地域，但提供了 `messages` 数组参数以支持多轮对话上下文传递。
  
- **Prompt 模板管理**：通过 OpenAPI 提供完整的 CRUD 能力（创建、获取、更新、删除、列表），支持变量插值（如 `${theme}`）与模板类型区分（`System`/`Custom`）。所有操作均需指定 `workspaceId`，且当前不支持文生图类 Prompt 模板 [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)。

- **[长期记忆](../concepts/long-term-memory.md)（旧）**：提供记忆体（Memory）与记忆片段（MemoryNode）两级抽象，支持结构化存储用户状态信息。注意：文档明确标注该能力为“旧”，且[长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)说明中指出其不支持用户画像管理，需通过控制台操作。

> **注意**：文档 7 和文档 8 均声明“仅适用于华北2（北京）地域”，但文档 5 中 Workspace ID 的使用说明提到“德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）地域下的模型时，API 请求中才必须包含 Workspace ID”。这表明应用调用接口的地域支持范围实际更广，但 DashScope API 文档未完整覆盖——开发者应以控制台实际可用地域为准，避免仅依赖 API 文档中的地域限制描述。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 所属接口类型 |
|------|------|------|------|--------------|
| `app_id` | string | 是 | 应用唯一标识，从控制台「应用管理」获取 | 应用调用（DashScope / Responses） |
| `prompt` 或 `input` | string/array | 是 | 单轮文本输入或消息数组（含 `system`/`user` 角色） | DashScope / Responses |
| `session_id` | string | 否 | 对话历史标识，1 小时无请求自动失效；与 `messages` 冲突时后者优先 | DashScope |
| `messages` | array | 否 | 多轮对话上下文，需 SDK ≥ Python 1.20.14 / Java 2.17.0 | DashScope（工作流/旧版） |
| `stream` | boolean | 否（默认 `false`） | 是否启用[流式输出](../concepts/streaming-output.md)；设为 `true` 时需处理 SSE 响应 | DashScope |
| `incremental_output` | boolean | 否（默认 `false`） | 仅在 `stream=true` 时生效，控制是否增量返回（推荐 `true`） | DashScope（新版） |
| `background` | boolean | 否（默认 `false`） | Responses API 异步模式开关；设为 `true` 返回任务 ID | Responses（异步） |
| `workspaceId` | string | 是（OpenAPI）<br/>条件必填（DashScope） | 业务空间 ID；OpenAPI 所有请求必需；DashScope 仅子业务空间或特定地域下必需 | 组件类（OpenAPI）<br/>应用调用（条件） |

## 使用方式

### 1. 认证方式严格分离
- **应用调用接口**（如 `/apps/{APP_ID}/completion`）：使用阿里云百炼 API Key，通过 `Authorization: Bearer <your-api-key>` 传入。
- **组件类接口**（如 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)）：使用阿里云 AccessKey 进行 `ACS3-HMAC-SHA256` 签名，**不支持** `Bearer` 方式；强烈推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成签名代码。

### 2. 典型调用路径
- **获取凭证**：先通过控制台手动获取 `APP ID` 和（如需）`Workspace ID` —— 文档明确说明“目前只能通过控制台手动获取，不支持通过 API 或 CLI 查询” [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。
- **同步调用（推荐实时场景）**：
  - DashScope：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - Responses（OpenAI 兼容）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **异步调用（推荐长耗时任务）**：Responses API 设置 `background=true`，后续通过 `retrieve(task_id)` 轮询结果；注意[异步任务](../concepts/asynchronous-task.md)**不支持[流式输出](../concepts/streaming-output.md)**。
- **组件管理**：调用 OpenAPI，Base URL 为 `https://bailian.{regionId}.aliyuncs.com`，路径含 `{workspaceId}`，例如 `GET /{workspaceId}/promptTemplates`。

### 3. 错误处理
- **应用调用接口**：返回标准 HTTP 状态码（400/401/403/404/429/500）及 `request_id`，便于问题定位。
- **组件类接口**：遵循阿里云 OpenAPI 统一格式，错误信息在 `Code` 与 `Message` 字段中返回。

## 限制和注意事项

- **地域限制**：DashScope 应用调用接口（文档 7、8、10、11）均标注“仅适用于华北2（北京）地域”，但实际支持范围更广（见前述注意项）；组件类 OpenAPI 则按标准阿里云地域（如 `cn-beijing`）调用。
- **会话时效性**：`session_id` 在连续 1 小时无请求后自动失效，不可复用；若需持久会话，应自行维护并定期刷新。
- **异步限制**：Responses API 异步模式不支持 `stream=true`，且暂不支持基于 `pre_response_id` 或 `conversation_id` 的上下文自动续接，每次请求需传入完整对话历史。
- **长期记忆弃用提示**：所有长期记忆相关文档（文档 17–32）均标记为“（旧）”，且文档 20 明确指出“长期记忆体尚不支持存储与管理用户画像”，建议新项目优先评估新版记忆方案。
- **权限要求**：操作业务空间（如查询所有 Workspace ID）需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号默认仅可见已加入的空间。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)


