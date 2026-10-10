# model high speed inference

百炼平台提供多种高吞吐、低延迟的模型推理加速方案，主要包含 Prime 模式（轻量级性能增强）和吞吐预留（专属容量保障）两类机制。二者均通过模型标识符（model ID）触发，无需修改 API 协议或 SDK，但适用场景、资源隔离级别与计费模型存在本质差异。开发者应根据业务对确定性、成本敏感度与流量可预测性的要求进行选型。

## 支持的模型/功能

- **Prime 模式**：面向对输出速度敏感的通用场景（如实时对话、Agent 多步推理），提供 1.5~2 倍于标准 API 的 TPS 提升，**不提供容量独占保障**。支持模型包括 `glm-5.3-prime`、`glm-5.2-fast-preview`、`wan3.0-video-prime` 等，具体以 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 文档所列为准。  
- **吞吐预留**：为指定模型锁定专属推理容量（TPM），确保高峰期不受公共资源限流影响。支持 `Qwen3.8-Max`、`GLM-5.3`、`DeepSeek-v4-Pro` 等数十个主流模型，完整列表见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档。  
> **注意**：`glm-5.2-fast-preview` 在 Prime 模式中可用，但在吞吐预留文档中仅列出 `GLM-5.2`（无 `-fast-preview` 后缀）。实际调用时需使用吞吐预留生成的专属 model code，而非原模型名；该差异表明 Prime 模式与吞吐预留是正交能力，不可混用 model ID。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **性能提升** | 固定 1.5~2× TPS（无容量承诺） | 可选「标准模式」或「高速模式」（后者等效于 PTU 部署，TPS 提升 1.5~2×） |
| **容量保障** | 无专属容量；依赖平台剩余资源，实际 TPS ≥ 限流值 | 专属 kTPM 容量刚性兑付，预留内调用完全隔离 |
| **溢出策略** | 不适用（无预留概念） | 可选「自动溢出至按量计费」（默认）或「仅预留容量，超限返回 429」 |
| **计费单位** | 按输入/输出 token 计费（与标准 API 一致） | 按预付费 kTPM（输入/输出分开计量）+ 超额部分按 token 计费（若启用自动溢出） |

## 使用方式

- **Prime 模式**：直接将 `model` 参数设为对应 Prime 模型 ID（如 `"glm-5.2-fast-preview"`），请求域名使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。[详见 Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 的调用示例与流式处理说明。  
- **吞吐预留**：在控制台创建实例后，获取系统生成的**专属模型 code**，并在 API 请求中将其作为 `model` 值传入（替换原模型名）。接入域名与标准 API 相同（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。[详见 吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 的创建流程与代码示例。  
> **注意**：吞吐预留实例创建后需等待状态变为「运行中」方可调用；短时间内请求量快速拉升时，系统需短暂预热，期间可能出现延迟波动，建议客户端实现排队或重试机制。

## 限制和注意事项

- **模型能力一致性**：Prime 模式下模型的功能、限制与原版模型完全相同（如 `glm-5.2-fast-preview` 仍支持 `reasoning_content` 字段）；吞吐预留亦不改变基础模型行为，但 `GLM-5.2` 的 `thinking_budget` 参数在吞吐预留调用中不生效。  
- **地域与模型绑定**：Prime 模式与吞吐预留均按地域（如华北2、新加坡）独立配置，模型 ID 和价格因地域而异，不可跨地域复用。  
- **资源生命周期**：吞吐预留实例到期后有 2 小时宽限期（可续费），14 小时后彻底释放且专属 model code 失效；8 小时时段预留无宽限期，到期即失效。Prime 模式无生命周期管理，随 API Key 权限生效。  
- **调试与监控**：吞吐预留提供详细的「超额降级统计」和「利用率趋势」监控，便于容量评估；Prime 模式无专用监控视图，需依赖通用 API 指标。建议高可用业务优先采用吞吐预留并开启自动溢出策略，避免突发流量导致服务中断。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


