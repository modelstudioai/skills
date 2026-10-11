# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套遵循 OpenAI REST API 规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/responses` 等）的标准化模型调用通道。它允许开发者复用现有 OpenAI SDK（Python/Node.js/Java/Go/C#）或 HTTP 客户端代码，仅需替换 `base_url` 和 `api_key` 即可快速接入百炼的千问系列及第三方模型，无需修改业务逻辑。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与原型验证**：已有 OpenAI 技术栈的团队可零改造接入，例如将 `openai.OpenAI(base_url="https://api.openai.com/v1")` 替换为百炼兼容地址，5 分钟完成模型切换。
- **多模态应用开发**：通过 `/v1/chat/completions` 接口，传入含 `image_url` 或 `input_image` 的 `messages` 数组，即可调用 `qwen3-vl-plus`、`QVQ` 等视觉大模型；注意 `Qwen-Audio` 不支持该协议，须改用 DashScope 原生接口。
- **智能体（Agent）构建**：优先选用 `/v1/responses` 接口（OpenAI 兼容 Responses API），其原生支持联网搜索、网页抓取、代码解释器等工具链，并可通过 `previous_response_id` 自动维护上下文，比基础 Chat Completions 更适合复杂 Agent 场景。
- **向量检索与嵌入服务**：调用 `/v1/embeddings` 接口，支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型，兼容 OpenAI 的 `input`（字符串或字符串数组）、`dimensions`、`encoding_format` 等参数，无缝集成 RAG 流程。
- **批量与异步任务**：使用 `/v1/batch`（需显式配置超时）或 `/v1/responses` 的 `background=true` 模式，提交长耗时任务（如报告生成、文档分析），立即返回 `task_id`，后续轮询获取结果。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | **必需**，必须使用业务空间专属域名（推荐格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`）；旧域名 `dashscope.aliyuncs.com/compatible-mode/v1` 仍可用但性能较低。 | `{WorkspaceId}` 需从控制台「业务空间详情」页获取；地域（如 `cn-beijing`）必须与 API Key 所属地域一致。 |
| `api_key` | **必需**，即 `DASHSCOPE_API_KEY`，严格按地域隔离，不可跨地域复用。 | 强烈建议设为环境变量，禁止硬编码；北京 Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key`。 |
| `model` | **必需**，模型 ID 必须与[模型列表](raw/model-user-guide/get-started-with-models/models.md)完全一致（区分大小写，不接受别名）。 | 示例：`"qwen3.8-max"` ✅，`"Qwen/Qwen3.8-Max"` ❌；`qwen3.8-omni-flash` 支持音视频输入，但 `qwen3-vl-plus` 在 Anthropic 兼容协议下不支持。 |
| `stream` | 控制是否启用流式响应，默认 `false`。设为 `true` 时需客户端逐 chunk 解析。 | 部分模型（如思考模式模型、音频输出模型）强制要求 `true`，否则返回 `400-InvalidParameter`。 |
| `stream_options` | 对象，设 `{"include_usage": true}` 可在流式响应末尾返回 token 统计（`usage` 字段）。 | 仅流式调用生效。 |
| `messages` / `input` | Chat Completions 使用 `messages` 数组；Responses API 使用 `input`（支持字符串或消息数组），且支持 `developer` 角色等扩展。 | `input` 中多模态内容需按 `{"type": "text/image_url/file", "text": "...", "image_url": {...}}` 格式组织。 |
| `temperature` / `top_p` | 二选一设置，避免同时指定；取值范围 `[0.0, 2.0]`，超出将被静默截断。 | Anthropic 兼容接口中 `temperature` 范围为 `[0, 2)`，与官方 `[0.0, 1.0]` 不同。 |
| `seed` | 整数，用于确定性输出，取值范围 `0–2^31−1`。 | 启用后可复现相同结果，适用于测试与调试。 |

> ⚠️ 特别注意：  
> - `Qwen-Audio`、`Qwen-Math`、`Qwen-Coder`（部分场景）及全部视觉专用模型（如 `Qwen2.5-VL`）**不支持 OpenAI 兼容协议**，必须使用 DashScope 原生接口。  
> - `enable_thinking=true` 时，`result_format` 必须为 `"message"`，且 `incremental_output` 必须为 `true`（如 `qwen3.7-plus` 等模型强制启用思考模式）。  
> - `rag_options`（知识库/文档检索增强）**仅 DashScope 原生接口支持**，OpenAI 兼容接口中不可用。

## 面向开发者，简洁实用

- ✅ **一行初始化**（Python）：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  ```

- ✅ **标准 Chat 调用**（支持图像）：
  ```python
  response = client.chat.completions.create(
      model="qwen3-vl-plus",
      messages=[
          {"role": "user", "content": [
              {"type": "text", "text": "图中有什么？"},
              {"type": "image_url", "image_url": {"url": "https://example.com/photo.jpg"}}
          ]}
      ],
      stream=False
  )
  print(response.choices[0].message.content)
  ```

- ✅ **Responses API（推荐用于 Agent）**：
  ```python
  response = client.responses.create(
      model="qwen3.8-max",
      input=[{"role": "user", "content": "查一下今天北京天气"}],
      tools=[{"type": "web_search"}],  # 自动触发联网
      background=False
  )
  ```

- ❌ **避坑提示**：  
  - 不要混用协议参数（如在 OpenAI 接口里传 `vl_high_resolution_images`）；  
  - 不要省略 `base_url` —— 默认会指向 OpenAI 官方地址；  
  - 不要用开源模型名（如 `Qwen/Qwen3.7-Plus`）代替百炼模型 ID；  
  - 流式响应务必处理 `delta` 和 `finish_reason`，末尾 chunk 才含完整 `usage`。  

如遇问题，请记录响应头中的 `request_id`，用于日志排查或提工单。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


