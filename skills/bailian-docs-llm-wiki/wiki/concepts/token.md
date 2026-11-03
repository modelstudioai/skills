# Token

Token 是百炼平台中用于计量模型计算资源消耗与计费的核心单位，代表模型处理输入文本、生成输出内容或执行推理任务所消耗的最小语义单元。一个 Token 通常对应一个子词（subword）或标点符号，在中文场景下平均约等于 1.5~2 个汉字，英文场景下约等于 1 个单词或常见词缀。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与用量统计**：所有模型调用（含文本生成、[多模态](multi-modal.md)、嵌入、重排序等）均按 *输入 Token 数 + 输出 Token 数* 精确计费。监控中心中的「Token 消耗」指标即为此总和，是费用估算和配额管理的直接依据。
- **限流控制**：业务空间级权限支持 `token_limit`（每分钟 Token 总量上限），与 `qpm_limit`（每分钟请求数）共同构成双维度限流策略，防止突发高负载冲击服务稳定性。
- **高性能推理选型**：`Token 按量部署` 方案专为 LoRA 微调模型设计，按实际调用消耗的 Token 数实时计费，不调用不计费；`Prime 模式` 和 `吞吐预留（TPM）` 等加速方案也以 Token 处理能力（如 TPM = Tokens Per Minute）作为核心性能指标。
- **异步与批量任务**：Batch 推理按 JSONL 文件中每个请求的实际输入/输出 Token 总量结算；异步任务（如图像/视频生成）虽不显式暴露 Token，但其底层资源调度与计费仍映射为等效 Token 消耗。
- **安全与临时凭证**：临时 API Key 的有效期（`expire_in_seconds`）虽不直接关联 Token，但其典型使用场景（如前端直传）必须严格限制单次调用 Token 上限，避免凭证泄露导致不可控的 Token 消耗。

## 关键参数和配置

- `input_tokens` / `output_tokens`：API 响应体中标准字段（如 `/v1/chat/completions` 返回的 `usage` 对象），开发者应主动解析并用于本地用量审计。
- `thinking_tokens`：当启用 `enable_thinking=true` 时，思考过程产生的中间 Token 单独统计（如 `reasoning_content` 部分），计入总 Token 消耗，但不返回在最终 `content` 中。
- `thinking_budget`：可选参数，用于硬性限制思考阶段的最大 Token 数（如 `{"thinking_budget": 512}`），超出则提前终止思考并进入生成阶段，防止长思考导致超时或超额。
- `token_limit`：业务空间权限配置项，单位为「Tokens/Minute」，需在控制台「权限管理 → 模型调用」中设置，对绑定该空间的所有 API Key 生效。

## 面向开发者，简洁实用

- ✅ **必查响应字段**：每次调用后务必检查 `response.usage.input_tokens` 和 `response.usage.output_tokens`，不要依赖估算或字符数换算。
- ✅ **流式调用注意**：启用 `stream=true` 时，`output_tokens` 在最终 `done` 事件中才完整返回；中间 `delta` 仅含增量内容，不可累加估算。
- ✅ **批量任务核对**：Batch JSONL 输入中每个请求的 `model` 必须与提交 URL 匹配，否则该条请求将失败且不产生 Token 计费——但已成功解析的请求仍会计费。
- ⚠️ **避免隐式超限**：`thinking_budget` 未设置时，部分模型（如 `qwen3.7-plus`）可能因复杂问题生成大量中间 Token，导致首字延迟升高或触发 `429 Throttling.TokenQuota` 错误。
- ⚠️ **监控与告警联动**：在监控中心配置 `token_consumption_rate > 90% of quota` 类告警，结合 `p95_latency` 异常波动，可快速定位低效 Prompt 或异常循环调用。

## 关联主题页

- [preparations](../api/preparations.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model monitoring](../guides/model-monitoring.md)
- [application permission management](../guides/application-permission-management.md)
- [more about models](../api/more-about-models.md)


