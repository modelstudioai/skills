# qwen api reference

本文档提供调用 Qwen 系列文本生成模型的接口规范与开发指南。平台提供多种协议适配，开发者可根据现有技术栈快速接入或启用高级特性。所有接口均遵循统一的鉴权标准与流量管控策略。

## 支持的接口与功能
百炼平台目前开放四种主流调用协议，覆盖从第三方生态迁移到深度定制的开发场景。详细协议说明与能力矩阵可参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

- **OpenAI 兼容 Chat Completions**：完全对齐 OpenAI SDK 规范，支持标准 `chat.completions.create` 调用，迁移现有 LLM 应用成本最低。
- **OpenAI 兼容 Responses**：服务端内置联网搜索、代码解释器与网页内容提取 Agent，自动管理对话上下文，无需客户端手动维护状态。
- **Anthropic 兼容 Messages**：遵循 `anthropic` SDK 规范，原生支持模型思考过程（Thinking）与 Tool Use 结构化调用。
- **DashScope 原生接口**：提供最全的参数集与高级控制能力，适合对输出格式、系统提示词模板有精细化需求的场景。

## 关键参数
不同协议的核心请求体结构存在差异，但生成控制逻辑保持一致。建议在集成前通过 [[parameter-validation]] 进行字段校验。

| 参数 | 说明 | 适用协议 |
|------|------|----------|
| `model` | 指定模型标识（如 `qwen-turbo`, `qwen-max`, `qwen-plus`），需严格匹配当前可用模型池。 | 全部 |
| `messages` / `input` | 多轮对话数组或单轮输入文本，包含 `role`（`system`, `user`, `assistant`）与 `content`。 | 全部 |
| `temperature` / `top_p` | 控制输出随机性与多样性的超参数，二者通常只生效其一，建议仅配置其一。 | 全部 |
| `max_tokens` | 限制单次返回的最大 Token 数量，超出截断或触发结束符。 | 全部 |
| `stream` | 开启 SSE 流式响应，显著降低首字延迟（TTFT）。 | 全部 |
| `tools` / `tool_choice` | 外部工具定义与调用策略，用于 Function Calling。 | Chat/Responses/Messages/DashScope |

> **注意**：Responses 接口会自动管理历史上下文，无需手动拼接完整 `messages`；而 DashScope 与 Anthropic Messages 需客户端显式传递完整历史，否则模型将丢失前序状态。旧版示例代码中若出现非标准字段（如 `frequency_penalty` 硬编码为固定值），可能已与实际服务端实现不一致，请以最新 SDK 定义为准。

## 使用方式
1. **获取凭证**：在控制台生成 [[api-key]]，并通过环境变量 `DASHSCOPE_API_KEY` 或 `OPENAI_API_KEY` 注入。
2. **选择 SDK**：根据目标协议安装对应客户端（`openai`, `anthropic`, 或 `dashscope`）。协议对照与基础调用模板详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
3. **构造请求**：初始化客户端，配置 `base_url`（如需使用非默认网关），传入 `model` 与业务参数。
4. **处理响应**：同步请求等待完整 JSON；流式请求需逐块解析 `choices[0].delta` 或对应结构，并处理 `finish_reason` 终止逻辑。
5. **异常重试**：建议实现指数退避重试逻辑，重点处理 HTTP 429（限流）与 5xx 服务抖动。

## 限制和注意事项
- **并发与配额**：各模型规格均设有默认 RPM（每分钟请求数）与 TPM（每分钟 Token 数）上限。高并发业务需提前通过工单或控制台申请 [[rate-limit]] 扩容。
- **上下文窗口**：模型存在最大输入长度限制（如 32k/128k Token）。超出窗口时，系统可能丢弃最早的历史片段，建议业务层实现滑动窗口或摘要压缩。
- **计费口径**：所有协议均按实际消耗的输入/输出 Token 数阶梯计费。Thinking 过程产生的中间 Token 会计入输出侧，需在预算模型中单独核算。
- **网络与超时**：流式响应受网络质量影响较大，建议客户端设置合理的连接超时（Connection Timeout）与读取超时（Read Timeout）。

> **注意**：部分早期文档中提及的 `qwen-vl` 视觉理解接口已独立拆分至多模态专用网关。纯文本生成项目请勿混用端点，最新路由规范请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)

