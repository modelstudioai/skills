# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**吞吐预留（TPM Reservation）** 和 **Prime 模式**。前者通过预付费锁定专属容量保障服务稳定性，后者以更高 TPS 和兼容标准 API 的方式提供按量计费的加速体验。二者可独立使用，也可组合满足不同 SLA 要求。

## 支持的模型/功能

- **吞吐预留**：支持 Qwen3.x 系列（如 `Qwen3.8-Max`）、GLM-5.x 系列（如 `GLM-5.3`）、DeepSeek-v4 系列及 Kimi-K2.6 等主流模型，覆盖华北2（北京）与新加坡地域。支持「标准模式」与「高速模式」（即 PTU 部署），其中高速模式可提供 1.5～2 倍于标准 API 的 TPS [吞吐预留 (raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **Prime 模式**：当前支持 `glm-5.3-prime`、`glm-5.2-fast-preview` 及 `wan3.0-video-prime`，仅限文本生成与视频生成两类任务，地域覆盖同上 [Prime 模式 (raw/model-user-guide/model-high-speed-inference/prime-mode.md)](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
> **注意**：文档 1 中将“高速模式”定义为 PTU 专属部署的一种性能档位，而文档 2 中的 Prime 模式是独立命名、无需专属 code、直接通过 model ID 调用的加速通道。二者技术路径不同（前者为资源隔离，后者为调度与 kernel 优化），**不可混用或等价替换**；开发者应根据是否需要容量刚性保障（选吞吐预留）或仅需更高输出速率（选 Prime）进行选型。

## 关键参数

| 参数 | 吞吐预留 | Prime 模式 |
|------|-----------|-------------|
| **调用标识** | 专属模型 code（如 `tpm-reserved-xxx`），需替换 `model` 字段 [吞吐预留 (raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) | 原生 model ID（如 `glm-5.2-fast-preview`），无需额外参数 |
| **性能指标** | 输入/输出 TPM（kTPM），可分别配置；TPS 提升依赖所选「性能模式」（标准/高速） | TPS 提升 1.5～2 倍（相对标准 API），无显式 TPM 配置项 |
| **溢出策略** | 创建时可选：「自动溢出至按量」（默认）或「仅预留容量（429）」 | 不适用；实际可用 TPS 不低于限流值，平台有余量时不触发限流 |
| **缓存行为** | 支持缓存命中率影响输入 TPM 消耗估算 | 支持缓存（如 `glm-5.2-fast-preview` 支持 `cached_tokens` 统计） |

## 使用方式

- **吞吐预留**：创建成功后，在控制台获取专属模型 code，并在 API 请求中将其设为 `model` 值。示例：
  ```python
  response = dashscope.Generation.call(
      model="tpm-reserved-abc123",  # 替换为实际 code
      messages=[{"role": "user", "content": "你好"}]
  )
  ```
  > 注意：短时间内请求量快速拉升时，系统需短暂预热，期间可能出现延迟波动，建议实现请求排队或重试机制 [吞吐预留 (raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

- **Prime 模式**：直接使用对应 model ID 发起请求，**必须使用专属接入域名**（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），不可复用标准 dashscope 域名：
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model":"glm-5.2-fast-preview","messages":[{"role":"user","content":"你是谁"}]}'
  ```

## 限制和注意事项

- **模型兼容性**：`GLM-5.2` 在吞吐预留中不支持 `thinking_budget` 参数；而 Prime 模式下 `glm-5.2-fast-preview` 保留完整 reasoning 能力（含 `reasoning_content` 字段与 `reasoning_tokens` 统计）。
- **地域与计费约束**：8 小时时段预留仅支持标准模式，且下单窗口严格限定为每日 22:00–00:00；该时段预留不适用 2 小时宽限期，到期即失效 [吞吐预留 (raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **退订与失效**：吞吐预留退订后专属 model code 立即失效，请求回退至公共资源；Prime 模式无生命周期管理，只要 model ID 有效且配额充足即可持续调用。
- **监控与诊断**：吞吐预留提供「超额降级统计」与细粒度监控（含缓存命中量）；Prime 模式暂未提供独立监控页签，其用量计入标准模型调用统计，需通过 `usage` 字段解析 `reasoning_tokens` 等明细。

## 来源文档

- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)


