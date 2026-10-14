# model production

`model production` 指在百炼平台上将训练/调优后的模型转化为可稳定、可扩展、可计费的在线推理服务的完整流程，涵盖微调（fine-tuning）、导入（import）、压缩（compression）、部署（deployment）及吞吐预留（throughput reservation）等核心环节。该流程面向开发者提供标准化 API 接口与明确的地域、权限和参数约束，不依赖控制台操作即可完成端到端模型交付。

## 支持的模型/功能

百炼支持多模态模型的生产化，当前覆盖以下类型：

- **文本生成**：支持 SFT、CPT、DPO、LoRA 等多种微调方式，适用于 Qwen 系列（如 `qwen3-14b`）、`cosyvoice-v3-flash` 等模型；支持全参微调与 LoRA 导入 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **图像生成**：支持 `wan2.7-image-pro`、`qwen-image-2.0` 等模型的文生图/图生图微调，需指定 `generation_type`（`t2i`/`i2i`）与分辨率参数（`max_pixels`）[图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)。
- **视频生成**：支持 `wan2.7-i2v`（首帧/首尾帧）、`wan2.5-i2v-preview` 等模型，训练需严格匹配 `task_type` 与 `max_pixels` 范围，且仅支持 `efficient_sft` 微调 [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)。
- **语音合成**：CosyVoice 系列（如 `cosyvoice-v3-flash`）支持 LM/FM 双网络独立调优，超参数需分别配置 `lm_*` 与 `fm_*` 前缀字段 [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)。
- **模型压缩**：当前仅支持基于 `qwen3.5-flash-2026-02-23` 的全参微调模型的量化压缩，LoRA 模型与已量化模型不支持 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。

> **注意**：所有微调与部署 API（除吞吐预留外）**仅在华北2（北京）地域可用**，且必须使用该地域的 API Key。跨地域调用将失败，详见 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)、[图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md) 等文档的“适用范围”说明。

## 关键参数

| 参数 | 所属环节 | 必填 | 说明 | 示例值 |
|--------|-----------|------|------|---------|
| `model_name` | 微调/部署/导入 | 是 | 基础模型 ID（微调）或产出模型 ID（部署），非显示名；部署时必须为微调/导入后生成的 `finetuned_output` 或 `model_name` | `qwen3-14b`, `wan2.7-i2v-ft-202511111122-xxxx` |
| `training_type` | 微调 | 是 | 微调方法；文本支持 `sft`/`dpo_lora` 等，图像/视频/语音统一仅支持 `efficient_sft` | `sft`, `efficient_sft` |
| `n_epochs` / `max_steps` | 微调 | 是（文本/图像）<br>是（视频/语音） | 文本/语音用轮次，图像用总步数；直接影响训练时长与费用 | 文本：`3`；图像：`800`；视频：`50`；语音：`lm_max_epoch=60` |
| `plan` | 部署 | 是 | 部署计费方案：`mu`（模型单元）、`lora`（LoRA 共享）、`ptu`（预置吞吐）；**CosyVoice 仅支持 `mu`** | `mu`, `lora`, `ptu` |
| `ptu_capacity` | 吞吐预留 | 是 | 吞吐预留容量配置对象，单位为 kTPM（1000 [Token](../concepts/token.md)s/分钟）；`input_tpm` 和 `output_tpm` 必填 | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` | 部署（`mu`） | 条件必填 | 模型单元规格模板 ID（如 `MU1`, `MU5`），需通过 `/api/v1/deployments/models` 查询获取 | `MU5` |
| `capacity` | 部署（`mu`/`lora`） | 是 | 实例数量（`lora`）或资源单元数（`mu`）；`MU2` 要求为 8 的倍数，`MU5` 可为 1 | `1`, `8` |

## 使用方式

1. **微调训练**：  
   - 调用 `POST /api/v1/fine-tunes` 创建任务（文本/图像/视频/语音共用同一 endpoint）；  
   - 通过 `GET /api/v1/fine-tunes/{job_id}` 轮询状态，确认 `status=SUCCEEDED`；  
   - 从响应 `output.finetuned_output` 获取产出模型 ID。

2. **模型导入**：  
   - 调用 `POST /api/v1/custom_models/import` 提交 OSS 模型路径；  
   - 轮询 `GET /api/v1/custom_models/{job_id}` 直至 `status=SUCCESSED`；  
   - 使用 `output.model_name` 进行后续部署。

3. **模型压缩**：  
   - 先调用 `GET /api/v1/fine-tunes/compress/templates` 获取 `template_id`；  
   - 再 `POST /api/v1/fine-tunes/compress/jobs` 创建压缩任务；  
   - 轮询 `GET /api/v1/fine-tunes/compress/jobs/{job_id}`，成功后取 `output.quantized_output`。

4. **模型部署**：  
   - 调用 `POST /api/v1/deployments`，按 `plan` 类型传入对应参数（见上表）；  
   - 通过 `GET /api/v1/deployments/{deployed_model}` 轮询，`status=RUNNING` 即可调用；  
   - 部署成功后，`output.deployed_model` 即为模型调用标识（ModelCode）。

5. **吞吐预留**：  
   - 调用 `POST /api/v1/deployments`（同部署 endpoint，但 `plan=ptu`）创建预留；  
   - 返回的 `output.deployed_model` 即为 ModelCode，用于后续高并发调用；  
   - 注意：HTTP 200 不代表操作成功，必须检查 `output.operation_status` 字段 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

## 限制和注意事项

- **地域强约束**：微调、导入、部署、压缩、Checkpoint 管理等全部 API 仅支持华北2（北京）地域；吞吐预留 API 支持多地域（如弗吉尼亚），但需使用对应地域的 Endpoint 和 API Key [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **API Key 绑定**：API Key 与地域强绑定，不可跨地域复用；工作空间专属域名需显式构造（如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`）。
- **状态检查强制要求**：所有异步操作（微调、导入、压缩、吞吐预留、部署）均返回 HTTP 200 即刻响应，但实际结果需轮询查询接口并检查 `output.status` 或 `output.operation_status`；忽略此检查将导致调用失败或资源浪费。
- **模型兼容性限制**：  
  - 模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参微调模型，不支持 LoRA 或其他基础模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)；  
  - CosyVoice 部署仅支持 `plan=mu`，不支持 `lora` 或 `ptu` 方案 [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)；  
  - 视频生成微调中 `n_epochs` 与 `batch_size` 需满足 `steps = n_epochs × ⌈数据集大小 / batch_size⌉ ≥ 800`，否则训练可能不收敛 [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)。
- **部署后计费**：`plan=mu` 部署成功即开始计费，无论是否发起调用；建议部署前确认计费规则 [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [模型部署新 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-new-api-reference.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)


