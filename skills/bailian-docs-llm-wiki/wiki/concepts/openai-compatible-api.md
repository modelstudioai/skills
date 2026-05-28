# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套完全对齐 OpenAI SDK 与 REST API 规范的服务网关。开发者无需修改现有工程架构，仅需切换 `base_url` 与鉴权凭证，即可无缝调用千问全系列模型、主流第三方大模型及百炼智能体/工作流应用。

## 在百炼平台的核心应用场景
该接口已全面打通平台的基础模型、生态工具、业务应用与多模态服务，主要覆盖以下场景：
- **基础模型直调**：通过 `/compatible-mode/v1` 路径提供 `Chat Completions`（标准多轮对话）与 `Responses`（服务端自动托管上下文）两种范式，覆盖文本、视觉、向量化及重排序任务。
- **第三方生态集成**：为 Cursor、Claude Code、Dify、Postman 等主流 IDE、CLI 编程助手与低代码平台提供标准接入点，实现零成本迁移现有 LLM 应用。
- **应用与智能体调用**：通过 OpenAI 兼容 Responses API 调用平台发布的 [[智能体应用]] 与 [[工作流应用]]，支持同步/异步执行与 SSE [[streaming-output|流式输出]]。
- **语音与音视频翻译**：兼容标准 `chat.completions` 结构，支持公网 URL 输入与强制流式返回译文/音频，适用于 Web 后端批量处理场景。

## 关键参数与配置
接入时需严格匹配地域路由与协议规范，核心配置项如下：

| 参数 | 说明与约束 |
|:---|:---|
| `base_url` | **地域隔离**。北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`；弗吉尼亚：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`。严禁混用协议路径后缀。 |
| `api_key` | **鉴权凭证**。强烈建议通过环境变量（如 `DASHSCOPE_API_KEY`）注入。Key 与地域及 [[计费方案]]（按量/Coding Plan/Token Plan）强绑定，不可跨套餐或跨地域复用。 |
| `model` | **模型标识**。需与控制台当前地域可用列表严格一致。特定地域或功能版模型需使用对应后缀（如 `-us`、`-latest`）。 |
| `messages` / `input` | Chat 模式需客户端全量拼装历史；Responses 模式支持传入 `previous_response_id` 实现上下文自动关联（有效期 7 天）。 |
| `stream` | 推荐开启 `true` 降低首字延迟。音视频翻译、思考模式场景下为强制必填。 |
| `extra_body` | 非 OpenAI 标准参数（如 `translation_options`、`enable_thinking`、`corpus`）在 Python SDK 中必须置于该对象内传递。 |

## 使用方式与开发建议
1. **SDK 初始化**：安装官方 `openai` 多语言 SDK，覆盖 `api_key` 与 `base_url` 即可复用原有 `client.chat.completions.create` 逻辑。
2. **上下文管理**：长对话建议客户端实现滑动窗口裁剪或摘要压缩，避免触发模型上下文窗口超限。生产环境建议开启 `stream_options: {"include_usage": true}` 获取精确 Token 消耗。
3. **异步与批处理**：耗时任务可设置 `background: true`（与 `stream` 互斥）获取 `task_id` 后轮询；大规模离线处理推荐使用 `Batch File` 接口上传 JSONL，享受 50% 费用优惠且不受实时限流约束。
4. **容错机制**：客户端需捕获 HTTP 429（触发 [[rate-limit-policy]]）与 5xx 错误，结合指数退避算法与熔断降级策略保障服务高可用。

## 限制与注意事项
- **协议强约束**：开启 `enable_thinking=true` 时必须同步设置 `stream=true`，否则返回 400 校验错误；使用 `response_format: {"type": "json_object"}` 需在 Prompt 显式声明 `json` 并关闭思考模式。
- **套餐使用边界**：Coding Plan 与 Token Plan 团队版 **仅限** AI 编程工具与 Agent 客户端使用，接入 Dify/n8n 等自动化平台或自定义后端将被视为违规，可能导致 Key 封禁。
- **异步与流式互斥**：应用调用场景下，`background=true`（后台异步）与 `stream=true`（SSE 实时流）不可同时开启。
- **路径演进**：旧版兼容端点已逐步下线，新项目请统一采用 `{WorkspaceId}.地域.maas.aliyuncs.com/compatible-mode/v1` 标准路由。限流阈值、可用模型及功能矩阵动态迭代，集成前请以控制台 [[模型总览]] 与 [[model-monitoring]] 实时数据为准。

## 相关主题
[[api-key]] | [[rate-limit-policy]] | [[billing]] | [[thinking-mode]] | [[structured-output]] | [[batch-inference]] | [[model-monitoring]] | [[计费方案]]

## 关联主题页

- [[get-started-with-models|get started with models]] — `../guides/get-started-with-models.md`
- [[use-chat-client-or-development-tool|use chat client or development tool]] — `../guides/use-chat-client-or-development-tool.md`
- [[qwen-api-reference|qwen api reference]] — `../api/qwen-api-reference.md`
- [[preparations|preparations]] — `../api/[[preparations|preparations]].md`
- [[toolkits-and-[[frameworks|frameworks]]|toolkits and frameworks]] — `../api/toolkits-and-[[frameworks|frameworks]].md`
- [[application-call|application call]] — `../api/application-call.md`
- [[speech-translation-api-reference|speech translation api reference]] — `../api/speech-translation-api-reference.md`

