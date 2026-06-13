# model deployment 1

百炼平台提供[模型部署](../concepts/model-deployment.md)功能，支持将预置模型或调优后的[模型部署](../concepts/model-deployment.md)为独立的、资源专享的推理服务，以满足高并发、低延迟等不同业务性能需求。部署服务目前仅适用于华北二（北京）地域，支持通过控制台或 API 两种方式操作。此外，平台还支持从 OSS 导入本地训练的 LoRA 模型，导入后即可进行部署。

## 计费方式

百炼[模型部署](../concepts/model-deployment.md)提供三种计费方式，创建后不可更改。如需切换必须先下线再重新部署。详细说明参见 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

### 预置吞吐（PTU）

通过平台预留资源保障特定 TPM 吞吐能力，在保障额度内不限速。适用于流量稳定、需要保障并发体验的高负载生产环境。

- 吞吐/并发和生成速度由平台预置，用户不可调
- TPS 相比按 Token 用量计费通常提升约 1.5~2.0 倍
- 支持自动续费
- 预付费按天计费，后付费按小时计费
- 超出购买的 TPM 量时，自动切换为按量付费模式（API 返回 Header 包含 `x-dashscope-ptu-overflow:true`）

### 模型单元（MU）

按使用时长与模型单元数量计费，资源独占。适用于需要自定义性能指标的场景。

- 延迟/吞吐等性能指标可自定义
- 支持 PD 分离计算模式（将首 Token 计算与后续 Token 计算拆到不同节点执行，降低首 Token 延迟、提高吞吐）
- 后付费按小时计费，预付费按月计费
- 首月内提前退订，日单价按 1.2 倍计费

### 按 Token 用量

以每次调用产生的输入/输出 Token 作为计量依据，不使用不计费。

- 仅支持部分高效微调（LoRA）后的模型
- 一个月内不使用将自动释放
- 适合调优后模型效果验证

## 支持的模型

部署支持多种模型系列，包括：

| 系列 | 代表模型 | 计费模式 |
|------|---------|---------|
| 千问 | qwen3.7-max、qwen3.6-flash/plus、qwen-flash/plus 等 | PTU / MU |
| DeepSeek | deepseek-v4-pro、deepseek-v3.2、deepseek-v3 | PTU / MU |
| 千问 VL | qwen3-vl-plus、qwen3-vl-8b-instruct 等 | PTU / MU |
| 千问 Omni | qwen3.5-omni-flash、qwen3.5-omni-plus | MU |
| GLM | glm-5.1、glm-5、glm-4.7 | PTU / MU |
| 其他 | MiniMax-M2.5、Kimi-K2.5 | MU |
| LoRA 调优模型 | 千问3/2.5 系列（3B~72B） | Token 用量 |

完整的模型列表和价格信息参见 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) 中的计费详情部分。

## 控制台部署

1. 前往 [模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)
2. 填写服务名称，选择模型和计费方式
3. 等待部署状态变为**运行中**

> **注意**：部署成功后即开始计费，无论是否有调用请求。

## API 部署

通过 HTTP API 可以完成部署、查询、推理和删除的完整生命周期管理。详细操作参见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

### 创建部署

**PTU 模式**：

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

**模型单元模式**：

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

**按 Token 用量模式**（仅限 LoRA 调优模型）：

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

### 查询状态

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments/<deployed_model>" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

当返回 `"status": "RUNNING"` 时，服务部署完成。

### 调用推理

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
```

### 删除服务

```bash
curl --request DELETE \
  'https://dashscope.aliyuncs.com/api/v1/deployments/<deployed_model>' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

> **注意**：删除操作立即生效且不可恢复。

## 模型导入

百炼支持将本地训练的 LoRA 模型从 OSS 导入平台，导入后可进行部署。详细操作参见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

### 支持导入的基础模型

- 千问3：32B、14B、8B、4B-Instruct-2507
- 千问3-VL：8B-Instruct
- 千问2.5：72B、32B、14B、7B（Instruct 版本）
- 千问2.5-VL：72B、7B（Instruct 版本）

### 导入要求

- 仅支持 LoRA 模型，不支持全参微调模型
- 必需文件：`adapter_model.safetensors` 和 `adapter_config.json`
- rank 值必须为 8、16、32 或 64 之一
- 不可修改词汇表或 chat_template
- VL 模型必须冻结 VIT 部分

### OSS 授权

首次导入需完成以下步骤：

1. 在导入界面点击**前往授权**，确认开通 OSS 服务关联角色
2. 为目标 OSS Bucket 添加标签 `bailian-datahub-access`（值为 `read`）
3. 返回导入界面选择 Bucket 和模型目录

> **注意**：子账号需要主账号先授予 `ram:CreateServiceLinkedRole` 权限后才能完成授权。

## 部署配置选项

模型单元模式下支持更多配置：

| 配置项 | 说明 |
|-------|------|
| 推理模式 | Instruct（非思考）或 Thinking（思考） |
| 最长上下文 | 基于模型类型设置 |
| 服务限流 | 可限制 RPM、TPM |
| 部署副本数 | 影响并发处理能力 |
| 部署模版 | 单机部署等不同资源配置方案 |

## 常见问题

**权限不足**：确保 API Key 的归属[业务空间](../concepts/workspace.md)拥有[模型部署](../concepts/model-deployment.md)权限，且归属账号在该[业务空间](../concepts/workspace.md)中有操作权限。前往[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)检查[模型部署](../concepts/model-deployment.md)授权状态。

**导入模型推理效果不一致**：百炼推理引擎参数可能与本地框架默认值不同。建议将 `temperature` 设为 1.0、`top_p` 设为 1.0、`repetition_penalty` 设为 1.0 以对齐 vLLM 默认行为。

**OSS 报错 10041495**：主账号需先前往 OSS 管理控制台开通对象存储服务。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)



