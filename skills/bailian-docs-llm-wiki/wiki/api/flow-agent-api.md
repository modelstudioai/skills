# flow agent api

Flow Agent API 是阿里云百炼平台提供的核心接口体系，用于调用已发布的智能体（Agent）与工作流（Workflow）应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等底层组件。该 API 分为两类：面向应用调用的 DashScope 网关接口（使用 [API Key 鉴权](../concepts/api-key-authentication.md)），以及面向组件管理的百炼 OpenAPI（使用 AccessKey 签名鉴权）。两类接口在 Base URL、认证方式、错误响应格式上均不兼容，需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 本身**不直接暴露模型选择能力**，其功能完全由所调用的智能体或工作流应用封装决定。应用在控制台发布时已绑定特定模型（如 Qwen-Max、Qwen-Plus）及编排逻辑，API 调用仅触发该预设流程。当前支持的应用类型包括：

- **新版智能体应用（Agent 2.0）**：基于全新架构，支持深度思考、多工具协同等高级能力，详见[新版智能体应用 API 参考](raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)；
- **旧版智能体应用与工作流应用**：兼容历史部署，提供稳定的基础推理与流程执行能力，详见[工作流与旧版智能体应用 API](raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)；
- **Prompt 模板管理**：通过百炼 OpenAPI 提供完整的 CRUD 能力，支持系统级与用户自定义模板，适用于提示工程标准化场景；
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：提供 `Memory`（记忆体）与 `MemoryNode`（记忆片段）两级抽象，用于持久化存储对话上下文信息，但文档明确标注其为“旧”机制，新项目应评估替代方案；
- **其他辅助能力**：包括支付宝打赏状态查询、临时文件上传许可申请等，属于边缘功能，详见[其他](raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)。

> **注意**：文档中多次提及“[长期记忆](../concepts/long-term-memory.md)（旧）”，且其所属目录路径（`api-bailian-2023-12-29-dir-long-term-memory`）包含明确的时间戳，结合[概览](raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)中“Prompt 模板、长期记忆（旧）与其他组件”的括号标注，可确认该能力已被标记为遗留（legacy），官方推荐路径应以新版智能体内置的记忆机制为准。

## 关键参数

### 应用调用类（DashScope API）
- `app_id`（URL 路径参数）：必填，目标应用唯一标识，从控制台应用卡片复制；
- `prompt`（请求体 `input.prompt`）：必填，用户单轮输入文本；
- `session_id`（请求体 `input.session_id`）：可选，用于恢复云端对话历史，1 小时无请求自动失效；
- `messages`（请求体 `input.messages`）：可选，替代 `prompt` 和 `session_id` 的多轮对话数组，需符合 OpenAI 格式（含 `role: "system"` / `"user"` 及 `content`）；
- `workspace`（Header `X-DashScope-WorkSpace`）：可选，仅当调用子业务空间下的应用时必需；
- `stream`（Header `X-DashScope-SSE: enable` 或请求体 `parameters.stream`）：可选，启用[流式输出](../concepts/streaming-output.md)，默认 `false`；
- `incremental_output`（请求体 `parameters.incremental_output`）：仅在 `stream=true` 时生效，控制是否增量返回（`true` 推荐）；
- `enable_thinking`（请求体 `parameters.enable_thinking`）：可选，启用深度思考模型，具体行为依赖应用配置。

### 组件管理类（OpenAPI）
- `workspaceId`（URL 路径参数）：所有组件接口必填，业务空间唯一 ID；
- `promptTemplateId` / `memoryId` / `memoryNodeId`：各资源操作的主键，由创建接口返回；
- `name`, `content`, `description`：各资源的核心属性字段，均有明确长度与字符集限制（如 `content` 最长 200 字符）。

## 使用方式

### 认证方式
- **应用调用接口**（如 `/apps/{APP_ID}/completion`）：使用百炼 API Key，通过 `Authorization: Bearer <your-api-key>` Header 传递；
- **组件类接口**（如 `/promptTemplates`, `/memories`）：使用阿里云 AccessKey，必须通过 `ACS3-HMAC-SHA256` 签名，**不支持** `Bearer` 方式；强烈推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成调用代码。

### 典型调用路径
1. **获取凭证**：在控制台[获取APP ID和Workspace ID](raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)并配置 API Key 或 AccessKey；
2. **选择协议**：
   - 追求开箱即用与 OpenAI 兼容性 → 使用 [Responses API](raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)（同步/异步）；
   - 追求性能与完整功能 → 使用 [DashScope API](raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)；
   - 管理 Prompt 或记忆 → 使用百炼 OpenAPI（如 `CreatePromptTemplate`, `CreateMemory`）；
3. **构造请求**：根据所选接口，填充对应参数与 Header（注意 `workspace` Header 与 `workspaceId` 路径参数的区别）；
4. **处理响应**：应用调用接口返回标准 JSON，含 `output.text`；组件接口遵循阿里云统一 OpenAPI 响应结构，错误时返回 `Code`/`Message` 字段。

### 地域限制
所有文档（[新版智能体应用 API 参考](raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)、[工作流与旧版智能体应用 API](raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)、[同步调用 API 参考](raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)）均明确标注“**仅适用于华北2（北京）地域**”。若需在其他地域（如德国法兰克福、新加坡）调用，必须使用对应地域的 Base URL 并传入 `Workspace ID`，详见[获取APP ID和Workspace ID](raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。

## 限制和注意事项

- **地域强约束**：DashScope API 的 `https://dashscope.aliyuncs.com` Endpoint 仅服务华北2（北京），跨地域调用必须切换 Base URL 并确保 Workspace ID 正确嵌入（如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`），否则返回 404；
- **会话时效性**：`session_id` 在连续 1 小时无请求后自动失效，客户端需自行维护会话生命周期；
- **流式与异步互斥**：[异步调用API参考](raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md) 明确指出“异步任务暂不支持[流式输出](../concepts/streaming-output.md)（stream=true）”，二者不可同时启用；
- **长期记忆限流**：`CreateMemory` 等接口要求两次请求间隔 ≥1 秒，否则触发限流，需在客户端实现退避重试；
- **参数冲突规则**：当 `messages` 与 `session_id` 同时传入时，`messages` 优先级更高，`session_id` 和 `prompt` 将被忽略；
- **错误码差异**：应用调用接口返回 `request_id` 便于问题追踪，而组件类接口返回 `Code`/`Message` 字段，开发者需按接口类型分别处理错误响应；
- **权限最小化原则**：调用组件接口需精确授予 RAM 权限（如 `sfm:CreatePromptTemplate`），而非宽泛的 `AliyunBailianFullAccess`，避免安全风险。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/flow-agent-api/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [同步调用 API 参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [Responses API](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api.md)
- [异步调用API参考](../../raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-e09e2567b2b8646d.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-16aa76e6889fef61.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)


