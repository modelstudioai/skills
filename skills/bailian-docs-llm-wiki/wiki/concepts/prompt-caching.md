# 上下文缓存

上下文缓存（又称前缀缓存）是百炼平台提供的一种推理加速与成本优化能力：当多次请求共享相同的输入前缀时，平台会缓存该前缀的中间计算结果，后续命中缓存的部分按折扣价折算额度或计费，从而降低延迟与费用。

## 在百炼平台的使用场景

### 预置吞吐（PTU）部署中的前缀缓存

PTU 部署原生支持长输入与前缀缓存，是上下文缓存的主要应用场景。通过阶梯容量系数和缓存折扣管理额度消耗：

- **缓存命中折扣**：命中缓存的输入 token 按模型对应折扣折算容量。例如 glm-5.1 折扣为 0.2，deepseek-v4-pro 为 0.08，显著降低 TPM 消耗。
- **自动转按量计费**：当请求超出 PTU 额度或输入超过模型上下文上限（千问 128K / DeepSeek 64K）时，请求自动转为按量计费，响应头包含 `x-dashscope-ptu-overflow:true`，业务不中断。

### 显式缓存调用

百炼支持通过 OpenAI 兼容接口或 DashScope SDK 显式触发缓存。开发者可在请求中标识需要缓存的前缀（如系统提示词、[长上下文](long-context.md)文档），平台据此管理缓存命中与失效，适用于 RAG 应用、多轮对话等固定前缀反复出现的场景。

## 关键参数与响应字段

### 请求侧

- 在 PTU 部署下，缓存由平台自动管理，无需额外参数；显式缓存则按接口协议提供缓存控制字段。
- 建议将稳定不变的内容（系统提示、知识库文档、few-shot 示例）置于请求前缀部分，动态内容置于后段，以提高缓存命中率。

### 响应侧（PTU 部署）

PTU 部署的响应中包含额度相关字段，用于观测缓存命中情况：

- `service_tier`：`ptu-standard` 表示使用 PTU 额度；`default` 或不返回表示按量计费。
- `provisioned_tokens`：折算后实际消耗的 PTU 额度（含阶梯系数和缓存折扣）。
- `cached_tokens`：前缀缓存命中的 token 数。

`cached_tokens` 在不同 API 格式下的 JSON 路径有差异：

| API 格式 | 字段路径 |
| --- | --- |
| OpenAI Chat 兼容 | `usage.prompt_tokens_details.cached_tokens` |
| OpenAI Responses | `usage.input_tokens_details.cached_tokens` |
| Anthropic 兼容 | 暂不返回 `cached_tokens` |

## 容量评估建议

在创建或扩容 PTU 部署时，控制台提供容量计算器，可根据每分钟请求数（RPM）、平均输入/输出长度、预估缓存命中率推荐输入 TPM 和输出 TPM。长输入场景下建议先用计算器评估额度，结合预期缓存命中率规划容量，避免意外转为按量计费。

## 注意事项

- 缓存命中要求前缀完全一致，任何字符变化（包括空格、换行、字段顺序）都可能导致缓存失效。
- 缓存有有效期，长时间无请求后缓存会被淘汰，需重新预热。
- 兼容接口（OpenAI / Anthropic）为保持协议一致，可能不暴露百炼原生的全部缓存控制参数；如需最完整的缓存能力，建议使用 DashScope 原生接口。

## 关联主题页

- [use cases](../guides/use-cases.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [qwen api reference](../api/qwen-api-reference.md)




