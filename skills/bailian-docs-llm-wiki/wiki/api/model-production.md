# model production

`model production` 是百炼平台中模型从训练、优化、导入到部署上线的全生命周期管理能力集合，覆盖微调（Fine-tuning）、模型导入、量化压缩、专属部署及吞吐预留等核心环节。所有生产操作均通过统一 OpenAPI 接口提供，支持开发者在华北2（北京）地域完成端到端集成。关键流程需严格遵循地域隔离、权限校验与状态轮询规范。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务，每类均有专用 API 和差异化超参约束。例如，图像生成仅支持 `efficient_sft` 微调类型 [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)，而语音合成（CosyVoice）需分别配置 LM 与 FM 子网络超参 [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)。
- **模型导入**：支持将 OSS 中的全参（`full`）或 LoRA（`lora`）调优模型文件导入平台，导入成功后可直接部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参调优模型进行量化压缩，产出模型可用于部署 [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)。
- **部署方式**：支持三种计费与资源模型：
  - `mu`（Model Unit）：按模型单元规格（如 `MU1`/`MU5`）和使用时长计费，适用于高稳定、低延迟场景；
  - `lora`：LoRA 共享部署，按 [Token](../concepts/token.md) 用量计费，适用于轻量、多租户场景；
  - `ptu`（Pre-provisioned Throughput Unit）：按预置吞吐量（kTPM）计费，支持预付费与后付费 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

> **注意**：所有微调与部署 API 当前**仅在华北2（北京）地域可用**，且必须使用该地域的 API Key；其他地域用户需通过控制台操作或切换地域接入点。

## 关键参数

| 参数 | 类型 | 说明 | 约束 |
|------|------|------|------|
| `model_name` | string | 模型唯一标识符，用于微调输入、部署输入及调用。微调产出为 `finetuned_output`，导入产出为 `model_name` | 必填；长度、字符集依模型类型而异 |
| `plan` | string | 部署方案，取值 `mu`/`lora`/`ptu` | 必填；不同模型类型支持范围不同（如 CosyVoice 仅支持 `mu`） |
| `deploy_spec` | string | `mu` 方案下必需，指定硬件规格（如 `MU5`） | 必填（当 `plan=mu`）；需通过 `/deployments/models` 接口获取有效值 |
| `capacity` | integer | `mu` 或 `lora` 方案下的实例数或资源单元数 | 必填；须为 `base_capacity` 的整数倍（如 `MU2` 要求 8 的倍数） |
| `ptu_capacity` | object | `ptu` 方案下必需，含 `input_tpm` 和 `output_tpm`（单位：kTPM） | 必填（当 `plan=ptu`）；步长与上限依模型和地域而定 |
| `aigc_config` | object | 视频生成部署必需，含 `use_input_prompt`、`prompt` 等提示词模板配置 | 必填（当 `plan=lora` 且为视频生成模型） |

## 使用方式

1. **准备环境**：  
   - 在华北2（北京）地域开通百炼服务并完成实名认证；  
   - 获取并配置该地域的 API Key（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；  
   - 若使用子账号，需授予 `AliyunBailianFullAccess` 或最小化权限策略。

2. **执行核心操作**：  
   - **微调**：调用 `POST /api/v1/fine-tunes`，传入 `model`、`training_type` 及领域特定超参（如文本生成的 `n_epochs`，图像生成的 `max_steps`）；  
   - **导入**：调用 `POST /api/v1/custom_models/import`，指定 `model_name`、`weight_type` 和 `storage_info`（OSS bucket & key）；  
   - **压缩**：先 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 提交任务；  
   - **部署**：调用 `POST /api/v1/deployments`，根据 `plan` 填写对应参数（如 `mu` 填 `deploy_spec` + `capacity`，`ptu` 填 `ptu_capacity`）；  
   - **状态确认**：所有异步操作（微调、导入、部署、压缩）均需轮询 `GET /api/v1/fine-tunes/{job_id}` 或 `GET /api/v1/deployments/{deployed_model}`，直至 `status` 为 `SUCCEEDED` 或 `RUNNING`。

3. **调用服务**：  
   - 部署成功后，`output.deployed_model` 即为模型调用 ID；  
   - 吞吐预留模型使用 `deployed_model`（即 ModelCode）作为 `model` 参数调用标准推理接口。

## 限制和注意事项

- **地域强绑定**：所有 API（微调、导入、压缩、部署、吞吐预留）均**仅支持华北2（北京）地域**，跨地域调用将失败。DashScope 域名 `https://dashscope.aliyuncs.com` 在此上下文中即代表北京地域入口。
- **HTTP 成功 ≠ 业务成功**：吞吐预留等容量操作返回 HTTP 200 仅表示请求接收成功，实际结果需检查响应体中的 `output.operation_status` 字段（可能为 `FAILED`）[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型兼容性限制**：  
  - 模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参调优模型，LoRA 模型和已量化模型不支持；  
  - DTU 计费模式的部署**不支持 API 管理**，必须通过控制台操作 [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)；  
  - `ptu_fast`（高速）吞吐预留不支持 8 小时时段预付费，仅 `ptu_default`（标速）支持 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **资源与配额**：各模型的 `input_tpm`/`output_tpm` 最小值、步长、上限，以及 `capacity` 的合法取值，均以目标地域控制台实时展示为准，API 文档中示例值仅为示意。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)


