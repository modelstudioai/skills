# model production

`model production` 是百炼平台面向开发者提供的模型全生命周期管理能力集合，覆盖模型微调（Fine-tuning）、导入（Import）、压缩（Compression）、部署（Deployment）及吞吐预留（Throughput Reservation）等核心环节。所有能力均通过标准化 RESTful API 提供，支持自动化集成与规模化生产。

## 支持的模型/功能

百炼 `model production` 支持多模态模型的定制化生产流程：

- **文本生成**：支持 SFT、CPT、DPO、Efficient SFT 等微调方式，适用于 Qwen 系列大语言模型（如 `qwen3-14b`、`qwen3-32b`）；训练任务需在华北2（北京）地域执行 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **图像生成**：支持 `wan2.7-image-pro`、`qwen-image-2.0` 等模型的 LoRA 微调，仅限文生图（t2i）与图生图（i2i）两种模式 [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)。
- **视频生成**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview` 等图生视频模型，当前仅支持 `efficient_sft` 微调类型 [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)。
- **语音合成**：仅支持 `cosyvoice-v3-flash` 模型，采用双网络解耦微调（LM + FM），需分别配置两套超参数 [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)。
- **模型导入与压缩**：支持从 OSS 导入全参或 LoRA 模型文件，并对特定全参模型（如 `qwen3.5-flash-2026-02-23`）进行量化压缩以降低推理成本 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。

> **注意**：所有微调任务（文本/图像/视频/语音）均**仅在华北2（北京）地域开放**，且必须使用该地域的 API Key；其他地域用户需通过控制台操作，详见各文档适用范围说明。

## 关键参数

| 功能 | 关键参数 | 说明 | 约束 |
|------|----------|------|------|
| **微调通用** | `model`, `training_type`, `hyper_parameters` | `model` 为基准模型 ID；`training_type` 决定微调方法（如 `sft`, `dpo_lora`, `efficient_sft`）；`hyper_parameters` 必须包含 `n_epochs`/`max_steps`、`batch_size`、`learning_rate` 等核心字段 | `n_epochs` 影响计费，需根据数据量合理设置；`max_length` 超限数据将被丢弃 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md) |
| **吞吐预留（PTU）** | `plan=ptu`, `service_tier`, `ptu_capacity`, `charge_type` | `service_tier`: `ptu_fast`（高速）或 `ptu_default`（标速）；`ptu_capacity`: `{input_tpm, output_tpm}` 单位为 kTPM；`charge_type`: `pre_paid` 或 `post_paid` | `ptu_fast` 支持预/后付费；`ptu_default` 仅支持预付费，且支持 `Hour` 周期（`duration=8`）[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| **部署通用** | `model_name`, `plan`, `capacity`/`deploy_spec` | `model_name` 为微调产出或导入的模型 ID（非基础模型名）；`plan`: `mu`（模型单元）、`lora`（LoRA 共享）、`dtu`（独占吞吐）、`ptu_v2`（预置吞吐）；`capacity` 或 `deploy_spec` 因 plan 而异 | `lora` 部署推荐 `capacity=1`；`mu` 部署需匹配 `deploy_spec`（如 `MU5`）并满足 `capacity` 整数倍要求 [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md) |

## 使用方式

1. **准备阶段**  
   - 获取并配置华北2（北京）地域的 API Key（部分功能如 PTU 也支持新加坡地域）；
   - 确保子账号已授予 `AliyunBailianFullAccess` 或最小权限策略（含 `bailian:FineTune*`, `bailian:Deploy*`, `bailian:Compress*`）；
   - 数据集上传至 OSS 或通过文件管理 API 上传，获取 `file_id` 或 `storage_info`。

2. **微调/导入/压缩**  
   - 调用对应微调接口（如 `/api/v1/fine-tunes`）提交任务，记录返回的 `job_id`；
   - 轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，提取 `finetuned_output`；
   - 若需压缩，先调用 `/api/v1/fine-tunes/compress/templates` 查询模板，再创建压缩任务，成功后取 `quantized_output`。

3. **部署服务**  
   - 根据模型类型选择 `plan`：
     - 文本/图像/视频 LoRA 模型 → `plan=lora`，传 `capacity=1`；
     - CosyVoice 模型 → `plan=mu`，指定 `deploy_spec`（如 `MU5`）和 `capacity`；
     - 吞吐预留（PTU）→ `plan=ptu`，配置 `ptu_capacity` 和 `service_tier`；
     - DTU 独占部署 → `plan=dtu`，需使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）并传 `sku_code`/`template_code` [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)；
   - 调用 `POST /api/v1/deployments` 创建部署，轮询 `GET /api/v1/deployments/{deployed_model}` 直至 `status=RUNNING`。

4. **调用与管理**  
   - 使用 `deployed_model` 作为 ModelCode 调用推理 API；
   - 通过 `/api/v1/deployments` 系列接口扩缩容、修改限流、删除部署。

## 限制和注意事项

- **地域强约束**：所有微调（文本/图像/视频/语音）、Checkpoint 管理、模型导入、模型压缩 API **仅在华北2（北京）地域可用**；部署 API 中 `mu`/`dtu` 仅支持北京，`ptu_v2` 支持北京与新加坡 [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)。
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作即使返回 HTTP 200，仍需检查响应体中 `output.operation_status` 字段，`FAILED` 时需解析 `error_code` 和 `message` [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型标识混淆风险**：部署时 `model_name` 必须是微调产出的 `finetuned_output` 或导入/压缩后的 `model_name`，**不可直接使用基础模型名**（如 `qwen3-14b`）。错误使用将导致 `ModelNotFound` 错误。
- **DTU 特殊要求**：DTU 部署必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）和对应工作空间的 API Key，**不可使用 `dashscope.aliyuncs.com`**；且仅支持 `pre_paid`，续费需在控制台操作 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。
- **容量单位统一**：吞吐预留（PTU）与 DTU 的 `input_tpm`/`output_tpm` 均以 **kTPM（1000 Tokens/分钟）为单位**，非原始 TPM；配置时需换算（例如 5000 TPM = `input_tpm: 5`）。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
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
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)


