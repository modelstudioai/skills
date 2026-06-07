# model deployment 1

百炼平台提供模型部署功能，可为预置模型或调优后的模型创建独立的、资源专享的推理服务，满足高并发、低延迟等业务需求。平台支持三种计费方式（预置吞吐、模型单元、Token 用量），同时支持从 OSS 导入本地训练的 LoRA 模型进行部署。本功能仅适用于"中国内地（北京）"地域。

## 计费方式

百炼模型部署提供三种计费模式，适用于不同业务场景。详细说明参见[模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

### 预置吞吐（PTU）

- **定义**：通过平台预留资源，保障特定 TPM 吞吐能力；在保障额度内不限速。
- **计费公式**：`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`
- **支持模型**：部分预置模型（千问系列、DeepSeek、千问VL、GLM 等）。
- **适用场景**：流量稳定的生产环境，如智能客服、内容审核、翻译 API 等。
- **付费方式**：后付费（按小时）或预付费（按天）。预付费订单支付后实时生效，到期后延后 2 小时停服，停服后资源保留 14 小时释放。
- **溢出处理**：超出购买的 TPM 量时，自动切换为按量付费模式，API 返回 Header 包含 `x-dashscope-ptu-overflow:true`。

### 模型单元（MU）

- **定义**：按使用时长与模型单元数量配置算力，资源独占。
- **计费公式**：`费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价`
- **支持模型**：部分预置模型与所有调优后模型，覆盖文本生成、多模态、语音合成等类型。
- **适用场景**：需要自定义性能指标、资源隔离的场景，如私有微调模型部署、长时计算任务。
- **特性**：支持 PD 分离计算模式（将 Prefill 和 Decode 拆到不同节点执行，降低首 Token 延迟）；支持配置推理模式（Instruct/Thinking）、最长上下文、服务限流（RPM/TPM）。
- **付费方式**：后付费（按小时）或预付费（包月）。首月内提前退订，日单价按 1.2 倍计费。

### Token 用量

- **定义**：按每次调用产生的输入/输出 Token 计量。
- **计费公式**：`费用 = 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价`
- **支持模型**：仅部分经过 LoRA 调优后的模型（千问系列、千问VL 系列）。
- **适用场景**：调优后模型的效果验证，不使用不计费。
- **限制**：一个月内不使用将自动释放；扩缩容需在控制台提交申请等待人工审核。

> **注意**：计费方式在服务创建后无法更改。如需切换，必须下线已部署的模型后重新部署。

## 部署方法

### 控制台部署

前往[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，选择模型和计费方式，设置模型名称后即可部署。部署状态为"运行中"时表示成功。

### API 部署

通过 HTTP API 可编程化创建部署服务，详细操作参见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。核心接口为 `POST https://dashscope.aliyuncs.com/api/v1/deployments`。

**预置吞吐部署示例**：

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

**模型单元部署示例**：

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

**关键 API 操作**：

| 操作 | 方法 | 端点 |
|------|------|------|
| 创建部署 | POST | `/api/v1/deployments` |
| 查询状态 | GET | `/api/v1/deployments/{deployed_model}` |
| 删除服务 | DELETE | `/api/v1/deployments/{deployed_model}` |

部署成功后返回的 `deployed_model` 为专属服务唯一 ID，状态为 `RUNNING` 时即可开始调用。

## 部署后调用

部署成功后，支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)、[DashScope 接口](../concepts/dashscope-api.md)及 Assistant SDK 调用。调用时 `model` 参数使用部署后的模型 `code`（在控制台获取）。

```python
from dashscope import Generation
from http import HTTPStatus
import os

response = Generation.call(
    model='qwen3-8b',
    prompt='你是谁？',
    enable_thinking=False,
    api_key=os.getenv('DASHSCOPE_API_KEY'),
)
if response.status_code == HTTPStatus.OK:
    print(response.output)
```

## 模型导入

百炼支持将本地训练的 LoRA 模型从 OSS 导入平台，然后进行部署。详细流程参见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

### 支持导入的基础模型

- 千问3：32B、14B、8B、4B-Instruct-2507
- 千问3-VL：8B-Instruct
- 千问2.5：72B、32B、14B、7B Instruct 版本
- 千问2.5-VL：72B、7B Instruct 版本

### 导入要求

- 仅支持 LoRA 模型，不支持全参微调模型。
- OSS Bucket 中必须包含 `adapter_model.safetensors`（权重文件）和 `adapter_config.json`（配置文件）。
- rank 值必须为 8、16、32 或 64 之一，且所有 LoRA 层 rank 值一致。
- 不支持修改了词汇表（vocab）或对话模板（chat_template）的模型。
- VL 模型必须冻结 VIT 部分（adapter 中不能包含 `visual` 相关权重参数）。
- 首次从 OSS 导入需完成授权，并为目标 Bucket 添加 `bailian-datahub-access` 标签。

### 推理效果一致性

导入模型的推理效果可能与本地 vLLM/SGLang 不一致。建议在 API 调用时对齐以下参数：`temperature=1.0`、`top_p=1.0`、`presence_penalty=0`、`repetition_penalty=1.0`。

## 权限与常见问题

- **部署权限不足**：检查 API Key 归属的业务空间是否拥有模型部署权限，以及 API Key 归属账号在该业务空间中是否有操作权限。
- **API Key 业务空间**：确保 API Key 所在的业务空间与模型部署所在的业务空间一致。
- **OSS 授权问题**：子账号需要主账号先授予 `ram:CreateServiceLinkedRole` 权限，再完成服务关联角色的创建。
- **10041495 报错**：主账号未开通 OSS 服务，需前往 OSS 控制台开通后重试。

## 来源文档

- [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


