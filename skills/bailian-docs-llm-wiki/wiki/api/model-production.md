# model production

model production 是百炼平台中用于将训练/调优后的模型投入实际服务的关键流程，涵盖[模型部署](../concepts/model-deployment.md)、资源预留（TPM）、以及生产环境下的生命周期管理。它通过统一的 OpenAPI 接口提供标准化能力，支持从模型版本发布到高可用服务上线的完整链路。开发者需结合 [模型生产](../../raw/model-api-reference/model-production.md) 文档理解整体架构与接口边界。

## 支持的模型/功能

- 支持已发布的模型版本（含通过 [模型调优](../../raw/model-api-reference/model-production.md) 生成的微调模型）进行服务化部署；
- 提供 TPM（[Token](../concepts/token.md)s Per Minute）资源预留能力，保障推理吞吐稳定性，详见 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production.md)；
- 支持灰度发布、流量切分、自动扩缩容（需配合集群配置），但不支持直接部署本地 PyTorch 模型文件（仅支持百炼托管的模型版本）。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 百炼平台内模型唯一标识（如 `qwen-max-20240815`），必须为已发布的模型版本 ID |
| `tpm_capacity` | integer | 否 | 预留 TPM 值，范围 100–100000；若不指定，则使用共享资源池，无 SLA 保障 |
| `replicas` | integer | 否 | 初始副本数，默认为 1；最大值受项目配额限制 |
| `endpoint_type` | string | 否 | 取值 `public`（公网可访问）或 `private`（VPC 内网），默认 `public` |

> **注意**：`model_id` 不接受 Hugging Face 模型 ID 或自定义路径格式；该约束在 [模型部署](../../raw/model-api-reference/model-production.md) 中明确，但部分旧版 SDK 示例误传 `hf://...` 格式，实际会返回 `InvalidModelId` 错误。

## 使用方式

1. 确保目标模型已完成发布（可通过控制台或 `POST /api/v1/models/{model_id}/publish` 调用）；
2. 调用 `POST /api/v1/deployments`，传入上述关键参数；
3. 部署成功后，获取返回的 `endpoint_url`，该地址即为生产调用入口（如 `https://dashscope.aliyuncs.com/api/v1/services/xxx`）；
4. 所有请求需携带 `Authorization: Bearer <api_key>`，且 `Content-Type: application/json`。

## 限制和注意事项

- 单个部署实例最大支持 `replicas=20`，超出需提工单申请配额扩容；
- TPM 预留生效需 3–5 分钟，期间请求可能被限流，建议在业务低峰期操作；
- 部署后不支持动态修改 `tpm_capacity`，如需调整，必须先删除再重建部署（[模型部署](../../raw/model-api-reference/model-production.md) 明确此行为）；
- 公网 endpoint 默认启用 DDoS 防护与 WAF 规则，若出现 403 错误，请检查请求头是否含非法字段（如 `X-Forwarded-For` 伪造）。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


