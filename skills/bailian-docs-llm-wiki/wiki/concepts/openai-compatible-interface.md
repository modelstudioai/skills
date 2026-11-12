# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 HTTP API，其请求格式、响应结构、错误码和 SDK 调用方式与 OpenAI 官方 API（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/reranks` 等）高度一致，使开发者无需修改业务逻辑即可将现有 OpenAI 集成快速迁移到百炼平台。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一能力，而是覆盖多类 AI 服务的统一接入范式，在以下核心场景中被广泛采用：

- **文本生成与对话**：通过 `POST /v1/chat/completions` 调用 Qwen 系列模型（如 `qwen-max`、`qwen3.8-max`），支持标准 `messages` 输入与流式响应；另有 `responses` 接口（`/v1/responses`）提供内置联网搜索、工具调用等智能体能力，自动管理多轮上下文。
- **向量嵌入**：通过 `POST /v1/embeddings` 调用 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型，输入 `input` 字符串或数组，返回稠密向量；注意不支持稀疏向量（`output_type=sparse` 将被忽略）。
- **文本与多模态排序（Rerank）**：通过 `POST /v1/reranks` 调用 `qwen3.7-text-rerank` 或 `qwen3-vl-rerank`，传入 `query` 和 `documents` 数组，直接获得重排序结果。
- **图像生成**：部分图像模型（如 `qwen-image-3.0-pro`）支持 OpenAI 兼容模式，但需注意：**Qwen-Audio 系列模型明确不支持该协议**，仅限 DashScope 原生接口。
- **语音识别（ASR）**：`Qwen-ASR` 模型同时支持 OpenAI 兼容接口（同步/流式）与 DashScope 协议，其余 ASR 模型（如 Paraformer、Fun-ASR）暂不兼容。

> ✅ 关键优势：复用 OpenAI 官方 SDK（如 `openai==1.49.0`），只需替换 `base_url`、`api_key` 和 `model` 参数，即可完成迁移。  
> ⚠️ 注意限制：工具调用（function calling）、`thinking` 字段、音视频输入等高级能力**不在 OpenAI 兼容接口中原生支持**，需切换至 Anthropic 兼容 Messages 接口或 DashScope 原生接口。

## 关键参数和配置

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `base_url` | 必填，必须使用**业务空间专属域名** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 旧域名 `dashscope.aliyuncs.com` 已不推荐，性能与稳定性较低；`{WorkspaceId}` 需从控制台获取 |
| `api_key` | 必填，API Key 严格绑定地域 | `sk-xxx` | 北京地域 Key 不可用于弗吉尼亚 endpoint，否则报 `invalid_api_key`（非密钥失效，而是地域不匹配） |
| `model` | 必填，必须为接口文档明确列出的支持型号 | `qwen-max`, `qwen3.8-max`, `text-embedding-v4`, `qwen3.7-text-rerank` | 模型名不可自定义；`responses` 接口仅支持特定模型（如 `qwen3.8-max`），否则缺失 Agent 能力 |
| `stream` | 布尔值，启用流式响应 | `true` | 流式响应需设置 `Content-Type: text/event-stream`，客户端按 `data: {...}` 行解析 |
| `max_tokens` | 输出长度上限（仅 `chat.completions` 等文本接口） | `1024` | DashScope 原生接口中对应字段为 `max_output_tokens`，二者语义相同但字段名不同 |
| `previous_response_id` | 仅 `responses` 接口需要，用于多轮对话状态延续 | `"resp_abc123"` | 必须传入上一轮响应顶层 `id`（UUID 格式），而非 `output` 中消息的 `msg_xxx` ID |

## 面向开发者，简洁实用

- ✅ **快速上手**：用 OpenAI Python SDK，3 行代码完成迁移：
  ```python
  from openai import OpenAI
  client = OpenAI(
      base_url="https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
      api_key="YOUR_API_KEY"
  )
  response = client.chat.completions.create(model="qwen-max", messages=[{"role": "user", "content": "你好"}])
  ```

- ✅ **调试建议**：
  - 使用 `curl` 直调时，务必检查 `Authorization` Header 是否正确携带 Bearer [Token](token.md)；
  - 流式响应需用 `curl -N` 或 SSE 客户端解析，避免 JSON 解析失败；
  - 所有 OpenAI 兼容接口均**不共享 session**，对话历史需由客户端自行维护（`responses` 接口除外）。

- ⚠️ **避坑提醒**：
  - 不要混用地域：Key、`base_url`、SDK 初始化中的 region 必须完全一致；
  - 不要传错模型名：`qwen3.5-flash` 在 `chat.completions` 下有效，在 `responses` 下无效；
  - 不要依赖未声明能力：`tool_choice`、`tools` 字段在 OpenAI 兼容接口中会被静默忽略，请改用 Anthropic 或 DashScope 接口。

如需完整能力（如工具调用、多模态融合、异步批量处理），请优先选用 DashScope 原生接口或 Anthropic 兼容 Messages 接口。OpenAI 兼容接口的核心价值在于**平滑迁移、降低集成成本、保持生态一致性**。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [image generation](../api/image-generation.md)
- [audio api directory](../api/audio-api-directory.md)


