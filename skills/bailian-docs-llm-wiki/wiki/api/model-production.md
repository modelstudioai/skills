# model production

model production 是百炼平台中用于将训练/调优后的模型投入实际服务的关键能力集合，涵盖吞吐预留、模型微调与在线部署三大核心环节。它面向需要稳定低延迟推理、定制化模型行为或规模化服务交付的开发者场景。所有功能均通过 RESTful API 提供，需配合百炼平台身份认证与资源配额使用。

## 支持的模型/功能

- **吞吐预留（Throughput Reservation）**：为指定模型实例预分配计算资源，保障 SLO（如 P95 延迟 ≤ 500ms），适用于高并发、低抖动要求的生产流量。  
- **模型调优（Fine-tuning）**：支持 LoRA 等轻量级参数高效微调，兼容 Qwen 系列、Llama 系列等主流开源基座模型；调优任务异步执行，结果生成可部署的新模型版本。  
- **模型部署（Deployments）**：将微调后模型或官方托管模型发布为 HTTPS 接口服务，支持自动扩缩容、灰度发布与健康探针配置。  
以上功能均在 [模型生产](../../raw/model-api-reference/model-production.md) 文档中统一归类说明。

## 关键参数

- `model_id`：必须为平台内已注册的模型标识（如 `qwen2-7b-instruct` 或用户微调任务生成的 `ft-xxx`）；非标准 ID 将返回 `404 Not Found`。  
- `throughput`（吞吐预留）：单位为 tokens/s，最小值为 100，最大值受账户配额限制；该参数定义的是**峰值 token 处理能力**，而非请求 QPS —— 实际并发请参考 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中的换算公式。  
- `fine_tuning_job_id`（调优）：仅在调用部署接口时用于绑定微调成果；若直接部署基础模型，则此字段不可填。  
- `instance_type`（部署）：目前仅支持 `gpu.a10.2xlarge` 和 `gpu.v100.2xlarge`，其他类型将被拒绝；详细规格说明见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

## 使用方式

1. **调优流程**：先提交 `POST /api/v1/fine_tuning_jobs` 创建任务（需提供训练数据集 ID 与超参），轮询 `GET /api/v1/fine_tuning_jobs/{id}` 直至状态为 `succeeded`；  
2. **预留吞吐**：调用 `POST /api/v1/throughput_reservations` 指定 `model_id` 与 `throughput`，获取 `reservation_id`；  
3. **部署服务**：`POST /api/v1/deployments` 中传入 `model_id`（可为微调产出 ID）、`reservation_id`（可选，但推荐绑定以保障性能）及 `instance_type`。  
> **注意**：[模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档中示例仍使用旧版 `POST /v1/models/{model_id}/deploy` 路径，该路径已于 v2.3 版本废弃，请务必使用 `/api/v1/deployments` 新接口。

## 限制和注意事项

- 单账户最多同时运行 5 个微调任务；单个任务最大训练时长为 72 小时，超时自动终止。  
- 吞吐预留资源按小时计费，即使无请求也持续扣费；释放前需先删除关联的部署实例。  
- 部署服务默认启用 TLS 1.2+，不支持 HTTP 明文访问；自定义域名需额外配置 CNAME 与证书。  
- 微调任务输出的模型**不可直接用于吞吐预留**，必须先完成部署步骤生成服务实例；该约束在 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 的“后续操作”章节中有明确说明。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


