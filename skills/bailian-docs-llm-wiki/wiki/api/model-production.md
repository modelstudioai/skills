# model production

model production 是百炼平台中用于将训练/调优后的模型投入实际服务的关键能力集，涵盖吞吐预留、模型微调与在线部署三大核心环节。它面向需要稳定推理性能、定制化模型行为及快速上线的开发者场景。所有功能均通过 RESTful API 提供，需配合平台身份认证与资源配额使用。

## 支持的模型/功能

- **吞吐预留（Throughput Reservation）**：为指定模型实例预分配 GPU 资源，保障最低 QPS 与低延迟，适用于流量可预期的生产负载。  
- **模型调优（Fine-tuning）**：支持 LoRA 等轻量级参数高效微调，当前仅限 `qwen-max`、`qwen-plus`、`qwen-turbo` 及部分开源基座模型（如 `llama3-8b-instruct`），详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。  
- **模型部署（Deployments）**：创建可独立访问的模型服务端点，支持自动扩缩容、A/B 测试与版本灰度，具体接口规范见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model_id` | 平台内唯一模型标识符，非 HuggingFace ID；调优任务与部署必须使用同一 `model_id` 的输出版本 | `"ft-qwen-turbo-20240510-123456"` |
| `throughput_reservation` | 吞吐预留配置对象，含 `min_replicas`、`max_replicas` 和 `target_qps_per_replica` | `{ "min_replicas": 1, "target_qps_per_replica": 5 }` |
| `fine_tuning_config` | 微调任务专属参数，包括 `training_file_id`、`lora_rank`、`epochs` 等 | `{ "lora_rank": 64, "epochs": 3 }` |

> **注意**：`model_id` 在 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中被定义为“部署时指定的模型别名”，但实际在部署 API 中要求其必须为微调任务生成的完整版本 ID（如 `ft-xxx` 格式），二者语义不一致，请以 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档为准。

## 使用方式

1. 提交微调任务：调用 `POST /v1/fine_tuning/jobs`，传入训练数据与 `fine_tuning_config`；  
2. 等待任务完成（状态变为 `succeeded`），获取输出 `model_id`；  
3. （可选）为该模型预留吞吐：调用 `POST /v1/throughput_reservations`，引用上一步的 `model_id`；  
4. 创建部署：调用 `POST /v1/deployments`，指定 `model_id` 与 `throughput_reservation`（若已配置）。  
全部操作均需携带 `Authorization: Bearer <api_key>` 与正确 `Content-Type: application/json`。

## 限制和注意事项

- 单个微调任务最大训练时长为 72 小时，超时自动终止；  
- 吞吐预留最小单位为 1 个 A10 GPU 实例，不支持跨机型混部；  
- 部署后模型不可直接修改 `model_id` 或基础架构，如需变更须重建部署；  
- 所有 API 均受账户级速率限制（默认 10 QPS），超出将返回 `429 Too Many Requests`；  
- 微调输入文件必须为 UTF-8 编码 JSONL，且每行 `messages` 字段需符合平台 schema —— 具体格式约束请严格参照 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


