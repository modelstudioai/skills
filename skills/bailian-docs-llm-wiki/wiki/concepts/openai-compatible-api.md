# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 RESTful API，严格遵循 OpenAI 的请求/响应格式（如 `/v1/chat/completions`、`/v1/embeddings` 等路径），支持复用 OpenAI SDK、LangChain、LlamaIndex 等生态工具，无需修改业务代码逻辑，仅需替换 `base_url`、`api_key` 和模型名即可快速接入百炼的 Qwen 系列及第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型直调**：通过 `Chat Completions` 接口调用文本生成（`qwen3.8-max`）、多模态理解（`qwen3-vl-plus`）、代码补全（`qwen-coder-turbo`）等能力；通过 `Embeddings` 接口获取向量（`qwen3.7-text-embedding`、`text-embedding-v4`）；通过 `Rerank` 接口（`/compatible-api/v1/reranks`）执行语义重排序。
- **智能体开发**：使用 `Responses API`（`/v1/responses`）替代标准 Chat 接口，自动启用联网搜索、网页抓取、代码解释器等内置工具，并支持 `previous_response_id` 上下文管理与 Session 缓存，适用于构建生产级 Agent。
- **应用集成**：在「应用调用」场景中，可选择 OpenAI 兼容的 Responses 协议（而非 DashScope 原生协议）对接已发布的百炼应用，便于复用现有 OpenAI 客户端逻辑，但需注意 `input` 字段需映射为 `messages` 数组格式。
- **工具链迁移**：CLI 工具（如 Hermes Agent、Qwen Code）、IDE 插件（Cline、Qoder）、低代码平台（Dify）等均支持 OpenAI 兼容模式，开发者只需配置专属 `base_url` 与对应方案的 API Key，即可一键切换至百炼服务。
- **批量与异步处理**：支持 OpenAI 风格的 `/v1/batches` 批量接口（单请求多任务），也支持在 `/v1/chat/completions` 中通过 `batch.dashscope.aliyuncs.com` 域名发起同步批量调用，适用于高吞吐推理场景。

> ⚠️ 注意：并非所有模型和能力均全协议支持。例如：
> - `Qwen-Audio` 不支持 OpenAI 兼容协议，仅可通过 DashScope 原生接口调用；
> - `Completions` 接口（非 Chat）仅限 `qwen-coder-turbo`，且仅在北京地域可用；
> - `Vision` 接口要求 `messages` 中包含 `image_url` 或 base64 图片，不接受 `input` 字段；
> - Token Plan / Coding Plan 用户需使用对应方案专属域名（如 `token-plan.cn-beijing.maas.aliyuncs.com`），不可混用按量计费凭证。

## 关键参数和配置

| 参数 | 说明 | 百炼特有约束 |
|------|------|--------------|
| `base_url` | 必填。必须使用工作空间专属域名：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>（如 `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`） | 旧域名（如 `dashscope.aliyuncs.com`）仍可访问，但性能与稳定性较低；Token Plan/Coding Plan 用户须使用对应方案域名（如 `token-plan.cn-beijing.maas.aliyuncs.com`）。 |
| `model` | 必填。使用百炼支持的模型 ID，**不可直接复用 OpenAI 模型名**（如 `gpt-4o` 无效）。 | 支持范围因接口而异：<br>• Chat：`qwen3.8-max`, `qwen3-vl-plus`, `deepseek-v4-pro` 等<br>• Responses：限定列表（如 `qwen3.8-max`, `qwen3.8-omni-flash`）<br>• Embedding：`qwen3.7-text-embedding`, `text-embedding-v4`<br>• Rerank：仅 `qwen3-rerank` 支持 OpenAI 兼容路径 |
| `api_key` | 必填。严格绑定地域与计费方案（如北京 Token Plan Key 无法调用弗吉尼亚 endpoint）。 | 跨方案或跨地域使用将返回 `invalid_api_key` 错误。 |
| `stream` | 可选。设为 `true` 启用 SSE 流式响应。 | `stream_options={"include_usage": true}` 为百炼扩展字段，可在流式末尾 chunk 返回 token 统计。 |
| `temperature` / `max_tokens` | 控制生成行为与长度。 | • `temperature` 取值范围为 `[0, 2)`（非 OpenAI 的 `[0, 2]`）<br>• `max_tokens` 含义依接口而异：Chat 中为输出上限；Responses 中为「输出 + 思考 tokens」总上限（若开启思考） |
| `enable_thinking` | 可选。显式控制 `qwen3.5+` 系列模型的思考模式（reasoning tokens）。 | 默认开启，建议显式设置 `true`/`false` 以精确控制成本与延迟。 |
| `dimensions` | Embedding 接口专用。指定向量维度（如 `1024`）。 | 仅部分模型支持（如 `qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding`）；`text-embedding-v2` 等固定维度模型不支持该参数。 |

## 面向开发者，简洁实用

- ✅ **快速上手**：用 OpenAI Python SDK，仅改三处即可运行：
  ```python
  from openai import OpenAI
  client = OpenAI(
      base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
      api_key="sk-xxx",  # 百炼专属 API Key
  )
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "你好"}],
      stream=True,
  )
  ```
- ✅ **调试建议**：  
  - 使用 `curl` 测试时，务必带上 `Content-Type: application/json` 和 `Authorization: Bearer <api_key>`；  
  - 流式响应需处理 `text/event-stream` MIME 类型；  
  - 错误响应结构与 OpenAI 一致（含 `error.message`, `error.code`），但错误码语义遵循百炼定义（如 `invalid_model_name`, `insufficient_quota`）。
- ✅ **避坑提示**：  
  - 不要混用协议：`input`（DashScope） ≠ `messages`（OpenAI），应用调用时需按协议转换；  
  - 多模态输入必须用 `messages` 数组，且 `content` 支持 `{"type": "image_url", "image_url": {"url": "..."}}` 或 `{"type": "text", "text": "..."}` 结构；  
  - 第三方模型（DeepSeek/GLM/Kimi）仅在北京地域可用，且需在控制台开通对应服务。

> 💡 提示：所有 OpenAI 兼容接口均支持统一监控、配额管理与用量统计，可在百炼控制台「API 调用分析」中按 `model`、`endpoint`、`status_code` 维度下钻分析。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)


