# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或[异步调用](../concepts/asynchronous-invocation.md)已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 与 OpenAI 兼容 Responses API），覆盖单轮/多轮对话、多模态输入（文本、图像、文件）、RAG 检索、插件调用、[长期记忆](../concepts/long-term-memory.md)等场景，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，但不同 API 路径和参数支持存在差异。
- **协议支持**：
  - `DashScope API`：原生高性能接口，提供最全功能控制（如 `enable_thinking`、`flow_stream_mode`、`rag_options` 等），详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
  - `Responses API`：OpenAI 兼容模式，分为同步（`/responses`）与异步（`background=true`）两种调用方式，便于复用现有 OpenAI 生态代码，详见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 和 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **多模态能力**：支持 `image_list`（DashScope API）或 `input_image`（Responses API）进行视觉理解；支持 `file_list`（仅智能体）或 `input_file`（仅智能体）进行文档问答。
- **高级功能**：深度思考模式（需 `enable_thinking` + `has_thoughts`）、RAG 知识库检索（`rag_options`）、插件参数传递（`biz_params.user_defined_params`）、[长期记忆](../concepts/long-term-memory.md)（`memory_id`）、子画布节点流式推送（`flow_stream_mode=message_format_plus`）。

> **注意**：新版智能体应用 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体应用 API 文档同样标注“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指出 Workspace ID 在德国（法兰克福）、新加坡等多地为必需项——这表明跨地域调用实际可行，但官方 API 文档未全面覆盖，开发者需以控制台实际可用 Base URL 为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属协议 |
|--------|------|------|------|----------|
| `app_id` | string | ✓ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需填入 URL 路径。 | 全部 |
| `prompt` | string | ✓（DashScope 单轮） | 用户指令文本。DashScope API 中用于单轮对话；Responses API 中被 `input` 替代。 | DashScope |
| `input` | string/array | ✓（Responses） | 核心输入：可为字符串（单轮）或消息数组（多轮/多模态）。消息支持 `system`/`user`/`assistant` 角色及 `input_text`/`input_image`/`input_file` 类型。 | Responses |
| `session_id` | string | ✗ | 对话历史标识，1 小时无请求自动失效。仅 DashScope API 支持。 | DashScope |
| `messages` | array | ✗（DashScope 多轮） | 完整对话历史数组（含 role/content），优先级高于 `session_id` 和 `prompt`。 | DashScope |
| `stream` | boolean | ✗（默认 false） | 是否启用[流式输出](../concepts/streaming-output.md)。DashScope 需 Header `X-DashScope-SSE: enable`；Responses 直接传 `stream=true`。 | 全部 |
| `incremental_output` | boolean | ✗（DashScope 流式下） | [流式输出](../concepts/streaming-output.md)是否增量（`true`）或全量（`false`）。仅 DashScope API 支持。 | DashScope |
| `flow_stream_mode` | string | ✗（工作流专用） | 工作流流式模式：`message_format_plus`（推荐）、`message_format`、`full_thoughts`（不推荐新业务）。仅 DashScope API 支持。 | DashScope |
| `biz_params` | object | ✗ | 传递自定义参数：`user_prompt_params`（提示词变量）、`user_defined_params`（插件参数）、`user_defined_tokens`（插件鉴权）。 | 全部 |
| `rag_options` | object | ✗（智能体专用） | RAG 检索配置：`pipeline_ids`（知识库ID列表，必填）、`file_ids`、`metadata_filter` 等。仅 DashScope API 支持。 | DashScope |
| `memory_id` | string | ✗（智能体专用） | [长期记忆](../concepts/long-term-memory.md)体 ID，需在应用中开启长期记忆开关。仅 DashScope API 支持。 | DashScope |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID`：访问 [应用管理](https://bailian.console.aliyun.com/#/app-center)，复制目标应用卡片上的 ID。
- 获取 `Workspace ID`（如需）：若应用位于子业务空间，或部署在非北京地域（如新加坡、法兰克福），必须提供。通过控制台右上角用户头像 → “业务空间ID” 查看，或主账号访问 [业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 页面获取。**注意：无法通过 API 或 CLI 查询**，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

### 2. 调用入口
- **DashScope API**（推荐功能完整性）：
  - Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - SDK：Python/Java SDK 默认配置 endpoint；HTTP 调用需手动设置 `X-DashScope-WorkSpace` Header（当需要 Workspace ID 时）。
- **Responses API**（推荐生态兼容性）：
  - 同步 Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - 异步 Endpoint：同上，但请求体中 `background=true`
  - SDK：使用 OpenAI Python/Java SDK，`base_url` 设为 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/`

### 3. 示例：单轮文本调用（DashScope SDK）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
if response.status_code == 200:
    print(response.output.text)
```

### 4. 示例：多模态流式调用（Responses API）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
)
response = client.responses.create(
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "描述这张图"},
                {"type": "input_image", "image_url": "https://example.com/image.jpg"}
            ]
        }
    ],
    stream=True
)
for chunk in response:
    if hasattr(chunk, 'delta') and chunk.delta:
        print(chunk.delta, end='', flush=True)
```

## 限制和注意事项

- **地域限制**：所有文档均标注“仅适用于华北2（北京）地域”，但实际跨地域调用（如新加坡）需配合正确的 Workspace ID 和 Base URL，开发者应以控制台实际环境为准。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `incremental_output` 要求 Java SDK ≥ 2.20.0，`file_list` 要求 Python SDK ≥ 1.24.7 / Java SDK ≥ 2.21.13，`flow_stream_mode` 要求 Java SDK ≥ 2.22.23。低版本 SDK 可能静默忽略参数。
- **异步限制**：Responses API 的[异步调用](../concepts/asynchronous-invocation.md)（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true` 会被忽略），且暂不支持基于 `pre_response_id` 或 `conversation_id` 的上下文自动续接，每次请求需传完整 `input`。
- **参数冲突**：当 `messages` 与 `session_id`/`prompt` 同时存在时，DashScope API 优先使用 `messages`，`session_id` 和 `prompt` 将被忽略。
- **安全实践**：API Key **严禁硬编码**，应通过环境变量（如 `DASHSCOPE_API_KEY`）注入，并在生产环境启用 RAM 权限最小化原则（如 `AliyunBailianFullAccess`）。

## 来源文档

- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


