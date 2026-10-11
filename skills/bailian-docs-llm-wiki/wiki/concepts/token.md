# Token 计量与管理

Token 计量与管理是百炼平台对模型调用资源消耗进行精确统计、配额控制与成本核算的核心机制，以输入 token 数与输出 token 数为唯一计量单位，贯穿 API 调用、配额分配、计费结算、监控告警及用量分析全链路。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 调用与配额控制（Token Plan）**：所有实时推理请求均按实际 `input_tokens` + `output_tokens` 四舍五入到整数进行计量；配额扣减实时发生，流式响应按每个 chunk 的实际 tokens 分次扣减；超限直接返回 HTTP 429，不降级。
- **计费与成本管理（[test 1](../guides/test-1.md)）**：Token 是最小计费粒度（1 Token 起计），输入/输出分开计价；免费额度（如 100 万 Token/模型）、资源包、节省计划均基于此计量结果按序抵扣；吞吐预留（TPM）也以 kTPM（千 Tokens/分钟）为单位购买和折算。
- **模型监控（[model monitoring](../guides/model-monitoring.md)）**：监控系统按 `model_id` 和 `api_key_hash` 维度聚合 Token 消耗量，用于用量趋势分析与异常检测；注意：监控值为内容长度粗略估算，与账单系统存在 ≤3% 偏差，不可用于精确对账。
- **账单与用量溯源（[test 1](../guides/test-1.md) / [model monitoring](../guides/model-monitoring.md)）**：账单明细中 `实例 ID` 字段（格式：`ApiKeyID;业务空间ID;模型名称;...`）关联 Token 消耗记录；开发者可通过 `/v1/token-plans/usage` 接口或控制台「API 密钥与配额」页实时查询绑定 Plan 的剩余配额。
- **开发调试与可观测性**：每次成功响应的 Header 中固定返回 `x-bailian-input-tokens` 和 `x-bailian-output-tokens`，是开发者验证 [prompt](../guides/prompt.md) 长度、评估输出效率、优化上下文截断策略的权威依据。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `input_tokens` / `output_tokens` | 响应头中返回的实际消耗 token 数（整数） | 唯一可信来源，用于调试、审计与自建配额校验；不依赖客户端 tokenizer 估算 |
| `max_tokens` | 单次请求允许生成的最大 token 数（如 Qwen3-8B 默认 8192） | 影响输出上限与配额占用，设过小可能导致截断，设过大则浪费配额 |
| `stream: true` | 启用流式响应 | 不改变总消耗，但触发多次细粒度配额扣减（每 chunk 独立扣减），需确保服务端能处理分块配额不足场景 |
| `temperature` / `top_p` | 采样参数 | **不影响 token 消耗量**，但显著影响实际输出长度分布，间接决定配额使用效率，建议在稳定性要求高的生产环境保持较低 temperature（如 0.1–0.3） |

> ⚠️ 注意事项：
> - 所有计量均四舍五入到整数（1.6 tokens → 2 tokens），无小数累计；
> - 多模态（语音/图像/VL）、离线批量推理、模型微调训练、私有化部署等任务**不纳入 Token Plan 统一计量体系**；
> - Coding Plan 等特殊 Plan 对代码上下文有专用截断逻辑，其 token 计量规则独立于通用 Plan；
> - 监控数据中的 Token 统计仅作参考，**不可替代账单与配额接口的精确值**。

## 面向开发者，简洁实用

- ✅ **必查响应头**：每次调用后检查 `x-bailian-input-tokens` 和 `x-bailian-output-tokens`，快速定位长 [prompt](../guides/prompt.md) 或失控输出；
- ✅ **配额自查**：调用 `GET /v1/token-plans/usage`（需对应 API Key 权限），避免静默失败；
- ✅ **流式容错**：若使用 `stream: true`，需在客户端处理 `429 Too Many Requests` 出现在任意 chunk 的可能性；
- ✅ **成本预估**：本地用 Hugging Face `transformers` 或 `tiktoken` 库对 [prompt](../guides/prompt.md) + stop sequence 进行 tokenizer 估算（注意：百炼使用自研 tokenizer，结果供参考，非最终计费依据）；
- ❌ **勿依赖监控值做配额判断**：监控延迟约 30 秒且存在估算偏差，配额控制必须依赖 Token Plan 接口或响应头；
- ❌ **勿复用同一 API Key 绑定多环境**：dev/staging/prod 应使用不同 API Key 并分别绑定 Plan，实现硬隔离。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [model data overview](../guides/model-data-overview.md)


