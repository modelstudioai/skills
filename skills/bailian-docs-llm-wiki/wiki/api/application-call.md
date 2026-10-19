# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的[智能体（Agent）](../concepts/agent.md)或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 与 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming.md)、多模态输入、长期记忆、RAG 检索等高级功能，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，但不同 API 文档覆盖范围不同：[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 仅适用于新版智能体；而 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 覆盖旧版智能体与工作流。
- **多模态能力**：支持图像（需选用通义千问 VL 系列模型）和文件（PDF/DOCX/MP3 等）输入，分别通过 `image_list`（DashScope API）或 `input_image`/`input_file`（Responses API）传递。
- **高级功能**：
  - [流式输出](../concepts/streaming.md)（`stream=true`）及增量模式（`incremental_output=true`）；
  - 长期记忆（`memory_id`，仅智能体应用支持）；
  - RAG 检索（`rag_options`，仅智能体应用支持）；
  - 工作流节点级流式推送（`flow_stream_mode=message_format_plus`）；
  - 思考过程输出（需同时设置 `enable_thinking=true` 和 `has_thoughts=true`）。

> **注意**：[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 明确声明“仅适用于华北2（北京）地域”，而 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 与 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 也标注了相同地域限制，但实际调用中若未显式指定 Workspace ID，在德国（法兰克福）等非北京地域可能失败——请务必参考 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 中关于 Workspace ID 必填场景的说明。

## 关键参数

| 参数名 | 类型 | 是否必选 | 说明 | 所属 API |
|--------|------|----------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台应用卡片复制。HTTP 调用时需嵌入 URL 路径。 | 全部 |
| `prompt` | string | 是（DashScope） | 单轮文本输入。DashScope API 中为顶层字段；Responses API 中需放入 `input` 字段。 | DashScope |
| `input` | string/array | 是（Responses） | Responses API 的核心输入：支持字符串（单轮）或消息数组（多轮/多模态）。 | Responses |
| `session_id` | string | 否 | 对话历史标识，1 小时无请求自动失效。仅 DashScope API 支持。 | DashScope |
| `messages` | array | 否（DashScope） | 多轮对话上下文（system/user/assistant），优先级高于 `session_id` 和 `prompt`。 | DashScope |
| `workspace` | string | 否（Header） | 子业务空间或特定地域（如法兰克福）下必需，通过 `X-DashScope-WorkSpace` Header 传递。 | 全部 |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming.md)。DashScope 默认 `false`；Responses 默认 `false`。 | 全部 |
| `background` | boolean | 否（Responses） | Responses API 专用：设为 `true` 即发起异步任务，立即返回 task_id。 | Responses |
| `biz_params` | object | 否 | 传递自定义变量、插件参数等，结构因应用配置而异。 | 全部 |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID` 和（必要时）`Workspace ID`：详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- 获取 `DASHSCOPE_API_KEY` 并配置为环境变量（推荐）或代码内传参。

### 2. 选择调用协议
- **DashScope 原生 API**（推荐用于新项目）：
  - 终端：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - SDK：使用 `Application.call()`（Python/Java）。
- **OpenAI 兼容 Responses API**（适合迁移现有 OpenAI 代码）：
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - 异步：在同步 Endpoint 请求体中添加 `"background": true`，再通过 `GET /responses/{task_id}` 查询结果。

### 3. 示例：单轮文本调用（Python）
```python
# DashScope 方式
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)

# Responses 方式（OpenAI SDK）
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
)
response = client.responses.create(input="你是谁？")
```

## 限制和注意事项

- **地域限制**：所有当前文档均明确标注“仅适用于华北2（北京）地域”。在德国（法兰克福）、新加坡等其他地域调用时，必须显式传入 `Workspace ID`，且 Base URL 中的地域路径需匹配（参见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `incremental_output` 要求 Python SDK ≥1.24.7、Java SDK ≥2.21.13；`flow_stream_mode` 要求 Java SDK ≥2.22.23。低版本将忽略参数或报错。
- **异步限制**：Responses API 的异步模式（`background=true`）不支持 `stream=true`，二者互斥。
- **参数冲突**：当同时传入 `messages` 和 `session_id` 时，DashScope API 会**优先使用 `messages`**，忽略 `session_id` 和 `prompt`（见 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）。
- **权限要求**：查询 Workspace ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看其已加入的业务空间（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)


