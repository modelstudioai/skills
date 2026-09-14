# model high speed inference

百炼平台的 high speed inference（高速推理）能力面向低延迟、高并发的生产场景，通过 Prime 模式与吞吐预留（TPM Reservation）两项核心技术实现稳定毫秒级响应。该能力适用于实时对话、搜索补全、API 网关等对 SLA 敏感的服务。其配置与生效依赖[模型部署](../concepts/model-deployment.md)时的运行时参数和资源策略。

## 支持的模型/功能

- 仅限已上线的 **SaaS 模型**（如 `qwen-max`, `qwen-plus`, `qwen-turbo`）支持 high speed inference；自定义训练模型（Fine-tuned Model）暂不支持 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)。  
- 支持两种加速模式：  
  - **Prime 模式**：自动启用模型预热、内存常驻与请求队列优化，降低冷启与抖动 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)；  
  - **吞吐预留（TPM Reservation）**：按需预购每分钟 [Token](../concepts/token.md) 处理量（TPM），保障最低服务吞吐与 P99 延迟上限 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `speed_mode` | string | 是 | 取值为 `"prime"` 或 `"reserved"`；不可同时启用两者 |
| `tpm_reservation` | integer | 仅当 `speed_mode="reserved"` 时必填 | 最小值 100，最大值由配额决定；单位：tokens/minute |
| `max_batch_size` | integer | 否 | Prime 模式下建议设为 `1`（禁用批处理）以保低延迟；默认 `4` |

> **注意**：文档中未明确 `speed_mode="prime"` 时是否允许设置 `tpm_reservation`，但实测会触发参数冲突错误；请严格遵循单模式原则，避免混用。

## 使用方式

1. 在调用 `POST /v1/chat/completions` 时，于请求体 `body` 中添加 `speed_mode` 字段（示例）：
   ```json
   {
     "model": "qwen-plus",
     "speed_mode": "prime",
     "messages": [{"role": "user", "content": "你好"}]
   }
   ```
2. 若启用吞吐预留，需提前在控制台「模型服务」→「TPM 预留」页面完成配额申请与绑定，否则请求将被拒绝（HTTP 403）；详情见 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)。

## 限制和注意事项

- Prime 模式仅对单次请求 token 数 ≤ 2048 的场景提供最优延迟保障；超长上下文（如 >4K tokens）可能退化为普通模式。  
- 吞吐预留配额按自然日重置，未使用部分不累计；且不支持跨模型共享（例如为 `qwen-turbo` 预留的 TPM 不能用于 `qwen-max`）。  
- 所有 high speed inference 请求均计入独立计费项，单价高于标准推理；具体资费以控制台最新公示为准。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


