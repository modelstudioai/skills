# model production

model production 是百炼平台面向模型全生命周期的生产级能力集合，覆盖模型微调（Fine-tuning）、模型导入、模型压缩、模型部署及吞吐预留等核心环节。所有能力均通过统一 OpenAPI 接口提供，支持开发者在生产环境中构建、优化和规模化交付定制化 AI 服务。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类模态的 LoRA/全参微调。各模态对应不同基准模型与超参体系，例如图像生成支持 `wan2.7-image-pro` 和 `qwen-image-2.0`，视频生成支持 `wan2.7-i2v` 和 `wan2.5-i2v-preview`，语音合成当前仅支持 `cosyvoice-v3-flash` [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)。
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 微调模型文件导入平台，导入后可直接部署。该功能当前**仅在北京 Region 开放**，其他地域需通过控制台操作 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：提供量化压缩能力，当前仅支持基于 `qwen3.5-flash-2026-02-23` 的自定义全参微调模型，LoRA 模型不支持 [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)。
- **模型部署**：支持 `mu`（模型单元）、`lora`（LoRA 共享）、`ptu`（预置吞吐）三种部署方案，适配不同性能、成本与弹性需求。
- **吞吐预留（TPU/PTU）**：为高稳定性、低延迟场景提供预置吞吐容量保障，支持高速（`ptu_fast`）与标速（`ptu_default`）两种性能档位。

## 关键参数

| 参数 | 说明 | 约束与示例 |
|------|------|------------|
| `plan` | 部署方案 | `mu`（专属资源）、`lora`（共享资源、按 Token 计费）、`ptu`（预置吞吐、按容量计费） |
| `service_tier` | 吞吐预留性能档位 | `ptu_fast`（默认，高速）、`ptu_default`（标速）；`ptu_fast` 不支持 8 小时时段付费周期 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| `ptu_capacity` | 吞吐容量配置 | 单位为 kTPM（1000 Tokens/分钟），含 `input_tpm` 和 `output_tpm`；扩缩容时传入目标绝对值，非增量 |
| `training_type` | 微调方法 | 文本生成支持 `sft`/`efficient_sft`/`dpo_lora` 等；图像/视频/语音生成当前**仅支持 `efficient_sft`** |
| `hyper_parameters` | 模型训练超参 | 因模态与模型而异：文本生成关注 `n_epochs`/`batch_size`/`max_length`；图像生成关注 `max_steps`/`learning_rate`/`generation_type`；语音合成需分别配置 `lm_*` 与 `fm_*` 前缀参数 |

> **注意**：文档 9（文本生成-创建调优任务）中 `training_type` 列出 `cpt`/`dpo_full` 等选项，但文档 6（图像生成）、文档 8（视频生成）、文档 10（语音合成）均明确限定“当前仅支持 `efficient_sft`”。实际调用时应以各模态专用文档为准，通用列表存在过时风险。

## 使用方式

1. **准备环境**：确保使用华北2（北京）地域的 API Key，并完成 RAM 权限配置（模型调用、训练、部署）[调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)。
2. **创建微调任务**：调用 `POST /api/v1/fine-tunes`，指定 `model`、`training_type`、`hyper_parameters` 及数据集（`training_file_ids` 或 `training_datasets`）。
3. **轮询任务状态**：使用 `GET /api/v1/fine-tunes/{job_id}` 查询 `status`，直至为 `SUCCEEDED`；成功后从 `output.finetuned_output` 获取模型 ID。
4. **（可选）模型压缩**：对全参微调模型调用 `/api/v1/fine-tunes/compress/jobs`，获取 `quantized_output` 后用于部署。
5. **部署模型**：调用 `POST /api/v1/deployments`，根据 `plan` 选择参数：
   - `mu`：必填 `deploy_spec`（如 `MU1`）、`capacity`、`billing_method`
   - `lora`：仅需 `model_name`、`capacity`、`plan`
   - `ptu`：使用 `ptu_capacity` 对象配置吞吐量
6. **验证部署**：调用 `GET /api/v1/deployments/{deployed_model}` 轮询 `status`，待变为 `RUNNING` 后即可调用。

## 限制和注意事项

- **地域限制**：微调、模型导入、模型压缩、模型部署（除吞吐预留外）API **全部仅在华北2（北京）地域可用**。吞吐预留 API 支持多地域，但需使用对应地域的 Endpoint 和 API Key。
- **吞吐预留关键约束**：
  - HTTP 200 不代表操作成功，必须检查响应体中 `output.operation_status` 字段是否为 `SUCCEEDED`；
  - `ptu_fast` 高速档位**不支持 `pricing_cycle=Hour`（8 小时时段）**，该配置仅 `ptu_default` 标速允许 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型部署限制**：DTU 独占算力部署暂不支持 API 管理，需通过控制台操作 [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)。
- **Checkpoint 管理**：语音合成（CosyVoice）模型的 Checkpoint `step` 字段为 `LM_epoch × 10000 + FM_epoch` 的组合值，排序与导出逻辑与其他模态不同 [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)。
- **计费提示**：`n_epochs`、`max_steps`、`batch_size` 等超参直接影响训练费用，务必参考各模态文档中的推荐值与计费说明。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)


