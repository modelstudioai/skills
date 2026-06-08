# model training

百炼平台提供完整的模型训练 API 体系，涵盖训练文件管理、模型调优（微调）、视频/图像生成模型微调以及模型压缩四大能力。开发者可通过 RESTful API 完成从数据上传、任务创建、状态监控到产出模型获取的全流程操作。

## 文件管理

模型训练的第一步是上传训练数据。[百炼文件管理 API](../../raw/model-api-reference/model-training/model-customization-file-management-service.md) 提供统一的文件管理服务，支持一次上传、多次复用。

核心接口：

| 操作 | 方法 | 端点 |
|------|------|------|
| 上传文件 | POST | `/api/v1/files` |
| 列举文件 | GET | `/api/v1/files` |
| 获取文件详情 | GET | `/api/v1/files/{file_id}` |
| 删除文件 | DELETE | `/api/v1/files/{file_id}` |

上传时通过 `purpose` 字段指定用途：`fine-tune`（模型调优）、`file-extract`（长上下文分析）、`batch`（Batch 任务）。

使用限制：
- 单个文件最大 1GB
- 有效文件总空间配额 5GB
- 有效文件总数量配额 100 个

## 模型调优（文本/视觉理解模型）

[模型调优 API](../../raw/model-api-reference/model-training/model-training-api-reference.md) 支持对文本生成、视觉理解等模型进行微调训练。

### 支持的训练方式

- `sft`：全参数监督微调
- `efficient_sft`：LoRA 高效微调
- `cpt`：继续预训练
- `dpo_full`：DPO 全参数训练
- `dpo_lora`：DPO LoRA 训练

### 关键超参数

| 参数 | 说明 | 备注 |
|------|------|------|
| `n_epochs` | 训练循环次数 | 必填；数据量 < 10000 建议 3-5，> 10000 建议 1-2 |
| `batch_size` | 批次大小 | 必填；不同模型默认值不同 |
| `max_length` | 序列最大 token 长度 | 必填；超长数据会被丢弃 |
| `learning_rate` | 学习率 | 建议使用默认值 |
| `lr_scheduler_type` | 学习率调整策略 | 推荐 `linear` 或 `inverse_sqrt` |
| `lora_rank` / `lora_alpha` | LoRA 参数 | 仅高效微调时使用；二次微调时需保持一致 |

高级功能：
- **混合训练**（`data_augmentation`）：将用户数据与百炼预置通用数据集混合，避免模型能力退化
- **Checkpoint 快照发布**（`save_strategy`）：支持按 epoch 或 steps 保存模型参数快照

### CosyVoice 语音合成模型

CosyVoice（`cosyvoice-v3-flash`）使用独立的超参数体系，包含 LM 和 FM 各 4 个参数（`lm_max_epoch`、`lm_step`、`lm_num`、`lm_batch_size` 及对应的 `fm_*` 参数），全部必填。仅支持 `efficient_sft` 训练方式。

### 任务状态

任务状态流转：`PENDING` → `QUEUING` → `RUNNING` → `SUCCEEDED` / `FAILED` / `CANCELED`。同一时间只能有一个训练任务在运行，其余排队等待。

## 视频/图像生成模型微调

[视频/图像生成模型微调 API](../../raw/model-api-reference/model-training/wan-generation-finetune-api-reference.md) 针对万相系列模型提供专用的微调能力。

### 支持的模型

| 场景 | 模型 |
|------|------|
| 图生视频（基于首帧） | `wan2.5-i2v-preview`、`wan2.2-i2v-flash` |
| 图生视频（基于首尾帧） | `wan2.2-kf2v-flash` |
| 图像生成（文生图/图生图） | `wan2.7-image-pro` |

所有万相模型当前仅支持 `efficient_sft`（LoRA 高效微调）。

### 超参数差异

视频生成模型与图像生成模型的超参数体系存在显著差异：

- **视频模型**使用 `n_epochs` + `eval_epochs` 控制训练和评估，推荐总训练步数不少于 800 步，还需设置 `max_pixels` 控制视频分辨率
- **图像模型**使用 `max_steps` + `eval_steps` 控制训练和评估，并需指定 `generation_type`（`t2i` 或 `i2i`）、`max_pixels`、`val_img_size`、`max_token_length` 等图像专用参数

> **注意**：上传视频/图像训练数据集时需使用 .zip 格式，通过 API 上传时压缩包大小不超过 1GB。

## 模型压缩

[模型压缩 API](../../raw/model-api-reference/model-training/model-compression-api-reference.md) 支持对自定义全参微调模型进行量化压缩，降低显存占用并提升推理吞吐。

### 使用前提

- 当前仅支持基于 `qwen3.5-flash-2026-02-23` 的全参微调模型
- LoRA 模型和已量化模型不支持
- 压缩功能限时免费

### 核心流程

1. 调用 `GET /api/v1/fine-tunes/compress/templates` 查询可用压缩模板
2. 调用 `POST /api/v1/fine-tunes/compress/jobs` 创建压缩任务，指定 `model`、`template_id` 和可选的 `output_model_suffix`
3. 轮询 `GET /api/v1/fine-tunes/compress/jobs/{job_id}` 等待任务完成
4. 成功后从 `quantized_output` 获取量化产出模型 ID，用于部署

产出模型命名规则：`{base_model}-{suffix}-{job_id}`。

### 任务管理

压缩任务支持列举（含多维过滤和排序）、查询详情、获取日志、取消和删除操作，任务状态与调优任务一致。

## 通用说明

- 所有接口域名为 `https://dashscope.aliyuncs.com`，通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 鉴权
- 文档仅适用于中国大陆版（北京地域）
- 调优任务消耗的 Token 数可通过查询任务详情的 `usage` 字段获取
- 调优完成后的模型 ID 通过 `finetuned_output`（调优）或 `quantized_output`（压缩）字段返回，可用于推理调用或模型部署

## 来源文档

- [百炼文件管理 API](../../raw/model-api-reference/model-training/model-customization-file-management-service.md)
- [模型调优 API 参考](../../raw/model-api-reference/model-training/model-training-api-reference.md)
- [视频/图像生成模型微调 API 参考](../../raw/model-api-reference/model-training/wan-generation-finetune-api-reference.md)
- [模型压缩 API 参考](../../raw/model-api-reference/model-training/model-compression-api-reference.md)



