# model production

model production 是百炼平台中用于将训练/调优后的模型投入实际服务的关键流程，涵盖[模型部署](../concepts/model-deployment.md)、资源预留（TPM）、以及生产环境下的生命周期管理。它通过统一的 OpenAPI 接口提供自动化能力，支持从模型版本发布到高可用服务上线的端到端操作。开发者需结合 [模型调优](../../raw/model-api-reference/model-production.md) 和 [模型部署](../../raw/model-api-reference/model-production.md) 文档完成完整链路。

## 支持的模型/功能

- 支持已通过 [模型调优](../../raw/model-api-reference/model-production.md) 生成的 fine-tuned 模型（如 Qwen 系列 LLM 微调版本）直接部署为 API 服务；
- 支持基础模型（如 qwen-max、qwen-plus）的按需部署与 TPM 预留部署两种模式；
- 提供模型版本管理、灰度发布、自动扩缩容（基于 QPS/TPM 阈值）等生产级功能。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，可为系统预置模型 ID（如 `qwen-max`）或微调任务产出的 `ft-xxx` ID |
| `deployment_type` | string | 是 | 取值 `on_demand` 或 `tpm_reserved`；后者需配合 `tpm_capacity` 使用 |
| `tpm_capacity` | integer | 否（仅 `tpm_reserved` 时必填） | 预留 TPM 值，最小 100，最大 100000 |
| `replicas` | integer | 否 | 实例副本数，默认 1；`on_demand` 模式下该参数被忽略 |

> **注意**：`tpm_capacity` 的单位是 *tokens per minute*，非请求 QPS；其计算逻辑与输入/输出总 token 数强相关，具体换算请参考 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production.md) 中的公式说明。

## 使用方式

1. 调用 `POST /v1/deployments` 创建部署（需携带上述关键参数）；
2. 部署成功后，返回 `endpoint` 和 `deployment_id`，后续推理请求发往该 endpoint；
3. 可通过 `GET /v1/deployments/{deployment_id}` 查询状态，`status: "active"` 表示就绪；
4. 更新配置（如扩缩容）需调用 `PATCH /v1/deployments/{deployment_id}`。

## 限制和注意事项

- 单账号最多同时运行 20 个 active deployment（含 `on_demand` 和 `tpm_reserved`）；
- `tpm_reserved` 部署创建后不可降配 `tpm_capacity`，仅支持升配或重建；
- 微调[模型部署](../concepts/model-deployment.md)前，必须确保其状态为 `succeeded` 且已通过模型校验（详见 [模型调优](../../raw/model-api-reference/model-production.md) 返回的 `validation_status` 字段）；
- `on_demand` 模式存在冷启动延迟（通常 < 3s），不适用于超低延迟敏感场景。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


