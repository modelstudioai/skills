# model high speed inference

百炼平台提供多种面向高吞吐、低延迟推理场景的加速能力，主要包括 Prime 模式（轻量级性能增强）和吞吐预留（专属容量保障）。二者均通过模型标识符（`model` 参数）触发，无需修改 API 协议或 SDK，适用于对响应速度、稳定性有明确要求的生产环境。选择时需根据业务负载特征（如可预测性、峰值强度、容错能力）权衡成本与确定性。

## 支持的模型/功能

- **Prime 模式**：面向通用高速输出场景，提供 1.5~2 倍于标准 API 的 TPS 提升，适用于 AI 编程助手、Agent 多步推理、实时对话等对输出速度敏感的场景。支持模型包括 `glm-5.3-prime`、`glm-5.2-fast-preview`、`wan3.0-video-prime` 等，具体以 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 文档所列为准。  
- **吞吐预留**：为指定模型锁定专属 TPM（[Token](../concepts/token.md)s Per Minute）容量，实现刚性容量保障，适用于流量可预估、不能接受限流的关键业务。支持模型覆盖 Qwen、GLM、DeepSeek、Kimi 等主流系列，详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档列表。  
- > **注意**：`glm-5.2-fast-preview` 在 Prime 模式中作为独立模型 ID 使用，而吞吐预留文档中仅列出 `GLM-5.2`（无 `-fast-preview` 后缀），二者是否等价未明确说明；实际调用时请以控制台生成的专属模型 code 或 Prime 模式文档中确认的 model ID 为准。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **触发方式** | 直接指定 model ID（如 `"glm-5.2-fast-preview"`） | 使用控制台生成的专属 model code（如 `"tpm-reserved-xxx"`） |
| **性能档位** | 固定高速档（TPS 提升 1.5~2×） | 可选「标准模式」或「高速模式」（后者等效于 PTU 部署，TPS 同样提升 1.5~2×） |
| **容量单位** | 无显式容量配置；实际可用 TPS 不低于限流值（见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)） | 按 kTPM（千 tokens/分钟）预设输入/输出吞吐量，支持叠加扩容 |
| **溢出策略** | 不适用（无预留概念） | 可选「自动溢出至按量计费」（默认）或「仅使用预留容量（返回 429）」 |

## 使用方式

- **Prime 模式**：无需额外参数，仅需将 `model` 设为对应 Prime 模型 ID，并使用兼容模式域名（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段。示例见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留**：创建成功后，在控制台详情页复制专属 `model code`，替换 API 请求中的 `model` 参数即可生效。首次调用可能存在短暂预热延迟，建议客户端实现请求排队或重试机制。接入示例见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- > **注意**：吞吐预留的「高速模式」与 Prime 模式在性能提升幅度上描述一致（1.5~2× TPS），但底层资源隔离级别不同（前者为专属容量，后者为共享池优化），不可混用或叠加；两者属于正交能力，应按业务 SLA 需求单独选用。

## 限制和注意事项

- **计费差异**：Prime 模式按实际输入/输出 token 计费，与标准 API 完全一致；吞吐预留为预付费模式，预留容量内调用不额外计费，超额部分按策略处理（自动溢出则转按量，仅预留则返回 429）。详细规则参见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 与 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 的计费说明。  
- **模型能力一致性**：Prime 模式下模型的功能、限制、输出格式与原版模型完全相同；吞吐预留亦继承基础模型全部能力，但部分参数（如 GLM-5.2 的 `thinking_budget`）在预留实例中不生效。  
- **地域与模型绑定**：两类能力均按地域（如华北2、新加坡）独立开通与配置，模型支持列表、价格、API 域名均因地域而异，不可跨地域复用 model ID 或 code。  
- **状态管理**：吞吐预留实例存在「运行中→已停止→已释放」状态迁移，服务到期后有 2 小时宽限期；Prime 模式无状态概念，依赖账号级限流与平台资源动态调度。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


