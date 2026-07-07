# model deployment 1

百炼平台的模型部署功能为预置模型和调优后模型提供独立的、资源专享的推理服务，支持预置吞吐（PTU）、模型单元和按 Token 用量三种计费方式。开发者可通过控制台或 API 完成部署，并可将本地训练的 LoRA 模型从 OSS 导入平台后进行部署。

## 计费方式概览

百炼提供三种计费方式，创建后不可更改，如需切换须先下线再重新部署。详见[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

| 计费方式 | 适用场景 | 性能特点 | 扩缩容 |
|---------|---------|---------|--------|
| **预置吞吐（PTU）** | 高负载生产环境，流量可预估 | 平台预置吞吐/并发，TPS 通常提升 1.5~2.0 倍 | 自助增减吞吐量 |
| **模型单元** | 调优后大规模推理，需自定义性能指标 | 延迟/吞吐可自定义，支持 PD 分离模式 | 自助增减单元数量 |
| **按 Token 用量** | 调优后效果验证，对并发和延迟要求不高 | 不使用不计费，价格优势最高 | 控制台提交申请，人工审核 |

### 预置吞吐（PTU）

费用公式：`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`

- 支持后付费（按小时）和预付费（按天）两种结算方式。
- 预付费订单支付后实时生效，无法提前终止；22:00 后下单到期日自动顺延 1 天。
- 超出购买的 TPM 量或输入超过模型上限时，自动切换为按量付费模式（响应头包含 `x-dashscope-ptu-overflow:true`）。
- 支持的模型包括千问3.7-Max、千问3.7-Plus、千问-Flash、DeepSeek-v4 系列、GLM-5.2 等。

### 模型单元

费用公式：`费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价`

- 支持后付费（按小时）和预付费（包月）。首月内提前退订，日单价按 1.2 倍计费。
- 模型单元规格从 MU1 到 MU9 不等，不同规格对应不同算力和性能。
- 部分模型支持 PD 分离模式（Prefill/Decode 分离），可降低首 Token 延迟、提高吞吐。
- 支持配置推理模式（Instruct 非思考 / Thinking 思考模式）、最长上下文、服务限流（RPM/TPM）。
- 后付费方式的算力资源先买到先得，购买不成功全额退款。

### 按 Token 用量

费用公式：`费用 = 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价`

- 仅支持部分基础模型完成 SFT 高效训练（LoRA）后的自定义模型。
- 一个月内不使用将自动释放。

## PTU 长输入与前缀缓存

PTU 部署支持长输入请求和前缀缓存，适用于长文档分析和多轮对话场景。详见[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

### 长输入阶梯系数

部分模型（如 glm-5.1）在输入超过 32K token 后，按更高的阶梯系数折算 TPM 消耗：

| 模型 | 输入上限 | 缓存折扣 | 阶梯系数 |
|------|---------|---------|---------|
| glm-5.1 | 200K | 0.2（命中部分按 20% 折算） | [0,32K): 1.0; [32K,200K]: 输入 1.33 / 输出 1.17 |
| deepseek-v4-pro | 256K | 0.08（命中部分按 8% 折算） | 无阶梯（1.0） |
| qwen3.7-plus-2026-05-26 | 256K | 0.2（命中部分按 20% 折算） | 无阶梯（1.0） |

### 前缀缓存

命中缓存的输入 token 按折扣系数消耗额度，可显著降低多轮对话场景的成本。通过 API 响应中的 `cached_tokens` 字段（值大于 0）确认缓存是否生效。

超出 PTU 额度或超过模型输入上限（千问 128K / DeepSeek 64K）时，请求自动转为按量计费，无需修改调用代码。

### 容量计算器

建议在创建或扩容前，使用控制台的容量计算器估算长输入场景的额度需求。输入参数包括每分钟请求数（RPM）、平均输入/输出长度和预估缓存命中率。

## 模型导入

百炼支持将本地训练的 LoRA 模型从 OSS 导入平台，导入后可进行部署、增量训练等操作。详见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

### 支持的基础模型

当前仅支持导入 LoRA 微调版本，不支持全参微调模型。支持的基础模型系列包括：千问3（32B/14B/8B/4B）、千问3-VL-8B、千问2.5（72B/32B/14B/7B）、千问2.5-VL（72B/7B）。

### 导入要求

- **必需文件**：`adapter_model.safetensors`（权重）和 `adapter_config.json`（配置）。
- **rank 值**：必须为 8、16、32 或 64 之一，且所有 LoRA 层使用相同 rank。
- 不支持修改词汇表或 chat_template 的模型。
- VL 模型必须冻结 VIT 部分（adapter 文件中不能包含 `visual` 相关权重）。

### OSS 授权

首次导入需完成 OSS 授权，并为目标 Bucket 添加 `bailian-datahub-access` 标签（值为 `read`）。子账号需额外授予 `ram:CreateServiceLinkedRole` 权限。

## 通过 API 部署模型

百炼支持通过 HTTP API 完成模型部署的全生命周期管理。详见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

> **注意**：API 部署目前仅适用于华北2（北京）地域。

### 创建部署

API 端点：`POST https://dashscope.aliyuncs.com/api/v1/deployments`

三种计费方式的关键参数差异：

| 参数 | PTU（`plan: "ptu"`） | 模型单元（`plan: "mu"`） | Token 用量（`plan: "lora"`） |
|------|---------------------|------------------------|---------------------------|
| `ptu_capacity` | 必填：`input_tpm` + `output_tpm` | - | - |
| `deploy_spec` | - | 必填：如 `"MU1"` | - |
| `capacity` | - | 副本数 | 必填但无实际效果 |
| `enable_thinking` | - | 可选：启用思考模式 | - |
| `max_context_length` | - | 可选：最长上下文 | - |
| `rpm_limit` / `tpm_limit` | - | 可选：服务限流 | - |

### 查询与删除

- 查询状态：`GET /api/v1/deployments/{deployed_model}`，`status` 为 `RUNNING` 表示部署完成。
- 删除服务：`DELETE /api/v1/deployments/{deployed_model}`，执行后立即开始下线且不可恢复。

### 推理调用

部署完成后，使用 [DashScope SDK](../concepts/dashscope-sdk.md) 或兼容的 OpenAI API 格式发起推理请求。确保 API Key 所在的[业务空间](../concepts/workspace.md)与模型部署所在的[业务空间](../concepts/workspace.md)一致。

## API 响应中的额度字段

PTU 部署的 API 响应包含以下关键字段：

| 字段 | 说明 |
|------|------|
| `service_tier` | `ptu-standard` 表示使用 PTU 额度；`default` 或不返回表示按量计费 |
| `provisioned_tokens` | 折算后实际消耗的 PTU 额度（含阶梯系数和缓存折扣） |
| `cached_tokens` | 前缀缓存命中的 token 数 |

上述字段在不同 API 格式（OpenAI Chat、OpenAI Responses、Anthropic、DashScope）下的 JSON 路径有所不同，具体位于 `usage.prompt_tokens_details` 和 `usage.completion_tokens_details`（或 `output_tokens_details`）下。

> **注意**：Anthropic 兼容格式暂不返回 `cached_tokens` 字段，可通过 `provisioned_tokens` 间接判断缓存效果。

## 常见问题

- **部署后报权限不足**：检查 API Key 归属[业务空间](../concepts/workspace.md)是否拥有目标模型的部署权限，并确认归属账号在该业务空间中有操作权限。
- **导入模型与本地推理效果不一致**：百炼推理引擎参数默认值可能不同，建议显式设置 `temperature=1.0`、`top_p=1.0`、`repetition_penalty=1.0` 以对齐 vLLM 默认行为。
- **PTU 利用率超过 100%**：长输入阶梯系数使折算消耗高于原始 token 数，超出部分自动转按量计费，不影响可用性。
- **OSS 导入报错 10041495**：主账号需先开通 OSS 服务。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


