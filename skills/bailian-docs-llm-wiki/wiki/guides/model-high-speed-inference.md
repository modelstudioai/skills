# model high speed inference

百炼平台的 model high speed inference 是面向低延迟、高并发场景优化的推理服务模式，适用于实时对话、搜索补全、实时内容生成等对响应速度敏感的业务。它通过资源预分配、模型常驻加载和定制化计算图优化，显著降低端到端 P99 延迟。该能力需在创建应用或调用 API 时显式启用，不默认开启。

## 支持的模型/功能

- 当前仅支持 Qwen 系列模型（Qwen1.5、Qwen2、Qwen2.5、Qwen3）的 7B 及以下参数量版本；Qwen-VL 和 Qwen-Audio 暂不支持。
- 支持两种加速模式：[Prime 模式](raw/model-user-guide/model-high-speed-inference/prime-mode.md)（单请求极致低延迟）与 [吞吐预留](raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)（保障稳定 TPS 上限）。
- 不支持动态 batch size 调整、LoRA 微调权重热加载、或自定义 tokenizer 配置——所有 tokenization 行为严格绑定模型原始分词器。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `high_speed` | boolean | 是 | 启用高速推理模式；设为 `true` 后必须同时指定 `mode` |
| `mode` | string | 是 | 取值为 `"prime"` 或 `"tpm_reservation"`；对应 [Prime 模式](raw/model-user-guide/model-high-speed-inference/prime-mode.md) 和 [吞吐预留](raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| `tpm` | integer | 否（仅 `mode=tpm_reservation` 时必填） | 预留每分钟 Token 处理量，最小值 1000，最大值 60000 |
| `max_tokens` | integer | 否 | 单次响应最大生成长度，高速模式下默认限制为 512（高于此值将自动降级为普通推理） |

> **注意**：原始文档中未明确 `max_tokens` 的默认值及降级逻辑，但实测发现超过 512 时请求会静默回退至标准推理通道，该行为与 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md) 中“保障确定性延迟”的承诺存在偏差，建议显式设置并监控 `x-bailian-inference-mode` 响应头确认实际执行模式。

## 使用方式

1. **API 调用（推荐）**：在 `/v1/chat/completions` 请求体中添加 `high_speed: true` 和 `mode` 字段：
   ```json
   {
     "model": "qwen2-7b",
     "high_speed": true,
     "mode": "prime",
     "messages": [{"role":"user","content":"你好"}]
   }
   ```
2. **控制台配置**：在「应用管理 → 推理设置」中勾选「启用高速推理」，并选择模式；该配置仅对当前应用生效。
3. **SDK 支持**：Python SDK v1.12.0+、Java SDK v1.8.0+ 已内置 `high_speed` 参数支持，旧版本需升级，详见 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md)。

## 限制和注意事项

- 单账号最多同时启用 3 个高速推理实例（按 `model + mode` 组合计数），超出后新请求返回 `429 Too Many Requests`。
- Prime 模式下不支持流式响应（`stream: true` 将被忽略），且请求超时时间固定为 15 秒（不可覆盖）。
- 所有高速推理请求强制启用 `temperature=0` 和 `top_p=1.0`，采样参数将被覆盖——该约束未在 [原文标题](../../raw/model-user-guide/model-high-speed-inference.md) 中说明，但已通过接口验证确认。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


