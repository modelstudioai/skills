# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/chat/completions`、`/embeddings`、`/files` 等端点），使开发者无需修改现有代码即可将基于 OpenAI SDK 或生态工具（如 LangChain、LlamaIndex、Dify、Cursor）构建的应用平滑迁移至百炼 Qwen 系列模型及专用能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用**：通过 `POST /compatible-mode/v1/chat/completions` 调用文本大模型（如 `qwen3.8-max`）、多模态模型（如 `qwen3.8-omni-flash`）或第三方模型（如 `deepseek-v4`），支持 `messages` 数组、`system` 角色、多模态 `image_url`/`video_url` 输入；`/compatible-mode/v1/embeddings` 和 `/compatible-mode/v1/rerank` 分别用于向量化与重排序任务。
- **批量处理**：使用 `/compatible-mode/v1/batches` 提交异步批量请求（最多 100 条），适用于离线分析；注意 `batch/chat` 与 `batch/file-input` 的 payload 结构不兼容，需按场景分别构造。
- **文件管理**：通过 `/compatible-mode/v1/files` 上传、查询和删除文件，替代旧版 `/api/v1/files` 接口；上传后获得 `file_id`，可用于后续 `batch` 或 `file-extract` 场景（需等待 `status: "processed"`）。
- **开发集成**：在 LangChain 中直接使用 `BailianChatModel` 和 `BailianEmbeddings` 封装；在 CLI 工具（如 Hermes Agent、Qwen Code）或桌面应用（如 Cursor、WorkBuddy）中，只需配置 `base_url`（以 `/compatible-mode/v1` 结尾）、`api_key` 和合法 `model` 名即可接入。
- **跨协议协同**：同一业务空间下，OpenAI 兼容接口与 DashScope 原生协议、Anthropic 兼容协议共享模型资源与配额，但能力边界不同（例如 OpenAI 兼容接口不支持 `functions`，而 Anthropic 支持 `tool_use`；Qwen-Audio 仅 DashScope 原生支持）。

## 关键参数和配置

- **必填参数**：
  - `model`：必须为百炼平台发布的合法模型 ID（如 `"qwen3.7-plus"`），**不可使用 OpenAI 模型名（如 `"gpt-4o"`）**；非法值返回 404。
  - `base_url`：格式为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京地域）或 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（[Token](token.md) Plan）；WorkBuddy 等工具需补全路径（如 `/v1/chat/completions`）。
  - `Authorization` 请求头：`Bearer <api_key>`，API Key 必须与所选计费方案（[Token](token.md) Plan / Coding Plan / 按量计费）严格匹配。

- **常用可选参数**：
  - `response_format`：仅 `chat/completions` 支持 `{"type": "json_object"}`，但需模型原生支持（如 `qwen-plus`），`qwen-max` 当前不支持。
  - `min_pixels` / `max_pixels`：控制图像/视频输入分辨率，不同模型有默认值（如 `qwen3.8-max` 默认 `min_pixels=65536`）。
  - `temperature`：取值范围 `[0, 2)`，注意 Anthropic 协议官方范围为 `[0.0, 1.0]`，迁移时需校验。
  - `tools` + `tool_choice`：百炼自研工具调用机制（支持 `web_search`, `code_interpreter` 等），**不兼容 OpenAI 原生 `functions` 参数**；LangChain 的 `bind_tools()` 将被忽略。

- **限制说明**：
  - 不支持 `conversations` 的长期会话状态（仅单轮上下文）；
  - `responses` 端点已于 2024 年 7 月下线，调用返回 404，请改用 `chat/completions`；
  - 文件上传大小上限为 50 MB，仅支持 `.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`；图像/视频需走 `qwen-vl` 专用接口；
  - 所有 `file_id` 和 `batch_id` 均为百炼平台内生成 ID，不可复用 OpenAI 的 ID。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [file management api](../api/file-management-api.md)


