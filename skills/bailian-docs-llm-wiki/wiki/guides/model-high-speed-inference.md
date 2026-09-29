# model high speed inference

百炼平台提供多种面向高吞吐、低延迟推理场景的加速能力，主要包括 Prime 模式（轻量级性能增强）和吞吐预留（专属容量保障）。二者均通过模型标识符（model ID）切换，无需修改 SDK 或协议，适用于对响应速度、稳定性或可预测性有明确要求的生产环境。开发者可根据业务负载特征（如峰值可预估性、容忍限流程度、成本敏感度）选择合适方案。

## 支持的模型/功能

- **Prime 模式**：面向输出速度敏感场景（如 AI 编程助手、Agent 多步推理、实时对话），在标准 API 基础上提升 1.5~2 倍 TPS，不改变模型能力与限制。支持模型包括 `glm-5.3-prime`、`glm-5.2-fast-preview`、`wan3.0-video-prime` 等，按地域分列计费，详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：为指定模型锁定专属 TPM（Tokens Per Minute）容量，实现刚性容量兑付，避免公共池限流影响。支持模型覆盖主流大模型，如 `Qwen3.8-Max`、`GLM-5.3`、`DeepSeek-v4-Pro` 等，华北2（北京）与新加坡地域均开放，具体列表以控制台为准，详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：文档 1 中称 `glm-5.2-fast-preview` 是 Prime 模式专用模型名，而文档 2 的吞吐预留支持列表中仅列出 `GLM-5.2`（无 `-fast-preview` 后缀）。实际调用时，若需同时启用 Prime 性能 *和* 吞吐预留保障，应先创建吞吐预留并获取专属 model code，该 code 内部已集成 Prime 加速逻辑；不可直接将 `glm-5.2-fast-preview` 作为吞吐预留的“基础模型”选择——后者仅接受标准模型 ID（如 `glm-5.2`）。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **性能提升** | TPS 提升 1.5~2 倍（相比同模型标准 API） | 标准模式：TPS 与标准 API 一致；高速模式：TPS 提升 1.5~2 倍（等效于 PTU 部署） |
| **容量保障** | 无专属容量，依赖平台剩余资源（特殊限流策略） | 专属 kTPM 容量，刚性兑付，不共享 |
| **计费单位** | 按 token 计费（输入/输出/cached） | 预付费按 kTPM × 时长；溢出部分按 token 计费（若选「自动溢出」） |
| **核心标识** | 使用预置 model ID（如 `glm-5.2-fast-preview`） | 使用系统生成的专属 model code（非原始模型名） |
| **溢出行为** | 不触发限流（平台有余力时持续服务） | 可选：自动降级为按量计费（默认）或返回 429 |

## 使用方式

- **Prime 模式**：直接使用文档中列出的 Prime 模型 ID（如 `glm-5.2-fast-preview`）发起请求，接入域名固定为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，无需额外 header 或参数。流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段。详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：在百炼控制台创建实例后，复制生成的**专属模型 code**，并在 API 请求中将其赋值给 `model` 参数（替换原模型名）。调用域名与标准 API 一致（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。注意：短时间内请求量快速拉升时存在短暂预热期，可能出现延迟波动，建议客户端实现排队或重试机制。详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 限制和注意事项

- **模型能力一致性**：Prime 模式下模型的功能、上下文长度、输出格式等与对应原版模型完全一致，仅推理性能优化；吞吐预留亦不改变模型本身能力。
- **缓存行为**：两者均支持缓存命中计费优惠（如 `cached_tokens` 单价更低），但缓存策略由平台统一管理，用户不可配置。
- **地域与模型绑定**：Prime 模型 ID 和吞吐预留支持列表均按地域（如华北2、新加坡）独立维护，跨地域不可复用 model ID 或 code。
- **调试与监控**：吞吐预留提供完整的监控页签（利用率、配额内外调用次数、超额降级统计），而 Prime 模式无独立监控视图，其用量计入标准 API 统计。
- **退订与失效**：吞吐预留实例退订后专属 model code 立即失效，后续请求回退至公共资源；Prime 模式无生命周期管理，只要模型可用即可调用。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


