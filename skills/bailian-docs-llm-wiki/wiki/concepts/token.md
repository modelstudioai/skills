# Token

Token 是百炼平台中用于计量模型输入与输出文本单元的最小计费与资源调度单位，1 个 Token 通常对应一个子词（subword）或标点符号。在百炼的计费、限流、配额和吞吐管理中，Token 是统一的度量基准——所有模型调用产生的输入（prompt）、输出（completion）及系统指令（如 system prompt、function call schema）均按实际消耗的 Token 数精确统计。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与额度**：免费额度（如 100 万 Token）、按量计费（¥2/百万 Token）、节省计划抵扣、TPM（Tokens Per Minute）预留等，均以 Token 为核算基础；注意：免费额度仅适用于华北2（北京）地域的实时推理调用，不覆盖 Batch、训练、部署等场景。
- **吞吐预留（TPM）**：TPM 表示每分钟可处理的 Token 总量，分“输入 TPM”和“输出 TPM”，购买时单位分别为“万 TPM/天”和“千 TPM/天”；长输入会按模型定义的折算系数（如 3×）计入 TPM 消耗。
- **Token Plan 配额管控**：通过 `token_limit`（总 Token 上限）和 `rate_limit`（Token/s 速率）实现细粒度用量隔离；`burst_capacity` 允许短时超额，但所有消耗 Token 均计入总量配额，且以模型返回的 `usage.total_tokens` 为准（含 system、tool calls 等结构化内容）。
- **模型能力边界**：各模型有明确的最长输入 Token 限制（如 `qwen3.7-plus-2026-05-26` 为 256K），超限将直接报错；阶梯计费也以 Token 数为触发条件（如 >256K 输入，整次请求按高价结算）。

## 关键参数和配置

| 参数 | 说明 | 典型取值/约束 |
|------|------|----------------|
| `usage.total_tokens` | API 响应中返回的实际消耗 Token 总数（输入 + 输出） | 开发者应以此值做用量审计，而非自行估算 |
| `token_limit`（Token Plan） | Token Plan 总量硬上限 | 必须 ≥ `burst_capacity`；超限返回 HTTP 429 |
| `rate_limit`（Token Plan） | Token 每秒允许消耗速率 | 单位：token/s；滑动窗口限流，精度毫秒级 |
| `burst_capacity`（Token Plan） | 突发容量，允许瞬时超额 | 建议设为 `rate_limit × 2`，不可超过 `token_limit` |
| TPM 购买单位 | 吞吐预留容量报价单位 | 输入：万 TPM/天；输出：千 TPM/天；起步量分别为 200k / 20k |
| 长输入折算系数 | 模型对超长输入段的 Token 加权系数 | 因模型而异（如 `qwen3.7-flash` 对 32K–256K 段用 3×，`glm-5.1` 用 1.33×） |

> ⚠️ 注意：  
> - 免费额度与 Token Plan **互不叠加**：免费额度用尽后自动切换至绑定的 Token Plan，不参与其配额抵扣；  
> - Token 统计由服务端最终确定，客户端不可绕过；所有 header（如 `X-Plugin-Id`）、参数（如 `model`）必须准确匹配，否则 Token 不计入对应 Plan 或额度；  
> - 子业务空间、[异步任务](asynchronous-task.md)、多模态文件上传等场景中，Token 消耗逻辑一致，无额外豁免。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [more about models](../api/more-about-models.md)


