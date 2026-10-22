# model production

`model production` 是百炼平台中模型从训练、优化、部署到服务化的核心流程，涵盖微调（Fine-tuning）、模型导入、压缩、吞吐预留及专属部署等关键能力。开发者可通过统一 API 体系完成端到端的模型定制与上线，支持文本、图像、视频、语音四大模态。所有生产环节均需在华北2（北京）地域调用，且依赖有效的 DashScope API Key 和对应权限配置。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持文本生成（SFT/CPT/DPO/LoRA）、图像生成（文生图/图生图）、视频生成（首帧/首尾帧）、语音合成（CosyVoice）四类任务。各模态使用独立的 `fine-tunes` 接口，但共用同一基础路径 `POST /api/v1/fine-tunes` [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型导入**：支持将 OSS 中的全参或 LoRA 微调模型文件导入平台，作为后续部署的输入源。当前仅在北京 Region 开放 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：通过量化技术降低自定义全参模型（如 `qwen3.5-flash-2026-02-23`）的显存占用与推理成本，暂不支持 LoRA 模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **吞吐预留（TPU/PTU）**：为已部署模型预购固定吞吐容量（input/output TPM），保障高并发下的低延迟与稳定性，支持 `ptu_fast`（高速）和 `ptu_default`（标速）两档性能 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **专属部署**：将微调/导入/压缩后的模型发布为在线 API 服务，支持 `mu`（模型单元）、`lora`（LoRA 共享）、`ptu`（吞吐预留）三种计费与资源模式。

> **注意**：文档 18（图像生成-部署模型）与文档 20（语音合成-部署模型）对 `plan` 参数的要求存在矛盾——前者明确推荐 `lora`，后者则强制要求 `mu`；实际部署时须严格依据模型类型选择：LoRA 微调产出的图像/视频模型应选 `lora`，而 CosyVoice 等语音模型因架构限制仅支持 `mu`。

## 关键参数

| 参数 | 所属环节 | 必填 | 说明 | 示例值 |
|------|----------|------|------|--------|
| `model_name` | 微调/部署/压缩 | 是 | 基础模型 ID 或微调产出模型 ID；部署时必须为 `finetuned_output` 字段值 | `qwen3-14b`, `wan2.7-i2v-ft-202511111122-xxxx` |
| `training_type` | 微调 | 是 | 微调方法；文本支持 `sft`/`cpt`/`dpo_full`/`dpo_lora`/`efficient_sft`；图像/视频/语音仅支持 `efficient_sft` | `sft`, `efficient_sft` |
| `n_epochs` / `max_steps` | 微调 | 是 | 文本/语音用 `n_epochs`，图像/视频用 `max_steps`；直接影响训练时长与费用 | 文本：`3`；图像：`800`；语音：`lm_max_epoch=60` |
| `plan` | 部署 | 是 | 部署方案：`mu`（专属资源）、`lora`（共享推理）、`ptu`（吞吐预留） | `lora`, `mu`, `ptu` |
| `ptu_capacity` | 吞吐预留 | 是 | 容量配置对象，含 `input_tpm` 和 `output_tpm`（单位：kTPM） | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` | `mu` 部署 | 是 | 模型单元规格，如 `MU1`/`MU5`/`MU2`；取值需与 `capacity` 匹配 | `MU5`（`capacity` 必须为 1 的倍数） |

## 使用方式

1. **微调训练**：  
   - 调用 `POST /api/v1/fine-tunes` 创建任务（如 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)）；  
   - 通过 `GET /api/v1/fine-tunes/{job_id}` 轮询状态，确认 `status=SUCCEEDED`；  
   - 从响应 `output.finetuned_output` 获取模型 ID。

2. **模型导入/压缩（可选）**：  
   - 导入：调用 `POST /api/v1/custom_models/import`，指定 OSS 路径与 `weight_type`（`full`/`lora`）；  
   - 压缩：先 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 提交任务，成功后取 `quantized_output`。

3. **部署服务**：  
   - 调用 `POST /api/v1/deployments`，传入 `model_name` 及对应 `plan`；  
     - `lora`：仅需 `model_name` + `plan=lora` + `capacity=1`；  
     - `mu`：必填 `deploy_spec`、`capacity`、`billing_method=POST_PAY`；  
     - `ptu`：需在 `ptu_capacity` 中明确 `input_tpm`/`output_tpm`。  
   - 轮询 `GET /api/v1/deployments/{deployed_model}` 直至 `status=RUNNING`。

4. **吞吐预留（独立于部署）**：  
   - 调用 `POST /api/v1/deployments`（同部署路径，但语义为预留），指定 `model_name`、`plan=ptu` 及 `ptu_capacity`，返回 `deployed_model` 即为预留标识。

## 限制和注意事项

- **地域强约束**：所有微调、导入、压缩、部署、吞吐预留 API **仅在华北2（北京）地域可用**，跨地域调用将失败；API Key 与地域绑定，不可复用 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型兼容性**：模型压缩仅支持 `qwen3.5-flash-2026-02-23` 的全参微调模型，LoRA 模型、其他版本或非百炼训练的模型均不支持 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **部署前验证**：部署前必须确保微调任务状态为 `SUCCEEDED`，否则部署会失败；图像/视频/语音部署文档均强调此前提 [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)。
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，实际结果需检查响应体中 `output.operation_status` 字段（可能为 `FAILED`）[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **限流与扩缩容**：部署后可通过 `GET /api/v1/deployments/{deployed_model}` 查询实时状态，并使用 `PATCH /api/v1/deployments/{deployed_model}` 修改 `capacity` 或限流参数（如 `rpm_limit`, `tpm_limit`），详见 [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [模型部署新 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-new-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)


