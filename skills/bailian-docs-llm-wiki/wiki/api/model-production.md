# model production

`model production` 是百炼平台中模型从训练、压缩、部署到高可用推理服务的全生命周期管理能力集合，涵盖微调（Fine-tuning）、模型导入、量化压缩、专属部署（含 DTU 吞吐预留）、智能路由等核心环节。所有能力均通过标准化 OpenAPI 提供，支持开发者在生产环境中构建可控、可扩展、可计费的 AI 服务。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成（Qwen 系列）、图像生成（Wan2.7 / Qwen-Image）、视频生成（Wan2.x-i2v/kf2v）、语音合成（CosyVoice）四大模态。各模态均提供独立的创建、查询、取消、日志与 Checkpoint 管理接口，且全部仅限华北2（北京）地域使用 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 调优模型文件导入平台，导入成功后即可部署。该功能当前仅在北京 Region 开放 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：通过量化技术降低自定义全参调优模型的显存占用与推理成本，目前仅支持 `qwen3.5-flash` 和 `qwen3.6-plus` 基础模型衍生的全参模型，LoRA 模型不支持 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。
- **专属部署**：提供多种部署模式：
  - `lora`：LoRA 共享部署，按 [Token](../concepts/token.md) 后付费；
  - `mu`（模型单元）：资源隔离部署，适用于 CosyVoice 等对延迟敏感场景；
  - `dtu`（独占吞吐）：预付费、TPM 容量预留，独占 GPU 资源，需使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）；
  - `mr`（智能路由）：基于效果/成本策略自动调度多个备选模型，仅支持后付费 [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)。

> **注意**：文档 16（文本生成-部署模型）称 DTU 部署“新购独占部署优先选择”，而文档 24（模型部署 API 参考）明确指出“DTU 部署仅支持预付费（`charge_type="pre_paid"`），不支持后付费创建”，但文档 18（图像生成-部署模型）和文档 20（视频生成-部署模型）的示例请求体中未包含 `charge_type` 字段，且其 `plan=lora` 示例隐含后付费逻辑。实际开发中必须按部署方式严格传入 `charge_type`：`dtu` 必须为 `pre_paid`，`lora`/`mu`/`mr` 必须为 `post_paid`。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 来源示例 |
|------|------|------|------|----------|
| `model_name` | string | 是 | 待部署/调优的模型 ID；微调产出取 `output.finetuned_output`，导入产出取 `output.model_name` | [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md) |
| `plan` | string | 是 | 部署方案：`lora`/`mu`/`dtu`/`mr`；不同模态支持不同 plan（如 CosyVoice 仅支持 `mu`） | [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md) |
| `capacity` | integer | 是（除 `dtu` 外） | 实例数量（`lora`/`mu`）或 DTU 容量对象（`dtu`）；`dtu` 需同时指定 `input_tpm` 和 `output_tpm` | [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| `training_type` | string | 是（微调） | 微调方法：`sft`/`cpt`/`dpo_full`/`efficient_sft`；图像/视频/语音仅支持 `efficient_sft` | [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md) |
| `hyper_parameters` | object | 是（微调） | 包含 `n_epochs`/`batch_size`/`max_length`（文本）、`max_steps`（图像）、`n_epochs`（视频）、`lm_max_epoch`/`fm_max_epoch`（语音）等关键超参 | [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md) |

## 使用方式

1. **准备环境**：获取并配置华北2（北京）地域的 API Key，确保子账号已授予 `AliyunBailianFullAccess` 或最小化权限策略。
2. **训练模型**：
   - 调用对应模态的 `POST /api/v1/fine-tunes` 创建微调任务；
   - 使用 `GET /api/v1/fine-tunes/{job_id}` 轮询状态，确认 `status=SUCCEEDED`；
   - （可选）调用 `GET /api/v1/fine-tunes/{job_id}/checkpoints` 获取最优 Checkpoint 的 `model_name`。
3. **（可选）压缩模型**：对全参调优模型调用 `/api/v1/fine-tunes/compress/jobs` 创建量化任务，轮询至 `SUCCEEDED` 后获取 `quantized_output`。
4. **部署服务**：
   - 构造 `POST /api/v1/deployments` 请求体，根据 `plan` 设置对应字段（如 `dtu_capacity`、`aigc_config`、`deploy_spec`）；
   - 注意：`dtu` 部署必须使用业务空间专属域名和对应 Workspace 的 API Key；
   - 调用 `GET /api/v1/deployments/{deployed_model}` 轮询，待 `status=RUNNING` 后即可调用。
5. **管理容量（DTU）**：使用吞吐预留 API 管理 `capacity-instances`，包括扩缩容、续订、设置溢出策略等 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

## 限制和注意事项

- **地域强约束**：所有微调、导入、压缩、Checkpoint 管理及大部分部署 API **仅支持华北2（北京）地域**；新加坡地域仅部分部署接口（如 `mu`）可用，且需使用 `dashscope-intl.aliyuncs.com` 域名。
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求已接收，必须检查响应体中 `output.operation_status`（如 `SUCCEEDED`/`FAILED`）及错误字段，否则可能使用未生效的容量 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型兼容性限制**：
  - 模型压缩仅支持特定基础模型（`qwen3.5-flash`/`qwen3.6-plus`）的**全参调优模型**，LoRA 模型、已量化模型、非百炼托管模型均不支持；
  - CosyVoice 部署仅支持 `mu` 方式，且 `deploy_spec` 必须匹配 `MU5`/`MU2` 规格与 `capacity` 倍数要求；
  - 智能路由（`mr`）仅支持后付费，且路由版本与备选模型需通过 `/model-routing/versions` 接口动态查询，不保证控制台中可见的模型均具备调用权限。
- **命名与标识**：`deployed_model`（部署标识）与 `model_name`（模型 ID）是两个独立字段，不可混用；`deployed_model` 由平台生成，用于后续查询/扩缩容/删除；`model_name` 是模型本身的唯一标识，用于部署输入与推理调用。

## 来源文档

- [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)


