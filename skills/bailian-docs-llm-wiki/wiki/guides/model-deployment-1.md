# model deployment 1

百炼平台提供模型部署能力，把预置模型或调优后的模型部署为资源专享的推理服务，满足高并发、低延迟等不同性能诉求。本文汇总部署计费方式、PTU 长输入与缓存、API/命令行部署流程，以及从 OSS 导入 LoRA 模型的全部要点。文中所述能力仅适用于华北二（北京）地域。

## 计费方式

部署服务创建后计费方式无法更改，切换需先下线再重新部署。三种计费方式对比见 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

| 计费方式 | 计费公式 | 扩缩容 | 典型场景 |
| --- | --- | --- | --- |
| 预置吞吐（PTU） | 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM) | 自助增减吞吐量 | 高负载生产环境，需稳定 TPS 与低延迟 |
| 模型单元 | 使用时长 × 模型单元数量 × 模型单元单价；包月则 包月数 × 模型单元数量 × 月单价 | 自助增减模型单元数量 | 私有模型独占资源、长时任务、PD 分离模式 |
| Token 用量 | 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价 | 控制台提交申请，人工审核 | 调优后模型效果验证，性价比最高 |

PTU 与模型单元均支持后付费（按小时/随用随付）与预付费（按天/按月）。预付费按天订单支付后实时生效，到期后延后 2 小时停止服务、资源保留 14 小时后释放；预付费无法提前终止退费，缩容退款按降配退款规则处理。模型单元预付费首月内退订，日单价按 1.2 倍计费。

支持模型覆盖千问、DeepSeek、千问 VL、千问 Omni、GLM、CosyVoice 等系列，详细单价表见 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。模型单元部署模式支持选择 Instruct（非思考）/ Thinking（思考）/ Instruct/Thinking（可切换）推理模式，以及 PD 分离模式（拆分 Prefill 与 Decode 节点，降低首 Token 延迟、提高吞吐）。

## PTU 长输入与缓存

PTU 部署支持长输入请求（部分模型最高 200K token）和前缀缓存，通过阶梯容量系数和缓存折扣管理额度消耗，详见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

当前支持模型参数：

| 模型 | 输入长度上限 | 缓存折扣 | 长输入阶梯系数 |
| --- | --- | --- | --- |
| glm-5.1 | 200K | 0.2 | [0,32K) 输入 1.0/输出 1.0；[32K,200K] 输入 1.33/输出 1.17 |
| deepseek-v4-pro | 256K | 0.08 | 无阶梯（1.0） |
| qwen3.7-plus-2026-05-26 | 256K | 0.2 | 无阶梯（1.0） |
| 其他模型 | 以控制台为准 | 暂不支持 | 无阶梯（1.0） |

额度超出或输入超过模型上限（千问 128K / DeepSeek 64K）时，请求自动转为按量计费，API 响应头返回 `x-dashscope-ptu-overflow:true`，业务不中断。建议在创建或扩容前用容量计算器评估 RPM、平均输入/输出长度、预估缓存命中率，避免额度不足导致转按量付费。

API 响应通过以下字段标识计费方式与额度消耗：

- `service_tier`：`ptu-standard` 表示使用 PTU 额度；`default` 或不返回表示按量计费。
- `provisioned_tokens`：折算后实际消耗的 PTU 额度（含阶梯系数与缓存折扣）。
- `cached_tokens`：前缀缓存命中 token 数。

不同 API 格式下字段 JSON 路径不同：OpenAI Chat 兼容与 DashScope 用 `usage.prompt_tokens_details` / `usage.completion_tokens_details`；OpenAI Responses 用 `usage.input_tokens_details` / `usage.output_tokens_details`；Anthropic 兼容暂不返回 `cached_tokens`，可通过 `provisioned_tokens` 间接判断。

