# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 HTTP API 协议，严格遵循 OpenAI 的 RESTful 设计规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/rerank` 等路径）和请求/响应格式（如 `messages` 数组、`choices[0].message.content` 结构），使开发者无需修改业务逻辑即可复用现有 OpenAI SDK（Python/Node.js/Java/Go 等）快速接入百炼全栈模型能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本生成与对话**：通过 `POST /compatible-mode/v1/chat/completions` 调用 `qwen3.8-max`、`qwen3.7-plus` 等大语言模型，支持 `system`/`user`/`assistant` 角色、流式响应（`stream=true`）、工具调用（`tool_choice` + `tools`）及多轮会话管理（配合 `Conversations API`）。
- **向量嵌入（Embedding）**：通过 `POST /compatible-mode/v1/embeddings` 调用 `text-embedding-v4` 或 `qwen3.7-text-embedding`，支持批量文本输入、自定义维度（`dimensions=1024`）和编码格式（`encoding_format="base64"`），但**不支持稀疏向量输出**（`output_type=sparse` 无效）。
- **文本重排序（Rerank）**：通过 `POST /compatible-mode/v1/rerank` 调用 `qwen3-rerank` 或 `qwen3.7-text-rerank`，需传入 `query` 和 `documents` 数组，支持任务指令（`instruct`）以提升领域适配性。
- **智能体增强（Responses API）**：通过 `POST /compatible-mode/v1/responses` 启用内置联网搜索、网页抓取、代码解释器等工具，需配合 `previous_response_id` 实现多轮工具链协同，仅对指定模型（如 `qwen3.8-max`、`deepseek-v4-pro`）完整生效。
- **文件与批量处理**：通过 `POST /compatible-mode/v1/batch/chat` 提交 JSONL 批量请求，或结合 `Conversations API`（`/compatible-mode/v1/conversations`）实现持久化会话，所有路径均基于 OpenAI 兼容协议设计。

> ⚠️ 注意：Qwen-Audio（语音合成/识别）、实时语音/多模态流式模型（如 Qwen-Omni 实时模式）、AOQ 协议模型**不支持 OpenAI 兼容接口**，必须使用 AOQ SDK 或 DashScope 原生协议。

## 关键参数和配置

| 参数 | 必填 | 类型 | 说明 | 示例值 |
|------|------|------|------|--------|
| `base_url` | ✅ | string | **必须使用业务空间专属域名**，旧版 `dashscope.aliyuncs.com` 已逐步停用。格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | ✅ | string | 通过百炼控制台按地域创建的 API Key，**不可跨地域混用**；[Token](token.md) Plan、Coding Plan、按量计费 Key 完全隔离 | `sk-xxx`（按量） / `tp-xxx`（[Token](token.md) Plan） |
| `model` | ✅ | string | **严格区分大小写与版本号**，必须使用百炼官方模型 ID（非开源名），错误命名将返回 `Model not exist.` | `qwen3.8-max`（正确） / `Qwen/Qwen3.8-Max`（错误） |
| `stream` | △ | boolean | 部分模型（如 QVQ、思考模式模型）**强制要求 `true`**；未设置或设为 `false` 将报错 | `true` |
| `max_completion_tokens` | △ | integer | OpenAI 兼容 Chat 接口**不支持 `max_tokens`**，须用此参数控制输出长度（上限由模型决定） | `2048` |
| `temperature` | ❌ | number | 取值范围 `[0.0, 2.0)`，超出将触发 `InvalidParameter` 错误 | `0.7` |
| `top_p` | ❌ | number | 取值范围 `(0.0, 1.0]`，与 `temperature` 共同调控输出多样性 | `0.95` |

其他重要约束：
- **地域强绑定**：API Key、`base_url`、模型列表三者必须属同一地域（如华北2），跨地域调用必然失败。
- **输入格式校验**：`messages` 必须为非空数组；纯文本模型禁止传入 `image_url` 等多模态 `content`；`system` 消息在 QwQ/QVQ 中可能被忽略。
- **流式要求**：QVQ、Qwen-Omni（非实时模式）等视觉模型**仅支持[流式输出](streaming-output.md)**，`stream=false` 将拒绝请求。

## 面向开发者，简洁实用

✅ **快速上手（Python 示例）**：
```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 推荐环境变量方式
    base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 文本生成
response = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你好"}],
    stream=True
)
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

# 向量嵌入
embed_resp = client.embeddings.create(
    model="text-embedding-v4",
    input=["hello world"],
    dimensions=1024
)
print(embed_resp.data[0].embedding[:5])
```

✅ **避坑指南**：
- 不要硬编码 API Key 到前端或客户端代码 → 使用临时 Key（最长 1800 秒）；
- 不要复用其他云厂商的 OpenAI Key → 百炼 Key 仅限百炼服务；
- 不要省略 `base_url` 中的 `/compatible-mode/v1` 路径 → 缺失将导致 404；
- 调试时优先用 `dashscope` CLI（`dashscope chat --model qwen3.8-max "你好"`）自动校验配置；
- 查看模型是否支持某功能？直接查 [模型与协议支持范围](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2)，而非依赖社区文档。

> 💡 提示：所有 OpenAI 兼容接口均计入百炼统一计费体系，token 统计规则与 DashScope 原生协议一致，无需额外换算。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


