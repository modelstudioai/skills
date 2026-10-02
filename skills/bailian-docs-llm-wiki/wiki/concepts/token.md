# Token

Token 是百炼平台中用于计量模型输入与输出内容长度的基本单位，也是资源配额、计费、限流与用量监控的核心度量基准。一个 Token 通常对应一个子词（subword）或字符片段（如中文单字、英文单词/标点/空格），具体切分逻辑由各模型的 tokenizer 决定；开发者无需手动分词，但需理解其在调用、成本与性能中的实际影响。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：所有模型服务（文本、多模态、语音）均按实际消耗的输入 Token 和输出 Token 分别计费。例如调用 `qwen-plus` 时，[prompt](../guides/prompt.md) 中的 512 个 Token + response 中的 128 个 Token = 共计 640 个计费 Token。免费额度、资源包、节省计划均以 Token 为最小抵扣单位。
  
- **Token Plan 配额控制**：Token Plan 通过 `rate_limit`（每秒 token 消耗上限）和 `burst_capacity`（突发可透支 token 数）实现稳定性保障。该配额严格绑定模型 Code（如 `qwen-vl-plus`），不跨模型共享；Coding Plan 则为代码类模型（如 `qwen2.5-coder`）提供独立的 token 计量与配额体系。

- **API 请求约束**：`max_tokens` 参数（非 `max_completion_tokens`）表示单次请求允许消耗的 **总 token 上限（[prompt](../guides/prompt.md) + completion）**，超限将被截断并返回 `400 Bad Request`；该值受当前 Token Plan 的 `burst_capacity` 限制，且不可通过 header 超越（如 `X-Request-Token-Limit` 仅能 ≤ burst_capacity）。

- **监控与告警**：模型监控中的「模型消耗 TotalToken 数」指标即该模型在指定时间窗口内所有成功/失败请求的实际 token 总消耗（含异步任务执行结果），可用于配置突增告警，辅助识别异常调用或额度耗尽风险。

- **批量与异步任务**：Batch 接口（`/v1/batch`）按实际执行结果计量 token，单价为实时推理的 50%，但**不支持免费额度抵扣**；异步任务（`/v1/async-tasks`）的 token 消耗在任务完成时才计入用量，失败任务仍计费。

## 关键参数和配置

| 参数名 | 说明 | 注意事项 |
|--------|------|----------|
| `max_tokens` | 单次请求允许消耗的最大 token 总数（[prompt](../guides/prompt.md) + completion） | 是硬性上限，非建议值；旧版 SDK 中误用为“响应长度限制”，请以最新文档为准；推荐显式设置以避免意外超限 |
| `rate_limit` | 每秒最大 token 消耗速率（如 `"10000/tokens-per-second"`） | 由账号类型（个人/团队）和模型能力决定，不可自定义数值，仅可在控制台选择档位 |
| `burst_capacity` | 突发流量可透支的 token 上限（单位：token） | 通常为 `rate_limit` 值的 2–5 倍；`X-Request-Token-Limit` header 的取值上限 |
| `X-Request-Token-Limit` | 请求级 token 消耗上限（header） | 可选，用于单次请求精细化控制；必须 ≤ 当前 plan 的 `burst_capacity`，否则拒绝 |

> ⚠️ 重要提示：  
> - Token Plan 不等同于 API Key 认证机制——前者管资源，后者管身份；Token Plan 配置对所有使用该 API Key 的调用生效。  
> - 免费额度仅适用于通用 API Key 发起的**实时推理**调用；Token Plan / Coding Plan 专属 API Key、Batch 调用、训练与部署均不享受免费额度。  
> - 所有 token 统计以模型实际 tokenizer 输出为准（如 `qwen3` 使用 QwenTokenizer v3），缓存命中部分按独立折算系数计费（如 10%），不计入标准输入单价。

## 面向开发者，简洁实用

- ✅ **查用量**：调用 `/v1/usage/token-usage` 实时获取已用 token；或在控制台「模型用量」页按分钟/小时查看（延迟约 1 小时，用于对账）。  
- ✅ **控成本**：开启「免费额度用完即停」开关（HTTP 403 响应），避免意外扣费；为 `TotalToken 数` 配置环比突增告警（如 5 分钟内增长 >300%）。  
- ✅ **避踩坑**：  
  - 不要假设 `max_tokens=1024` 表示“最多返回 1024 字符”——中文实际输出长度约为 300–600 字；  
  - 异步任务不要轮询过频（图像生成建议 ≥5s 间隔），否则触发 QPS 限流；  
  - Batch 调用务必确认业务逻辑是否允许无免费额度抵扣。  
- ✅ **调试建议**：启用推理日志（需投递至 SLS），查看原始 prompt/response 及对应 token count，精准定位长输入或幻觉导致的 token 溢出。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


