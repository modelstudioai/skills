# Token

Token 是百炼平台中用于计量和控制大模型调用资源消耗的核心计费与限流单位。它代表模型处理文本（或图像、音频等多模态内容）时的最小语义单元，1 个 Token 通常对应一个子词（subword）、标点、空格或特殊控制符；在实际计费与配额管理中，Token 总量 = 输入 Token 数 + 输出 Token 数。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用计费与限流**：所有 API 调用（含 `/v1/services/*`、`/v1/chat/completions` 等）均按实际消耗的 input + output Token 总量计费和限流。Token Plan 机制即基于此总量进行配额分配与速率控制。
- **应用调用（Application Call）**：智能体（Agent）和工作流（Workflow）调用中，Token 统计覆盖完整执行链路——包括用户输入、系统提示词、RAG 检索结果注入、模型推理输出及插件返回内容。监控中显示的「Token 总量」即该端到端总和。
- **可观测性（Monitoring）**：
  - *应用监控*：在 Trace 的 `LLM`、`EMBEDDING`、`RETRIEVER` 等节点详情中，明确展示各环节的 Token 消耗量（如 Embedding 节点仅统计向量化输入的 Token 数）；
  - *模型监控*：用量统计页以「模型消耗 TotalToken 数」为核心指标，支持按模型、API Key、时间粒度聚合分析，是成本优化与容量规划的关键依据。
- **配额管理（Token Plan API）**：组织级 Token 预算（`token_limit`）以整数 Token 为单位设置，支持 `total`（永久总额）或 `monthly`（月度配额）类型，直接约束成员/席位可调用的总资源上限。

## 关键参数和配置

- `max_tokens_per_request`：单次请求最大输出 Token 数，默认 2048，不可超过模型原生上限（如 Qwen-Max 为 8192）；
- `tokens_per_minute`：每分钟允许消耗的 Token 总量（input + output），是 Token Plan 的核心速率配额；
- `burst_capacity`：突发令牌桶容量（单位：tokens），默认值为 `tokens_per_minute / 60 × 5`（即 5 秒平均速率），用于应对瞬时流量高峰；
- `model_whitelist`：显式指定 Token Plan 生效的模型列表（如 `"qwen-plus"`），空值表示对所有支持模型生效；
- `token_limit`（Token Plan API）：组织/席位级总 Token 配额，设为 `0` 表示无限制（需管理员权限）；
- `stream` + `incremental_output`：流式调用中，`incremental_output=True` 可确保每次响应只返回新增 Token（delta），避免客户端重复渲染，提升体验。

> ⚠️ 注意：  
> - 输出 Token 数以模型实际返回的 `usage.output_tokens` 字段为准；若接口未返回该字段（如部分旧版兼容路径），平台将按响应文本长度粗略估算；  
> - 免费额度优先抵扣，超出后才触发 Token Plan 限流；  
> - 修改 `tokens_per_minute` 后，新配额在下一个整分钟生效；而 Token Plan API 中的 `token_limit` 变更则立即生效。

## 面向开发者，简洁实用

- **估算 Token 数**：使用百炼提供的 [Token 计算器工具](https://bailian.console.aliyun.com/#/tools/token-calculator) 或 SDK 中 `count_tokens()` 方法（支持 text/image/audio 多模态输入）；
- **调试建议**：在应用监控中按 `Token 总量` 过滤高消耗 Span，结合 `messages` 和 `rag_options` 分析是否因 Prompt 过长、知识库召回过多或重排策略不当导致浪费；
- **成本优化**：  
  - 控制输入长度（精简 system [prompt](../guides/prompt.md)、压缩检索结果）；  
  - 设置合理的 `max_tokens_per_request` 避免冗余生成；  
  - 对低敏感业务启用 `burst_capacity` 缓冲，减少 429 错误；  
- **告警配置**：务必为 `模型消耗 TotalToken 数` 配置环比突增告警（如 1 小时内增长 >300%），及时发现异常调用或 Prompt 注入攻击。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [application call](../api/application-call.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [application support](../guides/application-support.md)


