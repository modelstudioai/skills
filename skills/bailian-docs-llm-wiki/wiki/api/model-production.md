# model production

model production 是百炼平台面向模型全生命周期管理的核心能力集，覆盖模型调优、部署与吞吐资源预留等关键生产环节。它为开发者提供标准化 API 接口，支持从训练后优化到线上服务的端到端流程。所有功能均通过 RESTful API 调用，需配合有效的 API Key 与项目权限使用。

## 支持的模型/功能

- **模型调优（Fine-tuning）**：支持在百炼托管数据集或用户上传数据上对指定基础模型（如 Qwen 系列、Baichuan 系列）进行监督微调，输出可部署的定制化模型版本。  
- **模型部署（Deployments）**：支持将微调后模型或平台预置模型一键发布为高可用推理服务，自动分配 endpoint 并启用负载均衡。  
- **吞吐预留（Throughput Reservation）**：允许为已部署服务预先锁定 GPU 计算资源（如 vGPU 单位），保障低延迟与稳定 QPS，适用于有 SLA 要求的生产场景。  
以上能力详见 [模型生产](../../raw/model-api-reference/model-production.md) 文档的模块索引。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen2-7b-instruct` 或微调任务生成的 `ft-xxx` ID；必须已在 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中成功完成并进入 `succeeded` 状态。 |
| `instance_type` | string | 是 | 部署实例规格，如 `gpu.2xlarge`；需与吞吐预留中申请的 `resource_type` 严格一致，否则部署失败。 |
| `min_replicas` / `max_replicas` | integer | 否 | 自动扩缩容范围，默认为 `1/1`（固定单副本）；若已配置吞吐预留，则 `min_replicas` 必须 ≥ 预留资源所支持的最小副本数。 |

> **注意**：`instance_type` 在 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中定义为 `resource_type`，二者语义等价但字段名不一致——调用部署接口时务必使用 `instance_type`，调用吞吐预留接口时使用 `resource_type`，不可混用。

## 使用方式

1. **调优**：先通过 `/v1/fine_tuning_jobs` 创建任务，等待状态变为 `succeeded` 后获取 `fine_tuned_model_id`；  
2. **预留吞吐（可选）**：调用 `/v1/throughput_reservations` 预订资源，记录返回的 `reservation_id`；  
3. **部署**：向 `/v1/deployments` 提交请求，传入 `model_id`（即上步所得 ID）、`instance_type` 及其他参数；若需绑定预留资源，须在请求体中显式指定 `"throughput_reservation_id": "tr-xxx"`。  
完整交互流程与示例代码见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

## 限制和注意事项

- 单个账号最多同时运行 5 个活跃微调任务；  
- 已部署服务不可直接更换底层模型，需先删除再重建；  
- 吞吐预留资源按小时计费，即使未部署服务亦持续扣费，释放前请确认无关联 deployment；  
- 微调任务输出的模型仅可在同区域（Region）内部署，跨区域部署需重新微调或手动迁移——该约束在 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中明确说明，但部分旧版文档未强调，开发时务必校验 region 一致性。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


