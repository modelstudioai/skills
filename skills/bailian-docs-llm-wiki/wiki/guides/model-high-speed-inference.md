# model high speed inference

百炼平台提供多种高吞吐、低延迟的推理加速能力，核心包括吞吐预留（TPM Reservation）与 Prime 模式两类机制。前者通过预付费锁定专属容量保障确定性 SLA，后者以无感接入方式提升输出 TPS 且保持按 token 计费。二者可独立使用，也可组合满足不同业务场景对稳定性、速度与成本的综合诉求。

## 支持的模型/功能

- **吞吐预留**：支持 Qwen3.x 系列（如 `Qwen3.8-Max`）、GLM-5.x 系列（如 `GLM-5.3`）、DeepSeek-v4 系列及 Kimi-K2.6 等主流模型，覆盖华北2（北京）和新加坡地域。详情见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **Prime 模式**：当前支持 `glm-5.3-prime`、`glm-5.2-fast-preview` 及 `wan3.0-video-prime`，仅限文本生成与视频生成两类任务，不支持所有 Qwen 或 DeepSeek 模型。详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- > **注意**：文档 1 中提及“性能模式”含「高速模式（即 PTU 模型部署）」，但该描述实际指向 PTU 专属部署方案，**并非 Prime 模式**；Prime 模式是独立于吞吐预留的轻量级加速通道，无需专属 model code，也无 TPM 预留要求。二者技术路径与适用边界不同，请勿混淆。

## 关键参数

| 参数 | 吞吐预留 | Prime 模式 |
|------|-----------|-------------|
| **核心标识** | 专属 `model` code（如 `tpm-reserved-xxx`），由控制台自动生成 | 固定 model ID（如 `glm-5.2-fast-preview`），直接调用 |
| **性能提升** | 依赖「性能模式」选择：标准模式（TPS 同公共 API）或高速模式（TPS 提升 1.5~2 倍，等效 PTU） | 默认高速输出，TPS 提升 1.5~2 倍，无需配置 |
| **计费单位** | 预付费 kTPM（输入/输出分离），预留内调用不额外计费；溢出部分按 token 计费 | 完全按 token 计费，与标准 API 计费逻辑一致，无预付 |
| **限流行为** | 预留容量内无公共限流；溢出策略决定是否降级（自动溢出）或返回 429 | 存在独立限流阈值，但平台有资源时**实际可用 TPS 不低于限流值**，具备弹性缓冲能力 |

## 使用方式

- **吞吐预留**：创建后获取专属 model code，在 API 请求中替换 `model` 字段即可生效。示例见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的 Python/curl 调用片段。注意：短时间内请求量快速拉升需预热，建议实现请求排队或重试机制。
- **Prime 模式**：直接使用对应 model ID（如 `glm-5.2-fast-preview`），调用域名需为工作空间专属地址 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。接入零改造，无需修改参数或鉴权方式。参考 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 中的 OpenAI 兼容 SDK 示例。
- > **注意**：`glm-5.2` 在 Prime 模式下模型名为 `glm-5.2-fast-preview`，而文档 1 中明确指出 GLM-5.2 的 `thinking_budget` 参数在吞吐预留调用时不生效——该限制**不适用于 Prime 模式**，其参数兼容性以原版模型为准。

## 限制和注意事项

- **地域限制**：吞吐预留与 Prime 模式均仅支持华北2（北京）和新加坡地域，其他地域暂不可用。
- **缓存行为差异**：吞吐预留支持缓存命中率配置并影响输入 TPM 估算；Prime 模式虽支持缓存（见计费表中“缓存命中”单价），但无显式缓存控制参数，命中逻辑由服务端自动处理。
- **生命周期管理**：吞吐预留实例到期后有 2 小时宽限期（按天购买），期间仍可调用；8 小时时段预留无宽限，到期即失效。Prime 模式无有效期概念，只要模型可用即可持续调用。
- **监控与诊断**：吞吐预留提供专属监控页签（含利用率、超额降级统计等）；Prime 模式监控需通过通用模型监控路径查看，详情参见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **模型能力一致性**：Prime 模式下模型能力、输入/输出格式、流式字段（如 `reasoning_content`）与原模型完全一致；吞吐预留亦保持相同语义，但部分参数（如 `thinking_budget`）可能受限。

## 来源文档

- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)


