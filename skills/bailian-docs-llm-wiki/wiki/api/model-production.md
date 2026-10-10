# model production

model production 是百炼平台中用于将训练/调优后的模型投入实际服务的关键能力集合，涵盖吞吐预留、模型调优和模型部署三大核心环节。它面向需要稳定推理服务、定制化模型行为或规模化上线的开发者场景。所有功能均通过 RESTful API 提供，需配合百炼平台的身份认证与资源配额体系使用。

## 支持的模型/功能

- **吞吐预留（Throughput Reservation）**：为指定模型实例预分配 GPU 资源，保障低延迟与高并发下的服务稳定性，适用于 SLO 敏感型业务。  
- **模型调优（Fine-tuning）**：支持 LoRA 等轻量级参数高效微调方式，兼容 Qwen 系列、Qwen2 系列及部分开源基座模型（详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)）。  
- **模型部署（Deployments）**：支持一键创建可公网访问或 VPC 内网访问的模型服务端点，自动完成容器化、扩缩容配置与健康检查。该能力在 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中有完整接口定义。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model_id` | 百炼平台内注册的模型唯一标识（非 HuggingFace ID） | `qwen2-7b-instruct` |
| `throughput_type` | 吞吐预留类型，仅支持 `standard`（默认）或 `high`（需审批） | `standard` |
| `fine_tuning_method` | 调优方法，当前仅支持 `lora` | `lora` |
| `instance_type` | 部署所用实例规格，必须与模型显存需求匹配（如 `gpu-a10-24g`） | `gpu-a10-24g` |

> **注意**：`instance_type` 的可用值列表在 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中定义，但该文档未同步更新 2024 年 Q3 新增的 `gpu-v100-16g` 规格，实际可用性请以控制台或 `/v1/instance-types` 接口返回为准。

## 使用方式

1. **准备阶段**：确保模型已上传并注册至百炼模型仓库（参见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中的前置要求）；  
2. **调优（可选）**：提交 `POST /v1/fine_tuning_jobs` 请求，指定训练数据集与超参；  
3. **部署**：调用 `POST /v1/deployments`，传入 `model_id` 及 `instance_type`；若需保障性能，建议先调用 `POST /v1/throughput_reservations` 预留资源；  
4. **验证**：通过返回的 `endpoint_url` 发起 `POST /v1/chat/completions` 测试请求。

## 限制和注意事项

- 单个账号最多同时运行 5 个吞吐预留实例（含不同模型），超出需提工单申请扩容；  
- 模型部署后默认开启自动扩缩容（1–10 实例），若需固定实例数，须在创建时显式设置 `min_instances = max_instances`；  
- 所有调优任务日志保留 7 天，部署实例状态变更事件保留 30 天，历史记录需通过 API 主动拉取；  
- > **注意**：[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中描述的 `auto_renew` 字段已废弃，新版 API 不再支持自动续订，预留到期前 24 小时将触发站内信告警。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


