# model deployment 1

百炼平台提供模型部署功能，支持将预置模型或调优后的模型部署为独立的、资源专享的推理服务，满足高并发、低延迟等不同业务需求。平台提供三种计费方式（预置吞吐 PTU、模型单元、[Token](../concepts/token.md) 用量），并支持通过控制台或 API 完成部署操作，同时允许从 OSS 导入自训练的 LoRA 模型进行部署。

## 计费方式概述

百炼模型部署提供三种计费方式，创建后无法更改，如需切换需先下线再重新部署。详细计费规则参见[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

### 预置吞吐（PTU）

通过平台预留资源保障特定 TPM 吞吐能力，在保障额度内不限速。适用于流量稳定、需保障并发体验的高负载生产环境。

- 计费公式：`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`
- 支持后付费（按小时）和预付费（按天）两种模式
- 超出购买的 TPM 量或输入超过模型上限时，自动切换为按量付费模式（响应头包含 `x-dashscope-ptu-overflow:true`）
- TPS 相比按 [Token](../concepts/token.md) 计费通常提升约 1.5~2.0 倍
- 预付费订单无法提前终止

### 模型单元（MU）

按使用时长与模型单元数量配置算力，资源独占，性能指标可自定义。

- 计费公式：`费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价`
- 支持后付费（按小时）和预付费（包月），首月内提前退订日单价按 1.2 倍计费
- 支持 PD 分离计算模式（将 Prefill 和 Decode 拆到不同节点，降低首 [Token](../concepts/token.md) 延迟、提高吞吐）
- 后付费方式的算力资源先买到先得，购买不成功全额退款

### Token 用量

按调用产生的输入/输出 Token 计费，仅支持部分经过 LoRA 调优后的模型。

- 计费公式：`费用 = 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价`
- 不使用不计费，一个月内不使用将自动释放

## PTU 长输入与缓存

PTU 部署支持长输入请求和前缀缓存功能，详见[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

### 长输入阶梯系数

部分模型输入超过 32K token 时，按更高阶梯系数折算 TPM 消耗：

| 模型 | 输入上限 | 缓存折扣 | 阶梯系数 |
|------|---------|---------|---------|
| glm-5.1 | 200K | 0.2（命中部分按 20% 折算） | [0,32K): 1.0; [32K,200K]: 输入 1.33 / 输出 1.17 |
| deepseek-v4-pro | 256K | 0.08（命中部分按 8% 折算） | 无阶梯（1.0） |
| qwen3.7-plus-2026-05-26 | 256K | 0.2（命中部分按 20% 折算） | 无阶梯（1.0） |

### 前缀缓存

命中缓存的输入 token 按折扣系数消耗额度，可降低多轮对话和重复前缀场景的成本。通过 API 响应中的 `cached_tokens` 字段确认缓存是否生效（值大于 0 表示命中）。

### 溢出机制

超出 PTU 额度或输入超过模型上限（千问 128K / DeepSeek 64K）时，请求自动转为按量计费，业务不中断。API 响应中 `service_tier` 为 `default` 或不返回表示已转按量计费。

## 支持的模型

### PTU 支持的主要模型

| 模型 | 代码 | 最长输入 |
|------|-----|---------|
| 千问3.7-Max | qwen3.7-max-2026-05-20 | 256K |
| 千问3.7-Plus | qwen3.7-plus-2026-05-26 | 256K |
| DeepSeek-v4-Pro | deepseek-v4-pro | 256K |
| DeepSeek-v4-Flash | deepseek-v4-flash | 256K |
| GLM-5.2 | glm-5.2 | 1M |

### 模型单元支持的模型类别

模型单元支持更广泛的模型，包括文本生成（千问、DeepSeek、GLM 等）、[多模态](../concepts/multimodal.md)（千问 VL、千问 Omni）、语音合成（CosyVoice）等。部署时可选择 Instruct（非思考模式）或 Thinking（思考模式）推理模式。

### Token 用量支持的基础模型

仅支持部分千问系列和千问 VL 系列基础模型经 SFT 高效训练后的自定义模型，包括 qwen3-32b、qwen3-8b、qwen2.5-72b-instruct 等。

## 模型导入

百炼支持将本地训练的 LoRA 模型从 OSS 导入平台进行部署，详细流程参见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

### 导入要求

- 仅支持 LoRA 模型，不支持全参微调模型
- 必需文件：`adapter_model.safetensors`（权重）和 `adapter_config.json`（配置）
- rank 值必须为 8、16、32 或 64 之一
- 不支持修改了词汇表或 chat_template 的模型
- VL 模型必须冻结 VIT 部分（adapter 中不能包含 `visual` 相关参数）

### 支持导入的基础模型

千问3（32B/14B/8B/4B）、千问3-VL-8B、千问2.5（72B/32B/14B/7B）、千问2.5-VL（72B/7B）。

### OSS 授权

首次导入需完成 OSS 服务关联角色授权，并为目标 Bucket 添加 `bailian-datahub-access` 标签（值为 `read`）。子账号需额外获取 `ram:CreateServiceLinkedRole` 权限。

## 部署方式

### 控制台部署

前往[模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，填写服务名称、选择模型和计费方式，确认后等待状态变为"运行中"即部署成功。

### API 部署

通过 DashScope API 进行部署，适用于自动化场景，详细示例参见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

**PTU 部署示例：**

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

**模型单元部署示例：**

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
    "capacity": 4
}'
```

关键 `plan` 参数值：`ptu`（预置吞吐）、`mu`（模型单元）、`lora`（Token 用量）。

部署成功后通过 `GET /api/v1/deployments/{deployed_model}` 查询状态，`status` 为 `RUNNING` 表示可用。不再使用时通过 `DELETE` 请求删除，删除后立即停止计费且不可恢复。

## API 响应中的关键字段

PTU 部署的 API 响应包含额度相关字段，在不同 API 格式（OpenAI Chat、OpenAI Responses、Anthropic、DashScope）下 JSON 路径略有不同：

| 字段 | 说明 |
|------|------|
| `service_tier` | `ptu-standard` 表示使用 PTU 额度；`default` 或不返回表示按量计费 |
| `provisioned_tokens` | 折算后实际消耗的 PTU 额度 token 数（含阶梯系数和缓存折扣） |
| `cached_tokens` | 前缀缓存命中的 token 数 |

> **注意**：Anthropic 兼容格式暂不返回 `cached_tokens` 字段，仅可通过 `provisioned_tokens` 间接判断缓存效果。

## 限制与注意事项

- 计费方式在创建后无法更改，需下线重新部署才能切换
- 部署成功后即开始计费，即使尚未调用模型
- PTU 预付费订单无法提前终止；后付费欠费后资源保留 24 小时，超时底层资源被删除
- Token 用量计费方式一个月内不使用将自动释放
- 导入的 LoRA 模型若与本地 vLLM/SGLang 推理效果不一致，需调整 `temperature`、`top_p`、`top_k` 等参数对齐
- API 部署需确保 [API Key](../concepts/api-key.md) 所在[业务空间](../concepts/workspace.md)拥有模型部署权限，否则会报 `Workspace xxx does not have deployment privilege`
- 本文档仅适用于华北2（北京）地域

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


