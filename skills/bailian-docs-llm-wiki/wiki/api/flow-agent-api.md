# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体与工作流应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。API 分为两类：面向应用调用的 DashScope 网关接口（基于 Bearer Token 鉴权），以及面向组件管理的阿里云 OpenAPI（基于 AccessKey 签名）。二者在 Base URL、认证方式、错误响应结构上均不兼容，开发者需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 支持以下核心能力：

- **应用调用**：调用新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，支持同步/异步模式、[流式输出](../concepts/streaming-output.md)（`stream=true`）与增量[流式输出](../concepts/streaming-output.md)（`incremental_output=true`）；  
- **Prompt 模板管理**：提供完整的 CRUD 及列表查询能力（`CreatePromptTemplate`、`GetPromptTemplate` 等），支持变量插值（如 `${theme}`），但[暂不支持文生图 Prompt 模板的创建](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)；  
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：提供记忆体（`Memory`）与记忆片段（`MemoryNode`）两级管理接口，可用于持久化用户上下文信息；  
- **其他扩展能力**：包括支付宝打赏状态查询、临时文件上传许可申请等，详见[其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)。

> **注意**：文档中多次提及“[长期记忆](../concepts/long-term-memory.md)（旧）”，结合[概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)中明确标注“长期记忆（旧）”的表述，表明该能力已被标记为遗留方案，新项目应优先评估替代方案。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `app_id` | string | 是（URL 路径） | 应用唯一标识，从控制台应用卡片复制获取；新版智能体与工作流应用均适用 | [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md) |
| `prompt` / `input` | string 或 array | 是 | 用户输入指令或消息数组；若传 `messages`，则 `prompt` 和 `session_id` 将被忽略 | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md) |
| `session_id` | string | 否 | 对话历史标识，启用后自动加载云端存储的上下文；1 小时无请求自动失效 | [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md) |
| `workspace` / `X-DashScope-WorkSpace` | string | 否（子空间必需） | 业务空间 ID，仅当调用子业务空间或特定地域（如德国、新加坡）应用时必需；也是[Base URL 的组成部分](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md) | [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md) |
| `stream` | boolean | 否（默认 `false`） | 是否启用[流式输出](../concepts/streaming-output.md)；推荐设为 `true` 以降低超时风险 | [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md) |
| `incremental_output` | boolean | 否（默认 `false`） | 仅在 `stream=true` 时生效；设为 `true` 可获得增量文本块（如 `"I"` → `"like"` → `"apple"`） | [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md) |

## 使用方式

### 1. 认证方式（必须区分）
- **应用调用接口**（DashScope 网关）：使用阿里云百炼 API Key，通过 `Authorization: Bearer <your-api-key>` 传递；  
- **组件类接口**（Prompt 模板、长期记忆等）：使用阿里云 AccessKey，采用 `ACS3-HMAC-SHA256` 签名；**不支持 `Bearer` 方式**，推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动签名。

### 2. 典型调用路径
- **获取凭证**：在控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取 `APP ID`；按需获取 `Workspace ID`（[获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）；  
- **选择协议**：
  - 同步交互 → 使用 [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md) 或 [Responses API 同步调用](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)；  
  - 耗时任务 → 使用 [Responses API 异步调用](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)，通过 `task_id` 轮询结果；  
  - 管理 Prompt/记忆 → 使用阿里云 OpenAPI（如 `POST /{workspaceId}/promptTemplates`）。

### 3. 地域限制
所有应用调用类接口（DashScope & Responses）**当前仅支持华北2（北京）地域**，该限制在多份文档中反复强调（如[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)、[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)、[异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)），跨地域调用将失败。

## 限制和注意事项

- **地域强约束**：应用调用接口（DashScope/Responses）仅限华北2（北京），而组件类接口（Prompt/记忆）虽未明示地域限制，但其 Base URL 依赖 `workspaceId`，实际受控于业务空间所在地域；  
- **异步不支持流式**：[异步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md) 明确指出“[异步任务](../concepts/asynchronous-task.md)暂不支持流式输出（`stream=true`）”；  
- **Workspace ID 获取方式受限**：`Workspace ID` **仅支持控制台手动获取**，不提供 API 或 CLI 查询能力（见[获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）；  
- **长期记忆（旧）已标记为遗留**：文档标题及正文多次使用“（旧）”标注，且无对应“新”方案说明，建议新项目避免深度依赖；  
- **鉴权不可混用**：DashScope 接口若误传 AccessKey 签名，或 OpenAPI 接口误传 `Bearer` Token，均会返回 `401 Unauthorized`；  
- **限流策略**：长期记忆相关接口要求两次请求间隔 ≥1 秒，否则可能触发限流（见[CreateMemory](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md) 等文档）。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
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
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)


