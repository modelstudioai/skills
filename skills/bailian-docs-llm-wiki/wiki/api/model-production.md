# model production

`model production` 是百炼平台面向模型全生命周期的生产级能力集合，覆盖模型微调、压缩、部署与吞吐预留四大核心环节。开发者可通过统一 API 体系完成从定制训练到高可用服务上线的端到端流程，所有操作均需在指定地域（主要为华北2北京）使用对应工作空间的 API Key 进行鉴权。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类模态。文本生成支持 `sft`/`dpo_full`/`dpo_lora` 等训练类型；图像/视频/语音仅支持 `efficient_sft`（LoRA 高效微调）[文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 调优模型文件导入平台，导入后可直接部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参调优模型进行量化压缩，不支持 LoRA 模型或已量化模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **部署（Deployment）**：支持多种计费与资源模式：
  - `lora`：LoRA 共享部署，按 Token 用量后付费（适用于图像/视频生成）；
  - `mu`：模型单元部署，支持 `MU2`/`MU5` 规格（语音合成必需）；
  - `dtu`：独占吞吐（预付费），需通过业务空间专属域名调用；
  - `ptu_v2`：预置吞吐（预/后付费），支持北京与新加坡地域。

## 关键参数

| 功能 | 关键参数 | 说明 |
|--------|-----------|------|
| **微调通用** | `model`, `training_type`, `hyper_parameters` | `model` 必须为平台支持的基础模型 ID 或已有调优模型 ID；`hyper_parameters` 中 `n_epochs`/`batch_size`/`max_length`（文本）、`max_steps`（图像）、`n_epochs`（视频）、`lm_max_epoch`/`fm_max_epoch`（语音）均为必填项，直接影响训练时长与费用。 |
| **吞吐预留（PTU）** | `plan=ptu`, `service_tier`, `ptu_capacity`, `charge_type` | `service_tier` 取值 `ptu_fast`（高速，默认）或 `ptu_default`（标速）；`ptu_capacity` 单位为 kTPM（1000 Tokens/分钟）；`ptu_default` 标速支持 `Hour`（8 小时时段）与 `Day` 周期，`ptu_fast` 仅支持 `Day` [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。 |
| **部署通用** | `model_name`, `plan`, `capacity`/`deploy_spec` | `model_name` 必须为微调产出的 `finetuned_output` 或导入模型的 `model_name`；`capacity` 用于 `lora`/`mu` 部署；`deploy_spec`（如 `MU5`）与 `capacity` 配合用于语音合成部署。 |

> **注意**：文档 16 与文档 26 对 DTU 部署的域名要求存在表述差异——前者强调“DTU 部署的 API 请求需使用部署所在业务空间的 `maas.aliyuncs.com` 域名”，后者进一步明确“DTU 部署仅支持预付费（`charge_type="pre_paid"`）”，而文档 16 的示例请求体中未显式包含 `charge_type` 字段，易引发遗漏。实际调用必须传入 `charge_type: "pre_paid"`，否则请求将失败。

## 使用方式

1. **准备环境**：  
   - 仅华北2（北京）地域全面支持微调、导入、部署及压缩 API；新加坡仅支持 PTU 部署。  
   - 配置 `DASHSCOPE_API_KEY` 环境变量，并确保其与目标工作空间及地域绑定。  
   - 子账号需授予 `AliyunBailianFullAccess` 或最小化权限策略（含 `bailian:CreateFineTuningJob`, `bailian:CreateDeployment`, `bailian:DescribeDeployments` 等）。

2. **典型流程**：  
   ```mermaid
   graph LR
   A[创建微调任务] --> B[轮询查询 status=SUCCEEDED]
   B --> C[获取 finetuned_output]
   C --> D[部署模型]
   D --> E[轮询 deployed_model status=RUNNING]
   E --> F[调用服务]
   ```
   - 微调任务：调用 `POST /api/v1/fine-tunes`，响应中提取 `job_id` 后轮询 `/api/v1/fine-tunes/{job_id}`。  
   - 部署模型：根据模态选择对应部署接口（如文本用 `model-deployment-text-generation-api`），传入 `finetuned_output` 作为 `model_name`，`plan` 按需选 `lora`/`mu`/`dtu`。  
   - 查询状态：使用 `GET /api/v1/deployments/{deployed_model}`，当 `output.status == "RUNNING"` 时表示就绪。  

3. **吞吐预留（PTU）独立流程**：  
   - 调用 `POST /api/v1/deployments`（基础路径），`plan="ptu"`，配置 `ptu_capacity` 与 `pre_paid_info` 或 `charge_type="post_paid"`。  
   - 创建成功后，返回的 `deployed_model` 即为模型调用标识（ModelCode），无需额外部署步骤。

## 限制和注意事项

- **地域强约束**：微调、模型导入、Checkpoint 管理、模型压缩、绝大多数部署 API **仅在北京地域可用**；跨地域调用将返回 403 错误。  
- **API Key 绑定性**：API Key 与工作空间及地域严格绑定，不可复用；DTU 部署必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）及对应空间的 Key。  
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，必须检查响应体中 `output.operation_status` 是否为 `"SUCCEEDED"`，否则容量未生效 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。  
- **模型兼容性**：  
  - CosyVoice 语音合成模型部署**仅支持 `mu` plan**，且必须指定 `deploy_spec`（如 `MU5`）与匹配的 `capacity`（如 `MU5` 要求 `capacity` 为 1 的整数倍）；  
  - 图像/视频生成部署推荐 `plan="lora"`，但 `lora` 不支持语音合成；  
  - 模型压缩当前**仅限 `qwen3.5-flash-2026-02-23` 全参调优模型**，其他模型调用会返回 `MODEL_NOT_SUPPORTED` 错误。  
- **数据安全**：OSS 挂载需提前完成百炼平台授权；上传至 OSS 的模型文件需符合格式规范（如 LoRA 权重结构），校验失败将导致导入任务 `FAILED`。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)