监控指标可在 [模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 查看，长输入场景下 PTU 利用率超过 100% 属正常现象（折算后消耗高于原始 token 数）。

## 使用 API 或命令行部署

部署前需获取 API Key 并配置到环境变量，且熟悉部署基本步骤。所有部署请求调用 `https://dashscope.aliyuncs.com/api/v1/deployments`，认证头为 `Authorization: Bearer $DASHSCOPE_API_KEY`，详见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

部署成功后立即开始计费，建议先确认计费规则再执行部署命令。三种 plan 示例：

PTU（`plan: "ptu"`，吞吐与生成速度平台预置、不可调）：

```json
{
  "name": "my_qwen_flash",
  "model_name": "qwen-flash-2025-07-28",
  "plan": "ptu",
  "ptu_capacity": { "input_tpm": 10000, "output_tpm": 1000 }
}
```

模型单元（`plan: "mu"`，吞吐/并发/生成速度可自定义，支持 enable_thinking、max_context_length、rpm_limit、tpm_limit 等）：

```json
{
  "name": "my_qwen_plus",
  "model_name": "qwen-plus-2025-12-01",
  "plan": "mu",
  "deploy_spec": "MU1",
  "enable_thinking": true,
  "capacity": 4,
  "max_context_length": 10000,
  "rpm_limit": 500,
  "tpm_limit": 1000
}
```

Token 用量（`plan: "lora"`，仅支持 LoRA 调优后模型，capacity 必填但实际无效，扩缩容需去控制台提交申请）：

```json
{
  "model_name": "qwen3-8b-ft-202511132025-0260",
  "plan": "lora",
  "capacity": 1,
  "name": "qwen3-8b-ft"
}
```

返回体 `output.deployed_model` 为专属服务唯一 ID。查询服务状态用 `GET /api/v1/deployments/{deployed_model}`，`status` 为 `RUNNING` 时部署完成，可使用 `deployed_model` 作为 SDK `model` 参数发推理请求（确保 API Key [业务空间](../concepts/workspace.md)与部署空间一致）。删除服务用 `DELETE /api/v1/deployments/{deployed_model}`，删除后立即下线且不可恢复、停止计费。

## 部署配置项

模型单元部署模式支持服务名称、选择模型、模型单元类型、部署副本数、部署模版（如"单机部署"）、推理模式（Instruct/Thinking）、最长上下文、服务限流（RPM/TPM）。PTU 部署模式下吞吐/并发和生成速度均为平台预置，用户不可调。完整配置项说明见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 从 OSS 导入 LoRA 模型

部署调优后模型前，需先将本地训练的 LoRA 模型从 OSS 导入百炼，详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。支持的基础模型覆盖千问3（32B/14B/8B/4B-Instruct-2507）、千问3-VL-8B-Instruct、千问2.5（72B/32B/14B/7B-Instruct）与千问2.5-VL（72B/7B-Instruct）。

导入要求与限制：

- OSS Bucket 不支持归档/冷归档/深度冷归档类型，支持内容加密与私有 Bucket；不支持访问 Bucket 根目录文件，需选择子目录。
- 必需文件：`adapter_model.safetensors`（SafeTensors 权重）与 `adapter_config.json`（含 rank、alpha 等参数）。
- rank 值必须为 8、16、32 或 64，且同一模型所有 LoRA 层 rank 相同。
- 不支持导入修改词汇表、修改 chat_template、或未冻结 VIT 的视觉语言模型（adapter 文件中不应出现 `visual` 开头的权重键）。
- 当前版本仅支持导入 LoRA 模型，不支持全参微调模型；导入后使用百炼免费存储空间。

首次从 OSS 导入需主账号完成 OSS 服务关联角色授权，并为目标 Bucket 添加 `bailian-datahub-access`（值为 `read`）标签，子账号则需先由主账号在 RAM 控制台授予 `ram:CreateServiceLinkedRole`（Condition 限定 `datahub.sfm.aliyuncs.com`）权限。

## 推理参数对齐

导入模型在百炼的推理效果可能与本地 vLLM/SGLang 不一致。为对齐 vLLM 默认行为，建议调用 API 时：`temperature=1.0`、`top_p=1.0`、`top_k=None` 或大于 100（不启用 top_k）、`presence_penalty=0`、DashScope 协议下 `repetition_penalty=1.0`。SGLang 等其他框架请参考对应文档。

## 限制与注意事项

- 部署能力仅适用于华北二（北京）地域。
- 大部分模型需先完成模型调优方可部署；按 Token 用量计费仅支持对指定基础模型完成 SFT 高效训练后的自定义模型。
- 部署成功后立即产生费用，PTU 与模型单元均如此；预付费按天订单无法提前退费。
- 模型单元后付费算力资源先到先得，购买不成功全额退款。
- Token 用量计费模式下，一个月内不使用将自动释放。
- 权限不足报错 `Workspace xxx does not have deployment privilege for model xxxx` 需在[业务空间](../concepts/workspace.md)"模型权限流控设置"中授权目标模型的部署权限；`Workspace access denied` 需在"权限管理"确认 API Key 归属账号已加入对应[业务空间](../concepts/workspace.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


