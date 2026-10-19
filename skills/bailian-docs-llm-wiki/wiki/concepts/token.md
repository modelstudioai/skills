# Token（令牌）

Token 是百炼平台中用于衡量模型输入与输出文本（或多媒体内容）长度的基本计量单位，本质上是模型对原始内容进行分词（tokenization）后产生的最小语义单元。一个 token 可能是一个字符、一个单词、一个子词（subword）或一个标点符号；中文场景下通常对应一个汉字、一个词或一个标点，具体取决于所用模型的 tokenizer 实现。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型 API 调用（`/v1/chat/completions` 等）**：`max_tokens` 参数明确限制模型单次响应最多生成的 token 数；同时，整个 `input.messages` 的总长度（含 system/user/assistant 内容及内部结构标记）也以 token 数计，受模型上下文窗口（如 32K、128K）硬性约束——超限将直接返回 `400 Bad Request`。
  
- **Application Call（智能体/工作流调用）**：虽然接口层不显式暴露 token 计数，但底层仍严格遵循上下文窗口限制。当启用 RAG、长期记忆或复杂多轮对话时，历史消息、检索片段、工具描述等均计入 token 总量；若实际 token 数超限，服务端可能静默截断或返回 `context_length_exceeded` 错误。

- **Realtime API 与 Omni Realtime API**：所有实时流式接口均以 token 为粒度增量返回响应（Delta Frame），开发者可通过监听 `delta.text` 字段感知 token 级别生成节奏；`max_tokens` 同样生效，且部分模型（如 `qwen3.8-omni-flash-realtime`）支持高达 65536 的上限，适用于长文档摘要、会议转录等场景。

- **配额与限流**：平台动态限流策略（如 QPS、并发数）虽不直接按 token 计费，但 token 消耗量是后台资源调度与成本核算的核心依据；控制台「用量统计」中展示的“Token 使用量”即为此概念的实际累计值，用于账单结算与用量预警。

## 关键参数和配置

| 参数名 | 所属接口 | 类型 | 说明 | 常见取值 |
|--------|----------|------|------|-----------|
| `max_tokens` | 全部模型/应用/实时 API | integer | 单次响应最大生成 token 数 | `1024`（默认），`1~65536`（依模型而定） |
| `input.messages` 长度 | 模型 API / Application（Responses） | — | 输入消息数组经 tokenizer 编码后的总 token 数 | 需自行预估或调用 `/v1/tokenize` 接口校验 |
| `X-RateLimit-Remaining` | 所有 API 响应头 | string | 当前配额周期内剩余可调用次数（非 token 数），但 token 消耗速率影响其衰减速度 | 如 `"4"` |

> ⚠️ 注意：百炼平台**不提供公开的 `tokenize` 接口供生产环境实时调用**。建议在开发阶段使用 SDK 中的 `count_tokens()` 工具函数（Python/Java 支持），或参考 [Tokenizer 工具页](https://help.aliyun.com/zh/model-studio/tokenizer-tool) 进行离线估算；中文文本可粗略按「字数 × 1.3」、英文按「单词数 × 1.2」预估，但最终以模型实际编码为准。

## 面向开发者，简洁实用

- ✅ **必做**：始终显式设置 `max_tokens`，避免因平台默认值变更导致响应被意外截断；
- ✅ **必查**：在构造长对话或多模态输入前，用 SDK 工具或控制台调试器验证 token 总量是否低于模型上下文窗口；
- ✅ **必控**：流式场景下，若需精确控制响应长度（如语音合成对齐），应基于 `delta.text` 累计 token 数，而非字符数或字数；
- ❌ **勿依赖**：不要假设 token 数与字符数/字数严格线性对应——同一句话在不同模型（Qwen2 vs Qwen-VL）或不同语言（中/英/代码）下 token 化结果差异显著；
- 📈 **监控建议**：在日志中记录每次请求的 `prompt_tokens` 和 `completion_tokens`（响应头 `X-DashScope-Prompt-Tokens` / `X-DashScope-Completion-Tokens`），用于性能分析与成本优化。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


