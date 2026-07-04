# model deployment 1

百炼平台支持将预置模型或调优后的模型部署为资源专享的推理服务，提供预置吞吐（PTU）、模型单元、按 Token 用量三种计费方式，分别面向高并发稳定吞吐、自定义性能指标、低成本效果验证等场景。本文汇总部署基础概念、计费方式、长输入与缓存、模型导入以及 API 部署操作流程。

## 计费方式对比

| 计费方式 | 适用场景 | 扩缩容 | 支持模型 |
| --- | --- | --- | --- |
| 预置吞吐（PTU） | 高负载生产环境，需稳定吞吐、低延迟 | 自助增减吞吐量 | 部分预置模型 |
| 模型单元 | 性能指标自定义、资源独占、长时任务 | 自助增减模型单元数量 | 部分预置模型与所有调优后模型 |
| 按 Token 用量 | 调优后模型效果验证，低成本 | 控制台提交申请，人工审核 | 部分 LoRA 调优后模型 |

> **注意**：计费方式在服务创建后无法更改，如需切换必须先下线已部署的模型再重新部署。详见 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

### 计费公式

- PTU：`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`，后付费按小时、预付费按天计费。
- 模型单元：`费用 = 使用时长（小时） × 模型单元数量 × 模型单元单价`，预付费按月计费时改为 `包月数 × 模型单元数量 × 月单价`。
- 按 Token 用量：`费用 = 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价`，最小计费单位 1 token。

## 预置吞吐长输入与缓存

PTU 部署支持长输入（部分模型最高 200K token）和前缀缓存，通过阶梯容量系数和缓存折扣管理额度消耗。核心能力详见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)：

- **长输入阶梯系数**：超出 32K 的输入按更高系数折算 TPM。以 glm-5.1 为例，`[0, 32K)` 系数 1.0，`[32K, 200K]` 输入 1.33 / 输出 1.17。
- **前缀缓存折扣**：命中缓存的输入 token 按模型对应折扣折算容量（如 glm-5.1 为 0.2，deepseek-v4-pro 为 0.08）。
- **自动转按量计费**：超出 PTU 额度或输入超过模型上限（千问 128K / DeepSeek 64K）时，请求自动转为按量计费，响应头包含 `x-dashscope-ptu-overflow:true`，业务不中断。

### 容量计算器

在创建或扩容 PTU 部署时，控制台提供容量计算器，根据每分钟请求数（RPM）、平均输入/输出长度、预估缓存命中率推荐输入 TPM 和输出 TPM。建议在长输入场景下先用计算器评估额度，避免意外转为按量计费。

### API 响应字段

PTU 部署的响应包含额度相关字段：

- `service_tier`：`ptu-standard` 表示使用 PTU 额度；`default` 或不返回表示按量计费。
- `provisioned_tokens`：折算后实际消耗的 PTU 额度（含阶梯系数和缓存折扣）。
- `cached_tokens`：前缀缓存命中的 token 数。

字段在不同 API 格式下的 JSON 路径有差异：OpenAI Chat 兼容为 `usage.prompt_tokens_details.cached_tokens`；OpenAI Responses 为 `usage.input_tokens_details.cached_tokens`；Anthropic 兼容暂不返回 `cached_tokens`。

## 模型导入

部署调优后模型前，需先将本地训练的 LoRA 模型从 OSS 导入百炼平台，操作入口为「我的模型」页面。导入流程与限制详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

### 前提条件

- OSS Bucket 已创建并添加 `bailian-datahub-access` 标签（值为 `read`），不支持归档/冷归档类型，不支持根目录文件。
- 模型文件需包含 `adapter_model.safetensors` 和 `adapter_config.json`。
- rank 值必须为 8、16、32 或 64，且同一模型所有 LoRA 层 rank 一致。
- 不可修改词汇表（vocab）或 `chat_template`；VL 模型必须冻结 VIT 部分。

### 支持导入的基础模型

千问3 系列（32B/14B/8B/4B-Instruct-2507）、千问3-VL-8B-Instruct、千问2.5 系列（72B/32B/14B/7B-Instruct）、千问2.5-VL 系列（72B/7B-Instruct）。

### 首次授权

首次从 OSS 导入需主账号或子账号完成授权：开通 OSS 服务关联角色 `AliyunServiceLinkedRoleForSFMDataHubOSSImport`，并为目标 Bucket 添加 `bailian-datahub-access` 标签。子账号需先由主账号授予 `ram:CreateServiceLinkedRole` 权限。

> **注意**：若部署后调用效果与本地 vLLM/SGLang 不一致，建议调整 `temperature=1.0`、`top_p=1.0`、`top_k=None`、`presence_penalty=0`、`repetition_penalty=1.0` 等推理参数以对齐 vLLM 默认值。

## 通过 API 部署模型

部署操作仅适用于华北2（北京）地域。前提：已阅读 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)、已获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`。

### 1. 创建部署

按 PTU 计费：

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_flash",
    "model_name": "qwen-flash-2025-07-28",
    "plan": "ptu",
    "ptu_capacity": {"input_tpm": 10000, "output_tpm": 1000}
}'
```

按模型单元计费：

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

按 Token 用量计费：

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

> **注意**：按 Token 用量计费时 `capacity` 参数设置无效但必须填写，扩缩容需前往控制台提交表单申请。

### 2. 查询状态

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments/<deployed_model>" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

返回 `status` 为 `RUNNING` 时部署完成。响应中 `deployed_model` 为专属服务的唯一 ID。

### 3. 调用推理

使用 `deployed_model` 作为 `model` 参数调用 SDK，需保证 API Key 业务空间与部署所在空间一致：

```python
from dashscope import Generation
from http import HTTPStatus
import os

response = Generation.call(
    model='qwen3-8b-ft-202511132025-0260',
    prompt='你是谁？',
    enable_thinking=False,
    api_key=os.getenv('DASHSCOPE_API_KEY'),
)
```

### 4. 删除服务

```bash
curl --request DELETE 'https://dashscope.aliyuncs.com/api/v1/deployments/<deployed_model>' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

删除后服务立即下线且不可恢复，停止计费。完整流程参考 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 限制与注意事项

- PTU 预付费按天计费，无法提前退费；模型单元预付费首月内退订日单价按 1.2 倍计费。
- 按 Token 用量计费仅支持部分高效微调（LoRA）后的模型，一个月内不使用将自动释放。
- 部署大部分模型前需先完成模型调优。
- 部署成功后立即产生费用，即使未发起调用。
- API 部署需业务空间拥有目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx` 或 `Workspace access denied`。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)



