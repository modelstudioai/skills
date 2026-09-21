# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 RESTful API 协议，完全遵循 OpenAI 官方 API 的路径、请求/响应格式、参数命名与语义（如 `/chat/completions`、`messages` 数组、`stream` 流式开关等），使开发者能**零代码改造**复用现有 OpenAI SDK（如 `openai==1.0+`）、工具链（Dify、LlamaIndex、Cursor）及业务逻辑，快速接入千问（Qwen）全系列及主流第三方模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速原型开发**：使用标准 `openai` Python SDK 或 `curl` 直接调用，5 分钟完成首次推理（如 `qwen3.7-plus` 文本生成）；  
- **多模态推理**：通过 `chat/completions` 接口传入 Base64 图片（`qwen3-vl-plus`）、视频帧（`qwen3.8-omni-flash`），无需切换协议；  
- **智能体（Agent）构建**：选用 `/responses` 子路径（仍属 OpenAI 兼容体系），启用内置 `web_search`、`code_interpreter` 等工具，支持 `previous_response_id` 自动管理多轮上下文；  
- **向量化与检索**：调用 `/embeddings` 接口（如 `text-embedding-v4`），与 LangChain/LlamaIndex 的 `OpenAIEmbeddings` 无缝对接；  
- **批量处理**：使用 `/batches`（异步）或切换 `base_url` 至 `batch.dashscope.aliyuncs.com`（同步批处理），复用 OpenAI Batch 工作流；  
- **会话生命周期管理**：通过 `/conversations` 创建、查询、追加消息，实现跨设备上下文延续（替代自建 Session 存储）；  
- **代码补全**：调用 `/completions`（FIM 模式），专用于 `qwen-coder-turbo` 模型，兼容 OpenAI Code Completion 语义。

> ⚠️ 注意：并非所有能力都 100% 兼容。以下场景**必须使用 DashScope 原生接口**：  
> - 音频模型（`qwen-audio-*`）  
> - 多模态 Embedding（`qwen3-vl-embedding`）  
> - 视频生成、文生图（`wan2.6-t2i`）等非 Chat 类任务  
> - 需要 `max_frames`、`fps` 等细粒度视频参数的场景  

## 关键参数和配置

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| `base_url` | ✅ | **必须严格匹配地域、计费方案与功能模块**：<br>• 业务空间专属（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>• Token Plan（北京）：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>• Batch 同步：`https://batch.dashscope.aliyuncs.com/compatible-mode/v1` | `https://llm-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | ✅ | 与 `base_url` 所属地域及计费方案**强绑定**（北京 Key 不能调用弗吉尼亚 endpoint） | `sk-xxx`（从控制台创建） |
| `model` | ✅ | 必须为[文档明确列出的兼容模型名](../../raw/model-user-guide/get-started-with-models/models.md)，大小写敏感、不可拼错 | `qwen3.7-plus`, `qwen3-vl-plus`, `text-embedding-v4` |
| `messages` | ✅（Chat/Responses） | 标准数组格式，支持 `system`/`user`/`assistant` 角色；视觉模型需在 `content` 中嵌入 `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}` | `[{"role":"user","content":"你好"}]` |
| `stream` | ❌（默认 `false`） | 设为 `true` 启用 SSE 流式响应；部分模型（如 QVQ）**仅支持流式** | `true` |
| `temperature` | ❌（默认 `0.8`） | 取值范围 `[0, 2)`，非 OpenAI 官方 `[0, 1]`，迁移时需校准 | `0.5` |
| `max_tokens` | ❌（默认由模型决定） | 输出 token 上限；对 Responses 接口，该值限制“回复+思考”总长度 | `1024` |
| `tools` | ❌（Responses 专用） | 启用 Agent 工具时必填，支持 `web_search`, `code_interpreter`, `knowledge_search` 等内置工具 | `[{"type":"web_search"}]` |

## 面向开发者，简洁实用

- ✅ **立即上手**：复制粘贴示例代码，仅替换 `base_url` 和 `api_key` 即可运行；  
- ✅ **平滑迁移**：95% 的 OpenAI SDK 调用（含 `client.chat.completions.create()`、`client.embeddings.create()`）可直接复用；  
- ✅ **按需选型**：  
  - 通用对话 → `/chat/completions`  
  - 智能体 → `/responses`（需直供模型）  
  - 向量检索 → `/embeddings`  
  - 批量处理 → `/batches` 或 `batch.dashscope.aliyuncs.com`  
- ❌ **避坑提示**：  
  - 不要跨地域混用 `api_key` 与 `base_url`（报错 `invalid_api_key`）；  
  - 不要对 `qwen-audio` 或 `wan2.6-t2i` 使用 OpenAI 兼容接口；  
  - `qwen-coder-turbo` 仅支持华北2（北京）地域；  
  - 试用域名（`trial.cn-beijing.maas...`）RPM 仅为 1000，生产请务必使用业务空间专属域名。  

> 💡 提示：所有 OpenAI 兼容接口均位于 `compatible-mode/v1` 路径下，统一认证、统一限流、统一配额管理。调试时建议优先使用 [API Explorer](https://help.aliyun.com/zh/model-studio/api-explorer) 实时验证请求结构。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [frameworks](../api/frameworks.md)


