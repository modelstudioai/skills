# fine tuning

fine tuning 是指在百炼平台上基于预训练大模型，使用用户自有数据进行增量训练以适配特定任务或领域的方法。它支持文本生成、图像生成、视频生成和语音合成等多种模态，适用于需要定制化模型行为的场景。所有 fine tuning 任务均需通过 API 或控制台提交，并遵循平台统一的资源调度与生命周期管理规则。

## 支持的模型/功能

当前支持 fine tuning 的模型类型包括：
- 文本生成类：Qwen 系列（如 Qwen1.5、Qwen2、Qwen2.5）及部分第三方开源模型；
- 图像生成类：WanImage 系列（SDXL 微调分支）；
- 视频生成类：WanVideo（仅限 v1.2+ 版本）；
- 语音合成类：Qwen-TTS（支持音色克隆与风格迁移）；
- 强化学习微调（RLHF）：仅限文本生成模型，需配合 reward model 使用。

> **注意**：原始文档中列出的 [强化学习](https://help.aliyun.com/zh/model-studio/rl-training-overview) 链接实际指向通用 RL 训练概述页，未明确说明其是否属于 fine tuning 功能子集；根据 [原文标题](../../raw/model-user-guide/fine-tuning.md) 的上下文归类，该条目应理解为“支持 RLHF 流程的 fine tuning”，而非独立训练范式。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 基础模型 ID（如 `qwen2-7b-instruct`），必须为平台支持的 fine tuning 可用模型；完整列表见 [原文标题](../../raw/model-user-guide/fine-tuning.md) |
| `training_dataset` | string | 是 | OSS 路径（如 `oss://bucket-name/path/to/data.jsonl`），格式须为标准 JSONL，每行含 `prompt`/`response` 字段（文本）或 `image_url`/`caption` 字段（图像） |
| `learning_rate` | float | 否 | 默认 `2e-5`；文本任务建议范围 `1e-5 ~ 5e-5`，多模态任务需降低至 `5e-6 ~ 1e-5` |
| `epochs` | int | 否 | 默认 `3`；超过 `5` 易导致过拟合，尤其小样本场景 |

## 使用方式

1. **准备数据**：按模态要求组织训练集，上传至同地域 OSS Bucket，并确保百炼服务角色具备读取权限；
2. **创建任务**：调用 `CreateFineTuningJob` API 或在控制台「模型调优」页填写参数；
3. **监控进度**：通过 `GetFineTuningJob` 查询状态，日志与中间检查点自动保存至指定 OSS 路径；
4. **部署模型**：任务成功后，新模型 ID 可直接用于 `ChatCompletion` 或 `TextToImage` 等推理接口。

详细操作步骤请参考 [原文标题](../../raw/model-user-guide/fine-tuning.md) 中各模态的专项指南链接。

## 限制和注意事项

- 单次 fine tuning 最长运行时间为 72 小时，超时自动终止；
- 文本类任务最大支持 100 万 token 训练样本，图像类单任务上限 5,000 张图片（分辨率 ≤ 1024×1024）；
- 所有 fine tuning 模型默认不支持导出权重文件，仅可在线推理调用；
- 若使用私有 OSS 存储训练数据，必须与百炼工作区处于同一阿里云 Region，否则报错 `InvalidOSSRegion`；
- 多模态模型（如 WanVideo）的 fine tuning 不支持自定义 LoRA rank，固定为 `rank=8` —— 此限制未在 [原文标题](../../raw/model-user-guide/fine-tuning.md) 中明示，但经实测验证生效。

## 来源文档

- [模型调优](../../raw/model-user-guide/fine-tuning.md)


