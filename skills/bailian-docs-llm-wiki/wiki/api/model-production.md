# model production

model production 是百炼平台面向模型全生命周期管理的核心能力集，覆盖模型调优、部署与吞吐资源预留等关键生产环节。它为开发者提供标准化 API 接口，支持从训练后优化到线上服务的端到端交付。所有功能均通过 RESTful API 调用，需配合有效的 API Key 与权限策略使用。

## 支持的模型/功能

- **模型调优（Fine-tuning）**：支持 Qwen 系列（Qwen2、Qwen2.5）、Baichuan2、GLM4 等主流开源模型的监督微调；暂不支持 Llama3 的 LoRA 全参数微调（仅支持 QLoRA）。  
- **模型部署（Deployments）**：支持将微调后模型或基础模型一键部署为 HTTP 可调用服务，自动分配 endpoint 并启用请求队列与健康检查。  
- **吞吐预留（Throughput Reservation）**：允许为指定 deployment 预留固定 QPS 容量，保障 SLA，适用于高优先级业务流量。相关能力详见 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen2-7b-chat` 或微调任务生成的 `ft-qwen2-7b-chat-20240512-abc123`；必须已在 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中成功完成并处于 `succeeded` 状态 |
| `instance_type` | string | 是 | 实例规格，当前仅支持 `gpu-a10` 和 `gpu-v100`；`gpu-a10` 为默认且推荐选项 |
| `max_concurrent_requests` | integer | 否 | 单实例最大并发请求数，默认值为 32；超过将触发排队，该参数影响吞吐预留配额计算 |

> **注意**：原始文档中 `instance_type` 列表曾包含 `cpu-small`，但该类型已于 v2.3.0 版本下线；实际调用时若传入将返回 `400 Bad Request` —— 请以 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 当前版本描述为准。

## 使用方式

1. **调优模型**：先通过 `POST /v1/fine_tuning_jobs` 提交微调任务（参见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)）；等待状态变为 `succeeded` 后获取 `fine_tuned_model_id`。  
2. **创建部署**：使用 `POST /v1/deployments`，传入 `model_id`（即上步所得 ID）、`instance_type` 等参数。  
3. **预留吞吐**（可选）：部署成功后，调用 `POST /v1/deployments/{deployment_id}/throughput_reservation` 设置 QPS 预留值；该操作不可逆，释放需手动删除 reservation 资源。

## 限制和注意事项

- 单个账号最多同时运行 5 个 active deployment；超出需先停用或删除旧实例。  
- 微调模型部署后，其底层镜像与权重只读，不支持运行时热更新；变更需重新提交微调任务并部署新实例。  
- 吞吐预留生效需 2–5 分钟，期间新请求仍按共享资源池调度；首次预留失败时，请确认对应 deployment 处于 `running` 状态（而非 `creating` 或 `failed`）。  
- 所有 API 均强制要求 `Content-Type: application/json`，且请求体必须为 UTF-8 编码 JSON；非标准格式将直接拒绝，不返回详细错误原因。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


