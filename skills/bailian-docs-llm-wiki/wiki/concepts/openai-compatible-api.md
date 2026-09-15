# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 REST API 协议，完全遵循 OpenAI 的请求/响应格式（如 `/v1/chat/completions`）、参数命名、数据结构与错误码规范，使开发者无需修改业务逻辑即可将现有 OpenAI 应用无缝迁移至百炼，调用千问（Qwen）全系列及主流第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速接入与迁移**：开发者可直接复用 OpenAI Python SDK、Node.js SDK 或 curl 命令，仅需替换 `base_url` 和 `api_key`，数分钟内完成首次调用，适用于原型验证、PoC 开发和存量应用平滑升级。  
- **多模态联合推理**：在 `chat/completions` 接口中，通过标准 `messages` 数组传入文本+图像/视频 URL（或 base64），即可调用 `qwen3.5-omni-plus`、`qwen-vl-plus` 等模型，无需适配私有协议。  
- **生态工具集成**：LangChain、LlamaIndex、Dify、Cursor、Cherry Studio 等主流框架与客户端均原生支持 OpenAI 协议，配置百炼的兼容 endpoint 后即可开箱使用，大幅降低集成门槛。  
- **生产级部署**：推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），该路径具备独立限流、低延迟、高吞吐与业务空间级隔离能力，是生产环境首选。  
- **能力分层调用**：除基础 `chat/completions` 外，百炼还扩展了多个 OpenAI 兼容子接口，如：  
  - `POST /responses`：增强版对话接口，支持内置工具调用（联网搜索、代码解释器）、自动上下文管理与深度思考；  
  - `POST /embeddings`：调用 `qwen3.7-text-embedding` 等向量模型，兼容 `dimensions` 参数；  
  - `POST /files` + `POST /batches`：实现文件上传与批量异步推理，符合 OpenAI Batch 规范。

> ⚠️ 注意：部分能力（如 `Qwen-Audio` 语音合成/识别、`wan3.0-video` 视频生成）**不支持 OpenAI 兼容协议**，必须使用 DashScope 原生 API；`completions`（FIM 填空）接口仅支持 `qwen-coder-turbo`，且路径为 `/v1/completions`，非标准 OpenAI 行为。

## 关键参数和配置

| 参数 | 必填 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `base_url` | ✅ | string | **必须使用业务空间专属域名**，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；旧域名（如 `dashscope.aliyuncs.com`）已逐步淘汰，性能与稳定性较低 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | ✅ | string | 通过 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 创建，**严格按地域绑定**，不可跨地域混用 | `sk-xxx`（北京地域 Key 不可用于调用新加坡 endpoint） |
| `model` | ✅ | string | 模型 ID，需与所选地域支持列表一致；第三方模型名中 `.` 需替换为 `-`（如 `glm-5.2` → `glm-5-2`） | `"qwen3.8-max"`, `"deepseek-v4-pro"` |
| `messages` | ✅ | array | 标准 OpenAI 格式：`[{ "role": "user", "content": "..." }]`；多模态输入时 `content` 可为字符串或 `{ "type": "image_url", "image_url": { "url": "..." } }` 数组 | `[{"role":"user","content":"描述这张图"}]` |
| `stream` | ❌ | boolean | 是否启用流式响应，默认 `false`；设为 `true` 时返回 SSE 流 | `true` |
| `stream_options` | ❌ | object | 流式增强选项，`{"include_usage": true}` 可在末尾 chunk 返回 token 统计 | `{"include_usage": true}` |
| `enable_thinking` | ❌ | boolean | **Qwen 3.5+ 系列必需显式传入顶层字段**，控制是否启用深度思考模式（影响成本与延迟） | `true` |
| `max_tokens` | ❌ | integer | 输出长度上限（仅回复内容，不含思考过程）；注意：Anthropic 接口含义不同，勿混用 | `1024` |

> ✅ **最佳实践**：  
> - 将 `DASHSCOPE_API_KEY` 设为环境变量，避免硬编码；  
> - 使用 `WorkspaceId` 专属域名而非通用域名，确保生产稳定性；  
> - 第三方模型（如 DeepSeek、Kimi）仅在特定地域（如华北2）开通，调用前请确认控制台实时列表。

## 面向开发者，简洁实用

- **一句话启动**：  
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="sk-xxx",  # 替换为你的 API Key
      base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  resp = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "你好"}],
      stream=True
  )
  ```

- **调试技巧**：  
  - 遇到 `401 Unauthorized`：检查 `api_key` 所属地域是否与 `base_url` 地域一致；  
  - 遇到 `404 Not Found`：确认模型 ID 拼写正确，且该模型已在对应地域开通；  
  - 遇到 `429 Rate Limited`：检查账户级限流配额（[查询模型限流](../../raw/model-api-reference/more-about-models/list-quotas.md)），或升级消费档位。

- **避坑提醒**：  
  - ❌ 不要使用带日期后缀的快照模型（如 `qwen-plus-2025-07-28`），其限流额度远低于稳定版；  
  - ❌ 不要在 `extra_body` 中传 `enable_thinking`，必须作为请求体顶层字段；  
  - ❌ 不要将 Token Plan/Coding Plan 的 API Key 用于 Dify 等工作流平台（违规行为）。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)


