# model production

`model production` 是百炼平台中模型从训练、压缩、部署到高性能推理服务的全生命周期管理能力集合，覆盖微调（Fine-tuning）、导入（Import）、压缩（Compression）、部署（Deployment）及吞吐预留（Throughput Reservation）等核心环节。所有操作均通过标准化 RESTful API 实现，支持开发者在生产环境中自动化构建和运维专属模型服务。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类模态的 LoRA/全参微调。其中文本生成支持 `sft`/`cpt`/`dpo_full`/`dpo_lora` 等多种训练类型；图像/视频/语音仅支持 `efficient_sft`（LoRA 高效微调）[文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型导入**：支持将 OSS 中存储的自定义调优模型（`full` 或 `lora` 类型）导入平台，导入成功后可直接部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：当前仅支持对华北2（北京）地域产出的 `qwen3.5-flash-2026-02-23` 全参微调模型进行量化压缩，降低部署规格（如从 MU1×2 降至 MU5），不支持 LoRA 模型或基础模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **部署方式**：按模态与场景差异提供多种部署方案：
  - 文本/图像/视频：推荐 `lora`（LoRA 共享部署，按 [Token](../concepts/token.md) 计费）；
  - 语音合成（CosyVoice）：仅支持 `mu`（模型单元）部署；
  - 高性能/低延迟场景：支持 `dtu`（DTU 独占算力，预付费）和 `ptu`（预置吞吐量，含 `ptu_fast`/`ptu_default` 档位）[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

> **注意**：文档 16（文本生成-部署模型）称 DTU/PTU 支持北京与新加坡，但文档 24（模型部署 API 参考）明确指出“DTU 与 MU 部署仅支持华北2（北京）”，且文档 17/19/22 均限定图像/视频/语音部署仅在北京可用。实际以文档 24 和各模态部署文档的“适用地域”为准：**DTU、MU、模型导入、模型压缩、所有微调任务均仅限华北2（北京）；PTU 吞吐预留是唯一明确支持北京与新加坡的部署方式**。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `model_name` | 待部署/微调的模型标识符；微调产出模型取 `output.finetuned_output`，导入模型取 `output.model_name` | `qwen3-14b-suffix-ft-202410291653-1c7f` | [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md) |
| `plan` | 部署方案，决定计费与资源模型 | `lora`, `mu`, `dtu`, `ptu` | [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md) |
| `service_tier` | PTU 吞吐预留档位 | `ptu_fast`（高速）, `ptu_default`（标速） | [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| `ptu_capacity` / `dtu_capacity` | 吞吐/算力容量配置对象，必含 `input_tpm` 和 `output_tpm` | `{"input_tpm": 10000, "output_tpm": 1000}` | [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| `training_type` | 微调方法 | `sft`, `efficient_sft`, `dpo_lora` | [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md) |
| `hyper_parameters` | 模型无关超参（如 `n_epochs`, `batch_size`, `max_length`）与模态特有超参（如图像 `max_pixels`、语音 `lm_max_epoch`） | `{ "n_epochs": 3, "batch_size": 32 }` | [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md) |

## 使用方式

1. **微调训练**：调用 `POST /api/v1/fine-tunes` 创建任务，指定 `model`、`training_type` 和 `hyper_parameters`；使用 `GET /api/v1/fine-tunes/{job_id}` 轮询状态，`status=SUCCEEDED` 后获取 `output.finetuned_output`。
2. **模型导入**：调用 `POST /api/v1/custom_models/import` 提交 OSS 模型路径；轮询 `GET /api/v1/custom_models/import/{job_id}` 直至 `status=SUCCESSED`。
3. **模型压缩**（仅北京）：先调用 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 创建压缩任务；轮询 `GET /api/v1/fine-tunes/compress/jobs/{job_id}`，成功后取 `output.quantized_output`。
4. **模型部署**：
   - LoRA/通用部署：`POST /api/v1/deployments`，传 `model_name`、`plan=lora`（或 `mu`/`ptu_v2`）及对应容量参数；
   - DTU 部署：必须使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`），传 `plan=dtu`、`sku_code`、`template_code`；
   - PTU 吞吐预留：`POST /api/v1/deployments`，传 `plan=ptu`、`service_tier`、`ptu_capacity` 等。
5. **验证部署**：调用 `GET /api/v1/deployments/{deployed_model}` 轮询，`status=RUNNING` 即可调用。

## 限制和注意事项

- **地域强约束**：微调、导入、压缩、MU/DTU 部署全部仅限华北2（北京）；PTU 吞吐预留是唯一支持北京与新加坡的部署方式；新加坡仅支持 `ptu_v2` 部署（见文档 16 和 24）。
- **API Key 绑定地域**：API Key 与地域强绑定，不可跨地域复用；DTU 部署必须使用业务空间专属域名及对应空间的 API Key [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **HTTP 200 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，必须检查响应体中 `output.operation_status` 字段是否为 `SUCCEEDED`，否则视为失败 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型兼容性**：压缩仅支持 `qwen3.5-flash-2026-02-23` 全参微调模型，不支持 LoRA、基础模型或第三方模型；语音合成（CosyVoice）部署仅支持 `mu` 方案，不支持 `lora` 或 `ptu`。
- **部署后缀与命名**：`suffix`（部署标识后缀）和 `display_name`（展示名）均有长度限制（分别 ≤24 和 ≤50 字符），且 `suffix` 仅在部分部署方式（如 PTU）中生效，DTU 部署使用 `sku_code`/`template_code` 控制规格。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
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
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)


