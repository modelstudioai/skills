# model high speed inference

百炼平台的 model high speed inference 是面向低延迟、高并发场景优化的推理服务模式，适用于实时对话、搜索补全、流式响应等对端到端时延敏感的业务。它通过预热实例、资源隔离与请求调度优化，在保障 SLO 的前提下显著降低 P99 延迟。该能力需在创建模型服务时显式启用，并依赖底层 Prime 模式与吞吐预留机制协同工作 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)。

## 支持的模型/功能

- 当前仅支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）及部分 Llama3 定制版本（需白名单开通）；
- 必须部署为 `vLLM` 或 `Triton` 后端，不支持 `Transformers` 默认 CPU 推理路径；
- 支持的功能包括：[流式输出](../concepts/streaming-output.md)（`stream=true`）、动态 batch（自动合并同模型小请求）、优先级队列（基于 `priority` header）；
- Prime 模式是核心支撑机制，提供实例常驻与冷启规避能力 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `high_speed_inference` | boolean | 是 | 启用高速推理模式（默认 `false`） |
| `tpm_reservation` | integer | 否 | 预留吞吐量（TPM），单位 tokens/min，范围 100–10000；未设置时按模型默认值分配 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| `max_batch_size` | integer | 否 | 动态批处理最大尺寸，建议设为 8–32；超过将触发强制 flush |
| `timeout_ms` | integer | 否 | 单请求最大等待+执行时间，默认 15000ms；低于 3000ms 可能导致超时率上升 |

> **注意**：文档中提及 `tpm_reservation` 支持浮点数输入，但实际 API 校验仅接受整数 —— 请以 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的接口定义为准，浮点值将被向下取整并告警。

## 使用方式

1. 创建服务时在 `spec.modelConfig` 中添加配置：
   ```yaml
   high_speed_inference: true
   tpm_reservation: 2000
   ```
2. 调用时需在 HTTP Header 中声明：
   ```http
   X-Bailian-High-Speed: true
   ```
   （缺失该 header 将降级至普通推理路径）
3. 流式请求示例（curl）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $API_KEY" \
     -H "X-Bailian-High-Speed: true" \
     -d '{"model": "qwen2-7b-instruct", "input": {"messages": [...]}, "parameters": {"stream": true}}'
   ```

## 限制和注意事项

- 不支持多模态模型（如 Qwen-VL、Qwen2-Audio）；
- 启用后无法动态关闭，需重建服务；
- 同一模型在同一 region 下最多启用 3 个高速推理服务实例；
- 若请求中 `max_tokens` > `tpm_reservation / 60 * 2`，可能因令牌速率限制被限流；
- Prime 模式实例在空闲 5 分钟后进入轻量休眠（非完全释放），首次唤醒延迟约 800–1200ms —— 此行为由 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 定义，不可配置。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


