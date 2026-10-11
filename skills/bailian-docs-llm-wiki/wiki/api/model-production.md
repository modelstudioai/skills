# model production

model production 是百炼平台中用于将训练/调优后的模型投入实际服务的关键能力集合，涵盖吞吐预留、模型微调与在线部署三大核心环节。它为开发者提供从模型优化到稳定推理的端到端生产链路支持，所有操作均通过 RESTful API 实现。该能力依赖于百炼统一的模型生命周期管理框架，需配合 [模型生产](../../raw/model-api-reference/model-production.md) 主文档中的权限与资源约束使用。

## 支持的模型/功能

- **吞吐预留（Throughput Reservation）**：为指定模型实例预分配 GPU 资源与 QPS 保障，适用于高 SLA 场景；详见 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)  
- **模型调优（Fine-tuning）**：支持 LoRA 等轻量级微调方式，兼容 Qwen、Qwen2、Qwen2.5 系列及部分开源 LLM；调优任务通过异步作业提交，结果生成新模型版本；参考 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)  
- **模型部署（Deployment）**：将微调后模型或基础模型发布为可调用的 HTTP 接口，支持自动扩缩容与灰度发布；部署配置独立于训练流程，需显式指定 `model_id` 和 `instance_type`

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen2-7b-instruct` 或微调任务生成的 `ft-xxx` ID；必须已在平台注册或由调优任务产出 |
| `instance_type` | string | 是 | 实例规格，当前仅支持 `gpu-a10`、`gpu-v100`、`gpu-a100`；不支持 CPU 实例部署 |
| `throughput_reservation_id` | string | 否 | 绑定已创建的吞吐预留 ID，用于保障最低并发能力；若未提供，则按共享资源池调度 |
| `max_replicas` | integer | 否 | 部署最大副本数，默认为 1；设为 0 表示禁用自动扩缩容 |

> **注意**：`instance_type` 在 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中允许 `gpu-a10` 和 `gpu-a100`，但 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 当前对 `gpu-a100` 的支持仍处于灰度阶段，正式环境建议优先选用 `gpu-a10`，避免部署失败。

## 使用方式

1. **调优模型**：调用 `/v1/fine_tuning/jobs` 创建微调任务，等待 `status == "succeeded"` 后获取输出 `model_id`  
2. **（可选）预留吞吐**：调用 `/v1/throughput_reservations` 创建预留，记录返回的 `throughput_reservation_id`  
3. **部署服务**：调用 `/v1/deployments` 提交部署请求，传入 `model_id`、`instance_type` 及可选的 `throughput_reservation_id`  
4. **验证接口**：部署成功后，通过 `GET /v1/deployments/{deployment_id}/status` 确认状态为 `running`，再调用其 `endpoint` 发起推理  

所有 API 均需携带 `Authorization: Bearer <api_key>`，且请求体为 JSON 格式。

## 限制和注意事项

- 单个账号最多同时运行 5 个活跃部署（`status == running`），超出需先删除或停用旧部署  
- 微调任务生成的模型仅可在同一 Region 内部署，跨 Region 需重新调优或导出导入  
- 吞吐预留资源不可跨模型复用；一个 `throughput_reservation_id` 仅能绑定至单个部署  
- 部署启动后，`model_id` 和 `instance_type` 不可修改；如需变更，须重建部署  
- 所有模型生产操作均受项目配额限制，具体额度请查阅 [模型生产](../../raw/model-api-reference/model-production.md) 中的配额章节

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


