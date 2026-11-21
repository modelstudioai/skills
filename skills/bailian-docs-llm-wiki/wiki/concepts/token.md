# Token 计量与管理

Token 计量与管理是百炼平台对模型调用中输入/输出文本单元（token）进行精准识别、统计、计费与资源约束的核心机制。它贯穿模型推理、训练、部署及监控全链路，既是成本核算的基础单位，也是性能保障（如吞吐预留）和限流控制的关键依据。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用**：每次 API 请求均自动解析 prompt 和 response，分别统计 `input_tokens` 与 `output_tokens`；流式响应（`stream=true`）下按实际返回 token 累计，中断或超时可能导致 `output_tokens` 统计值略低于理论生成量。  
- **计费结算**：Token 是按量计费的最小计量单位，费用 = `input_tokens × 单价 + output_tokens × 单价`；单价由 `model_id` 决定，并受阶梯计价（如单次 output > 8192 tokens）、地域、计费模式（按量/预留/节省计划）影响。  
- **吞吐保障（TPM 预留）**：通过 `tpm_reservation` 参数预购每分钟可处理的 token 总量（如 `10000`），平台据此分配独占计算资源，确保高并发场景下的首 Token 延迟与稳定性。  
- **监控与告警**：`模型消耗 TotalToken 数` 是核心可观测指标，支持配置实时告警（如“单日 Token 消耗突增 300%”），用于成本异常检测，但该数据仅作运维参考，不替代账单系统。  
- **用量分析与对账**：通过「费用中心 → 模型用量」或 Billing API（如 `GetBillingTrend` 按 `BASE_MODEL` 分组）查询 token 级明细，结合 `project_id` 实现多项目成本分摊与预算控制。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `input_tokens` / `output_tokens` | 平台自动返回的整数字段，表示本次调用实际消耗的输入/输出 token 数量 | ✅ 始终存在；非字符数，基于模型 tokenizer 精确分词（如 `qwen-max` 使用 QwenTokenizer）；不可手动设置 |
| `tpm_reservation` | 吞吐预留等级，单位为 tokens/minute | ✅ 仅在开通 TPM 预留后生效；需与 `project_id` 绑定；不可跨地域复用 |
| `X-Bailian-Project-ID` | HTTP 请求头，指定成本归属项目 | ✅ 必须透传，否则 token 消耗计入默认项目，影响分账准确性 |
| `model_id` | 模型唯一标识（如 `qwen-max`, `text-embedding-v1`） | ✅ 直接决定 token 单价与计费策略；嵌入、VL、ASR 等模型均独立计价 |
| `stream`（布尔值） | 是否启用流式响应 | ⚠️ 流式下 `output_tokens` 统计以实际 flush 的 token 为准，非最大可能生成量 |

> **注意**：Token 统计由服务端完成，开发者无需自行 tokenizer；所有 token 数均四舍五入取整，无小数精度；免费额度仅覆盖 `input_tokens + output_tokens` 的基础推理，不包含训练、TPM 预留、文件上传等衍生费用。

## 面向开发者，简洁实用

- ✅ **查用量**：控制台 → 「费用中心 → 模型用量」或调用 `GetBillingTrend` API，按 `BASE_MODEL` + `project_id` 过滤。  
- ✅ **控成本**：对稳定负载，优先购买「节省计划」或「TPM 预留」；对突发流量，用 `project_id` 配合预算告警（最低阈值 10 元）。  
- ✅ **避坑**：  
  - 不要依赖 `response.usage` 中的 `prompt_tokens`/`completion_tokens` 字段做计费对账——以账单系统为准；  
  - 流式请求若提前关闭连接，`output_tokens` 可能偏少，属预期行为；  
  - 多模态模型（如 `qwen-vl-plus`）的图像 token 也计入 `input_tokens`，按统一规则计费。  
- ✅ **调试建议**：开启「审计日志」可查看每次调用的 `input_tokens`/`output_tokens` 原始值，用于快速验证 tokenizer 行为。

## 关联主题页

- [test 1](../guides/test-1.md)
- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [model monitoring](../guides/model-monitoring.md)
- [billing api](../api/billing-api.md)


