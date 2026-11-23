# flow agent api

Flow Agent API 是阿里云百炼平台提供的统一接口体系，用于调用智能体应用、工作流应用及管理 Prompt 模板、[长期记忆](../concepts/memory.md)等组件。它分为两类网关：面向终端应用调用的 DashScope 应用网关（Bearer 鉴权），以及面向平台组件管理的百炼 OpenAPI（AccessKey 签名鉴权）。两类接口在 Base URL、认证方式、错误响应结构上均存在差异，开发者需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 支持以下核心能力：

- **应用调用**：调用已发布的**新版智能体应用（Agent 2.0）**、**旧版智能体应用**和**工作流应用**，支持同步/异步、流式/非[流式输出](../concepts/streaming.md)；  
- **Prompt 工程**：通过 [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md) 等全套接口管理自定义 Prompt 模板，支持变量插值与类型区分（System/Custom）；  
- **[长期记忆](../concepts/memory.md)（旧）**：提供完整的 CRUD 能力，包括创建/查询/更新/删除[长期记忆](../concepts/memory.md)体（`Memory`）及其下属的记忆片段（`MemoryNode`），适用于需持久化用户上下文的复杂 Agent 场景；  
- **辅助功能**：含支付宝打赏状态查询、临时文件上传许可申请等扩展能力（见 [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)）。

> **注意**：文档中多次提及“长期记忆（旧）”，表明该能力已被标记为遗留方案；新项目应优先评估官方推荐的替代机制（如新版记忆服务或应用内状态管理），当前文档未说明替代方案细节。

## 关键参数

### 应用调用类（DashScope 网关）
- `app_id`（URL 路径参数）：必填，应用唯一标识；  
- `prompt` 或 `messages`（请求体 `input` 内）：二选一，`messages` 支持多轮对话与系统角色设定；  
- `session_id`（可选）：用于恢复云端对话历史，1 小时无请求自动失效；  
- `workspace`（Header `X-DashScope-WorkSpace`）：仅子业务空间或特定地域（如法兰克福、北京、新加坡等）调用时必需；  
- `stream` 与 `incremental_output`（均为布尔值）：控制[流式输出](../concepts/streaming.md)行为，推荐 `stream=true` + `incremental_output=true` 以优化延迟与客户端处理逻辑。

### 组件类（OpenAPI 网关）
- `workspaceId`（路径参数）：所有 Prompt 模板与长期记忆接口均强制要求，对应业务空间 ID；  
- `promptTemplateId` / `memoryId` / `memoryNodeId`（路径参数）：各资源操作的唯一标识；  
- `name`, `content`, `description`（请求体）：分别用于模板命名、Prompt 内容、记忆体描述，均有长度与字符集限制（如 `description` 限 1–50 字符）。

## 使用方式

### 认证方式
- **应用调用接口**（如 `/apps/{APP_ID}/completion`）：使用阿里云百炼 API Key，通过 `Authorization: Bearer <your-api-key>` 传入；  
- **组件类接口**（如 Prompt 模板、长期记忆）：属于阿里云 OpenAPI，必须使用 AccessKey 进行 `ACS3-HMAC-SHA256` 签名，不支持 Bearer 方式；推荐直接使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成调用代码。

### 请求构造示例
- **DashScope 同步调用**：  
  `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  Header：`Authorization: Bearer sk-xxx`, `X-DashScope-WorkSpace: llm-xxx`（如需）  
  Body：`{"input": {"prompt": "你好"}}`  

- **OpenAPI 获取 Prompt 模板**：  
  `GET /{workspaceId}/promptTemplates/{promptTemplateId}`  
  需签名，或通过 SDK 构造（如 `bailian_client.get_prompt_template(workspace_id='llm-xxx', prompt_template_id='xxx')`）。

### 开发者工具链
- SDK：推荐使用 DashScope SDK（Python/Java）调用应用接口，阿里云 SDK（Alibaba Cloud SDK for Python/Java）调用组件接口；  
- 调试：应用接口可通过控制台「应用卡片 → 发布 → API 调试」在线测试；组件接口建议使用 [OpenAPI Explorer](https://api.aliyun.com/) 实时调试并生成代码。

## 限制和注意事项

- **地域限制**：所有 DashScope 应用调用接口（含新版/旧版智能体、工作流、Responses API）当前**仅支持华北2（北京）地域**，调用前需确认 Base URL 及 workspace 所属地域一致；  
- **[流式输出](../concepts/streaming.md)约束**：[异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md) 明确指出异步任务**不支持 `stream=true`**，若需流式响应，请改用同步模式；  
- **凭证获取方式**：APP ID 和 Workspace ID **仅支持控制台手动复制**，不提供 API 或 CLI 查询能力（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)）；  
- **限流策略**：长期记忆类接口（如 `GetMemory`, `ListMemories`）要求两次请求间隔 ≥ 1 秒，否则可能触发限流；  
- **错误处理**：两类接口错误码体系不同——应用调用返回 `request_id` + 自定义错误字段，组件类遵循阿里云 OpenAPI 标准（`Code`/`Message` 字段），详见 [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)；  
- **幂等性**：`GetMemory`, `UpdateMemory`, `ListMemories`, `DeleteMemory` 等接口声明具有幂等性，但 `CreateMemory` 明确注明**不具备幂等性**，重复调用将创建多个独立记忆体。

## 来源文档

- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [Flow Agent API 错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)


