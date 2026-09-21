# model production

`model production` 是百炼平台中模型从训练、优化、导入到部署上线的全生命周期管理能力集合，涵盖微调（Fine-tuning）、模型压缩、自定义模型导入及多种部署模式（MU、LoRA、PTU）。所有生产环节均通过统一 OpenAPI 接口提供，支持开发者在华北2（北京）地域完成端到端自动化集成。吞吐预留（PTU）作为独立的高性能推理资源供给机制，与模型部署解耦但可协同使用。

## 支持的模型与功能

- **微调支持多模态任务**：文本生成（[文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)）、图像生成（[图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)）、视频生成（[视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)）和语音合成（[语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)）。
- **模型压缩仅限特定全参模型**：当前仅支持基于 `qwen3.5-flash-2026-02-23` 的自定义全参调优模型，LoRA 模型和已量化模型不支持（见 [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)）。
- **自定义模型导入支持两种类型**：全参调优（`full`）和 LoRA（`lora`）模型，需通过 OSS 挂载并完成结构与安全校验（见 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)）。
- **部署覆盖全部微调产出模型**：文本、图像、视频、语音模型均可部署，但部署方式因模型类型而异：文本/图像/视频 LoRA 模型推荐 `plan=lora`；CosyVoice 语音模型**仅支持 `plan=mu`**（见 [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)）。

> **注意**：文档 19（图像生成部署）与文档 22（语音合成部署）对 `plan` 参数的要求存在明显差异——前者明确推荐 `lora`，后者强制要求 `mu`。该差异非矛盾，而是由模型架构与推理特性决定：LoRA 部署适用于参数增量轻量、可共享底座的场景（如文生图），而 CosyVoice 的双子网络（LM+FM）需独占资源单元以保障音色一致性与低延迟，故不支持 LoRA 共享部署。

## 关键参数

| 参数 | 适用场景 | 必填性 | 说明 |
|------|----------|--------|------|
| `model_name` | 所有部署接口 | 是 | 微调产出模型 ID（如 `qwen3-14b-suffix-ft-xxx`）或导入模型 ID，**非基础模型名**；须从调优任务响应 `output.finetuned_output` 或导入任务响应 `output.model_name` 获取。 |
| `plan` | 部署接口 | 是 | 部署计费与资源模式：<br>• `mu`：按模型单元（Model Unit）计费，资源专属，支持 `deploy_spec` 和 `capacity` 配置；<br>• `lora`：LoRA 共享部署，按 Token 用量计费，仅适用于 LoRA 微调模型；<br>• `ptu`：按预置吞吐量（TPM）计费，需配合吞吐预留 API 使用。 |
| `ptu_capacity` | `plan=ptu` 时 | 否（默认 `input_tpm=10000, output_tpm=1000`） | 单位为 kTPM（1000 Tokens/分钟），指定每分钟输入/输出 Token 容量上限；扩缩容时传入**绝对值**，非增量。 |
| `deploy_spec` & `capacity` | `plan=mu` 时 | 是（`deploy_spec`）/ 是（`capacity`） | `deploy_spec` 如 `"MU1"`、`"MU5"` 决定单单元规格；`capacity` 为单元数量，须为 `base_capacity` 整数倍（如 `MU2` 要求 `capacity` 为 8 的倍数）。 |
| `aigc_config` | 视频生成部署 | 是 | 包含 `use_input_prompt`（控制 prompt 来源）、`prompt`（自动生成模板）和 `lora_prompt_default`（兜底模板），仅当 `use_input_prompt=false` 时生效（见 [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)）。 |

## 使用方式

1. **微调训练**：  
   - 统一调用 `POST https://dashscope.aliyuncs.com/api/v1/fine-tunes`，按模态选择对应超参数（如文本用 `n_epochs`，图像用 `max_steps`，语音用 `lm_max_epoch`/`fm_max_epoch`）。  
   - 任务状态轮询 `GET /api/v1/fine-tunes/{job_id}`，确认 `status=SUCCEEDED` 后获取 `output.finetuned_output`。

2. **模型导入/压缩（可选）**：  
   - 导入：`POST /api/v1/custom_models/import` 提交 OSS 路径，轮询至 `status=SUCCESSED`。  
   - 压缩：先 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 创建任务，成功后取 `output.quantized_output`。

3. **部署服务**：  
   - `POST https://dashscope.aliyuncs.com/api/v1/deployments`，根据模型类型选择 `plan` 并填充对应参数。  
   - 部署后轮询 `GET /api/v1/deployments/{deployed_model}`，待 `status=RUNNING` 即可调用。

4. **吞吐预留（PTU）独立管理**：  
   - 通过 `/api/v1/deployments`（吞吐预留专用路径）创建预留容量，获得 `deployed_model`（即 ModelCode），该标识**直接用于模型调用**，无需额外部署步骤（见 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)）。

## 限制和注意事项

- **地域强约束**：所有微调、导入、压缩及部署 API **仅在华北2（北京）地域可用**，必须使用该地域的 API Key 和 Endpoint（`https://dashscope.aliyuncs.com`），跨地域调用将失败。
- **HTTP 200 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，**必须检查响应体中的 `output.operation_status` 字段**（如 `SUCCEEDED`/`FAILED`），否则可能误用未就绪容量（见 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)）。
- **模型部署与吞吐预留解耦**：PTU 预留的 `deployed_model` 是独立调用标识，不依赖于 `model-deployment-*` 接口创建的部署；反之，`plan=ptu` 的部署请求实际是绑定已有 PTU 实例，而非创建新预留。
- **Checkpoint 管理**：语音合成（CosyVoice）的 Checkpoint `step` 为 `LM_epoch × 10000 + FM_epoch`，排序与导出需按此逻辑处理（见 [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)）。
- **免费与限时策略**：模型压缩功能当前限时免费，且仅支持指定基础模型；具体免费期限与支持模型列表请以控制台实时信息为准。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)


