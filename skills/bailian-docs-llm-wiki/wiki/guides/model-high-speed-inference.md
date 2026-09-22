# model high speed inference

百炼平台提供多种高吞吐、低延迟的推理加速能力，主要通过「吞吐预留（TPM Reservation）」和「Prime 模式」两类机制实现：前者通过预付费锁定专属容量保障确定性服务，后者通过优化部署架构提升单位时间输出速度。两者可独立使用，也可组合（如在吞吐预留中启用高速模式），适用于对稳定性、响应速度或成本敏感的不同业务场景。

## 支持的模型/功能

- **吞吐预留**：支持 Qwen3.x 系列（如 `Qwen3.8-Max`）、GLM-5.x 系列（如 `GLM-5.3`）、DeepSeek-v4 系列（如 `DeepSeek-v4-Pro`）及 Kimi-K2.6 等主流模型，覆盖华北2（北京）与新加坡地域。具体支持列表以控制台实时展示为准，详见[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **Prime 模式**：当前支持 `glm-5.3-prime`、`glm-5.2-fast-preview` 及 `wan3.0-video-prime`，仅限文本生成与视频生成两类任务，不支持所有 Qwen 或 DeepSeek 模型。模型能力与原版一致，但输出 TPS 提升 1.5~2 倍，详见[Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- > **注意**：文档 1 中将「性能模式」分为「标准模式」与「高速模式」，并指出高速模式即 PTU [模型部署](../concepts/model-deployment.md)；而文档 2 的 Prime 模式明确为独立部署形态、按 token 计费且无需专属 model code。二者技术路径不同：吞吐预留的「高速模式」本质是 PTU 专属实例，而 Prime 是共享资源池内的性能增强通道。**不可将 Prime 模式的 model ID（如 `glm-5.2-fast-preview`）用于吞吐预留的专属 model code 字段，反之亦然**。

## 关键参数

| 参数 | 吞吐预留 | Prime 模式 |
|------|----------|------------|
| **核心标识** | 专属 model code（如 `tpm-reserved-xxx`），由控制台创建后自动生成 | 固定 model ID（如 `glm-5.2-fast-preview`），直接写入请求 |
| **性能档位** | 创建时选择「标准模式」或「高速模式」（后者 TPS 提升 1.5~2 倍） | 默认高速输出，无显式开关 |
| **容量单位** | 输入/输出 TPM（kTPM），需分别配置 | 无容量预留概念，按实际 token 计费 |
| **溢出策略** | 可选「自动溢出至按量」或「仅预留容量（429）」 | 无溢出概念；达限流阈值时若平台有余量仍可服务，实际 TPS ≥ 限流值 |
| **缓存支持** | 支持（但 GLM-5.2 的 `thinking_budget` 参数在调用时不生效） | 支持（`cached_tokens` 在 usage 中返回） |

## 使用方式

- **吞吐预留**：创建成功后，在 API 请求中将 `model` 替换为控制台提供的专属 model code 即可生效。示例：
  ```python
  response = dashscope.Generation.call(
      model="tpm-reserved-abc123",  # 替换为此 code
      messages=[{"role": "user", "content": "你好"}]
  )
  ```
  详细步骤见[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

- **Prime 模式**：直接使用指定 model ID 发起请求，**必须使用专属接入域名**（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），不可使用通用 dashscope 域名。示例：
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model":"glm-5.2-fast-preview","messages":[{"role":"user","content":"你是谁"}]}'
  ```
  详见[Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。

- > **注意**：吞吐预留实例创建后存在短暂预热期，短时间内请求量快速拉升可能导致延迟波动；建议客户端实现请求排队或指数退避重试机制，该提示源自[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 限制和注意事项

- **地域与模型绑定**：吞吐预留与 Prime 模式均严格按地域（如华北2、新加坡）提供，model ID 和专属 code 不跨地域通用。
- **计费隔离**：吞吐预留为预付费模式，预留容量内调用不额外计费；Prime 模式为纯按 token 计费，与预留无关。两者费用不互通、不抵扣。
- **生命周期管理**：吞吐预留到期后 2 小时内仍可调用，14 小时后释放且 model code 失效；而 Prime 模式无有效期，只要账号有效、配额充足即可持续调用。
- **功能兼容性**：GLM-5.2 在吞吐预留中调用时 `thinking_budget` 参数不生效；而 Prime 模式下 `glm-5.2-fast-preview` 支持 `reasoning_content` [流式输出](../concepts/streaming-output.md)，需按特定字段解析（见[Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)示例）。
- **叠加与扩缩容**：吞吐预留支持叠加容量包与扩缩容，专属 model code 保持不变；Prime 模式无容量管理能力，仅能通过调整业务请求频率或切换模型来应对负载变化。

## 来源文档

- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)


