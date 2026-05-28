# model training

模型训练（Fine-tuning/调优）功能支持开发者使用自定义数据集对百炼平台上的基础模型进行定向优化，覆盖大语言模型（LLM）、视频生成模型及语音识别（ASR）热词定制。通过标准 RESTful API 或官方 SDK，您可完成数据集管理、任务提交、进度轮询与产物部署的全链路操作。

## 支持的模型与功能
平台提供多模态与垂类场景的调优支持，调用前需确认目标模型所属的任务域：
- **大语言模型 (LLM)**：支持 `qwen` 系列等。提供全量微调（`cpt`/`sft`）、高效微调（`efficient_sft`）、偏好优化（`dpo_full`/`dpo_lora`）等多种训练范式。
- **视频生成模型**：支持 `wan2.5-i2v-preview`、`wan2.2-i2v-flash`（图生视频）及 `wan2.2-kf2v-flash`（首尾帧视频）。当前仅开放高效微调（LoRA）能力。详见 [视频生成模型微调API参考](../../raw/model-api-reference/model-training/wan-video-generation-finetune-api-reference.md)。
- **语音识别 (ASR) 热词**：针对 `paraformer` 系列模型，支持通过词表权重调整优化特定领域术语的识别率。需使用 `AsrPhraseManager` SDK 进行管理。

## 核心工作流与调用方式
训练任务遵循标准的 `上传文件 -> 创建任务 -> 查询状态 -> 部署调用` 流程：
1. **文件准备与上传**：通过文件管理服务上传训练集（LLM 推荐 `.jsonl`，视频模型为 `.zip`）。获取唯一的 `file_id` 后，该 ID 可在多个任务中复用。接口规范请参考 [百炼文件管理 API](../../raw/model-api-reference/model-training/model-customization-file-management-service.md)。
2. **创建调优任务**：调用 `POST /api/v1/fine-tunes`，传入基准模型 `model`、文件 ID 列表 `training_file_ids`、训练方式 `training_type` 及超参数集 `hyper_parameters`。
3. **任务状态监控**：使用 `GET /api/v1/fine-tunes/{job_id}` 轮询查询。任务生命周期状态包括：`PENDING` → `QUEUING` → `RUNNING` → `SUCCEEDED`/`FAILED`。视频生成模型训练通常耗时数小时，请结合业务需求设置合理的轮询间隔。完整生命周期与响应结构见 [模型调优 API 参考](../../raw/model-api-reference/model-training/model-training-api-reference.md)。
4. **产物调用**：任务状态为 `SUCCEEDED` 后，通过返回的 `finetuned_output` 字段获取新模型 ID，随后可接入 [[model-deployment]] 或直接用于 [[inference-api]] 调用。

## 关键参数说明
超参数 `hyper_parameters` 直接影响训练质量、耗时与成本，提交前建议结合数据规模进行配置：
| 参数 | 说明 | 推荐配置 |
|:---|:---|:---|
| `n_epochs` | 数据遍历次数。数据量 `<10k` 建议 `3~5`，`>10k` 建议 `1~2`。视频模型需确保总步数 `≥800`。 | 必填，控制过拟合与训练成本 |
| `learning_rate` | 学习率，控制权重更新步长。过高易发散，过低收敛慢。 | 使用控制台/文档默认值 |
| `batch_size` | 批次大小。过小显著拉长训练时间。各模型默认值不同。 | 必填 |
| `max_length` | 单条数据最大 token 长度（超阈值将被丢弃）。 | LLM 默认 `8192` |
| `lora_*` 系列 | LoRA 秩值(`lora_rank`)、缩放系数(`lora_alpha`)等。仅 `efficient_sft` 及 DPO 变体生效。 | 二次微调时必须保持与首次一致 |

> **注意**：不同模型对 `training_type` 的约束存在差异。LLM 支持多种范式，但视频生成模型目前强制固定为 `efficient_sft`。混用或传入不支持的参数将直接返回 `BadRequest`。同时，LLM 文档中提到的 `split`（自动划分训练/验证集比例）在已显式传入 `validation_file_ids` 时会自动失效。

## 限制与注意事项
- **地域与权限**：所有训练接口仅支持中国大陆版（北京地域）。使用子账号（RAM）时，需显式授予模型训练、部署及 [[workspace-management]] 相关权限。
- **文件配额**：单个训练文件上限 `1GB`，账号总有效存储配额 `5GB`，文件数量上限 `100` 个。建议训练完成后通过 `DELETE` 接口清理冗余文件以释放空间。
- **计费与快照**：混合训练（Data Augmentation）产生的额外数据 Token 将按标准计入总训练费用。可通过 `save_strategy` 与 `save_total_limit` 控制 Checkpoint 的保存频次与上限，默认最多保留 `10` 个快照供发布。
- **参数快照一致性**：若对已采用 LoRA/高效微调的模型进行二次微调，`lora_rank`、`lora_alpha`、`lora_dropout` 必须与初始训练保持严格一致，否则将导致权重合并异常。

## 来源文档

- [模型调优 API 参考](../../raw/model-api-reference/model-training/model-training-api-reference.md)
- [百炼文件管理 API](../../raw/model-api-reference/model-training/model-customization-file-management-service.md)
- [视频生成模型微调API参考](../../raw/model-api-reference/model-training/wan-video-generation-finetune-api-reference.md)
- [paraformer热词](../../raw/model-api-reference/model-training/paraformer-asr-phrase-manager.md)

