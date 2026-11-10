# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应结构、字段命名与语义规范（如 `/v1/chat/completions`、`messages` 数组、`delta` 流式字段等），使开发者能复用现有 OpenAI SDK、LangChain 等生态工具，仅需替换 `base_url` 和 `model` 即可快速迁移，无需重写业务逻辑。

## 在百炼平台的不同场景中如何使用

- **文本生成**：调用 `POST /compatible-mode/v1/chat/completions`，支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen3.8-max` 等全系列千问模型，适用于对话、摘要、代码生成等通用任务；注意其**不原生支持[工具调用](tool-calling.md)自动触发联网搜索**，需自行封装或改用 DashScope 原生接口。
- **多模态理解**：通过 `chat.completions` 接口传入含 `image_url` 的 `content` 数组，兼容 `qwen3-vl-plus`、`qwen3.5-omni-plus` 等视觉模型；音视频模型（如 `qwen3.8-omni-flash`）仅支持对应媒体输入，不可用于纯文本调用。
- **向量嵌入**：调用 `POST /compatible-mode/v1/embeddings`，支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型；**不支持稀疏向量输出**（`output_type=sparse` 将返回空 embedding）。
- **排序（Rerank）**：调用 `POST /compatible-mode/v1/reranks`，支持 `qwen3.7-text-rerank`、`qwen3-vl-rerank`，可用于 RAG 场景的召回结果精排。
- **文件处理**：使用 `POST /compatible-mode/v1/files` 上传文档，生成 `file_id` 后在 `chat.completions` 请求中通过 `file_ids` 引用，实现文档问答与数据提取；该能力已全面替代旧版原生文件管理 API，支持多地域。
- **批量推理**：支持两种模式——同步批处理（单请求多条 `messages`，走 `/chat/completions` endpoint）和异步 JSONL 批处理（`POST /batches`），后者成本降低 50%，适合离线预处理。

> ⚠️ 注意：`qwen-deep-research`、`qwen-audio` 等部分专用模型**暂不支持 OpenAI 兼容接口**，必须使用 DashScope 原生 SDK 或接口。

## 关键参数和配置

- **必配项（所有 OpenAI 兼容接口共用）**：
  - `base_url`：**必须显式设置为业务空间专属域名**，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（如 `https://abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）；旧域名 `dashscope.aliyuncs.com` 已逐步停用，性能与稳定性无保障。
  - `api_key`：按地域绑定，北京地域密钥不可用于弗吉尼亚 endpoint，否则返回 `invalid_api_key`。
  - `model`：严格匹配文档所列模型名（如 `qwen3.8-max`），大小写敏感，拼写错误将导致 404。

- **功能增强参数（按场景选用）**：
  - `stream`: `true`/`false`，启用流式响应（返回 `delta` 字段）。
  - `response_format`: 仅支持 `{"type": "json_object"}`，配合 `tools` 使用时可约束输出为 JSON Schema 格式。
  - `tools` + `tool_choice`: 支持[函数调用](function-calling.md)定义与选择策略（`auto`/`required`/`none`），但**不支持自动触发联网搜索**（该能力仅 DashScope 和 Anthropic 兼容接口提供）。
  - `enable_thinking`: 对 `qwen3.5+` 系列模型有效，控制思考链开关（`true`/`false`），默认开启；**必须置于 JSONL 请求体顶层，不可嵌套在 `extra_body` 中**。
  - `previous_response_id`: 仅 `responses` API 支持，用于自动关联上下文；**必须传入上一轮响应的顶层 `id`（UUID 格式）**，而非 `output` 内消息的 `id`。
  - `dimensions`: 文本/多模态向量模型支持，指定输出向量维度（如 `1024`, `2048`），需严格对照模型文档取值范围。
  - `instruct`: Rerank 模型支持，用英文描述排序任务意图（如 `"Given a query, rank documents by relevance"`），显著影响排序质量。

- **地域与 Endpoint 映射**：
  - 北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
  - 弗吉尼亚：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1`

## 面向开发者：简洁实用提示

- ✅ **推荐初始化方式（Python）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  # 后续调用完全复用 OpenAI 官方 SDK 语法
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "你好"}],
      stream=True
  )
  ```

- ✅ **流式解析要点**：OpenAI 兼容接口返回 `delta.content` 增量，需按 `finish_reason` 判断结束；与 DashScope 原生 `output.text` 增量字段语义不同，不可混用解析逻辑。

- ❌ **避坑提醒**：
  - 不要省略 `base_url` —— 默认会指向 OpenAI 官方服务；
  - 不要复用跨地域 API Key；
  - 不要在 `tools` 调用中依赖自动联网能力（如搜索、代码执行）；
  - `max_tokens` 在 OpenAI 兼容接口中为可选参数，但在 Anthropic 兼容接口中为必填，切勿混淆；
  - `qwen3.8-omni-flash` 等音视频模型不支持纯文本 `chat.completions`，调用前请确认模型能力矩阵。

- 📌 **调试建议**：开启 `DEBUG=1` 环境变量（Python SDK）或检查 HTTP 响应头 `X-DashScope-Request-ID`，便于在控制台日志中快速定位问题请求。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [file management api](../api/file-management-api.md)
- [more models](../api/more-models.md)


