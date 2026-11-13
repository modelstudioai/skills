# model production

`model production` 指在百炼平台完成模型的全生命周期管理，涵盖微调训练、导入、压缩、部署及智能路由等核心环节。该流程支持文本、图像、视频、语音等多种模态，面向开发者提供标准化 API 接口与明确的地域/权限约束。所有操作均需通过百炼 API Key 鉴权，并严格遵循各环节的地域可用性与计费模式要求。

## 支持的模型/功能

- **微调训练**：支持文本生成（SFT/CPT/DPO）、图像生成（文生图/图生图）、视频生成（首帧/首尾帧图生视频）、语音合成（CosyVoice）四类任务，统一使用 `POST /api/v1/fine-tunes` 接口提交；强化学习（RL）与 OPD 蒸馏训练需通过 DashScope SDK/CLI 提交，**不支持 REST API** [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型导入**：支持将 OSS 中的全参或 LoRA 调优模型文件导入平台，仅限华北2（北京）地域 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 基础模型的全参调优产出进行量化压缩，LoRA 模型和已量化模型不支持 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **智能路由**：提供效果优先（`EFFECT_FIRST`）与成本优先（`COST_FIRST`）两种策略，动态调度至最优备选模型（如 `qwen3.8-flash`, `qwen3.7-plus`），仅支持后付费 [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)。
- **部署方式**：覆盖 DTU（独占吞吐，预付费）、MU（模型单元）、PTU（预置吞吐，北京/新加坡）、LoRA 共享部署（按 Token 计费）等多种模式，不同模式适用地域与参数结构差异显著。

## 关键参数

- **地域约束**：绝大多数生产 API（微调、导入、部署、压缩）**仅在华北2（北京）开放**；PTU 与智能路由支持北京+新加坡；DTU 部署必须使用业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）且仅限北京。
- **模型标识**：
  - 微调产出模型名取自响应体 `output.finetuned_output`；
  - 导入模型名取自 `output.model_name`；
  - 部署时 `model_name` 必须为上述生成的完整 ID，**不可用基础模型名**（如 `qwen3-14b`）。
- **部署必填字段**：
  - `plan`：决定计费与资源模型（`dtu`/`mu`/`lora`/`ptu`/`mr`）；
  - `charge_type`：DTU 固定为 `pre_paid`，智能路由与 MU/PTU 多为 `post_paid`；
  - `capacity`：图像/视频/语音部署需显式指定（推荐 1），DTU 则需 `dtu_capacity.{input/output_tpm}`；
  - `aigc_config`：视频生成部署必需，控制提示词来源与模板 [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)。
- **超参数共性**：`n_epochs`（文本/语音）、`max_steps`（图像）、`batch_size` 等直接影响训练耗时与费用，文档中均标注“**重要**该参数影响[训练计费](raw/model-user-guide/test-1/model-training-and-deployment-billing.md)”。

## 使用方式

1. **准备环境**：获取并配置北京地域的 API Key，确认子账号已授予 `model:Train`, `model:Deploy`, `model:Invoke` 权限。
2. **训练/导入模型**：
   - 文本/图像/视频/语音：调用对应 `/api/v1/fine-tunes` 接口创建任务 → 轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED` → 提取 `output.finetuned_output`；
   - 自定义模型：调用 `/api/v1/custom_models/import` → 轮询至 `status=SUCCESSED` → 提取 `output.model_name`。
3. **（可选）压缩模型**：仅限 `qwen3.5-flash-2026-02-23` 全参调优模型，调用 `/api/v1/fine-tunes/compress/jobs` → 轮询至 `SUCCEEDED` → 提取 `output.quantized_output`。
4. **部署服务**：
   - 确认目标部署方式（如 `lora` for LoRA, `mu` for CosyVoice, `dtu` for dedicated GPU）；
   - 构造 `POST /api/v1/deployments` 请求体，填入 `model_name`, `plan`, `capacity`（或 `dtu_capacity`）等必填字段；
   - 对于 PTU/智能路由，注意切换域名（`dashscope-intl.aliyuncs.com` 或 `maas.aliyuncs.com`）；
   - 轮询 `/api/v1/deployments/{deployed_model}` 直至 `status=RUNNING`。
5. **调用服务**：使用 `deployed_model` 作为模型 ID，通过标准推理接口（如 `/api/v1/services/...`）发起请求。

> **注意**：文档 17（文本部署）与文档 18（图像部署）均声明“仅在华北2（北京）地域开放”，但文档 25（模型部署 API 参考）明确指出“PTU 等部署方式支持北京与新加坡地域”。此处存在矛盾——实际应以具体部署方式为准：PTU 和智能路由确支持新加坡，而 MU/DTU/LoRA 部署仍仅限北京。开发者需根据 `plan` 值选择对应地域与域名。

## 限制和注意事项

- **地域强绑定**：API Key、请求域名、OSS Bucket 地域必须一致。例如，北京 API Key 无法调用新加坡 `dashscope-intl.aliyuncs.com` 的微调接口；OSS 挂载训练集时，`region` 参数必须与 API Key 所属地域匹配 [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)。
- **状态轮询必要性**：所有[异步任务](../concepts/asynchronous-task.md)（微调、导入、压缩、部署）均需主动轮询查询状态，HTTP 200 不代表任务成功，必须检查响应体 `output.status` 字段 [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)。
- **模型权限隔离**：智能路由返回的 `supported_candidate_model_ids` 仅为平台能力列表，**不保证当前业务空间已获调用授权**；无权限模型会在路由时被实时过滤，调用失败而非静默降级。
- **部署命名冲突**：`suffix` 参数用于避免部署标识重复，若省略则由系统自动生成；但 `display_name`（文本部署）或 `name`（语音部署）为控制台展示名，不影响调用标识。
- **DTU 特殊要求**：必须使用业务空间专属域名与对应 Workspace API Key；续费与自动续费变更**仅支持控制台操作**，API 不提供相关接口 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。

## 来源文档

- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
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
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)


