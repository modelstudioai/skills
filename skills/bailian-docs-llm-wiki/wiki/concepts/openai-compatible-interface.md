# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI RESTful API 规范（如 `/chat/completions`、`/embeddings`、`/images/generations` 等路径与请求/响应格式）的标准化模型服务入口。它允许开发者复用现有 OpenAI 生态代码（SDK、LangChain、LlamaIndex 等），仅需替换 `base_url` 和 `model` 即可快速迁移，无需重写业务逻辑。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有应用**：当您已基于 OpenAI SDK（Python/Node.js/Java 等）或 LangChain 构建了应用，只需将 `openai.base_url` 改为百炼专属兼容地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并传入百炼控制台发布的模型名（如 `qwen3.8-max`），即可直接调用 Qwen 及其他百炼托管模型。
  
- **多模态与嵌入支持**：除文本生成外，OpenAI 兼容接口还覆盖：
  - **视觉理解**：通过 `chat/completions` 提交含 `image_url` 的消息，调用 `qwen3-vl-plus` 等多模态模型；
  - **向量嵌入**：使用 `/embeddings` 端点调用 `text-embedding-v4` 等模型，完全兼容 OpenAI Embedding 请求体；
  - **批量处理**：支持 OpenAI 风格的 Batch 接口（JSONL 文件异步提交），适用于评测、标注等非实时任务。

- **高级对话管理**：通过 `Conversations API`（`/conversations`）创建会话，再结合 `Responses API`（`/chat/responses`）发起请求，可自动维护上下文、启用联网搜索与代码解释器等内置工具能力——该组合是 OpenAI 兼容体系中唯一支持“智能体原生行为”的通道。

- **开发工具直连**：主流 AI 编程工具（如 Cursor、WorkBuddy、Qwen Code、Dify、Cherry Studio）均原生支持 OpenAI 兼容协议，配置对应 `Base URL` 和 `API Key` 后，即可在 IDE 或 Web 界面中直接调用百炼模型，无需额外适配层。

- **框架集成**：LlamaIndex、Spring AI Alibaba 等框架可通过标准 `ChatOpenAI` 或 `OpenAIEmbeddings` 类接入，只需设置 `api_base` 为百炼兼容地址，即可复用全部链路能力（如 RAG、Agent 调度）。

> ⚠️ 注意：`Qwen-Audio`、`qwen3-vl-embedding` 等专用模型**不支持** OpenAI 兼容接口，必须使用 DashScope 原生协议。

## 关键参数和配置

| 参数 | 说明 | 必填 | 示例值 | 注意事项 |
|------|------|------|--------|----------|
| `base_url` | OpenAI 兼容接口专属端点，**必须使用业务空间专属域名** | 是 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | 旧域名 `dashscope.aliyuncs.com` 已弃用，性能与稳定性无保障；`{WorkspaceId}` 需替换为控制台实际 ID |
| `api_key` | 百炼 API Key，**严格按计费方案与地域绑定** | 是 | `sk-xxx` | [Token](token.md) Plan、Coding Plan、按量计费 Key **不可混用**；北京 Key 无法调用新加坡 endpoint |
| `model` | 模型 ID，**必须与控制台发布的名称完全一致** | 是 | `qwen3.8-max`（正确）<br>`qwen-max`（错误，旧版命名） | 不区分大小写但禁止后缀（如 `qwen3.8-max-v1` 无效）；部分工具（如 Cursor）要求小数点转连字符（`kimi-k2.6` → `kimi-k2-6`） |
| `stream` | 是否启用流式响应 | 否 | `true` / `false` | 全部支持，但 `Responses API` 的流式字段命名（如 `delta.content`）与标准 OpenAI 一致，而 `chunk` 结构中不包含 `tool_calls` 中间步骤（此能力仅 DashScope 原生接口支持） |
| `enable_thinking` | 控制是否启用深度推理模式（Qwen3 系列必需） | 否（Qwen3 默认开启） | `true` / `false` | 若未显式设置 `true`，`qwen3.7-plus` 等模型可能降级为普通响应；Batch 场景下建议设为 `false` 以节省 token |
| `previous_response_id` | 多轮对话时用于关联上下文（仅 `Responses API`） | 是（多轮必填） | `resp_abc123` | 必须传入上一轮响应顶层 `id`（格式 `resp_xxx`），而非 `output` 内消息的 `msg_xxx` |

## 面向开发者，简洁实用

- ✅ **三步接入**：  
  1. 控制台创建对应计费方案的 API Key；  
  2. 设置 `base_url`（确认地域 + WorkspaceId）和 `model`（查控制台最新名称）；  
  3. 用任意 OpenAI SDK 发起 `client.chat.completions.create(...)` —— 无需修改请求结构。

- ✅ **调试建议**：  
  - 优先使用 `curl` 或 Postman 验证基础请求（避免 SDK 封装干扰）；  
  - 响应中 `id` 字段以 `resp_` 开头即表示走的是 `Responses API`（带工具链），以 `chatcmpl_` 开头则为标准 `Chat Completions`（无工具调用）；  
  - 流式响应请按 SSE 格式解析，每行以 `data:` 开头，末尾空行分隔。

- ❌ **避坑清单**：  
  - 不要复用 OpenAI 的 `gpt-4` 模型名——必须用百炼真实模型 ID；  
  - 不要忽略 `enable_thinking`：Qwen3 系列默认开启思考，但若需低延迟响应，请显式设为 `false`；  
  - 不要混淆 `max_tokens` 含义：OpenAI 兼容接口中该参数仅代表**输出 token 上限**（非总上下文）；  
  - 不要在前端硬编码 `api_key`：生产环境务必通过后端签发临时 Key（有效期 ≤ 1800 秒）。

- 📦 **推荐组合**：  
  - 新项目 & 需要工具调用 → 选 `Responses API`（`/chat/responses`）；  
  - 迁移存量 OpenAI 应用 & 无需工具 → 选标准 `Chat Completions`（`/chat/completions`）；  
  - 需要最全参数控制（如 `repetition_penalty`、`enable_search`）或流式返回工具中间步骤 → 切换至 DashScope 原生接口。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)
- [frameworks](../api/frameworks.md)


