# application call

`application call` 是百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持文本、图像、文件等[多模态](../concepts/multi-modal.md)输入，提供流式/增量输出、会话管理、自定义参数传递及长期记忆等功能，适用于构建对话机器人、自动化工作流、RAG 应用等场景。所有调用均需在华北2（北京）地域进行，且必须配置有效的 API Key 和应用 ID。

## 支持的模型/功能

- **应用类型**：支持新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，但不同应用类型对参数的支持存在差异（详见下文限制说明）。
- **[多模态](../concepts/multi-modal.md)能力**：
  - 图像理解：需应用内选用通义千问 VL 系列模型，并在 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 中配置 `image_list` 参数；工作流应用则需将模型节点入参设为 `imageList`。
  - 文件处理：仅智能体应用支持 `file_list`（HTTP）或 `files`（SDK），需在控制台选择“全文引用”或“切片检索”模式。
- **高级功能**：
  - [流式输出](../concepts/streaming-output.md)（`stream=true`）与增量输出（`incremental_output=true`）提升响应实时性；
  - 思考模式（`enable_thinking=true` + `has_thoughts=true`）返回 `thought` 字段，适用于深度思考模型；
  - 长期记忆（`memory_id`）仅限智能体应用；
  - RAG 检索（`rag_options`）仅限智能体应用，支持按知识库 ID（`pipeline_ids`）、文档 ID（`file_ids`）、元数据（`metadata_filter`）及标签（`tags`）过滤。

> **注意**：`flow_stream_mode`（如 `message_format_plus`）仅适用于工作流应用，新版智能体应用不支持该参数；而 `enable_thinking` 仅在 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 中定义，旧版智能体与工作流应用文档未提及此参数，实际调用时可能被忽略。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 适用场景 |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需填入 URL 路径。 | 所有调用 |
| `prompt` | string | 是（单轮） | 用户指令文本。HTTP 调用时置于 `input.prompt`。 | 新版智能体、旧版智能体（单轮） |
| `messages` | array | 是（多轮） | 消息数组，含 `system`/`user`/`assistant` 角色对象。HTTP 调用时置于 `input.messages`。 | 旧版智能体、工作流、OpenAI 兼容模式 |
| `session_id` | string | 否 | 对话历史标识，1 小时无请求自动失效。HTTP 调用时置于 `input.session_id`。 | 旧版智能体、新版智能体（单轮+`prompt`必传） |
| `workspace` | string | 否 | 子业务空间 ID，需通过 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取。HTTP 调用时通过 Header `X-DashScope-WorkSpace` 传递。 | 子业务空间下的所有应用 |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md)。HTTP 调用需 Header `X-DashScope-SSE: enable`；SDK 使用 `streamCall` 或 `stream=True`。 | 所有调用 |
| `incremental_output` | boolean | 否 | 流式下是否增量输出（推荐 `true`）。HTTP 调用时置于 `parameters.incremental_output`。 | 所有流式调用 |
| `biz_params` | object | 否 | 传递自定义变量、[插件](../concepts/plugin.md)参数等。结构为 `{ "user_prompt_params": {}, "user_defined_params": {} }`。HTTP 调用时置于 `input.biz_params`。 | 旧版智能体、工作流、OpenAI 兼容模式（通过 `extra_body`） |
| `rag_options` | object | 否 | RAG 检索配置，含 `pipeline_ids`（必填）、`file_ids`、`metadata_filter` 等。HTTP 调用时置于 `parameters.rag_options`。 | 仅新版/旧版智能体应用 |

## 使用方式

### 1. 接口地址
- **DashScope API（推荐）**：  
  `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  （适用于新版/旧版智能体、工作流；[工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md) 与 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 均采用此 endpoint）
- **OpenAI 兼容模式（Responses API）**：  
  `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  （同步调用）或启用 `background=true` 实现异步（见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）

### 2. SDK 调用示例（Python）
```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="APP_ID",
    prompt="你是谁？",
    stream=True,
    incremental_output=True
)
```

### 3. HTTP 调用示例（curl）
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-SSE: enable" \
  -d '{
        "input": {"prompt": "你是谁？"},
        "parameters": {"incremental_output": true}
      }'
```

### 4. 在线调试
通过控制台 **应用卡片 → 发布 → API 调试** 页面填写参数并运行，无需编码即可验证请求结构与响应。

## 限制和注意事项

- **地域限制**：所有 API 调用仅支持华北2（北京）地域，其他地域暂不可用。
- **SDK 版本要求**：
  - Python DashScope SDK ≥ 1.24.7（支持 `file_list`/`image_list`）；
  - Java DashScope SDK ≥ 2.22.23（支持 `flow_stream_mode`）；
  - OpenAI Python SDK（兼容模式）需适配 v1.x 版本。
- **参数冲突规则**：
  - 若同时传入 `session_id` 和 `messages`，系统优先使用 `messages`，忽略 `session_id` 和 `prompt`；
  - `model_id` 参数优先级高于控制台配置，但仅在新版智能体应用中明确支持。
- **异步限制**：OpenAI 兼容模式的异步调用（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true` 会被忽略），且暂不支持基于 `pre_response_id` 或 `conversation_id` 的上下文自动恢复。
- **安全建议**：生产环境严禁硬编码 `DASHSCOPE_API_KEY`，务必通过环境变量或密钥管理服务注入。
- **调试提示**：若返回 `400 Bad Request`，请检查 `prompt`/`messages` 是否缺失、`pipeline_ids` 是否超出 5 个上限、或 `metadata_filter` 键值类型是否匹配（字符串/数组）。

## 来源文档

- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)


