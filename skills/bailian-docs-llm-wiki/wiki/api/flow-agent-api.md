# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。该 API 分为两类：**应用调用接口**（通过 DashScope 应用网关）和**组件类接口**（通过百炼 OpenAPI），二者在鉴权方式、Base URL 和功能边界上存在明确划分。开发者需根据使用场景选择对应接口并严格遵循其认证与参数规范。

## 支持的模型/功能

Flow Agent API 支持以下核心能力：

- **应用调用**：调用新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，覆盖同步、异步与流式响应模式；
- **Prompt 工程支持**：提供完整的 Prompt 模板生命周期管理（创建、读取、更新、删除、列表），详见 [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)；
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：支持创建、查询、更新和删除[长期记忆](../concepts/long-term-memory.md)体（Memory）及其下属的记忆片段（MemoryNode），适用于需跨会话持久化用户上下文的场景；
- **辅助能力**：包括支付宝打赏状态查询、临时文件上传许可申请等扩展功能（见 [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)）。

> **注意**：文档中多次提及“长期记忆（旧）”，且 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 明确标注为“旧”，表明该能力已被新机制替代或即将下线，不建议新项目采用；当前主推的记忆能力应以控制台最新指南或新版 Agent SDK 文档为准。

## 关键参数

### 应用调用类（DashScope / Responses API）
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取 |
| `prompt` 或 `input` | string / array | 是 | 单轮输入文本，或多轮对话消息数组（含 `system`/`user` 角色） |
| `session_id` | string | 否 | 用于恢复云端对话历史；1 小时无请求自动失效 |
| `messages` | array | 否（替代 `prompt`+`session_id`） | 完整多轮上下文，优先级高于 `session_id`；要求 SDK 版本 ≥ Python 2.0.1 / Java 2.17.0 |
| `workspace` / `X-DashScope-WorkSpace` | string | 否（子业务空间必需） | 仅当应用部署于子业务空间或特定地域（如德国、新加坡）时需显式传入 |
| `stream` | boolean | 否（默认 `false`） | 是否启用[流式输出](../concepts/streaming-output.md)；推荐设为 `true` 以降低超时风险 |
| `incremental_output` | boolean | 否（流式下默认 `false`） | 流式增量输出开关；设为 `true` 时每 chunk 仅返回新增内容 |

### 组件类（OpenAPI）
- **Prompt 模板**：`workspaceId`（必填）、`name`（必填）、`content`（必填，支持 `${var}` 变量语法）；
- **长期记忆**：`workspaceId`（必填）、`memoryId`（必填，由 `CreateMemory` 返回）、`content`（记忆片段内容，≤200 字符）；
- 所有组件类接口均需通过阿里云 AccessKey 签名（`ACS3-HMAC-SHA256`），不接受 `Authorization: Bearer`。

## 使用方式

### 1. 鉴权方式（关键区分点）
- **应用调用接口**（如 `/apps/{APP_ID}/completion`）：使用 **百炼 API Key**，Header 中传 `Authorization: Bearer <your-api-key>`；
- **组件类接口**（如 `/promptTemplates`、`/memories`）：使用 **阿里云 AccessKey**，需按 OpenAPI 规范签名（推荐使用 [OpenAPI Explorer](https://api.aliyun.com/) 或官方 SDK）；  
  > **注意**：[认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md) 明确指出两类接口鉴权方式互斥，混用将导致 `401 Unauthorized`。

### 2. 调用路径示例
- **新版智能体应用（DashScope）**：  
  `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
- **工作流应用（Responses API 同步）**：  
  `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **创建 Prompt 模板（OpenAPI）**：  
  `POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/{workspaceId}/promptTemplates`
- **创建长期记忆体（OpenAPI）**：  
  `POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/{workspaceId}/memories`

### 3. 开发建议
- 优先使用 SDK（DashScope SDK 或阿里云 OpenAPI SDK）避免手动签名；
- 流式调用务必设置 `X-DashScope-SSE: enable`（HTTP）或使用 `streamCall`（Java SDK）；
- [异步任务](../concepts/asynchronous-task.md)（`background=true`）不支持[流式输出](../concepts/streaming-output.md)，且需轮询 `retrieve` 接口获取结果。

## 限制和注意事项

- **地域限制**：所有 DashScope API（含新版/旧版智能体、工作流、Responses）当前**仅支持华北2（北京）地域**，其他地域调用将失败；
- **凭证获取**：APP ID 和 Workspace ID **仅可通过控制台手动复制**，不支持 API 或 CLI 查询（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）；
- **长期记忆限流**：`CreateMemory` 等接口要求两次请求间隔 ≥1 秒，否则触发限流；
- **错误处理**：
  - 应用调用接口返回 `request_id`，便于问题定位；
  - 组件类接口遵循阿里云 OpenAPI 统一结构（`Code`/`Message` 字段）；
  - 常见 HTTP 状态码含义见 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)；
- **功能弃用提示**：文档中多处强调“长期记忆（旧）”及“Prompt 模板（暂不支持文生图）”，表明相关能力存在演进或范围限制，生产环境应确认最新兼容性。

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
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
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


