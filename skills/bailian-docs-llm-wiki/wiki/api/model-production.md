# model production

`model production` 指在百炼平台上将训练/调优后的模型转化为可稳定、高效、规模化调用的在线服务的完整流程，涵盖模型微调、导入、压缩、部署及吞吐预留等核心环节。该流程面向开发者提供标准化 API 接口与明确的地域、权限和参数约束，是模型从实验阶段走向生产环境的关键路径。

## 支持的模型与功能

百炼 `model production` 当前支持以下模态的模型全生命周期管理：

- **文本生成**：支持 SFT/CPT/DPO 等多种微调方式（`sft`, `cpt`, `dpo_full`, `dpo_lora`），适用于 Qwen 系列大模型（如 `qwen3-14b`, `qwen3-32b`）[文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)；
- **图像生成**：支持 `wan2.7-image-pro`, `qwen-image-2.0` 等模型的 LoRA 微调，区分 `t2i`（文生图）与 `i2i`（图生图）模式 [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)；
- **视频生成**：支持 `wan2.7-i2v`, `wan2.2-kf2v-flash` 等图生视频/首尾帧视频模型，仅限 `efficient_sft` 微调 [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)；
- **语音合成**：支持 `cosyvoice-v3-flash` 的双网络（LM + FM）解耦微调 [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)；
- **模型导入与压缩**：支持从 OSS 导入全参或 LoRA 调优模型；支持对 `qwen3.5-flash-2026-02-23` 全参模型进行量化压缩以降低推理成本 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。

> **注意**：所有微调（fine-tuning）、导入（custom_models）、压缩（compress）及部署（deployments）API 均**仅在华北2（北京）地域可用**，且必须使用该地域的 API Key。其他地域用户需通过控制台操作，详见 [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md) 和 [模型部署新 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-new-api-reference.md)。

## 关键参数

### 微调通用参数
- `model`: 基础模型 ID（必填），如 `qwen3-14b`, `wan2.7-i2v`, `cosyvoice-v3-flash`；
- `training_type`: 微调方法（必填），各模态支持范围不同：文本支持 `sft`/`dpo_lora`，图像/视频/语音当前仅支持 `efficient_sft`；
- `hyper_parameters`: 超参数对象（必填项依模型而异）：
  - 文本：`n_epochs`, `batch_size`, `max_length`（推荐 8192）为必填；
  - 视频：`n_epochs`, `learning_rate`, `eval_epochs`, `max_pixels` 为必填；
  - CosyVoice：`lm_max_epoch`, `fm_max_epoch`, `lm_batch_size`, `fm_batch_size` 等双网络参数均为必填；
  - 图像：`max_steps`, `learning_rate`, `generation_type`, `max_pixels` 为必填。

### 部署关键参数
- `plan`: 部署计费方案（必填），取值包括：
  - `mu`: 模型单元部署（专属资源，支持 `enable_thinking`, `max_context_length`, `rpm_limit` 等高级配置）；
  - `lora`: LoRA 共享部署（按 Token 计费，轻量级，适用于多租户场景）；
  - `ptu`: 吞吐预留（预置输入/输出 TPM，适用于高并发、低延迟场景）；
- `deploy_spec` / `capacity`: `plan=mu` 时必填，指定部署模板（如 `MU1`, `MU5`）及资源单元数量（需为 `base_capacity` 整数倍）；
- `ptu_capacity`: `plan=ptu` 时生效，结构为 `{ "input_tpm": 10000, "output_tpm": 1000 }`，单位为 kTPM（1 kTPM = 1000 Tokens/分钟）[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)；
- `aigc_config`: 视频生成部署特有，用于控制提示词来源与模板（`use_input_prompt`, `prompt`, `lora_prompt_default`）。

## 使用方式

1. **准备与鉴权**：  
   获取华北2（北京）地域的 API Key，并通过环境变量或请求头 `Authorization: Bearer <api-key>` 传入；确保子账号已授予 `model:FineTune`, `model:Deploy`, `oss:GetObject` 等必要权限。

2. **微调/导入/压缩**：  
   - 微调：调用 `POST /api/v1/fine-tunes` 创建任务，轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，获取 `finetuned_output`；
   - 导入：调用 `POST /api/v1/custom_models/import` 提交 OSS 模型路径，轮询状态至 `SUCCESSED`；
   - 压缩：先 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 创建任务，轮询至 `SUCCEEDED` 后获取 `quantized_output`。

3. **部署模型**：  
   调用 `POST /api/v1/deployments`，传入 `model_name`（即上步产出的 `finetuned_output`/`model_name`/`quantized_output`）、`plan` 及对应参数。部署任务异步执行，需轮询 `GET /api/v1/deployments/{deployed_model}` 直至 `status=RUNNING`。

4. **调用与管理**：  
   使用 `deployed_model` 作为模型标识调用推理 API；通过 `GET /api/v1/deployments` 列表、`GET /api/v1/deployments/{deployed_model}` 查询状态、`PATCH` 扩缩容、`DELETE` 删除部署。

## 限制和注意事项

- **地域强绑定**：全部 `model production` API（微调、部署、压缩、导入、吞吐预留）均**仅支持华北2（北京）地域**，跨地域调用将失败。吞吐预留虽在文档中提及弗吉尼亚地域 Endpoint，但实际创建接口未开放该地域支持，应以 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中“工作空间专属域名”说明为准，且需确认目标地域模型与购买限制。
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，**必须检查响应体中的 `output.operation_status` 字段**（如 `SUCCEEDED`/`FAILED`），否则可能误用未就绪容量 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型部署模板约束**：`plan=mu` 时，`capacity` 必须为 `base_capacity` 的整数倍（如 `MU2` 要求 8 的倍数，`MU5` 要求 1 的倍数）；`plan=lora` 时无需 `capacity`，但仅支持 LoRA 类型模型。
- **Checkpoint 状态依赖**：导出或部署 Checkpoint 前，需确保其 `status=SUCCEEDED`，否则 `model_name` 字段不会返回，无法用于后续部署 [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)。
- **计费触发时机**：模型部署成功（`status=RUNNING`）后立即开始计费，即使尚未发起任何推理请求；吞吐预留容量购买后即开始计费，与是否调用无关。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
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
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [模型部署新 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-new-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)


