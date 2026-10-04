# model production

model production 是百炼平台中用于将训练/调优后的模型投入实际服务的关键能力集，涵盖吞吐预留、模型调优和模型部署三大核心环节。它面向需要稳定推理服务、定制化模型行为或规模化上线的开发者场景。所有功能均通过 RESTful API 提供，需配合百炼认证体系使用。

## 支持的模型/功能

- **吞吐预留（Throughput Reservation）**：为指定模型实例预分配计算资源，保障低延迟与高并发稳定性，适用于 SLO 敏感型业务。  
- **模型调优（Fine-tuning）**：支持 LoRA 等轻量级参数高效微调，当前仅限 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类基础模型（详见 [模型生产](../../raw/model-api-reference/model-production.md)）。  
- **模型部署（Deployments）**：可将调优后模型或官方托管模型发布为独立 endpoint，支持自定义名称、版本标签及流量灰度策略。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen-max` 或调优任务生成的 `ft-xxx` ID；必须已在 [模型生产](../../raw/model-api-reference/model-production.md) 中注册并完成状态校验 |
| `throughput` | integer | 否（吞吐预留必填） | 预留 QPS，取值范围 1–1000；单位为每秒请求数，超出将触发限流 |
| `fine_tuning_job_id` | string | 否（调优任务必填） | 来自 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 创建的作业 ID，格式为 `ftj-xxxx` |
| `deployment_name` | string | 是（部署时） | 全局唯一，仅支持小写字母、数字和连字符，长度 3–32 字符 |

> **注意**：`model_id` 在 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中被定义为 `model` 字段，而 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档中统一使用 `model_id` —— 实际请求体中请始终使用 `model_id`，`model` 字段已废弃，避免兼容性问题。

## 使用方式

1. **调优模型**：先调用 `/fine_tuning_jobs` 创建任务（参考 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)），等待 `status == "succeeded"`；  
2. **预留吞吐**（可选）：对目标模型（含调优后模型 ID）调用 `/throughput_reservations` 预分配资源；  
3. **部署服务**：向 `/deployments` 提交 `model_id`（可为原始模型或 `ft-xxx`）、`deployment_name` 等参数，获取 `endpoint_url`。

所有接口均需在请求头携带 `Authorization: Bearer <api_key>`，且 `Content-Type: application/json`。

## 限制和注意事项

- 单个账号最多同时运行 5 个活跃调优任务；  
- 吞吐预留最小单位为 1 QPS，但实际生效需模型实例处于 `ready` 状态（可通过 `/deployments/{id}/status` 查询）；  
- 调优模型部署后不支持直接修改 base model，如需切换需新建部署；  
- 所有模型生产操作均受项目配额约束，超限将返回 `429 Too Many Requests`；详情见 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 的配额章节。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


