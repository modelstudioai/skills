# fine tuning

fine tuning 是指在百炼平台提供的预训练大模型基础上，使用用户自有数据进行增量训练，以适配特定任务或领域。该能力支持文本生成、图像生成、视频生成和语音合成等多模态模型，适用于需要定制化输出效果的场景。所有 fine tuning 任务均通过平台 API 或控制台提交，并由后台异步执行。

## 支持的模型/功能

当前支持以下模型类别的 fine tuning：
- 文本生成模型（如 Qwen 系列）：支持指令微调（SFT）、LoRA 等轻量适配方式  
- 图像生成模型（WanImage）：支持基于提示词风格迁移与可控生成微调  
- 视频生成模型（WanVideo）：支持短时序一致性增强的微调流程  
- 语音合成模型（TTS）：支持音色克隆与语调定制微调  
- 强化学习（RL）训练：提供 PPO 等算法支持，用于对齐人类偏好（详见 [强化学习](../../raw/model-user-guide/fine-tuning.md)）

> **注意**：原始文档中列出的 [千问模型调优](../../raw/model-user-guide/fine-tuning.md) 和 [图像生成模型调优](../../raw/model-user-guide/fine-tuning.md) 均指向外部帮助中心链接，实际平台内可用模型列表以控制台「模型调优」页实时展示为准；部分旧版文档未同步新增的 Qwen2-VL 多模态视觉语言模型 fine tuning 支持，该能力已在 v2.3.0 版本上线。

## 关键参数

调用 fine tuning API 或配置控制台任务时，需指定以下必需参数：
- `model_id`：目标基础模型 ID（如 `qwen-max`, `wan-image-v1`），必须为平台当前支持的 fine tuning 可用模型  
- `training_dataset`：OSS 路径或上传的 JSONL 格式训练数据集（格式要求见 [千问模型调优](../../raw/model-user-guide/fine-tuning.md)）  
- `hyperparameters`：含 `learning_rate`, `num_epochs`, `lora_rank`（LoRA 场景）等，不同模型类型默认值不同  
- `output_model_name`：微调后模型的自定义名称，全局唯一  

## 使用方式

1. **准备数据**：按模型类型整理训练数据（如文本任务需 [prompt](prompt.md)/completion 对，图像任务需 image+[prompt](prompt.md) pair），确保符合 [图像生成模型调优](../../raw/model-user-guide/fine-tuning.md) 所述格式规范  
2. **创建任务**：通过控制台「模型调优」→「新建任务」填写参数，或调用 `POST /v1/fine-tunes` API  
3. **监控与部署**：任务状态可在「训练记录」中查看；成功后生成专属模型 ID，可直接用于推理 API 调用  

## 限制和注意事项

- 单次训练最大数据量：文本 ≤ 100 万 token，图像 ≤ 5,000 张，视频 ≤ 200 段（每段 ≤ 4s）  
- 训练时长上限：免费版 ≤ 2 小时，企业版 ≤ 24 小时（超时自动终止）  
- 微调后模型不支持导出权重文件，仅限百炼平台内调用  
- 数据隐私：训练数据仅用于本次任务，任务结束后立即从 GPU 内存及临时存储清除（参见 [视频生成模型调优](../../raw/model-user-guide/fine-tuning.md) 中的安全说明）  
- LoRA 微调不改变基础模型参数，但部署时需显式指定 `adapter_id`；全参数微调暂不开放，仅限白名单客户申请

## 来源文档

- [模型调优](../../raw/model-user-guide/fine-tuning.md)


