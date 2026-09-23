# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API（包括 DashScope 原生接口和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者无需自行部署模型与编排逻辑，只需传入业务输入、凭证及可选上下文，即可获得结构化或流式响应。该机制统一了应用层抽象，支持文本、图像、文件、多轮对话及异步长任务等多种调用模式。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，对应不同 API 文档路径：[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)、[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **多模态能力**：当应用配置为通义千问 VL 系列模型时，可通过 `image_list`（DashScope API）或 `input_image`（Responses API）传入图像 URL 或 Data URL；文件输入（如 PDF、MP3）仅限智能体应用，通过 `file_list` 或 `input_file` 传递。
- **[长期记忆](../concepts/memory.md)与 RAG**：智能体应用支持 `memory_id` 参数启用[长期记忆](../concepts/memory.md)；同时支持 `rag_options` 配置知识库检索（需指定 `pipeline_ids`），详见 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **OpenAI 兼容模式**：提供 Responses API（同步/异步），复用 OpenAI SDK 和请求格式，适用于快速迁移现有生态工具。

> **注意**：新版智能体 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API 同样标注“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指出 Workspace ID 在德国（法兰克福）、新加坡等多地为必需项。这表明地域限制可能已随服务演进发生变化，实际调用前请以控制台可用地域和当前 API Endpoint 为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属接口 |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需嵌入 URL 路径。 | 全部 |
| `prompt` | string | 是（DashScope） | 单轮文本指令，用于指导模型生成回复。 | DashScope API |
| `input` | string/array | 是（Responses） | 替代 `prompt` 的通用输入字段：支持字符串（单轮）或消息数组（多轮/多模态）。 | Responses API |
| `session_id` | string | 否 | 对话历史标识，启用后自动加载云端会话上下文（1 小时失效）。 | DashScope API |
| `messages` | array | 否（DashScope） | 多轮对话消息数组（含 `system`/`user`/`assistant` 角色），优先级高于 `session_id`。 | DashScope API |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)（默认 `false`）。流式模式下需按 chunk 解析响应。 | 全部 |
| `incremental_output` | boolean | 否 | 仅 DashScope 流式有效：`true` 表示增量 delta（推荐），`false` 表示全量追加。 | DashScope API |
| `workspace` | string | 否 | 子业务空间 ID，调用子空间应用或特定地域模型时必需，通过 Header `X-DashScope-WorkSpace` 传递。 | DashScope API |
| `background` | boolean | 否 | 仅 Responses API：设为 `true` 启动异步任务，立即返回 `task_id`。 | Responses API |
| `biz_params` | object | 否 | 传递自定义变量、插件参数或用户鉴权信息（如 `user_prompt_params`, `user_defined_params`）。 | 全部 |

## 使用方式

### 1. 凭证准备
- 获取 `APP_ID`：在[应用管理](https://bailian.console.aliyun.com/#/app-center)列表中复制目标应用卡片上的 ID。
- 获取 `Workspace ID`（如需）：登录控制台 → 右上角用户图标 → 查看“业务空间ID”（当前空间）或进入[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)（主账号/超级管理员权限）。详情见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- 获取 `API Key`：通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建并配置至环境变量 `DASHSCOPE_API_KEY`。

### 2. 接口选择与调用
- **DashScope 原生 API**（推荐高阶控制）：
  - Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - 支持 `parameters`（如 `enable_thinking`, `flow_stream_mode`）和 `input`（含 `prompt`, `messages`, `image_list`）对象。
  - SDK 示例（Python）：
    ```python
    from dashscope import Application
    response = Application.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id="APP_ID",
        prompt="你是谁？"
    )
    ```

- **Responses API（OpenAI 兼容）**（推荐快速集成）：
  - Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - 同步调用：`background=False`（默认），阻塞等待结果。
  - 异步调用：`background=True`，立即返回 `task_id`，后续通过 `GET /responses/{task_id}` 查询状态。详细流程见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
  - SDK 示例（Python）：
    ```python
    from openai import OpenAI
    client = OpenAI(base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/APP_ID/compatible-mode/v1/")
    response = client.responses.create(input="你好")
    ```

### 3. 流式与[异步处理](../concepts/asynchronous-processing.md)
- **[流式输出](../concepts/streaming-output.md)**：设置 `stream=True`，逐 chunk 解析（如 Python 中遍历 `response` 迭代器）。工作流应用需在控制台节点开启“[流式输出](../concepts/streaming-output.md)”开关。
- **异步任务**：`background=True` 后，需轮询 `retrieve` 接口直至状态为 `completed`/`failed`/`cancelled`。注意：异步模式不支持 `stream=True`。

## 限制和注意事项

- **地域限制**：所有文档均强调“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 明确指出 Workspace ID 在法兰克福、新加坡等多地为必需项。> **注意**：此矛盾表明服务地域支持范围可能已扩展，开发者应以控制台实际可用地域和最新 API 文档为准，避免硬编码地域假设。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `incremental_output` 要求 Java SDK ≥ 2.20.0，`flow_stream_mode` 要求 Java SDK ≥ 2.22.23。低版本可能导致参数被忽略。
- **参数冲突规则**：当 `messages` 与 `session_id` 同时存在时，DashScope API 优先使用 `messages` 内容，忽略 `session_id`；`model_id` 参数优先级高于控制台配置。
- **异步限制**：异步调用不支持流式输出（`stream=true` 无效），且暂不支持基于 `pre_response_id` 的上下文续写，每次请求需传递完整 `input`。
- **安全实践**：禁止在代码中硬编码 `API Key`，务必通过环境变量（如 `DASHSCOPE_API_KEY`）注入。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


