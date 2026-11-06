# flow agent api

Flow Agent API 是百炼平台提供的核心接口体系，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等底层组件。该 API 分为两类：面向终端应用调用的 DashScope 应用网关接口（使用 API Key 鉴权），以及面向开发者能力扩展的百炼 OpenAPI 组件接口（使用 AccessKey 签名鉴权）。两类接口在 Base URL、认证方式、错误响应结构上均存在显著差异，需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 支持以下核心功能：

- **应用调用**：调用新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，支持同步/异步、流式/非[流式输出](../concepts/streaming-output.md)等多种交互模式；
- **Prompt 工程支持**：通过 [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md) 等全套 CRUD 接口，实现 Prompt 模板的创建、更新、查询与批量管理；
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：提供 `Memory` 和 `MemoryNode` 两级抽象，支持创建、读取、更新、删除[长期记忆](../concepts/long-term-memory.md)体及其片段，适用于需跨会话持久化用户偏好或上下文的场景；
- **辅助能力**：包括支付宝打赏状态查询、临时文件上传许可申请等扩展能力（见 [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)）。

> **注意**：文档中多次提及“长期记忆（旧）”，表明该能力已被标记为遗留方案；当前主推的记忆机制应以控制台最新指南或新版 Agent SDK 文档为准，本 API 不代表长期演进方向。

## 关键参数

### 应用调用类（DashScope API）
- `app_id`（必选，URL 路径参数）：应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取；
- `prompt` 或 `messages`（必选，请求体）：单轮输入用 `prompt` 字符串；多轮/系统指令场景用 `messages` 数组（含 `system`/`user` 角色对象）；
- `session_id`（可选）：启用云端对话历史续写，1 小时无活动后自动失效；
- `workspace`（可选 Header：`X-DashScope-WorkSpace`）：仅子业务空间或特定地域（如法兰克福、东京）下必需；
- `stream`（可选，默认 `false`）：启用 Server-Sent Events [流式输出](../concepts/streaming-output.md)，需设置 Header `X-DashScope-SSE: enable`；
- `incremental_output`（可选，默认 `false`）：仅在 `stream=true` 时生效，控制是否返回增量 token（推荐设为 `true`）。

### 组件类（OpenAPI）
- `workspaceId`（必选，路径参数）：所有 Prompt 模板与 Memory 接口均需显式传入，对应业务空间 ID；
- `promptTemplateId` / `memoryId` / `memoryNodeId`（必选，路径参数）：各资源唯一标识，由创建接口返回；
- `content`（Prompt 模板/记忆片段必填）：模板内容或记忆文本，长度与字符集受严格限制（如记忆片段限 1–200 字符）。

## 使用方式

### 认证方式（必须区分）
- **应用调用接口**（如 `/apps/{APP_ID}/completion`）：使用百炼 API Key，Header 中传 `Authorization: Bearer <your-api-key>`；
- **组件类接口**（如 `/promptTemplates`、`/memories`）：使用阿里云 AccessKey 进行 `ACS3-HMAC-SHA256` 签名，**不支持** `Bearer` 方式；推荐直接使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成调用代码。

### 典型调用路径
1. **获取凭证**：在控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)复制 `APP_ID`；按需获取 `Workspace ID`（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）；
2. **选择协议**：
   - 实时交互 → 用 DashScope API（HTTP 或 SDK），推荐 `stream=true` + `incremental_output=true`；
   - 耗时任务 → 用 Responses API 异步模式（`background=true`），轮询 `retrieve` 接口查状态；
   - 管理 Prompt/Memory → 用百炼 OpenAPI，通过 `workspaceId` 定位资源；
3. **调试验证**：所有应用均支持控制台内“发布 → API 调试”在线测试；OpenAPI 接口可直连 [OpenAPI Explorer](https://api.aliyun.com/)。

## 限制和注意事项

- **地域限制**：DashScope 应用调用接口（含新版 Agent、工作流、Responses API）目前**仅支持华北2（北京）地域**，其他地域调用将失败；
- **异步限制**：Responses API 的异步模式（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（即 `stream=true` 无效），且暂不支持基于 `pre_response_id` 的上下文自动续接；
- **鉴权隔离**：两类接口鉴权完全独立——误用 API Key 调用 OpenAPI 或误用 AccessKey 调用 DashScope API 均会返回 `401 Unauthorized`；
- **长期记忆弃用提示**：文档标题明确标注为“长期记忆（旧）”，且其功能描述中强调“尚不支持存储与管理用户画像”，建议新项目优先评估新版记忆方案；
- **限流策略**：Memory 相关接口（如 `CreateMemory`、`ListMemories`）有明确限流要求：“两次请求间隔至少 1 秒”，超频将触发服务端限流；
- **参数冲突**：当 `messages` 与 `session_id` 同时传入时，DashScope API 会**优先使用 `messages` 内容，忽略 `session_id` 和 `prompt`**，此行为已在 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md) 中明确定义。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
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
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)


