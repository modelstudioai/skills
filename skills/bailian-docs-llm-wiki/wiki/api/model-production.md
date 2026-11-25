# model production

`model production` 是百炼平台面向模型全生命周期的生产级能力集合，覆盖模型微调、压缩、部署、吞吐预留与智能路由等核心环节。所有能力均通过标准化 RESTful API 提供，支持开发者在生产环境中构建稳定、可控、可扩展的模型服务。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务。各模态均有专属创建接口，如 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)、[视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md) 等。所有微调任务均仅限华北2（北京）地域。
- **模型导入与压缩**：支持从 OSS 导入自定义模型（仅北京地域），并提供量化压缩能力以降低推理成本；[模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md) 仅支持全参调优模型（如 `qwen3.5-flash-2026-02-23`），不支持 LoRA 模型。
- **部署方式**：支持多种部署模式：
  - `lora`：LoRA 共享部署（按 Token 计费），适用于轻量微调模型；
  - `mu`：模型单元（后付费），如 CosyVoice 必须使用 `mu` 部署；
  - `dtu`：独占吞吐（预付费），需通过业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）调用，且必须使用对应工作空间的 API Key；
  - `mr`：智能路由（后付费），复用 `/api/v1/deployments` 接口，通过 `plan="mr"` 区分，当前仅支持华北2（北京）与新加坡地域。
- **高级能力**：吞吐预留（TPM Capacity Reservation）用于保障稳定低延迟推理；智能路由支持多模型策略调度（如 `EFFECT_FIRST`、`COST_FIRST`）。

> **注意**：文档 15（文本生成-部署模型）称 DTU “是模型单元（MU）的继任方案，新购独占部署优先选择”，但文档 26 明确指出“DTU 部署仅支持预付费（`charge_type="pre_paid"`），不支持后付费创建”，而 MU 为后付费。二者定位不同，并非简单替代关系，应按业务 SLA 与计费模型选型。

## 关键参数

- `plan`：部署类型标识，决定计费模式与资源隔离级别（`lora`/`mu`/`dtu`/`mr`），是所有部署接口的核心参数。
- `model_name`：待部署模型 ID（非基础模型名），通常来自微调任务响应的 `output.finetuned_output` 或模型导入任务的 `output.model_name`。
- `capacity`：实例数量，语义因 `plan` 而异——`lora`/`mu` 下为并发实例数；`dtu` 下需配合 `sku_code` 和 `template_code` 使用，由 `/deployments/models?plan=dtu` 接口返回。
- `aigc_config`：视频生成部署必需，控制提示词来源（`use_input_prompt=true/false`）及模板填充逻辑。
- `deploy_spec`：语音合成（CosyVoice）部署必需，指定 `MU5` 或 `MU2` 等模板规格，约束 `capacity` 取值倍数。
- `route_model_version`：智能路由创建时必需，需先调用 `/api/v1/deployments/model-routing/versions` 获取支持的版本及候选模型列表。

## 使用方式

1. **准备环境**：获取华北2（北京）地域的 API Key（部分能力如智能路由也支持新加坡），配置 `Authorization: Bearer <key>` 与 `Content-Type: application/json` 请求头。
2. **选择地域与域名**：
   - 北京：`https://dashscope.aliyuncs.com`
   - 新加坡：`https://dashscope-intl.aliyuncs.com`
   - DTU/mr/业务空间专属部署：必须使用 `https://{workspaceId}.{region}.maas.aliyuncs.com`
3. **典型流程**：
   - 微调：调用 `/api/v1/fine-tunes` → 轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED` → 获取 `finetuned_output`
   - 部署：调用 `/api/v1/deployments`（带 `plan` 和 `model_name`）→ 轮询 `/api/v1/deployments/{deployed_model}` 直至 `status=RUNNING`
   - 吞吐预留：调用 `/api/v1/deployments`（`plan=dtu`）创建预留 → 通过 `/capacity-instances` 叠加或扩缩容
   - 智能路由：先查 `/model-routing/versions` → 再 POST `/api/v1/deployments`（`plan=mr` + `route_model_version`）

> **注意**：文档 1（吞吐预留 API 参考）强调“HTTP 请求成功不等于容量操作成功”，所有写操作（如创建/扩缩容）必须轮询 `/operations/{id}` 确认 `operation_status=SUCCESS`，否则可能处于中间状态。

## 限制和注意事项

- **地域强绑定**：微调、模型导入、模型压缩、大部分部署 API 均**仅限华北2（北京）地域**；智能路由额外支持新加坡；DTU 部署必须使用业务空间专属域名，不可用 `dashscope.aliyuncs.com`。
- **权限要求**：RAM 子账号需显式授予模型调用、训练、部署权限，详见 [权限管理概述](../../model-user-guide/security-and-compliance/permission-management-overview.md)。
- **模型兼容性**：
  - 视频/图像/语音微调任务中，`training_type` 当前**仅支持 `efficient_sft`**（LoRA），与文本生成支持 `sft`/`dpo_full` 等多类型不同。
  - 模型压缩仅支持特定基础模型（`qwen3.5-flash-2026-02-23` 等），且**不支持 LoRA 或已量化模型**。
- **状态轮询必要性**：所有异步操作（微调、部署、压缩、吞吐预留变更）均需主动轮询状态接口（如 `/fine-tunes/{id}`、`/deployments/{id}`、`/operations/{id}`），不能依赖 HTTP 200。
- **DTU 特殊约束**：开通 DTU 需控制台申请额度；续费与自动续费开关**仅支持控制台操作**，API 不提供对应接口；不支持 `AssumedRoleUser` 身份调用。

## 来源文档

- [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
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
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)


