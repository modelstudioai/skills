# 模型微调

模型微调（Fine-tuning）是百炼平台提供的核心模型优化能力，指基于预训练大模型（基座模型），利用领域特定数据进行有监督或偏好对齐的增量训练，从而生成在业务场景中更准确、更安全、更符合预期行为的专属模型版本。

## 在百炼平台的不同场景中，这个概念如何使用

模型微调不是单一操作，而是贯穿模型生产全链路的关键环节，其具体形态和约束因模型类型与业务目标而异：

- **文本生成模型**（如 `qwen3-32b`、`qwen3.7-plus-2026-05-26`）：支持最丰富的训练范式，包括 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）、RL（强化学习）和 OPD（在线策略蒸馏）。其中 CPT 仅限华北2（北京）地域可用；部分轻量模型（如 `qwen3.7-plus-2026-05-26`）仅支持 SFT 全参训练。
- **视觉理解模型**（千问VL）：仅支持 SFT（全参或高效），不支持 CPT 和 DPO，适用于图文理解、多模态指令跟随等任务。
- **图像/视频生成模型**（万相、千问图像）：仅支持 LoRA 高效微调（SFT-LoRA），参数控制方式与文本模型不同（如万相用 `max_steps`，千问用 `n_epochs`），适合风格迁移、特定物体生成等场景。
- **语音合成模型**（CosyVoice）：仅支持 `efficient_sft`，且要求输入为同一发音人多条高质量录音，输出为独立部署的单音色模型，不可跨音色复用。
- **决策模型**（如 `decision-model-preview-2026-09-24`）：不参与通用 CPT/SFT/DPO 流程，需使用平台专属微调路径，聚焦于策略稳定性与动作空间对齐。

所有微调任务均需依托已发布的**训练数据集**（`dataset_type=training`，JSONL 格式，含 `input`/`output` 字段），产出结果为一个可部署的专属模型 ID（如 `ft-xxx`），该 ID 可直接用于后续模型部署与评测。

## 关键参数和配置

微调效果高度依赖参数选择。以下为通用性最强、开发者需重点关注的核心参数（单位与默认值以控制台/API 实际界面为准）：

| 参数 | 类型 | 推荐值 | 说明 |
|------|------|--------|------|
| `learning_rate` | float | 高效训练：`1e-4`；全参/CPT：`1e-5` | 过高易发散，过低收敛慢；建议从推荐值开始，±10% 调整 |
| `n_epochs` | integer | 数据 <10k 条：3–5；>10k 条：1–2 | 文本模型常用；图像模型（万相）用 `max_steps` 替代 |
| `batch_size` | integer | 16 或 32（默认值通常可用） | 受显存与模型大小限制，控制台会动态提示合法范围 |
| `max_length` | integer | 设为模型最大上下文长度（如 8192） | SFT 会丢弃超长样本；DPO 自动截断，但影响偏好对齐质量 |
| `lora_rank` / `lora_alpha` / `lora_dropout` | integer / float / float | `8` / `16` / `0.1`（高效训练默认） | 调整 `rank` 和 `alpha` 可平衡效果与参数量；`dropout` 用于防过拟合 |

> ⚠️ 注意事项：
> - 所有微调任务**不支持中断后恢复**，失败需重提；
> - 训练时长上限为 **72 小时**，超时自动终止并标记为 `failed`；
> - API 方式创建的任务**仅支持按 Token 计费**，不支持训练单元计费；
> - 数据集必须已发布（`status=published`），且 `dataset_id` 格式为 `ds-xxx`。

## 面向开发者，简洁实用

- ✅ **快速上手**：控制台 →「模型调优」→ 选模型 + 选数据集 + 点启动（适合验证）；  
- ✅ **工程集成**：API 调用 `/api/v1/files`（上传数据，`purpose="fine-tune"`）→ `/api/v1/fine-tunes`（创建任务）→ 轮询 `status == "succeeded"` → 获取 `model_id`；  
- ✅ **部署衔接**：将微调产出的 `model_id` 直接传入 `/api/v1/deployments` 即可发布为在线服务；  
- ✅ **评测闭环**：用该 `model_id` 调用 `/v2/evaluations`，搭配自定义评测集或平台预置集（如 CMMLU），量化优化效果；  
- ❌ **避坑提醒**：CPT 仅在北京地域可用；图像模型不接受 `n_epochs`；语音模型必须同音色；训练集 JSONL 必须含 `input`/`output` 字段且编码为 UTF-8。

## 关联主题页

- [fine tuning](../guides/fine-tuning.md)
- [model production](../api/model-production.md)
- [model data overview](../guides/model-data-overview.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [more about models](../api/more-about-models.md)


