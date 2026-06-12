# 模型部署

模型部署是阿里云百炼平台将预置模型、微调模型或导入模型发布为在线推理服务的核心环节，是连接"模型资产"与"生产推理"的桥梁。部署完成后，应用即可通过推理接口调用该模型，满足高并发、低延迟等不同业务性能需求。

## 部署的典型场景

在百炼平台的不同工作流中，模型部署扮演着关键角色：

- **预置模型上线**：将平台提供的千问、DeepSeek、GLM 等系列模型部署为资源专享的推理服务，获得稳定的吞吐和延迟保障。
- **微调模型上线**：通过模型调优（Fine-tuning）训练得到的定制模型，需要经过部署才能被推理接口寻址和调用。这是 SFT/DPO/CPT 训练流程的最后一步。
- **压缩模型上线**：模型压缩产出的低精度模型可直接用于部署，以更小的部署单元规格获得更低的推理成本。
- **导入模型上线**：从 OSS 导入的本地训练 LoRA 模型，导入后即可创建部署。
- **监控与运维**：部署上线后，可通过模型监控查看调用量、Token 消耗、性能指标（首 Token 延时、RPM、TPM）和失败率，并配置告警规则。

## 计费模式

部署服务提供三种计费方式，创建后不可更改，如需切换必须先下线再重新部署：

| 计费模式 | 适用场景 | 计费方式 | 特点 |
|---------|---------|---------|------|
| **预置吞吐（PTU）** | 流量稳定的高负载生产环境 | 预付费按天 / 后付费按小时 | 预留资源保障 TPM 吞吐，超出部分自动切换按量付费 |
| **模型单元（MU）** | 需要自定义性能指标的场景 | 预付费按月 / 后付费按小时 | 资源独占，支持 PD 分离模式降低首 Token 延迟 |
| **按 Token 用量** | 调优后模型效果验证 | 按实际 Token 消耗 | 仅支持部分 LoRA 微调模型，一个月内不使用将自动释放 |

## 关键参数与配置

### 创建部署的核心字段

| 参数 | 说明 |
|------|------|
| `name` | 部署服务名称 |
| `model_name` | 目标模型标识（如 `qwen-flash-2025-07-28`） |
| `plan` | 计费模式：`ptu`、`mu` 或 `lora` |
| `ptu_capacity` | PTU 模式下的吞吐配置，包含 `input_tpm` 和 `output_tpm` |
| `deploy_spec` | MU 模式下的部署规格（如 `MU1`、`MU5`、`MU8`） |
| `capacity` | MU/LoRA 模式下的部署单元数量 |
| `enable_thinking` | 是否启用深度思考（MU 模式） |
| `max_context_length` | 最大上下文长度（MU 模式） |
| `rpm_limit` / `tpm_limit` | 速率限制（MU 模式） |

### PTU 溢出机制

当实际调用量超出购买的 TPM 额度时，PTU 部署会自动切换为按量付费模式，API 响应 Header 中会包含 `x-dashscope-ptu-overflow:true` 标识。

## 操作方式

### 控制台部署

在百炼控制台的"模型部署"页面创建部署任务，填写服务名称、选择模型和计费方式，等待状态变为"运行中"即可开始调用。

### API 部署

通过 Deployments API（`https://dashscope.aliyuncs.com/api/v1/deployments`）完成部署的完整生命周期管理，包括创建、查询状态、推理调用和删除/下线。

请求示例（PTU 模式）：

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_flash",
    "model_name": "qwen-flash-2025-07-28",
    "plan": "ptu",
    "ptu_capacity": {
        "input_tpm": 10000,
        "output_tpm": 1000
    }
}'
```

## 支持的模型

部署支持多种模型系列，不同系列适用的计费模式有所差异：

- **千问系列**（qwen3.7-max、qwen3.6-flash/plus 等）：PTU / MU
- **DeepSeek 系列**（deepseek-v4-pro、deepseek-v3.2 等）：PTU / MU
- **千问 VL / Omni**：PTU / MU（Omni 仅 MU）
- **GLM 系列**：PTU / MU
- **LoRA 调优模型**（千问3/2.5 系列 3B~72B）：仅按 Token 用量

## 限制与注意事项

- 部署服务目前仅适用于**华北二（北京）地域**。
- 部署成功后即开始计费，无论是否有调用请求。
- 计费方式创建后不可更改，切换需先下线再重新部署。
- MU 模式预付费首月内提前退订，日单价按 1.2 倍计费。
- 按 Token 用量模式的部署一个月内无调用将自动释放。
- 压缩产出模型的可用部署规格由所选量化模板决定。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [deployments api](../api/deployments-api.md)
- [model compression](../guides/model-compression.md)
- [fine tuning](../guides/fine-tuning.md)
- [fine tuning jobs api](../api/fine-tuning-jobs-api.md)
- [model monitoring](../guides/model-monitoring.md)


