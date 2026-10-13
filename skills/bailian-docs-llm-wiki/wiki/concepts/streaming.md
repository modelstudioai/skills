# 流式输出

流式输出（Streaming）是指模型 API 在生成响应过程中，将结果以连续、分块（chunk）的方式逐步返回给客户端，而非等待整个响应生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户体验，尤其适用于长文本生成、实时对话、前端渐进渲染等场景。

## 在百炼平台的不同场景中如何使用

- **标准对话（Chat Completions）**：所有支持流式的 Qwen 文本模型（如 `qwen3.8-max`、`qwen3.7-plus`）均通过 [OpenAI 兼容接口](openai-compatibility.md)提供流式能力。客户端设置 `stream=true` 后，服务端按 token 或语义单元（如句子）分 chunk 返回 `delta.content`，开发者可实时消费并渲染。
  
- **增强智能体（Responses API）**：在调用内置工具链（如 `web_search`、`code_interpreter`）时，流式输出不仅包含最终答案，还可逐段返回思考过程（`delta.reasoning`）、工具调用日志（`delta.tool_calls`）和中间执行结果，便于构建透明、可控的 Agent 应用。

- **多模态与文件处理**：当前流式能力**暂不支持**图像/视频/音频等多模态输入的解析过程流式化；但若请求含 `input_video` 且模型为 `qwen3.8-omni-flash`，其文本生成部分仍可流式返回。文件类 API（Files、Batch）本身为异步批量接口，不提供流式响应。

> ⚠️ 注意：Qwen-Audio 模型**不支持 OpenAI 兼容协议**，因此无法使用 `stream=true`；必须通过 DashScope 原生协议调用，且原生协议当前亦不支持音频模型的流式输出。

## 关键参数和配置

- `stream`: 布尔值，必需设为 `true` 以启用流式输出（默认为 `false`）。  
- `stream_options`: 对象，可选，用于控制流式行为：
  - `include_usage: true`：在最后一个 chunk 中附加 `usage` 字段（含 `prompt_tokens`、`completion_tokens`、`total_tokens`），便于精确计费与监控。
- 兼容性要求：
  - 必须使用 `/compatible-mode/v1/chat/completions` 或 `/compatible-mode/v1/responses` 等新版 OpenAI 兼容路径；
  - `base_url` 需指向业务空间专属域名（如 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`），旧域名（如 `dashscope.aliyuncs.com`）虽能响应，但流式稳定性与低延迟保障不足，**不推荐生产使用**；
  - 模型 ID 必须为明确支持流式的型号（参见各模型文档的能力矩阵），`qwen-audio`、`qwq`、`qvq` 等模型不支持。

## 开发者提示

- 客户端需正确处理 Server-Sent Events（SSE）格式：每行以 `data:` 开头，空行分隔 chunk；最后一行通常为 `data: [DONE]`。
- 不要依赖 chunk 的大小或频率——模型可能因内容长度、token 化策略或内部优化而动态调整分块粒度。
- 若需结构化输出（如 JSON），请搭配 `output_config.format.json_schema`（Anthropic 协议）或 Responses API 的 `response_format` 参数使用，流式下仍保证最终输出合法，但中间 chunk 可能不完整。
- 流式请求同样受动态限流约束：QPS 按请求次数计，Token 数按实际消耗加权统计，请合理设计重试与降级逻辑。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


