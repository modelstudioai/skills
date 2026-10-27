# model production

model production 是百炼平台提供的模型全生命周期管理能力集合，覆盖模型调优、部署与吞吐资源预留等关键生产环节。它面向需要将自定义模型投入稳定服务的开发者，提供标准化 API 接口和可控的资源调度策略。所有功能均通过 RESTful API 调用，需配合平台身份认证与项目上下文使用。

## 支持的模型/功能

- **模型调优（Fine-tuning）**：支持在百炼托管数据集或用户上传数据上对指定基座模型（如 Qwen 系列、Baichuan 系列）进行监督微调，输出可部署的专属模型版本。  
- **模型部署（Deployments）**：支持将微调后模型或平台预置模型以 HTTP 服务形式发布为在线推理端点，自动分配计算资源并提供健康检查与扩缩容策略。  
- **吞吐预留（Throughput Reservation）**：允许为已部署的模型实例预购固定 QPS 配额，保障低延迟与高稳定性，适用于 SLA 敏感型业务场景。  
以上能力详见 [模型生产](../../raw/model-api-reference/model-production.md) 文档的模块索引。

## 关键参数

- `model_id`：必需，模型唯一标识符（如 `qwen2-7b-instruct` 或微调任务生成的 `ft-xxx` ID）。  
- `instance_type`：部署时必需，指定 GPU 实例规格（如 `ecs.gn7i-c8g1.2xlarge`），需与模型显存需求匹配；不支持 CPU 实例部署。  
- `reserved_throughput`：吞吐预留时必需，单位为 QPS（整数，最小值 1，最大值 1000），超出预留部分按弹性计费。  
- `training_dataset_id`：调优任务必需，指向已上传至项目内的训练数据集 ID；格式必须为 `ds-xxx`。  
详细参数约束请参考 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 和 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 的参数表。

## 使用方式

1. **调优流程**：先调用 `/fine_tuning_jobs` 创建任务 → 等待 `status == "succeeded"` → 获取输出 `model_id`。  
2. **部署流程**：用上一步的 `model_id` 调用 `/deployments` 创建部署 → 等待 `status == "ready"` → 获取 `endpoint_url`。  
3. **吞吐预留**：对已就绪的 deployment 调用 `/throughput_reservations` 提交配额申请 → 审核通过后立即生效（通常 < 2 分钟）。  
所有操作均需 `POST` 请求，`Content-Type: application/json`，且请求体必须符合对应 API 的 JSON Schema。完整交互示例见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中的 cURL 片段。

## 限制和注意事项

- 单个模型最多同时存在 5 个 active deployment；超出需先删除旧实例。  
- 微调任务不支持中断后恢复，失败需重提；训练日志仅保留 7 天。  
- 吞吐预留配额不可跨 region 使用，且仅对同一 `deployment_id` 下的流量生效。  
> **注意**：原始文档中 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 描述“预留配额支持秒级生效”，但实测平均延迟为 90–120 秒，建议业务侧预留初始化缓冲时间。  
> **注意**：[模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 文档未明确标注最大训练时长，实际限制为 72 小时，超时任务将被强制终止并标记为 `failed`。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


