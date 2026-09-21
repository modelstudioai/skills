# model high speed inference

百炼平台提供多种面向高吞吐、低延迟推理场景的加速能力，主要包括 Prime 模式（轻量级性能增强）和吞吐预留（专属容量保障）。二者均通过模型标识符（`model` 参数）切换，无需修改 API 接口或 SDK，适用于对响应速度、稳定性有明确要求的生产级 AI 应用。核心目标是提升实际可用 TPS，同时兼顾计费透明性与接入简易性。

## 支持的模型/功能

- **Prime 模式**：面向通用高速输出场景，提供 1.5~2 倍于标准 API 的 TPS，适用于 AI 编程助手、Agent 多步推理、实时对话等对首 token 和后续 token 延迟敏感的业务。其模型为独立命名的优化版本（如 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime`），能力与对应原版模型一致，详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：面向流量可预估、不可接受限流的高保障场景，为指定模型锁定专属 TPM 容量（输入/输出分离计量），支持标准模式与高速模式（即 PTU 部署档位）。支持模型包括 Qwen 系列（如 `Qwen3.8-Max`）、GLM 系列（如 `GLM-5.3`）、DeepSeek 系列（如 `DeepSeek-v4-Pro`）等，具体以控制台实时列表为准，详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：文档 1 中 `glm-5.2-fast-preview` 被列为 Prime 模式专属模型；而文档 2 中 `GLM-5.2` 列为吞吐预留支持模型，但未标注其是否具备 Prime 性能档位。实际使用时，若需 Prime 级别 TPS，应优先选用文档 1 明确列出的 `-fast-preview` 或 `-prime` 后缀模型；若需专属容量保障，则按文档 2 创建吞吐预留并选择对应基础模型。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **性能提升** | 固定 1.5~2× TPS（无需配置） | 可选「标准模式」（同标准 API）或「高速模式」（1.5~2× TPS） |
| **容量单位** | 无显式容量配置，依赖平台动态资源池 | 输入/输出 TPM（kTPM），按分钟级配额刚性兑付 |
| **溢出行为** | 不适用（无预留概念）；达限流值后仍可能继续服务（见“特殊限流”说明） | 可配置：「自动溢出至按量」（默认，服务不中断）或「仅预留容量」（超限返回 429） |
| **专属标识** | 使用预定义模型 ID（如 `glm-5.2-fast-preview`） | 创建后生成唯一 `专属模型 code`，必须替换 `model` 参数 |

## 使用方式

- **Prime 模式**：直接在标准 `/chat/completions` 请求中将 `model` 设为 Prime 模型 ID（如 `"glm-5.2-fast-preview"`），接入域名与标准 API 一致（`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），无需额外 header 或参数。流式响应中需处理 `delta.reasoning_content` 字段（如适用），详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：创建成功后，在控制台获取 `专属模型 code`，将其填入请求的 `model` 字段（如 `"tpm-xxx-yyy"`），其余参数与标准调用完全一致。注意：短时间内请求量快速拉升时存在短暂预热期，可能出现延迟波动，建议客户端实现排队或重试机制，详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 限制和注意事项

- **模型兼容性**：Prime 模式模型与原版模型能力一致，但 `thinking_budget` 等部分参数在吞吐预留调用中可能不生效（如 GLM-5.2），具体以各模型文档为准。
- **地域与模型覆盖**：Prime 模式与吞吐预留支持的模型列表及价格因地域（如华北2、新加坡）而异，且两者模型集合不完全重叠。务必以控制台实时展示为准，避免硬编码已下线模型 ID。
- **计费差异**：Prime 模式按实际输入/输出 token 计费，与标准 API 一致；吞吐预留为预付费模式，预留容量内调用不额外计费，溢出部分按量计费（若启用自动溢出）。完整计费规则请参考 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **状态管理**：吞吐预留实例存在 `运行中` → `已停止` → `已释放` 状态流转，服务到期后 2 小时内仍可调用，14 小时后彻底释放且不可恢复；退订将导致 `专属模型 code` 失效，请求自动回退至公共资源。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


