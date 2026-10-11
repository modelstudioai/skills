# model high speed inference

百炼平台的 model high speed inference（高速推理）能力面向低延迟、高并发的生产级推理场景，通过 Prime 模式与吞吐预留（TPM Reservation）两项核心技术，实现模型响应时间稳定可控、P99 延迟显著降低。该能力适用于实时对话、搜索补全、实时风控等对时延敏感的业务。所有功能均需在创建推理服务时显式启用，并受配额与模型兼容性约束。

## 支持的模型/功能

- **Prime 模式**：为指定模型实例独占分配 GPU 资源，关闭动态批处理与共享调度，确保单请求端到端延迟稳定在毫秒级（典型 P99 < 150ms）。仅支持 Qwen 系列（Qwen2、Qwen2.5、Qwen3）及部分 Llama3 定制版本（见 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)）。
- **吞吐预留（TPM Reservation）**：允许用户按每分钟 Token 吞吐量（TPM）预购资源配额，平台保障该 TPM 下的 SLO（如 P95 延迟 ≤ 300ms）。不保证单请求延迟，但保障整体吞吐稳定性。该机制与 Prime 模式互斥，不可同时启用。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `high_speed_inference` | boolean | 是 | 启用高速推理总开关；设为 `true` 后需进一步配置子模式 |
| `mode` | string | 是（当 `high_speed_inference=true`） | 取值 `"prime"` 或 `"tpm_reservation"`；对应 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 和 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| `tpm` | integer | 仅 `mode="tpm_reservation"` 时必填 | 预留的每分钟 Token 吞吐量（单位：token/min），最小值 1000 |
| `instance_type` | string | 仅 `mode="prime"` 时必填 | 指定 GPU 实例类型（如 `"gn7i-c8g1.2xlarge"`），需与模型尺寸匹配 |

> **注意**：原始文档中 `instance_type` 在 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 中被定义为可选（默认自动选择），但当前 API 实际强制要求传入；请以接口文档和 SDK 最新行为为准。

## 使用方式

1. 创建服务时，在 `create_service` 请求体中设置 `high_speed_inference: true` 并指定 `mode`；
2. 根据所选模式补充 `tpm` 或 `instance_type`；
3. 调用 `deploy_service` 完成部署（部署耗时较普通模式增加 2–5 分钟，因需独占资源调度）；
4. 推理请求无需额外 header，服务自动路由至高速通道。

示例（curl）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "qwen2-7b-instruct",
    "high_speed_inference": true,
    "mode": "prime",
    "instance_type": "gn7i-c8g1.2xlarge"
  }'
```

## 限制和注意事项

- Prime 模式下不支持动态批处理（`batch_size` 固定为 1），且无法与其他服务共享 GPU 显存；
- TPM 预留服务不支持弹性扩缩容，`tpm` 值在服务生命周期内不可修改；
- 所有高速推理服务均不支持流式响应（`stream=false` 强制生效），若需流式，请使用标准推理通道；
- 当前仅支持 `chat` 类型模型，`embedding` 和 `rerank` 模型暂未开放高速推理能力；
- 配额需提前申请：Prime 模式需单独审批 GPU 实例配额；TPM 预留需在控制台提交 TPM 预估用量并获审批。详情参见 [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)。

## 来源文档

- [模型推理](../../raw/model-user-guide/model-high-speed-inference.md)


