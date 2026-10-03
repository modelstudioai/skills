# fine tuning

fine tuning 是指在百炼平台上基于预训练大模型，使用用户自有数据进行有监督微调，以适配特定任务或领域。该能力支持文本生成、图像/视频生成、语音合成等多种模态，同时提供强化学习、策略蒸馏等高级调优范式。所有 fine tuning 功能均通过 API 或控制台统一接入，需遵循平台的数据格式、资源配额与生命周期规范。

## 支持的模型与功能

当前支持 fine tuning 的模型类型包括：
- 文本生成类（如 Qwen 系列）：支持指令微调、多轮对话对齐 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)  
- 多模态生成类：图像生成（WanImage）、视频生成（WanVideo）及语音合成（TTS）模型均提供专用 fine tuning 流程 [图像生成模型调优](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[视频生成模型调优](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)、[语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)  
- 决策与策略类：支持强化学习（RL）框架下的策略优化、在线策略蒸馏（OPD）及决策模型专项微调 [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md)、[在线策略蒸馏](../../raw/model-user-guide/fine-tuning/opd-overview.md)、[决策模型微调](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)

> **注意**：文档中提及的“WanVideo v1.2 支持端到端视频时序微调”与最新 API 文档（v2.3）中仅支持关键帧条件微调存在不一致，实际请以 `POST /v2/fine_tuning/jobs` 接口的 `supported_task_types` 字段返回值为准。

## 关键参数

调用 fine tuning API 时需指定以下核心参数：
- `model_id`：必须为平台已发布的可微调模型 ID（如 `qwen-max-0428`），不可使用自定义别名  
- `training_file_id`：训练数据集文件 ID（需提前通过 `/v2/files/upload` 上传，格式为 JSONL，每行含 `prompt`/`completion` 或对应模态字段）  
- `hyperparameters.learning_rate`：推荐范围 `1e-6 ~ 5e-5`；超出此范围可能导致梯度爆炸或收敛停滞  
- `hyperparameters.epoch`：文本类默认 `3`，多模态类建议 `1~2`（受显存与数据规模限制）  
- `validation_file_id`（可选）：验证集文件 ID，用于监控过拟合；若未提供，系统自动按 10% 划分训练集  

## 使用方式

1. **准备数据**：按 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md) 中定义的 schema 构建训练集（JSONL 格式），确保字段名与目标模型要求严格匹配  
2. **创建任务**：调用 `POST /v2/fine_tuning/jobs`，传入 `model_id`、`training_file_id` 及超参配置  
3. **监控与管理**：通过 `GET /v2/fine_tuning/jobs/{job_id}` 查询状态；任务成功后返回 `fine_tuned_model_id`，可用于后续推理  

## 限制和注意事项

- 单次训练最大数据量：文本类 ≤ 10 GB，图像/视频类 ≤ 5000 样本（因分辨率与帧数影响实际体积）  
- 微调模型不可导出或下载，仅支持在百炼平台内调用（`/v2/models/{fine_tuned_model_id}/chat/completions`）  
- 训练任务最长运行时限为 72 小时；超时将自动终止并标记为 `failed`  
- 同一 `model_id` 下最多保留 5 个成功完成的微调版本；超出后需手动删除旧版本释放配额  
- 所有 fine tuning 任务均计入用户「训练算力配额」，详情见配额管理页面；免费额度不适用于 RL/OPD 类高级调优路径

## 来源文档

- [模型调优](../../raw/model-user-guide/fine-tuning.md)


