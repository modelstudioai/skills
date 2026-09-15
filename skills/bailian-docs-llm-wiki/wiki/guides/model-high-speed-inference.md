# model high speed inference

百炼平台提供模型高并发、低延迟推理能力，适用于对响应时间敏感的在线服务场景。其核心机制包括 Prime 模式（预热+常驻）和吞吐预留（TPM Reservation），可显著降低首 token 延迟并保障稳定 QPS。该能力需在创建应用或调用 API 时显式启用，并受模型类型与配额限制。

## 支持的模型/功能

- 当前仅支持部分 Qwen 系列模型（如 `qwen-max`, `qwen-plus`, `qwen-turbo`），其他模型开启后将自动降级为普通推理模式。  
- 支持两种加速模式：  
  - **Prime 模式**：通过模型预热与实例常驻，消除冷启动延迟，适合请求频率波动但要求首 token < 200ms 的场景 [原文标题](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)；  
  - **吞吐预留（TPM Reservation）**：按分钟级预留固定 TPM（Tokens Per Minute）资源，保障最低服务水位，适用于 SLA 可承诺的生产流量 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- 不支持多模态模型（如 `qwen-vl`）、自定义微调模型及非 Qwen 系列开源模型。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `enable_high_speed` | boolean | 是 | 启用高密推理开关，设为 `true` 才生效 |
| `mode` | string | 否 | 可选 `"prime"` 或 `"tpm_reservation"`；未指定时默认为 `"prime"` |
| `tpm_capacity` | integer | 仅 mode=tpm_reservation 时必填 | 预留 TPM 值，最小 1000，最大 50000（需审批） |
| `timeout` | integer | 否 | 请求超时（毫秒），Prime 模式建议 ≤ 30000，TPM 预留模式建议 ≥ 60000 |

> **注意**：文档 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md) 中未明确 `tpm_capacity` 的上下限，实际取值应以控制台配额页或 `GET /v1/models/{model}/quota` 接口返回为准，避免因超限导致创建失败。

## 使用方式

1. **API 调用**：在 `/v1/chat/completions` 请求体中添加 `extra_parameters` 字段：
   ```json
   {
     "model": "qwen-max",
     "messages": [...],
     "extra_parameters": {
       "enable_high_speed": true,
       "mode": "prime"
     }
   }
   ```
2. **控制台配置**：在「应用管理 → 创建应用」流程中，于「模型设置」页勾选「启用高速推理」并选择模式。  
3. **SDK 示例（Python）**：
   ```python
   client.chat.completions.create(
       model="qwen-max",
       messages=[...],
       extra_parameters={"enable_high_speed": True, "mode": "tpm_reservation", "tpm_capacity": 5000}
   )
   ```

## 限制和注意事项

- 单账号默认最多同时启用 3 个 Prime 实例或 2 个 TPM 预留实例，超出需提交配额申请；  
- Prime 模式下实例空闲 5 分钟后自动释放，再次请求将触发轻量级重预热（约 800ms 延迟）；  
- TPM 预留资源按分钟计费，即使无请求也持续扣费，建议结合监控告警动态调整；  
- 同一模型版本不可同时被 Prime 和 TPM 预留共用，否则后启用的模式会覆盖前者；  
- > **注意**：原始文档 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md) 将 Prime 模式归类为“Fast Mode”，但当前 API 字段名统一为 `mode: "prime"`，请勿使用 `"fast"` 等别名，否则将被忽略。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


