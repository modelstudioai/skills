# model deployment 1

百炼平台提供[模型部署](../concepts/model-deployment.md)功能，支持将预置模型或调优后的[模型部署](../concepts/model-deployment.md)为独立的、资源专享的推理服务，满足高并发、低延迟等不同业务需求。部署功能目前仅适用于华北二（北京）地域，提供预置吞吐（PTU）、模型单元和按 Token 用量三种计费方式，同时支持从 OSS 导入本地训练的 LoRA 模型进行部署。

## 计费方式概览

百炼[模型部署](../concepts/model-deployment.md)提供三种计费模式，适用于不同业务场景（详见 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)）：

| 计费方式 | 适用场景 | 性能特点 | 支持模型 |
|---------|---------|---------|---------|
| 预置吞吐（PTU） | 流量稳定的生产环境，需保障并发体验 | 平台预置吞吐，TPS 提升约 1.5~2.0 倍 | 部分预置模型 |
| 模型单元 | 大规模推理业务，需自定义性能指标 | 延迟/吞吐可自定义，支持 PD 分离 | 部分预置模型及所有调优后模型 |
| Token 用量 | 调优后模型效果验证，对并发要求不高 | 价格最优，不使用不计费 | 部分 LoRA 调优后模型 |

> **注意**：计费方式在服务创建后无法更改，如需切换必须下线已部署的模型后重新部署。

### 预置吞吐（PTU）计费

费用公式：`费用 = 使用时长 x (输入 TPM 单价 x 输入 TPM + 输出 TPM 单价 x 输出 TPM)`

- 支持后付费（按小时）和预付费（按天）两种模式
- 预付费订单支付后实时生效，到期后延后 2 小时停止服务
- 超出购买的 TPM 量时，调用自动切换为按量付费模式（API 返回 Header 含 `x-dashscope-ptu-overflow:true`）
- 支持自助增减吞吐量进行扩缩容

### 模型单元计费

费用公式：`费用 = 使用时长（小时）x 模型单元数量 x 模型单元单价`

- 支持后付费（按小时）和预付费（包月）
- 首月内提前退订，日单价按 1.2 倍计费
- 后付费算力资源先买到先得，购买不成功全额退款
- 支持 PD 分离计算模式（Prefill 和 Decode 拆到不同节点执行），可降低首 Token 延迟、提高吞吐

### Token 用量计费

费用公式：`费用 = 输入 Token 数 x 输入单价 + 输出 Token 数 x 输出单价`

- 仅支持完成 SFT 高效训练后的自定义模型
- 一个月内不使用将自动释放

## 支持的模型

### 预置吞吐支持的主要模型

- **千问系列**：qwen3.7-max、qwen3.6-flash/plus、qwen3.5-plus、qwen3-max、qwen-flash、qwen-plus 等
- **DeepSeek 系列**：deepseek-v4-pro、deepseek-v3.2、deepseek-v3
- **千问 VL**：qwen3-vl-plus
- **其他**：GLM-5.1

### 模型单元支持的主要模型

涵盖文本生成、多模态、语音合成等类型，包括千问全系列（1.7B 到 397B）、DeepSeek、GLM、MiniMax、Kimi 等模型。模型单元规格从 MU1 到 MU9 不等，部分模型支持 PD 分离模式部署。

## 控制台部署方法

1. 前往[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)
2. 填写服务名称，选择模型和计费方式
3. 等待部署状态变为"运行中"即部署成功

模型单元计费模式下可额外配置：推理模式（Instruct/Thinking）、最长上下文、服务限流（RPM/TPM）、部署副本数和部署模板。

## API 部署方式

百炼支持通过 HTTP API 进行[模型部署](../concepts/model-deployment.md)的全生命周期管理（详见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)）。

### 创建部署

**PTU 模式：**

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

**模型单元模式：**

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

**Token 用量模式（仅限 LoRA 调优后模型）：**

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b-ft-202511132025-0260",
    "plan": "lora",
    "capacity": 1,
    "name": "qwen3-8b-ft"
}'
```

### 查询与删除

- **查询状态**：`GET /api/v1/deployments/{deployed_model}`，状态为 `RUNNING` 时部署完成
- **删除服务**：`DELETE /api/v1/deployments/{deployed_model}`，执行后立即下线且不可恢复

### 调用推理

部署成功后使用 DashScope SDK 发起推理请求，需确保 API Key 所在的[业务空间](../concepts/workspace.md)与[模型部署](../concepts/model-deployment.md)所在的[业务空间](../concepts/workspace.md)相同。

## 模型导入

百炼支持从阿里云 OSS 导入本地训练的 LoRA 模型（详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)）。

### 支持导入的基础模型

- 千问3：32B、14B、8B、4B-Instruct-2507
- 千问3-VL：8B-Instruct
- 千问2.5：72B、32B、14B、7B Instruct
- 千问2.5-VL：72B、7B Instruct

### 导入要求

- **必需文件**：`adapter_model.safetensors`（权重文件）和 `adapter_config.json`（配置文件）
- **rank 参数**：必须为 8、16、32 或 64，且所有 LoRA 层使用相同 rank 值
- **不支持**：修改了词汇表或 chat_template 的模型、未冻结 VIT 的视觉语言模型
- 导入前需完成 OSS 授权并为目标 Bucket 添加 `bailian-datahub-access` 标签

### 导入后推理效果对齐

导入模型与本地 vLLM/SGLang 推理效果可能不一致，建议调整 `temperature=1.0`、`top_p=1.0`、`presence_penalty=0`、`repetition_penalty=1.0` 等参数以对齐效果。

## 权限与常见问题

- **权限不足**：检查 API Key 归属[业务空间](../concepts/workspace.md)的[模型部署](../concepts/model-deployment.md)权限，以及归属账号在[业务空间](../concepts/workspace.md)中的操作权限
- **子账号使用**：需主账号先在 RAM 控制台授予 `ram:CreateServiceLinkedRole` 权限，再完成 OSS 服务关联角色授权
- **OSS 报错 10041495**：通常是主账号未开通 OSS 服务，需先开通后再授权

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)



