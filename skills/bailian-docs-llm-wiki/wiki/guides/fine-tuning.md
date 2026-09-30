# fine tuning

fine tuning 是指在百炼平台上基于预训练大模型，使用用户自有数据进行增量训练以适配特定任务或领域的能力。它支持文本生成、图像/视频生成、语音合成等多种模态，适用于业务逻辑定制、风格迁移、知识注入等场景。所有 fine tuning 任务均通过 API 或控制台提交，训练完成后生成专属模型版本供推理调用。

## 支持的模型与功能

当前支持 fine tuning 的模型类型包括：  
- 文本生成类（如 Qwen 系列）：支持指令微调、长文本续写、多轮对话对齐等；详见 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)。  
- 多模态生成类：图像生成（WanImage）、视频生成（WanVideo）和语音合成（TTS）模型均提供专用 fine tuning 流程，各流程的数据格式、标注规范与评估指标差异显著；参考 [图像生成模型调优](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) 和 [视频生成模型调优](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- 决策与强化学习类：支持决策模型微调及在线策略蒸馏（OPD），但需注意 OPD 当前仅限白名单客户开通；相关能力说明见 [决策模型微调](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

> **注意**：原始文档中 [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md) 页面未明确标注是否已全量开放，且其训练周期与资源要求与常规监督微调存在本质差异；实际接入前请务必确认当前控制台或 API 文档中 RL 微调模块的可用状态。

## 关键参数

- `base_model`: 必填，指定基础模型 ID（如 `qwen2-7b-instruct`），必须为平台当前支持 fine tuning 的模型；不支持任意自定义 checkpoint。  
- `training_dataset`: 必填，OSS 路径或上传的 JSONL 文件，每行一个样本，字段需严格匹配目标模型类型要求（如文本任务需含 `prompt`/`response`，图像任务需含 `image_url`+`caption`）。  
- `learning_rate`, `epochs`, `batch_size`: 可选，若未指定则使用平台默认值；默认超参组合经通用任务验证，但高噪声数据或小样本场景建议显式调优。  
- `validation_dataset`: 可选，用于监控过拟合；若未提供，系统将自动从训练集划分 10% 作为验证集（不支持图像/视频类任务的自动划分）。

## 使用方式

1. 准备符合格式要求的训练数据（参考对应模态的 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md) 中的数据样例）；  
2. 调用 `POST /v1/fine_tunes` 接口或在控制台「模型调优」页创建任务；  
3. 任务提交后，可通过 `GET /v1/fine_tunes/{id}` 查询状态，`succeeded` 表示完成，返回 `model_id` 即可用于后续 `/v1/chat/completions` 等推理接口；  
4. 训练日志与 loss 曲线可在任务详情页查看，图像/视频类任务额外提供中间生成效果预览（需开启 `enable_preview` 参数）。

## 限制和注意事项

- 单次训练最大时长：文本类 ≤ 72 小时，图像/视频类 ≤ 168 小时；超时自动终止且不计费。  
- 数据规模限制：文本训练集上限 100 万条，图像/视频单任务上限 5 万张/段；超出需分批提交或申请配额扩容。  
- 模型版本管理：fine tuned 模型不继承基础模型的自动更新策略，升级需重新训练；历史版本保留 90 天，过期后不可恢复。  
- **重要**：语音合成模型 fine tuning 仅支持音色克隆类任务，不支持改变语言或语种；该限制在 [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md) 中有明确说明，与部分旧版 SDK 示例代码存在冲突，请以该文档为准。

## 来源文档

- [模型调优](../../raw/model-user-guide/fine-tuning.md)


