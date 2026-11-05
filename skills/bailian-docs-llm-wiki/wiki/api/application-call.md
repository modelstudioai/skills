# application call

`application call` 是百炼平台提供的核心能力，用于通过 API 同步或[异步调用](../concepts/asynchronous-invocation.md)已发布的智能体（Agent）或工作流（Workflow）应用。它支持文本、图像、文件等多模态输入，提供流式/增量输出、[长期记忆](../concepts/long-term-memory.md)、RAG 检索、插件调用等高级功能，并兼容 DashScope 原生协议与 OpenAI 兼容模式，适用于实时交互与长耗时任务两类场景。

## 支持的模型/功能

- **应用类型**：支持新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，但不同应用类型对参数的支持存在差异（如 `memory_id` 仅限智能体应用，`flow_stream_mode` 仅限工作流应用）。
- **多模态能力**：  
  - 图像理解：需在应用中选用[通义千问VL系列模型](raw/model-user-guide/model-experience/text-generation-model/vision.md)，并通过 `image_list`（DashScope API）或 `input_image`（Responses API）传入图片 URL 或 Data URL；  
  - 文件问答：仅智能体应用支持，需配置文件处理方式为“全文引用”或“切片检索”，并通过 `file_list`（DashScope API）或 `input_file`（Responses API）传入文件 URL。
- **高级功能**：  
  - [长期记忆](../concepts/long-term-memory.md)：通过 `memory_id` 参数启用，需在应用中开启[长期记忆](../concepts/long-term-memory.md)开关并发布；  
  - RAG 检索：通过 `rag_options`（仅智能体应用）指定知识库 ID（`pipeline_ids`）、文档 ID（`file_ids`）及元数据过滤条件；  
  - 插件调用：通过 `biz_params.user_defined_params`（DashScope API）或 `extra_body.biz_params`（Responses API）传递插件参数；  
  - 思考过程：设置 `enable_thinking=true` 且 `has_thoughts=true` 可在 `thought` 字段获取模型思考链（详见 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)）。

> **注意**：`messages` 参数在 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 中明确支持多轮对话上下文，但在 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 中未提及该参数——实际使用中应以应用类型为准：新版智能体推荐使用 `session_id` 管理会话，旧版智能体/工作流可直接使用 `messages` 实现无状态多轮。

## 关键参数

| 参数名 | 类型 | 是否必选 | 说明 | 所属协议 |
|--------|------|----------|------|----------|
| `app_id` | string | 必选 | 应用唯一标识，从[应用管理](https://bailian.console.aliyun.com/#/app-center)获取。HTTP 调用时需填入 URL 路径；SDK 调用时作为方法参数。 | 两者均支持 |
| `prompt` | string | 必选（单轮） | 用户输入指令。仅 DashScope API 使用；Responses API 中由 `input` 字段替代。 | DashScope API |
| `input` | string/array | 必选（Responses） | 单轮字符串或消息数组（含 `system`/`user`/`assistant` 角色）。支持多模态内容（文本、图片、文件）。 | Responses API |
| `session_id` | string | 可选 | 对话历史标识，1 小时无请求后自动失效。仅 DashScope API 支持。 | DashScope API |
| `messages` | array | 可选 | 完整对话历史数组，优先级高于 `session_id` 和 `prompt`。仅 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 明确支持。 | DashScope API（旧版） |
| `stream` | boolean | 可选 | 是否[流式输出](../concepts/streaming-output.md)。DashScope API 需配合 `X-DashScope-SSE: enable` Header；Responses API 直接设为 `true`。 | 两者均支持 |
| `incremental_output` | boolean | 可选 | 流式下是否增量输出（后续 chunk 不重复前序内容）。DashScope API 中放入 `parameters`；Responses API 不支持此参数。 | DashScope API |
| `flow_stream_mode` | string | 可选（工作流） | 工作流流式模式：`message_format_plus`（推荐）、`message_format`、`full_thoughts`（不推荐新业务）。仅 DashScope API 支持。 | DashScope API（工作流） |
| `workspace` | string | 可选 | 子业务空间 ID，调用子空间应用时必需。DashScope API 通过 `X-DashScope-WorkSpace` Header 传递；Responses API 需配置在 `base_url` 中。 | 两者均支持 |

## 使用方式

- **协议选择**：  
  - **DashScope API**（推荐用于全功能场景）：Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，支持全部参数与高级功能；  
  - **Responses API**（推荐用于 OpenAI 生态迁移）：分为同步（`/responses`）与异步（`background=true`）两种模式，Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，语法更简洁但部分参数（如 `incremental_output`）不支持。

- **调用示例**：  
  - **DashScope SDK（Python）**：  
    ```python
    response = client.apps.completions.create(
        app_id='APP_ID',
        prompt='你是谁？',
        stream=True,
        parameters={'enable_thinking': True, 'has_thoughts': True}
    )
    ```  
  - **Responses API（OpenAI SDK）**：  
    ```python
    client = OpenAI(base_url=f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/')
    response = client.responses.create(input="你是谁？", stream=True)
    ```  
  - **HTTP（curl）**：  
    ```bash
    curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion" \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"input": {"prompt": "你是谁？"}, "parameters": {}}'
    ```

- **调试路径**：所有应用均支持控制台在线调试——进入**应用卡片 → 发布 → API 调试**，填写参数后运行即可验证。

## 限制和注意事项

- **地域限制**：所有文档均明确标注“仅适用于华北2（北京）地域”，其他地域暂不支持（见 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)、[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)、[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)）。
- **SDK 版本要求**：  
  - DashScope Python SDK ≥ 2.0.1（`file_list`/`messages`）、≥ 2.20.0（`enable_thinking`）；  
  - DashScope Java SDK ≥ 2.17.0（`messages`）、≥ 2.22.23（`flow_stream_mode`）；  
  - Responses API 需使用 OpenAI SDK（非 DashScope SDK）。
- **异步限制**：[异步调用](../concepts/asynchronous-invocation.md)（`background=true`）不支持[流式输出](../concepts/streaming-output.md)（`stream=true`），且需自行轮询 `retrieve` 接口获取结果（详见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。
- **参数冲突**：当同时传入 `session_id` 和 `messages` 时，DashScope API 以 `messages` 为准，忽略会话历史（见 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）；而新版智能体 API 未定义 `messages`，若误用将导致参数解析失败。

## 来源文档

- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)


