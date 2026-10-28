# model high speed inference

百炼平台的 model high speed inference（高速推理）能力面向低延迟、高并发的生产级推理场景，通过 Prime 模式与吞吐预留（TPM Reservation）两项核心技术，实现模型响应时间稳定可控、P99 延迟显著降低。该能力适用于实时对话、搜索补全、实时风控等对时延敏感的业务。所有功能均需在创建推理服务时显式启用，并受配额与模型兼容性约束。

## 支持的模型/功能

- **Prime 模式**：为指定模型实例独占分配 GPU 资源，关闭动态批处理与请求排队，确保单请求端到端延迟 ≤ 150ms（以 Qwen2-7B 为例）。仅支持部分已优化的开源模型（如 Qwen 系列、Llama3-8B），不支持自定义 LoRA 微调后的部署变体。  
- **吞吐预留（TPM Reservation）**：允许用户按需预购每分钟 [Token](../concepts/token.md) 处理量（TPM），平台保障该额度下的 P95 延迟不劣于承诺值（如 300ms）。该能力依赖底层资源池调度，[原文标题](../../raw/model-user-guide/model-high-speed-inference.md) 中明确指出其仅对 `qwen-max`、`qwen-plus` 及 `qwen-turbo` 三类模型开放。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `prime_enabled` | boolean | 否 | 启用 Prime 模式；若设为 `true`，则自动禁用 `max_batch_size` 和 `stream` 参数 |
| `tpm_reservation` | integer | 否 | 预留 TPM 值，范围 100–10000；设置后将触发配额校验与资源锁定 |
| `latency_sla_ms` | integer | 否 | 仅当 `tpm_reservation > 0` 时生效，指定 SLA 延迟阈值（单位 ms），取值 100–500 |

> **注意**：[原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 中描述 `prime_enabled` 默认为 `false`，但最新 API 文档（v2.3.1）要求显式传入，未传时行为未定义；请始终显式声明。  
> **注意**：[原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 提到 `tpm_reservation` 支持按小时释放，但当前控制台 UI 仅提供“永久预留”选项，API 层虽保留 `release_after_hours` 字段，实际未生效——该字段暂为预留接口，勿依赖。

## 使用方式

1. 创建服务时，在 `inference_config` 中配置高速推理参数：
   ```json
   {
     "model_id": "qwen-plus",
     "inference_config": {
       "prime_enabled": true,
       "tpm_reservation": 2000,
       "latency_sla_ms": 250
     }
   }
   ```
2. 调用时保持 `stream: false`（Prime 模式下流式响应被强制禁用）；  
3. 通过 `/v1/services/{service_id}/metrics` 接口实时查询 `p95_latency_ms` 与 `reserved_tpm_utilization` 指标，验证 SLA 达成情况。

## 限制和注意事项

- Prime 模式与 TPM 预留不可同时启用：若 `prime_enabled = true`，`tpm_reservation` 必须为 `0` 或未设置；反之亦然。  
- 所有高速推理服务不支持跨可用区容灾，故障恢复依赖单 AZ 内快速重建。  
- 模型版本升级（如 `qwen-plus-v1.2` → `v1.3`）将自动解除现有 TPM 预留，需重新申请；Prime 实例则需手动重建。  
- 资源隔离仅作用于推理阶段，预处理（[prompt](prompt.md) 工程、tokenize）与后处理（logit 解析）仍共享 CPU 资源，极端长 [prompt](prompt.md) 场景下可能影响端到端延迟稳定性。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


