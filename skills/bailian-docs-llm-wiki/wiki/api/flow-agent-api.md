# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体与工作流应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。该 API 分为两类：面向应用调用的 DashScope 网关接口（使用 API Key 鉴权），以及面向组件管理的阿里云 OpenAPI（使用 AccessKey 签名鉴权）。两类接口在 Base URL、认证方式、错误响应格式上均存在差异，开发者需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 支持以下三类核心能力：

- **应用调用**：调用新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，支持同步与异步模式、[流式输出](../concepts/streaming-output.md)（`stream=true`）及增量输出（`incremental_output=true`）[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)。
- **Prompt 模板管理**：提供完整的 CRUD 接口（创建、获取、更新、删除、列表），支持变量占位符（如 `${theme}`）和系统/自定义模板类型 [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)。
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：提供记忆体（Memory）与记忆片段（MemoryNode）两级管理能力，包括增删改查及分页列表，适用于持久化存储用户上下文信息 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)。

> **注意**：文档中多次提及“[长期记忆](../concepts/long-term-memory.md)（旧）”，表明该能力已被标记为遗留方案；新项目应优先评估平台推荐的替代方案（如新版会话状态管理），但当前 API 仍完全可用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 所属接口类型 |
|--------|------|------|------|--------------|
| `app_id` | string | 是 | 应用唯一标识，从控制台应用卡片复制获取 | 应用调用（DashScope/API） |
| `workspace` / `workspaceId` | string | 否（子空间必填） | 业务空间 ID；应用位于默认空间时可省略，子空间或特定地域（如法兰克福、东京）下必须传入 | 全局（两类接口均需） |
| `prompt` | string | 是（部分场景） | 用户单轮指令文本；若使用 `messages` 数组则无需此字段 | 应用调用（DashScope） |
| `messages` | array | 否（替代 `prompt`） | 多轮对话消息数组，含 `system`/`user` 角色，支持[多模态](../concepts/multi-modal.md)内容 | 应用调用（DashScope & Responses） |
| `session_id` | string | 否 | 对话历史标识，有效期为 1 小时内无请求即失效 | 应用调用（DashScope） |
| `stream` | boolean | 否（默认 `false`） | 是否启用[流式输出](../concepts/streaming-output.md)；设为 `true` 时需配合 `X-DashScope-SSE: enable` Header | 应用调用（DashScope） |
| `incremental_output` | boolean | 否（默认 `false`） | 仅在 `stream=true` 时生效，控制是否增量返回（推荐设为 `true`） | 应用调用（DashScope） |
| `background` | boolean | 否（默认 `false`） | Responses API 异步调用标志；设为 `true` 则立即返回任务 ID | 应用调用（Responses） |

## 使用方式

### 1. 认证方式（关键区分点）
- **应用调用接口**（如 `/apps/{app_id}/completion`）：使用 **百炼 API Key**，通过 `Authorization: Bearer <your-api-key>` Header 传递 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)。
- **组件类接口**（如 Prompt 模板、长期记忆）：使用 **阿里云 AccessKey**，采用 `ACS3-HMAC-SHA256` 签名；**不支持** `Bearer` 方式，推荐使用阿里云 SDK 或 OpenAPI Explorer 自动签名。

### 2. 基础调用流程
- **获取凭证**：通过控制台手动获取 `APP ID` 和（如需）`Workspace ID`；API Key 在 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。
- **选择协议**：
  - 同步实时交互 → 使用 DashScope API（`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`）或 Responses 同步端点（`/responses`）；
  - 耗时任务 → 使用 Responses 异步端点（`/responses` + `background=true`），再轮询 `retrieve` 接口 [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)；
  - 组件管理 → 使用 OpenAPI（`bailian.{region}.aliyuncs.com`），按 `/{workspaceId}/promptTemplates/...` 路径构造请求。

### 3. 地域限制
所有应用调用类接口（DashScope & Responses）**当前仅支持华北2（北京）地域**，其他地域调用将失败。组件类接口（Prompt/记忆）未明确限制，但 `workspaceId` 必须与实际业务空间所在地域一致。

## 限制和注意事项

- **地域强约束**：DashScope API 与 Responses API 的文档均明确标注“仅适用于华北2（北京）地域”，跨地域调用将返回 404 或鉴权失败，不可绕过。
- **异步与流式互斥**：Responses API 的异步调用（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true`），否则请求将被拒绝 [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **长期记忆限流**：所有长期记忆相关接口（Create/Get/List 等）要求两次请求间隔 ≥ 1 秒，否则可能触发服务端限流，需在客户端实现退避重试。
- **凭证获取方式**：`APP ID` 和 `Workspace ID` **仅支持控制台手动复制**，不提供 API 或 CLI 查询能力，自动化部署需预先配置 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。
- **错误处理差异**：应用调用接口返回 `request_id` 便于问题定位；组件类接口遵循阿里云 OpenAPI 标准，错误信息在 `Code`/`Message` 字段中 [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
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
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)


