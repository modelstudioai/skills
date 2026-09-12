# model high speed inference

百炼平台提供高吞吐、低延迟的模型推理服务，适用于批量请求或高并发实时场景。其核心能力基于 Prime 模式与吞吐预留（TPM Reservation）机制实现资源隔离与性能保障。该能力需在创建应用或调用 API 时显式启用，并受模型类型与部署规格约束。

## 支持的模型/功能

- 仅限已上线的 **百炼托管模型**（如 Qwen 系列、Qwen-VL、Qwen-Audio），不支持用户自定义模型或 BYOM 部署；
- 支持两种加速模式：  
  - **Prime 模式**：自动优化调度与内存复用，降低首 token 延迟；  
  - **吞吐预留（TPM Reservation）**：预分配计算资源，保障稳定 QPS 上限，避免共享资源抖动。  
  详细能力覆盖请参见 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)。

## 关键参数

| 参数 | 说明 | 取值范围 | 是否必需 |
|------|------|----------|----------|
| `enable_prime` | 启用 Prime 模式 | `true` / `false` | 否（默认 `false`） |
| `tpm_reservation` | 预留吞吐量（tokens per minute） | ≥ 1000，且为 1000 的整数倍 | 否（启用后生效） |
| `max_batch_size` | 批处理最大请求数（仅 Prime 模式下生效） | 1–32 | 否（默认由系统动态调整） |

> **注意**：`tpm_reservation` 值不可超过所选实例规格的理论 TPM 上限，具体上限请查阅 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md) 中的规格对照表；部分旧版文档误标为“TPS 预留”，实际单位为 **tokens/minute**，以 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md) 为准。

## 使用方式

1. **控制台配置**：在「应用管理 → 创建应用」流程中，于「推理设置」区域勾选「启用高速推理」，并选择 Prime 模式或设置 TPM 预留值；  
2. **API 调用**（`/v1/services/aigc/text-generation/generation`）：在 `parameters` 字段中传入上述参数，例如：
   ```json
   {
     "parameters": {
       "enable_prime": true,
       "tpm_reservation": 5000
     }
   }
   ```
   更多请求示例见 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)。

## 限制和注意事项

- Prime 模式与 TPM 预留**不可同时禁用**：至少启用其中一项，否则回退至标准推理路径；  
- 吞吐预留按小时计费，未使用部分不退款；预留生效需约 2–5 分钟，期间请求可能被限流；  
- 不支持流式响应（`stream: true`）与 Prime 模式共用，启用 `enable_prime` 时必须关闭流式；  
- 多模态模型（如 Qwen-VL）仅支持 Prime 模式，暂不支持 TPM 预留。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


