# model production

`model production` 是百炼平台面向模型全生命周期的生产级能力集合，覆盖模型微调、压缩、导入、部署及吞吐预留等关键环节。所有能力均通过统一 OpenAPI 接口提供，支持开发者在生产环境中构建、优化和规模化运行定制化模型服务。核心流程为：训练（fine-tuning）→ 优化（compression/import）→ 部署（deployment）→ 保障（throughput reservation）。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成四类任务，对应不同基准模型与训练范式：
  - 文本生成：支持 `qwen3-*` 系列，训练类型包括 `sft`、`dpo_full`、`dpo_lora` 等 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)；
  - 图像生成：仅支持 `wan2.7-image-pro`、`qwen-image-2.0` 等万相/千问图像模型，训练类型固定为 `efficient_sft`；
  - 视频生成：支持 `wan2.7-i2v`、`wan2.5-i2v-preview` 等，训练类型同样限定为 `efficient_sft`；
  - 语音合成（CosyVoice）：仅支持 `cosyvoice-v3-flash`，采用双网络（LM + FM）解耦训练 [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)。

- **模型优化**：
  - **压缩（Quantization）**：仅支持基于 `qwen3.5-flash-2026-02-23` 的**全参调优模型**，LoRA 模型不支持 [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)；
  - **导入（Import）**：支持从 OSS 导入全参（`full`）或 LoRA（`lora`）调优模型文件，需提前完成 OSS 授权与文件上传 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。

- **部署（Deployment）**：支持四类模态模型的在线服务发布，但部署方案因模型类型而异：
  - 文本/语音模型：支持 `mu`（模型单元）、`lora`（共享）、`ptu`（吞吐预留）三种 plan；
  - 图像/视频模型：当前仅推荐 `lora` 方案（文档明确标注“LoRA高效微调推荐为`lora`”），`mu` 和 `ptu` 未在对应部署文档中列出。

> **注意**：多份文档（[图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)、[视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)、[语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)）均强调部署 API **仅在华北2（北京）地域可用**，但[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)明确支持多地域（如弗吉尼亚 `us-east-1`）。这意味着 `ptu` 部署能力与地域强绑定，而其他部署方式暂不支持跨地域。

## 关键参数

| 参数 | 所属场景 | 必填性 | 说明 |
|------|----------|--------|------|
| `model_name` | 微调、部署、导入 | 是 | 微调时为基础模型 ID；部署/导入时为待操作模型 ID（如 `qwen3-14b` 或 `wan2.7-i2v-ft-xxx`） |
| `training_type` | 微调 | 是 | 文本支持 `sft`/`dpo_lora` 等；图像/视频/语音均强制为 `efficient_sft` |
| `hyper_parameters` | 微调 | 条件必填 | 包含 `n_epochs`/`batch_size`/`max_length`（文本）、`max_steps`（图像）、`n_epochs`（视频）、`lm_max_epoch`（语音）等，具体字段依模型类型而异 |
| `plan` | 部署 | 是 | `mu`（专属资源）、`lora`（共享推理）、`ptu`（吞吐预留）；语音模型仅支持 `mu`，图像/视频仅推荐 `lora` |
| `deploy_spec` | 部署（`mu` 时） | 是 | 如 `MU1`、`MU5`；语音模型明确要求 `MU5` 或 `MU2` [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md) |
| `ptu_capacity` | 部署（`ptu` 时） | 否（默认 10k/1k） | `{ "input_tpm": 10000, "output_tpm": 1000 }`，单位为 kTPM（1000 [Token](../concepts/token.md)s/分钟） |
| `capacity` | 部署（`mu`/`lora` 时） | 是 | `mu` 时为资源单元数（需满足 `base_capacity` 倍数）；`lora` 时为实例数（推荐 1） |

## 使用方式

1. **微调训练**：  
   调用 `POST /api/v1/fine-tunes` 创建任务，指定 `model`、`training_type` 和 `hyper_parameters`。任务状态需轮询 `GET /api/v1/fine-tunes/{job_id}` 查询，成功后获取 `output.finetuned_output` 作为模型 ID。

2. **模型优化（可选）**：  
   - **压缩**：先 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 提交任务，轮询至 `SUCCEEDED` 后取 `quantized_output`；  
   - **导入**：`POST /api/v1/custom_models/import` 提交 OSS 路径，轮询至 `SUCCESSED` 后取 `output.model_name`。

3. **模型部署**：  
   调用 `POST /api/v1/deployments`，根据模型类型选择 `plan` 并传入对应参数（如 `deploy_spec`+`capacity` for `mu`，或 `capacity` for `lora`）。部署状态通过 `GET /api/v1/deployments/{deployed_model}` 轮询，`status: RUNNING` 表示就绪。

4. **吞吐预留（PTU）**：  
   作为独立资源层，通过 `POST /api/v1/deployments`（同部署接口但 `plan=ptu`）创建预留容量，返回 `deployed_model`（即 ModelCode）用于后续模型调用。其扩缩容、续订等操作均围绕该 ModelCode 进行 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

## 限制和注意事项

- **地域限制**：微调、导入、部署（除吞吐预留外）所有 API **仅支持华北2（北京）地域**，必须使用该地域的 API Key 和 Endpoint；吞吐预留支持多地域（如 `us-east-1`），但需匹配工作空间地域。
- **模型兼容性**：  
  - 模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参调优模型，LoRA 模型和已量化模型明确不支持；  
  - 语音合成模型（CosyVoice）部署**仅支持 `mu` plan**，不支持 `lora` 或 `ptu`；  
  - 图像/视频模型部署文档未提及 `mu`/`ptu`，实践中应优先使用 `lora`。
- **参数校验**：HTTP 200 不代表操作成功。吞吐预留接口返回 `output.operation_status` 可能为 `FAILED`，必须检查该字段及 `error` 信息 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)；部署接口同理，需确认 `output.status` 为 `RUNNING`。
- **计费提示**：`n_epochs`、`max_steps`、`batch_size` 等超参数直接影响训练费用；`ptu` 容量购买后立即计费，即使未调用；`mu` 部署成功即开始计费，与调用无关。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)


