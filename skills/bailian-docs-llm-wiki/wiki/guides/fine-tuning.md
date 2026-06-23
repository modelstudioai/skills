# fine tuning

百炼平台的模型调优（fine tuning）能力覆盖文本生成、视觉理解、图像生成、视频生成、语音合成等多种模型，支持 SFT（监督微调）、CPT（继续预训练）、DPO（直接偏好优化）三种训练方式，以及全参训练与 LoRA 高效训练两种模式。除语音合成（CosyVoice）调优目前仅支持 API 方式发起外，其他模型既可在控制台可视化操作，也可通过 API / 命令行完成，详见 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

> **注意**：所有模型调优功能仅适用于华北2（北京）地域，必须使用该地域的 API Key。

## 调优方式与适用场景

百炼提供三种递进、可组合的调优方式，推荐顺序为 `CPT（可选）→ SFT → DPO（可选）`，详见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

| 方式 | 目标 | 数据要求 | 学习方式 |
| --- | --- | --- | --- |
| CPT（继续预训练） | 补知识，注入领域知识 | 1000 万+ Token 无标签领域文本 | 自监督（预测下一词） |
| SFT（监督微调） | 学做事，遵循指令 | 1000+ 条高质量「问-答」对 | 监督学习（模仿标准答案） |
| DPO（直接偏好优化） | 做得更好，对齐人类偏好 | 100+ 组同一指令的「更好-更差」回答对 | 直接偏好学习 |

### 训练模式对比

- **全参训练**：更新全部模型参数，效果通常更好，训练时间较长。百炼推荐若模型支持全参训练则优先使用，性价比更高。
- **高效训练（LoRA）**：通过低秩矩阵分解只更新低秩部分参数，速度快、成本低，适用于快速验证或数据集较小场景。

### 支持的模型与训练方式

文本生成类（Qwen 系列）支持矩阵较广，例如 Qwen3-32B、Qwen2.5-72B-Instruct 等支持 CPT/SFT/DPO 全部方式；Qwen3-8B、Qwen3-14B 等支持 SFT/DPO。视觉理解类（千问 VL）支持 SFT 全参与高效训练。万相图像 / 视频生成模型仅支持 SFT-LoRA 高效微调（`efficient_sft`）。CosyVoice 语音合成仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调。完整支持矩阵请参见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 数据集格式

### 文本生成 SFT

