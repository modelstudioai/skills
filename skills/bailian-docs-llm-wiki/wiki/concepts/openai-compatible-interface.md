# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 RESTful API 协议，完全遵循 OpenAI 的请求结构、响应格式与错误规范（如 `/v1/chat/completions`、`/v1/embeddings` 等路径），使开发者无需修改代码逻辑即可将现有基于 OpenAI SDK 或工具链（如 LangChain、LlamaIndex、Cursor、Dify）的应用快速迁入百炼，调用千问全系列及主流第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速接入与迁移**：开发者可直接复用 `openai` Python SDK（v1.0+）或 `@langchain/openai` 等标准客户端，仅需替换 `base_url` 和 `api_key`，即可调用文本生成、多模态理解、[向量嵌入](embedding.md)、文件处理、批量推理等能力，大幅降低集成成本。  
- **多模态统一调用**：通过 `/chat/completions` 接口，支持图像（`image_url`）、音视频（`video`）、文档（`file_id`）等多模态输入，无需切换协议；`qwen3.8-omni-flash` 等模型在该接口下原生支持端到端音视频理解。  
- **智能体（Agent）开发**：`/responses` 接口是 OpenAI 兼容体系中的增强型能力入口，内置联网搜索、网页抓取、代码解释器等工具调用能力，并支持 `previous_response_id` 实现轻量级上下文延续，适用于构建自主决策型应用。  
- **会话状态管理**：配合 `/conversations` 接口（`POST /conversations`, `POST /conversations/{id}/items`），可跨设备持久化对话历史，与 `/responses` 联用实现长周期、高一致性 Agent 交互。  
- **部署与生产适配**：所有部署类型（Token 按量、PTU 预置吞吐、DTU 独占算力、专属实例）均通过同一套 OpenAI 兼容接口对外暴露，业务侧无需感知底层资源形态；智能路由自动将请求分发至最优实例，保障 SLA。

> ⚠️ 注意：Qwen-Audio 系列模型（如 ASR/TTS）**不支持** OpenAI 兼容协议，必须使用 DashScope 原生接口；QVQ 模型在 OpenAI 接口中不支持 `system` 消息，且仅支持[流式输出](streaming-output.md)。

## 关键参数和配置

| 参数 | 必需 | 说明 | 示例值 |
|------|------|------|--------|
| `base_url` | 是 | OpenAI 兼容接口的根地址，**必须使用业务空间专属域名**（推荐生产环境），旧域名（`dashscope.aliyuncs.com`）已逐步停用 | `https://llm-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | 是 | 与 `base_url` 所属计费方案严格绑定（如业务空间 Key 不能用于 Token Plan 域名） | `sk-xxx` |
| `model` | 是 | 模型 ID，区分大小写与版本后缀；不同接口支持范围不同（如 `/responses` 仅支持 `qwen3.8-*` 主力型号） | `"qwen3.8-max"`, `"deepseek-v4-pro-0813"` |
| `messages` | 是（`/chat/completions`） | 标准 OpenAI 消息数组，支持 `user`/`assistant`/`system` 角色；多模态内容需按规范嵌入（如 `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}`） | `[{"role": "user", "content": "你好"}]` |
| `previous_response_id` | 是（`/responses`） | 上一轮 `/responses` 返回的顶层 `id`（UUID 字符串），用于自动继承上下文与工具执行状态 | `"resp_abc123..."` |
| `temperature` / `max_tokens` | 否 | 控制生成行为；注意：`temperature` 在 OpenAI 接口取值范围为 `[0, 2)`，非 `[0, 1]`；`max_tokens` 在 `/chat/completions` 中仅限制输出长度，在 `/responses` 中默认限制输出（思考 token 单独计） | `0.7`, `1024` |
| `enable_thinking` | 否（Qwen3/R1 模型推荐启用） | 显式开启 Qwen3 系列模型的 R1 思考模式（Reasoning + Response），否则可能返回 `400 InternalError.Algo.InvalidParameter` | `true` |

> ✅ 提示：所有 OpenAI 兼容接口均要求 `Content-Type: application/json`，并使用 `Authorization: Bearer <api_key>` 认证；请求体必须为合法 JSON，空字段（如 `null`）可能导致解析失败。

## 面向开发者，简洁实用

- **一句话启动**：  
  ```bash
  curl -X POST https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer sk-xxx" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "qwen3.8-max",
          "messages": [{"role": "user", "content": "你好，请用中文简要介绍你自己"}]
        }'
  ```

- **SDK 快速上手（Python）**：  
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="sk-xxx",
      base_url="https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "你好"}]
  )
  print(response.choices[0].message.content)
  ```

- **避坑指南**：  
  - ❌ 不要用 `dashscope.aliyuncs.com` 作为生产 `base_url`（新特性已停用）；  
  - ❌ 不要将 Token Plan 的 Key 用于业务空间专属域名；  
  - ❌ 不要在 `messages` 中传入非法 `system` 消息给 QVQ/QwQ 模型；  
  - ✅ 优先使用 `workspace_id` 专属域名 —— 更低延迟、更高并发、业务隔离；  
  - ✅ 调试时用 `curl -v` 查看完整响应头与错误码（如 `429` 表示限流，`401` 表示 Key 不匹配）。  

如需查看支持模型列表、地域可用性或详细参数说明，请访问 [模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market) 及对应 API 文档页。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [model deployment index](../guides/model-deployment-index.md)


