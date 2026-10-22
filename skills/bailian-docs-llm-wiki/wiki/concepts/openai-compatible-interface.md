# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI REST API 协议规范（如 `/v1/chat/completions`、`/v1/responses`、`/v1/embeddings` 等）的标准化模型调用入口，允许开发者复用现有 OpenAI SDK、工具链和代码逻辑，零改造或极小改造即可接入百炼托管的 Qwen 系列及第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与原型验证**：开发者可直接将原有 OpenAI Python/Node.js SDK 初始化代码中的 `base_url` 替换为百炼业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），保持 `api_key` 和调用方式（如 `client.chat.completions.create()`）不变，即可调用 `qwen3.8-max`、`qwen3-vl-plus`、`deepseek-v4.1-flash-1017` 等模型，适用于本地 IDE 调试、Postman 测试或低代码平台（如 Dify、Cherry Studio）快速接入。

- **智能体（Agent）开发**：通过 OpenAI 兼容的 **Responses API**（`/v1/responses`），可原生使用 `tools`（内置 `web_search`、`code_interpreter`）、`tool_choice` 与 `parallel_tool_calls`，并借助 `previous_response_id` 实现免手动拼接上下文的多轮对话管理，显著简化 Agent 工作流编排。

- **多模态与结构化输出**：在 `/v1/chat/completions` 接口下，支持图像 URL/Base64 输入（需搭配 `qwen3-vl-plus` 等视觉模型）、`response_format: { "type": "json_object" }` 强制 JSON 输出、以及 `system` 消息控制行为，满足文档理解、GUI 自动化（`gui-plus`）、OCR 提取等场景需求。

- **批量与嵌入任务**：通过 OpenAI 兼容的 **Batch 接口**（JSONL 格式）和 **Embedding 接口**（`/v1/embeddings`），可高效处理千级文档向量化（如 `text-embedding-v4`）或异步批量推理，费用为实时调用的 50%，且完全兼容 LangChain 的 `OpenAIEmbeddings` 或 `BatchClient` 抽象。

- **会话生命周期管理**：配合 **Conversations API**（`/v1/conversations`），可创建、更新、追加消息并持久化会话状态，与 Responses API 的 `previous_response_id` 协同，实现跨设备、跨会话的上下文延续。

> ⚠️ 注意：并非所有模型均支持全部 OpenAI 兼容接口。例如：
> - `Qwen-Audio` 仅支持 DashScope 原生协议，**不支持任何 OpenAI 兼容接口**；
> - `qwen-deep-research` **仅支持 DashScope Python SDK，不支持 OpenAI 兼容接口**；
> - `QwQ` 模型不建议设置 `system` 消息，`QVQ` 模型则忽略 `system` 消息；
> - 视频帧数控制（`max_frames`）等细粒度参数在 OpenAI 兼容路径下通常不可用，应优先选用 DashScope 原生 API。

## 关键参数和配置

| 参数 | 作用 | 是否必填 | 说明 |
|------|------|----------|------|
| `base_url` | 接口根地址 | 是 | **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）性能与稳定性较低。 |
| `api_key` | 认证凭证 | 是 | 严格按地域绑定（如北京地域 Key 无法调用弗吉尼亚 endpoint），需在百炼控制台【API 密钥】页创建。 |
| `model` | 指定模型 ID | 是 | 必须从各接口支持的模型列表中精确选择：<br>• Chat API：`qwen3.8-max`、`qwen3-vl-plus`、`deepseek-v4-pro` 等；<br>• Responses API：限定 `qwen3.8-*`/`qwen3.7-*` 系列及部分三方模型；<br>• Embedding API：仅 `text-embedding-v4`、`qwen3.7-text-embedding` 等指定嵌入模型。 |
| `messages` | 对话输入 | 是（Chat/Responses） | 标准 OpenAI 数组格式，含 `role`（`system`/`user`/`assistant`）与 `content`；多模态时 `content` 可为含 `image_url` 或 `text` 的对象数组。 |
| `input` | 非对话输入 | 是（Embedding/Batch） | Embedding 接口传字符串或字符串数组；Batch 接口在 JSONL 中按行传 `{"input": "...", "model": "..."}`。 |
| `stream` | 启用流式响应 | 否 | 设为 `true` 返回 SSE 流，客户端需正确解析 `data:` 前缀与 `event: message` 字段。 |
| `previous_response_id` | 多轮上下文锚点 | 是（Responses API） | 必须传入上一轮响应顶层 `id`（UUID 格式），用于自动加载历史会话，替代手动拼接 `messages`。 |
| `tools` / `tool_choice` | 工具调用控制 | 否 | Responses API 支持内置工具（`web_search`, `code_interpreter`）与自定义 function；`tool_choice="auto"` 或指定工具名。 |
| `response_format` | 结构化输出 | 否 | `{"type": "json_object"}` 强制返回合法 JSON，适用于 Schema 约束场景。 |
| `temperature` / `top_p` / `max_tokens` | 生成控制 | 否 | `temperature` 默认 `0.8`（范围 `[0.0, 2.0]`），`max_tokens` 默认 `1024`（上限依模型而定，如 `qwen-plus` 支持 `8192`）。 |

## 面向开发者，简洁实用

- ✅ **即插即用**：安装 `openai>=1.0.0` 后，3 行代码完成初始化：
  ```python
  from openai import OpenAI
  client = OpenAI(base_url="https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", api_key="sk-xxx")
  response = client.chat.completions.create(model="qwen3.8-max", messages=[{"role": "user", "content": "你好"}])
  ```

- ✅ **SDK 无缝集成**：LangChain 用户可直接使用 `ChatOpenAI`（基础兼容）或推荐的 `ChatTongyi`（全模型支持）；无需修改 Prompt 模板或链路逻辑。

- ✅ **错误排查要点**：
  - 返回 `401 invalid_api_key` → 检查 API Key 地域是否匹配 endpoint；
  - 返回 `400 model not supported` → 确认 `model` 是否在当前接口支持列表内（如 Embedding 接口不支持 `qwen3-vl-plus`）；
  - 流式响应中断 → 客户端未正确处理 `data:` 分块或连接超时（建议设 `timeout=60`）；
  - `system` 消息无效 → 检查模型兼容性（`QwQ`/`QVQ` 不支持）或工具是否启用（如 Anthropic API 需额外 header）。

- 🚫 **避坑提示**：
  - 不要混用协议：同一请求勿同时传 `messages`（OpenAI 风格）和 `input`（DashScope 风格）；
  - 不要依赖未声明参数：`max_frames`、`vl_high_resolution_images` 等非 OpenAI 标准参数在兼容接口中无效；
  - 文件上传请优先使用 **OpenAI 兼容的 File 接口**（非原生 `/api/v1/files`），以获得统一权限与用途管理。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [file management api](../api/file-management-api.md)
- [more models](../api/more-models.md)


