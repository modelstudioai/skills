# model production

`model production` 是百炼平台面向模型全生命周期的生产级能力集合，覆盖模型微调（Fine-tuning）、导入（Import）、压缩（Compression）、部署（Deployment）及吞吐预留（Throughput Reservation）等核心环节。所有能力均通过统一 OpenAPI 接口提供，支持华北2（北京）地域的自动化集成与编排，适用于文本、图像、视频、语音等多模态模型的规模化上线。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务。各类型对应专属 API 路径与超参数体系，例如文本生成使用 `POST /api/v1/fine-tunes` [创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)，而视频生成需指定 `task_type` 切换首帧/首尾帧模式。
- **模型导入与压缩**：支持从 OSS 导入全参或 LoRA 微调模型，并通过量化压缩降低推理成本；当前仅支持 `qwen3.5-flash-2026-02-23` 的全参模型量化 [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)。
- **部署方式**：提供三种部署方案：
  - `mu`（Model Unit）：资源专属，按单元时长计费，支持限流（`rpm_limit`, `tpm_limit`）与上下文扩展（`max_context_length`）；
  - `lora`：LoRA 共享部署，按 [Token](../concepts/token.md) 用量计费，适用于轻量级微调模型；
  - `ptu`（Pre-provisioned Throughput Unit）：预置吞吐量，按输入/输出 TPM 配额计费，适用于高稳定性、低延迟场景 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **吞吐预留**：独立于模型部署的容量层，通过 `plan: "ptu"` 创建，支持 `ptu_fast`（高速）和 `ptu_default`（标速）两档性能，可叠加购买、扩缩容与自动续订。

> **注意**：文档中多次声明“仅在华北2（北京）地域可用”，但[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)明确列出弗吉尼亚（`us-east-1`）地域 Endpoint，且未限定地域限制。实际调用需以目标地域的模型与购买限制为准，建议优先验证地域可用性。

## 关键参数

| 参数 | 作用 | 适用场景 | 示例值 |
|------|------|----------|--------|
| `model_name` | 模型唯一标识符 | 所有微调与部署请求必填 | `qwen3-14b`, `wan2.7-i2v-ft-xxx` |
| `plan` | 部署/预留方案 | `mu`, `lora`, `ptu` | `"ptu"`, `"mu"` |
| `ptu_capacity` | 吞吐配额（kTPM） | `plan=ptu` 时生效 | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` & `capacity` | 资源规格与数量 | `plan=mu` 时必填，`capacity` 需为 `base_capacity` 整数倍 | `"MU1"`, `4` |
| `training_type` | 微调方法 | 文本生成支持 `sft`, `dpo_lora`；其余模态当前仅支持 `efficient_sft` | `"efficient_sft"` |
| `aigc_config` | AIGC 提示词模板 | 视频生成部署必需，控制 [prompt](../guides/prompt.md) 生成逻辑 | `{ "use_input_prompt": false, "prompt": "..." }` |

## 使用方式

1. **准备环境**：获取并配置华北2（北京）地域的 API Key，确保子账号已授予 `AliyunBailianFullAccess` 或最小化权限策略。
2. **微调模型**：
   - 上传训练数据集（OSS 或 API 上传）；
   - 调用对应模态的 `POST /api/v1/fine-tunes`，传入 `model`, `training_type`, `hyper_parameters`；
   - 轮询 [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md) 接口确认 `status=SUCCEEDED`，获取 `finetuned_output`。
3. **部署服务**：
   - 对微调产出模型，调用 `POST /api/v1/deployments`，根据模型类型选择 `plan`：
     - LoRA 模型 → `plan=lora`（无需 `deploy_spec`）；
     - CosyVoice → `plan=mu` + `deploy_spec=MU5`；
     - 吞吐预留 → `plan=ptu` + `ptu_capacity`；
   - 轮询 [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md) 接口，等待 `status=RUNNING`。
4. **调用服务**：使用响应中返回的 `output.deployed_model` 作为 `model` 参数，向 `/api/v1/services/{deployed_model}/infer` 发起推理请求。

## 限制和注意事项

- **地域强约束**：微调、导入、压缩、部署（除吞吐预留外）所有 API 均**仅支持华北2（北京）地域**，跨地域调用将失败。吞吐预留虽提供 `us-east-1` Endpoint，但模型与容量购买限制仍以目标地域为准。
- **模型兼容性**：
  - 模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参微调模型，LoRA 模型不支持；
  - CosyVoice 部署强制要求 `plan=mu`，不支持 `lora` 或 `ptu` 方案；
  - `ptu` 预留不支持思考输出（`thinking_output_tpm`）单独配额，仅部分 `mu` 部署支持 `enable_thinking`。
- **操作幂等性与状态检查**：
  - HTTP 200 不代表操作成功，必须检查响应体中 `output.operation_status`（预留）或 `output.status`（部署/微调）字段；
  - 扩缩容、变配等异步操作需轮询查询接口，不可依赖响应时间。
- **命名与唯一性**：
  - `suffix`（部署后缀）全局唯一，长度 ≤8，仅小写字母与数字；
  - `deployed_model` 是调用入口，非 `model_name`，二者不可混用。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)


