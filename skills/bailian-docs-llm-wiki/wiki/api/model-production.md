# model production

`model production` 是百炼平台面向模型全生命周期管理的核心能力集合，覆盖模型微调（Fine-tuning）、压缩（Compression）、部署（Deployment）、吞吐预留（Throughput Reservation）与智能路由（Model Routing）等关键生产环节。所有能力均通过统一的 RESTful API 体系提供，支持开发者在生产环境中安全、可控地将定制模型投入服务。

## 支持的模型/功能

百炼 `model production` 支持多模态模型的端到端生产化，包括：

- **文本生成**：支持 Qwen 系列（如 `qwen3.8-flash`、`qwen3.7-plus`）的 SFT/CPT/DPO 微调，以及 LoRA 高效微调与全参微调 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)；
- **图像生成**：支持 Wan2.7 系列（如 `wan2.7-image-pro`）与 Qwen-VL 图像模型的微调，部署时推荐 `lora` 方式 [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)；
- **视频生成**：支持 Wan2.x 系列图生视频（`i2v`/`kf2v`）模型的 LoRA 微调，部署需配置 `aigc_config` 实现提示词模板化 [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)；
- **语音合成**：支持 CosyVoice-v3 系列模型的双网络（LM+FM）解耦微调，部署仅支持 `mu`（模型单元）方式，且必须指定 `deploy_spec`（如 `MU5`）[语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)；
- **智能路由**：支持跨模型效果/成本优先的动态路由服务，仅限华北2（北京）与新加坡地域，且**仅支持后付费**（`charge_type="post_paid"`）[智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)；
- **吞吐预留**：提供独占算力保障能力（DTU），支持预付费容量购买、扩缩容、续订与溢出策略配置 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)；
- **模型压缩**：支持对自定义全参微调模型（如 `qwen3.5-flash-2026-02-23-ft-*`）进行量化压缩，降低推理显存与成本 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。

> **注意**：文档 16（文本生成-部署模型）与文档 25（模型部署 API 参考）对 DTU 部署的域名要求存在不一致：前者明确要求使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`），而后者在“前提条件”中仅强调“DTU 部署的请求需使用部署所在业务空间、地域对应的 `maas.aliyuncs.com` 业务空间域名”，未明确排除 `dashscope.aliyuncs.com`。实际调用 DTU 接口时，**必须使用业务空间专属域名**，否则将返回鉴权或资源定位错误。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 来源示例 |
|------|------|------|------|----------|
| `model_name` | string | 是 | 待部署/微调的模型 ID（非基础模型名），如 `qwen3-14b-suffix-ft-202410291653-1c7f`；微调产出模型取自 `output.finetuned_output`，导入模型取自 `output.model_name` | [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md) |
| `plan` | string | 是 | 部署方案：`mu`（模型单元）、`lora`（LoRA 共享）、`dtu`（独占吞吐）、`mr`（智能路由） | [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md) |
| `charge_type` | string | 是 | 计费类型：`pre_paid`（DTU 必填）、`post_paid`（MR/mu/lora 默认） | [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| `dtu_capacity` | object | 是（DTU） | 吞吐容量对象，含 `input_tpm` 与 `output_tpm` 字段，步长与上限依模型而异 | [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| `aigc_config` | object | 是（视频生成） | 视频部署必需，控制提示词来源（`use_input_prompt`）与模板（`prompt`/`lora_prompt_default`） | [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md) |
| `deploy_spec` | string | 是（语音合成） | CosyVoice 部署必需，指定规格如 `MU5` 或 `MU2`，决定 `capacity` 的倍数约束 | [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md) |

## 使用方式

1. **微调训练**：  
   - 调用 `/api/v1/fine-tunes` 创建任务（文本/图像/视频/语音各类型参数不同）；  
   - 通过 `GET /api/v1/fine-tunes/{job_id}` 轮询状态，确认 `status=SUCCEEDED`；  
   - 从响应 `output.finetuned_output` 获取产出模型 ID。

2. **模型压缩（可选）**：  
   - 先调用 `/api/v1/fine-tunes/compress/templates` 获取模板；  
   - 再调用 `/api/v1/fine-tunes/compress/jobs` 创建压缩任务；  
   - 轮询至 `SUCCEEDED` 后，使用 `output.quantized_output` 作为新模型 ID 部署。

3. **模型部署**：  
   - 构造 `POST /api/v1/deployments` 请求体，按 `plan` 填写对应字段（如 `dtu_capacity`、`aigc_config`、`deploy_spec`）；  
   - 使用**部署目标工作空间的专属域名**（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）和该空间的 API Key；  
   - 通过 `GET /api/v1/deployments/{deployed_model}` 轮询，待 `status=RUNNING` 后即可调用。

4. **吞吐预留与路由**：  
   - 吞吐预留：使用 `/api/v1/deployments`（`plan=dtu`）创建，后续通过 `/capacity-instances` 管理实例；  
   - 智能路由：使用 `/api/v1/deployments`（`plan=mr`）创建，需先调用 `/model-routing/versions` 查询可用路由版本。

> **注意**：所有异步操作（微调、压缩、部署、吞吐变更）均返回 `operation_id` 或 `job_id`，**HTTP 200 不代表操作成功**。必须轮询查询终态（如 `SUCCEEDED`/`RUNNING`），并检查 `output.status` 与 `output.error_code` 字段，详见 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) 中的“重要”提示。

## 限制和注意事项

- **地域限制严格**：  
  - 微调（Fine-tuning）、模型导入、模型压缩、所有部署 API（除 DTU 外）**仅在华北2（北京）地域开放**；  
  - DTU 吞吐预留与智能路由（MR）支持北京与新加坡，但 MR **不支持其他地域**；  
  - 新加坡地域部署仅支持 `mu`/`lora` 方式，且必须使用 `dashscope-intl.aliyuncs.com` 域名 [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)。

- **权限与配额**：  
  - 子账号（RAM 用户）需被授予 `AliyunBailianFullAccess` 或精细化权限（含 `bailian:CreateFineTuneJob`, `bailian:DeployModel` 等）；  
  - DTU 需提前在控制台开通功能并申请 GPU 资源额度，否则创建失败；  
  - 吞吐预留实例的 `input_tpm`/`output_tpm` 有最小值、步长及单实例上限，具体以 `/deployments/models?plan=dtu` 接口返回为准。

- **模型与部署兼容性**：  
  - LoRA 微调模型**不可用于 DTU 部署**，仅支持 `lora` 或 `mu` 方式；  
  - CosyVoice 模型**仅支持 `mu` 部署**，不支持 `lora` 或 `dtu`；  
  - 智能路由服务**不支持 LoRA 模型作为备选模型**，仅接受已部署的 `mu`/`dtu` 服务或系统原生模型。

- **安全与稳定性**：  
  - 所有 API 请求必须携带 `Authorization: Bearer <api-key>`，API Key 与工作空间及地域强绑定，不可跨地域复用；  
  - 吞吐预留的容量变更（扩缩容/续订）为异步操作，同一 `deployed_model` 下的操作按顺序排队，新请求可能被拒绝；  
  - 模型部署后，`deployed_model` 即为服务唯一标识，调用推理 API 时需使用此值而非 `model_name`。

## 来源文档

- [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
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
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)


