# model high speed inference

百炼平台提供多种面向高吞吐、低延迟推理场景的加速能力，主要包括 Prime 模式（轻量级性能增强）和吞吐预留（专属容量保障）。二者均通过模型标识符（`model` 参数）触发，无需修改 API 协议或 SDK，适用于对响应速度、稳定性有明确要求的生产级 AI 应用。

## 支持的模型/功能

- **Prime 模式**：面向输出速度敏感场景（如实时对话、Agent 多步推理），提供 1.5~2 倍于标准 API 的 TPS 提升。支持模型包括 `glm-5.3-prime`、`glm-5.2-fast-preview`、`wan3.0-video-prime` 等，详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 文档。
- **吞吐预留**：为指定模型锁定专属 TPM（[Token](../concepts/token.md)s Per Minute）容量，实现刚性容量保障。支持 Qwen、GLM、DeepSeek、Kimi 等主流大模型系列，覆盖华北2（北京）与新加坡地域，具体列表见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档。
- > **注意**：`glm-5.2-fast-preview` 在 Prime 模式下仍沿用原模型名，而吞吐预留为同一基础模型（如 `GLM-5.2`）生成全新专属 `model` code，二者不可混用；调用时必须严格匹配对应模式的模型标识符。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **触发方式** | 直接使用预置模型 ID（如 `glm-5.2-fast-preview`） | 使用控制台生成的专属 `model` code |
| **性能档位** | 固定高速档（无配置项） | 创建时可选「标准模式」或「高速模式」（后者等效 PTU 部署，TPS 提升 1.5~2 倍） |
| **容量单位** | 无显式容量配置；实际 TPS 受平台资源动态调节 | 按 kTPM（千 token/分钟）预设输入/输出吞吐量 |
| **溢出行为** | 不适用（无预留概念） | 可选「自动溢出至按量计费」（默认）或「仅预留容量，超限返回 429」 |
| **计费粒度** | 按实际输入/输出 token 计费，与标准 API 一致 | 预付费购买 kTPM 容量，预留内调用不额外计费；溢出部分按 token 计费 |

## 使用方式

- **Prime 模式**：仅需将请求中的 `model` 字段设为对应 Prime 模型 ID（如 `"model": "glm-5.2-fast-preview"`），并确保请求域名指向兼容模式入口（`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段。完整示例见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：在百炼控制台创建实例后，复制生成的专属 `model` code，并在 API 请求中替换 `model` 参数。调用前需确保实例状态为「运行中」。注意：短时间内请求量快速拉升时存在短暂预热期，可能引发延迟波动，建议客户端实现排队或重试机制。接入细节参见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- > **注意**：吞吐预留创建时若选择「高速模式」，其性能表现与 Prime 模式接近（TPS 提升 1.5~2 倍），但二者底层资源隔离策略、计费模型与 SLA 保障等级不同，不可等价替代。

## 限制和注意事项

- **模型能力一致性**：Prime 模式下模型的功能、上下文长度、工具调用等能力与对应基础模型完全一致，无降级；吞吐预留亦不改变基础模型能力，仅保障容量 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **地域与模型绑定**：Prime 模型 ID 与地域强绑定（如 `glm-5.3-prime` 在北京与新加坡价格不同）；吞吐预留也需在目标地域创建，且专属 `model` code 仅在该地域有效。
- **缓存行为**：两者均支持 token 缓存（`cached_tokens`），但 Prime 模式在 `usage` 中明确返回 `prompt_tokens_details.cached_tokens`，而吞吐预留监控中提供独立的「缓存命中量」指标，详见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **退订与失效**：吞吐预留退订后专属 `model` code 立即失效，请求回退至公共资源；Prime 模式无生命周期管理，只要模型可用即可持续调用。
- **调试建议**：首次使用吞吐预留时，建议先以小容量（如 10 kTPM 输入/1 kTPM 输出）创建并观察 7 天用量趋势，再结合 [TPM 容量计算器](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 进行扩容。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


