# model high speed inference

百炼平台提供多种高吞吐、低延迟的模型推理加速方案，主要包含 Prime 模式（轻量级性能增强）与吞吐预留（专属容量保障）两类机制。二者均通过模型标识符（model ID）切换，无需修改 SDK 或协议，适用于对响应速度、稳定性或确定性 SLA 有明确要求的生产场景。开发者应根据业务流量特征（可预测性、峰谷比、容错能力）选择合适方案。

## 支持的模型/功能

- **Prime 模式**：面向输出速度敏感场景（如 AI 编程助手、Agent 多步推理、实时对话），在标准 API 基础上提升 TPS 至 1.5~2 倍，**不改变模型能力与使用限制**。支持模型包括 `glm-5.3-prime`、`glm-5.2-fast-preview`、`wan3.0-video-prime` 等，按地域分列计费，详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：为指定模型锁定专属 TPM（[Token](../concepts/token.md)s Per Minute）容量，实现刚性容量保障。支持 Qwen、GLM、DeepSeek、Kimi 等主流大模型系列，但具体可用模型以控制台实时列表为准；**不支持所有 Prime 模型**（例如 `glm-5.2-fast-preview` 未出现在吞吐预留支持列表中）。详情见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：文档 1 中提及 `glm-5.2-fast-preview` 是 Prime 模式专用模型，而文档 2 的吞吐预留支持列表中仅包含 `GLM-5.2`（无 `-fast-preview` 后缀），二者为不同模型实例。调用 `glm-5.2-fast-preview` 不会触发吞吐预留容量，必须使用吞吐预留生成的专属 model code 才能启用预留资源。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **性能提升** | 固定 1.5~2× TPS 提升（相比同模型标准 API） | 可选「标准模式」（等同标准 API TPS）或「高速模式」（即 PTU 部署，1.5~2× TPS） |
| **容量单位** | 无显式容量配置；实际 TPS 受平台剩余资源动态影响（[原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 中称“实际可用 TPS 不低于限流值”） | 按 kTPM（千 tokens/分钟）预购输入/输出独立容量，支持叠加扩容 |
| **溢出行为** | 无溢出策略；超限请求直接进入公共池排队或限流 | 可选「自动溢出至按量计费」（默认，服务不中断）或「仅使用预留容量」（超限返回 HTTP 429） |
| **专属标识** | 使用预定义 model ID（如 `glm-5.2-fast-preview`） | 创建后生成唯一专属 model code，**必须替换 `model` 参数** |

## 使用方式

- **Prime 模式**：直接将 `model` 参数设为对应 Prime 模型 ID（如 `"glm-5.2-fast-preview"`），调用域名与标准 API 一致（`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），无需额外 header 或参数。流式响应中需处理 `delta.reasoning_content` 字段（[原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)）。
- **吞吐预留**：创建成功后，在控制台获取专属 model code，并**全局替换所有 API 请求中的 `model` 字段**。接入域名仍为标准兼容模式地址（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。注意：短时间内请求量快速拉升时存在短暂预热期，可能引起延迟波动，建议客户端实现重试或排队机制（[原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。

## 限制和注意事项

- **模型兼容性**：Prime 模式与吞吐预留是正交能力，不可叠加使用。例如，`glm-5.2-fast-preview` 仅支持 Prime 模式，不支持吞吐预留；而 `GLM-5.2` 可开通吞吐预留，但其预留实例默认运行于标准或高速模式，**并非 Prime 模式**。
- **计费差异**：Prime 模式按实际输入/输出 token 计费，与标准 API 完全一致；吞吐预留为预付费模式，预留容量内调用不额外计费，溢出部分才按 token 计费（[原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。
- **地域与模型绑定**：所有高加速能力均按地域隔离。华北2（北京）与新加坡的模型 ID、价格、支持列表均不同，跨地域调用需分别配置 workspace 和 model ID。
- **调试与监控**：吞吐预留提供完整的监控页签（利用率、超额降级统计等），而 Prime 模式无独立监控视图，需复用标准 API 的用量统计。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


