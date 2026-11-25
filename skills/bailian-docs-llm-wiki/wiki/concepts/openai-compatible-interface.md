# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI API 规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/files` 等）的标准化模型调用入口，使开发者无需修改业务代码逻辑，仅通过切换 `base_url` 和 `api_key` 即可将现有 OpenAI 生态应用（包括 SDK、LangChain、LlamaIndex、各类 IDE 插件等）快速迁移至百炼平台。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理**：通过 `/v1/chat/completions` 调用 `qwen4-max`、`qwen3.8-*`、`qwen-vl`、`qwen-omni` 等文本与多模态模型；通过 `/v1/embeddings` 调用 `text-embedding-v4`、`qwen3.7-text-embedding` 等嵌入模型；注意 `qwen-audio` 明确不支持 OpenAI 兼容协议，仅可通过 DashScope 原生接口访问。
- **智能体开发**：通过 `/v1/agents/chat/completions` 使用具备工具调用、Session 状态保持和环境隔离能力的 Agent 服务，当前仅支持 `qwen-plus` 和 `qwen-max` 模型。
- **复杂对话与 Agent 编排**：通过 `/v1/responses`（OpenAI 兼容 Responses 接口）构建生产级对话 Agent，内置联网搜索、代码解释器、文搜图、知识库检索等工具，并支持 `previous_response_id` 多轮串联与自动 Session 缓存。
- **文件与批量处理**：通过 `/v1/files` 上传文档用于内容提取（`purpose=file-extract`）或批量任务（`purpose=batch`）；通过 `/v1/batches` 提交异步批量推理任务，显著降低成本。
- **会话管理**：通过 `/v1/conversations` 自动维护跨设备、跨请求的上下文状态，与 `/v1/responses` 配合实现原生多轮交互体验。
- **Token Plan 工具集成**：在 Qoder、Trae、Qwen Code 等 AI 编程助手或智能体开发工具中，配置 Token Plan 专属 `sk-sp-` 密钥与 OpenAI 兼容 Base URL（如 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），即可零代码接入百炼能力。

## 关键参数和配置

- **必填认证参数**：
  - `base_url`：必须为业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），**不可使用 `dashscope.aliyuncs.com`**；Token Plan 用户需使用其专用地址。
  - `api_key`：必须匹配 `base_url` 所属产品体系（百炼用 `sk-xxx`，Token Plan 用 `sk-sp-xxx`），且严格按地域隔离（如北京 Key 不可用于调用弗吉尼亚 endpoint）。
- **核心请求参数**：
  - `model`：字符串，大小写敏感，必须严格匹配支持列表（如 `"qwen4-max"`、`"text-embedding-v4"`）；Token Plan 场景下该字段常被网关忽略。
  - `messages`：Chat 类接口必填，数组格式，`role` 仅支持 `user`/`assistant`/`system`；`system` 在 `qwen-omni` 和 `qwen-vl` 中可能被忽略。
  - `input`：Responses 接口使用，支持 string 或 array，且额外支持 `developer` 角色用于调试注入。
  - `stream`：布尔值，启用流式响应（默认 `false`）；流式末尾统计需显式设置 `stream_options.include_usage: {"include_usage": true}`。
  - `previous_response_id`：Responses API 多轮必需，传上一轮响应顶层 `id`（非 `output[].id`）。
  - `session_id`：Agents API 可选，用于复用已有 Session 的上下文与工具执行历史。
- **高级控制参数**：
  - `reasoning.effort`（仅 Responses）：取值 `none`/`low`/`medium`/`high`，控制推理深度并影响计费。
  - `x-dashscope-session-cache: enable`（仅 Responses）：请求头启用服务端自动上下文缓存。
  - `enable_thinking`（Batch 场景）：必须作为 JSONL 请求体顶层字段（与 `model` 同级），不可置于 `extra_body`。

## 面向开发者，简洁实用

- ✅ **快速迁移**：用 OpenAI Python SDK 时，只需 `client = OpenAI(api_key="sk-xxx", base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")`，后续调用完全一致。
- ✅ **生态兼容**：原生支持 LangChain 的 `ChatOpenAI`、LlamaIndex 的 `OpenAIEmbedding` 等封装，无需适配层。
- ⚠️ **避坑提示**：
  - `qwen-audio` 不支持任何 OpenAI 兼容路径，请改用 DashScope 原生接口；
  - Token Plan 的 `sk-sp-` 密钥**严禁混用**百炼或 Coding Plan 的 `base_url`，否则触发鉴权失败或意外按量扣费；
  - Agents API 仅 `qwen-plus`/`qwen-max` 支持完整能力，其他模型返回 `400 Unsupported model`；
  - Batch 场景下 `enable_thinking` 必须为顶层字段，示例代码若未体现此结构，请以文档说明为准；
  - 所有 OpenAI 兼容接口均推荐使用业务空间专属域名，旧域名性能与稳定性较低。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [file management api](../api/file-management-api.md)


