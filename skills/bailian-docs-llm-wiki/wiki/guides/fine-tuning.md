# fine tuning

fine tuning 是在百炼平台对预训练大模型进行领域适配或任务定制的关键能力，支持文本生成、图像生成、视频生成和语音合成等[多模态](../concepts/multi-modal.md)模型。用户可通过上传标注数据集，配置训练参数，在平台托管环境中完成模型微调并部署为专属服务。该能力基于 [模型调优](../../raw/model-user-guide/fine-tuning.md) 文档所定义的统一入口与流程设计。

## 支持的模型与功能

当前支持以下四类模型的 fine tuning：
- **文本生成模型**：如 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5），支持指令微调（SFT）与 LoRA 微调；
- **图像生成模型**：如 WanImage，支持 ControlNet 与 Dreambooth 风格微调；
- **视频生成模型**：如 WanVideo，支持短时序视频生成任务的 [prompt](prompt.md)-aware 微调；
- **语音合成模型**：如 Qwen-TTS，支持音色克隆与风格迁移微调。

> **注意**：强化学习（RL）训练虽在 [模型调优](../../raw/model-user-guide/fine-tuning.md) 中列为子项，但其目标、数据格式与训练范式与监督式 fine tuning 本质不同；实际使用中 RL 不属于本文所述的“fine tuning”范畴，应参考独立的 [强化学习](../../raw/model-user-guide/reinforcement-learning.md) 文档。

## 关键参数

| 参数 | 说明 | 取值示例 |
|------|------|----------|
| `base_model` | 基座模型 ID（必填） | `qwen2-7b-instruct`, `wanimage-v1` |
| `training_type` | 微调方式 | `full`, `lora`, `qlora`（仅文本模型支持后两者） |
| `learning_rate` | 初始学习率 | `2e-5`（LoRA）、`5e-6`（全参） |
| `epochs` | 训练轮数 | `3`（推荐 1–5） |
| `max_seq_length` | 输入最大长度（文本） | `2048`（需 ≤ 基座模型上下文限制） |

所有参数均需符合 [模型调优](../../raw/model-user-guide/fine-tuning.md) 中定义的校验规则，例如 `base_model` 必须为平台当前开放 fine tuning 的白名单模型。

## 使用方式

1. **准备数据集**：按模型类型提供标准格式数据（如文本模型需 JSONL，每行含 `prompt`/`response` 字段）；
2. **创建训练任务**：通过控制台「模型训练」→「新建微调任务」，或调用 `POST /v1/fine-tunes` API；
3. **监控与验证**：训练过程中可查看 loss 曲线、样本生成效果；任务完成后自动评估并生成测试报告；
4. **部署服务**：训练成功后，可在「已部署模型」中一键发布为 API 服务。

详细操作步骤见 [模型调优](../../raw/model-user-guide/fine-tuning.md)。

## 限制和注意事项

- 单次训练最大时长：文本模型 ≤ 72 小时，图像/视频模型 ≤ 120 小时；
- 数据集大小限制：文本 ≤ 10 GB，图像 ≤ 50,000 张，视频 ≤ 2,000 个片段；
- LoRA 微调不支持跨基座模型复用 adapter（例如 `qwen2-7b` 训练的 LoRA 不能加载到 `qwen2-14b`）；
- 所有微调任务均需指定 `region`，且训练与部署必须在同一地域（如 `cn-shanghai`）；
- 若使用私有 OSS 存储数据，请确保授权策略已授予百炼服务角色读取权限。

如遇训练中断或评估异常，请优先核查数据格式是否符合 [模型调优](../../raw/model-user-guide/fine-tuning.md) 中的 schema 要求。

## 来源文档

- [模型调优](../../raw/model-user-guide/fine-tuning.md)


