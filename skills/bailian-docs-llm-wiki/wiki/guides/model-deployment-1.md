# model deployment 1

百炼平台的模型部署功能允许用户将预置模型或调优后的模型部署为独立的、资源专享的推理服务，以满足高并发、低延迟等业务需求。部署支持三种计费方式（预置吞吐 PTU、模型单元、Token 用量），并可通过控制台或 API 完成操作。此外，用户还可以从 OSS 导入本地训练的 LoRA 模型到平台进行部署。

> **注意**：模型部署功能目前仅适用于"中国内地（北京）"地域。

## 计费方式

百炼模型部署提供三种计费方式，适用于不同业务场景。详细的计费规则和模型价格请参考[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

### 预置吞吐（PTU）

- **定义**：通过平台预留资源，保障特定 TPM 吞吐能力，在保障额度内不限速。
- **优势**：TPS 通常比按 Token 计费提升约 1.5～2.0 倍；支持自动续费。
- **计费公式**：`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`
- **适用场景**：流量稳定的智能客服、实时内容审核、公有云翻译 API 等。
- **支持模型**：部分预置模型（千问系列、DeepSeek、GLM 等）。
- **溢出机制**：超出购买的 TPM 量时，自动切换为按量付费模式，API 返回 Header 包含 `x-dashscope-ptu-overflow:true`。

### 模型单元（MU）

- **定义**：按模型单元数量配置算力，资源独占。
- **优势**：性能指标可自定义（延迟、吞吐）；支持 PD 分离计算模式；支持自动续费。
- **计费公式**：`费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价`
- **适用场景**：调优模型的大规模推理、需独占资源的长时任务。
- **PD 分离模式**：将首 Token 计算（Prefill）和后续 Token 计算（Decode）拆到不同节点执行，可降低首 Token 延迟、提高吞吐。
- **可配置项**：推理模式（Instruct/Thinking）、最长上下文、RPM/TPM 限流。

### Token 用量

- **定义**：按实际输入/输出 Token 数量计费。
- **计费公式**：`费用 = 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价`
- **适用场景**：调优后模型的效果验证，对并发和延迟要求不高的场景。
- **限制**：仅支持部分经过 LoRA 调优后的模型；一个月内不使用将自动释放。

> **注意**：计费方式在服务创建后无法更改。如需切换，必须先下线已部署的模型再重新部署。

## 部署方式

### 控制台部署

1. 前往[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)。
2. 选择模型和计费方式，设置模型名称并开始部署。
3. 部署状态为"运行中"时即部署成功。

### API 部署

通过 HTTP API 可编程化地管理模型部署的全生命周期，包括创建、查询、调用和删除。完整的 API 操作流程请参考[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

**创建部署**（以 PTU 方式为例）：

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

**关键参数**：

| 参数 | 说明 |
| --- | --- |
| `plan` | 计费方式：`ptu`（预置吞吐）、`mu`（模型单元）、`lora`（Token 用量） |
| `model_name` | 模型代码或自定义模型 ID |
| `deploy_spec` | 模型单元规格（仅 `mu` 模式），如 `MU1` |
| `capacity` | 模型单元数量（`mu` 模式）或副本数（`lora` 模式，设置无效但必填） |
| `enable_thinking` | 是否启用思考模式（仅部分模型支持） |
| `max_context_length` | 最长上下文长度（仅 `mu` 模式部分模型支持） |

**查询状态**：`GET /api/v1/deployments/{deployed_model}`，状态为 `RUNNING` 时部署完成。

**调用已部署模型**：使用部署后的模型 `code` 作为 `model` 参数，通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)、DashScope SDK 或 Assistant SDK 调用。

**删除服务**：`DELETE /api/v1/deployments/{deployed_model}`，执行后立即下线且不可恢复。

## 模型导入

百炼支持从 OSS 导入本地训练的 LoRA 模型。详细操作请参考[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

### 支持的基础模型

- 千问3 系列：千问3-32B、千问3-14B、千问3-8B、千问3-4B-Instruct-2507
- 千问3-VL 系列：千问3-VL-8B-Instruct
- 千问2.5 系列：千问2.5-72B/32B/14B/7B-Instruct
- 千问2.5-VL 系列：千问2.5-VL-72B/7B-Instruct

### 导入要求

- **仅支持 LoRA 模型**，不支持全参微调模型。
- 必需文件：`adapter_model.safetensors`（权重）和 `adapter_config.json`（配置）。
- rank 值必须为 8、16、32 或 64 之一，所有 LoRA 层须使用相同 rank 值。
- 不支持修改了词汇表（vocab）或对话模板（chat_template）的模型。
- VL 模型必须冻结 VIT 部分（adapter 中不能包含 `visual` 相关权重参数）。
- OSS Bucket 需添加 `bailian-datahub-access` 标签，且模型文件不能放在根目录。

## 权限与常见问题

- **权限不足**：确认 API Key 所在[业务空间](../concepts/workspace.md)有模型部署权限，且 API Key 归属账号在该空间中有操作权限。
- **推理效果不一致**：从 OSS 导入的模型在百炼平台推理时，`temperature`、`top_p`、`top_k`、`repetition_penalty` 等参数默认值可能与 vLLM/SGLang 不同，需手动对齐。
- **计费生效时间**：部署命令执行后立即开始计费，即便尚未调用模型。
- **预付费退订**：模型单元包月模式下，首月内提前退订，日单价按 1.2 倍计费。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


