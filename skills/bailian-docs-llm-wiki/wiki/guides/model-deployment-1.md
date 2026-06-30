# model deployment 1

百炼平台提供独立的、资源专享的[模型部署](../concepts/model-deployment.md)能力，将平台预置模型或您调优后的[模型部署](../concepts/model-deployment.md)为推理服务，满足高并发、低延迟等业务需求。部署支持预置吞吐（PTU）、模型单元、按 [Token](../concepts/token.md) 用量三种[计费](../concepts/billing.md)方式，可通过控制台或 API/命令行完成部署、查询、推理和删除全流程操作。本文相关能力仅适用于华北二（北京）地域。

## [计费](../concepts/billing.md)方式

部署前可在[模型部署](../concepts/model-deployment.md)控制台（北京）查看不同模型的预估每小时费用。[计费](../concepts/billing.md)方式在服务创建后无法更改，如需切换必须下线已部署模型后重新部署。三种计费方式对比：

| 计费方式 | 适用场景 | 计费依据 | 扩缩容 | 关键约束 |
| --- | --- | --- | --- | --- |
| 预置吞吐（PTU） | 高负载生产环境、稳定吞吐、低延迟、流量可预估 | 使用时长 × 预置吞吐 | 自助增减吞吐量 | 超出额度自动转按量计费；预付费无法提前退费 |
| 模型单元 | 资源独占、性能指标自定义、长时任务 | 使用时长 × 模型单元数量 × 单价（包月：包月数 × 数量 × 月单价） | 自助增减模型单元数量 | 后付费先到先得；首月内退订日单价按 1.2 倍计费 |
| [Token](../concepts/token.md) 用量 | 调优后效果验证、高性价比、对并发延迟要求不高 | 输入/输出 [Token](../concepts/token.md) 数 × 单价 | 控制台提交申请，人工审核 | 仅支持部分 LoRA 调优模型；一个月不使用自动释放 |

PTU 模式相比按 Token 计费，TPS 通常提升约 1.5~2.0 倍；模型单元模式支持 PD 分离计算模式（将 Prefill 与 Decode 拆到不同节点，降低首 Token 延迟、提高吞吐）；按 Token 用量模式为"不使用不计费"。详细计费规则与单价表见 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 预置吞吐长输入与缓存

PTU 部署支持长输入和前缀缓存，通过阶梯容量系数和缓存折扣管理额度消耗。核心能力：

- **长输入支持**：部分模型支持超过 32K token 的输入，超出部分按更高的阶梯系数折算 TPM 消耗。
- **前缀缓存优惠**：命中缓存的输入 token 按折扣系数消耗额度，可降低多轮对话和重复前缀场景的额度消耗。
- **自动转按量计费**：超出 PTU 额度或输入超过模型上限（千问 128K / DeepSeek 64K）时，请求自动转为按量计费，无需修改调用代码。响应头会包含 `x-dashscope-ptu-overflow:true`。

各模型长输入阶梯系数与缓存折扣不同，例如 `glm-5.1`（200K 上限，缓存折扣 0.2）：[0, 32K) 区间输入/输出系数均为 1.0，[32K, 200K] 区间输入 1.33 / 输出 1.17；`deepseek-v4-pro` 与 `qwen3.7-plus-2026-05-26` 为无阶梯（1.0）。

API 响应通过以下字段标识计费方式和额度消耗：

| 字段 | 说明 |
| --- | --- |
| `service_tier` | `ptu-standard` 表示使用 PTU 额度；`default` 或不返回表示按量计费 |
| `provisioned_tokens` | 折算后实际消耗的 PTU 额度 token 数（含阶梯系数和缓存折扣） |
| `cached_tokens` | 前缀缓存命中的 token 数 |

不同 API 格式（OpenAI Chat 兼容 / OpenAI Responses / Anthropic 兼容 / DashScope）下，上述字段的 JSON 路径存在差异。Anthropic 兼容格式暂不返回 `cached_tokens`，可通过 `provisioned_tokens` 间接判断缓存效果。完整字段说明见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

> **注意**：PTU 利用率在长输入场景下可能超过 100%（因阶梯系数使折算消耗高于原始 token 数），属正常现象，超出部分自动转按量计费，不影响服务可用性。

## 模型导入

部署自定义 LoRA 模型前，需先将本地训练的 LoRA 模型从阿里云 OSS 导入到百炼。**当前版本仅支持导入 LoRA 模型，不支持全参微调模型**。支持导入的基础模型涵盖千问3 系列（32B/14B/8B/4B-Instruct-2507、千问3-VL-8B-Instruct）和千问2.5 系列（72B/32B/14B/7B-Instruct、千问2.5-VL-72B/7B-Instruct）。

导入前提与限制：

