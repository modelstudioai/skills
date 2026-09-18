# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的加速能力：**Prime 模式**（轻量级性能增强）和**吞吐预留**（专属容量保障）。二者均通过模型标识符（`model` 参数）启用，无需修改 API 协议或请求结构，适用于对输出速度敏感（如 AI 编程助手、实时对话）或业务稳定性要求极高（如 SaaS 服务 SLA 保障）的场景。开发者可根据流量可预测性、成本敏感度与容错能力选择合适方案。

## 支持的模型/功能

- **Prime 模式**：为特定模型提供优化推理路径，TPS 提升至标准 API 的 1.5~2 倍，**不隔离资源池**，依赖平台剩余资源动态调度。支持模型包括 `qwen3.8-max-prime`、`glm-5.2-fast-preview`、`wan3.0-video-prime` 等，详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- **吞吐预留**：为指定模型锁定专属 TPM（Tokens Per Minute）容量，实现刚性容量兑付，**完全隔离于公共资源池**。支持模型覆盖 Qwen、GLM、DeepSeek、Kimi 等主流系列，包括 `Qwen3.8-Max`、`GLM-5.2`、`DeepSeek-v4-Pro` 等，详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- > **注意**：`glm-5.2-fast-preview` 在 Prime 模式文档中被列为独立模型 ID；而在吞吐预留文档中，`GLM-5.2` 是预留对象，其专属模型 code 由系统生成。二者逻辑不同：前者是预置优化模型别名，后者是运行时动态生成的容量绑定标识。调用时不可混用，需严格按所选方案使用对应 model 字符串。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **启用方式** | 直接指定 `model`（如 `"glm-5.2-fast-preview"`） | 使用控制台生成的专属 `model` code（如 `"tpm-reserved-abc123"`） |
| **性能档位** | 固定高速模式（1.5~2× TPS） | 可选「标准模式」或「高速模式」（后者等效于 PTU 部署） |
| **容量单位** | 无显式容量配置，依赖平台弹性资源 | 显式配置输入/输出 TPM（单位：kTPM），支持叠加扩容 |
| **溢出行为** | 不适用（无容量承诺） | 可选：自动溢出至按量计费（默认）或返回 429 |
| **缓存支持** | 支持缓存命中计费折扣（如 `qwen3.8-max-prime` 输入缓存单价 3 元/百万 token） | 支持长输入阶梯系数与缓存折扣，具体规则见 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md) |

## 使用方式

- **Prime 模式**：仅需将请求中的 `model` 替换为对应 Prime 模型 ID，接入域名与标准 API 一致（`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。流式响应中需分别处理 `delta.reasoning_content` 与 `delta.content` 字段，详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 示例。
- **吞吐预留**：
  1. 在百炼控制台创建预留实例，填写模型、输入/输出 TPM、溢出策略等；
  2. 复制生成的专属 `model` code；
  3. 将 API 请求中 `model` 参数替换为该 code（其他参数不变）；
  4. 注意：首次调用后存在短暂预热期，期间可能出现延迟波动，建议客户端实现重试或排队机制。

## 限制和注意事项

- **资源隔离性**：Prime 模式**不保证容量独占**，高负载时仍可能受公共限流影响；吞吐预留则提供**物理/逻辑隔离的专属容量**，是唯一能规避公共限流的方案。
- **模型能力一致性**：Prime 模式下模型能力、输入/输出长度限制、工具调用等行为与原版模型完全一致；吞吐预留亦继承基础模型全部能力，但 `thinking_budget` 等部分参数在调用时可能不生效（如 GLM-5.2），详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 说明。
- **计费差异**：Prime 模式按实际 token 计费，与标准 API 完全一致；吞吐预留为预付费模式，预留容量内调用不额外计费，溢出部分才触发按量计费。
- **地域与模型对齐**：同一模型（如 `glm-5.2-fast-preview`）在华北2与新加坡地域的计费单价不同，且吞吐预留支持的模型列表在两地存在细微差异（如新加坡暂未列出 `Kimi-K2.6`），务必以控制台实时展示为准。
- > **注意**：吞吐预留文档中明确指出“服务到期后 2 小时内实例仍为运行中，可继续调用”，而 Prime 模式无生命周期管理概念——其可用性完全依赖账号权限与模型服务状态。两者运维边界清晰，不可相互替代。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


