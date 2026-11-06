# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组标准化 RESTful API，严格遵循 OpenAI 的请求/响应格式（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/batches` 等路径）、数据结构（如 `messages` 数组、`choices[0].message.content`）和认证方式（`Authorization: Bearer $API_KEY`），使开发者无需修改业务代码即可将现有 OpenAI SDK（Python/Node.js）、LangChain、LlamaIndex 等框架无缝迁入百炼。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有应用**：已集成 OpenAI SDK 的项目，只需将 `base_url` 替换为百炼业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并确保 `api_key` 为 DashScope API Key，即可直接调用 Qwen、GLM、Kimi、DeepSeek 等数十种模型，零代码改造。
  
- **多模态与专业能力扩展**：通过同一套 `/v1/chat/completions` 接口，传入 `qwen3-vl-plus` 或 `QVQ` 模型 ID，即可支持图像 URL/Base64 输入；传入 `text-embedding-v4` 即可调用[向量嵌入](vector-embedding.md)服务——所有能力均复用 OpenAI 标准字段（如 `content` 中嵌入 `{"type": "image_url", "image_url": {"url": "..."}}`）。

- **高阶智能体开发**：仅 **OpenAI Responses API**（`/v1/responses`）支持原生工具调用（联网搜索、代码解释器、[函数调用](function-calling.md)），适用于构建自主 Agent。注意：该能力仅对百炼直供模型（如 `qwen3.8-max`）开放，第三方模型不支持。

- **性能与成本优化场景**：
  - **Prime 模式**：指定 `model="glm-5.2-fast-preview"` 等 Prime 模型 ID，自动启用低延迟推理，TPS 提升 1.5–2 倍；
  - **吞吐预留（PTU/DTU）**：购买专属资源后，使用分配的 `model-code` 替换模型名，保障高峰期稳定吞吐；
  - **批量处理（Batch）**：上传 JSONL 文件调用 `/v1/batches`，成本降低约 50%，适用于评测、标注等离线任务；
  - **智能路由**：设置 `model="auto-model-xxxxxx"`，由平台根据输入内容、`max_completion_tokens` 等参数动态选择最优模型。

- **会话与上下文管理**：配合 Conversations API（`/v1/conversations`）创建会话，再在 `chat/completions` 请求中传入 `conversation_id`，实现跨请求、跨设备的上下文延续；或使用 Responses API 的 `previous_response_id` 参数自动拼接历史输出，简化多轮逻辑。

> ⚠️ 注意限制：  
> - Qwen-Audio 模型**不支持** OpenAI 兼容协议，必须使用 DashScope 原生接口；  
> - QwQ/QVQ 模型的 `system` 消息无效；  
> - 子业务空间部署的**调优模型不支持 OpenAI 兼容调用**，仅限 DashScope SDK；  
> - 视频理解参数（如 `max_frames`）仅 DashScope 原生协议支持，OpenAI Chat 不识别。

## 关键参数和配置

| 参数 | 必填 | 说明 | 典型值 | 适用接口 |
|------|------|------|--------|----------|
| `base_url` | ✅ | 业务空间专属 endpoint，地域必须与 API Key 一致 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 所有 OpenAI 兼容接口 |
| `model` | ✅ | 模型 ID，需严格匹配[支持列表](https://help.aliyun.com/zh/model-studio/model-list) | `"qwen3.8-max"`, `"text-embedding-v4"`, `"auto-model-xxxxxx"` | 所有 |
| `messages` | ✅（Chat） | 对话消息数组，支持 `user`/`assistant`/`system`（部分模型除外） | `[{"role":"user","content":"你好"}]` | `/v1/chat/completions` |
| `input` | ✅（Embedding） | 文本或文本数组，用于向量生成 | `"hello world"` 或 `["a", "b"]` | `/v1/embeddings` |
| `stream` | ❌（默认 `false`） | 是否启用流式响应 | `true` | 所有 |
| `temperature` | ❌（默认 `0.7`） | 采样温度，取值范围 `[0, 2)` | `0.3` | 所有 |
| `previous_response_id` | ✅（Responses） | 上一轮响应的 `id`，用于自动续写上下文 | `"resp_xxx"` | `/v1/responses` |
| `enable_thinking` | ❌（默认依模型而定） | 控制是否启用深度思考（影响 token 成本与时长） | `false` | Chat / Responses / Batch |
| `dimensions` | ❌（Embedding） | 向量维度（仅 `text-embedding-v3`/`v4` 支持） | `1024` | `/v1/embeddings` |

- **认证方式**：HTTP Header 中传入 `Authorization: Bearer $DASHSCOPE_API_KEY`（非 OpenAI 的 `sk-xxx` 格式）；  
- **文件上传**：多模态调用前需先调用百炼文件上传接口获取 `oss://` URL，并在请求 Header 中添加 `X-DashScope-OssResourceResolve: enable`；  
- **错误处理**：返回标准 HTTP 状态码（如 `400` 参数错误、`401` 认证失败、`429` 限流）及 OpenAI 风格 `error` 对象（含 `code`、`message`、`param`）。

## 面向开发者，简洁实用

- ✅ **即插即用**：安装 `openai==1.40.0+` 或 `langchain_openai`，5 行代码完成迁移：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="YOUR_DASHSCOPE_API_KEY",
      base_url="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(model="qwen3.7-plus", messages=[{"role":"user","content":"你好"}])
  print(response.choices[0].message.content)
  ```

- ✅ **调试友好**：所有请求/响应结构与 OpenAI 官方完全一致，可直接复用 Postman Collection、cURL 示例或 LangChain 日志分析工具；

- ✅ **平滑演进**：当需要启用百炼特有能力（如工具调用、显式缓存、视频抽帧）时，仅需在标准字段中增加兼容性参数（如 `tool_choice="auto"`、`cache_control={"type": "ephemeral"}`），不影响基础功能；

- ⚠️ **避坑提示**：
  - 不要混用 `system` 消息与 QwQ/QVQ 模型；
  - [异步任务](asynchronous-task.md)（图像/视频生成）**不走 OpenAI 兼容接口**，需使用独立 `/api/v1/tasks` 路径；
  - 流式响应中，`reasoning_content` 字段仅在 Prime 模式下随 `delta.reasoning_content` 分块返回，需单独解析。

如需完整支持列表、各模型能力矩阵或 SDK 配置示例，请参考 [Qwen API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference) 与 [工具包与框架指南](https://help.aliyun.com/zh/model-studio/toolkits-and-frameworks)。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [more about models](../api/more-about-models.md)


