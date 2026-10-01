# model production

`model production` 指在百炼平台上将训练/调优后的模型转化为可稳定、可扩展、可计费的在线推理服务的完整流程，涵盖模型微调、压缩、导入、部署及吞吐预留等关键环节。该流程面向开发者提供标准化 API 接口，支持文本、图像、视频、语音四类生成式模型的全生命周期管理。所有生产操作当前均**强制限定在华北2（北京）地域**，需使用对应地域的 API Key 与 Endpoint。

## 支持的模型与功能

百炼 `model production` 支持以下生成任务类型的模型定制与服务化：

- **文本生成**：支持全参微调（`sft`, `cpt`, `dpo_full`, `dpo_lora`）、LoRA 高效微调及模型压缩（量化），适用于 Qwen 系列大语言模型 [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)；
- **图像生成**：支持 `wan2.7-image-pro`、`qwen-image-2.0` 等基准模型的 LoRA 微调（`efficient_sft`），并提供专用部署配置 [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)；
- **视频生成**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview` 等图生视频模型的 LoRA 微调，部署时需配置 `aigc_config` 实现提示词模板化生成 [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)；
- **语音合成（CosyVoice）**：支持 `cosyvoice-v3-flash` 的双网络（LM + FM）独立微调，部署仅支持 `mu` 方案，需指定 `MU5` 或 `MU2` 规格 [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)。

> **注意**：文档 17（文本部署）与文档 19（图像部署）对 `plan` 参数的约束不一致——前者明确支持 `mu`/`lora`/`ptu` 三类方案，后者仅推荐 `lora`；但文档 23（语音部署）则强制要求 `plan=mu`。实际选型应以具体模型类型为准：**LoRA 类模型优先用 `lora`，全参/量化/语音模型必须用 `mu`，吞吐保障场景用 `ptu`**。

## 关键参数

| 功能 | 必填参数 | 说明 | 来源示例 |
|------|----------|------|----------|
| **微调任务创建** | `model`, `training_type`, `hyper_parameters` | `hyper_parameters` 中各字段必填性因模型而异：文本需 `n_epochs`/`batch_size`/`max_length`；图像需 `max_steps`/`learning_rate`/`generation_type`；语音需 `lm_max_epoch`/`fm_max_epoch` 等双网络参数 | [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md) |
| **模型部署** | `model_name`, `plan`, `capacity`（`mu`/`lora`）或 `ptu_capacity`（`ptu`） | `capacity` 含义不同：`mu` 下为资源单元数（如 `MU1` 的倍数），`lora` 下为实例数（通常为 1）；`ptu_capacity` 单位为 kTPM（1000 Tokens/分钟） | [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| **吞吐预留（PTU）** | `model_name`, `plan="ptu"`, `ptu_capacity.{input_tpm,output_tpm}` | `ptu_capacity` 为绝对容量值（非增量），扩缩容需重发完整对象；`service_tier` 控制性能档位（`ptu_fast`/`ptu_default`） | [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |

## 使用方式

1. **准备环境**：仅华北2（北京）地域可用；获取该地域 API Key 并配置 `DASHSCOPE_API_KEY` 环境变量；子账号需授予模型训练与部署权限 [获取 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
2. **创建微调任务**：调用 `POST /api/v1/fine-tunes`，传入模型 ID、数据集 ID/路径及超参，轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，提取 `finetuned_output`；
3. **（可选）模型压缩/导入**：对全参微调模型，可调用 `/api/v1/fine-tunes/compress/jobs` 进行量化；对 OSS 存储的模型，调用 `/api/v1/custom_models/import` 导入；
4. **部署模型**：
   - LoRA 模型：`POST /api/v1/deployments`，`plan=lora`, `capacity=1`；
   - 全参/量化/语音模型：`plan=mu`, `deploy_spec`（如 `MU5`）, `capacity`（按规格要求）；
   - 吞吐保障场景：`plan=ptu`, `ptu_capacity`，返回 `deployed_model` 即 ModelCode；
5. **验证服务**：调用 `GET /api/v1/deployments/{deployed_model}` 轮询 `status=RUNNING` 后，即可用 `deployed_model` 作为模型 ID 发起推理请求。

## 限制和注意事项

- **地域强约束**：所有微调、部署、压缩、导入 API 均**仅在华北2（北京）地域生效**，跨地域调用将失败（文档 4/7/10/11/13/14/17/19/21/23/24 均明确声明）；
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作接口返回 HTTP 200 仅表示请求接收，**必须检查响应体中 `output.operation_status` 字段**（可能为 `FAILED`），否则可能导致容量未生效 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)；
- **模型命名与后缀**：部署时若需多次部署同一模型，`suffix` 参数必须显式指定且全局唯一（长度 ≤8，仅小写字母+数字）；压缩产出模型的 `quantized_output` 命名含固定前缀规则，不可自定义；
- **计费起点**：`mu` 方案部署成功即开始计费（即使未调用），`lora` 和 `ptu` 方案按实际用量/预留容量计费；
- **Checkpoint 管理**：语音合成模型的 Checkpoint `step` 为 `LM_epoch × 10000 + FM_epoch`，排序与导出需按此逻辑理解 [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)


