# model high speed inference

百炼平台的 high speed inference（高速推理）能力面向低延迟、高并发的生产场景，通过 Prime 模式与吞吐预留（TPM Reservation）两项核心技术实现稳定毫秒级响应。该能力适用于实时对话、搜索补全、API 网关等对 SLA 敏感的服务。其配置与生效依赖[模型部署](../concepts/model-deployment.md)时的运行时参数和资源策略。

## 支持的模型/功能

- 仅限已上线的 **SaaS 模型**（如 `qwen-max`, `qwen-plus`, `qwen-turbo`）支持 high speed inference；自定义微调模型（Fine-tuned Model）暂不支持 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)。  
- 支持两种加速模式：  
  - **Prime 模式**：自动启用模型预热、KV Cache 优化与请求队列优先级调度，降低 P99 延迟；  
  - **吞吐预留（TPM Reservation）**：按需预购每分钟 [Token](../concepts/token.md) 处理量（TPM），保障最低服务吞吐与稳定性，避免突发流量导致排队 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)。  
- 不支持[多模态](../concepts/multi-modal.md)模型（如 `qwen-vl`）及非标准输入格式（如非 JSON-RPC 的二进制协议）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `speed_mode` | string | 否 | 可选 `"prime"` 或 `"none"`；设为 `"prime"` 即启用 Prime 模式；默认为 `"none"` |
| `tpm_reservation` | integer | 否 | 预留 TPM 值（≥1000），单位：tokens/minute；需提前在控制台购买配额，否则请求将降级为普通模式 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md) |
| `max_tokens` | integer | 否 | 建议 ≤ 2048；过大的生成长度会显著削弱 Prime 模式的延迟收益 |

> **注意**：文档中提及的 `enable_prime` 布尔参数已被废弃，当前统一使用 `speed_mode` 字符串字段；旧 SDK 示例中若仍使用该字段，将被忽略并记录 warning 日志。

## 使用方式

1. **控制台配置**：在「模型服务」→「部署管理」中选择目标模型实例，点击「编辑配置」，勾选「启用高速推理」，并设置 TPM 预留值（需已有可用配额）。  
2. **API 调用**（HTTP）：在请求 body 中显式传入参数：
   ```json
   {
     "model": "qwen-plus",
     "speed_mode": "prime",
     "tpm_reservation": 5000,
     "input": { "messages": [...] }
   }
   ```
3. **SDK 调用**（Python）：
   ```python
   client.chat.completions.create(
       model="qwen-plus",
       speed_mode="prime",
       tpm_reservation=5000,
       messages=[...]
   )
   ```

## 限制和注意事项

- Prime 模式仅在模型实例处于 **Running** 状态且无 pending 更新任务时生效；滚动升级期间自动暂停，恢复后需手动触发预热（或等待 2 分钟自动恢复）。  
- TPM 预留配额不可跨模型、跨地域共享；未使用的配额不累计、不退款。  
- 当实际请求速率持续超过 `tpm_reservation × 1.2` 时，系统将开始限流并返回 `429 Too Many Requests`，此时需扩容或优化 [prompt](prompt.md) 长度。  
- > **注意**：部分历史文档称 “Prime 模式支持流式响应（stream=true）”，但实测 v2.3.0+ 版本中，启用 `speed_mode="prime"` 时 `stream=true` 将被强制忽略并静默降级为非流式——该行为已在 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md) 的最新修订版中修正说明。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)



