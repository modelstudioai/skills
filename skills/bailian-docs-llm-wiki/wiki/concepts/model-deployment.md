# 模型部署

模型部署是百炼平台将预置模型、微调模型或导入模型发布为在线推理服务的能力，使应用可通过统一接入点调用模型推理，满足高并发、低延迟的生产需求。本文相关能力仅适用于华北二（北京）地域。

## 在百炼场景中的使用

模型部署是「调优 → 压缩 → 部署」模型生产链路的最后一环：

- 接收**模型调优**产出的自定义微调模型，或**模型压缩**产出的低精度量化模型，部署为在线推理服务。
- 也支持将**从阿里云 OSS 导入的 LoRA 模型**部署上线（当前仅支持 LoRA，不支持全参微调模型导入）。
- 部署后获得可调用的接入点，应用通过 OpenAI Chat 兼容、OpenAI Responses、Anthropic 兼容或 DashScope 协议调用。

部署、查询、推理和删除全流程均可通过控制台或 API/命令行完成；模型压缩产出的模型在「我的模型」中单击「部署」即可上线，支持的部署规格由所选量化模板决定（如 MU5、MU8）。

## 计费方式

部署前可在模型部署控制台查看不同模型的预估每小时费用。计费方式在服务创建后无法更改，如需切换必须下线已部署模型后重新部署。三种计费方式：

| 计费方式 | 适用场景 | 计费依据 | 扩缩容 | 关键约束 |
| --- | --- | --- | --- | --- |
| 预置吞吐（PTU） | 高负载生产、稳定吞吐、低延迟 | 使用时长 × 预置吞吐 | 自助增减吞吐量 | 超额自动转按量计费；预付费无法提前退费 |
| 模型单元 | 资源独占、性能自定义、长时任务 | 使用时长 × 单元数 × 单价 | 自助增减单元数 | 后付费先到先得；首月内退订日单价按 1.2 倍计费 |
| Token 用量 | 调优效果验证、性价比优先 | 输入/输出 Token 数 × 单价 | 控制台提交申请，人工审核 | 仅支持部分 LoRA 调优模型；一个月不使用自动释放 |

PTU 模式相比按 Token 计费 TPS 通常提升约 1.5~2.0 倍；模型单元模式支持 PD 分离（Prefill 与 Decode 拆到不同节点，降低首 Token 延迟、提高吞吐）；按 Token 用量模式为「不使用不计费」。

## PTU 长输入与缓存

PTU 部署支持长输入和前缀缓存，通过阶梯容量系数和缓存折扣管理额度消耗：

- **长输入**：部分模型支持超过 32K token 的输入，超出部分按更高的阶梯系数折算 TPM 消耗。例如 `glm-5.1`（200K 上限，缓存折扣 0.2）：[0, 32K) 区间输入/输出系数均为 1.0，[32K, 200K] 区间输入 1.33 / 输出 1.17。
- **前缀缓存优惠**：命中缓存的输入 token 按折扣系数消耗额度，降低多轮对话和重复前缀场景的额度消耗。
- **自动转按量计费**：超出 PTU 额度或输入超过模型上限（千问 128K / DeepSeek 64K）时，请求自动转为按量计费，无需修改调用代码，响应头含 `x-dashscope-ptu-overflow:true`。

API 响应通过以下字段标识计费方式与额度消耗：

| 字段 | 说明 |
| --- | --- |
| `service_tier` | `ptu-standard` 表示使用 PTU 额度；`default` 或不返回表示按量计费 |
| `provisioned_tokens` | 折算后实际消耗的 PTU 额度 token 数（含阶梯系数和缓存折扣） |
| `cached_tokens` | 前缀缓存命中的 token 数 |

不同 API 格式下上述字段的 JSON 路径存在差异；Anthropic 兼容格式暂不返回 `cached_tokens`，可通过 `provisioned_tokens` 间接判断缓存效果。PTU 利用率在长输入场景下可能超过 100%（因阶梯系数使折算消耗高于原始 token 数），属正常现象。

## 模型导入（部署前置）

部署自定义 LoRA 模型前，需先将本地训练的 LoRA 模型从阿里云 OSS 导入到百炼。基础模型涵盖千问3 系列（32B/14B/8B/4B-Instruct-2507、千问3-VL-8B-Instruct）和千问2.5 系列（72B/32B/14B/7B-Instruct、千问2.5-VL-72B/7B-Instruct）。

导入前提与限制：

- **OSS Bucket**：需添加 `bailian-datahub-access` 标签（值为 `read`）；不支持归档/冷归档/深度冷归档存储；须选择子目录；支持内容加密和私有 Bucket。
- **必需文件**：`adapter_model.safetensors`（权重）与 `adapter_config.json`（配置）。
- **rank 限制**：rank 必须为 8、16、32 或 64，同一模型所有 LoRA 层 rank 值需一致。
- **词汇表与对话模板**：训练时添加新 token 或修改 vocab、修改 `chat_template` 的模型无法导入。
- **VIT 冻结**：VL 模型必须冻结 Vision Transformer，LoRA adapter 中包含 `visual` 开头的权重参数则无法导入。

首次从 OSS 导入需完成授权：主账号单击「前往授权」自动开通 OSS 服务关联角色（`AliyunServiceRoleForSFMDataHubOSSImport`）并为 Bucket 添加标签；子账号需主账号先在 RAM 控制台授予 `ram:CreateServiceLinkedRole` 权限。导入后模型状态包括创建中、创建成功（可部署）、创建失败、已失效。注意：导入模型在百炼推理的效果可能与本地使用 vLLM、SGLang 不一致。

## 来源文档

- 模型部署介绍（model-deployment-1/model-deployment-introduction.md）
- 预置吞吐长输入与缓存（model-deployment-1/ptu-long-input-and-cache.md）
- 模型导入（model-deployment-1/model-import.md）
- 模型压缩（model-compression/model-compression-introduction.md）
- 模型调优简介（fine-tune-text-generation-model/model-training-overview.md）
- 模型生产 API（model-api-reference/model-production/deployments-api.md）

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model compression](../guides/model-compression.md)
- [fine tuning](../guides/fine-tuning.md)


