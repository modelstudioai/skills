# model deployment 1

百炼平台支持将预置模型或调优后的模型部署为资源专享的推理服务，提供预置吞吐（PTU）、模型单元、按 Token 用量三种计费方式，并支持通过控制台或 API 创建、查询、删除部署服务。本文汇总模型部署的计费规则、PTU 长输入与缓存能力、模型导入要求，以及 API/命令行快速部署流程。

## 计费方式

部署服务创建后，计费方式无法更改，如需切换必须先下线已部署的模型再重新部署。三种计费方式的对比如下，详细单价请参考 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

| 计费方式 | 适用场景 | 扩缩容方式 | 计费粒度 |
| --- | --- | --- | --- |
| 预置吞吐（PTU） | 高负载生产环境，需稳定吞吐、低延迟 | 自助增减吞吐量 | 按使用时长 + 输入/输出 TPM |
| 模型单元 | 私有模型部署，性能指标自定义，支持 PD 分离 | 自助增减模型单元数量 | 按使用时长 × 模型单元数量 |
| 按 Token 用量 | 调优后模型效果验证，不使用不计费 | 控制台提交申请，人工审核 | 按输入/输出 Token 数 |

PTU 模式下，当输入超过最长输入 Token 或购买的 TPM 量时，调用自动切换为按量付费模式，此时响应头会包含 `x-dashscope-ptu-overflow:true`。模型单元模式支持 PD 分离部署（Prefill/Decode 拆到不同节点），可降低首 Token 延迟、提高吞吐。按 Token 用量模式仅支持部分经过 LoRA 调优后的模型，且一个月内不使用将自动释放。

> **注意**：预付费 PTU 按天计费，无法提前退费；模型单元预付费首月内提前退订，日单价按 1.2 倍计费。

## PTU 长输入与缓存

PTU 部署支持长输入请求和前缀缓存，通过阶梯容量系数和缓存折扣管理额度消耗，详见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

- **长输入**：部分模型支持超过 32K token 的输入，超出部分按更高阶梯系数折算 TPM 消耗。例如 glm-5.1 在 [32K, 200K] 区间输入系数为 1.33、输出系数为 1.17。
- **前缀缓存**：命中缓存的输入 token 按折扣系数消耗额度（glm-5.1 为 0.2，deepseek-v4-pro 为 0.08，qwen3.7-plus-2026-05-26 为 0.2）。
- **自动转按量计费**：超出 PTU 额度或输入超过模型上限（千问 128K / DeepSeek 64K）时，请求自动转为按量计费，无需修改调用代码。

API 响应中通过以下字段标识计费方式：`service_tier`（值为 `ptu-standard` 表示使用 PTU 额度，`default` 或不返回表示按量计费）、`provisioned_tokens`（折算后实际消耗的 PTU 额度）、`cached_tokens`（前缀缓存命中的 token 数）。各字段在不同 API 格式（OpenAI Chat 兼容、OpenAI Responses、Anthropic 兼容、DashScope）下的 JSON 路径存在差异，Anthropic 兼容格式暂不返回 `cached_tokens`。

创建或扩容 PTU 部署前，建议在控制台的"容量计算器"中填写 RPM、平均输入/输出长度、预估缓存命中率，以评估额度需求，避免额度不足导致请求转为按量计费。

## 模型导入

部署调优后的 LoRA 模型前，需先将本地训练的模型从 OSS 导入到百炼平台，详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

导入前提条件：

- 已创建 OSS Bucket 并添加 `bailian-datahub-access` 标签（标签值为 `read`），不支持归档/冷归档/深度冷归档存储类型。
- 模型文件需直接放在 OSS Bucket 的子目录下（不支持访问根目录文件），导入后使用百炼提供的免费存储空间。
- 首次导入需主账号或子账号完成 OSS 服务关联角色授权（`AliyunServiceRoleForSFMDataHubOSSImport`）。

导入要求与限制：

- **必需文件**：`adapter_model.safetensors`（权重）和 `adapter_config.json`（配置）。
- **rank 限制**：rank 值必须为 8、16、32 或 64，且同一模型所有 LoRA 层使用相同 rank。
- **词汇表**：训练过程中添加新 token 或修改 vocab 的模型无法导入，必须与基础模型完全一致。
- **对话模板**：修改 `chat_template` 配置的模型无法导入，需与开源基础模型默认配置一致。
- **VIT 冻结**：VL 模型必须冻结 Vision Transformer 部分，若 adapter 中包含 `visual` 开头的权重参数则无法导入。

支持导入的基础模型包括千问3系列（32B/14B/8B/4B-Instruct-2507、千问3-VL-8B-Instruct）和千问2.5系列（72B/32B/14B/7B-Instruct、千问2.5-VL-72B/7B-Instruct）。

## API 部署流程

通过 API 或命令行部署模型适用于华北2（北京）地域，完整流程参考 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

### 1. 创建部署

调用 `POST https://dashscope.aliyuncs.com/api/v1/deployments`，通过 `plan` 字段指定计费方式：

- **PTU**：`plan=ptu`，需提供 `ptu_capacity.input_tpm` 和 `ptu_capacity.output_tpm`。
- **模型单元**：`plan=mu`，需提供 `deploy_spec`（如 `MU1`）、`capacity`（副本数），可选 `enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit`。
- **按 Token 用量**：`plan=lora`，`capacity` 参数设置无效但必须填写，扩缩容需在控制台提交申请。

返回结果中的 `deployed_model` 为专属服务的唯一 ID，后续查询、调用、删除均使用此 ID。

### 2. 查询状态

调用 `GET https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}`，当返回 `status` 为 `RUNNING` 时表示服务部署完成。其他状态包括 `PENDING`、`DELETING` 等。

### 3. 执行推理

部署完成后，使用 DashScope SDK 或 OpenAI 兼容接口调用，`model` 参数填入 `deployed_model`（专属服务 ID）。需确保 API Key 所在业务空间与模型部署所在业务空间相同。

### 4. 删除服务

调用 `DELETE https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}`，删除后服务立即开始下线且不可恢复，停止计费。

## 限制与注意事项

- **地域限制**：API 部署目前仅适用于华北2（北京）地域。
- **权限要求**：API Key 归属业务空间需拥有目标模型的部署权限（报错 `Workspace xxx does not have deployment privilege for model xxxx` 时需在业务空间管理中授权）；API Key 归属账号需在对应业务空间中拥有操作权限（报错 `Workspace access denied` 时需在权限管理中确认用户列表）。
- **计费生效**：部署成功后立即开始计费，即使未发起调用，建议先确认计费规则再执行部署。
- **模型单元资源**：后付费方式算力资源先到先得，购买不成功会全额退款。
- **欠费处理**：后付费账户欠费后，资源保留并计费 24 小时，期间服务可正常使用；超过 24 小时停止计费，底层资源将被删除但部署任务保留，补足欠费后重新分配资源。
- **效果一致性**：导入的 LoRA 模型在百炼平台推理效果可能与本地 vLLM/SGLang 不一致，建议调整 `temperature`（1.0）、`top_p`（1.0）、`top_k`（None 或 >100）、`presence_penalty`（0）、`repetition_penalty`（1.0）等参数对齐。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


