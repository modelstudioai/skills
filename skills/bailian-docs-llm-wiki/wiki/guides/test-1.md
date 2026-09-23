# test 1

test 1 是百炼平台面向开发者提供的基础模型调用服务，支持按量计费与资源预留两种使用模式。其核心能力聚焦于低延迟推理、高并发吞吐保障及细粒度成本控制。所有计费规则与资源配额均以实际调用行为为依据，开发者需结合自身业务场景选择合适计费方式。

## 支持的模型/功能

- 支持 Qwen 系列大模型（Qwen1.5、Qwen2、Qwen2.5）的在线推理调用  
- 提供同步 API 调用与异步批量处理两种接口模式  
- 支持自定义 `temperature`、`top_p`、`max_tokens` 等生成参数（详见 [原文标题](../../raw/model-user-guide/test-1.md)）  
- 可选吞吐预留（TPM Reservation）以保障稳定 QPS，适用于有确定性 SLA 要求的生产环境  

## 关键参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `model` | string | 模型标识符，如 `qwen-max`、`qwen-plus` | 必填 |
| `tpm_reservation_id` | string | 吞吐预留资源 ID，启用后优先使用预留额度 | 无 |
| `stream` | boolean | 是否启用流式响应 | `false` |
| `max_tokens` | integer | 最大生成 token 数 | `2048` |

> **注意**：`max_tokens` 的实际生效上限受模型本身 context 长度限制，例如 `qwen-max` 最高支持 32768 tokens，但 `test 1` 服务层对单次请求默认硬限为 8192 —— 此限制在 [原文标题](../../raw/model-user-guide/test-1.md) 中未明确说明，需参考 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md) 中“高上下文请求附加费用”条款确认。

## 使用方式

1. 在控制台开通 `test 1` 服务并完成实名认证  
2. 获取 API Key 并设置 `Authorization: Bearer <api_key>` 请求头  
3. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`  
4. 请求体为标准 OpenAI 兼容格式（含 `model`, `messages`, `parameters` 字段）  

示例调用中 `parameters` 字段结构与计费粒度强相关，详细字段定义请参阅 [原文标题](../../raw/model-user-guide/test-1.md)。

## 限制和注意事项

- 单账户默认最大并发请求数为 100，可通过工单申请提升  
- 流式响应不支持 `tpm_reservation_id` 参数，启用预留吞吐时须关闭 `stream`  
- 免费额度仅适用于首次开通用户，且不可跨区域叠加（具体规则见 [原文标题](../../raw/model-user-guide/test-1.md)）  
- 模型训练与微调功能**不包含**在 `test 1` 服务范围内，需单独开通 `model-training` 服务

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)


