# model production

`model production` 是百炼平台面向模型全生命周期的生产级能力集合，覆盖模型微调（Fine-tuning）、压缩（Quantization）、导入（Import）、部署（Deployment）及吞吐预留（Throughput Reservation）等核心环节。所有能力均通过统一 OpenAPI 接口提供，支持开发者在华北2（北京）地域完成端到端的模型定制与服务化，适用于文本、图像、视频、语音等多模态场景。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务，对应不同基准模型与训练范式。文本生成支持 `cpt`/`sft`/`dpo_full` 等多种训练类型；图像/视频/语音生成当前仅支持 `efficient_sft`（LoRA 高效微调）[文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型压缩**：仅支持对基于 `qwen3.5-flash-2026-02-23` 的**自定义全参调优模型**进行量化压缩，不支持 LoRA 模型或已量化模型 [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)。
- **模型导入**：支持从 OSS 导入全参（`full`）或 LoRA（`lora`）格式的调优模型文件，导入后可直接部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型部署**：支持 `mu`（模型单元）、`lora`（LoRA 共享）、`ptu`（预置吞吐）三种部署方案，适配不同性能与成本需求。各模态部署接口统一使用 `/api/v1/deployments` 路径，但参数结构差异显著 [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)。
- **吞吐预留（TPU）**：为已部署模型提供确定性推理吞吐保障，支持按预付费（`pre_paid`）或后付费（`post_paid`）购买输入/输出 kTPM 容量 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

> **注意**：文档中多次声明“仅在华北2（北京）地域可用”，但[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)明确列出弗吉尼亚（`us-east-1`）地域 Endpoint，且未限定地域。实际使用时需以目标地域的模型与购买限制为准，避免因地域不匹配导致调用失败。

## 关键参数

| 功能 | 关键参数 | 说明 | 约束 |
|--------|-----------|------|------|
| **微调通用** | `model`, `training_type`, `hyper_parameters` | `model` 为基准模型 ID 或上游调优产出 ID；`training_type` 决定训练范式；`hyper_parameters` 中 `n_epochs`/`batch_size`/`max_length`（文本）或 `max_steps`/`learning_rate`（图像/视频）为必填项 | `n_epochs` 影响训练费用，数据量 < 10,000 推荐 3~5 次 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md) |
| **部署（mu）** | `plan=mu`, `deploy_spec`, `capacity`, `billing_method` | `deploy_spec`（如 `MU1`/`MU5`）决定硬件规格；`capacity` 必须为 `base_capacity` 的整数倍（如 `MU2` 需为 8 的倍数） | `enable_thinking`、`max_context_length`、`rpm_limit` 等为部分模型可选扩展参数 |
| **部署（lora）** | `plan=lora` | 无需 `deploy_spec` 和 `capacity`，按 [Token](../concepts/token.md) 用量计费 | 仅适用于 LoRA 微调模型，不支持全参模型 |
| **部署（ptu）** | `plan=ptu`, `ptu_capacity` | `ptu_capacity` 包含 `input_tpm` 和 `output_tpm`（单位：kTPM），默认值为 `10000`/`1000` | `ptu_fast`（高速）和 `ptu_default`（标速）档位支持不同付费周期，`ptu_fast` 不支持 8 小时时段 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| **视频/图像部署** | `aigc_config`（视频） | 视频部署必需，控制提示词来源（`use_input_prompt`）及模板（`prompt`/`lora_prompt_default`） | `prompt` 会覆盖调用时传入的 [prompt](../guides/prompt.md) 参数 |

## 使用方式

1. **准备环境**：确保使用华北2（北京）地域的 API Key，并配置 `Authorization: Bearer ${YOUR_API_KEY}` 与 `Content-Type: application/json` 请求头。
2. **微调模型**：
   - 文本：调用 `POST /api/v1/fine-tunes` 创建任务，轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，获取 `finetuned_output`。
   - 图像/视频/语音：同上，注意各模型超参数必填项差异（如视频需 `n_epochs`，图像需 `max_steps`）。
3. **（可选）压缩模型**：仅限 `qwen3.5-flash-2026-02-23` 全参模型，先 `GET /api/v1/fine-tunes/compress/templates` 获取 `template_id`，再 `POST /api/v1/fine-tunes/compress/jobs` 创建任务，轮询至 `SUCCEEDED` 后取 `quantized_output`。
4. **部署模型**：
   - 全参/压缩模型：`plan=mu`，指定 `deploy_spec` 与 `capacity`。
   - LoRA 模型：`plan=lora`，无需 `deploy_spec`。
   - 吞吐预留：`plan=ptu`，设置 `ptu_capacity`。
   - 所有部署均调用 `POST /api/v1/deployments`，成功响应中 `output.deployed_model` 为调用标识。
5. **验证部署**：调用 `GET /api/v1/deployments/{deployed_model}` 轮询，当 `status=RUNNING` 时表示就绪。

## 限制和注意事项

- **地域限制**：微调、压缩、导入、部署（除吞吐预留外）所有 API 均**仅在华北2（北京）地域可用**。跨地域调用将失败，需确保 API Key、Endpoint、OSS Bucket 地域一致。
- **吞吐预留特殊性**：吞吐预留 API 支持弗吉尼亚（`us-east-1`）等多地，但容量实例与模型必须位于同一地域，且模型需已在该地域完成部署。
- **HTTP 200 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，**必须检查响应体中的 `output.operation_status` 字段**（如 `SUCCEEDED`/`FAILED`），否则可能误用未生效的容量 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型命名与后缀**：部署时若需多次部署同一模型，必须通过 `suffix` 参数指定唯一后缀（≤8 字符，小写字母+数字），否则会因名称冲突失败。
- **资源释放**：部署服务一旦创建即开始计费（`mu`/`ptu` 方案），即使未调用。建议通过 `DELETE /api/v1/deployments/{deployed_model}` 及时释放不再使用的部署。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)


