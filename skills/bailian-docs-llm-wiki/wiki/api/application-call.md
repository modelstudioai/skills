# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过标准化 API 接口调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者无需关心底层模型调度与编排细节，只需传入业务输入、会话上下文及可选的运行时参数，即可获得结构化响应。该能力同时支持 DashScope 原生协议与 OpenAI 兼容模式，兼顾功能完整性与生态迁移便利性。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）和工作流（Workflow）三类应用，对应不同 API 文档路径与参数集 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 和 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **多模态能力**：支持图像（`image_list` / `input_image`）与文件（`file_list` / `input_file`）输入，需在应用中选用通义千问 VL 系列模型并完成相应配置 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **[长期记忆](../concepts/long-term-memory.md)与 RAG**：智能体应用支持通过 `memory_id` 启用[长期记忆](../concepts/long-term-memory.md)；同时支持 `rag_options` 配置知识库检索策略，包括 `pipeline_ids`、`metadata_filter` 等细粒度控制。
- **OpenAI 兼容模式**：提供 Responses API（含同步与异步），复用 OpenAI SDK 接口风格，`base_url` 格式为 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/`，适用于快速集成现有生态工具。

> **注意**：新版智能体 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API、Responses API 同样标注相同地域限制，但[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)文档指出 Workspace ID 在德国（法兰克福）、新加坡等多地为必需字段——这表明实际服务已支持多地域，API 文档的地域说明存在滞后，应以控制台可用地域为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 所属协议 |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需嵌入 URL 路径。 | 全部 |
| `prompt` | string | 是（单轮） | 用户指令文本，用于单轮对话。DashScope API 中置于 `input.prompt`。 | DashScope |
| `input` | string/array | 是（单轮/多轮） | OpenAI 模式核心输入：字符串（单轮）或消息数组（多轮），支持 `input_text`/`input_image`/`input_file` 类型。 | Responses |
| `messages` | array | 否（替代 prompt+session_id） | 多轮对话上下文数组，含 `system`/`user`/`assistant` 角色消息。DashScope 工作流/旧版 Agent 支持。 | DashScope |
| `session_id` | string | 否 | 对话历史标识，启用后自动加载云端历史（1 小时有效期）。DashScope 单轮场景常用。 | DashScope |
| `workspace` | string | 否（子空间必需） | 业务空间 ID，调用子业务空间应用或特定地域模型时必须传入，HTTP 请求头为 `X-DashScope-WorkSpace`。 | 全部 |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)。DashScope 需设 `X-DashScope-SSE: enable`；Responses 直接传 `stream=true`。 | 全部 |
| `incremental_output` | boolean | 否（仅 stream=true 时生效） | 流式增量输出开关（`true` 返回 delta，`false` 返回全量前缀）。DashScope 特有参数。 | DashScope |
| `flow_stream_mode` | string | 否（仅工作流） | 工作流流式模式：`message_format_plus`（推荐）、`message_format`、`full_thoughts`（不推荐新业务）。 | DashScope |
| `biz_params` | object | 否 | 传递自定义变量、插件参数等，如 `{"city": "杭州"}` 或 `{"user_prompt_params": {...}}`。Responses 通过 `extra_body` 透传。 | 全部 |
| `background` | boolean | 否（仅 Responses 异步） | 设为 `true` 启动[异步任务](../concepts/asynchronous-task.md)，立即返回 `task_id`，后续通过 `retrieve` 查询结果。 | Responses |

## 使用方式

### 1. 凭证准备
- 获取 `APP_ID`：访问 [应用管理](https://bailian.console.aliyun.com/#/app-center)，复制目标应用卡片上的 ID。
- 获取 `Workspace ID`（如需）：登录控制台 → 右上角用户图标 → 查看“业务空间ID”；或主账号进入 [业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 页面复制。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- 获取 `DASHSCOPE_API_KEY`：通过 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建并配置至环境变量。

### 2. 调用入口
- **DashScope 原生 API**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  Header：`Authorization: Bearer ${DASHSCOPE_API_KEY}`，子空间需加 `X-DashScope-WorkSpace: ${WORKSPACE_ID}`  
  SDK：Python/Java 官方 SDK 提供 `client.apps.completions.create()` 等封装方法。

- **OpenAI 兼容 Responses API**  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上 endpoint，请求体中 `background=true`  
  SDK：使用 `openai` 或 `async-openai` 包，`base_url` 指向兼容模式地址。

### 3. 代码示例（Python）
```python
# DashScope 单轮调用
from dashscope import Client
client = Client(api_key=os.getenv("DASHSCOPE_API_KEY"))
response = client.apps.completions.create(app_id="xxx", prompt="你是谁？")

# Responses 同步多轮调用
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/api/v2/apps/agent/xxx/comptible-mode/v1/"
)
response = client.responses.create(input=[{"role":"user","content":"你好"}])

# Responses 异步调用
response = client.responses.create(input="长任务", background=True)
task_id = response.id
# 后续调用 client.responses.retrieve(task_id) 轮询结果
```

## 限制和注意事项

- **地域限制**：所有文档均标注“仅适用于华北2（北京）地域”，但实际服务已扩展至德国（法兰克福）、新加坡等多地，`Workspace ID` 在这些地域为强制参数，开发者需根据部署地域选择对应 Base URL 和 Workspace 配置。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `enable_thinking` 需 Java SDK ≥ 2.20.0，`flow_stream_mode` 需 Java SDK ≥ 2.22.23，`file_list` 需 Python SDK ≥ 2.0.1 —— 低版本将导致参数被忽略或报错。
- **异步与流式互斥**：Responses API 明确禁止 `background=true` 与 `stream=true` 同时设置，否则请求将被拒绝；DashScope API 的流式需额外 Header，无此限制。
- **参数作用域差异**：`messages` 与 `prompt`/`session_id` 互斥（DashScope）；`biz_params` 在 DashScope 中置于 `input`，而在 Responses 中需通过 `extra_body` 透传；`image_list` 仅智能体应用支持文件输入，工作流需显式配置 `imageList` 模型入参变量。
- **调试建议**：优先使用控制台“发布 → API 调试”功能验证参数组合；生产环境务必避免硬编码 API Key，应通过环境变量或密钥管理服务注入。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


