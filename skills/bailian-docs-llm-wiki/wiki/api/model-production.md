# model production

model production 是百炼平台中用于将训练/调优后的模型投入实际服务的关键流程，涵盖[模型部署](../concepts/model-deployment.md)、资源预留（TPM）、以及生产环境下的生命周期管理。它通过统一的 OpenAPI 接口提供自动化能力，支持从模型上线到扩缩容的全链路管控。该能力与 [模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning-jobs-api) 和 [模型部署](https://help.aliyun.com/zh/model-studio/deployments-api) 深度集成，是 MLOps 实践的核心环节。

## 支持的模型与功能

- 支持所有已完成训练或调优的百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等），需已通过 [模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning-jobs-api) 或 [模型部署](https://help.aliyun.com/zh/model-studio/deployments-api) 流程生成有效模型 ID。
- 提供三大核心功能：  
  - **TPM 预留**：为部署实例预分配吞吐量配额（Transactions Per Minute），保障 SLA；  
  - **灰度发布**：支持按流量比例分发请求至新旧版本；  
  - **自动扩缩容**：基于实时 TPM 指标动态调整实例数（需开启 `auto_scaling_enabled: true`）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 百炼平台内唯一模型标识，来自 [模型部署](https://help.aliyun.com/zh/model-studio/deployments-api) 创建的 deployment 或 [模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning-jobs-api) 输出的 fine-tuned model ID |
| `tpm_reserved` | integer | 否 | 预留 TPM 值，范围 10–10000；若未指定，则使用默认共享队列（无 SLA 保障） |
| `version_alias` | string | 否 | 自定义别名（如 `"prod-v2"`），用于灰度路由；同一 `model_id` 下不可重复 |
| `auto_scaling_enabled` | boolean | 否 | 默认 `false`；设为 `true` 时需同时配置 `min_instances` / `max_instances` |

> **注意**：原始文档 [模型生产 (raw/model-api-reference/model-production.md)](../../raw/model-api-reference/model-production.md) 中列出的 TPM 预留文档链接指向 DashScope OpenAPI，但百炼平台 model production 的 TPM 参数实际由百炼专属 `/v1/model-productions` 接口处理，**不兼容 DashScope 的 `/api/v1/services/...` 路径**。请以 [模型生产 (raw/model-api-reference/model-production.md)](../../raw/model-api-reference/model-production.md) 中的接口定义为准，而非外部链接。

## 使用方式

1. **创建生产实例**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/model-productions \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model_id": "qwen-max-20240601-001",
           "tpm_reserved": 500,
           "version_alias": "stable",
           "auto_scaling_enabled": true,
           "min_instances": 1,
           "max_instances": 4
         }'
   ```
2. **查询状态**：  
   `GET /v1/model-productions/{production_id}` 返回 `status` 字段（`pending` / `running` / `failed`）及当前 `actual_tpm`。
3. **更新配置**：  
   仅支持修改 `tpm_reserved`、`version_alias` 和扩缩容参数；不可变更 `model_id`。详见 [模型生产 (raw/model-api-reference/model-production.md)](../../raw/model-api-reference/model-production.md)。

## 限制和注意事项

- 单个 `model_id` 最多关联 5 个 active production 实例（含不同 `version_alias`）；
- `tpm_reserved` 修改后生效延迟 ≤ 60 秒；实例数变更延迟 ≤ 120 秒；
- 灰度发布期间，`version_alias` 为 `"stable"` 的实例始终接收至少 10% 流量，避免零流量切流；
- 若模型未通过 [模型部署](https://help.aliyun.com/zh/model-studio/deployments-api) 完成服务化封装，直接调用 model production 接口将返回 `400 InvalidModelId`。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


