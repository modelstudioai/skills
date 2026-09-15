# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 与 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming-output.md)、多模态输入、[长期记忆](../concepts/long-term-memory.md)、RAG 检索等高级功能，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，但不同 API 路径和参数支持存在差异。
- **多模态能力**：支持图像（`image_list` 或 `input_image`）和文件（`file_list` 或 `input_file`）输入，需在应用中选用通义千问 VL 系列模型或配置对应文件处理方式 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **RAG 检索**：仅智能体应用支持 `rag_options` 参数，可指定知识库（`pipeline_ids`）、文档（`file_ids`）、元数据（`metadata_filter`）及标签（`tags`）进行精准检索 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **[长期记忆](../concepts/long-term-memory.md)**：仅智能体应用支持 `memory_id` 参数，启用后系统自动构建、保存并恢复用户偏好记忆 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **思考模式**：通过 `enable_thinking` 和 `has_thoughts` 组合控制是否启用并返回模型思考过程，适用于深度思考模型 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。

> **注意**：新版智能体 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API、Responses API 同样标注“仅适用于华北2（北京）地域”，但[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)文档指出 Workspace ID 在德国（法兰克福）、新加坡等多地为必需项——这表明跨地域调用能力实际存在，但官方 API 文档未全面覆盖，开发者需以控制台实际可用性为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属 API |
|--------|------|------|------|----------|
| `app_id` | string | ✓ | 应用唯一标识，从控制台应用卡片复制 | 全部 |
| `prompt` | string | ✓（DashScope） | 单轮文本输入，仅 DashScope API 使用 | DashScope（新版/旧版） |
| `input` | string/array | ✓（Responses） | 支持字符串（单轮）或消息数组（多轮/多模态），Responses API 的核心输入字段 | Responses API |
| `session_id` | string | ✗ | 对话历史标识，1 小时无请求自动失效；与 `messages` 冲突时后者优先 | DashScope（新版/旧版） |
| `messages` | array | ✗（DashScope） | 多轮对话上下文，含 `system`/`user`/`assistant` 角色消息 | DashScope（旧版）、Responses API |
| `stream` | boolean | ✗（默认 false） | 是否[流式输出](../concepts/streaming-output.md)；DashScope 需 Header `X-DashScope-SSE: enable`，Responses 直接传入 body | 全部 |
| `incremental_output` | boolean | ✗（DashScope 流式下） | 流式增量输出（true）或全量追加（false）；Responses API 无此参数，由服务端统一处理 | DashScope（新版/旧版） |
| `workspace` | string | ✗（子空间必需） | 业务空间 ID，子业务空间或特定地域（如法兰克福）调用时必须传入，通过 Header `X-DashScope-WorkSpace` 传递 | 全部 |
| `biz_params` | object | ✗ | 传递自定义变量、插件参数（`user_prompt_params`, `user_defined_params`）等，是工作流与智能体应用对接外部逻辑的关键入口 | DashScope（旧版）、Responses API（via `extra_body`） |

## 使用方式

### 1. 协议选择
- **DashScope 原生 API**：路径为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，功能最全，SDK 支持成熟，推荐新项目使用。
- **Responses API（OpenAI 兼容）**：路径为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，兼容 OpenAI SDK，适合快速迁移或复用生态工具，但部分高级参数（如 `incremental_output`）不支持。

### 2. 认证与凭证
- **API Key**：通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取，并建议配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码。
- **APP ID & Workspace ID**：必须通过控制台手动获取，不支持 API 查询 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。默认业务空间仅需 `APP ID`；子业务空间或非北京地域必须同时提供 `Workspace ID` 并设置 Header。

### 3. 典型调用示例
- **单轮文本（DashScope Python SDK）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  ```
- **多轮+图像（Responses API cURL）**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/responses" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "input": [{
            "role": "user",
            "content": [
              {"type": "input_text", "text": "这是什么？"},
              {"type": "input_image", "image_url": "https://example.com/image.jpg"}
            ]
          }]
        }'
  ```

## 限制和注意事项

- **地域限制**：所有文档均标注“仅适用于华北2（北京）地域”，但实际调用中 Workspace ID 在法兰克福等多地为必需项，开发者应以目标地域控制台的 Base URL 和 Workspace ID 获取流程为准。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `incremental_output` 要求 Java SDK ≥2.20.0，`flow_stream_mode` 要求 Java SDK ≥2.22.23，`file_list` 要求 Python SDK ≥1.24.7 —— 低版本将导致参数被忽略或报错。
- **异步与流式互斥**：Responses API 中 `background=true` 与 `stream=true` 不可同时设置，异步任务不支持[流式输出](../concepts/streaming-output.md) [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **参数冲突规则**：当 `messages` 与 `session_id`/`prompt` 同时存在时，DashScope API 优先使用 `messages`；`biz_params` 中的插件参数需与应用内配置的 `TOOL_ID` 严格一致，否则调用失败。
- **调试建议**：所有应用均支持控制台“发布 → API 调试”在线调试，可实时验证参数组合与响应结构，避免因格式错误导致 400 错误。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


