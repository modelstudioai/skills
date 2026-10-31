# model production

model production 是百炼平台面向开发者提供的模型全生命周期管理能力，覆盖微调训练、模型导入、压缩优化、专属部署及吞吐预留等核心环节。所有能力均通过标准化 RESTful API 提供，支持自动化集成与规模化管理，适用于文本、图像、视频、语音等多模态模型的生产化落地。

## 支持的模型/功能

- **微调训练**：支持文本生成（SFT/CPT/DPO）、图像生成（文生图/图生图）、视频生成（首帧/首尾帧）、语音合成（CosyVoice）四类任务，各类型对应独立的创建与管理接口，如 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md) 和 [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)。
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 调优模型文件导入平台，仅限华北2（北京）地域，详见 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参调优模型进行量化压缩，不支持 LoRA 或已量化模型，详见 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **专属部署**：支持多种部署方式：`mu`（模型单元）、`dtu`（DTU 独占算力）、`ptu_v2`（预置吞吐 V2）、`lora`（LoRA 共享部署），不同模态模型支持的部署方式存在差异（如 CosyVoice 仅支持 `mu`，图像/视频 LoRA 推荐 `lora`）。
- **吞吐预留**：通过 PTU 预留容量保障推理稳定性，支持 `ptu_fast`（高速）和 `ptu_default`（标速）两档性能，支持预付费（含 8 小时时段）与后付费模式。

> **注意**：文档中关于部署地域的支持存在矛盾。[文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md) 明确指出 PTU 部署支持北京与新加坡，而 [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)、[视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md) 和 [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md) 均声明“仅在华北2（北京）地域开放”。实际开发中应以具体模型类型的部署文档为准，并优先通过 `/api/v1/deployments/models?model_source=custom&version=v1.0` 查询目标模型在当前地域的实际可用部署方案。

## 关键参数

- **微调通用参数**：
  - `model`：基础模型 ID（必填），如 `qwen3-14b`、`wan2.7-i2v`、`cosyvoice-v3-flash`。
  - `training_type`：微调方法（必填），文本支持 `sft`/`dpo_lora` 等，图像/视频/语音当前仅支持 `efficient_sft`。
  - `hyper_parameters`：超参对象（必填），关键字段因模型而异：
    - 文本：`n_epochs`、`batch_size`、`max_length`；
    - 图像：`max_steps`、`learning_rate`、`max_pixels`；
    - 视频：`n_epochs`、`batch_size`、`max_pixels`；
    - 语音：`lm_max_epoch`、`fm_max_epoch`、`lm_batch_size`、`fm_batch_size`。

- **部署核心参数**：
  - `plan`：部署方案（必填），决定计费与资源模型。
  - `model_name`：待部署模型 ID（非基础模型名），通常来自微调任务响应的 `output.finetuned_output`。
  - 方案特有参数：
    - `dtu`：`sku_code`、`template_code`、`dtu_capacity`（含 `input_tpm`/`output_tpm`）；
    - `lora`：`capacity`（实例数，推荐为 1）；
    - `mu`：`deploy_spec`（如 `MU5`）、`capacity`（需为 `base_capacity` 整数倍）；
    - `ptu_v2`：`service_tier`（`ptu_fast`/`ptu_default`）、`ptu_capacity`（单位 kTPM）。

- **吞吐预留关键参数**：
  - `service_tier`：性能档位，`ptu_fast`（默认）或 `ptu_default`。
  - `charge_type`：`pre_paid`（预付费）或 `post_paid`（后付费）。
  - `ptu_capacity`：容量配置对象，含 `input_tpm` 和 `output_tpm`（单位：kTPM = 1000 Tokens/分钟）。
  - `pre_paid_info`：预付费专属，含 `duration`（天数或 8 小时）、`auto_renewal`。

## 使用方式

1. **准备环境**：获取并配置 API Key，确保子账号具备 `AliyunBailianFullAccess` 或最小化权限策略；确认地域与模型兼容性（绝大多数训练/部署 API 仅支持华北2（北京））。
2. **训练模型**：
   - 调用对应模态的创建调优任务接口（如文本用 `/api/v1/fine-tunes`）；
   - 通过 [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md) 轮询 `status` 直至 `SUCCEEDED`；
   - 从响应 `output.finetuned_output` 获取模型 ID。
3. **（可选）优化模型**：对全参模型调用模型压缩 API，轮询任务状态，成功后使用 `output.quantized_output` 作为新模型 ID。
4. **部署服务**：
   - 调用 `/api/v1/deployments` 创建部署，传入 `model_name` 及对应 `plan` 的必要参数；
   - 通过 [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md) 轮询 `status`，待变为 `RUNNING` 后即可调用；
   - 对于吞吐预留，使用相同 `/api/v1/deployments` 路径，但 `plan="ptu"` 并提供 `ptu_capacity` 等参数。
5. **调用服务**：使用返回的 `output.deployed_model`（即 ModelCode）作为 `model` 参数，向 `https://dashscope.aliyuncs.com/api/v1/services/{deployed_model}/...` 发起推理请求。

## 限制和注意事项

- **地域强约束**：微调训练、模型导入、Checkpoint 管理、绝大多数部署 API（除 PTU 外）**仅支持华北2（北京）地域**。跨地域调用将失败，必须使用该地域的 API Key 和 Endpoint。
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作的 API 返回 HTTP 200 仅表示请求被接收，**必须检查响应体中的 `output.operation_status` 字段**（如 `FAILED`），否则可能误用未生效的容量 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型 ID 来源严格**：部署时的 `model_name` 必须是微调产出的 `finetuned_output` 或导入/压缩产出的 `model_name`，不可直接使用基础模型名（如 `qwen3-14b`），否则部署会失败。
- **DTU 部署特殊要求**：必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）和对应业务空间的 API Key，**不可使用 `dashscope.aliyuncs.com`**；且仅支持 `pre_paid`，续费操作需在控制台完成。
- **PTU 容量单位**：`ptu_capacity` 中的 `input_tpm`/`output_tpm` 单位为 **kTPM（千 Tokens/分钟）**，非 TPM；`ptu_default` 标速支持 8 小时时段预付费，`ptu_fast` 高速不支持。

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
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)


