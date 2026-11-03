# model production

`model production` 是百炼平台中模型从训练、压缩、部署到高可用服务交付的完整生命周期管理能力集合，涵盖微调（Fine-tuning）、导入（Import）、压缩（Compression）、部署（Deployment）及吞吐预留（Throughput Reservation）等核心环节。所有操作均通过标准化 REST API 实现，支持开发者在生产环境中自动化构建和管理专属模型服务。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成四类模态。文本生成支持 `sft`/`cpt`/`dpo_full`/`dpo_lora` 等训练类型；图像/视频/语音生成当前仅支持 `efficient_sft`（LoRA 微调）[文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。  
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 微调模型文件导入平台，导入后可直接部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。  
- **模型压缩**：仅支持对华北2（北京）地域的 `qwen3.5-flash-2026-02-23` 全参微调模型进行量化压缩，降低推理显存占用并减小 MU 部署规格 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。  
- **部署方式**：支持多种计费与资源隔离模式：  
  - `lora`：LoRA 共享部署，按 [Token](../concepts/token.md) 用量后付费（适用于 LoRA 微调模型）；  
  - `mu`：模型单元（Model Unit），按实例规格（如 `MU5`）后付费（适用于 CosyVoice 等语音模型）；  
  - `dtu`：独占吞吐（Dedicated Throughput Unit），预付费、独占 GPU 资源（需控制台开通额度）；  
  - `ptu_v2`：预置吞吐量 V2（即吞吐预留），支持预/后付费及多档性能（`ptu_fast`/`ptu_default`）。  

> **注意**：文档 14 与文档 27 均声明 DTU 部署必须使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）及对应工作空间 API Key，但文档 14 的请求示例仍使用 `dashscope.aliyuncs.com`，该示例已过时，应以文档 27 的说明为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_name` | string | 是 | 待部署/压缩/微调的模型标识：微调产出模型取自 `output.finetuned_output`；导入模型取自 `output.model_name`；基础模型名需与控制台一致。 |
| `plan` | string | 是 | 部署方案，决定计费与资源模型，如 `lora`、`mu`、`dtu`、`ptu_v2`。 |
| `training_type` | string | 是（微调） | 文本生成支持 `sft`/`cpt`/`dpo_lora`；图像/视频/语音生成固定为 `efficient_sft`。 |
| `hyper_parameters` | object | 是（微调） | 含 `n_epochs`/`batch_size`/`max_length`（文本）、`max_steps`/`learning_rate`（图像）、`n_epochs`/`fm_max_epoch`（语音）等，具体字段依模型类型而异。 |
| `ptu_capacity` / `dtu_capacity` / `capacity` | object / integer | 是（部署） | 吞吐预留需指定 `input_tpm`/`output_tpm`；DTU 同理；`lora`/`mu` 部署则传整数 `capacity`（如 1）。 |
| `service_tier` | string | 否（吞吐预留） | 性能档位：`ptu_fast`（高速，默认）或 `ptu_default`（标速）；`ptu_fast` 支持后付费，`ptu_default` 仅支持预付费且支持 8 小时时段购买。 |

## 使用方式

1. **微调**：调用 `POST /api/v1/fine-tunes` 创建任务（华北2 地域），轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，获取 `output.finetuned_output`。  
2. **导入**：调用 `POST /api/v1/custom_models/import` 提交 OSS 模型路径，轮询 `GET /api/v1/custom_models/{job_id}` 确认 `status=SUCCESSED`。  
3. **压缩**：先调用 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 创建任务，轮询 `GET /api/v1/fine-tunes/compress/jobs/{job_id}` 获取 `quantized_output`。  
4. **部署**：统一调用 `POST /api/v1/deployments`，根据 `plan` 传入对应参数：  
   - `lora`：传 `model_name` + `capacity` + `plan=lora`；  
   - `mu`：传 `model_name` + `plan=mu` + `deploy_spec`（如 `MU5`）+ `capacity`；  
   - `dtu`：**必须使用业务空间域名**，传 `sku_code`/`template_code`/`dtu_capacity`；  
   - `ptu_v2`（吞吐预留）：传 `model_name` + `plan=ptu` + `service_tier` + `ptu_capacity` + `charge_type`。  
5. **验证部署**：调用 `GET /api/v1/deployments/{deployed_model}`，当 `output.status=RUNNING` 时即可调用。  

## 限制和注意事项

- **地域限制**：微调、导入、压缩、`mu`/`dtu` 部署仅支持**华北2（北京）**；`ptu_v2`（吞吐预留）及部分基础模型部署支持北京与新加坡。  
- **模型兼容性**：模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参微调模型，不支持 LoRA、基础模型或第三方模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)。  
- **API 域名与鉴权**：DTU 部署必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）及该工作空间的 API Key；其他部署方式可使用 `dashscope.aliyuncs.com` 或 `dashscope-intl.aliyuncs.com`。  
- **状态检查**：HTTP 200 不代表操作成功——吞吐预留创建、部署等接口返回的 `output.operation_status` 或 `output.status` 必须显式检查为 `SUCCEEDED`/`RUNNING`，否则不可调用 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。  
- **参数不可逆**：压缩后的模型不可继续微调，也不可二次压缩；吞吐预留的 `service_tier`（`ptu_fast`/`ptu_default`）创建后不可变更。

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
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)


