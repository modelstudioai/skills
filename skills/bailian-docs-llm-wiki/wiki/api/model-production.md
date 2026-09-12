# model production

model production 是百炼平台中用于将训练/调优后的模型投入实际服务的关键流程，涵盖[模型部署](../concepts/model-deployment.md)、资源预留（TPM）、以及生产环境下的生命周期管理。它通过统一的 OpenAPI 接口提供可编程控制能力，适用于需要稳定低延迟推理或批量任务调度的场景。该能力与 [模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning-jobs-api) 和 [模型部署](https://help.aliyun.com/zh/model-studio/deployments-api) 深度集成，构成端到端的 MLOps 闭环。

## 支持的模型与功能

- 支持所有已在百炼平台完成训练或微调的模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等），需先通过 [模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning-jobs-api) 生成 `fine_tuning_job_id` 或通过 [模型部署](https://help.aliyun.com/zh/model-studio/deployments-api) 创建 `deployment_id`
- 提供两种核心生产模式：
  - **TPM 预留模式**：为指定模型实例预分配推理吞吐量（TPM），保障 SLO，适用于高并发、低延迟场景  
  - **弹性部署模式**：基于请求自动扩缩容，按实际调用量计费，适合流量波动大的任务  
- 功能覆盖模型上线、灰度发布、版本回滚、监控指标订阅（如 p95 延迟、错误率）

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识（如 `qwen2-7b-instruct` 或微调后生成的 `ft-xxx`） |
| `deployment_id` | string | 否（TPM 模式必填） | 已创建的部署 ID，来自 [模型部署](https://help.aliyun.com/zh/model-studio/deployments-api) 接口响应 |
| `tpm_capacity` | integer | 否（TPM 模式必填） | 预留 TPM 值，最小 10，最大 10000；单位：tokens/minute |
| `instance_type` | string | 否 | 实例规格（如 `ecs.gn7i-c8g1.2xlarge`），默认由平台自动匹配最优 GPU 类型 |

> **注意**：`instance_type` 在 [TPM 预留 DashScope OpenAPI 接口文档](https://help.aliyun.com/zh/model-studio/tpm-reserved-openapi) 中被标记为“推荐指定”，但实测若不传值，平台仍可成功创建实例；该行为与 [模型部署](https://help.aliyun.com/zh/model-studio/deployments-api) 文档中“`instance_type` 为必填”的描述存在矛盾，请以实际 API 返回 `400` 错误为准，建议显式传入。

## 使用方式

1. **准备模型资源**：确保模型已完成训练或微调，并获取 `model_id`（参考 [模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning-jobs-api)）  
2. **创建部署（可选）**：如需复用已有部署配置，先调用部署接口生成 `deployment_id`（见 [模型部署](https://help.aliyun.com/zh/model-studio/deployments-api)）  
3. **发起生产请求**：向 `/v1/model-productions` 发送 `POST` 请求，携带上述关键参数  
4. **轮询状态**：通过 `GET /v1/model-productions/{production_id}` 查询 `status` 字段（`creating` → `active` → `failed`）  

示例请求体（TPM 模式）：
```json
{
  "model_id": "ft-abc123",
  "tpm_capacity": 500,
  "instance_type": "ecs.gn7i-c8g1.2xlarge"
}
```

## 限制和注意事项

- 单账号最多同时运行 5 个 active 的 model production 实例（含 TPM 与弹性模式）  
- TPM 模式下，`tpm_capacity` 修改需先停用再更新，不支持热变更  
- 所有 model production 实例默认启用自动日志采集（含输入/输出 token 数、耗时），日志保留 7 天  
- 若使用微调模型，必须确保其 `status` 为 `succeeded`，否则创建失败 —— 此约束在 [原文标题](../../raw/model-api-reference/model-production.md) 中未明确说明，但实测报错 `model_not_ready`，请务必校验微调作业状态  
- 资源释放需显式调用 `DELETE /v1/model-productions/{production_id}`；未释放的实例将持续计费  
- 当前不支持跨地域迁移 production 实例，且 [原文标题](../../raw/model-api-reference/model-production.md) 中列出的外部链接（如 DashScope TPM 文档）仅适用于旧版 DashScope 用户，百炼新用户应优先使用本平台原生 `/v1/model-productions` 接口 —— 此差异已在 [原文标题](../../raw/model-api-reference/model-production.md) 的链接注释中隐含提示，但未作显式区分

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)



