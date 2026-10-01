# model high speed inference

百炼平台的 model high speed inference 是面向低延迟、高并发场景优化的推理服务模式，适用于实时对话、搜索补全、流式响应等对端到端时延敏感的业务。它通过专用计算资源调度、模型编译优化和通信协议精简，在保障 SLO 的前提下显著降低 P99 延迟。该能力需在创建模型服务实例时显式启用，并依赖底层硬件与模型架构的协同支持。

## 支持的模型/功能

- 当前仅支持 Qwen 系列（Qwen2、Qwen2.5、Qwen3）及部分 Llama3 衍生模型（如 `llama3-8b-instruct`），其他模型暂不支持 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)。
- 必须启用 **Prime 模式**（即预热 + 预分配 + 请求队列优先级调度），否则不触发高速推理路径 [原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- 支持吞吐预留（TPM Reservation），允许用户为关键服务锁定最小每分钟 Token 处理量，避免突发流量导致的排队或降级 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 关键参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `high_speed_enabled` | bool | 启用高速推理通道 | `false` |
| `prime_mode` | string | 可选 `"on"` / `"off"` / `"auto"`；设为 `"on"` 强制启用 Prime 模式 | `"off"` |
| `tpm_reservation` | integer | 预留 TPM（Tokens Per Minute），范围 100–100000 | `0`（未预留） |
| `max_concurrent_requests` | integer | 单实例最大并发请求数（影响资源分配粒度） | `32` |

> **注意**：`prime_mode: "auto"` 在 v3.2.1+ 版本中已废弃，文档 [原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 中仍保留该选项，实际行为等同于 `"off"`，请明确指定 `"on"` 或 `"off"`。

## 使用方式

1. 创建服务时在 `model_config` 中设置：
   ```json
   {
     "high_speed_enabled": true,
     "prime_mode": "on",
     "tpm_reservation": 5000,
     "max_concurrent_requests": 64
   }
   ```
2. 调用时需使用 `/v1/chat/completions` 接口（不支持 `/v1/completions` 等旧路径），且 `stream=true` 可进一步降低感知延迟。
3. 首次请求将触发 Prime 预热（约 2–5 秒），后续请求进入低延迟通路；若服务空闲超 60 秒，可能自动降级至普通模式，需再次预热。

## 限制和注意事项

- 不支持 LoRA 微调权重动态加载，所有高速推理实例必须基于完整权重部署。
- 输入 `max_tokens` 超过 2048 或输出长度超过 1024 时，延迟优势明显减弱，建议拆分长上下文。
- 吞吐预留（TPM）按小时计费，即使未用尽也全额收取；预留值不可在运行中动态调整，需重启实例生效 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- 多模态模型（如 Qwen-VL）当前**不支持**高速推理路径，相关说明见 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


