# model high speed inference

百炼平台的 model high speed inference 是面向低延迟、高并发场景优化的推理服务模式，通过预热实例、资源独占和请求队列调度等机制，显著降低 P99 延迟并提升吞吐稳定性。该能力适用于实时对话、搜索排序、A/B 测试等对响应时效敏感的生产场景。详细设计原理可参考 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)。

## 支持的模型与功能

- 当前仅支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）及部分定制化 Llama3 模型（需白名单开通）；
- 支持 **Prime 模式**：自动保持最小实例数常驻，消除冷启动延迟；  
- 支持 **吞吐预留（TPM Reservation）**：按分钟级预购固定 TPM（[Token](../concepts/token.md)s Per Minute）配额，保障 SLA；  
- 不支持微调模型的直接部署，须先将微调权重合并至基础模型后启用 high speed inference。更多适用模型列表见 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)。

## 关键参数

| 参数 | 说明 | 取值范围 | 默认值 |
|------|------|----------|--------|
| `prime_enabled` | 是否启用 Prime 模式 | `true` / `false` | `false` |
| `tpm_reservation` | 预留 TPM 总量（含输入+输出 token） | ≥ 1000，步长 1000 | `0`（未预留） |
| `max_concurrent_requests` | 单实例最大并发请求数 | 1–32 | `8` |

> **注意**：`tpm_reservation` 与 `max_concurrent_requests` 存在隐式约束——当 `tpm_reservation = 1000` 时，系统强制限制 `max_concurrent_requests ≤ 4`，该行为与旧版文档中“无强耦合”的描述矛盾，以当前控制台实际生效策略为准；详情参见 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)。

## 使用方式

1. 在[模型部署](../concepts/model-deployment.md)页选择目标模型 → 点击「高级设置」→ 开启「High Speed Inference」开关；  
2. 根据业务负载配置 `prime_enabled` 和 `tpm_reservation`；  
3. 调用时在请求 Header 中添加 `X-Bailian-Mode: high-speed`（HTTP API）或设置 `mode="high-speed"`（SDK）；  
4. 首次启用后需等待约 2 分钟完成实例预热，期间请求将自动降级至标准模式。

## 限制和注意事项

- 不支持流式响应（`stream=true`）与 high speed inference 同时启用；  
- 输入长度超过 8192 token 或输出长度超 2048 token 时，自动回退至标准推理路径；  
- Prime 模式下实例不支持自动缩容，停用需手动关闭开关并等待 5 分钟释放资源；  
- 所有 high speed inference 请求计入独立计费项，不与标准推理共享配额。如需确认计费粒度，请查阅 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


