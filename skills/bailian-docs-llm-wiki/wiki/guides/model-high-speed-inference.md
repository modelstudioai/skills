# model high speed inference

百炼平台的 model high speed inference 是面向低延迟、高并发场景优化的推理服务模式，适用于实时对话、搜索补全、流式响应等对端到端时延敏感的业务。该模式通过资源隔离、预热加载与调度优化，在保障 SLO 的前提下显著降低 P99 延迟。其能力依赖底层模型部署形态与配额配置，需结合具体模型规格使用。

## 支持的模型/功能

- 当前仅支持已标注 `high_speed_inference: true` 的模型（如 `qwen-max-20240919`、`qwen-plus-20240919`），不支持自定义模型或未发布版本。  
- 支持两种核心加速机制：[Prime 模式](raw/model-user-guide/model-high-speed-inference/prime-mode.md)（单请求优先调度）和 [吞吐预留](raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)（TPM 级别资源锁定）。  
- 功能启用需在创建推理服务实例时显式声明 `inference_mode: "high_speed"`，否则默认走标准推理路径。详情见 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `inference_mode` | string | 是 | 固定值 `"high_speed"`，不可与其他 mode 混用 |
| `prime_enabled` | boolean | 否 | 启用 Prime 模式（默认 `false`）；启用后自动禁用 `tpm_reservation` |
| `tpm_reservation` | integer | 否 | 预留每分钟 [Token](../concepts/token.md) 处理量（TPM），最小值为 1000，最大值依模型而定；与 `prime_enabled` 互斥 |
| `max_batch_size` | integer | 否 | 最大批处理大小（仅当未启用 Prime 且未设 TPM 时生效），默认 `1` |

> **注意**：`tpm_reservation` 的最大值在 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中定义为 60000，但 [原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 明确指出 Prime 模式下该字段将被忽略——二者逻辑一致，无矛盾；但需注意配置互斥性，避免无效参数被静默丢弃。

## 使用方式

1. 在调用 `/v1/chat/completions` 或 `/v1/completions` 时，于 `body` 中传入上述关键参数（非 header）；  
2. 若启用 `prime_enabled: true`，请求将获得最高调度优先级，但不保证绝对延迟上限（受模型实际计算负载影响）；  
3. 若设置 `tpm_reservation: 5000`，系统将为该服务实例预留对应 TPM 资源，超出部分可能排队或限流；  
4. 所有 high speed 请求必须使用 `model` 字段指定支持该模式的模型 ID，否则返回 `400 Bad Request`。完整参数示例可参考 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)。

## 限制和注意事项

- 单账号下 high speed inference 实例总数上限为 5 个（含 Prime 和 TPM 预留类型）；  
- 不支持 streaming 响应（`stream: true`）与 high speed mode 共用，强制设置将被拒绝；  
- 模型 warmup 时间约为 30–60 秒，首次请求延迟可能偏高，建议通过健康检查接口预热；  
- 日志中 `inference_type` 字段将标记为 `"high_speed"`，可用于监控链路区分；  
- 资源超售行为不受保障：当集群整体负载 > 85% 时，high speed SLO（P99 < 800ms）可能临时降级。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


