# Token

Token 是百炼平台中用于计量模型调用资源消耗的最小计费与配额单位，代表模型输入或输出内容经原生分词器（tokenizer）处理后生成的语义单元（如子词、标点、空格、换行符等）。所有 API 调用的用量统计、配额控制、计费结算均以 token 为统一基准，其计算逻辑严格对齐对应模型的官方 tokenizer 行为。

## 在百炼平台的不同场景中，这个概念如何使用

- **用量计量与计费**：每次 API 调用的 `input_tokens`（含 system prompt、user message、history messages 全部原始文本，含 JSON 符号、空格、换行）和 `output_tokens`（实际生成的 tokens，含截断部分）均被精确统计，并计入绑定的 Token Plan 配额。计费按千 token（k-token）为单位，实时扣减。
- **配额管控**：通过 Token Plan 实现多层级（user/workspace/app）的 token 消耗限制，包括月度总配额（`total_quota`）、突发配额（`burst_quota`）及单次响应上限（`max_tokens`）。配额不足时请求直接拒绝（HTTP 403），并返回 `X-RateLimit-Remaining: 0` 响应头。
- **高加速能力计量**：吞吐预留（TPM）以「tokens per minute」为容量单位，需按输入/输出 token 分别预购 kTPM；Prime 模式虽不改变 token 计费逻辑，但其性能提升效果（1.5–2× TPS）直接影响单位时间内的 token 处理吞吐量。
- **异步与多模态场景**：异步任务（如文生图、语音转写）的输入/输出 token 同样纳入 Token Plan 统一计量；上传图像/视频等文件生成的 `oss://` URL 在调用时被解析为等效文本描述（如 base64 片段或元数据摘要），其解析开销也计入 input tokens。
- **安全凭证隔离**：临时 API Key（`st-***`）本身不携带 token 配额，其调用产生的 token 消耗归属所绑定的主账号或工作空间的 Token Plan；子业务空间（workspace）的模型调用，token 计量与配额作用域严格限定在该空间内。

## 关键参数和配置

- `max_tokens`：单次请求允许的最大输出 token 数（硬限制，超限将截断并返回 HTTP 400）。取值范围为 `[1, 模型最大输出长度]`，需根据模型文档确认上限（如 `qwen3-235b` 为 8192）。
- `total_quota`：账户或工作空间级月度总 token 配额（单位：千 token），每月 1 日 UTC+0 00:00 自动重置。超出后所有绑定该 Plan 的 API Key 请求均被拒绝。
- `burst_quota`：突发配额（单位：千 token），用于应对瞬时流量高峰，按小时重置。团队版中默认为 `0`，须由管理员显式配置生效。
- `quota_scope`：配额作用域，支持 `user`（个人）、`workspace`（工作空间）、`app`（应用）三级，决定配额继承关系与共享范围（例如 workspace 级配额可被其下所有 user 共享）。
- `stream` 与 `incremental_output`：影响 token 流式返回行为——启用流式时，`output_tokens` 按 chunk 累计上报；`incremental_output=true` 可确保 reasoning content 等中间 token 被完整计量。

> ⚠️ 注意：token 计算包含所有原始输入字符（含 JSON 结构符、空格、换行），不可通过精简格式规避配额；分词结果与模型原生 tokenizer 完全一致，不提供自定义分词选项。

## 面向开发者，简洁实用

- **查用量**：调用 `GET /v1/usage/quota`（需 `read:quota` 权限），实时获取当前周期剩余 `total_quota` 和 `burst_quota`。
- **控风险**：客户端应解析响应头 `X-RateLimit-Remaining` 和 `X-RateLimit-Reset`，实现配额耗尽时的退避重试或降级策略。
- **避踩坑**：
  - 不要混用模型 ID 命名（如 `Qwen/Qwen3-235B`），必须使用控制台开通的精确 model ID（如 `qwen3-235b-a22b-instruct-2507`），否则 token 计量可能异常或失败；
  - 多模态请求中，务必添加 `X-DashScope-OssResourceResolve: enable` 请求头，否则 OSS 文件 URL 不被解析，导致 input tokens 计算为 0 或报错；
  - 临时 API Key 有效期最长 1800 秒，超时后 token 扣减仍发生但请求失败，生产环境请使用长期 API Key + Token Plan 精细管控。
- **调优建议**：对长上下文对话，可主动截断 history 或压缩 message 内容以降低 input tokens；对确定性低延迟场景，优先选用 Prime 模型（如 `glm-5.2-fast-preview`），其 token 计费不变但单位时间处理量翻倍。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


