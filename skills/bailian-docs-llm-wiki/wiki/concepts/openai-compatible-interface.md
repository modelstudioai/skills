# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套遵循 OpenAI REST API 规范的标准化模型调用协议，允许开发者复用现有 OpenAI SDK、工具链和工程实践，仅需替换 `base_url`、`api_key` 和模型名称即可快速接入百炼的 Qwen 系列及第三方大模型（如 DeepSeek、GLM、Kimi），无需重写业务逻辑。

## 在百炼平台的不同场景中如何使用

OpenAI 兼容接口在百炼中按功能维度组织为多个专用端点，覆盖主流 AI 应用场景：

- **标准对话（`/chat/completions`）**：适用于通用文本生成、多轮聊天、简单 Agent 编排。支持文本与多模态模型（如 `qwen3.7-plus`、`qwen3-vl-plus`），但**不支持 `Qwen-Audio`**。
- **增强型智能体（`/responses`）**：百炼特有扩展端点，内置联网搜索、网页抓取、代码解释器、文搜图、图搜图、知识库调用等工具能力；支持 `previous_response_id` 实现多轮上下文自动管理，并通过 `x-dashscope-session-cache` 启用会话级缓存。
- **视觉理解（Vision）**：兼容 OpenAI 的 `image_url` 消息格式，支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等模型，可直接传入公网 URL 或 Base64 Data URI。
- **向量嵌入（`/embeddings`）**：支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等 6 种稠密向量模型，输出维度可选（如 1024、2048），但**不支持稀疏向量**。
- **会话管理（`/conversations`）**：用于跨设备、长时间中断的上下文延续，配合 `/responses` 自动注入历史消息，提升长周期任务连贯性。
- **异步批量处理（Batch）**：支持 JSONL 文件批量提交或单请求同步等待模式，显著降低单位成本，适用于数据标注、模型评测等非实时场景。

> ⚠️ 注意：`Qwen-Audio`、`Qwen-Deep-Research` 及多模态嵌入模型（如 `qwen3-vl-embedding`）**均不支持 OpenAI 兼容协议**，必须使用 DashScope 原生接口。

## 关键参数和配置

| 参数 | 位置 | 说明 | 示例值 |
|------|------|------|--------|
| `base_url` | 客户端初始化时必填 | 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名 `dashscope.aliyuncs.com` 已不推荐 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | 请求 Header（`Authorization: Bearer <key>`）或客户端初始化参数 | 严格按地域绑定，北京 Key 无法调用新加坡 endpoint | `sk-xxx` |
| `model` | 请求体顶层字段 | 必填，需严格匹配文档列表（大小写、连字符敏感），如 `qwen3.8-max`，不可简写为 `qwen38-max` | `"qwen3.8-max"` |
| `enable_thinking` | 请求体顶层字段（非嵌套） | 对 `qwen3.5`–`qwen3.8` 系列模型，默认开启深度思考；设为 `false` 可跳过思考阶段、节省 token | `false` |
| `previous_response_id` | `/responses` 请求体 | 上一轮 `/responses.create()` 返回的 `id`（UUID 格式），用于多轮上下文关联 | `"resp_abc123..."` |
| `conversation_id` | `/conversations` 相关接口 | 由 `/conversations.create()` 创建的会话 ID，用于长期状态恢复 | `"conv_xyz789..."` |
| `reasoning.effort` | `/responses` 请求体 | 控制思考强度，可选 `"low"` / `"medium"` / `"high"`，影响响应深度与耗时 | `"high"` |

- 多模态输入统一采用 OpenAI 标准 `messages` 数组格式，`content` 支持 `text`、`image_url`（含 `url` 字段）、`video_url` 等类型；
- 所有 OpenAI 兼容接口均支持流式响应（`stream=true`），chunk 格式与 OpenAI 完全一致；
- 不支持 OpenAI 的 `functions` / `function_call` 字段，工具调用请使用 `/responses` 的原生工具机制。

## 面向开发者：快速上手建议

- ✅ **推荐 SDK**：`pip install -U openai`（通用）或 `pip install langchain_openai`（LangChain 场景）；
- ✅ **初始化示例（Python）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
      api_key="sk-xxx"
  )
  # 标准对话
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "你好"}]
  )
  # 增强智能体
  response = client.responses.create(
      model="qwen4-max-preview",
      input="查一下今天北京天气",
      reasoning={"effort": "high"}
  )
  ```
- ✅ **调试技巧**：启用 `DEBUG=1` 环境变量可输出完整 HTTP 请求/响应日志；
- ❌ **避坑提示**：勿将 `enable_thinking` 放入 `extra_body`；勿混用地域 Key 与域名；勿对 `Qwen-Audio` 使用 OpenAI 接口。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [more models](../api/more-models.md)


