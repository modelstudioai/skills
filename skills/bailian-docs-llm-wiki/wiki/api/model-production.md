# model production

model production 是百炼平台中用于将训练/调优后的模型投入实际服务的关键流程，涵盖[模型部署](../concepts/model-deployment.md)、资源预留（TPM）、以及生产环境下的生命周期管理。它通过统一的 OpenAPI 接口提供标准化能力，支持从模型上线到流量调度的全链路管控。开发者需结合 [模型生产](../../raw/model-api-reference/model-production.md) 文档理解整体能力边界。

## 支持的模型/功能

- 支持已通过 [模型调优](../../raw/model-api-reference/model-production.md) 完成 fine-tuning 的自定义模型（如 Qwen 系列 LoRA 微调模型）；
- 支持基础模型的直接部署（如 qwen-max、qwen-plus），无需前置调优；
- 提供 TPM（[Token](../concepts/token.md)s Per Minute）资源预留能力，保障推理稳定性，详见 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production.md)；
- 支持灰度发布、AB 测试、自动扩缩容（需配合弹性计算资源策略）。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，取值为调优任务输出的 `fine_tuned_model_id` 或官方模型名（如 `qwen-max`） |
| `tpm_capacity` | integer | 否 | 预留 TPM 上限，范围 100–100000；若不指定，则使用共享资源池（无 SLA 保障） |
| `replicas` | integer | 否 | 初始副本数，默认为 1；最大支持 10（受配额限制） |
| `timeout` | integer | 否 | 单次请求超时（秒），默认 60，最大 300 |

> **注意**：`tpm_capacity` 在部分旧版 SDK 中被误标为 `qps`，实际语义为 TPM（非 QPS），请以 [模型生产](../../raw/model-api-reference/model-production.md) 中的接口定义为准。

## 使用方式

1. **准备模型**：确保模型已完成调优并获取 `fine_tuned_model_id`，或确认目标基础模型已开通权限；
2. **创建部署**：调用 `POST /v1/deployments`，传入 `model_id` 和可选 `tpm_capacity`、`replicas`；
3. **验证状态**：轮询 `GET /v1/deployments/{deployment_id}`，待 `status == "running"` 后即可调用；
4. **发起推理**：使用部署生成的 `endpoint`，按标准 DashScope OpenAPI 格式发送请求（`Authorization: Bearer ${api_key}`）。

示例请求体：
```json
{
  "model_id": "ft-qwen-plus-20240510-123456",
  "tpm_capacity": 5000,
  "replicas": 2
}
```

## 限制和注意事项

- 单账号最多同时运行 5 个 active deployment（含 `running` 和 `pending` 状态）；
- `tpm_capacity` 设置后不可动态调整，如需变更须删除重建部署；
- 部署成功后，`model_id` 不可修改，但可通过更新 `replicas` 实现水平扩缩；
- 免费试用额度不覆盖 TPM 预留资源费用，相关计费规则参见 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production.md)；
- [模型部署](../concepts/model-deployment.md)失败常见原因：`model_id` 不存在、配额不足、地域不支持（当前仅 `cn-shanghai` 和 `cn-beijing` 可用）。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


