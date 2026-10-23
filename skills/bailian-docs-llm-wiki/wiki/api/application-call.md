# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 和 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming-output.md)、多模态输入、[长期记忆](../concepts/long-term-memory.md)、RAG 检索等高级功能，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）和工作流（Workflow）三类应用，但不同 API 路径和参数支持存在差异。
- **协议支持**：
  - `DashScope API`：原生协议，功能最全，推荐用于新项目开发 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)；
  - `Responses API`：OpenAI 兼容协议，分为同步（`/responses`）和异步（`background=true`）两种模式，便于复用现有 OpenAI 生态代码 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **多模态能力**：支持图像（`image_list` / `input_image`）和文件（`file_list` / `input_file`）输入，需在应用中选用通义千问 VL 系列模型或配置对应文件处理方式。
- **高级功能**：
  - [流式输出](../concepts/streaming-output.md)（`stream=true`）与增量输出（`incremental_output=true`）；
  - 多轮对话（`messages` 数组）与历史会话管理（`session_id`）；
  - [长期记忆](../concepts/long-term-memory.md)（`memory_id`，仅智能体应用）；
  - RAG 检索（`rag_options`，仅智能体应用）；
  - 插件调用与自定义参数传递（`biz_params`）。

> **注意**：新版智能体应用 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体应用 API 同样标注“仅适用于华北2（北京）地域”；但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指出，Workspace ID 在德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）等多地均需使用。这表明跨地域调用能力实际存在，但部分 API 文档未及时更新地域兼容性说明。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属协议 |
|--------|------|------|------|----------|
| `app_id` | string | ✅ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需嵌入 URL 路径。 | DashScope & Responses |
| `prompt` | string | ✅（DashScope 单轮） | 用户指令文本。DashScope API 中为必填（单轮场景）；Responses API 中由 `input` 字段替代。 | DashScope |
| `input` | string/array | ✅（Responses） | 核心输入：可为字符串（单轮）或 `messages` 数组（多轮/多模态）。`messages` 内支持 `input_text`/`input_image`/`input_file` 类型。 | Responses |
| `session_id` | string | ❌（可选） | 会话标识，用于恢复云端存储的历史对话。1 小时无请求自动失效。仅 DashScope API 支持。 | DashScope |
| `messages` | array | ❌（可选） | 完整对话历史数组，含 `system`/`user`/`assistant` 角色消息。当存在时，优先级高于 `prompt` 和 `session_id`。 | DashScope & Responses |
| `workspace` | string | ❌（按需） | 业务空间 ID，调用子业务空间或特定地域（如法兰克福、东京）应用时必需。HTTP 调用需通过 `X-DashScope-WorkSpace` Header 传递。 | DashScope |
| `stream` | boolean | ❌（默认 false） | 是否启用[流式输出](../concepts/streaming-output.md)。DashScope 默认 `false`；Responses 默认 `false`，且异步模式下不支持。 | 两者均支持 |
| `incremental_output` | boolean | ❌（仅 DashScope 流式下有效） | 流式输出时是否启用增量 delta（true）而非全量快照（false）。 | DashScope |
| `biz_params` | object | ❌（可选） | 传递自定义变量、插件参数、用户鉴权信息（`user_defined_params`, `user_defined_tokens`）等。结构复杂，需与应用内配置严格一致。 | DashScope & Responses（via `extra_body`） |
| `rag_options` | object | ❌（仅智能体） | 控制知识库检索行为，含 `pipeline_ids`（必填）、`file_ids`、`metadata_filter` 等子字段。 | DashScope |

## 使用方式

### 1. 准备工作
- 在控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 创建并发布目标应用，获取 `APP ID`；
- 通过 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 获取 `DASHSCOPE_API_KEY`，并配置至环境变量（推荐）；
- 如需跨业务空间调用，按 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 指南获取 `Workspace ID`。

### 2. 调用路径选择
- **追求功能完整性与性能**：使用 DashScope API  
  Endpoint: `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
- **快速迁移 OpenAI 项目**：使用 Responses API  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上 endpoint，请求体中设置 `"background": true`

### 3. 代码示例（Python）
```python
# DashScope SDK（推荐）
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    stream=True,
    incremental_output=True
)

# Responses API（OpenAI SDK）
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
)
response = client.responses.create(
    input=[{"role": "user", "content": "你是谁？"}],
    stream=True
)
```

## 限制和注意事项

- **地域限制**：所有文档均强调“仅适用于华北2（北京）地域”，但实际支持包括德国（法兰克福）、新加坡、中国香港、日本（东京）等多地，调用前请确认所用 `Base URL` 与目标地域匹配 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如：
  - `enable_thinking` 要求 Java SDK ≥ 2.20.0；
  - `flow_stream_mode` 要求 Java SDK ≥ 2.22.23；
  - `file_list`/`image_list` 要求 Python SDK ≥ 1.24.7 / Java SDK ≥ 2.21.13。
- **异步模式约束**：Responses API 的异步调用（`background=true`）**不支持流式输出**（`stream=true` 会被忽略），且需自行实现轮询逻辑获取结果。
- **参数冲突规则**：当 `messages` 与 `prompt` + `session_id` 同时存在时，DashScope API 以 `messages` 为准，忽略后两者；`biz_params` 中的插件参数必须与应用内已关联的插件 ID 和字段名完全一致，否则调用失败。
- **凭证获取方式**：`APP ID` 和 `Workspace ID` **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口，自动化部署需预先配置。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


