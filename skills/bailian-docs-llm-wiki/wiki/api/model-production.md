# model production

`model production` 是百炼平台中模型从训练、优化、导入到部署上线的全生命周期管理能力集合，涵盖微调（Fine-tuning）、模型压缩、自定义模型导入、专属部署及吞吐预留等核心环节。所有生产操作均通过统一 OpenAPI 接口提供，支持文本、图像、视频、语音四类生成式模型，但多数功能当前仅在华北2（北京）地域可用。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持文本生成（[文本生成](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)）、图像生成（[图像生成](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)）、视频生成（[视频生成](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)）和语音合成（[语音合成](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)）四大模态。各模态支持的基准模型、超参数集与训练方式不同，例如图像生成仅支持 `efficient_sft`，而文本生成支持 `sft`、`dpo_lora` 等多种方法。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参微调模型进行量化压缩，不支持 LoRA 模型或已量化的模型（见 [模型压缩](raw/_short/model-compression-api-09615482a618bd21.md)）。
- **模型导入**：支持将 OSS 中存储的全参（`full`）或 LoRA（`lora`）微调模型文件导入平台，导入后可直接部署（见 [模型导入](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)）。
- **专属部署**：支持三种部署方案：`mu`（模型单元，资源专属）、`lora`（LoRA 共享，按 [Token](../concepts/token.md) 计费）和 `ptu`（预置吞吐，按容量计费），覆盖不同性能、成本与隔离性需求（见 [文本生成-部署模型](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)）。
- **吞吐预留（TPM 预留）**：为高并发、低延迟场景提供确定性推理吞吐保障，通过 `ptu` 方案实现，支持预付费与后付费模式（见 [吞吐预留 API参考](raw/model-api-reference/model-production/throughput-reservation-api.md)）。

> **注意**：文档 17（图像生成部署）、文档 19（视频生成部署）和文档 21（语音合成部署）均声明“仅在华北2（北京）地域开放”，但文档 24（文本生成部署）未明确限定地域，仅强调“如您使用其他地域，请通过该地域的百炼控制台完成模型部署操作”。这表明文本生成部署 API 可能已在更多地域上线，而其他模态部署仍严格限于北京。开发者应以实际调用结果和控制台地域支持为准。

## 关键参数

| 参数 | 所属功能 | 说明 | 示例值 |
|------|----------|------|--------|
| `training_type` | 微调任务创建 | 微调方法类型，不同模态取值不同：文本支持 `sft`/`dpo_lora`；图像/视频/语音仅支持 `efficient_sft` | `"efficient_sft"` |
| `plan` | 部署模型 | 部署方案，决定计费与资源模型：`mu`（专属）、`lora`（共享）、`ptu`（吞吐预留） | `"ptu"` |
| `ptu_capacity` | `ptu` 部署 | 吞吐容量配置对象，含 `input_tpm` 和 `output_tpm`（单位：kTPM） | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` | `mu` 部署 | 模型单元规格模板，决定基础资源与扩缩容约束，如 `MU1`、`MU5` | `"MU5"` |
| `capacity` | 所有部署 | 资源数量：`mu` 下为模型单元数；`lora` 下为实例数（推荐 1）；`ptu` 下为容量实例数 | `1` |
| `service_tier` | 吞吐预留创建 | 性能档位：`ptu_fast`（高速，默认）或 `ptu_default`（标速） | `"ptu_fast"` |

## 使用方式

1. **准备阶段**：确保使用华北2（北京）地域的 API Key（除文本生成外，其余模态部署与训练均强制要求），并完成 RAM 权限配置（见 [权限管理概述](raw/model-user-guide/security-and-compliance/permission-management-overview.md)）。
2. **训练/优化**：
   - 创建微调任务：调用 `POST /api/v1/fine-tunes`，指定 `model`、`training_type` 和 `hyper_parameters`（如 `n_epochs`、`batch_size`）。
   - （可选）压缩模型：对已有的 `qwen3.5-flash-2026-02-23` 全参模型，调用 `/api/v1/fine-tunes/compress/jobs` 创建量化任务。
   - （可选）导入模型：调用 `/api/v1/custom_models/import` 将 OSS 模型导入平台。
3. **部署服务**：
   - 查询任务状态：轮询 `GET /api/v1/fine-tunes/{job_id}`，确认 `status` 为 `SUCCEEDED`。
   - 提交部署：调用 `POST /api/v1/deployments`，根据 `plan` 填写对应参数（如 `ptu_capacity` 或 `deploy_spec`）。
   - 等待就绪：轮询 `GET /api/v1/deployments/{deployed_model}`，直至 `status` 变为 `RUNNING`。
4. **调用服务**：使用返回的 `deployed_model` 作为 `model` 参数，调用标准推理 API（如 `/api/v1/services/aigc/text-generation`）。

## 限制和注意事项

- **地域限制**：微调任务创建（文档 4、7、10、12）、Checkpoint 管理（文档 15）、模型导入（文档 5）、模型压缩（文档 6）以及图像/视频/语音部署（文档 17、19、21）均**仅支持华北2（北京）地域**。文本生成部署（文档 24）虽未明文限定，但其示例 Endpoint 与前述一致，建议默认按北京地域使用。
- **吞吐预留关键约束**：HTTP 200 响应不表示操作成功，必须检查响应体中 `output.operation_status` 字段；`ptu_fast` 高速档位不支持 8 小时时段预付费，仅 `ptu_default` 标速支持（见 [吞吐预留 API参考](raw/model-api-reference/model-production/throughput-reservation-api.md)）。
- **模型兼容性**：模型压缩功能**仅支持 `qwen3.5-flash-2026-02-23` 的全参微调模型**，LoRA 模型、其他基础模型或已量化的模型均不支持（见 [模型压缩](raw/_short/model-compression-api-09615482a618bd21.md)）。
- **部署参数依赖**：`deploy_spec` 和 `capacity` 为 `mu` 部署的必填项，且 `capacity` 必须为 `base_capacity` 的整数倍（如 `MU2` 要求 `capacity` 为 8 的倍数）；`ptu_capacity` 为 `ptu` 部署的可选参数，若不提供则使用默认值（10,000 input_tpm / 1,000 output_tpm）。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)


