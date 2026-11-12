# flow agent api

Flow Agent API 是阿里云百炼平台提供的核心接口集合，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等底层组件。API 分为两类：面向应用调用的 DashScope 网关接口（Bearer 鉴权）和面向组件管理的百炼 OpenAPI（AccessKey 签名鉴权），二者在认证方式、Endpoint 和功能边界上严格分离。

## 支持的模型/功能

Flow Agent API 本身不直接暴露模型选择能力，而是通过**预配置的应用实例**间接使用模型。支持的功能包括：

- **应用调用**：同步/异步调用新版智能体（Agent 2.0）、旧版智能体及工作流应用，支持多轮对话（`messages`）、会话状态（`session_id`）、[流式输出](../concepts/streaming-output.md)（`stream=true`）与增量流式（`incremental_output=true`）；  
- **Prompt 工程**：通过 [CreatePromptTemplate](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md) 等接口全生命周期管理 Prompt 模板，支持变量插值（如 `${theme}`）；  
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：通过 `CreateMemory` / `CreateMemoryNode` 等接口构建结构化记忆体与记忆片段，供智能体在后续调用中显式引用；  
- **辅助能力**：支付宝打赏链接生成、临时文件上传许可申请等扩展功能（见 [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)）。

> **注意**：文档中多次提及“[长期记忆](../concepts/long-term-memory.md)（旧）”，表明该能力已被新架构替代，官方文档未提供迁移路径或新接口说明，建议优先评估新版记忆方案。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 所属接口类型 |
|------|------|------|------|--------------|
| `app_id` | string | 是 | 应用唯一标识，从控制台获取 | 应用调用（DashScope/API） |
| `prompt` 或 `input` | string/array | 是 | 单轮文本或消息数组（含 `system`/`user` 角色） | 应用调用 |
| `session_id` | string | 否 | 会话 ID，启用云端历史上下文（1 小时失效） | 应用调用（DashScope） |
| `workspace` / `workspaceId` | string | 条件必填 | 子业务空间 ID；默认空间可省略。注意：DashScope 接口 Header 传 `X-DashScope-WorkSpace`，OpenAPI 路径中作为 `{workspaceId}` | 两类接口均需 |
| `stream` | boolean | 否 | 是否启用 Server-Sent Events 流式响应（默认 `false`） | 应用调用（DashScope） |
| `incremental_output` | boolean | 否 | 仅 `stream=true` 时有效，控制是否增量返回（推荐 `true`） | 应用调用（DashScope） |
| `background` | boolean | 否 | Responses API 异步模式开关（设为 `true` 时立即返回任务 ID） | 应用调用（Responses） |

## 使用方式

### 1. 认证方式
- **应用调用接口**（如 `/apps/{APP_ID}/completion`）：使用阿里云百炼 API Key，Header 中传 `Authorization: Bearer <your-api-key>`；  
- **组件类接口**（如 Prompt 模板、长期记忆）：属于阿里云 OpenAPI，必须使用 AccessKey 进行 `ACS3-HMAC-SHA256` 签名，[不支持 Bearer 方式](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)。推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成代码。

### 2. Endpoint 与地域约束
- **应用调用 Base URL**：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（DashScope）或 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（Responses）；  
- **组件类 Base URL**：`https://bailian.{region}.aliyuncs.com`，路径含 `{workspaceId}`（如 `/llm-us9hjmt32nysdxxx/promptTemplates`）；  
- **重要限制**：所有应用调用接口（DashScope/Responses）当前**仅支持华北2（北京）地域**，跨地域调用将失败。

### 3. 典型调用流程
1. 在控制台获取 `APP_ID` 和（若需要）`Workspace ID`（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）；  
2. 根据场景选择协议：  
   - 实时交互 → 使用 DashScope 同步接口或 Responses 同步 API；  
   - 长耗时任务（如报告生成）→ 使用 Responses 异步 API（`background=true`），再轮询 `retrieve`；  
3. 组件管理（如创建 Prompt 模板）→ 调用 OpenAPI，确保签名正确且 `workspaceId` 路径匹配。

## 限制和注意事项

- **地域锁定**：所有应用调用接口（DashScope/Responses）强制限定于华北2（北京），其他地域（如德国法兰克福、新加坡）的请求将被拒绝；  
- **异步限制**：Responses API 的异步模式（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true` 会被忽略）；  
- **会话时效性**：`session_id` 对应的云端对话历史在连续 1 小时无请求后自动失效，不可恢复；  
- **权限要求**：  
  - 查询全部业务空间需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；  
  - 普通子账号默认只能查看其已加入的业务空间 ID；  
- **错误处理**：两类接口错误码体系不同——应用调用返回 `request_id` + 自定义错误码，组件类接口遵循阿里云 OpenAPI 统一格式（`Code`/`Message` 字段），详见 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)；  
- **API Key 与 AccessKey 不可混用**：向 DashScope 接口发送 AccessKey 签名请求，或向 OpenAPI 发送 Bearer [Token](../concepts/token.md)，均会导致 `401 Unauthorized`。

## 来源文档

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
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)


