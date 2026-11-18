# flow agent api

Flow Agent API 是阿里云百炼平台提供的核心接口体系，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。该 API 分为两类：**应用调用接口**（通过 DashScope 应用网关）和**组件类接口**（通过百炼 OpenAPI），二者在鉴权方式、Endpoint 和功能定位上存在明确区分。开发者需根据使用场景选择对应路径并严格遵循其认证与参数规范。

## 支持的模型/功能

Flow Agent API 主要支持以下三类能力：

- **智能体与工作流应用调用**：覆盖新版智能体（Agent 2.0）、旧版智能体及工作流应用的实时推理与异步任务调度。所有应用调用均基于 DashScope 网关，当前仅支持华北2（北京）地域（见[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)与[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)）。
- **Prompt 模板管理**：提供完整的 CRUD 接口（`CreatePromptTemplate`、`GetPromptTemplate` 等），支持系统预置与用户自定义模板，但**暂不支持文生图 Prompt 模板的创建**（见[CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)）。
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：提供 `Memory`（记忆体）与 `MemoryNode`（记忆片段）两级抽象的增删改查能力，用于持久化存储对话上下文信息。> **注意**：文档中多次强调该能力为“旧”版本（如[长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)标题所示），且说明中明确指出“[长期记忆](../concepts/long-term-memory.md)体尚不支持存储与管理用户画像”，建议关注后续替代方案。

## 关键参数

### 应用调用（DashScope API）
- `app_id`（URL 路径参数）：必填，应用唯一标识，从控制台获取。
- `prompt` 或 `messages`（请求体）：二选一。`prompt` 适用于单轮输入；`messages` 为数组，支持多轮对话与系统角色设定（`role: "system"`），若同时传入则优先使用 `messages`。
- `session_id`（可选）：用于恢复云端对话历史，1 小时无请求后自动失效。
- `workspace`（Header：`X-DashScope-WorkSpace`）：仅调用子业务空间应用时必需。
- `stream`（布尔，默认 `false`）：启用[流式输出](../concepts/streaming-output.md)，推荐设为 `true` 以降低超时风险。
- `incremental_output`（布尔，默认 `false`）：仅在 `stream=true` 时生效，控制是否增量返回（`true` 时每 chunk 仅含新增内容）。

### 组件类接口（OpenAPI）
- `workspaceId`（路径参数）：所有 Prompt 模板与长期记忆接口均强制要求，代表业务空间 ID。
- `promptTemplateId` / `memoryId` / `memoryNodeId`（路径参数）：各资源操作的核心标识符。
- `content`、`name`、`description` 等：按具体接口定义的业务字段（如 [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md) 返回 `content` 与 `variables`）。

## 使用方式

### 认证方式
- **应用调用接口**：使用 **阿里云百炼 API Key**，通过 `Authorization: Bearer <your-api-key>` Header 传递（见[认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)）。
- **组件类接口**（Prompt 模板、长期记忆等）：使用 **AccessKey 签名（ACS3-HMAC-SHA256）**，不支持 `Bearer` 方式；强烈推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成签名与代码（见[认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)）。

### 调用路径
- **应用调用**：
  - HTTP：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（同步）或 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（OpenAI 兼容模式）。
  - SDK：Python/Java DashScope SDK 已预置 endpoint，亦支持自定义 `base_url`。
- **组件类接口**：
  - HTTP：统一 Base URL 为 `https://bailian.{regionId}.aliyuncs.com`，路径含 `{workspaceId}`（如 `/llm-czal8nvvwb8d4xxx/promptTemplates`）。
  - SDK：使用阿里云通用 OpenAPI SDK，传入 `workspaceId` 作为路径参数。

### 典型流程
1. 在控制台获取 `APP_ID`、`Workspace ID` 与 `API Key`（见[获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）；
2. 根据场景选择调用方式（DashScope API 或 OpenAPI）并配置对应认证；
3. 构造请求（注意 `prompt`/`messages` 互斥、`workspace` Header、`stream`/`incremental_output` 组合等细节）；
4. 处理响应：应用调用返回 `request_id` 便于排查；组件接口遵循阿里云标准 `Code`/`Message` 结构。

## 限制和注意事项

- **地域限制**：所有应用调用接口（DashScope API）当前**仅支持华北2（北京）地域**，其他地域（如德国、新加坡）调用必须显式传入 `Workspace ID` 并确认 Base URL 合法性（见[获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）。
- **限流策略**：长期记忆相关接口（如 `ListMemories`、`UpdateMemory`）明确要求“两次请求间隔至少 1 秒”，否则可能触发限流（见[UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)）。
- **异步限制**：OpenAI 兼容模式的异步调用（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true` 会被忽略）（见[异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。
- **凭证获取**：`APP ID` 和 `Workspace ID` **仅能通过控制台手动获取**，不支持 API 或 CLI 查询（见[获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）。
- **幂等性**：`UpdateMemory`、`ListMemories`、`DeleteMemory` 等接口声明具备幂等性，但 `CreateMemory` 明确注明“不具备幂等性”，重复调用将创建新资源（见[CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)）。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)


