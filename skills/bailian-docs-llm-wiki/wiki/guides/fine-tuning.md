# fine tuning

模型调优（Fine-tuning）是突破提示词优化瓶颈、将基础大模型深度适配特定业务场景与行业标准的核心策略。平台提供覆盖文本生成、视觉理解与视频生成模型的完整训练能力，支持监督微调、持续预训练与偏好对齐等多种范式。开发者可通过可视化控制台或标准 API 完成从数据注入、模型训练到服务部署的全流程操作。

## 支持的模型与功能
平台调优能力按模态与任务划分如下：
- **文本生成**：覆盖 Qwen2.5 与 Qwen3 全系列模型（如 `qwen2.5-7b-instruct`、`qwen3-32b` 等），支持 CPT、SFT 与 DPO 三种训练范式。
- **视觉理解**：支持 Qwen2.5-VL 与 Qwen3-VL 系列，允许在 ChatML 格式中混排图片与视频路径进行多模态指令微调。
- **视频生成**：提供万相系列模型（如 `wan2.5-i2v-preview`）的 SFT-LoRA 高效微调，用于定制首帧/首尾帧驱动的特定动作或视觉风格。详见 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **核心特性**：内置零代码控制台与完整 API/CLI 链路，支持与 [[模型部署]]、[[模型评测]] 模块无缝衔接，提供训练快照（Checkpoint）保存、数据增强与混合训练等企业级功能。

## 关键参数
训练效果高度依赖超参数配置，以下为高频核心参数建议：

| 参数 | 推荐配置 | 说明 |
|:---|:---|:---|
| `n_epochs` | 数据量 < 10k 时 3~5，> 10k 时 1~2 | 训练循环轮次。过高易过拟合，过低易欠拟合。 |
| `learning_rate` | LoRA: `1e-4` 量级（安全对齐案例推荐 `3e-4`）<br>全参/CPT: `1e-5` 量级 | 控制权重更新步长。过大导致震荡，过小导致训练停滞。 |
| `batch_size` | 16 或 32（视显存与配额调整） | 单次梯度更新的数据量。 |
| `max_length` | 设为模型支持的最大上下文长度 | 超出该 Token 长度的 SFT 样本会被丢弃，DPO 样本会被截断。 |
| `lora_rank` / `lora_alpha` | Rank 设为支持的最大值，Alpha 默认或 32 | Rank 决定低秩矩阵容量，Alpha 控制微调权重与基础权重的缩放比例。 |
| `lr_scheduler_type` | `linear`、`inverse_sqrt` 或 `cosine` | 学习率衰减策略。短任务推荐 linear，长周期任务推荐 cosine。 |
| `split` | `0.9` | 训练集与验证集自动切分比例。未传验证集时生效。 |

## 使用方式
标准调优流程包含四个阶段：**数据准备 → 任务创建 → 状态轮询 → 部署调用**。

### 1. 数据准备与上传
- **文本 SFT**：采用 ChatML JSONL 格式，每行一个 JSON 对象，包含 `messages` 数组。不支持 OpenAI 的 `name` 与 `weight` 字段，所有 `assistant` 回复默认参与 Loss 计算。
- **视觉/视频 SFT**：打包为 ZIP，根目录必须直接包含 `data.jsonl` 及多媒体文件。图片单张 ≤10MB 且宽高 ≤1024px。
- **API 上传**：通过 `POST /api/v1/files` 上传文件，获取 `file_id`。单个文件 ≤300MB，总配额 5GB/100个文件。详见 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

### 2. 创建训练任务
- **控制台操作**：进入模型调优页面，选择基础模型与训练类型（全参/高效），配置超参数并绑定训练集/验证集。平台提供参数推荐与实时 Loss 曲线观测。参考 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 操作**：请求 `POST /api/v1/fine-tunes`，传入 `model`、`training_file_ids` 与 `hyper_parameters`。响应将返回 `job_id` 用于进度追踪，以及 `finetuned_output`（微调后模型标识）。

### 3. 监控与部署
- 轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status` 为 `SUCCEEDED`。
- 调用部署接口将 `finetuned_output` 发布为在线服务。部署成功后状态变为 `RUNNING`，即可用于业务调用。视频类微调模型需在部署时通过 `aigc_config` 固化 Prompt 模板，推理时建议关闭 `[[prompt|prompt]]_extend`。

## 限制和注意事项
- **地域与权限**：当前模型调优服务**仅面向中国大陆版（北京地域）**开放。使用 RAM 子账号需提前授予模型调用、训练任务管理与资源部署的完整权限。
- **数据格式严格性**：视觉/视频训练集的 `data.jsonl` 内引用媒体文件时仅需写文件名，不可包含相对路径。思考型模型（Thinking）训练时，`<think>` 标签及前后换行符必须严格保留，且仅对最后一个 `assistant` 轮次生效。
- **调优策略优先级**：强烈建议优先通过 [[Prompt工程]] 或插件调用验证业务可行性。模型调优通常作为最终手段，推荐遵循 `CPT（注入领域知识）→ SFT（规范任务行为）→ DPO（对齐人类偏好）` 的递进路径。
- **计费机制**：训练费用按 `(训练 Token + 混合 Token) × n_epochs × 单价` 计算。微调后的模型部署后按实例规格独立计费，成本显著高于基础模型，上线前需充分评估。
> **注意**：不同文档对高效训练（LoRA）与全参训练的推荐存在侧重差异。一方指出 LoRA 收敛快、成本低，适合小数据验证与快速迭代；另一方说明在单价相同时，优先使用全参训练可获得更优的泛化效果与性价比。实际选型应结合数据规模（<5万 Token 建议 LoRA）、业务对泛化边界的要求及容错周期综合决策。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)

