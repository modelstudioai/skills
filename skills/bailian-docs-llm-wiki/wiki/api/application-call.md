# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者无需自行部署模型与编排逻辑，只需传入输入内容、会话上下文及可选的业务参数，即可获得结构化响应。该能力支持 DashScope 原生协议与 OpenAI 兼容模式两种调用路径，适配不同技术栈与集成需求。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）和工作流（Workflow）三类应用，对应不同 API 接口与参数集。
- **模型能力**：底层可调用通义千问系列（Qwen）、深度思考模型（Deep Thinking）、千问 VL（多模态视觉理解）等，具体取决于应用配置；API 调用时可通过 `model_id` 参数覆盖控制台默认模型 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。
- **多模态输入**：支持图像（URL 或 Data URL）、音频、视频及文档（PDF/DOCX/TXT 等）输入，需在应用中启用对应模型与文件处理方式（如“全文引用”或“切片检索”）[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **[长期记忆](../concepts/long-term-memory.md)与 RAG**：智能体应用支持通过 `memory_id` 激活[长期记忆](../concepts/long-term-memory.md)，以及通过 `rag_options` 指定知识库、文档 ID 和元数据过滤条件进行精准检索 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。

> **注意**：新版智能体 API 与工作流/旧版智能体 API 的参数命名、结构和语义存在差异（如 `messages` 在后者中为顶层字段，在 Responses API 中嵌套于 `input`），且 SDK 版本要求不同（例如 Java SDK 对 `flow_stream_mode` 要求 ≥2.22.23）。开发者需严格依据所调用的应用类型选择对应文档，不可混用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 所属接口 |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取 | 全部 |
| `prompt` | string | 是（DashScope） | 单轮文本输入指令 | [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)、[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) |
| `input` | string/array/object | 是（Responses） | 支持字符串（单轮）或消息数组（多轮/多模态），`content` 可含 `input_text`/`input_image`/`input_file` | [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) |
| `session_id` | string | 否 | 用于恢复对话历史，1 小时无请求后失效；与 `messages` 冲突时优先使用 `messages` | DashScope 接口 |
| `messages` | array | 否（DashScope） | 多轮对话上下文，含 `system`/`user`/`assistant` 角色消息 | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) |
| `workspace` | string | 否 | 子业务空间 ID，仅当应用位于子空间或特定地域（如法兰克福、北京、新加坡等）时必需，通过 Header `X-DashScope-WorkSpace` 传递 | 全部 |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)；Responses API 中设为 `true` 即开启 SSE 流，DashScope 中需额外指定 Header `X-DashScope-SSE: enable` | 全部 |
| `incremental_output` | boolean | 否 | 仅流式下生效，控制是否增量返回（`true`）或全量追加（`false`） | DashScope 接口 |
| `flow_stream_mode` | string | 否（工作流） | 工作流专用流式模式，推荐 `message_format_plus`；`full_thoughts` 已不推荐新业务使用 | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) |
| `biz_params` | object | 否 | 传递自定义变量、插件参数或用户鉴权信息，结构依应用配置而定 | DashScope 与 Responses API 均支持 |

## 使用方式

### 1. 准备凭证
- 获取 `APP ID` 和（如需）`Workspace ID`：通过百炼控制台手动复制，[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 明确指出“目前只能通过控制台手动获取，不支持通过 API 或 CLI 查询”。
- 获取 `DASHSCOPE_API_KEY`：在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建并配置至环境变量。

### 2. 选择调用路径
- **DashScope 原生 API**（推荐用于高性能、全功能场景）：
  - 终端：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - SDK：Python/Java 客户端直接调用 `client.apps.completions.create()` 或 `Application.call()`。
- **OpenAI 兼容 Responses API**（推荐用于快速迁移 OpenAI 生态项目）：
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - 异步：在同步请求体中添加 `"background": true`，立即返回 `task_id`，再通过 `GET /responses/{task_id}` 轮询结果 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

### 3. 构造请求
- **HTTP 示例（DashScope 同步）**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/your-app-id/completion" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "X-DashScope-WorkSpace: your-workspace-id" \
    -H "Content-Type: application/json" \
    -d '{
      "input": {"prompt": "你好"},
      "parameters": {"stream": true, "incremental_output": true}
    }'
  ```
- **SDK 示例（Responses 同步流式）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/"
  )
  stream = client.responses.create(input=[{"role":"user","content":"你是谁？"}], stream=True)
  for chunk in stream:
      if hasattr(chunk, 'delta') and chunk.delta:
          print(chunk.delta, end='', flush=True)
  ```

## 限制和注意事项

- **地域限制**：所有文档均明确标注“本文档仅适用于华北2（北京）地域”，其他地域（如德国法兰克福、中国香港）调用需确认 Workspace ID 是否已正确拼入 Base URL，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本强依赖**：关键功能需满足最低 SDK 版本，例如 `flow_stream_mode` 要求 Java SDK ≥2.22.23，`image_list` 要求 Python SDK ≥2.0.1；版本不匹配将导致参数被忽略或报错。
- **异步与流式互斥**：Responses API 中 `background=true` 与 `stream=true` 不可同时设置，否则请求将失败 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **会话状态管理**：`session_id` 仅维持 1 小时活跃期，超时后需新建会话；`messages` 参数虽可替代 `session_id` 实现多轮，但需客户端自行维护完整历史并每次全量提交。
- **权限边界**：RAM 子账号默认无法查看全部业务空间，仅能访问已加入的空间；查询所有 Workspace ID 需主账号或具备 `AliyunBailianFullAccess` 权限的超级管理员 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


