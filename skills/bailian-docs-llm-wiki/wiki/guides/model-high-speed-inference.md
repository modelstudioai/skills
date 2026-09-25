# model high speed inference

百炼平台提供多种高吞吐、低延迟推理能力，主要通过「吞吐预留」（TPM Reservation）和「Prime 模式」两类机制实现：前者通过预付费锁定专属容量保障稳定性，后者通过优化调度与算力分配提升单位时间输出速度。两者可独立使用，也可组合（如在吞吐预留中启用 Prime 性能模式），适用于对响应速度、服务可用性或成本结构有差异化要求的生产场景。

## 支持的模型/功能

- **吞吐预留**：支持 Qwen3.x 系列（如 `Qwen3.8-Max`）、GLM-5.x 系列（如 `GLM-5.3`）、DeepSeek-v4 系列及 Kimi-K2.6 等主流模型，覆盖华北2（北京）与新加坡地域。详情见[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **Prime 模式**：当前仅支持 `glm-5.3-prime`、`glm-5.2-fast-preview` 及 `wan3.0-video-prime`，按地域区分定价，不支持 Qwen 或 DeepSeek 系列。详情见[Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **性能模式叠加**：吞吐预留创建时可选「高速模式」（即 PTU 模型部署），该模式实际等效于 Prime 模式的 TPS 提升能力（1.5~2 倍标准 API），但需预付费并绑定专属 model code；而 Prime 模式为按量计费、无需预购，直接调用对应 `-prime` 或 `-fast-preview` 模型 ID 即可生效。

> **注意**：文档 1 中将「高速模式」描述为“即 PTU 模型部署”，但 PTU（Pre-provisioned Throughput Unit）在[模型部署](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)中被定义为完全隔离的专属实例部署方案，与吞吐预留中的「高速模式」在资源隔离粒度、扩缩容机制和计费模型上存在本质差异。此处「高速模式」实为吞吐预留内启用的 Prime 调度策略，非完整 PTU 部署。开发者应以控制台实际选项和[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)为准。

## 关键参数

| 参数 | 吞吐预留 | Prime 模式 |
|------|----------|------------|
| **核心标识** | 专属 `model` code（如 `tpm-reserved-xxx`），由系统生成 | 固定模型 ID（如 `glm-5.2-fast-preview`） |
| **性能档位** | 创建时选择「标准模式」或「高速模式」 | 无显式开关，调用 `-prime` 模型即自动启用 |
| **吞吐单位** | 输入/输出 TPM（kTPM），需分别配置 | 无 TPM 预留概念，按 token 实时限流，但实际 TPS ≥ 限流值 |
| **溢出策略** | 可选「自动溢出至按量」（默认）或「仅预留容量（429）」 | 不适用；超出限流仍可能成功（平台资源富余时） |
| **缓存行为** | 支持缓存命中率影响输入 TPM 消耗（见 TPM 计算器） | 支持缓存（如 `glm-5.2-fast-preview` 的 `cached_tokens` 字段） |

## 使用方式

- **吞吐预留**：创建后获取专属 model code，在 API 请求中替换 `model` 字段，并确保请求域名与标准百炼 API 一致（如 `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`）。示例见[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **Prime 模式**：直接调用指定模型 ID（如 `glm-5.2-fast-preview`），**必须使用专属接入域名**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（华北2）或对应新加坡地域域名。标准 dashscope 域名不支持 Prime 模式。
- **组合使用**：在吞吐预留中选择「高速模式」并完成购买后，其专属 model code 即具备 Prime 级 TPS 能力，此时仍使用标准 dashscope 域名调用，无需切换接入地址。

## 限制和注意事项

- **模型兼容性限制**：Prime 模式仅支持明确标注的模型（如 `glm-5.2-fast-preview`），调用非 Prime 模型 ID（如 `glm-5.2`）即使走 Prime 域名也不会提速；吞吐预留仅支持文档中列出的模型，控制台未展示的模型不可选。
- **地域与域名强绑定**：Prime 模式必须使用 `{workspace_id}.<region>.maas.aliyuncs.com` 域名，且 workspace_id 需与业务空间所在地域匹配；吞吐预留无此限制，但预留地域需与模型实际部署地域一致（如北京预留不可用于新加坡模型）。
- **预热与稳定性**：吞吐预留实例在流量快速拉升时需短暂预热，期间可能出现延迟波动，建议客户端实现请求排队或指数退避重试 —— 此要求同样适用于 Prime 模式突发流量场景，详见[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **状态生命周期**：吞吐预留到期后有 2 小时宽限期（可续费），14 小时后彻底释放；8 小时时段预留无宽限期，到期即失效。Prime 模式无生命周期管理，按量生效。

## 来源文档

- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)


