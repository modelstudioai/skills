# flow agent api

Flow Agent API 是阿里云百炼平台提供的核心接口体系，用于调用已发布的智能体与工作流应用，并管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件能力。API 分为两类：面向终端应用的「应用调用接口」（通过 DashScope 网关）和面向开发者的「组件类接口」（通过百炼 OpenAPI）。二者在鉴权方式、Base URL、错误格式上均不兼容，需严格区分使用场景。

## 支持的模型/功能

Flow Agent API 本身不直接绑定特定大模型，而是通过封装后的智能体（Agent）或工作流（Workflow）应用对外提供能力。当前支持以下两类应用形态：

- **新版智能体应用（Agent 2.0）**：基于 DashScope API 调用，支持 `stream` [流式输出](../concepts/streaming-output.md)、`incremental_output` 增量流、`enable_thinking` 深度思考等高级参数，详见[新版智能体应用 API 参考](raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)。
- **工作流与旧版智能体应用**：同样通过 DashScope API 调用，但支持更灵活的 `messages` 多轮对话输入格式（含 system/user 角色），并兼容部分 OpenAI 风格结构，详见[工作流与旧版智能体应用 API](raw/_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)。

此外，组件类接口提供可编程的 Prompt 模板与[长期记忆](../concepts/long-term-memory.md)管理能力：
- **Prompt 模板**：支持全生命周期操作（Create/Get/Update/Delete/List），适用于标准化提示词复用与版本管理，参见[CreatePromptTemplate - 创建Prompt模板](raw/_short/api-bailian-2023-12-29-createprompttemplate-5d322a6c80396e15.md)。
- **[长期记忆](../concepts/long-term-memory.md)（旧）**：提供 `Memory`（记忆体）与 `MemoryNode`（记忆片段）两级抽象，支持结构化存储用户上下文信息，供智能体在后续调用中引用，参见[CreateMemory - 创建长期记忆体](raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)。

> **注意**：文档中多次提及“长期记忆（旧）”，表明该能力已被标记为遗留方案；新项目应优先评估平台最新记忆机制（如向量库集成），本文档未覆盖其替代方案。

## 关键参数

### 应用调用通用参数（DashScope API）
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取。 |
| `prompt` | string | 是（当未传 `messages` 时） | 单轮文本输入指令。通过 HTTP 调用时需置于 `input.prompt` 中。 |
| `messages` | array | 否（替代 `prompt`） | 多轮对话消息数组，含 `system`/`user` 角色对象；若同时传 `session_id`，则优先使用 `messages`。 |
| `session_id` | string | 否 | 对话历史标识，启用后自动加载云端存储的上下文；1 小时无请求即失效。 |
| `workspace` | string | 否（子业务空间必需） | 业务空间 ID，仅当应用部署于子业务空间或特定地域（如法兰克福、北京、新加坡等）时需显式传递，作为 Header `X-DashScope-WorkSpace`。 |
| `stream` | boolean | 否（默认 `false`） | 是否启用流式响应。推荐设为 `true`，需配合 `X-DashScope-SSE: enable` Header 使用。 |
| `incremental_output` | boolean | 否（默认 `false`） | 仅在 `stream=true` 时生效，控制是否增量返回（`true`）或全量追加（`false`）。 |

### 组件类接口共性参数
所有 Prompt 模板与长期记忆接口均需：
- `workspaceId`：业务空间 ID，路径参数，不可省略；
- `AccessKey` 签名认证（非 Bearer [Token](../concepts/token.md)），必须使用阿里云 SDK 或 OpenAPI Explorer 构造合法请求。

## 使用方式

### 1. 应用调用（DashScope API）
- **Base URL**：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（同步）或 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（OpenAI 兼容模式）。
- **认证**：使用百炼 API Key，Header 中设置 `Authorization: Bearer <your-api-key>`。
- **调用示例（HTTP 同步）**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/abc123/completion" \
    -H "Authorization: Bearer sk-xxx" \
    -H "Content-Type: application/json" \
    -d '{
          "input": {"prompt": "你好，请介绍你自己"},
          "parameters": {"stream": true, "incremental_output": true}
        }'
  ```

### 2. 组件类接口（OpenAPI）
- **Base URL**：`https://bailian.{regionId}.aliyuncs.com`（如 `bailian.cn-beijing.aliyuncs.com`），具体 region 由业务空间所在地域决定。
- **认证**：采用阿里云 AccessKey 签名（ACS3-HMAC-SHA256），**不支持** `Authorization: Bearer` 方式。强烈推荐使用 [OpenAPI Explorer](https://api.aliyun.com/) 或官方 SDK 自动生成签名。
- **典型流程**：
  1. 调用 `CreatePromptTemplate` 创建模板；
  2. 在智能体配置中引用该模板 ID；
  3. 调用 `ListPromptTemplates` 进行模板治理。

### 3. OpenAI 兼容模式（Responses API）
提供同步/异步两种调用路径：
- **同步**：适用于低延迟交互，Endpoint 为 `/responses`，支持 `input` 字符串或 `messages` 数组；
- **异步**：适用于耗时任务（如多步骤工具链），设置 `background=true` 后立即返回 `task_id`，再通过 `retrieve` 轮询结果；**注意：[异步任务](../concepts/asynchronous-task.md)不支持 `stream=true`**，详见[异步调用API参考](raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

## 限制和注意事项

- **地域限制**：所有 DashScope API 文档（包括新版智能体、工作流、Responses API）均明确标注“仅适用于华北2（北京）地域”。若应用部署在其他地域（如德国法兰克福），必须使用 `workspace` 参数并确保 Base URL 匹配对应地域的 workspace endpoint（如 `https://{workspaceId}.eu-central-1.maas.aliyuncs.com`），参见[获取APP ID和Workspace ID](raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。
  
- **凭证获取方式**：APP ID 和 Workspace ID **仅支持控制台手动复制**，不提供 API 或 CLI 查询接口。RAM 子账号需被授予 `AliyunBailianFullAccess` 权限才能访问业务空间管理页面。

- **鉴权隔离**：应用调用接口（Bearer [Token](../concepts/token.md)）与组件类接口（AccessKey 签名）**完全独立**，混用将导致 401 错误。例如，对 `CreatePromptTemplate` 接口发送 `Authorization: Bearer xxx` 将被拒绝。

- **长期记忆服务限流**：所有 Memory 相关接口（Create/Get/List 等）要求两次请求间隔 ≥1 秒，否则触发限流。生产环境需实现退避重试逻辑。

- **错误处理差异**：应用调用接口错误响应含 `request_id` 字段；组件类接口遵循阿里云 OpenAPI 标准，错误时返回 `Code` 与 `Message` 字段。统一错误码含义见[错误码](raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
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
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-33268b72d11a1cac.md)
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
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-e7dac02713c2120e.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [其他](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-1e6bc508cb390a4f.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-23a13524c8ed9f9d.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)


