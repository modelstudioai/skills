# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 和 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming.md)、多模态输入、[长期记忆](../concepts/memory.md)、RAG 检索等高级功能，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，但不同 API 路径和参数支持存在差异。
- **多模态能力**：支持图像（`image_list` / `input_image`）和文件（`file_list` / `input_file`）输入，需在应用中选用通义千问 VL 系列模型或配置对应文件处理方式 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。
- **RAG 检索**：仅智能体应用支持 `rag_options` 参数，可指定知识库（`pipeline_ids`）、文档（`file_ids`）、元数据（`metadata_filter`）及标签（`tags`）进行精准检索 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **[长期记忆](../concepts/memory.md)**：仅智能体应用支持 `memory_id` 参数，用于启用用户级[长期记忆](../concepts/memory.md)体 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **思考模式**：通过 `enable_thinking` 和 `has_thoughts` 控制是否启用并返回模型思考过程，适用于深度思考模型 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。

> **注意**：`flow_stream_mode`（如 `message_format_plus`）仅对工作流应用有效，且要求在控制台结束节点或流程输出节点开启流式开关；而 `incremental_output` 是 DashScope 原生 API 的通用流式增量控制参数，二者作用域和语义不同，不可混用。

## 关键参数

| 参数名 | 类型 | 是否必选 | 说明 | 所属 API |
|--------|------|----------|------|-----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取 | 全部 |
| `prompt` | string | 是（DashScope 单轮） | 用户指令文本 | DashScope 原生 API |
| `input` | string/array | 是（Responses API） | 单轮字符串或符合 OpenAI 格式的 `messages` 数组（含 `system`/`user`/`assistant`） | Responses API |
| `session_id` | string | 否 | 对话会话 ID，用于恢复历史上下文（1 小时内有效） | DashScope 原生 API |
| `messages` | array | 否（DashScope 多轮） | 替代 `prompt` + `session_id` 的显式多轮对话数组 | DashScope 原生 API |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming.md)（`true` 推荐） | 全部 |
| `workspace` | string | 否（子业务空间必需） | 业务空间 ID，调用子业务空间或特定地域（如法兰克福、北京、新加坡等）应用时必须传入 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) | DashScope 原生 API（Header） |
| `background` | boolean | 否（Responses 异步） | 设为 `true` 启用异步调用，立即返回任务 ID | Responses API |
| `biz_params` | object | 否 | 传递自定义变量、插件参数（`user_prompt_params`, `user_defined_params` 等） | DashScope & Responses API |

## 使用方式

### 1. 协议选择
- **DashScope 原生 API**：路径为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，功能最全，推荐新项目使用。
- **Responses API（OpenAI 兼容）**：路径为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，便于复用 OpenAI 生态代码，分同步与异步两种模式 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

### 2. 认证与凭证
- 必须配置 `DASHSCOPE_API_KEY`（通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取）。
- 若应用位于**子业务空间**，请求 Header 中必须包含 `X-DashScope-WorkSpace: {WORKSPACE_ID}`；若为默认业务空间，则无需该 Header [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

### 3. 示例调用（Python）
```python
# DashScope SDK 调用（新版智能体）
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    stream=True,
    incremental_output=True
)

# Responses API 同步调用（OpenAI SDK）
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
)
response = client.responses.create(input="你是谁？", stream=True)
```

## 限制和注意事项

- **地域限制**：所有文档均明确标注“本文档仅适用于华北2（北京）地域”，其他地域（如德国法兰克福、中国香港）虽支持调用，但需确认 `Workspace ID` 是否已正确嵌入 Base URL 或 Header，且部分功能（如 `flow_stream_mode`）可能未全量开放。
- **SDK 版本要求**：关键参数依赖特定 SDK 版本，例如 `incremental_output` 要求 Python SDK ≥1.24.7、Java SDK ≥2.21.13；`enable_thinking` 要求 Java SDK ≥2.20.0 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。
- **异步限制**：Responses API 的异步模式（`background=true`）不支持[流式输出](../concepts/streaming.md)（`stream=true` 会被忽略），且暂不支持基于 `pre_response_id` 或 `conversation_id` 的上下文自动恢复，需每次传入完整 `messages` [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **参数冲突**：当同时传入 `session_id` 和 `messages` 时，DashScope 原生 API 优先使用 `messages` 内容，忽略 `session_id` 和 `prompt` [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **权限约束**：`Workspace ID` 仅主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号可通过[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面查询，普通子账号只能查看当前登录空间 ID [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


