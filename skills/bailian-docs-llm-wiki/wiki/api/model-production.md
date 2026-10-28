# model production

`model production` 是百炼平台面向模型全生命周期管理的核心能力集合，覆盖从模型微调、压缩、导入到部署与吞吐保障的完整链路。开发者可通过统一 API 接口完成定制化模型的训练、优化与上线，所有环节均支持程序化编排与状态轮询。该能力当前主要在华北2（北京）地域开放，部分部署方式（如 PTU）同步支持新加坡地域。

## 支持的模型与功能

- **微调支持**：文本生成（Qwen 系列）、图像生成（Wan2.7 / Qwen-Image）、视频生成（Wan2.x-i2v/kf2v）、语音合成（CosyVoice-v3-flash），均通过 `/api/v1/fine-tunes` 统一入口创建任务 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 微调模型文件导入平台，仅限北京地域 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：仅支持对 `qwen3.5-flash-2026-02-23` 全参微调模型进行量化压缩，产出低精度版本以降低 MU 部署规格与成本 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **部署方式**：
  - `lora`：LoRA 模型共享部署（按 [Token](../concepts/token.md) 计费），适用于图像/视频生成等场景；
  - `mu`：模型单元部署（后付费），语音合成模型强制使用此方式；
  - `dtu`：DTU 独占算力（预付费），需业务空间专属域名与额度申请；
  - `ptu`：预置吞吐预留（预/后付费），支持北京与新加坡两地 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

> **注意**：文档 16 与文档 23 均声明 DTU 部署“仅支持预付费”，但文档 16 的请求体示例中 `charge_type` 字段被截断，未明确写出 `pre_paid`；而文档 23 明确指出“DTU 部署仅支持预付费（`charge_type="pre_paid"`）”，应以文档 23 为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源示例 |
|------|------|------|------|----------|
| `model_name` | string | 是 | 微调产出模型 ID（如 `qwen3-14b-suffix-ft-...`），非基础模型名；部署时必须使用 `output.finetuned_output` 值 | [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md) |
| `plan` | string | 是 | 部署方案：`lora`/`mu`/`dtu`/`ptu_v2`；不同模型类型有强约束（如 CosyVoice 仅支持 `mu`） | [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md) |
| `training_type` | string | 是 | 微调方法：文本支持 `sft`/`dpo_full` 等；图像/视频/语音当前仅支持 `efficient_sft`（LoRA） | [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md) |
| `hyper_parameters` | object | 是（多数场景） | 包含 `n_epochs`/`batch_size`/`max_length`（文本）、`max_steps`（图像）、`lm_max_epoch`+`fm_max_epoch`（语音）等，直接影响训练费用与效果 | [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md) |
| `ptu_capacity` / `dtu_capacity` / `capacity` | object / integer | 是 | 吞吐预留需指定 `input_tpm`/`output_tpm`；DTU 需 `sku_code`+`template_code`；LoRA 部署仅需整数 `capacity`（推荐为 1） | [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |

## 使用方式

1. **微调**：调用 `POST /api/v1/fine-tunes`，传入 `model`、`training_type` 和 `hyper_parameters`，轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，提取 `output.finetuned_output`。
2. **压缩（可选）**：对全参微调模型调用 `/api/v1/fine-tunes/compress/jobs`，轮询至 `SUCCEEDED` 后获取 `quantized_output`。
3. **部署**：
   - LoRA 模型：`POST /api/v1/deployments`，`plan=lora`，`capacity=1`；
   - MU 模型（如语音）：`plan=mu`，指定 `deploy_spec`（如 `MU5`）与 `capacity`（须为 `base_capacity` 整数倍）；
   - DTU 模型：使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`），`plan=dtu`，传 `sku_code`/`template_code`/`dtu_capacity`；
   - PTU 吞吐预留：`POST /api/v1/deployments`，`plan=ptu`，指定 `service_tier`（`ptu_fast` 或 `ptu_default`）与 `ptu_capacity`。
4. **验证部署**：调用 `GET /api/v1/deployments/{deployed_model}`，等待 `status=RUNNING` 后即可调用推理接口。

## 限制和注意事项

- **地域限制**：微调、模型导入、模型压缩、MU/DTU 部署均**仅在北京地域可用**；PTU 吞吐预留与部分 `ptu_v2` 部署支持北京与新加坡 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型约束**：模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参微调模型，LoRA 模型、基础模型、第三方模型均不支持 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)。
- **状态检查**：HTTP 200 不代表操作成功。吞吐预留创建接口返回 `output.operation_status=FAILED` 时仍为 HTTP 200，必须检查响应体中的 `operation_status` 和 `error_code` 字段 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **部署后不可逆操作**：压缩后的模型不支持继续微调或二次压缩；DTU 续费与自动续费变更仅支持控制台操作，API 不支持 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。
- **命名规范**：`suffix`（部署后缀）与 `output_model_suffix`（压缩后缀）均仅支持小写字母和数字，长度上限分别为 24 和 8 位。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)


