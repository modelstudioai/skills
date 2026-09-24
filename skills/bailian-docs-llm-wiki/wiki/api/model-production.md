# model production

model production 是百炼平台面向模型全生命周期管理的核心能力集，覆盖模型调优、部署与吞吐资源预留等关键生产环节。它为开发者提供标准化 API 接口，支持从训练后优化到线上服务的端到端交付。所有功能均通过 RESTful API 调用，需配合有效的 API Key 与项目权限使用。

## 支持的模型/功能

- **模型调优（Fine-tuning）**：支持 Qwen 系列（Qwen2、Qwen2.5）、Qwen-VL、Qwen-Audio 等开源基座模型的监督微调；暂不支持闭源商用模型（如 GPT、Claude）的微调 [模型生产](../../raw/model-api-reference/model-production.md)。  
- **模型部署（Deployments）**：支持将微调完成的模型或官方托管模型一键发布为可调用的 HTTP 服务，自动分配 endpoint 并启用请求路由、负载均衡与健康检查。  
- **吞吐预留（Throughput Reservation）**：允许为已部署的模型预购固定 QPS 配额，保障低延迟与高稳定性，适用于有 SLA 要求的生产场景 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen2-7b-chat` 或微调任务生成的 `ft-xxx` ID |
| `instance_type` | string | 是 | 实例规格，如 `gpu.a10.2xlarge`；必须与模型显存需求匹配，详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) |
| `max_concurrent_requests` | integer | 否 | 单实例最大并发请求数，默认值由实例类型决定，超限将触发排队或 429 响应 |
| `throughput_reservation_id` | string | 否 | 绑定已创建的吞吐预留 ID，用于保障该部署的最小可用 QPS |

## 使用方式

1. **调优 → 部署 → 预留** 为推荐流程：先通过 `/fine_tuning_jobs` 创建并等待训练完成，再以输出的 `fine_tuned_model_id` 调用 `/deployments` 创建服务，最后可选调用 `/throughput_reservations` 为其绑定配额。  
2. 所有 API 均需 `POST` 至 `https://dashscope.aliyuncs.com/api/v1/{resource}`，Header 中携带 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`。  
3. 部署成功后，`endpoint` 字段返回可直接调用的 HTTPS 地址，格式为 `https://dashscope.aliyuncs.com/api/v1/services/{service_id}/chat/completions`。

## 限制和注意事项

- 单个账号最多同时运行 5 个活跃微调任务；每个微调任务最多保留 90 天，超期后模型权重将被自动清理。  
- 部署实例一旦创建，`instance_type` 不可变更，如需升级需重建部署。  
- > **注意**：[模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档中列出的 `gpu.v100.2xlarge` 规格已于 v2.3.0 版本下线，当前仅支持 A10/A100/H100 系列，旧文档未同步更新。  
- 吞吐预留配额不可跨模型复用，且仅对绑定的 deployment 生效；若 deployment 被删除，预留配额不会自动释放，需手动调用 `/throughput_reservations/{id}/release`。  
- 微调任务失败时，错误码 `FT_JOB_FAILED` 对应的日志需通过 `/fine_tuning_jobs/{id}/events` 查询，原始日志中可能包含数据格式或 tokenization 异常详情 [模型生产](../../raw/model-api-reference/model-production.md)。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


