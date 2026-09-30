# model high speed inference

百炼平台提供多种高吞吐、低延迟的模型推理加速方案，主要包含 Prime 模式（轻量级性能增强）和吞吐预留（专属容量保障）两类机制。二者均通过模型标识符（model ID）触发，无需修改 API 协议或 SDK，但适用场景、资源隔离级别与计费模型存在本质差异。开发者应根据业务对确定性、成本敏感度与流量可预测性的要求进行选型。

## 支持的模型/功能

- **Prime 模式**：面向输出速度敏感场景（如实时对话、Agent 多步推理），在标准 API 基础上提升 1.5~2 倍 TPS，不提供容量独占保障。支持模型包括 `glm-5.3-prime`、`glm-5.2-fast-preview`、`wan3.0-video-prime` 等，具体列表详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：为指定模型锁定专属 TPM（Tokens Per Minute）容量，实现刚性容量兑付，适用于流量可预估且不可接受限流的生产场景。支持模型覆盖 Qwen、GLM、DeepSeek、Kimi 等主流系列，华北2（北京）与新加坡地域均开放，完整列表见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：`glm-5.2-fast-preview` 在 Prime 模式文档中被明确列为 Prime 模型；但在吞吐预留文档的支持模型列表中仅列出 `GLM-5.2`（无 `-fast-preview` 后缀）。实际调用时，`glm-5.2-fast-preview` 仅适用于 Prime 模式，不可用于吞吐预留；吞吐预留需使用基础模型名（如 `GLM-5.2`）创建实例并获取专属 model code。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **性能提升** | 固定 1.5~2× TPS 提升（无需配置） | 可选「标准模式」或「高速模式」（即 PTU 部署），高速模式同样提供 1.5~2× TPS 提升 |
| **容量单位** | 无显式容量配置；依赖平台动态资源池 | 按 kTPM（千 tokens/分钟）预购输入/输出吞吐量，精确到 10 kTPM（输入）、1 kTPM（输出） |
| **溢出行为** | 不适用（无容量锁定） | 可选：「自动溢出至按量计费」（默认，服务不中断）或「仅使用预留容量」（超限返回 429） |
| **专属标识** | 使用预定义 model ID（如 `glm-5.2-fast-preview`） | 创建后生成唯一专属 model code，必须替换请求中的 `model` 字段 |

## 使用方式

- **Prime 模式**：直接使用文档中列出的 Prime 模型 ID 发起标准 OpenAI 兼容 API 调用，接入域名格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。示例见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 中的 curl 与 Python 示例。
- **吞吐预留**：在百炼控制台创建实例后，复制生成的专属 model code，并将其作为 `model` 参数值传入 API 请求（其他参数不变）。调用域名与标准 API 一致（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。注意：短时间内请求量快速拉升时系统需短暂预热，建议客户端实现排队或重试机制 —— 此说明出自 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 限制和注意事项

- **模型能力一致性**：Prime 模式下模型的功能、上下文长度、输出格式等与对应原版模型完全一致，仅推理链路优化；吞吐预留亦复用基础模型全部能力，无功能降级。
- **缓存行为**：两者均支持 token 缓存（如 `cached_tokens` 字段），但 Prime 模式文档明确指出其缓存单价独立计费（如 ¥4/百万 token），而吞吐预留未单独说明缓存计费逻辑，实际以预留容量内消耗为准。
- **地域与模型绑定**：Prime 模型 ID（如 `glm-5.3-prime`）与地域强绑定，不同地域价格不同；吞吐预留创建时需显式选择地域与模型，专属 model code 仅在该地域有效。
- **退订与失效**：吞吐预留实例到期后有 2 小时宽限期（可续费），14 小时后彻底释放且 model code 失效；Prime 模式无生命周期管理，只要模型可用即可持续调用。
- **流式响应差异**：Prime 模式在[流式输出](../concepts/streaming.md)时会分别推送 `delta.reasoning_content` 和 `delta.content` 字段（见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 返回示例），而吞吐预留未声明此行为，开发者应以实际返回结构为准。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


