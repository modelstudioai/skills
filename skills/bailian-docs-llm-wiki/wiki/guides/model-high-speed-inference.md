# model high speed inference

百炼平台提供多种面向高吞吐、低延迟推理场景的加速能力，主要包括 Prime 模式（轻量级性能增强）和吞吐预留（专属容量保障）。二者均通过模型标识符（`model` 参数）切换，无需修改 API 接口或 SDK，适用于对响应速度、稳定性有明确要求的生产环境。选择方案时需结合业务流量特征（是否可预估、峰值持续时间、容错能力）与成本模型综合决策。

## 支持的模型/功能

- **Prime 模式**：面向输出速度敏感场景（如 AI 编程助手、Agent 多步推理、实时对话），在标准 API 基础上提升 1.5~2 倍 TPS，不改变模型能力与限制。支持模型包括 `glm-5.3-prime`、`glm-5.2-fast-preview`、`wan3.0-video-prime` 等，详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：为指定模型锁定专属 TPM（Tokens Per Minute）容量，实现刚性容量保障。支持主流大模型，如 `Qwen3.8-Max`、`GLM-5.3`、`DeepSeek-v4-Pro` 等，覆盖华北2（北京）与新加坡地域，具体列表见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：Prime 模式文档中列出的 `glm-5.2-fast-preview` 在吞吐预留文档中对应基础模型 `GLM-5.2`，但二者能力边界不同——Prime 是模型变体，吞吐预留是容量调度策略；调用 `glm-5.2-fast-preview` 无法享受吞吐预留保障，反之亦然。两者不可叠加使用。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **核心标识** | 模型 ID（如 `glm-5.2-fast-preview`） | 专属模型 code（控制台生成，非公开模型名） |
| **性能档位** | 固定高速档（无配置项） | 创建时可选「标准模式」或「高速模式」（后者等效 PTU 部署，TPS 提升 1.5~2 倍） |
| **容量单位** | 无显式容量配置，依赖平台动态资源池 | 输入/输出 TPM（kTPM），按分钟级吞吐量预设 |
| **溢出行为** | 不适用（无预留概念） | 可选「自动溢出至按量计费」（默认）或「仅使用预留容量（返回 429）」 |

## 使用方式

- **Prime 模式**：直接将请求中的 `model` 参数设为 Prime 模型 ID（如 `"glm-5.2-fast-preview"`），接入域名使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。流式响应中需分别处理 `delta.reasoning_content` 与 `delta.content` 字段，详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 示例。
- **吞吐预留**：创建成功后，在控制台获取专属模型 code，并将其填入 `model` 参数。调用域名与标准 API 一致（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。**注意**：短时间内请求量快速拉升时，系统需短暂预热，期间可能出现延迟波动，建议客户端实现排队或重试机制，参见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 限制和注意事项

- **模型兼容性**：Prime 模式下模型能力、输入/输出限制、缓存逻辑与原版模型完全一致；吞吐预留不改变模型能力，但部分参数（如 GLM-5.2 的 `thinking_budget`）在预留实例上调用时无效。
- **地域与模型绑定**：Prime 模型按地域独立发布（如北京与新加坡价格不同），吞吐预留也需在对应地域控制台创建并绑定模型，跨地域不共享。
- **计费差异**：Prime 按实际 token 计费，与标准 API 一致；吞吐预留为预付费模式，预留容量内调用不额外计费，超额部分按所选溢出策略处理（自动溢出则转按量，仅预留则返回 429）。
- **生命周期管理**：吞吐预留实例到期后有 2 小时宽限期（按天预留），期间仍可调用；8 小时时段预留无宽限，到期即失效。退订后专属模型 code 立即失效，请求回退至公共资源，详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


