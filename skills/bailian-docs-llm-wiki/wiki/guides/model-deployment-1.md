# model deployment 1

模型部署让你为平台预置模型或调优后的自定义模型获得独立、资源专享的推理服务，以满足高并发、低延迟等生产需求。本页汇总三种计费方式的选型、PTU 长输入与前缀缓存机制、LoRA 模型导入约束，以及通过控制台或 API 完成部署的完整流程，面向需要落地专属推理服务的开发者。

## 三种计费方式与选型

百炼提供三种互斥的部署计费方式，计费方式在服务创建后无法更改，如需切换必须先下线已部署的模型再重新部署（详见 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)）：

- **预置吞吐（PTU，Provisioned Throughput Unit）**：平台预留资源保障特定 TPM 吞吐能力，额度内不限速。相比按 Token 计费，TPS 通常提升约 1.5～2.0 倍，适合流量可预估的高负载生产环境（智能客服、实时内容审核）。支持预付费（按天）与后付费（按小时），可自助增减吞吐量并设置自动续费。
- **模型单元（MU）**：按使用时长 × 模型单元数量计费，资源独占，延迟/吞吐等性能指标可自定义。支持部分预置模型与所有调优后模型，可自助增减模型单元数量，支持 PD 分离计算模式（拆分 Prefill 与 Decode 阶段以降低首 Token 延迟、提高吞吐）。
- **按 Token 使用量**：以每次调用的输入/输出 Token 计量，不使用不计费。仅支持对基础模型完成 SFT 高效训练后的自定义模型，主要用于调优后模型的效果验证；扩缩容需在控制台提交申请等待人工审核。

关键计费公式：

- 预置吞吐（按时长）：`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`
- 模型单元（按时长）：`费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价`；预付费按月时改为 `包月数 × 模型单元数量 × 月单价`
- 按 Token：`费用 = 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价`

## PTU 长输入与前缀缓存

PTU 部署支持长输入请求（部分模型最高 200K token）和前缀缓存，通过阶梯容量系数和缓存折扣管理额度消耗，详见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)：

- **长输入阶梯系数**：超过 32K token 的输入按更高阶梯系数折算 TPM。例如 glm-5.1 在 `[32K, 200K]` 区间输入系数为 1.33、输出为 1.17；deepseek-v4-pro 与 qwen3.7-plus-2026-05-26 无阶梯（1.0）。
- **前缀缓存折扣**：命中缓存的输入 token 按折扣系数消耗额度（glm-5.1 为 0.2，deepseek-v4-pro 为 0.08，qwen3.7-plus 为 0.2），可显著降低多轮对话和重复前缀场景的额度消耗。
- **自动转按量计费**：超出 PTU 额度或输入超过模型上限时，请求自动转为按量计费，无需修改调用代码，业务不中断。

API 响应关键字段：`service_tier`（值为 `ptu-standard` 表示使用 PTU 额度，`default` 或不返回表示按量计费）、`provisioned_tokens`（折算后实际消耗的额度 token 数）、`cached_tokens`（前缀缓存命中数）。不同 API 格式（OpenAI Chat / Responses、Anthropic、DashScope）下这些字段的 JSON 路径不同，需按对应格式取值。

> **注意**：模型输入上限存在两处口径。[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) 的价格表中千问系列多为 128K、部分新模型达 256K，而 PTU 文档明确将「千问 128K / DeepSeek 64K」作为触发自动转按量计费的上限。请以控制台实际展示与所选具体模型为准。

> **注意**：长输入场景下 PTU 利用率可能超过 100%，这是阶梯系数导致折算消耗高于原始 token 数的正常现象，超出部分自动转按量计费，不影响服务可用性。

## 模型导入（LoRA）

通过**我的模型**页面可将本地训练的 LoRA 模型从 OSS 导入百炼平台，详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。当前版本**仅支持 LoRA 模型，不支持全参微调模型**。

导入前提与约束：

- **OSS Bucket**：需为目标 Bucket 添加 `bailian-datahub-access` 标签（标签值 `read`）；不支持归档/冷归档类存储；不支持访问 Bucket 根目录文件，需放入子目录。首次导入需先完成 OSS 服务关联角色授权（子账号还需主账号授予 `ram:CreateServiceLinkedRole` 权限）。
- **必需文件**：`adapter_model.safetensors`（权重）与 `adapter_config.json`（含 rank、alpha 等配置）。
- **rank 限制**：必须为 8、16、32、64 之一，且同一模型所有 LoRA 层使用相同 rank。
- **词汇表与对话模板**：不得修改原始 vocab 或 chat_template，必须与开源基础模型默认配置一致，否则无法导入。
- **VL 模型**：必须冻结 VIT，若 adapter 中包含 `visual` 开头的权重参数则无法导入。

支持导入的基础模型涵盖千问3、千问3-VL、千问2.5、千问2.5-VL 系列的指定版本。导入后模型状态包括创建中、创建成功（可部署）、创建失败、已失效。

> **注意**：导入模型若与本地 vLLM/SGLang 推理效果不一致，通常是推理引擎参数默认值差异所致。可将 `temperature`、`top_p`、`repetition_penalty` 设为 1.0、`presence_penalty` 设为 0 以对齐 vLLM 默认行为。

## 使用 API/命令行部署

除控制台外，可通过 DashScope HTTP API 完成部署，**仅适用于华北2（北京）地域**，需先获取并配置 API Key，详见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。核心接口为 `POST/GET/DELETE https://dashscope.aliyuncs.com/api/v1/deployments`，通过 `plan` 字段区分计费方式：

- **PTU**：`plan: "ptu"`，配合 `ptu_capacity.input_tpm` / `output_tpm`。
- **模型单元**：`plan: "mu"`，配合 `deploy_spec`（如 `MU1`）、`capacity`（副本数）、`enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit`。
- **按 Token（LoRA 自定义模型）**：`plan: "lora"`，`capacity` 必填但设置无效，扩缩容需在控制台申请。

典型部署命令（模型单元）：

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

部署流程：创建部署 → 返回 `deployed_model`（专属服务唯一 ID）→ 轮询 `GET /deployments/{id}` 直到 `status` 为 `RUNNING` → 通过 DashScope SDK 或兼容 API 发起推理 → 不再使用时 `DELETE /deployments/{id}` 下线并停止计费。

## 部署配置与列表管理

在控制台部署时可配置：服务名称、选择模型、模型单元类型（部署规格）、部署副本数、部署模板（如「单机部署」，仅模型单元模式可用）、推理模式（Instruct 非思考 / Thinking 思考）、最长上下文、服务限流（RPM/TPM）。

部署列表页展示服务名称、模型名称、**模型 Code**（API 调用时指定模型的唯一标识）、部署状态（待部署、部署中、运行中、部署失败、下线中、已停止、变配中等）、计费方式、部署详情与限流详情。

## 限制与注意事项

- **计费不可逆变更**：计费方式创建后不可改；预付费按天/按月无法提前退费，首月内提前退订按日单价 1.2 倍计费。
- **部署即计费**：模型部署成功后即产生费用，即便尚未发起任何调用；后付费欠费后资源保留并继续计费 24 小时，超时后停止计费并删除底层资源（部署任务保留）。
- **按 Token 模式约束**：仅支持 LoRA 调优后模型，一个月内不使用将自动释放。
- **权限**：API 部署报错 `Workspace ... does not have deployment privilege` 或 `Workspace access denied` 时，需检查 API Key 归属业务空间的模型部署授权与账号操作权限。
- **删除不可恢复**：执行 DELETE 后服务立即下线且不可恢复。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)



