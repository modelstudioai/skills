# model production

`model production` 指在百炼平台上将训练/调优后的模型转化为可稳定、高效、规模化调用的在线服务的完整流程，涵盖模型微调、导入、压缩、部署及吞吐预留等关键环节。该流程面向开发者提供标准化 API 接口与明确的地域、权限、参数约束，是模型从实验阶段走向生产环境的核心路径。

## 支持的模型与功能

百炼支持多模态模型的生产化，覆盖文本生成、图像生成、视频生成、语音合成四大类任务，每类均提供完整的微调（fine-tuning）、部署（deployment）能力：

- **文本生成**：支持 SFT、CPT、DPO 等多种微调方式，适用于 `qwen3-*` 系列模型；微调后可通过 `lora`、`mu`、`dtu` 或 `ptu_v2` 等多种 plan 部署 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **图像生成**：支持 `wan2.7-image-pro`、`qwen-image-2.0` 等模型的 LoRA 微调；部署时推荐 `lora` 方式，实例数通常设为 1 [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)。
- **视频生成**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview` 等模型的首帧/首尾帧微调；部署需配置 `aigc_config` 控制提示词生成逻辑 [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)。
- **语音合成（CosyVoice）**：仅支持 `cosyvoice-v3-flash` 模型，采用 LM/FM 双网络解耦微调；部署强制使用 `mu` plan，且必须指定 `deploy_spec`（如 `MU5`）[语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)。
- **模型压缩**：当前仅支持基于 `qwen3.5-flash-2026-02-23` 的全参调优模型的量化压缩，用于降低显存占用与推理成本 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。

> **注意**：模型导入（OSS 导入自定义模型）与模型压缩功能目前**仅在北京（cn-beijing）地域开放**，其他地域用户需通过控制台操作或切换地域调用 API。

## 关键参数

| 参数 | 作用 | 必填性 | 说明 |
|------|------|--------|------|
| `model_name` | 标识待微调或部署的模型 | 微调/部署均必填 | 微调时为基准模型 ID（如 `qwen3-14b`）；部署时为微调产出 ID（如 `qwen3-14b-ft-xxx`）或导入模型 ID。获取方式见各任务响应体 `output.finetuned_output` 或 `output.model_name`。 |
| `training_type` | 指定微调方法 | 微调必填 | 文本支持 `sft`/`dpo_full` 等；图像/视频/语音统一为 `efficient_sft`（LoRA）。 |
| `hyper_parameters` | 控制训练过程 | 微调必填 | 包含 `n_epochs`/`batch_size`/`max_length`（文本）、`max_steps`/`learning_rate`（图像）、`n_epochs`/`learning_rate`（视频）、`lm_max_epoch`/`fm_max_epoch`（语音）等，具体字段因模型类型而异。 |
| `plan` | 指定部署计费与资源模式 | 部署必填 | 常见值：`lora`（共享、按 token 计费）、`mu`（模型单元）、`dtu`（独占 GPU）、`ptu_v2`（预置吞吐）。不同 plan 对应的请求体结构与域名要求不同。 |
| `deployed_model` / `model_service_id` | 部署服务唯一标识 | 调用时必填 | 创建部署成功后返回，用于后续查询状态、限流配置及实际 API 调用。在吞吐预留文档中亦称 `model_service_id` [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。 |

## 使用方式

1. **微调训练**：  
   - 在华北2（北京）地域调用 `POST /api/v1/fine-tunes` 提交任务；  
   - 通过 `GET /api/v1/fine-tunes/{job_id}` 轮询状态，确认 `status=SUCCEEDED`；  
   - 从响应 `output.finetuned_output` 获取微调后模型 ID。

2. **模型导入（可选）**：  
   - 先将模型文件上传至已授权的 OSS Bucket；  
   - 调用 `POST /api/v1/custom_models/import` 提交导入任务；  
   - 等待 `status=SUCCESSED` 后，使用 `output.model_name` 进行部署。

3. **模型压缩（可选）**：  
   - 仅限 `qwen3.5-flash-2026-02-23` 全参调优模型；  
   - 先调用 `/api/v1/fine-tunes/compress/templates` 获取模板；  
   - 创建压缩任务，轮询至 `SUCCEEDED`，取 `output.quantized_output` 作为新模型 ID。

4. **部署服务**：  
   - 根据 `plan` 选择对应域名与参数：  
     - `lora`/`mu`：用 `dashscope.aliyuncs.com`（北京）或 `dashscope-intl.aliyuncs.com`（新加坡）；  
     - `dtu`：**必须**使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）；  
   - 提交 `POST /api/v1/deployments`，传入 `model_name`、`plan` 及对应容量/规格参数；  
   - 轮询 `GET /api/v1/deployments/{deployed_model}`，待 `status=RUNNING` 即可调用。

5. **吞吐预留（可选）**：  
   - 为已部署服务（或未部署的 `model_name`）创建吞吐预留，保障稳定 QPS；  
   - 调用 `POST /api/v1/deployments`（同部署接口），`plan=ptu`，指定 `ptu_capacity`（单位 kTPM）与 `service_tier`（`ptu_fast` 或 `ptu_default`）。

## 限制和注意事项

- **地域强约束**：  
  所有微调类 API（文本/图像/视频/语音）及模型导入、压缩 API **仅支持华北2（北京）地域**；部署 API 中 `mu`/`dtu` 仅支持北京，`ptu_v2` 支持北京与新加坡。跨地域调用将失败。

- **API Key 绑定性**：  
  API Key 与地域强绑定，不可跨地域复用；DTU 部署还要求 API Key 必须属于目标业务空间，且请求必须使用该空间专属域名 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

- **HTTP 成功 ≠ 操作成功**：  
  吞吐预留等异步操作接口即使返回 HTTP 200，其 `output.operation_status` 仍可能为 `FAILED`，**必须检查该字段及错误码**，否则可能导致容量未生效 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

- **部署状态轮询必要性**：  
  模型部署耗时约 5–10 分钟，需轮询 `GET /api/v1/deployments/{deployed_model}` 直至 `status=RUNNING`，不可依赖创建接口返回即认为可用。

- **语音合成特殊限制**：  
  CosyVoice 模型部署**不支持 `lora` plan**，仅支持 `mu`，且 `deploy_spec`（如 `MU5`）与 `capacity`（如 `1`）必须严格匹配规格约束，否则创建失败 [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)