采用 ChatML 格式，每行一个 JSON 对象，支持多轮对话；不支持 OpenAI 的 `name`、`weight` 参数，所有 assistant 输出都会被训练：

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入"},
  {"role": "assistant", "content": "期望的模型输出"}
]}
```

- 思考模型（thinking）：仅对最后一条 assistant 输出训练，思考内容用 `<think>...</think>` 包裹，标签前后的 `\n` 必须保留。
- 视觉理解（千问 VL）：`content` 使用数组格式，支持 `image`、`video`（文件路径模式或图片帧列表模式，仅 qwen3.5 及以后 VL 模型支持视频）。`system` 消息的 `content` 必须为数组格式 `[{"text":"..."}]`。
- `loss_weight`（邀测参数）：单条 assistant 行可设置 0.0~1.0 的相对重要性。

### DPO 数据集

在 `messages` 之外额外提供 `chosen`（赞同输出）与 `rejected`（反对输出），模型对最后一条 user 输入学习正负反馈；`chosen` 支持 `loss_weight`。

### CPT 数据集

纯文本格式，每行 `{"text":"文本内容"}`。

### 图像 / 视频生成微调数据集

打包为 `.zip`，根目录下必须包含 `data.jsonl`：

- 文生图：`data.jsonl` 每行 `{"prompt":"...","img_path":"./1_0.png"}`，训练目标图像平铺在根目录。
- 图生图：包含参考图像（输入）与训练目标图像（输出）。
- 图生视频：基于首帧或首尾帧训练，详见 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

> **注意**：图像 / 视频微调数据集文件名仅支持英文字符，平铺结构，禁止子目录。

### CosyVoice 语音合成数据集

目录结构为 `user_data/data.jsonl` + `train/*.wav`，`data.jsonl` 每行 `{"wav_fn":"train/100001.wav","text":"你好。"}`，`wav_fn` 必须以 `train/` 为前缀。音频为 `.wav`、采样率不低于 16kHz、单条 2~30 秒；训练数据必须为同一发音人。详见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 关键超参数

以下以文本生成 SFT 为例，控制台与 API 均可配置：

| 参数 | 推荐设置 | 说明 |
| --- | --- | --- |
| `batch_size` | 默认值（一般 16/32） | 模型每看 N 条数据更新一次参数 |
| `learning_rate` | 高效训练 1e-4 量级；全参/CPT 1e-5 量级 | 控制权重修正强度，过高表现变差，过低无明显变化 |
| `n_epochs` | <1万条数据 3~5 次；>1万条 1~2 次 | 训练循环次数，越多越慢越贵，范围 [1, 200] |
| `max_length` | 模型支持的最大值 | 单条数据 token 上限，SFT 超出则丢弃，DPO 超出则截断，范围 [500, 32768] |
| `lr_scheduler_type` | linear 或 Inverse_sqrt | 学习率调整策略 |
| `warmup_ratio` | 默认值 | 训练初期学习率线性递增占比，范围 [0, 1] |
| `weight_decay` | 默认值 | L2 正则化强度，范围 [0, 0.2] |
| `lora_rank` | 模型支持的最大值 | LoRA 低秩矩阵秩，越大效果略好但略慢 |
| `lora_alpha` / `lora_dropout` | 默认值 | LoRA 结合缩放系数与丢弃率 |
| `freeze_vit` | 默认值 | 仅千问 VL 适用；设为 true 才能按 Token 用量计费 |

万相图像 / 视频微调使用 `learning_rate`、`max_steps`/`n_epochs`、`lora_rank`、`max_pixels`、`save_total_limit` 等参数，不同子模型取值有差异，请参见 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。CosyVoice 调优使用 LM 与 FM 两套独立超参（`lm_max_epoch`/`fm_max_epoch` 等 8 个字段全部必填），推荐 `lm_max_epoch=60`、`fm_max_epoch=100`，最小化超参仅供跑通流程。

## 使用方式

### 控制台

前往「模型调优」页面点击「创建训练任务」，依次选择调优方式、基础模型、训练模态与思考模式、训练模式（全参 / 高效）、上传数据集并配置超参。任务优先级分 L0~L3 四级，影响调度顺序。零代码 SFT 流程示例可参见 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

### API / 命令行

通过 DashScope API 完成「上传文件 → 创建调优任务 → 查询状态 → 部署 → 调用」全流程，详见 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。核心步骤：

1. 上传数据集获取 `file_id`（`POST /api/v1/files`，`purpose=fine-tune`）。
2. 创建调优任务获取 `job_id` 与 `finetuned_output`（`POST /api/v1/fine-tunes`）。
3. 轮询任务状态直到 `SUCCEEDED`（`GET /api/v1/fine-tunes/<job_id>`）。
4. 部署为在线服务获取 `deployed_model`（`POST /api/v1/deployments`）。
5. 轮询部署状态直到 `RUNNING`，随后用 `deployed_model` 调用推理接口。

> **注意**：通过 API 创建的训练任务仅支持按 Token 计费，暂不支持模型训练单元（预付费 / 后付费）；如需使用训练单元请走控制台。CosyVoice 调优目前仅支持 API 方式，控制台暂不支持；且平台同一时刻仅运行一个 CosyVoice 训练任务，新任务进入 `QUEUING` 排队。

## 计费说明

文本生成模型按训练数据量计费：`费用 = (训练数据 Token 总数 + 混合训练数据 Token 总数) × 循环次数 × 训练单价`，最小计费单位 1 token。全参训练与高效训练费用相同。千问系列单价从 ¥0.003/千Token（Qwen3-0.6B）到 ¥0.15/千Token（Qwen2.5-72B-Instruct）不等。图像 / 视频生成微调按训练消耗的 `usage` 字段（总 Token 数）计费。CosyVoice 训练单价 ¥0.2/千Tokens，Token 消耗 ≈ `(lm_max_epoch + fm_max_epoch) × 25 × 训练集总时长(秒)`，部署另按模型单元使用时长计费。

## 典型场景

- **安全合规强化**：以 Qwen3-8B 为基础模型，用覆盖政治、历史、社会、网络安全等维度的指令数据集进行 SFT，将安全对齐目标写入模型参数。实验数据显示全量微调 `n_epochs=3, learning_rate=1e-5` 时 Pass 率可达 99%；LoRA `n_epochs=3, learning_rate=3e-4` 时 Pass 率 98%，更具性价比。
- **图像生成风格定制**：训练人物 LoRA、IP 角色风格化、末日废土红黑机甲等特效模型，调用时在 [prompt](prompt.md) 中包含触发词（如 `s86b5p`）激活风格。
- **视频特效定制**：训练「金钱雨」「时尚杂志」等特效 LoRA，部署时通过 `aigc_config` 配置预置 [prompt](prompt.md) 模板，调用时无需提示词即可复现训练集特效。
- **专属音色定制**：CosyVoice 调优面向同一发音人多条录音的高还原度场景，调优产物为单音色独立模型，调用时 `voice` 固定为 `default`。

## 限制与注意事项

- 所有调优功能仅限华北2（北京）地域；子账号需授予调用、训练、部署权限。
- 万相图像 / 视频微调训练耗时参考：文生图 2K/300 步约 77 分钟，图生图约 110 分钟；视频微调通常需数小时；CosyVoice 推荐超参训练耗时与 Token 消耗约为最小化超参的 20 倍。
- CosyVoice 调优训练轮次越高，基础模型原有能力「遗忘」越严重，可能导致长文本稳定性、多音字准确率退化；调优无法扩展基础模型不支持的语种，不支持 `instruction` 指令控制，不再提供声音复刻 / 声音设计能力。
- 图像 / 视频微调部署后调用参数用法与对应基础模型 API 基本一致，但需使用 `deployed_model` 名称，调用 LoRA 模型时建议关闭 `prompt_extend`。
- 思考模型训练样本中未使用 `<think>` 标签时，训练完成后不建议再开启思考模式调用。
- 视觉理解训练数据压缩包最大 2GB，图片单张宽高不超过 1024px、不超过 10MB；Qwen2.5-VL 训练坐标为缩放后图像左上角的绝对像素值，Qwen3-VL 为缩放到 `[0, 999]` 的相对坐标。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)


