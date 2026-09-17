# model production

`model production` 指在百炼平台完成模型的微调、压缩、导入、部署及吞吐预留等全生命周期操作，将定制化模型转化为稳定、可扩展、可计费的在线推理服务。该流程覆盖文本、图像、视频、语音四类生成式AI模型，核心能力围绕模型资产化（fine-tuning / import / compression）和服务化（deployment / throughput reservation）展开，所有操作均通过统一 OpenAPI 接口驱动。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成四类任务。文本生成支持 `cpt`/`sft`/`dpo_full` 等多种训练范式；图像/视频/语音生成当前仅支持 `efficient_sft`（LoRA高效微调）[文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)。
- **模型导入**：支持从 OSS 导入全参微调（`full`）或 LoRA（`lora`）模型文件，导入后可直接部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参微调模型进行量化压缩，产出低显存、高吞吐的量化模型 [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)。
- **部署与服务化**：提供三种部署模式：`mu`（模型单元，专属资源）、`lora`（LoRA共享部署，按[Token](../concepts/token.md)计费）、`ptu`（预置吞吐量，按TPM预留计费）。不同模态模型支持的部署方式存在差异：语音合成（CosyVoice）仅支持 `mu`；图像/视频生成推荐 `lora`；文本生成三者皆可。

> **注意**：所有微调、导入、压缩、部署类 API 当前**仅在华北2（北京）地域开放**，且必须使用该地域的 API Key。其他地域用户需通过控制台操作，详见各文档适用范围说明。

## 关键参数

| 参数 | 作用 | 取值示例 | 说明 |
|------|------|----------|------|
| `plan` | 部署方案 | `"mu"` / `"lora"` / `"ptu"` | 必填。决定资源模型与计费方式。`ptu` 仅用于吞吐预留场景，不适用于自定义模型部署。 |
| `deploy_spec` | 模型单元规格 | `"MU1"` / `"MU5"` | `plan=mu` 时必填。不同规格对应不同 base_capacity 和 capacity 倍数约束（如 `MU2` 要求 `capacity` 为 8 的倍数）。 |
| `capacity` | 资源单元数量 | `1`, `4`, `8` | `plan=mu` 或 `plan=lora` 时必填。`lora` 模式下通常设为 `1`；`mu` 模式下需满足 `base_capacity` 的整数倍。 |
| `ptu_capacity` | 吞吐预留容量 | `{"input_tpm": 10000, "output_tpm": 1000}` | `plan=ptu` 时生效，单位为 kTPM（1000 [Token](../concepts/token.md)s/分钟）。扩缩容时传入目标绝对值，非增量。 |
| `aigc_config` | AIGC 模板配置 | `{"use_input_prompt": false, "prompt": "..."}` | 仅视频生成部署必需，用于控制提示词生成逻辑 [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)。 |

## 使用方式

1. **准备阶段**：获取北京地域的 API Key，并确保子账号已授予 `model:Invoke`, `model:Train`, `model:Deploy` 权限。
2. **模型资产化**（任选其一）：
   - 微调：调用 `/api/v1/fine-tunes` 创建任务，轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，获取 `finetuned_output`。
   - 导入：调用 `/api/v1/custom_models/import` 提交 OSS 模型路径，轮询 `/api/v1/custom_models/{job_id}` 直至 `status=SUCCESSED`，获取 `model_name`。
   - 压缩：先调用 `/api/v1/fine-tunes/compress/templates` 获取模板，再调用 `/api/v1/fine-tunes/compress/jobs` 创建压缩任务，成功后取 `quantized_output`。
3. **部署服务**：使用上一步获得的 `model_name`，调用 `/api/v1/deployments`，指定 `plan`、`capacity` 等参数。部署状态需轮询 `/api/v1/deployments/{deployed_model}`，待 `status=RUNNING` 后方可调用。
4. **吞吐预留（独立场景）**：若需为**基础模型**（非微调/导入模型）预留固定吞吐，直接调用 `/api/v1/deployments`（同部署接口），但 `model_name` 填基础模型名，`plan=ptu`，并传入 `ptu_capacity` 和 `pre_paid_info`（预付费时）。

## 限制和注意事项

- **地域强绑定**：微调、导入、压缩、部署、Checkpoint 管理等全部生产类 API 仅在北京地域可用。吞吐预留 API（文档1）虽未明确限定地域，但其 Endpoint 依赖工作空间地域，实际使用仍需匹配目标模型所在地域。
- **HTTP 200 ≠ 操作成功**：所有写操作（创建/更新/删除）返回 HTTP 200 仅表示请求被接收，**必须检查响应体中 `output.operation_status` 或 `output.status` 字段**。例如吞吐预留创建返回 `WAIT_PRE_PAID_BILLING_TO_DEPLOYING` 表示订单处理中，非最终就绪 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型与部署方案兼容性**：
  - CosyVoice 语音合成模型**仅支持 `mu` 部署**，不支持 `lora` 或 `ptu`。
  - 图像/视频生成模型部署时 `plan` 必须为 `lora`，且 `capacity` 推荐为 `1`。
  - `ptu` 方案仅适用于百炼官方提供的基础模型（如 `qwen-plus`），**不支持微调、导入或压缩后的自定义模型**。
- **命名与唯一性**：部署时若需多次部署同一模型，必须通过 `suffix` 参数指定唯一后缀（最多8位小写字母/数字），否则会因模型名冲突失败。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)
- [图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)


