# flow agent api

Flow Agent API 是百炼平台提供的核心接口集合，用于调用已发布的智能体与工作流应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。API 分为两类：**应用调用接口**（通过 DashScope 应用网关）和**组件类接口**（通过阿里云 OpenAPI），二者在 Base URL、鉴权方式、错误响应格式上均不兼容，开发者需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 不直接暴露底层大模型选型，而是通过预发布应用封装能力。支持以下核心功能：

- **应用调用**：调用新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，支持同步/异步、流式/非[流式输出](../concepts/streaming-output.md)；
- **Prompt 工程**：提供完整的 Prompt 模板生命周期管理，包括创建、读取、更新、删除及列表查询，详见 [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)；
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：支持构建结构化记忆体（Memory）及记忆片段（MemoryNode），用于跨会话状态持久化，但文档明确标注其为“旧”能力，新项目应评估替代方案；
- **辅助能力**：含临时文件上传许可（`ApplyTempStorageLease`）、支付宝打赏状态查询等扩展接口，适用于特定高代码或商业化场景。

> **注意**：文档 1 明确指出“[长期记忆](../concepts/long-term-memory.md)（旧）”属于历史组件，而新版智能体应用（文档 7）和工作流应用（文档 9）均未提及集成该能力；同时，[长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 文档未说明其与新版 Agent 的兼容性，建议优先使用应用内建的状态管理机制。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 所属接口类型 |
|------|------|------|------|--------------|
| `app_id` | string | 是 | 应用唯一标识，在控制台应用卡片中获取。HTTP 调用时需嵌入 URL；SDK 中作为字段传入。 | 应用调用（DashScope / Responses） |
| `workspace_id` | string | 条件必填 | 业务空间 ID。调用子业务空间应用、或在德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）地域调用时必需。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。 | 全局（两类接口均需） |
| `session_id` | string | 否 | 对话会话标识。启用后自动加载云端历史，1 小时无请求即失效。仅 DashScope API 支持。 | 应用调用（DashScope） |
| `input` / `prompt` | string \| array | 是 | 用户输入内容。DashScope API 使用 `prompt`（单轮）或 `messages`（多轮）；Responses API 统一使用 `input` 字段，支持字符串或消息数组。 | 应用调用（两类） |
| `background` | boolean | 否 | Responses API 异步调用开关。设为 `true` 时立即返回任务 ID，后续需轮询结果。**注意：异步任务不支持 `stream=true`**。 | 应用调用（Responses） |
| `workspaceId` | string | 是 | 组件类接口（如 Prompt、Memory）的路径参数，对应业务空间 ID，不可省略。 | 组件类（OpenAPI） |

## 使用方式

### 1. 鉴权方式（关键区别）
- **应用调用接口**（DashScope / Responses）：使用 **百炼 API Key**，Header 中传递 `Authorization: Bearer <your-api-key>`；
- **组件类接口**（Prompt 模板、长期记忆等）：使用 **AccessKey 签名（ACS3-HMAC-SHA256）**，不支持 Bearer [Token](../concepts/token.md)，必须通过阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 调用。

### 2. 典型调用路径
- **调用智能体/工作流应用**：
  - 推荐使用 **DashScope API**（低延迟、功能全）：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - 兼容 OpenAI 生态可选 **Responses API**：同步用 `/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，异步需加 `background=true`。
- **管理 Prompt 模板**：
  - 创建：`POST /{workspaceId}/promptTemplates`（需 AccessKey 签名）
  - 列表：`GET /{workspaceId}/promptTemplates?name=xxx`（支持分页与关键词搜索）
- **管理长期记忆体**：
  - 创建 Memory：`POST /{workspaceId}/memories`
  - 创建 MemoryNode：`POST /{workspaceId}/memories/{memoryId}/memoryNodes`

### 3. 开发者工具链
- 控制台：用于获取 `APP_ID`、`Workspace ID`、`API Key` 及在线调试（应用卡片 → 发布 → API 调试）；
- SDK：DashScope SDK（应用调用）、阿里云通用 SDK（组件类）；
- OpenAPI Explorer：免签名调试所有组件类接口，自动生成各语言示例代码。

## 限制和注意事项

- **地域限制**：DashScope API（文档 7、9、10、11）和 Responses API（文档 10、11）均明确声明“仅适用于华北2（北京）地域”，其他地域调用将失败；
- **凭证获取限制**：`APP ID` 和 `Workspace ID` **仅支持控制台手动复制**，不提供 API 或 CLI 查询能力（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）；
- **长期记忆限流**：所有 Memory 相关接口（创建、查询、更新等）要求两次请求间隔 ≥ 1 秒，否则触发限流（文档 17、18、19、20、22）；
- **异步流式冲突**：Responses API 的异步调用（`background=true`）**明确不支持[流式输出](../concepts/streaming-output.md)**（文档 11），若需流式响应，请改用 DashScope API 的 `stream=true`；
- **错误处理差异**：应用调用接口返回 `request_id` 便于问题定位；组件类接口遵循阿里云 OpenAPI 标准，返回 `Code`/`Message` 字段（见 [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)）；
- **幂等性说明**：`GetMemory`、`UpdateMemory`、`DeleteMemory`、`ListMemories` 等接口具有幂等性；`CreateMemory` 不具备幂等性（文档 17、18、19、20、22）。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)


