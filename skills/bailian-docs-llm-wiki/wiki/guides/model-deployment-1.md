# model deployment 1

百炼平台提供模型部署功能，支持将预置模型或调优后的模型部署为独享推理服务，满足高并发、低延迟等不同业务需求。平台提供三种计费方式（预置吞吐 PTU、模型单元、Token 用量），并支持从 OSS 导入自训练的 LoRA 模型进行部署。本功能仅适用于华北二（北京）地域。

## 计费方式概览

百炼模型部署提供三种计费方式，适用于不同业务场景：

### 预置吞吐（PTU）

通过平台预留资源保障特定 TPM 吞吐能力，适用于流量稳定、需要保障并发体验的高负载生产环境。主要特点：

- 在保障额度内不限速，TPS 相比按 Token 计费通常提升约 1.5~2.0 倍
- 按使用时长和预置吞吐计费，支持后付费（按小时）和预付费（按天）
- 超出购买的 TPM 量时，自动切换为按量付费模式（API 响应头返回 `x-dashscope-ptu-overflow:true`）
- 预付费订单支付后实时生效，无法提前终止

PTU 部署还支持长输入请求和前缀缓存。部分模型（如 glm-5.1）支持超过 32K token 的输入，超出部分按阶梯系数折算 TPM 消耗。前缀缓存命中的 token 按折扣系数消耗额度（如 glm-5.1 为 20%、deepseek-v4-pro 为 8%），可降低多轮对话场景的成本。详见[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

### 模型单元

按使用时长与模型单元数量计费，资源独占，性能指标可自定义。主要特点：

- 支持后付费（按小时）和预付费（按月）
- 支持 PD 分离计算模式（将 Prefill 和 Decode 拆到不同节点执行，降低首 Token 延迟）
- 部署时可配置推理模式（Instruct / Thinking）、最长上下文、服务限流（RPM/TPM）
- 预付费首月内提前退订，日单价按 1.2 倍计费

### Token 用量

按模型输入和输出 Token 数量计费，仅支持部分经过 LoRA 调优后的模型，不使用不计费，适用于调优后模型的效果验证场景。

> **注意**：计费方式在服务创建后无法更改。如需切换，必须下线已部署的模型后重新部署。

## 支持的模型

PTU 和模型单元计费方式支持多种预置模型和调优后模型，涵盖以下系列：

- **千问系列**：qwen3.7-max、qwen3.7-plus、qwen3.6-flash/plus、qwen3.5-plus/flash 等多个版本
- **DeepSeek 系列**：deepseek-v4-flash、deepseek-v4-pro、deepseek-v3.2、deepseek-v3
- **多模态模型**：千问 VL 系列（qwen3-vl-plus、qwen3-vl-8b 等）、千问 Omni 系列
- **其他模型**：GLM-5/5.1、MiniMax-M2.5、Kimi-K2.5
- **语音合成**：CosyVoice-v3-flash

Token 用量计费仅支持部分千问和千问 VL 基础模型经 SFT 高效训练后的自定义模型。完整的模型列表和价格详见[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 部署方法

### 控制台部署

1. 前往[模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)
2. 填写服务名称，选择模型和计费方式，确认提交
3. 部署状态变为"运行中"即表示部署成功

### API / 命令行部署

通过 HTTP API 调用 `https://dashscope.aliyuncs.com/api/v1/deployments` 创建部署。不同计费方式的请求参数有所不同：

**PTU 部署**：指定 `plan: "ptu"`，配置 `ptu_capacity` 中的 `input_tpm` 和 `output_tpm`。

**模型单元部署**：指定 `plan: "mu"`，配置 `deploy_spec`（如 MU1）、`capacity`（副本数）、可选设置 `enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit`。

**Token 用量部署**：指定 `plan: "lora"`，仅支持调优后模型。

详细 API 用法和参数说明参见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 模型导入

百炼支持从阿里云 OSS 导入本地训练的 LoRA 模型。导入要求：

- 必需文件：`adapter_model.safetensors`（权重文件）和 `adapter_config.json`（配置文件）
- rank 值必须为 8、16、32 或 64
- 不支持修改过词汇表或 chat_template 的模型
- VL 模型必须冻结 VIT 部分
- 支持的基础模型包括千问3（32B/14B/8B/4B）、千问3-VL-8B、千问2.5（72B/32B/14B/7B）、千问2.5-VL（72B/7B）

首次导入需完成 OSS 授权并为目标 Bucket 添加 `bailian-datahub-access` 标签。详细操作步骤参见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## PTU 长输入与前缀缓存

PTU 部署的长输入按阶梯系数折算额度消耗：

| 模型 | 输入长度上限 | 缓存折扣 | 长输入阶梯系数 |
|------|-------------|---------|--------------|
| glm-5.1 | 200K | 0.2 | [32K, 200K] 区间输入 1.33 / 输出 1.17 |
| deepseek-v4-pro | 256K | 0.08 | 无阶梯（1.0） |
| qwen3.7-plus-2026-05-26 | 256K | 0.2 | 无阶梯（1.0） |

超出 PTU 额度或输入超过模型上限时，请求自动转为按量计费，无需修改调用代码。可通过控制台的容量计算器提前估算所需额度。

API 响应中通过 `service_tier`（值为 `ptu-standard` 表示使用 PTU）、`provisioned_tokens`（折算后额度消耗）、`cached_tokens`（缓存命中数）等字段标识计费状态。这些字段在 OpenAI Chat 兼容、OpenAI Responses、Anthropic 兼容、DashScope 四种 API 格式中的 JSON 路径有所不同，详见[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 部署管理

部署成功后可在部署列表页进行以下操作：

- **查看状态**：通过控制台或 API（`GET /api/v1/deployments/{deployed_model}`）查看服务运行状态
- **扩缩容**：PTU 自助增减吞吐量，模型单元自助增减副本数，Token 用量需提交申请
- **监控**：前往[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)查看 TPM 统计、PTU 利用率、缓存命中率等指标
- **删除服务**：通过控制台或 API（`DELETE /api/v1/deployments/{deployed_model}`）下线服务，操作不可恢复

## 常见问题

**部署时提示权限不足**：确认 API Key 的归属[业务空间](../concepts/workspace.md)拥有模型部署权限，且归属账号在该[业务空间](../concepts/workspace.md)中有操作权限。可在[业务空间](../concepts/workspace.md)管理页面的"模型权限流控设置"中检查和授权。

**导入模型与本地推理效果不一致**：百炼推理引擎参数默认值可能与 vLLM/SGLang 不同。建议在 API 调用时显式设置 `temperature=1.0`、`top_p=1.0`、`presence_penalty=0`、`repetition_penalty=1.0` 以对齐 vLLM 默认行为。

**PTU 利用率超过 100%**：部分模型的长输入阶梯系数使折算后消耗高于原始 token 数，超出部分自动转为按量计费，不影响服务可用性。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


