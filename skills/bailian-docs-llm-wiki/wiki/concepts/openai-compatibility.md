# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议，完全遵循 OpenAI REST API 的路径、请求体结构、响应格式与流式传输规范（如 `/v1/chat/completions`），使开发者能复用现有 OpenAI 生态工具链（如 `openai` 官方 SDK、LangChain、LlamaIndex 等），仅需替换 `base_url` 和模型名即可快速接入百炼的 Qwen 系列及第三方直供模型，无需修改业务逻辑代码。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用**：支持文本生成（`qwen3.8-max`、`qwen3.7-plus`）、多模态理解（`qwen3-vl-plus`、`qwen3.8-omni-flash`）、向量嵌入（`text-embedding-v4`、`qwen3.7-text-embedding`）、排序（`qwen3-rerank`）、机器翻译（`qwen-mt`）、OCR（`qwen3.5-ocr`）等全栈能力，统一通过 `/compatible-mode/v1/` 前缀路由。
- **智能体开发**：`Responses API`（路径 `/v1/responses`）在 OpenAI 兼容模式下独家支持内置工具调用（`web_search`、`code_interpreter`、`file_search`），并可通过 `previous_response_id` 自动注入多轮上下文，实现轻量级 Agent 构建。
- **批量处理**：支持两种 OpenAI 兼容批量模式——  
  - *单请求批量*：在 `/v1/chat/completions` 中传入多条 `messages` 并启用 `batch.dashscope.aliyuncs.com` 域名；  
  - *文件批量*：使用 `/v1/batches` 提交 JSONL 文件，适用于数千级异步任务。
- **文件协同**：OpenAI 兼容的 File 接口（`/v1/files`）替代旧版文件管理 API，支持 `purpose=file-extract` / `purpose=batch` 等语义化用途，与 Chat/Responses/Batch 流程深度集成。
- **框架集成**：原生兼容 `langchain_openai`（部分模型）、`llamaindex` 等主流框架；对不完全兼容的模型（如 GUI-Plus、Qwen-Deep-Research），推荐搭配 `langchain-community` + `dashscope` 适配器使用。

> ⚠️ 注意：`Qwen-Audio`、`QwQ`（纯推理模型）、`Qwen-Deep-Research`（仅 DashScope SDK 支持）明确**不支持** OpenAI 兼容协议；三方模型（如 DeepSeek、Kimi）在该协议下不支持内置工具调用。

## 关键参数和配置

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `base_url` | **必填**，服务端点，必须匹配 API Key 所在地域与业务空间 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 需从控制台「业务空间详情」获取；旧域名 `dashscope.aliyuncs.com` 已不推荐 |
| `model` | **必填**，模型 ID，严格区分大小写与版本号 | `"qwen3.7-plus"`, `"qwen3-vl-plus"`, `"text-embedding-v4"` | 不同模型支持的能力不同（如 OCR 模型不支持 `chat/completions`） |
| `messages` | Chat/Responses/Vision 接口必填，标准 OpenAI 格式数组 | `[{"role":"user","content":"你好"},{"role":"assistant","content":"您好！"}]` | Vision 模型支持 `content` 中嵌入 `image_url`（Base64 或公网 URL） |
| `input` | Embedding/Rerank 接口必填，接受字符串或字符串数组 | `"hello world"` 或 `["query1", "doc2"]` | Rerank 接口需同时传 `query` 和 `documents` 字段 |
| `previous_response_id` | Responses API 可选，用于自动关联上一轮响应上下文 | `"resp_abc123..."`（UUID 格式） | 必须为响应顶层 `id` 字段值，非 `output.msg_xxx` |
| `dimensions` | Embedding 模型可选，指定输出向量维度 | `1024`, `2048` | 仅 `qwen3.7-text-embedding`、`text-embedding-v3/v4` 等新模型支持 |
| `enable_thinking` | Batch/Responses/GUI-Plus 等接口可选，启用深度思考链 | `true` | 影响 [Token](token.md) 计费，须与 `model` 同级传入，不可置于 `extra_body` |

## 面向开发者，简洁实用

- ✅ **快速迁移**：将 OpenAI SDK 初始化中的 `base_url` 替换为百炼专属地址，`api_key` 改为 `DASHSCOPE_API_KEY`，`model` 改为百炼控制台可用模型名，即可运行。
- ✅ **调试建议**：  
  - 使用 `curl` 直调时，务必添加 `Authorization: Bearer ${DASHSCOPE_API_KEY}`；  
  - 开启流式响应（`stream=true`）时，按 SSE 格式解析 `data:` 行；  
  - 错误码统一遵循 OpenAI 标准（如 `400 Bad Request`, `401 Unauthorized`, `429 Rate Limit Exceeded`）。
- ✅ **最佳实践**：  
  - 优先使用业务空间专属域名（非 `dashscope.aliyuncs.com`）以保障性能；  
  - 多模态输入前检查 `min_pixels`/`max_pixels` 是否符合模型要求（如 `qwen3.5-ocr` 默认 `min_pixels=3072`）；  
  - 批量任务优先选用 `/v1/batches` 异步接口，避免超时风险；  
  - LangChain 用户推荐 `langchain-community` + `dashscope` 组合，覆盖全部模型能力。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [file management api](../api/file-management-api.md)
- [vector and sort](../api/vector-and-sort.md)
- [more models](../api/more-models.md)


