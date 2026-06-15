# 模型部署

模型部署是百炼平台将预置模型、微调模型或导入模型发布为在线推理服务的过程。通过部署，开发者可获得资源专享、可独立寻址的推理 endpoint，满足生产环境对高并发、低延迟等性能指标的要求。

## 在百炼平台中的定位

模型部署是连接"模型资产"与"在线推理"的桥梁。在典型的模型生命周期中，开发者先通过模型调优（SFT/CPT/DPO）产出微调模型，再经由模型压缩降低资源占用，最后通过模型部署将其上线为可调用的推理服务。部署完成后，应用即可通过 DashScope API 或兼容 OpenAI 的接口发起推理请求。

## 计费方式

百炼模型部署提供三种计费方式，服务创建后不可更改：

| 计费方式 | 资源模式 | 性能可调 | 适用场景 |
|---------|---------|---------|---------|
| 预置吞吐（PTU） | 平台预留资源，保障 TPM | 不可调 | 流量稳定的智能客服、实时内容审核 |
| 模型单元（MU） | 按时长和单元数独占算力 | 可自定义延迟/吞吐，支持 PD 分离 | 独占资源场景，如专属微调模型、自动驾驶仿真 |
| 按 Token 用量 | 按输入/输出 Token 计量 | 不可调 | 低频调用，仅支持部分 LoRA 调优模型 |

关键注意事项：

- PTU 模式下，超出购买的 TPM 量时调用自动降级为按量付费，API 返回 Header 包含 `x-dashscope-ptu-overflow:true`。
- MU 模式的算力资源先买到先得，购买不成功会全额退款。
- 按 Token 用量模式下，一个月内不使用将自动释放。

## 部署方法

### 控制台部署

在百炼控制台的模型部署页面填写服务名称、选择模型和计费方式即可创建部署服务。当前仅支持华北二（北京）地域。

### API 部署

通过 Deployments API 实现自动化部署，核心流程：

1. **创建部署服务**：`POST /api/v1/deployments`，指定 `name`、`model_name` 和 `plan`（取值 `ptu` / `mu` / `lora`）
2. **查询服务状态**：`GET /api/v1/deployments/<deployed_model>`，等待 `status` 变为 `RUNNING`
3. **发起推理调用**：使用 DashScope SDK 或 [OpenAI 兼容接口](openai-compatible-api.md)调用已部署模型
4. **删除服务**：`DELETE /api/v1/deployments/<deployed_model>`（不可恢复，立即停止计费）

PTU 模式创建示例：

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

MU 模式还支持 `deploy_spec`、`enable_thinking`、`capacity`、`max_context_length`、`rpm_limit`、`tpm_limit` 等配置项。

## 关键配置参数

| 参数 | 说明 | 适用计费方式 |
|------|------|------------|
| `plan` | 计费方式：`ptu` / `mu` / `lora` | 所有 |
| `ptu_capacity.input_tpm` / `output_tpm` | 预置吞吐的输入/输出 TPM | PTU |
| `deploy_spec` | 部署规格 | MU |
| `enable_thinking` | 是否启用思考模式 | MU |
| `capacity` | 模型单元数量 | MU |
| `max_context_length` | 最大上下文长度 | MU |
| `rpm_limit` / `tpm_limit` | 请求/Token 限流 | MU |

## 与相关功能的关系

- **模型调优**：调优产出的微调模型需要通过模型部署上线后才能调用。LoRA 调优模型支持按 Token 用量方式部署。
- **模型压缩**：压缩后的量化模型可直接用于模型部署，部署规格由量化模板决定，通常比全精度模型所需的部署单元更小。
- **模型导入**：开发者可将本地训练的 LoRA 模型从 OSS 导入百炼平台后进行部署，支持千问3、千问2.5 等系列的多个规格。

## 限制与注意事项

- 当前模型部署仅适用于华北二（北京）地域。
- 计费方式在服务创建后无法更改，如需切换必须下线后重新部署。
- 删除部署操作不可恢复，服务将立即停止计费。
- MU 后付费预付费首月内提前退订，日单价将按 1.2 倍计费。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [deployments api](../api/deployments-api.md)
- [model compression](../guides/model-compression.md)
- [get started with models](../guides/get-started-with-models.md)
- [fine tuning](../guides/fine-tuning.md)


