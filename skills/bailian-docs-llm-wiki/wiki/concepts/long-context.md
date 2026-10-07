# 长上下文

长上下文（Long Context）指大语言模型在单次推理中能够有效处理和理解的输入文本长度，通常以 token 数量为单位衡量。百炼平台支持最高 32K tokens 的输入上下文长度，使模型可处理长文档、多轮复杂对话历史、大规模代码文件或结构化知识片段，显著提升 RAG、文档摘要、代码分析等场景的准确性与完整性。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用文本生成（API/SDK 调用）**：当 `input.messages` 中所有消息（含 system、user、assistant 角色内容）的总 token 数 ≤ 32768 时，请求可正常执行；超出将返回 `400 Bad Request` 错误（`code: InvalidParameter.InputLengthExceeded`）。适用于需传入完整日志、合同全文、会议纪要等长输入的定制化应用。

- **RAG 知识库问答**：RAG API 自动对知识库切片进行检索与拼接，最终构造的 [prompt](../guides/prompt.md) 上下文（含检索出的 top_k 个 chunk + 用户 query + 系统指令）同样受 32K token 总长限制。若检索结果过大，系统会按优先级截断低相关性切片，确保 [prompt](../guides/prompt.md) 可被模型接收——开发者无需手动分块，但应合理设置 `top_k`（建议 ≤5）并启用 `enable_rerank` 提升关键信息保留率。

- **零代码知识库应用**：控制台构建的问答应用默认启用长上下文能力，上传的 PDF/Word/TXT 文档在切片、向量化及召回阶段均适配 32K 上下文窗口。用户提问时，系统自动注入最相关的上下文片段，无需配置额外参数。

- **高吞吐/低延迟推理（Prime 模式、吞吐预留）**：长上下文能力与性能加速模式完全正交——所有支持长上下文的模型（如 `qwen-plus`, `qwen-max`），在启用 Prime 或吞吐预留后，上下文长度上限保持不变（仍为 32K），且 token 缓存（`cached_tokens`）机制对长 [prompt](../guides/prompt.md) 的重复部分仍生效，可降低实际计费 token 量。

## 关键参数和配置

- **无显式开关参数**：长上下文是模型原生能力，由所选 `model` 决定。仅当使用明确标注支持长上下文的模型（如 `qwen-plus`, `qwen-max`, `qwen-turbo`）时可用；旧版小模型（如 `qwen-1.8b`）不支持，调用将失败。

- **输入长度校验**：可通过 SDK 的 `dashscope.Tokenizer` 或服务端返回的 `usage.prompt_tokens` 字段实时监控输入长度；建议在业务侧预估 token 数（中文约 1 字符 ≈ 1.5–2 tokens），避免临界超限。

- **输出长度限制**：长上下文仅约束输入，输出仍受模型自身限制（如 `qwen-plus` 最大输出为 8192 tokens），需通过 `parameters.max_output_tokens`（如有）或响应截断逻辑做兜底。

- **流式响应兼容性**：启用 `stream: true` 时，长上下文输入不影响流式生成，但首 token 延迟可能随输入长度增加而上升，建议结合客户端超时设置（如 `timeout=120s`）。

## 面向开发者，简洁实用

- ✅ **推荐做法**：对长文档类输入，优先使用 RAG API 或知识库应用，由平台自动优化上下文构造；自定义 prompt 时，用 `system` 消息精简指令，用 `user` 消息组织核心内容，避免冗余描述。

- ⚠️ **避坑提示**：不要依赖模型“记住”超长历史——32K 是单次请求上限，非会话状态持久化；多轮对话需由业务层维护 history 并显式传入，同时注意累计 token 不超限。

- 🔍 **调试技巧**：若遇到 `InputLengthExceeded`，用 `dashscope.Tokenizer.encode(text)` 本地估算 token 数；若响应被意外截断，检查 `usage.completion_tokens` 是否接近模型输出上限，并确认未开启 `max_output_tokens` 限制。

- 📏 **实测参考**：32K tokens ≈ 2.4 万汉字（纯中文）、约 200 页 A4 文档（标准排版）、或 8000 行 Python 代码。

## 关联主题页

- [start using](../guides/start-using.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [more about models](../api/more-about-models.md)
- [rag api](../api/rag-api.md)


