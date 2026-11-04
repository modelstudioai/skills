# model production

model production 是百炼平台提供的模型服务工业化能力集合，涵盖模型调优、部署与吞吐预留三大核心环节，面向需要稳定、可控、可扩展模型服务的生产场景。所有能力均通过 RESTful API 提供，支持细粒度资源控制与异步任务管理。开发者需结合具体模型类型与业务负载特征选择合适的能力组合。

## 支持的模型/功能

- **模型调优（Fine-tuning）**：支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Baichuan2、GLM4 等开源基座模型的监督微调；暂不支持闭源模型（如 GPT 系列）或非文本模态模型的微调。  
- **模型部署（Deployments）**：支持将微调后模型或官方托管模型以 HTTP 服务形式发布为独立 endpoint，提供自动扩缩容、健康检查与流量灰度能力。  
- **吞吐预留（Throughput Reservation）**：为已部署的模型实例预分配 GPU 资源配额，保障 P95 延迟与并发稳定性，适用于高 SLA 要求场景。  
以上能力均在 [模型生产](../../raw/model-api-reference/model-production.md) 文档中统一归类说明，其子模块细节见对应 API 参考页。

## 关键参数

- `model_id`：必须为平台内已注册模型 ID（如 `qwen2-7b-instruct`），不可使用 HuggingFace 模型路径；微调任务中该字段指向基座模型。  
- `instance_type`：部署与吞吐预留共用规格标识（如 `gpu-a10-2x`），需与目标模型显存需求匹配；不匹配将导致创建失败，详见 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中的规格对照表。  
- `max_tokens` / `temperature` 等推理参数仅在调用部署后的 endpoint 时生效，**不参与部署或微调任务创建**——此行为与部分旧版文档描述存在差异，> **注意**：[模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中“创建时可设默认 temperature”的示例已过时，实际须在 inference 请求头中传入。

## 使用方式

1. **调优**：先调用 `/fine_tuning_jobs` 创建任务，指定训练数据集 ID 与 `model_id`；任务完成后获取 `finetuned_model_id`。  
2. **部署**：用上一步的 `finetuned_model_id` 或官方模型 ID 调用 `/deployments` 创建服务；成功后返回 `endpoint_id` 与访问 URL。  
3. **预留吞吐**：对已存在的 `deployment_id` 调用 `/throughput_reservations` 分配资源，支持按小时计费的弹性预留。  
完整流程与各步骤的请求体/响应结构，请参考 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 和 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的 API 示例。

## 限制和注意事项

- 单个微调任务最大训练时长为 72 小时，超时自动终止；数据集大小上限为 10 GB（压缩后）。  
- 部署实例默认保留 30 天，到期未续期将自动下线；可通过 `auto_restart` 参数启用自动续期（需账户余额充足）。  
- 吞吐预留与部署实例绑定，**不可跨 deployment 共享**；若需多 endpoint 共享资源，须分别创建预留并聚合监控——该约束在 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中有明确说明。  
- 所有 API 均要求 `Authorization: Bearer <api_key>`，且 `X-Timeout-Seconds` 请求头最大值为 300（5 分钟），长任务请使用异步轮询模式。

## 来源文档

- [模型生产](../../raw/model-api-reference/model-production.md)


