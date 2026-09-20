# model production

`model production` 指在百炼平台上将训练/调优后的模型转化为可稳定、可扩展、可计费的在线推理服务的完整流程，涵盖吞吐预留、模型微调、模型导入与压缩、以及多模态模型部署等核心能力。该流程面向开发者提供标准化 API 接口，支持从华北2（北京）地域统一接入，但部分能力存在地域与模型类型强约束。

## 支持的模型与功能

- **微调支持**：文本生成、图像生成、视频生成、语音合成（CosyVoice）四类主流模态，均通过统一 `/api/v1/fine-tunes` 接口创建任务，但各模态的超参数、数据格式与适用模型严格隔离。例如，图像生成仅支持 `wan2.7-image-pro` 等万相系列模型，而语音合成当前仅支持 `cosyvoice-v3-flash` [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)。
- **模型引入**：支持两种路径——通过微调任务产出模型（如 `qwen3-14b-suffix-ft-...`），或通过 OSS 导入自定义全参/LoRA 模型 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型优化**：提供量化压缩能力，当前仅支持基于 `qwen3.5-flash-2026-02-23` 的自定义全参调优模型，LoRA 模型和已量化模型不支持 [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)。
- **部署方案**：支持三种计费与资源模型：
  - `mu`（Model Unit）：按专属算力单元时长计费，适用于高 SLA、低延迟场景；
  - `lora`：LoRA 共享部署，按 Token 用量计费，适用于轻量、低成本推理；
  - `ptu`（Predefined Throughput Unit）：按预置吞吐量（kTPM）计费，适用于流量可预测的稳态业务。

> **注意**：文档中多次声明“仅在华北2（北京）地域可用”，但[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)明确指出其支持多地域（如弗吉尼亚 `us-east-1`），且工作空间专属域名含 `{region}` 变量。此处地域限制仅针对微调与部署 API，吞吐预留能力本身是跨地域的。

## 关键参数

| 参数 | 所属能力 | 必填性 | 说明 |
|------|----------|--------|------|
| `model_name` | 微调、部署、导入 | 是 | 基础模型 ID（如 `qwen3-14b`）或微调产出模型 ID（如 `qwen3-14b-suffix-ft-...`）；部署时必须为已存在模型。 |
| `plan` | 部署 | 是 | 取值为 `mu` / `lora` / `ptu`，决定资源模型与计费方式。 |
| `ptu_capacity.{input_tpm,output_tpm}` | 吞吐预留 | 是 | 单位为 kTPM（1000 Tokens/分钟），表示预置吞吐能力，扩缩容操作为绝对值变更，非增量 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。 |
| `deploy_spec` & `capacity` | `mu` 部署 | 条件必填 | `deploy_spec`（如 `MU1`, `MU5`）定义硬件规格；`capacity` 必须为对应 `base_capacity` 的整数倍（如 `MU2` 要求 8 的倍数）。 |
| `aigc_config` | 视频生成部署 | 必填 | 包含 `use_input_prompt`, `prompt`, `lora_prompt_default`，用于控制提示词生成逻辑，是视频生成服务的核心配置 [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)。 |

## 使用方式

1. **准备环境**：获取华北2（北京）地域的 API Key，并配置 `DASHSCOPE_API_KEY` 环境变量；确认子账号已授予 `AliyunBailianFullAccess` 或最小化权限策略。
2. **训练/引入模型**：
   - 微调：调用 `POST /api/v1/fine-tunes`，传入 `model`, `training_type`, `hyper_parameters` 等，轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，提取 `finetuned_output`。
   - 导入：调用 `POST /api/v1/custom_models/import`，指定 `model_name`, `weight_type`, `storage_info`，轮询至 `status=SUCCESSED`。
3. **（可选）压缩模型**：对符合条件的全参模型，调用 `POST /api/v1/fine-tunes/compress/jobs` 创建量化任务，成功后获得 `quantized_output`。
4. **部署服务**：调用 `POST /api/v1/deployments`，根据 `plan` 选择必填字段：
   - `mu`: 填 `deploy_spec`, `capacity`, `billing_method`
   - `lora`: 仅需 `capacity`, `plan`
   - `ptu`: 填 `ptu_capacity` 对象
5. **验证与调用**：轮询 `GET /api/v1/deployments/{deployed_model}`，待 `status=RUNNING` 后，使用 `deployed_model` 作为 `model` 参数调用对应模态的推理 API。

## 限制和注意事项

- **地域强绑定**：所有微调（文本/图像/视频/语音）、模型导入、模型压缩、模型部署 API **仅支持华北2（北京）地域**，API Key 和 Endpoint 必须匹配该地域；吞吐预留 API 则支持多地域，但需显式构造对应地域的 Endpoint。
- **HTTP 200 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求被接收，实际状态需检查响应体中的 `output.operation_status` 字段，可能为 `FAILED` [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型兼容性限制**：
  - `ptu` 部署不支持 LoRA 模型，仅支持基础模型或全参微调模型；
  - `lora` 部署仅适用于 LoRA 微调产出模型，不支持全参模型或导入模型；
  - `mu` 部署对模型类型最开放，但语音合成（CosyVoice）当前**仅支持 `mu` 方案**，不支持 `lora` 或 `ptu`。
- **资源与配额**：`capacity` 值受 `deploy_spec` 约束（如 `MU2` 必须为 8 的倍数）；吞吐预留的 `input_tpm`/`output_tpm` 有模型级最小值、步长及上限，不可随意设置。
- **命名唯一性**：部署时若指定 `suffix`，其值必须全局唯一（同一工作空间内），否则创建失败。

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
- [图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)