- **OSS Bucket**：需创建 Bucket 并添加 `bailian-datahub-access` 标签（标签值为 `read`）。不支持归档/冷归档/深度冷归档存储类型；不支持访问 Bucket 根目录下的文件，须选择或新建子目录；支持内容加密和私有 Bucket。
- **必需文件**：`adapter_model.safetensors`（权重）与 `adapter_config.json`（配置）。
- **rank 限制**：rank 必须为 8、16、32 或 64 之一，同一模型所有 LoRA 层 rank 值需一致。
- **词汇表与对话模板**：训练时添加新 token 或修改 vocab、修改 `chat_template` 的模型均无法导入。
- **VIT 冻结**：VL 模型必须冻结 Vision Transformer，LoRA adapter 中若包含 `visual` 开头的权重参数则无法导入。

首次从 OSS 导入需完成授权：主账号单击"前往授权"自动开通 OSS 服务关联角色（`AliyunServiceRoleForSFMDataHubOSSImport`）并为 Bucket 添加标签；子账号则需主账号先在 RAM 控制台授予 `ram:CreateServiceLinkedRole` 权限后再完成授权。导入后模型状态包括创建中、创建成功（可部署）、创建失败、已失效。详细操作步骤见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

> **注意**：导入的模型在百炼平台推理的效果可能与本地使用 vLLM、SGLang 不一致，原因是推理引擎默认参数不同。建议调用 API 时参照 vLLM 默认值调整 `temperature`（1.0）、`top_p`（1.0）、`top_k`（None 或 >100）、`presence_penalty`（0）、`repetition_penalty`（1.0）等参数。

## 使用 API 或命令行部署

通过 `https://dashscope.aliyuncs.com/api/v1/deployments` 接口可完成部署、查询、推理、删除全流程。前提：已获取并配置 [API Key](../concepts/api-key.md) 到环境变量，且 [API Key](../concepts/api-key.md) 归属[业务空间](../concepts/workspace.md)与模型部署所在[业务空间](../concepts/workspace.md)相同。

**1. 部署模型**：通过 `model_name` 参数指定模型 ID，`plan` 字段区分计费方式。

- PTU 计费：`"plan": "ptu"`，配合 `ptu_capacity`（含 `input_tpm`/`output_tpm`）。
- 模型单元计费：`"plan": "mu"`，配合 `deploy_spec`（如 `MU1`）、`capacity`（副本数）、`enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit` 等。
- Token 用量计费：`"plan": "lora"`，`capacity` 参数必须填写但设置无效，扩缩容需在控制台提交申请。

部署成功后返回 `deployed_model`（专属服务唯一 ID）和 `status`（初始为 `PENDING`）。

**2. 查询服务状态**：`GET /api/v1/deployments/{deployed_model}`，当 `status` 为 `RUNNING` 时部署完成。响应包含 `base_capacity`、`capacity`、`ready_capacity`、`model_unit_spec` 等字段。

**3. 执行推理请求**：部署完成后，使用 SDK 或 HTTP 调用专属服务。调用时 `model` 参数填基础模型名（如 `qwen3-8b`），并通过 `enable_thinking` 等控制推理行为。

**4. 删除专属服务**：`DELETE /api/v1/deployments/{deployed_model}`。删除后服务立即下线且不可恢复，无法再调用该模型，部署停止计费。完整 API 示例见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 部署配置项

模型单元计费模式下支持的关键配置：服务名称、选择模型（预置或调优后）、模型单元类型（不同规格对应不同算力）、部署副本数（影响并发）、部署模版（如单机部署）、推理模式（Instruct 非思考 / Thinking 思考，部分模型可在部署时选择是否开启思考模式）、最长上下文（基于模型类型）、服务限流（限制 RPM/TPM）。PTU 模式下吞吐/并发和生成速度均由平台预置，用户不可调。

## 限制与注意事项

- 仅适用于华北二（北京）地域。
- 计费方式创建后无法更改，切换须下线后重新部署。
- 部署大部分模型前需先完成模型调优（预置模型可直接部署的除外）。
- PTU 预付费按天计费，无法提前退费；订单到期后延后 2 小时停止服务，资源保留 14 小时后释放；22:00 后下单到期日顺延 1 天。
- 后付费欠费时资源保留并计费 24 小时（期间服务可用），超过 24 小时停止计费、底层资源删除但任务保留；补足欠费后重新分配资源恢复使用。
- 模型单元首月内提前退订，日单价按 1.2 倍计费。
- 按 Token 用量计费仅支持部分基础模型经 SFT 高效训练后的自定义模型，一个月不使用自动释放。
- 部署时报"权限不足"：需确保 [API Key](../concepts/api-key.md) 归属[业务空间](../concepts/workspace.md)拥有模型部署权限（业务空间管理 > 模型权限流控设置），且 API Key 归属账号在该业务空间有操作权限（权限管理用户列表包含主账号）。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)




