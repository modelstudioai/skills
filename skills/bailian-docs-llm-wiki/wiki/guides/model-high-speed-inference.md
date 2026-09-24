# model high speed inference

百炼平台提供多种面向高吞吐、低延迟推理场景的加速能力，主要包括 Prime 模式（轻量级性能增强）和吞吐预留（专属容量保障）。二者均通过模型标识符（`model` 参数）切换，无需修改 API 接口或 SDK，适用于对响应速度、稳定性有明确要求的生产级 AI 应用。核心目标是提升实际可用 TPS，同时兼顾计费透明性与接入简易性。

## 支持的模型/功能

- **Prime 模式**：面向通用高速输出场景，提供 1.5~2 倍于标准 API 的 TPS，适用于 AI 编程助手、Agent 多步推理、实时对话等对首 token 和后续 token 延迟敏感的业务。其模型为独立命名的优化版本（如 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime`），能力与对应原版模型一致，详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：面向流量可预估、不可接受限流的高保障场景，为指定模型锁定专属 TPM 容量（输入/输出分离计量），支持标准模式与高速模式（即 PTU 部署档位）。支持模型包括 Qwen 系列（如 `Qwen3.8-Max`）、GLM 系列（如 `GLM-5.3`）、DeepSeek 系列（如 `DeepSeek-v4-Pro`）等，具体以控制台实时列表为准，详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：文档 1 中 `glm-5.2-fast-preview` 被列为 Prime 模式专属模型；而文档 2 中 `GLM-5.2` 列为吞吐预留支持模型，但未标注是否兼容 Prime 性能档位。实际使用中，若需 Prime 级别 TPS 且要求容量刚性保障，应选择吞吐预留的「高速模式」而非标准模式，并确认该模型在控制台创建页中“性能模式”选项可用。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **性能提升** | 固定 1.5~2× TPS（相比同模型标准 API） | 可选「标准模式」（同标准 API）或「高速模式」（1.5~2× TPS） |
| **容量保障** | 无专属容量，依赖平台剩余资源（特殊限流逻辑） | 专属 kTPM 容量，刚性兑付，不与其他用户共享 |
| **计费单位** | 按实际输入/输出 token 计费（与标准 API 一致） | 预付费购买 kTPM（按天或 8 小时时段），预留内调用不额外计费；溢出部分按 token 计费（若启用自动溢出） |
| **模型标识** | 使用预定义 Prime 模型 ID（如 `glm-5.2-fast-preview`） | 使用系统生成的专属 `model code`（如 `tpm-xxx`），不可复用原模型名 |
| **溢出行为** | 达限流值后仍可能继续服务（不触发 429），但延迟可能上升 | 可配置：「自动溢出」（降级为按量，返回 200）或「仅预留容量」（超限返回 429） |

## 使用方式

- **Prime 模式**：直接将请求中的 `model` 参数设为对应 Prime 模型 ID（如 `"model": "glm-5.2-fast-preview"`），调用域名与标准 API 相同（`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），无需额外 header 或 query 参数。流式响应中需分别处理 `delta.reasoning_content` 与 `delta.content` 字段。
- **吞吐预留**：创建成功后，在控制台详情页复制专属 `model code`，替换 API 请求中的 `model` 参数。接入示例与标准调用完全一致，仅模型名不同。注意：短时间内请求量快速拉升时，系统需短暂预热，建议客户端实现请求排队或重试机制，详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 限制和注意事项

- **模型能力一致性**：Prime 模式下模型的功能、上下文长度、输入/输出格式、错误码等均与对应原版模型完全一致，无能力降级或扩展。
- **地域与模型绑定**：Prime 模型与吞吐预留支持的模型均按地域（如华北2、新加坡）独立发布，价格与可用性存在差异，需按实际部署地域查阅控制台或文档。
- **缓存行为**：两者均支持 token 缓存（`cached_tokens` 字段可见于 usage），但 Prime 模式未明确说明缓存命中对 TPS 的影响；吞吐预留监控中可查看缓存命中量，命中率直接影响输入 TPM 消耗速率。
- **调试与监控**：Prime 模式无专属监控视图；吞吐预留提供完整的「概览」「监控」「API 接入」三页签，支持用量趋势、超额降级统计、配额内外调用分离分析，推荐高保障场景必用。
- **退订与失效**：吞吐预留退订后专属 `model code` 立即失效，请求回退至公共资源；Prime 模式无生命周期管理，只要模型在服务中即可持续调用。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


