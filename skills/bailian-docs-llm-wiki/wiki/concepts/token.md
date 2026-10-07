# Token

Token 是百炼平台中用于计量模型输入与输出文本（及多模态内容）长度的基本单位，也是资源配额控制、计费结算和请求限流的核心度量标准。1 个 token 通常对应一个子词（subword）或字符级单元，具体切分方式由模型底层 tokenizer 决定；实际消耗以 API 响应中 `usage.total_tokens` 字段为准，包含 [prompt](../guides/prompt.md) 和 completion 全部内容。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用计费与配额控制**：所有支持按 token 计费的模型（Qwen 系列、Qwen-VL、Qwen-Audio、Qwen-Coder 等）均以实际消耗的 token 数为计费依据。Token Plan 机制通过 `quota`（月度总配额）、`grace_period`（超限缓冲）和 `enforce_mode`（硬/软限制）实现服务级或请求级的 token 消耗管控。
- **请求级输出截断**：参数 `max_tokens`（在 OpenAI 兼容 Messages 接口等场景为必填）用于限制模型生成内容的最大 token 数，其生效优先级高于 Token Plan 配额——任一条件先触发即截断输出。
- **异步任务预占与用量统计**：异步任务（如视频生成、语音转写）在提交时会预估并预占 token 额度；完成后的实际消耗以 `usage.total_tokens` 为准，并计入对应 Token Plan 的日/月用量统计（可通过 `GET /v1/token-plans/{plan_id}/usage` 查询）。
- **Coding Plan 特殊规则**：代码生成类模型（如 `qwen-coder-next`）采用独立的 token 计算逻辑（例如对注释、缩进、模板代码做差异化计权），不与通用 Token Plan 混用。
- **安全与调试辅助**：`usage.total_tokens` 同时用于识别异常长 [prompt](../guides/prompt.md) 或失控生成，是排查超时、截断、成本突增等问题的关键诊断字段。

## 关键参数和配置

| 参数名 | 所属上下文 | 类型 | 说明 |
|--------|------------|------|------|
| `max_tokens` | API 请求参数（OpenAI Messages / DashScope Responses 等） | integer | 模型生成内容的最大 token 数（不含 [prompt](../guides/prompt.md)）。注意：在 OpenAI Chat 接口中不支持，在 DashScope 原生接口中亦不支持。 |
| `quota` | Token Plan 创建参数 | integer | Token Plan 的月度总配额（单位：token），最小值为 1000。 |
| `grace_period` | Token Plan 创建/更新参数 | integer | 超配额后允许继续调用的缓冲时间（秒），默认值为 300（非 0）。 |
| `enforce_mode` | Token Plan 创建/更新参数 | string | `"hard"`（立即拒绝超限请求）或 `"soft"`（记录告警但放行），默认 `"soft"`。 |
| `X-Token-Plan-ID` | HTTP 请求 Header | string | 单次请求级覆盖 Token Plan 绑定，优先级高于模型实例级配置。 |
| `usage.total_tokens` | API 响应体（`choices[0].message` 同级） | integer | 实际消耗的总 token 数（prompt + completion），是计费、审计与用量统计的唯一事实来源。 |

> ⚠️ 注意：`max_tokens` 与 Token Plan 配额是**并行生效、互不替代**的双重控制机制；模型将在任一条件先满足时截断输出。

## 面向开发者，简洁实用

- ✅ **始终检查响应中的 `usage.total_tokens`**：这是你实际被计费和占用配额的唯一依据，不要依赖估算或前端输入长度。
- ✅ **生产环境务必设置 `max_tokens`（如适用）**：防止意外长输出导致 token 爆涨、响应延迟或配额耗尽。
- ✅ **Token Plan 应绑定到模型实例级，再通过 `X-Token-Plan-ID` 头做请求级覆盖**：避免全局配额误配，便于 A/B 测试或灰度发布。
- ✅ **异步任务需主动轮询或配置事件通知获取 `usage.total_tokens`**：其值在任务完成时才确定，不体现在提交响应中。
- ❌ **不要将 `max_tokens` 误解为“最大输出长度”**：它受模型上下文窗口、prompt 长度、系统消息等共同约束；实际生成长度可能小于该值。
- ❌ **不要复用不同模型的 token 配额逻辑**：Qwen-Coder 使用 Coding Plan，Qwen-Audio 使用专用音频 token 规则，不可混用通用 Plan。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)


