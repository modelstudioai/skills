# test 1

test 1 是百炼平台面向开发者提供的基础模型调用服务，支持按需调用与资源预留两种使用模式。其计费体系覆盖模型推理、训练部署、吞吐保障及成本优化等多个维度，适用于不同规模和稳定性的业务场景。详细计费规则与成本管理能力请参考 [产品计费](../../raw/model-user-guide/test-1.md)。

## 支持的模型/功能

- 支持主流开源与自研大语言模型的 API 调用（如 Qwen 系列、Baichuan 等），具体可用模型列表以控制台实时展示为准  
- 提供同步推理、流式响应、批量异步处理三种调用方式  
- 支持通过吞吐预留（TPM）保障高并发稳定性，详见 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)  
- 同时支持模型微调与私有化部署，相关费用独立核算，参见 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)

## 关键参数

| 参数 | 说明 | 取值范围 | 默认值 |
|------|------|----------|--------|
| `model` | 模型标识符 | 如 `qwen-max`, `qwen-plus` 等 | 必填 |
| `max_tokens` | 最大生成 token 数 | 1–8192 | 2048 |
| `temperature` | 采样温度 | 0.0–2.0 | 1.0 |
| `top_p` | 核采样阈值 | 0.01–1.0 | 0.8 |
| `tpm` | 请求级吞吐预留量（仅限已购买 TPM 预留包的用户） | ≥100 | 不启用 |

> **注意**：`tpm` 参数仅在已开通吞吐预留服务且配额可用时生效；未配置时系统按共享池调度，延迟与并发能力受整体负载影响——该行为与 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md) 中描述的“免费调用默认走共享通道”一致，但与旧版文档中“免费调用自动绑定 50 TPM”的说法存在冲突，以当前 [产品计费](../../raw/model-user-guide/test-1.md) 为准。

## 使用方式

1. 在百炼控制台开通 test 1 服务并完成实名认证  
2. 获取 API Key（位于「API 密钥管理」页面）  
3. 构造 HTTP POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`，Header 中携带 `Authorization: Bearer <api_key>`  
4. 请求体为标准 JSON，示例：
   ```json
   {
     "model": "qwen-max",
     "input": {"messages": [{"role": "user", "content": "你好"}]},
     "parameters": {"max_tokens": 512}
   }
   ```
5. 成本监控与账单分析可通过 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md) 页面完成

## 限制和注意事项

- 免费额度仅限新注册用户首次开通后 30 天内使用，总额度不可叠加，详见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)  
- 单次请求最大上下文长度为 32768 tokens（含 input + output），超长输入将被截断并返回 `400` 错误  
- 吞吐预留（TPM）与节省计划（Savings Plan）不可同时应用于同一模型调用链路，二者互斥，具体约束见 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)  
- 所有计费项均以 UTC+8 时间为准，账期按自然月结算，跨月未使用的预留资源不结转

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)


