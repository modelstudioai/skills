# 模型部署

模型部署是百炼平台将预置模型、微调模型或导入模型发布为在线推理服务的功能，使模型能够以独立的、资源专享的方式对外提供推理能力，满足不同业务场景对并发、延迟和成本的要求。

## 核心概念

模型部署是连接"模型资产"与"在线推理"的桥梁。开发者通过部署操作，将一个模型版本上线为可被推理接口寻址的 endpoint，后续应用和 Agent 即可通过标准 API 调用该模型。部署服务目前仅适用于华北二（北京）地域。

## 计费方式

百炼模型部署提供三种计费方式，创建后不可更改，如需切换必须先下线再重新部署。

### 预置吞吐（PTU）

通过平台预留资源保障特定 TPM 吞吐能力，在保障额度内不限速。适用于流量稳定、需要保障并发体验的高负载生产环境。

- 吞吐和并发由平台预置，用户不可调
- TPS 相比按 Token 用量计费通常提升约 1.5 至 2.0 倍
- 预付费按天计费，后付费按小时计费
- 超出购买的 TPM 量时自动切换为按量付费（API 返回 Header 包含 `x-dashscope-ptu-overflow:true`）

### 模型单元（MU）

按使用时长与模型单元数量计费，资源独占。适用于需要自定义延迟、吞吐等性能指标的场景。

- 支持 PD 分离计算模式（将首 Token 计算与后续 Token 计算拆到不同节点，降低首 Token 延迟、提高吞吐）
- 后付费按小时计费，预付费按月计费
- 可配置 `enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit` 等参数

### 按 Token 用量

以每次调用产生的输入/输出 Token 作为计量依据，不使用不计费。

- 仅支持部分高效微调（LoRA）后的模型
- 一个月内不使用将自动释放
- 适合调优后模型效果验证

## 支持的模型

部署支持多种模型系列：

| 系列 | 代表模型 | 可用计费模式 |
|------|---------|------------|
| 千问 | qwen3.7-max、qwen3.6-flash/plus、qwen-flash/plus 等 | PTU / MU |
| DeepSeek | deepseek-v4-pro、deepseek-v3.2、deepseek-v3 | PTU / MU |
| 千问 VL | qwen3-vl-plus、qwen3-vl-8b-instruct 等 | PTU / MU |
| 千问 Omni | qwen3.5-omni-flash、qwen3.5-omni-plus | MU |
| GLM | glm-5.1、glm-5、glm-4.7 | PTU / MU |
| 其他 | MiniMax-M2.5、Kimi-K2.5 | MU |
| LoRA 调优模型 | 千问3/2.5 系列（3B 至 72B） | 按 Token 用量 |

## 部署方式

### 控制台部署

1. 前往模型部署控制台（北京地域）
2. 填写服务名称，选择模型和计费方式
3. 等待部署状态变为"运行中"

部署成功后即开始计费，无论是否有调用请求。

### API 部署

通过 Deployments API 可完成部署、查询、推理和删除的完整生命周期管理。

**创建部署示例（PTU 模式）**：

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

**创建部署示例（MU 模式）**：

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_plus",
    "model_name": "qwen-plus-2025-12-01",
    "plan": "mu",
    "deploy_spec": "MU1",
    "enable_thinking": true,
    "capacity": 4,
    "max_context_length": 10000,
    "rpm_limit": 500,
    "tpm_limit": 1000
}'
```

## 关键参数

| 参数 | 说明 | 适用模式 |
|------|------|---------|
| `plan` | 计费模式：`ptu`、`mu` 或 `lora` | 全部 |
| `model_name` | 要部署的模型名称（含版本号） | 全部 |
| `ptu_capacity.input_tpm` / `output_tpm` | 预置吞吐的输入/输出 TPM 额度 | PTU |
| `deploy_spec` | 模型单元规格（如 MU1） | MU |
| `capacity` | 模型单元数量 | MU / LoRA |
| `enable_thinking` | 是否启用思考模式 | MU |
| `max_context_length` | 最大上下文长度 | MU |
| `rpm_limit` / `tpm_limit` | 请求数/Token 数限流 | MU |

## 与模型压缩的关系

通过模型压缩（量化）可将微调后的全精度模型转换为低精度版本，降低显存占用、缩小所需部署单元规格，从而降低部署成本并提升推理吞吐。压缩产出的模型可直接用于模型部署，其可用的部署单元规格由量化模板决定。

## 与模型调优的关系

模型调优（微调）产出的自定义模型，需要通过模型部署才能对外提供推理服务。典型流程为：调优完成 -> 获得 `finetuned_output` -> 调用 Deployments API 创建部署 -> 部署状态变为 RUNNING 后即可调用。LoRA 调优模型支持按 Token 用量的低成本部署方式，适合效果验证阶段使用。

## 注意事项

- 部署成功后即开始计费，即使没有调用请求
- 计费方式创建后不可更改，切换需先下线再重新部署
- 按 Token 用量模式仅支持 LoRA 调优模型，且一个月不使用会自动释放
- PTU 模式超出购买额度时会自动降级为按量付费
- 部署服务当前仅支持华北二（北京）地域

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [deployments api](../api/deployments-api.md)
- [model compression](../guides/model-compression.md)
- [fine tuning](../guides/fine-tuning.md)
- [release notes](../guides/release-notes.md)


