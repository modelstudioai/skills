# model deployment 1

模型部署用于将百炼平台的预置模型或调优/导入后的自定义模型发布为独立、资源专享的推理服务，满足高并发、低延迟场景的性能需求。本主题覆盖三种计费部署方式（预置吞吐 PTU、模型单元、按 Token 用量）的选型与计费规则、PTU 长输入与前缀缓存的额度消耗机制、从 OSS 导入 LoRA 模型的完整流程，以及通过 API/命令行完成部署、查询、推理和下线的操作步骤。

## 三种部署计费方式选型

根据 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)，平台提供三种部署方式，**计费方式在服务创建后无法更改**，切换需先下线再重新部署：

| 方式 | 定义 | 支持模型 | 计费 | 典型场景 |
| --- | --- | --- | --- | --- |
| 预置吞吐（PTU） | 平台预留资源，保障特定 TPM 吞吐，额度内不限速 | 部分预置模型 | 按使用时长和预置吞吐；随用随付、包天 | 高负载生产环境（智能客服、内容审核），TPS 比按量计费提升约 1.5~2.0 倍 |
| 模型单元（MU） | 按模型单元数量配置算力、资源独占，性能指标可自定义 | 部分预置模型与所有调优后模型 | 按使用时长 × 模型单元数量；随用随付、包月 | 私有微调模型、长时独占计算任务；支持 PD 分离模式 |
| Token 用量 | 按输入/输出 Token 计量，不使用不计费 | 部分 LoRA 调优后模型 | 按 Token 用量随用随付 | 调优后模型效果验证 |

关键计费公式：

- PTU：`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`，后付费按小时、预付费按天。
- 模型单元：`费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价`；预付费为 `包月数 × 模型单元数量 × 月单价`。
- Token 用量：`费用 = 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价`（最小计费单位 1 token），仅 SFT 高效训练（LoRA）后的自定义模型支持。

限制与注意事项：

- PTU 预付费按天计费、无法提前退费；预付费订单到期后延迟 2 小时停服，资源再保留 14 小时后释放。
- 模型单元预付费首月内提前退订，日单价（≈ 月单价 / 30）按 1.2 倍计费；后付费算力资源先买到先得，购买不成功全额退款。
- Token 用量方式的部署一个月内不使用将自动释放；扩缩容需在控制台提交申请人工审核。
- 后付费欠费后资源继续保留并计费 24 小时，超时后停止计费、底层资源删除，补足欠费后可恢复。
- PD 分离模式将 Prefill 与 Decode 拆到不同计算节点，降低首 Token 延迟、提高吞吐，仅模型单元部署支持。

## PTU 长输入、前缀缓存与溢出策略

[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) 描述了 PTU 的额度消耗细则：

- **长输入阶梯系数**：部分模型支持超 32K token 输入（如 glm-5.1 最高 200K），超出 32K 部分按更高系数折算 TPM（glm-5.1：[32K, 200K] 区间输入 1.33 / 输出 1.17）。deepseek-v4-pro、qwen3.7-plus-2026-05-26 无阶梯（1.0）。
- **前缀缓存折扣**：命中缓存的输入 token 按折扣系数消耗额度（glm-5.1 为 0.2，deepseek-v4-pro 为 0.08），适合多轮对话与重复前缀场景。
- **溢出策略**（创建 PTU 时选择）：「自动溢出」超额请求转为按量计费，业务不中断，响应头带 `x-dashscope-ptu-overflow:true`；「仅使用 PTU 容量」超额返回 429，不产生额外费用。
- **API 响应字段**：`service_tier`（`ptu-standard` 表示走 PTU 额度）、`provisioned_tokens`（折算后额度消耗）、`cached_tokens`（缓存命中数）。不同 API 格式（OpenAI Chat / Responses、Anthropic 兼容、DashScope）的 JSON 路径不同；Anthropic 兼容格式暂不返回 `cached_tokens`。
- 监控中 PTU 利用率超过 100% 属正常现象（长输入阶梯系数导致折算消耗高于原始 token 数）。

> **注意**：关于单次输入超出模型上限的行为，该文档 FAQ 称"千问系列输入上限 128K、DeepSeek 系列 64K"，但同文档额度规则表及 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) 价格表中已出现 256K 输入的模型（qwen3.7-max、deepseek-v4 系列）。各模型实际上限请以控制台展示为准。

创建或扩容前建议使用控制台的**预置吞吐额度计算器**，输入 RPM、平均输入/输出长度、缓存命中率，估算建议购买的输入/输出 KTPM。

## 从 OSS 导入 LoRA 模型

按 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)，可将本地训练的 LoRA 模型从阿里云 OSS 导入百炼后再部署。要点：

1. **首次授权**：一键创建服务关联角色 `AliyunServiceRoleForSFMDataHubOSSImport`（服务名 `datahub.sfm.aliyuncs.com`）；子账号需先由主账号授予 `ram:CreateServiceLinkedRole` 权限。目标 Bucket 必须添加标签 `bailian-datahub-access=read`，否则下拉不可选。
2. **文件要求**：子目录（不支持 Bucket 根目录）中须包含 `adapter_model.safetensors`、`adapter_config.json`、`config.json`。
3. **训练约束**：rank 必须为 8/16/32/64 且所有 LoRA 层一致；词汇表与 chat_template 不可修改；视觉语言模型必须冻结 VIT（adapter 中不能含 `visual` 开头的参数键）。
4. **限制**：仅支持 LoRA 模型（全参微调不可导入）；导入来源仅 OSS；导入的模型不支持增量训练；删除仅移除百炼侧记录、不影响 OSS 源文件；OSS 源文件变更后模型状态变为"已失效"，需重新导入。
5. **推理效果对齐**：百炼推理引擎默认参数与 vLLM/SGLang 可能不同，如需对齐 vLLM 默认值可设置 `temperature=1.0`、`top_p=1.0`、`presence_penalty=0`、`repetition_penalty=1.0` 等。

常见错误：`AvailableModelFileNotFound`（文件校验未通过）、`10041495`（主账号未开通 OSS）。

## 通过 API/命令行部署

[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) 给出了完整调用流程（**仅适用于华北2（北京）地域**，需先配置 `DASHSCOPE_API_KEY`）：

1. **创建部署**：`POST https://dashscope.aliyuncs.com/api/v1/deployments`，核心参数：
   - `model_name`：模型代码或调优后的模型 ID；
   - `plan`：`ptu`（预置吞吐，配 `ptu_capacity.input_tpm/output_tpm`）、`mu`（模型单元，配 `deploy_spec`、`capacity`、`enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit`）或 `lora`（按 [Token 计费](../concepts/token-billing.md)，`capacity` 必填但无效）。
   - 返回的 `deployed_model` 为专属服务唯一 ID。
2. **查询状态**：`GET /api/v1/deployments/<deployed_model>`，`status` 为 `RUNNING` 即部署完成。
3. **推理调用**：通过 DashScope SDK 调用，注意 API Key 所在[业务空间](../concepts/workspace.md)必须与部署所在[业务空间](../concepts/workspace.md)一致。
4. **删除服务**：`DELETE /api/v1/deployments/<deployed_model>`，删除后立即下线、停止计费、不可恢复。

> **注意**：部署成功后即开始计费，即使尚未发起任何调用；执行部署命令前请先确认计费规则。

权限报错排查：`Workspace xxx does not have deployment privilege for model xxxx` 需在[业务空间](../concepts/workspace.md)管理中对目标模型授权"模型部署"；`Workspace access denied` 需确认 API Key 归属账号在该业务空间的权限管理用户列表中。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


