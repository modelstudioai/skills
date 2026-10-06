# model high speed inference

百炼平台的 model high speed inference 是面向低延迟、高并发场景优化的推理服务模式，适用于实时对话、搜索补全、流式响应等对端到端时延敏感的业务。该模式通过资源隔离、预热调度与硬件级加速协同，显著降低 P99 延迟并提升吞吐稳定性。其能力边界和配置方式需严格遵循平台当前运行时约束。

## 支持的模型/功能

- 当前仅支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）及部分 Llama3 定制量化版本（INT4/FP16），不支持非白名单模型或自定义 LoRA 微调后未重新编译的实例。  
- 核心功能包括：Prime 模式（[Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)）、吞吐预留（[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）及自动批处理（Auto-batching）启用开关。  
- 不支持动态 batch size 调整、运行时模型切换或跨 region 的共享实例复用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `mode` | string | 是 | 取值为 `"prime"` 或 `"default"`；`"prime"` 启用低延迟路径，需配合 `tpm_reservation` 使用 |
| `tpm_reservation` | integer | 否（`mode=prime` 时必填） | 预留每分钟 [Token](../concepts/token.md) 处理量（TPM），最小值 1000，最大值见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档 |
| `stream` | boolean | 否 | 设为 `true` 时启用流式响应，但 Prime 模式下流式首 token 延迟仍受 `tpm_reservation` 下限约束 |

> **注意**：原始文档中 `tpm_reservation` 单位曾被误标为“每秒”，实际单位为“每分钟”——请以 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中最新定义为准。

## 使用方式

1. 在调用 `/v1/chat/completions` 或 `/v1/completions` 时，于请求体中显式传入 `mode` 和（如适用）`tpm_reservation`；  
2. Prime 模式需提前申请配额并通过工单开通，未开通时设置 `mode="prime"` 将返回 `403 Forbidden`；  
3. 推荐搭配 `temperature=0` 与 `top_p=1.0` 使用，避免采样逻辑引入不可控延迟；  
4. 初始化冷启动延迟约 8–12 秒，后续请求可稳定在 <150ms（P99，输入≤512 tokens，输出≤256 tokens）。

## 限制和注意事项

- 单次请求最大 `max_tokens` 为 1024（Prime 模式下强制限制，`default` 模式仍为 4096）；  
- 不支持 `logprobs`、`echo`、`functions` 等增强字段，启用将导致 400 错误；  
- 同一 `tpm_reservation` 值在 24 小时内不可重复提交，变更需先调用释放接口（见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)）；  
- > **注意**：文档 1 中未明确说明多租户隔离粒度，但实测表明 `tpm_reservation` 配额按 API Key 维度独占，而非 project 或 uid —— 该行为与 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 描述一致，但与早期内部设计稿存在偏差，请以运行时实际表现为准。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


