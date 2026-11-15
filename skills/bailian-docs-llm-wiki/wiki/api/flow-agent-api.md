# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。API 分为两类：面向终端应用调用的 **DashScope 应用网关接口**（使用 API Key 鉴权），以及面向开发者配置管理的 **百炼 OpenAPI 组件接口**（使用 AccessKey 签名鉴权）。二者在 Base URL、认证方式、错误响应结构上均不兼容，需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 支持以下核心能力：

- **应用调用**：调用新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，覆盖同步、异步、[流式输出](../concepts/streaming-output.md)等多种交互模式；
- **Prompt 工程支持**：通过 [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md) 等全套 REST 接口，实现 Prompt 模板的增删改查与变量注入；
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：提供完整的记忆体（Memory）与记忆片段（MemoryNode）生命周期管理，包括创建、查询、更新与删除（如 [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md) 和 [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)）；
- **辅助功能**：含支付宝打赏状态查询、临时文件上传许可申请等扩展能力（见 [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)）。

> **注意**：文档中多次提及“[长期记忆](../concepts/long-term-memory.md)（旧）”，表明该能力已被标记为遗留方案；当前主推的记忆能力应以控制台或新版 SDK 中的“长期记忆（新）”为准，但本文档未提供其接口说明，开发者需参考控制台指引或后续更新文档。

## 关键参数

### 应用调用类（DashScope API）
- `app_id`（URL 路径参数）：必填，应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取；
- `prompt` 或 `messages`（请求体）：二选一。`prompt` 用于单轮文本输入；`messages` 为数组，支持 system/user 多角色上下文（详见 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)）；
- `session_id`（可选）：启用云端对话历史续写，1 小时无请求自动失效；
- `workspace`（Header `X-DashScope-WorkSpace`）：仅子业务空间或特定地域（如德国、新加坡）下必需；
- `stream` 与 `incremental_output`（可选）：控制[流式输出](../concepts/streaming-output.md)行为，推荐 `stream=true` + `incremental_output=true` 以降低超时风险并提升体验。

### 组件类（OpenAPI）
- `workspaceId`（路径参数）：所有 Prompt 模板与长期记忆接口均强制要求，对应业务空间 ID；
- `promptTemplateId` / `memoryId` / `memoryNodeId`（路径参数）：各资源操作的核心标识符；
- `content`、`name`、`description` 等（请求体）：按接口语义定义，长度与格式有明确限制（如 `content` 最长 200 字符，见 [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)）。

## 使用方式

### 认证方式严格分离
- **应用调用接口**（如 `/api/v1/apps/{APP_ID}/completion`）：使用阿里云百炼 API Key，通过 `Authorization: Bearer <your-api-key>` 传入；
- **组件类接口**（如 `/promptTemplates`）：属于阿里云 OpenAPI，必须使用 AccessKey 签名（ACS3-HMAC-SHA256），**不支持 `Bearer` Token**；推荐直接使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 生成调用代码。

### 调用路径示例
- DashScope 同步调用（北京地域）：  
  `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
- DashScope [异步调用](../concepts/asynchronous-invocation.md)（OpenAI 兼容模式）：  
  `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  （需设置 `background=true`）
- Prompt 模板创建（OpenAPI）：  
  `POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/{workspaceId}/promptTemplates`

> **注意**：文档 5 明确指出，`Workspace ID` 目前**只能通过控制台手动获取，不支持 API 或 CLI 查询**，此限制直接影响自动化部署流程设计。

## 限制和注意事项

- **地域限制**：DashScope 应用调用接口（含新版智能体、工作流、Responses API）当前**仅支持华北2（北京）地域**，其他地域调用将失败（见 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)、[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)）；
- **异步与流式互斥**：Responses API 的[异步调用](../concepts/asynchronous-invocation.md)（`background=true`）**不支持 `stream=true`**，若需流式响应，必须使用同步接口；
- **长期记忆限流**：所有 Memory/MemoryNode 接口均要求两次请求间隔 ≥1 秒，否则触发限流（见 [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)）；
- **错误处理差异**：应用调用接口返回 `request_id` 便于问题定位；组件类接口遵循阿里云统一 OpenAPI 结构，错误信息在 `Code`/`Message` 字段中（见 [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)）；
- **幂等性说明**：`UpdateMemory`、`ListMemories`、`DeleteMemory` 等接口声明具有幂等性，但 `CreateMemory` 明确注明“不具备幂等性”，重复调用将创建多个独立记忆体。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)


