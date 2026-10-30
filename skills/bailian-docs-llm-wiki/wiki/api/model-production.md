# model production

`model production` 指在百炼平台上完成模型的微调训练、压缩优化、导入管理及在线部署的完整生命周期。该流程覆盖文本、图像、视频、语音等多模态模型，支持从 SFT/DPO/LoRA 等训练方式到 PTU/MU/DTU 等多种部署模式，所有操作均通过统一 API 接口驱动，适用于生产环境下的模型迭代与服务化。

## 支持的模型与功能

- **微调任务类型**：支持文本生成（[文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)）、图像生成（[图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)）、视频生成（[视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)）和语音合成（[语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)）四类主流模态。
- **训练方法**：文本生成支持 `sft`、`cpt`、`efficient_sft`、`dpo_full`、`dpo_lora`；图像/视频/语音生成当前**仅支持 `efficient_sft`（LoRA）**，不支持全参微调（详见 [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md) 和 [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)）。
- **模型压缩**：提供量化压缩能力，当前**仅支持基于 `qwen3.5-flash-2026-02-23` 的自定义全参调优模型**，LoRA 模型和已量化模型不支持（见 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)）。
- **模型导入**：支持将 OSS 中存储的 LoRA 或全参调优模型文件导入平台（[模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)），导入后可直接部署。

> **注意**：文档 2 文档结构中列出“模型压缩”为文本生成子项，但实际 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md) 是独立功能模块，且适用范围远超文本生成（如支持后续部署的图像/视频模型推理加速），该归类易引发误解，应以独立文档为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 示例值 | 来源 |
|------|------|------|------|--------|------|
| `model` | string | 是 | 基准模型 ID 或已有调优模型 ID | `qwen3-14b`, `wan2.7-image-pro` | [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md) |
| `training_type` | string | 是 | 微调方法 | `sft`, `efficient_sft`, `dpo_lora` | 同上 |
| `hyper_parameters` | object | 条件必填 | 超参数集合，各模型差异大 | `{"n_epochs": 3, "batch_size": 32}`（文本）；`{"max_steps": 800, "learning_rate": 3e-5}`（图像） | [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md) |
| `model_name` | string | 是（部署） | 部署时需传入**微调产出或导入后的模型 ID**（非基础模型名） | `qwen3-14b-ft-202410291653-1c7f`, `wan2.7-image-pro-ft-202507011122-xxxx` | [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md) |
| `plan` | string | 是（部署） | 部署方案 | `lora`（LoRA 共享）、`mu`（模型单元）、`dtu`（独占算力）、`ptu_v2`（预置吞吐） | [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md) |

> **注意**：`hyper_parameters` 中的必填字段因模型类型而异——文本生成要求 `n_epochs`/`batch_size`/`max_length`；图像生成要求 `max_steps`/`eval_steps`/`learning_rate`；视频生成要求 `n_epochs`/`batch_size`/`learning_rate`；语音合成则需分别指定 `lm_*` 和 `fm_*` 两组参数。开发者必须依据目标模型查阅对应文档，不可复用参数模板。

## 使用方式

1. **训练准备**  
   - 仅限**华北2（北京）地域**调用训练与部署 API（所有训练类文档均明确标注，如 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)）；
   - 配置北京地域的 API Key，并授予 RAM 子账号 `model:Train`、`model:Deploy` 等必要权限；
   - 数据集通过 API 上传或 OSS 挂载（支持 `training_file_ids` 或 `training_datasets` 二选一）。

2. **提交训练任务**  
   ```bash
   POST https://dashscope.aliyuncs.com/api/v1/fine-tunes
   # 请求体包含 model、training_type、hyper_parameters 等
   ```

3. **监控与获取产出**  
   - 轮询 [查询调优任务状态](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)（`GET /api/v1/fine-tunes/{job_id}`），确认 `status=SUCCEEDED`；
   - 产出模型 ID 位于响应 `output.finetuned_output` 字段（文本/视频/语音）或 `output.model_name`（图像/导入模型）。

4. **部署服务**  
   - 使用产出模型 ID 调用 `POST /api/v1/deployments`；
   - 文本/图像/视频 LoRA 模型推荐 `plan=lora`；语音合成（CosyVoice）**强制使用 `plan=mu`**（见 [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)）；
   - 部署成功后，轮询 [查询部署模型状态](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)（`GET /api/v1/deployments/{deployed_model}`），等待 `status=RUNNING`。

5. **（可选）模型压缩**  
   - 仅限 `qwen3.5-flash-2026-02-23` 全参模型，调用 `/api/v1/fine-tunes/compress/jobs` 创建任务；
   - 成功后使用 `output.quantized_output` 替代原模型 ID 进行部署。

## 限制和注意事项

- **地域强约束**：所有训练类 API（微调、导入、压缩、Checkpoint 管理）**仅在北京地域可用**；部署 API 部分支持新加坡（如 PTU），但 MU/DTU/LoRA 部署仍限北京（见 [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md) 和 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)）。
- **模型兼容性限制**：
  - 图像/视频/语音生成微调**不支持强化学习（RL）与在线策略蒸馏（OPD）**，仅支持 `efficient_sft`（见 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md) 的 RL/OPD 说明）；
  - 模型压缩**仅支持 `qwen3.5-flash-2026-02-23` 全参模型**，其他模型（含所有 LoRA）无法压缩（见 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)）。
- **部署参数差异**：
  - `plan=lora` 部署时，`capacity` 为整数（如 1），表示共享实例数；
  - `plan=mu` 部署时，`capacity` 需为 `base_capacity` 的整数倍（如 `MU5` 要求 capacity=1,2,…；`MU2` 要求 capacity=8,16,…）；
  - `plan=dtu` 部署**必须使用业务空间专属域名**（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）和对应 Workspace API Key，不可用 `dashscope.aliyuncs.com`（见 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)）。
- **计费关键点**：`n_epochs`（文本/语音）、`max_steps`（图像）、`n_epochs × ⌈数据集大小 / batch_size⌉`（视频）等参数**直接影响训练费用**，务必按需设置（见各创建调优任务文档中的“重要”提示）。

## 来源文档

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
- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)


