# 模型部署

模型部署是将训练完成或调优后的模型（包括平台预置模型、用户导入模型、微调生成模型等）转化为可稳定提供推理服务的在线 API 的核心过程。它涵盖资源分配、服务发布、流量接入与生命周期管理，是模型从开发走向生产的关键环节。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础服务化**：通过 `model deployment 1` 能力，开发者可按需选择专属部署、PTU 预置吞吐、独占算力（MU/DTU）或 [Token](token.md) 按量等模式，快速发布模型为标准 RESTful API，适用于验证、测试及通用生产场景。  
- **高性能低延迟场景**：启用 *High Speed Inference* 模式（需在部署时显式开启），通过 Prime 实例常驻、TPM 预留和队列调度机制，保障 P99 延迟 ≤ 300ms 和吞吐稳定性，适用于实时对话、搜索排序等严苛 SLA 场景。  
- **轻量化与边缘适配**：结合 *模型压缩* 流程，先对模型进行 INT4/INT8 量化或 KV Cache 剪枝，生成体积更小、推理更快的压缩模型包，再以标准方式部署——压缩模型 ID 可直接作为 `model_id` 传入部署接口。  
- **生产级规模化运营**：在 *[model production](../api/model-production.md)* 流程中，模型部署是“模型上线”的最终动作，需配合 TPM 预留、副本数（`replicas`）、网络类型（公网/VPC）等参数，实现高可用、可灰度、可监控的生产服务。  
- **微调模型交付闭环**：所有 *[fine tuning](../guides/fine-tuning.md)* 任务成功后，生成的专属模型 ID 自动进入「我的模型」中心，可立即用于部署——无需导出权重，不依赖本地环境，真正实现“训练即服务”。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 必填 | 示例值 |
|------|----------|------|------|--------|
| `deployment_type` | [model deployment 1](../guides/model-deployment-1.md) | 部署模式：`dedicated`（专属）、`ptu`（预置吞吐）、`mu`/`dtu`（独占算力）、`token`（按量） | 是 | `"ptu"` |
| `ptu_capacity` | [model deployment 1](../guides/model-deployment-1.md) | PTU 规格，决定最大上下文长度与并发能力（如 PTU-200 支持 32k tokens） | 仅 `ptu` 模式必填 | `200` |
| `tpm_reservation` | High Speed Inference / [model production](../api/model-production.md) | 预留 [Token](token.md)s Per Minute 总量，保障吞吐 SLA | 否（但推荐设为 ≥1000） | `5000` |
| `prime_enabled` | High Speed Inference | 是否启用实例常驻（消除冷启动），默认 `false` | 否 | `true` |
| `replicas` | [model production](../api/model-production.md) | 初始服务副本数，默认 1；影响容灾与并发承载 | 否 | `3` |
| `endpoint_type` | model production | 网络暴露类型：`public`（公网）或 `private`（VPC 内网） | 否 | `"private"` |
| `quantization_type` | 模型压缩（前置步骤） | 压缩精度选项，影响部署后延迟与显存占用 | 是（压缩时） | `"int4"` |

> ⚠️ 注意：  
> - `instance_count` 已被弃用，请勿在新部署中使用；`model_id` 必须为百炼平台内发布的合法 ID（如 `qwen2-7b-20240801`），不支持 Hugging Face 格式路径；  
> - High Speed Inference 与流式响应（`stream=true`）互斥；[Token](token.md) 按量部署亦不支持流式；  
> - 所有部署均受项目级配额约束，超限返回 `429`；TPM 预留变更需重建部署。

## 面向开发者，简洁实用

- ✅ **一步部署**：确认模型已发布 → 调用 `POST /v1/deployments` → 轮询状态 → 状态为 `active` 后即可调用 `endpoint`；  
- ✅ **即用即扩**：部署后可通过更新 `replicas` 或 `tpm_reservation`（需重建）弹性伸缩，无需修改业务代码；  
- ✅ **灰度无忧**：配合 [模型路由](https://help.aliyun.com/zh/model-studio/model-routing) 可对多版本部署做流量切分，支持 A/B 测试与平滑升级；  
- ✅ **计费透明**：不同部署模式对应独立计费项（PTU 小时费、DTU 租赁费、Token 按量费、High Speed TPM 费），控制台实时展示用量；  
- ✅ **错误速查**：常见失败原因包括 `InvalidModelId`（模型未发布）、`QuotaExceeded`（配额不足）、`UnsupportedModel`（如多模态模型不支持 High Speed Inference）——请优先检查模型状态与文档兼容性声明。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model compression](../guides/model-compression.md)
- [model production](../api/model-production.md)
- [fine tuning](../guides/fine-tuning.md)


