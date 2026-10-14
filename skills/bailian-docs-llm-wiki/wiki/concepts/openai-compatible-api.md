# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 REST API 协议，完全遵循 OpenAI 官方 API 的路径、请求/响应格式、参数命名与语义规范，使开发者能直接复用现有 OpenAI SDK（如 `openai==1.0+`）和代码逻辑，零改造接入千问（Qwen）全系列及主流第三方模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速原型验证**：无需部署模型或维护服务，仅配置 `api_key`、`base_url` 和 `model`，几分钟内即可调用 `qwen3.8-plus` 等文本模型或 `qwen3.8-omni-flash` 等多模态模型，适用于 MVP 开发与 A/B 测试。  
- **生产级集成**：通过业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）接入，获得流量隔离、高吞吐（TPM 可达数万）、低延迟（P95 < 300ms）与 SLA 保障，支撑高并发 AI 应用。  
- **多协议平滑迁移**：同一套客户端代码可切换调用 OpenAI 兼容、Anthropic 兼容或 DashScope 原生协议（只需改 `base_url`），便于技术栈演进与模型能力对比。  
- **工具链复用**：支持 Cursor、Dify、Postman、LangChain、LlamaIndex 等主流开发工具与框架，无需适配新 SDK；CLI 工具（如 Kilo CLI）、IDE 插件（如 Qwen Code）和 Web UI（如百炼控制台 Chatbox）均原生兼容。  
- **高性能推理加速**：所有加速方案（Prime 模式、吞吐预留、批量推理、智能路由、专属部署）均基于 OpenAI 兼容接口暴露，仅需替换 `model` 参数（如 `glm-5.3-prime` 或 `auto-model-2026-0908`），无需修改调用逻辑。

## 关键参数和配置

| 参数 | 必填 | 类型 | 说明 | 注意事项 |
|------|------|------|------|----------|
| `api_key` | ✅ | string | 从 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 创建的密钥，**严格绑定地域与计费方案**（如 [Token](token.md) Plan 团队版 Key 不可用于 Coding Plan） | 不同地域 Key 不通用；试用 Key RPM 限流为 1000 |
| `base_url` | ✅ | string | 接入端点，**必须使用业务空间专属域名**：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 需替换为控制台获取的真实 ID；`{region}` 如 `cn-beijing`、`ap-southeast-1`；DashScope 域名（`dashscope.aliyuncs.com`）将于 2026 年 9 月 30 日停用新特性 |
| `model` | ✅ | string | 模型 ID，**必须与当前地域、计费方案、接口类型三者匹配**（如 `qwen3.8-max` 支持 `chat/completions` 和 `responses`，但 `qwen-coder-turbo-latest` 仅支持 `completions`） | 不支持别名或大小写变体；`Qwen-Audio` 系列模型**明确不支持**该协议，仅可用 DashScope 原生协议 |
| `messages` | ✅（`chat/completions`） | array | 对话消息数组，格式严格遵循 OpenAI：<br>`[{ "role": "system", "content": "..." }, { "role": "user", "content": "..." }]` | 多模态模型支持 `content` 为混合类型数组（字符串 + 图像/视频对象）；`system` 角色在 `QwQ` 中不生效，在 `QVQ` 中被忽略 |
| `stream` | ❌ | boolean | 是否启用流式响应 | 设为 `true` 时，支持 `stream_options={"include_usage": true}` 在末尾 chunk 返回 token 统计 |
| `enable_thinking` | ⚠️（按需） | boolean | 控制是否启用深度思考模式（仅 `qwen3.5+` 及部分加速方案支持） | 批量推理中即使设为 `true`，结果文件也**不返回** `reasoning_content` 字段；必须作为 `body` 顶层参数传入，不可置于 `extra_body` 内 |
| `dimensions` | ⚠️（Embedding） | number | 指定向量维度（仅 `text-embedding-v3/v4` 支持） | `v1/v2` 嵌入模型忽略此参数；稀疏向量（`output_type=sparse`）**不支持** |

> 💡 提示：所有 OpenAI 兼容接口路径统一为 `/compatible-mode/v1/{endpoint}`，常用端点包括：  
> - `chat/completions`（标准对话）  
> - `completions`（补全模式，适用于代码生成等）  
> - `responses`（内置工具调用，支持联网搜索、知识库、代码解释器等）  
> - `embeddings`（向量生成）  
> - `batch`（异步批量处理，需 JSONL 文件提交）

## 面向开发者，简洁实用

- ✅ **开箱即用**：复制粘贴示例代码，替换 `WorkspaceId` 和 `model` 即可运行。  
- ✅ **零学习成本**：参数名、错误码（如 `401 Unauthorized`, `429 Rate Limited`）、重试策略与 OpenAI 官方完全一致。  
- ✅ **调试友好**：支持 `curl` 直接调用，响应结构清晰（含 `id`, `object`, `created`, `usage` 等标准字段）。  
- ⚠️ **避坑提醒**：  
  - 不要混用计费方案凭证（[Token](token.md) Plan Key + Coding Plan URL → `401`）；  
  - 不要在 `Qwen-Audio` 场景下误用 OpenAI 兼容接口（必报错）；  
  - `max_frames`、`reasoning.effort` 等高级参数**仅 DashScope 原生协议支持**，OpenAI 兼容接口中无效；  
  - 智能路由要求 `max_completion_tokens`（非 `max_tokens`），且会自动过滤不支持该参数的备选模型。  

立即开始：[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) → [创建业务空间](https://bailian.console.aliyun.com/cn-beijing/settings/workspace) → [调用第一个 API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


