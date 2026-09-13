# model high speed inference

百炼平台的 model high speed inference 是面向低延迟、高并发场景优化的推理服务模式，适用于实时对话、搜索补全、流式响应等对端到端时延敏感的业务。它通过预热实例、资源独占调度和底层 Kernel 优化，在保障 SLO 的前提下显著降低 P99 延迟。该能力需配合特定模型规格与参数配置启用。

## 支持的模型/功能

- 当前仅支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 及部分已标注 `high_speed: true` 的定制模型（参见 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)）。
- 支持 Prime 模式（自动实例预热与请求路由优化）和吞吐预留（TPM 预留保障）两种加速机制，二者可叠加使用。
- 不支持[多模态](../concepts/multi-modal.md)输入、Function Calling 或长上下文（>32k tokens）场景下的高速推理；相关限制详见 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `enable_high_speed` | boolean | 是 | 启用高速推理通道；设为 `true` 后触发 Prime 调度与预留资源匹配 |
| `tpm_reservation_id` | string | 否 | 吞吐预留 ID，需提前在控制台创建；未提供时按共享池调度（[模型推理](../../raw/model-user-guide/model-high-speed-inference.md)） |
| `max_tokens` | integer | 推荐设置 | 建议 ≤ 1024，过大将导致无法命中高速路径 |

> **注意**：`temperature=0` 并非高速推理的强制要求，但实测非零温度可能触发动态采样分支，绕过部分优化路径——该行为与文档中“仅影响输出多样性”的描述存在偏差，建议生产环境统一设为 `0`。

## 使用方式

1. 确保模型已开通高速推理权限（联系商务或检查控制台「模型服务」页签）；
2. 在 API 请求 `body` 中显式传入 `"enable_high_speed": true`；
3. 若已购买吞吐预留，添加 `"tpm_reservation_id": "tr-xxx"`；
4. 调用 `/v1/chat/completions` 或 `/v1/completions` 接口（不支持 `/v1/embeddings`）。

示例请求片段：
```json
{
  "model": "qwen-plus",
  "enable_high_speed": true,
  "tpm_reservation_id": "tr-abc123",
  "messages": [{"role": "user", "content": "你好"}],
  "max_tokens": 512
}
```

## 限制和注意事项

- 单次请求 `input_tokens + max_tokens` 总和不得超过 8192，否则降级至普通推理通道；
- 高速通道不支持流式响应（`stream: true`），启用 `enable_high_speed` 时必须禁用流式；
- 实例预热需 3–5 分钟生效，首次请求可能延迟略高；若 10 分钟内无新请求，实例将自动释放；
- 吞吐预留资源不可跨地域复用，且 `tpm_reservation_id` 仅对绑定模型生效。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


