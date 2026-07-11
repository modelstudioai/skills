# model deployment 1

阿里云百炼的模型部署功能可为平台预置模型或调优后的模型提供独立、资源专享的推理服务，满足高并发、低延迟等生产需求。本页汇总部署的三种计费方式、PTU 长输入与前缀缓存机制、LoRA 模型导入要求，以及通过 API/命令行完成部署的完整流程，面向需要落地私有推理服务的开发者。

## 三种计费方式与选型

部署时需在服务创建阶段选定计费方式，[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)将其分为三类：

- **预置吞吐（PTU，Provisioned Throughput Unit）**：平台预留资源保障特定 TPM 吞吐，额度内不限速。适合流量稳定、需并发/延迟确定性的高负载生产环境（如智能客服、实时内容审核）。相比按 Token 计费，TPS 通常提升约 1.5～2.0 倍。计费按使用时长 × TPM 单价，支持后付费（按小时）与预付费（按天）。
- **模型单元（MU）**：按使用时长 × 模型单元数量计费，资源独占、性能指标（延迟/吞吐）可自定义，支持 PD 分离计算模式（拆分 Prefill/Decode 阶段以降低首 Token 延迟、提高吞吐）。适合部署私有微调模型、长时任务。支持后付费（按分钟）与预付费（按月）。
- **按 Token 使用量**：仅对完成 SFT 高效训练（LoRA）后的自定义模型开放，不使用不计费，主要用于调优效果验证。

> **注意**：计费方式在服务创建后无法更改。如需切换，必须先下线已部署的模型再重新部署。

关键约束：预付费按天/按月计费，无法提前退费；首月内提前退订日单价按 **1.2 倍**计费。PTU 场景下如果单位时间使用超出购买吞吐量，或输入超过模型上限，将**自动切换为按量付费**（响应头返回 `x-dashscope-ptu-overflow:true`）。

## PTU 长输入与前缀缓存

[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)描述了 PTU 的额度消耗规则：

- **长输入阶梯系数**：部分模型（如 glm-5.1，上限 200K）对超过 32K 的输入按更高系数折算 TPM 消耗，例如 `[32K, 200K]` 区间输入系数 1.33 / 输出 1.17；deepseek-v4-pro、qwen3.7-plus 则无阶梯（1.0）。
- **前缀缓存折扣**：命中缓存的输入 token 按折扣系数消耗额度（glm-5.1 为 0.2，deepseek-v4-pro 低至 0.08），可显著降低多轮对话与重复前缀场景的额度。
- **自动转按量计费**：超出 PTU 额度或输入超过模型上限（千问 128K / DeepSeek 64K）时，请求自动转为按量计费，无需改代码。

响应字段用于识别计费与额度消耗：`service_tier`（`ptu-standard` 表示走 PTU 额度，`default` 或不返回表示按量）、`provisioned_tokens`（折算后实际消耗的额度 token）、`cached_tokens`（缓存命中数）。这些字段在 OpenAI Chat 兼容、OpenAI Responses、Anthropic 兼容、DashScope 四种格式下的 JSON 路径不同，需按对应协议读取。

> **注意**：Anthropic 兼容格式暂不返回 `cached_tokens`，只能通过 `provisioned_tokens` 间接判断缓存效果。此外长输入阶梯系数会使监控中的 PTU 利用率超过 100%，属于正常现象。

建议在创建或扩容前使用控制台**容量计算器**，根据 RPM、平均输入/输出长度、预估缓存命中率推荐输入/输出 TPM，避免额度不足导致意外的按量费用。

## 模型导入（LoRA）

若要部署自训练模型，需先通过[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)从 OSS 导入 LoRA 微调版本。核心要求与限制：

- **仅支持 LoRA**，不支持全参微调模型。
- **必需文件**：`adapter_model.safetensors`（权重）与 `adapter_config.json`（含 rank、alpha 等配置）。
- **rank 限制**：必须为 8、16、32 或 64 之一，且同一模型所有 LoRA 层使用相同 rank。
- **词汇表/对话模板**：若训练中新增 token、修改了 vocab 或 chat_template，则无法导入，须与开源基础模型完全一致。
- **VL 模型**：必须冻结 VIT，若 adapter 中包含 `visual` 开头的权重参数则无法导入。
- **OSS 前提**：Bucket 需添加 `bailian-datahub-access` 标签（标签值 `read`）；不支持访问 Bucket 根目录文件，须放在子目录；不支持归档类存储。首次导入需完成 OSS 服务关联角色授权（子账号还需主账号授予 `ram:CreateServiceLinkedRole` 权限）。

支持导入的基础模型涵盖千问3、千问3-VL、千问2.5、千问2.5-VL 系列。导入后模型状态包括创建中/创建成功（可部署）/创建失败/已失效。

## 使用 API / 命令行部署

[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)给出了完整流程（仅适用于华北2·北京地域，需先配置 `DASHSCOPE_API_KEY`）。部署接口统一为 `POST https://dashscope.aliyuncs.com/api/v1/deployments`，通过 `plan` 字段区分计费方式：

- **PTU**：`"plan": "ptu"`，配合 `ptu_capacity.input_tpm` / `output_tpm`。
- **模型单元**：`"plan": "mu"`，配合 `deploy_spec`（如 `MU1`）、`capacity`（副本数）、`enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit` 等。
- **按 Token（LoRA）**：`"plan": "lora"`，`capacity` 必填但设置无效，扩缩容需在控制台申请。

部署自定义模型时 `model_name` 使用**模型 ID**（在"我的模型"页面获取）。其余操作：

- **查询状态**：`GET /deployments/{deployed_model}`，`status` 为 `RUNNING` 表示部署完成。返回的 `deployed_model` 是专属服务唯一 ID。
- **推理**：通过 [DashScope SDK](../concepts/dashscope-sdk.md) 对专属服务发起请求（`Generation.call(model=...)`）。API Key 所在业务空间需与部署所在业务空间一致。
- **删除**：`DELETE /deployments/{deployed_model}`，立即下线且不可恢复，删除后停止计费。

> **注意**：执行部署命令后，即便未调用模型，服务在部署成功后即开始计费；建议先确认计费规则再部署。

**权限排查**：报错 `Workspace xxx does not have deployment privilege for model xxxx` 表示业务空间缺少该模型的部署授权，需在"业务空间管理 > 模型权限流控设置"中开启；报错 `Workspace access denied` 表示归属账号在该业务空间缺少操作权限。

**推理效果一致性**：从 OSS 导入的模型若与本地 vLLM/SGLang 推理结果不一致，通常是引擎默认参数差异所致，可将 `temperature`、`top_p`、`presence_penalty`、`repetition_penalty` 等设为对应框架默认值对齐。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


