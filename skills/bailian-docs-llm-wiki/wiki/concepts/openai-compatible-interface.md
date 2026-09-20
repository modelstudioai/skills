# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组标准化 RESTful API，严格遵循 OpenAI 官方 API 的路径、请求/响应格式、参数命名与语义（如 `/v1/chat/completions`），使开发者能复用现有 OpenAI SDK（如 `openai>=1.0.0`）和业务代码，仅需替换 `base_url` 和 `api_key` 即可快速接入百炼的 Qwen 系列及第三方模型，实现零逻辑改造迁移。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用**：通过 OpenAI 兼容 Chat API（`/v1/chat/completions`）调用文本、多模态（VL）、代码（Coder）等模型；通过 Completions API（`/v1/completions`）进行代码补全（FIM）；通过 Embedding API（`/v1/embeddings`）生成文本向量；通过 Rerank API（`/v1/rerank`）执行语义排序。  
- **智能体（Agent）应用**：使用 OpenAI 兼容 Responses API（`/v1/responses`）同步或[异步调用](asynchronous-invocation.md)已发布的智能体应用，天然支持工具调用（联网搜索、网页抽取、代码解释器等）、多轮上下文管理（`previous_response_id`）、Session 缓存（`x-dashscope-session-cache: enable`）及结构化输出。  
- **批量处理**：通过 Batch Chat 接口（`/v1/batch/chat`）提交 JSONL 格式批量请求，费用为实时调用的 50%，适用于离线分析、评测等场景。  
- **开发工具集成**：在 VS Code 插件（Cline、Qoder）、CLI 工具（Kilo CLI、Qwen Code）、低代码平台（Dify）等中，只需配置百炼专属 `base_url` 和对应计费方案的 API Key，即可直接使用 OpenAI SDK 调用百炼服务。  
- **跨协议协同**：同一业务可混合使用 OpenAI 兼容接口（快速迁移）与 DashScope 原生接口（精细控制），例如用 OpenAI Chat API 做前端交互，用 DashScope 原生 API 处理视频帧级参数（`max_frames`）或深度思考模式（`enable_thinking`）。

> ⚠️ 注意：Qwen-Audio 模型**不支持任何 OpenAI 兼容协议**，必须使用 DashScope 原生 API；所有 OpenAI 兼容接口均**不支持 `max_frames`、`fps` 等视频细粒度参数**。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填，**必须使用业务空间专属域名**：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>（如 `https://wk-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`） | ❌ 禁用旧域名 `dashscope.aliyuncs.com`（性能差、稳定性低）；<br>✅ `{WorkspaceId}` 和 `{region}` 需与 API Key 创建地域严格一致。 |
| `api_key` | 必填，**严格按计费方案与地域绑定**：<br>- Token Plan / Coding Plan：使用对应方案生成的 Key；<br>- 按量计费：必须使用该 Workspace 下创建的 Key。 | 跨方案或跨地域使用将返回 `invalid_api_key` 错误。 |
| `model` | 必填，模型 ID（如 `"qwen3.8-max"`、`"qwen3-vl-plus"`、`"text-embedding-v4"`）。 | 模型可用性因接口而异：Responses API 支持最全（含 `qwen3.8-omni-flash`），Chat API 次之，Embedding/Rerank API 仅限对应向量/排序模型。 |
| `input` / `messages` | - Responses API：用 `input`（字符串或消息数组）；<br>- Chat API：用 `messages`（标准 OpenAI 消息数组）；<br>- Embedding/Rerank：用 `input` 或 `query`+`documents`。 | Responses API 支持 `previous_response_id` 自动注入历史；Chat API 不支持 `system` 角色对 QwQ/QVQ 模型生效。 |
| `stream` | 控制流式响应（`true`/`false`）。 | Responses API 流式事件字段为 `response.output_text.delta`；启用 `stream_options={"include_usage": true}` 可在流结束时返回 token 统计。 |
| `temperature` / `top_p` | 控制生成随机性。 | 二选一设置，避免同时指定；Anthropic 协议温度范围为 `[0, 2)`，但 OpenAI 兼容接口保持 `[0.0, 2.0]` 一致行为。 |
| `max_tokens` | 仅作响应截断用（非模型内部长度限制）。 | Responses API 中该参数**未定义**，实际输出长度由模型窗口隐式约束；DashScope 原生 API 才具备精确控制能力。 |

## 面向开发者，简洁实用

- ✅ **快速上手**：  
  ```python
  from openai import OpenAI
  client = OpenAI(
      base_url="https://wk-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
      api_key="sk-xxx",  # 与 base_url 地域/方案匹配
  )
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "你好"}],
      stream=True,
  )
  ```

- ✅ **关键检查清单**：  
  - [ ] `base_url` 是否含 `{WorkspaceId}` 且地域正确？  
  - [ ] `api_key` 是否为同一地域、同一计费方案下创建？  
  - [ ] `model` 是否在目标接口的支持列表中？（查 [Qwen API Reference](api/qwen-api-reference.md)）  
  - [ ] 多模态输入是否使用 `image_url` 格式（Vision）或 `input_image`（Responses）？  
  - [ ] 需要工具调用或[长期记忆](long-term-memory.md)？→ 请优先选用 **Responses API**，而非 Chat API。  

- ❌ **常见陷阱**：  
  - 用 Token Plan Key 调用按量计费 `base_url` → `401`；  
  - 对 `qwen3.8-omni-flash` 使用 Chat API → 无法处理音视频输入（必须用 Responses API）；  
  - 在 Embedding API 中传 `output_type=sparse` → 返回空 embedding（百炼不支持稀疏向量）。  

如需更高性能、更细粒度控制（如视频抽帧、深度思考、RAG 知识库显式配置），请切换至 [DashScope 原生 API](api/qwen-api-reference.md)。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)


