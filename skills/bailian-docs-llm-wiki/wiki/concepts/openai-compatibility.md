# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，完全遵循 OpenAI 的公开协议规范（如 `/v1/chat/completions`、`/v1/embeddings` 等），使开发者能复用现有 OpenAI 生态工具、SDK 和代码逻辑，零改造接入百炼托管的 Qwen 系列大模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速原型与本地开发**：无需编写新 SDK，直接使用 `openai>=1.0.0` 官方 Python/JS SDK、Postman、Kilo CLI、Chatbox、Cursor 等第三方客户端，仅需替换 endpoint 和 API Key 即可调用。
- **框架集成**：LangChain、LlamaIndex 等主流框架可通过官方封装（如 `BaiLianChatModel`）无缝替换 `ChatOpenAI` 实例，自动适配百炼认证与参数映射。
- **多模态与文件工作流**：支持 OpenAI 兼容的 `/v1/files`（上传）、`/v1/chat/completions`（引用 `file://{file_id}` 图像/PDF）、`/v1/batches`（异步批量推理）等端点，实现类 GPT-4V 的文本+图像联合理解（需先上传文件并确认状态为 `processed`）。
- **生产环境平滑迁移**：已有 OpenAI 项目只需修改 `base_url` 和 `model` 参数（如将 `"gpt-4o"` 改为 `"qwen-plus"`），即可在保留全部业务逻辑的前提下切换至百炼服务，降低迁移成本与风险。

> ⚠️ 注意：所有 OpenAI 兼容接口均为无状态请求，不维护跨请求会话历史；`conversations` 等扩展端点当前仅为路由兼容，实际仍需客户端自行管理 `messages` 数组。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `base_url` | string | 是 | 固定为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（注意路径含 `/compatible-mode/v1`，非 `/v1`） |
| `api_key` | string | 是 | 百炼控制台生成的 **API Key**（非阿里云 AccessKey），需通过 `Authorization: Bearer <key>` 传入 Header |
| `model` | string | 是 | 必须为百炼已开通的模型 ID，例如 `qwen-max`、`qwen-plus`、`qwen-turbo`；不支持 OpenAI 原生模型名（如 `gpt-4o`）或未启用模型 |
| `messages` | array | 是（chat 场景） | 标准 OpenAI 格式：`[{"role": "user", "content": "..." }, ...]`；支持 `role="system"`，但不支持 `tool_use`（需用 Anthropic 或 DashScope 原生接口） |
| `stream` | boolean | 否 | 设为 `true` 启用 SSE 流式响应；GUI 工具（如 Cline）可能默认关闭，需手动开启 |
| `temperature` / `top_p` / `max_tokens` | number | 否 | 行为与 OpenAI 一致；但 `qwen-turbo` 的 `max_tokens` 上限为 8192，超限返回 400 |

> ✅ 提示：推荐通过环境变量配置以简化开发：
> ```bash
> export OPENAI_API_KEY="sk-xxx"  # 百炼 API Key
> export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
> ```

## 面向开发者，简洁实用

- **一句话启动**：安装 `openai==1.35.0+`，设置上述两个环境变量，即可用原生 `openai.ChatCompletions.create()` 调用百炼模型。
- **调试技巧**：
  - 返回 `401 Unauthorized` → 检查 API Key 是否过期或权限不足（需在百炼控制台「API Key 管理」中确认启用状态）；
  - 返回 `404 Not Found` → 核对 `model` 名称是否拼写正确、是否已在「模型服务」页开通；
  - 流式响应无数据 → 确认客户端是否正确处理 SSE（如 Python 中用 `response.iter_lines()`，而非 `.json()`）。
- **避坑指南**：
  - 不支持上传本地文件路径（如 `./image.jpg`），图像必须先调用 `/v1/files` 上传，再在 `messages` 中以 `{"type": "image_url", "image_url": {"url": "file://{file_id}"}}` 引用；
  - 所有文件操作（上传/查询/删除）均需通过 `/v1/files` 端点，DashScope 原生 `/api/v1/files` 接口已逐步迁移，新项目请优先使用兼容模式；
  - Embedding 接口仅支持 `text-embedding-v3`，`text-embedding-ada-002` 等别名已废弃，使用即报 404。

如需更高控制力（如显式开关联网搜索、获取完整 `usage` 统计、调试元信息），请切换至 [DashScope 原生接口](https://help.aliyun.com/zh/model-studio/dashscope-native-api)。

## 关联主题页

- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [file management api](../api/file-management-api.md)
- [more about models](../api/more-about-models.md)


