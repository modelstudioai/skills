# Token

Token 是百炼平台中用于计量模型计算资源消耗的最小单位，代表模型在处理输入（如文本、图像）和生成输出时所消耗的计算量。它不是独立的数据对象，而是由平台 tokenizer 对原始内容进行标准化分词后得到的整数计数，是计费、配额控制、性能监控与用量分析的核心度量基准。

## 在百炼平台的不同场景中，这个概念如何使用

- **配额与限流（Token Plan）**：Token 是 Token Plan 的核心计量单位。所有绑定 Token Plan 的 API Key 发起的模型调用，其请求输入（[prompt](../guides/prompt.md)）与响应输出（completion）的总 token 数将被实时累加，并受 `quota`（总配额）和 `rate_limit`（TPS，token per second）双重约束。当配额耗尽或瞬时速率超限，请求将返回 `429 Too Many Requests`。

- **模型调用与计费**：所有支持按 token 计费的模型（如 `qwen-*`、`lingji-*` 系列）均以实际消耗的 token 总数为计费依据。流式（`stream=true`）与非流式响应统一按最终完整输出 token 数结算；[函数调用](function-calling.md)（Function Calling）的 token 消耗也计入主 Token Plan，不单独计费。

- **监控与告警**：在模型监控系统中，“TotalToken 数”是关键用量指标，支持按模型、API Key、时间粒度（分钟/小时/天）统计，并可配置环比突增类告警，用于主动识别异常调用或成本风险。

- **[多模态](multimodal.md)场景**：图像、视频等非文本输入的 token 计算方式与纯文本不同。例如，一张 1024×1024 图像经视觉 tokenizer 编码后可能对应数百至数千 token，具体换算规则由模型类型决定，详见[多模态](multimodal.md) tokenization 表格。

- **数据管理（间接关联）**：虽然训练/评测数据集本身不直接以 token 为单位存储，但在 SFT/DPO 等训练任务中，数据集的 token 分布（如平均 [prompt](../guides/prompt.md) 长度、max_tokens 设置）直接影响训练成本与显存占用，是调优前需评估的关键参数。

## 关键参数和配置

- **Token 计算逻辑**：由模型内置 tokenizer 执行，开发者无需手动分词。输入文本、Base64 图像、URL 图像均自动转换为 token 序列；输出 token 数 = 生成的全部 tokens（含 stop token）。

- **Token Plan 配置参数**（影响 token 使用边界）：
  - `quota`：整型，总 token 配额，范围 1000–100,000,000；
  - `rate_limit`：整型，最大允许 token 每秒消耗速率（TPS），范围 1–10000；
  - `valid_until`：ISO 8601 时间字符串，Token Plan 生效截止时间（UTC+0），最长 365 天。

- **监控指标字段**：
  - `total_tokens`：单次请求的 [prompt](../guides/prompt.md)_tokens + completion_tokens；
  - `prompt_tokens` / `completion_tokens`：分别统计输入与输出 token 数（部分接口响应头或审计日志中返回）；
  - `X-RateLimit-Remaining`：HTTP 响应头，指示当前周期剩余可用 token 数。

- **SDK 与 API 行为**：
  - 所有模型 API 调用默认返回 `usage` 字段（含 `prompt_tokens`, `completion_tokens`, `total_tokens`），无需额外开关；
  - Token Plan 校验全自动触发：只要 API Key 已绑定有效 Plan，且请求通过该 key 鉴权，即生效；
  - 不支持手动指定 token 限制（如 `max_tokens` 仅控制生成长度，不影响配额校验逻辑）。

## 面向开发者，简洁实用

- ✅ **务必检查响应中的 `usage` 字段**：这是验证 token 计算是否符合预期的最直接方式，尤其在调试[多模态](multimodal.md)输入或长文本场景时。
- ✅ **用 `GET /v1/token-plans/{id}/usage` 主动查用量**：延迟 ≤3s，比监控图表（1 小时延迟）更及时，适合构建自定义配额看板或熔断逻辑。
- ✅ **流式响应也要关注 total_tokens**：`stream=true` 时，`usage` 仅在最后一个 chunk 中返回，勿在中间 chunk 解析。
- ⚠️ **图像 token 不等于像素数**：避免按分辨率粗略估算；实际消耗取决于模型架构与编码器，建议用少量样本实测。
- ⚠️ **Token Plan 按自然日重置（UTC+0）**：非滚动周期，注意跨时区业务的配额规划。
- ⚠️ **API Key 绑定 Plan 后立即生效**：无需重启服务或刷新缓存，但解绑后新请求将不再受该 Plan 约束。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [model data overview](../guides/model-data-overview.md)
- [model monitoring](../guides/model-monitoring.md)
- [preparations](../api/preparations.md)


