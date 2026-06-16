# model deployment 1

百炼平台提供模型部署功能，支持将预置模型或调优后的模型部署为独立的、资源专享的推理服务，满足高并发、低延迟等业务需求。部署功能仅适用于华北二（北京）地域，支持三种计费方式和多种部署管理操作。

## 计费方式

百炼模型部署提供三种计费方式，适用于不同业务场景。详细说明参见 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

### 预置吞吐（PTU）

通过平台预留资源保障特定 TPM 吞吐能力，在保障额度内不限速。适用于流量稳定、需保障并发体验的生产环境。

- 计费公式：`费用 = 使用时长 x (输入 TPM 单价 x 输入 TPM + 输出 TPM 单价 x 输出 TPM)`
- 支持后付费（按小时）和预付费（按天）
- 预付费订单支付后实时生效，到期后延后 2 小时停止服务，停止后资源保留 14 小时后释放
- 预付费订单无法提前终止
- 当输入超过最长 Token 或超出购买 TPM 量时，调用自动切换为按量付费模式，API 返回 Header 包含 `x-dashscope-ptu-overflow:true`
- 支持长输入阶梯容量系数和缓存折扣
- TPS 相比按 Token 计费通常提升约 1.5~2.0 倍

### 模型单元（MU）

按使用时长与模型单元数量配置算力，资源独占，性能指标可自定义。

- 计费公式：`费用 = 使用时长（小时）x 模型单元数量 x 模型单元单价`
- 支持后付费（按小时）和预付费（包月）
- 首月内提前退订，日单价按 1.2 倍计费
- 后付费方式算力资源先买到先得
- 支持 PD 分离计算模式（Prefill 和 Decode 拆到不同节点，降低首 Token 延迟、提高吞吐）
- 可配置推理模式（Instruct/Thinking）、最长上下文、服务限流（RPM/TPM）

### 按 Token 用量

以每次调用产生的输入 Token 与输出 Token 作为计量依据，不使用不计费。

- 计费公式：`费用 = 输入 Token 数 x 输入单价 + 输出 Token 数 x 输出单价`
- 仅支持部分 LoRA 调优后的模型
- 一个月内不使用将自动释放
- 扩缩容需在控制台提交申请，等待人工审核

> **注意**：计费方式在服务创建后无法更改。如需切换，必须下线已部署的模型后重新部署。

## 支持的模型

PTU 模式支持部分预置模型，包括千问系列（qwen3.7-max、qwen3.6-flash/plus、qwen3.5-plus、qwen3-max、qwen-flash、qwen-plus 等）、DeepSeek 系列（v4-flash/pro、v3.2、v3）、千问 VL（qwen3-vl-plus）及 GLM-5.1。

模型单元模式支持范围更广，涵盖文本生成（千问、GLM、DeepSeek、MiniMax、Kimi）、多模态（千问 VL、千问 Omni）、语音合成（CosyVoice）等类型。支持 MU1~MU9 多种规格，部分模型支持 PD 分离模式部署。

按 Token 计费模式仅支持对千问 3/2.5 系列及千问 VL 系列基础模型完成 SFT 高效训练后的自定义模型。

## 部署方式

### 控制台部署

前往模型部署控制台（北京），填写服务名称、选择模型和计费方式后确认即可。部署状态为"运行中"时表示部署成功。需先完成模型调优方可部署大部分模型。

### API 部署

通过 HTTP API 可完成模型的部署、查询、推理和删除全流程，详细操作参见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

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
    "capacity": 4,
    "max_context_length": 10000,
    "rpm_limit": 500,
    "tpm_limit": 1000
}'
```

**查询服务状态：** `GET /api/v1/deployments/{deployed_model}`，当 `status` 为 `RUNNING` 时部署完成。

**删除服务：** `DELETE /api/v1/deployments/{deployed_model}`，删除后立即开始下线且不可恢复。

**推理调用：** 部署成功后可通过 DashScope SDK 发起推理请求，需确保 API Key 所在[业务空间](../concepts/workspace.md)与模型部署所在[业务空间](../concepts/workspace.md)相同。

## 模型导入

百炼支持将本地训练的 LoRA 模型从阿里云 OSS 导入到平台，导入后可进行部署、增量训练等操作。详细流程参见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

### 支持导入的基础模型

- 千问 3：32B、14B、8B、4B-Instruct-2507
- 千问 3-VL：8B-Instruct
- 千问 2.5：72B、32B、14B、7B（Instruct）
- 千问 2.5-VL：72B、7B（Instruct）

### 导入要求

- 仅支持 LoRA 模型，不支持全参微调模型
- 必需文件：`adapter_model.safetensors`（权重）和 `adapter_config.json`（配置）
- rank 值必须为 8、16、32 或 64，且所有 LoRA 层使用相同 rank
- 不支持修改了词汇表或 chat_template 的模型
- VL 模型必须冻结 VIT 部分
- OSS Bucket 需添加 `bailian-datahub-access` 标签且文件不能放在根目录

### 推理效果差异

导入模型在百炼上的推理效果可能与本地 vLLM/SGLang 不一致，建议调整 `temperature=1.0`、`top_p=1.0`、`presence_penalty=0`、`repetition_penalty=1.0` 等参数以对齐默认行为。

## 权限与常见问题

- 部署时提示权限不足：需检查 API Key 归属[业务空间](../concepts/workspace.md)的模型部署权限，以及归属账号在业务空间中的操作权限
- 首次从 OSS 导入需完成服务关联角色授权；子账号需主账号先授予 `ram:CreateServiceLinkedRole` 权限
- 模型监控（TPM 统计、调用次数）可在模型监控控制台查看
- 后付费账户欠费时，资源保留并继续计费 24 小时后自动释放

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


