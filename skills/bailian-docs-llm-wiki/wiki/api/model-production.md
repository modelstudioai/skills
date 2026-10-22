# model production

`model production` 指在百炼平台完成模型的全生命周期管理，涵盖微调训练、压缩优化、导入部署及吞吐预留等关键环节。该流程面向开发者提供标准化 API 接口，支持文本、图像、视频、语音四类生成式模型的定制化生产与高性能推理服务交付。

## 支持的模型/功能

百炼 `model production` 当前支持以下模型类型与核心功能：

- **微调训练**：覆盖文本生成（SFT/CPT/DPO）、图像生成（LoRA）、视频生成（首帧/首尾帧图生视频）、语音合成（CosyVoice）四大模态。所有微调任务均**仅限华北2（北京）地域**调用，且必须使用该地域的 API Key [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型压缩**：支持对 `qwen3.5-flash-2026-02-23` 全参微调模型进行量化压缩，降低显存占用并提升吞吐，但 LoRA 模型和已量化模型不支持 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **模型导入**：支持从 OSS 导入全参或 LoRA 类型的自定义模型，导入后可直接部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型部署**：支持将微调产出、导入或压缩后的模型发布为在线 API 服务，适配文本、图像、视频、语音四类模型，但部署接口同样**仅限华北2（北京）地域** [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)。
- **吞吐预留（TPU/PTU）**：为部署的模型预置稳定推理吞吐能力，支持 `ptu_fast`（高速）与 `ptu_default`（标速）两种性能档位，容量单位为 kTPM（1000 [Token](../concepts/token.md)s/分钟）。

> **注意**：文档中多处声明“仅在华北2（北京）地域可用”，但[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)明确指出其支持弗吉尼亚（`us-east-1`）等地域的 Endpoint，且工作空间专属域名格式包含 `{region}` 变量。此处存在地域支持范围矛盾，实际使用请以各接口文档标注的适用地域为准，吞吐预留功能不受“仅北京”限制。

## 关键参数

| 功能 | 关键参数 | 说明 | 约束/示例 |
|------|----------|------|-----------|
| **微调训练** | `training_type` | 微调方法。文本支持 `sft`/`dpo_full`/`efficient_sft`；图像/视频/语音当前**仅支持 `efficient_sft`**（LoRA） | 文本生成示例中 `n_epochs`、`batch_size`、`max_length` 为必填超参；视频生成中 `n_epochs` 与 `batch_size` 共同决定总步数，需确保 `steps ≥ 800` |
| | `model` | 基准模型 ID。如 `qwen3-14b`、`wan2.7-image-pro`、`cosyvoice-v3-flash` | 不同模态支持的模型列表见对应文档，不可混用 |
| **模型部署** | `plan` | 部署方案。`mu`（模型单元）、`lora`（LoRA共享）、`ptu`（吞吐预留） | 图像/视频生成推荐 `lora`；语音合成（CosyVoice）**仅支持 `mu`**；`ptu` 方案下需配置 `ptu_capacity` |
| | `ptu_capacity` | 吞吐预留容量配置对象，含 `input_tpm` 和 `output_tpm` 字段 | 单位为 kTPM；当前不支持单独配置思考输出配额；默认值为 `input_tpm: 10000`, `output_tpm: 1000` |
| | `deploy_spec` & `capacity` | `mu` 方案必需。`deploy_spec` 如 `MU1`/`MU5`，`capacity` 需为对应 `base_capacity` 的整数倍 | `MU2` 要求 `capacity` 为 8 的倍数；`MU5` 要求为 1 的倍数 |
| **吞吐预留** | `service_tier` | 性能档位。`ptu_fast`（高速，默认）或 `ptu_default`（标速） | `ptu_fast` 支持预付费/后付费；`ptu_default` 支持按天（`Day`）与 8 小时（`Hour`）两种预付费周期 |

## 使用方式

1. **准备环境**：获取华北2（北京）地域的 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`；确认子账号已授予模型调用、训练、部署权限。
2. **模型生产**：
   - *微调*：调用 `/api/v1/fine-tunes` 创建任务（如 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)），通过 `GET /api/v1/fine-tunes/{job_id}` 查询状态，待 `status=SUCCEEDED` 后获取 `finetuned_output`。
   - *压缩*：先调用 `/api/v1/fine-tunes/compress/templates` 获取模板，再用 `/api/v1/fine-tunes/compress/jobs` 创建压缩任务，轮询至 `SUCCEEDED` 后取 `quantized_output`。
   - *导入*：调用 `/api/v1/custom_models/import` 提交 OSS 路径，轮询至 `status=SUCCESSED` 后取 `model_name`。
3. **模型部署**：
   - 调用 `/api/v1/deployments` 提交部署请求，`model_name` 填写上一步产出的模型 ID（如 `finetuned_output` 或 `quantized_output`）。
   - 根据模型类型选择 `plan`：LoRA 模型选 `lora`；CosyVoice 选 `mu`；需预置吞吐则选 `ptu` 并配置 `ptu_capacity`。
4. **服务验证**：调用 `/api/v1/deployments/{deployed_model}` 查询部署状态，当 `status=RUNNING` 时即可开始推理调用。

## 限制和注意事项

- **地域强约束**：所有微调、部署、压缩、导入 API 均**仅支持华北2（北京）地域**，跨地域调用将失败。吞吐预留 API 是例外，支持多地域（如 `us-east-1`），需使用对应地域的 Endpoint [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，必须检查响应体中的 `output.operation_status` 字段（如 `SUCCEEDED`/`FAILED`），否则可能使用未就绪的容量 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型部署前置条件**：部署前必须确保调优/导入/压缩任务状态为 `SUCCEEDED` 或 `SUCCESSED`，否则部署会失败。部署过程本身需 5–10 分钟，需轮询状态接口确认。
- **计费敏感参数**：`n_epochs`（微调）、`max_steps`（图像）、`ptu_capacity`（吞吐预留）等参数直接影响费用，务必根据实际需求合理设置，避免资源浪费。
- **命名唯一性**：部署时若指定 `suffix`，其长度不得超过 8 字符，且需全局唯一；未指定时系统自动生成，同一模型多次部署必须显式指定不同 `suffix`。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
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
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [模型部署新 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-new-api-reference.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)


