# model deployment 1

阿里云百炼平台的**模型部署**功能为预置模型和调优后的模型提供独立的、资源专享的推理服务，用于满足高并发、低延迟或自定义性能指标的业务需求。当前模型部署**仅适用于"中国内地（北京）"地域**，计费方式在服务创建后无法更改，需要切换时必须先下线已有部署再重新创建。部署的完整简介、模型清单和计费细则见 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 三种计费方式对比

部署时需要在三种计费方式中选择其一，它们分别面向不同的负载形态：

| 计费方式 | 计费单元 | 适用场景 | 支持的模型范围 | 扩缩容 |
| --- | --- | --- | --- | --- |
| 预置吞吐（PTU） | 输入/输出 TPM × 时长 | 高并发、可预估流量、需要稳定吞吐保障（如智能客服、内容审核） | 部分预置模型 | 自助增减 TPM |
| 模型单元（MU） | 模型单元数量 × 时长 | 自定义性能指标、资源隔离、长时任务、私有模型（如电商微调模型、分子筛选） | 部分预置模型 + 所有调优后模型 | 自助增减 MU 数量 |
| 按 Token 使用量 | 输入/输出 Token 数 | 调优后低成本验证、对并发和延迟不敏感 | 部分经过 LoRA 调优后的模型 | 需提交工单人工审核 |

> **注意**：PTU 和 MU 的后付费/预付费一旦下单即生效，即便没有调用也会产生费用；Token 使用量模式不使用不计费。

### 预置吞吐（PTU）

- 后付费按小时计费，预付费按天计费；预付费订单到期后延后 2 小时停服，资源保留 14 小时后释放。
- 当输入超过最长 Token 或超出购买的 TPM 量时，调用会自动切换为按量付费模式，API 返回 Header 中会带 `x-dashscope-ptu-overflow:true`，同时推理性能可能下降。
- 预付费订单支付后无法提前终止，也无法提前退费。

### 模型单元（MU）

- 后付费按小时，预付费包月；首月内提前退订日单价按 1.2 倍计费。
- 后付费算力"先买先得"，购买不成功会全额退款。
- 支持配置：推理模式（Instruct / Thinking）、最长上下文、RPM/TPM 限流，部分模型还支持 PD 分离模式（Prefill/Decode 拆分到不同节点，用于降低首 Token 延迟）。

### 按 Token 使用量

- 仅支持部分基础模型经 SFT 高效训练后得到的自定义模型，且一个月内不使用会自动释放。
- `capacity` 参数虽然必须填写但实际无效，扩缩容需在控制台提交申请。

## 支持的模型概览

模型部署覆盖以下系列（具体到每个模型代码、最长输入 Token 和单价请以官方价格表为准）：

- **千问（Qwen）**：千问 3/3.5/3.6/3.7 系列的 Max、Plus、Flash 等预置模型；千问 3/2.5 开源版（1.7B / 4B / 8B / 14B / 32B / 72B / 235B-A22B / 397B-A17B 等）；千问 3-Embedding、千问 3-Rerank、千问 3-MoE-Rerank。
- **千问 VL / Omni**：千问 3-VL 系列（2B / 4B / 8B / 32B / 235B-A22B，含 Instruct 和 Thinking）、千问 VL-Max、千问 VL-OCR、千问 3.5-Omni-Flash/Plus、CosyVoice 语音合成。
- **DeepSeek**：DeepSeek-v3 / v3.2 / v4-Pro / v4-Flash。
- **其他**：GLM-5 / GLM-5.1 / GLM-4.7、MiniMax-M2.5、Kimi-K2.5。

> **注意**：不同计费方式支持的模型清单并不完全重合。例如 PTU 仅覆盖部分预置模型，而 Token 使用量模式仅适用于部分基础模型的 LoRA 调优版本，部署前需要在[模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)核对具体模型的可用计费方式。

## 部署方法

部署可以通过控制台或 API 完成。完整的 API 部署流程（含部署、查询状态、推理、删除）见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

### 控制台部署

1. 前往[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)。
2. 选择模型、计费方式，按需调整模型单元规格、推理模式、最长上下文、RPM/TPM 限流等参数。
3. 部署状态变为"运行中"即表示成功；从此刻起开始计费。

### API 部署

调用 `https://dashscope.aliyuncs.com/api/v1/deployments`，关键字段：

- `model_name`：预置模型填模型代码；调优后的自定义模型填模型 ID（在"模型调优 → 产出 → 我的模型"中查看）。
- `plan`：`ptu` / `mu` / `lora`（分别对应三种计费方式）。
- PTU 模式需指定 `ptu_capacity.input_tpm` 与 `output_tpm`。
- MU 模式需指定 `deploy_spec`（如 `MU1`）、`capacity`、可选 `enable_thinking` / `max_context_length` / `rpm_limit` / `tpm_limit`。
- LoRA 模式 `capacity` 必填但无效，扩缩容走控制台工单。

部署成功后返回的 `deployed_model` 字段即为该专属服务的唯一 ID，也是后续调用时 `model` 参数应填的值（**不是**原始 `model_name`）。

### 调用已部署的模型

支持 OpenAI 兼容、DashScope、Assistant SDK 三种协议；需要保证 API Key 所在的[业务空间](../concepts/workspace.md)与部署所在[业务空间](../concepts/workspace.md)一致，否则会报错 `Workspace access denied` 或 `does not have deployment privilege`。

## 导入自定义 LoRA 模型

如果要部署的模型是本地训练的 LoRA，需要先从 OSS 导入到百炼。完整限制条件和主/子账号授权流程见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

### 前提

- OSS Bucket 已创建并添加了 `bailian-datahub-access=read` 标签；不支持归档/冷归档/深度冷归档类型，不支持直接访问根目录下的文件。
- 已完成服务关联角色授权（主账号直接确认；子账号需要主账号先授予 `ram:CreateServiceLinkedRole` 权限）。

### 文件要求

- 必须包含 `adapter_model.safetensors` 和 `adapter_config.json`。
- `rank` 必须是 8 / 16 / 32 / 64 之一，且同一模型所有 LoRA 层 rank 必须一致。
- **不允许**修改词汇表（vocab）、修改 `chat_template`、或未冻结 VL 模型的 VIT 部分（`adapter_model.safetensors` 中不能出现 `visual.*` 键）。

### 当前支持导入的基础模型

- 千问 3：32B / 14B / 8B / 4B-Instruct-2507
- 千问 3-VL：8B-Instruct
- 千问 2.5：72B / 32B / 14B / 7B-Instruct
- 千问 2.5-VL：72B / 7B-Instruct

> **注意**：当前版本**只支持 LoRA**，不支持全参微调模型。如需部署全参模型，请使用 MU 或 PTU 方式部署平台预置模型。

## 限制与常见问题

- **地域限制**：所有部署能力仅限北京地域。
- **计费方式锁定**：创建后不可更改，切换必须下线重建。
- **权限报错**：`Workspace xxx does not have deployment privilege for model xxxx` 需要在[业务空间](../concepts/workspace.md)"模型权限流控设置"中给模型开启部署授权；`Workspace access denied` 需要检查 API Key 归属账号在该业务空间的成员权限。
- **推理效果与本地不一致**：通常由采样参数差异导致。推荐将 `temperature=1.0`、`top_p=1.0`、`top_k=None 或 >100`、`presence_penalty=0`、`repetition_penalty=1.0` 对齐 vLLM 默认值。
- **欠费处理**：后付费欠费后资源保留并继续计费 24 小时，之后自动释放。
- **Token 用量模式自动释放**：一个月内无调用会自动释放，需重新部署。

## 来源文档

- [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


