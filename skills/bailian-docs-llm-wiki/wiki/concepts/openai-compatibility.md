# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 HTTP API 协议，完全遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与错误码规范，使开发者可直接复用现有 OpenAI SDK（Python/Node.js/Java/Go）和工具链，无需修改业务逻辑即可调用百炼托管的各类大模型服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与多语言开发**：开发者可沿用熟悉的 `openai` Python 包、`@openai/openai-node` 或 `openai-java` 等 SDK，仅需替换 `base_url` 和 `api_key`，即可接入百炼模型，显著降低技术栈切换成本。  
- **主流 AI 工具集成**：Cursor、Cherry Studio、WorkBuddy、QwenPaw、Dify、Hermes、Claude Code 等客户端与平台均原生支持该协议，配置后即可直接选用 `qwen3.8-max`、`qwen3.7-plus` 等模型进行对话、代码补全或 Agent 编排。  
- **框架无缝对接**：在 LlamaIndex 中可通过 `OpenAILike` LLM 类接入（需指定 `api_base` 和 `api_key`），在 Spring AI Alibaba 中亦支持 `OpenAiChatModel` 风格配置，实现 RAG、智能体等高级应用的快速构建。  
- **批量与会话管理**：通过 `/batch/chat` 和 `/conversations` 等兼容子路径，支持异步批量处理（JSONL 输入）和跨设备上下文延续，适用于数据标注、评测、客服会话等生产场景。  
- **能力分层调用**：  
  - `chat/completions`：基础文本/多模态对话（支持 `qwen3-vl-plus` 等视觉模型）；  
  - `responses`：增强型智能体接口，内置 `web_search`、`code_interpreter` 等工具，支持音视频输入（`qwen3.8-omni-flash`）；  
  - `embeddings`：向量嵌入服务（如 `text-embedding-v4`），但**不支持稀疏向量输出**；  
  - `files`：文档上传与解析（用于 `Qwen-Long` 等长文本模型问答）；  
  - `completions`：专为代码补全设计（仅限华北2地域 + `qwen-coder-turbo-latest`）。  

> ⚠️ 注意：Qwen-Audio、万相（文生图/文生视频）、实时语音（Realtime API）及多模态 Embedding（如 `qwen3-vl-embedding`）**不支持 OpenAI 兼容接口**，必须使用 DashScope 原生协议或专用 SDK。

## 关键参数和配置

| 参数 | 必填 | 说明 | 示例值 | 注意事项 |
|------|------|------|--------|----------|
| `base_url` | ✅ | 接口根地址，**必须使用业务空间专属域名** | `https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 旧域名 `dashscope.aliyuncs.com/compatible-mode/v1` 仍可用但性能较低，强烈建议迁移；地域（如 `cn-beijing`）必须与 API Key 绑定地域一致 |
| `api_key` | ✅ | 百炼控制台生成的密钥（`sk-xxx`） | `sk-abc123def456...` | Token Plan、Coding Plan、按量计费三类凭证**完全隔离**，混用将返回 `401 Incorrect API key provided` |
| `model` | ✅ | 严格匹配控制台「模型市场」中开通的模型 ID | `qwen3.8-max`、`text-embedding-v4`、`qwen3-vl-plus` | 大小写敏感；不可加后缀（如 `qwen3.8-max-v1` 错误）；未开通模型返回 `The product is not activated` |
| `messages` | ✅（chat/responses） | 标准 OpenAI 消息数组，`content` 类型依模型而异 | `[{"role":"user","content":"你好"}]` | 纯文本模型要求 `content` 为字符串；多模态模型要求 `content` 为数组，且 `type` 仅限 `text`/`image_url`/`video_url` 等白名单类型 |
| `stream` | ❌（可选） | 启用流式响应 | `true` | 流式下最后一 chunk 可通过 `stream_options={"include_usage": true}` 获取 token 统计 |
| `enable_thinking` | ⚠️（按模型强制） | 控制深度推理模式 | `true` | `qwen3.8-max`、`qwen3.7-plus` 等模型**强制要求为 `true`**；若设为 `false` 将报错 `"The value of the enable_thinking parameter is restricted to True"` |
| `temperature` | ❌（可选） | 控制输出随机性 | `0.7` | 取值范围 `[0, 2)`，**非 OpenAI 官方的 `[0, 1]`**，迁移时需校准 |

## 面向开发者，简洁实用

- ✅ **立即上手**：安装 `openai` SDK → 设置 `base_url` + `api_key` → 调用 `client.chat.completions.create(model="qwen3.8-max", messages=[...])`。  
- ✅ **调试建议**：优先使用环境变量 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`，避免硬编码；流式响应务必处理 `delta.content` 和 `finish_reason` 字段。  
- ✅ **避坑清单**：  
  - 不要用开源模型名（如 `Qwen/Qwen3.7-Plus`），只用控制台显示的标准 ID（`qwen3.7-plus`）；  
  - 不要混用地域或计费方案凭证；  
  - 多模态请求中，`image_url.url` 必须是公网可访问 URL 或 base64 编码（前缀 `data:image/jpeg;base64,`）；  
  - `responses` 接口不支持 `system` 消息，`qwen3.8-omni-flash` 的音视频输入需通过 `input_audio`/`input_video` 字段传入。  
- ✅ **推荐组合**：  
  - 生产部署：`base_url` 使用 Workspace 专属域名 + `openai==1.45.0`（稳定版） + `model=qwen3.8-max` + `enable_thinking=true`；  
  - 批量处理：改用 `/batch/chat` 路径，JSONL 请求体顶层传 `enable_thinking`，节省 50% 成本。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [frameworks](../api/frameworks.md)


