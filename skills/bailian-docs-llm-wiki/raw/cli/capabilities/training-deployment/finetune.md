# 模型微调

阿里云百炼 CLI 按文本、音频、图像、视频模态创建和管理模型微调任务的命令速查。

在终端管理模型微调全生命周期：按文本、音频、图像、视频选择创建命令，管理微调任务、Checkpoint 和模型压缩。

> **重要**
>
> 任意命令追加 `--help` 可查看完整参数说明，例如 `bl finetune list --help`。本文命令明细中，原有命令以 bl 2.8.4 为基准核实，RL、OPD 和运行时管理命令以 bl 2.10.4 为基准核实。

<a id="按模态选择命令"></a>

## 按模态选择命令

| 模态 | 创建命令 | 说明 |
| --- | --- | --- |
| 文本 | `bl finetune text create` | 文本生成模型微调，支持 sft、sft-lora、dpo、dpo-lora、cpt |
| 音频 | `bl finetune audio create` | 音频模型微调 |
| 图像 | `bl finetune image create` | 图像生成模型微调 |
| 视频 | `bl finetune video create` | 视频生成模型微调 |

<a id="文本微调"></a>

## 文本微调

<a id="bl-finetune-text-create"></a>

### bl finetune text create

创建文本模型微调任务（sft | sft-lora | dpo | dpo-lora | cpt）。需要 API Key 鉴权。

**语法**

<a id="code-block"></a>

```bash
bl finetune text create
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--base-model <model>` | string | 是 | 要微调的基础模型（例如 qwen3-8b；不是输出模型名称） |
| `--datasets <ids\|paths>` | string | 是 | 数据集文件 ID 或本地路径，以逗号分隔（文本使用 .jsonl，音频、图片和视频使用 .zip）。本地路径会先验证并上传，再使用对应的 file-id。 |
| `--validations <ids\|paths>` | string | 否 | 验证数据集文件 ID 或本地路径，以逗号分隔（与 --datasets 一样自动上传）。 |
| `--model-name <name>` | string | 否 | 训练完成后的输出模型名称 |
| `--suffix <text>` | string | 否 | 平台追加的输出后缀（finetuned\_output\_suffix） |
| `--job-name <value>` | string | 否 | 训练任务显示名称（job\_name） |
| `--priority <value>` | string | 否 | 请求的调度优先级；请核对服务端回执 |
| `--eval-steps <value>` | number | 否 | 训练验证间隔步数 |
| `--lora-alpha <value>` | number | 否 | LoRA 缩放系数 |
| `--lora-dropout <value>` | number | 否 | LoRA 丢弃率 |
| `--lora-rank <value>` | number | 否 | LoRA 矩阵秩 |
| `--lr-scheduler-type <value>` | string | 否 | 所选模型支持的学习率调度策略 |
| `--save-strategy <value>` | string | 否 | Checkpoint 保存策略 |
| `--save-total-limit <value>` | number | 否 | 最多保存的 Checkpoint 数量 |
| `--save-steps <value>` | number | 否 | 按 steps 保存时的间隔 |
| `--split <value>` | number | 否 | 未指定验证集时训练集所占比例 |
| `--max-split-val-dataset-sample <value>` | number | 否 | 自动切分验证集的样本数量上限 |
| `--data-augmentation <value>` | string | 否 | 是否混入平台训练数据（true 或 false） |
| `--training-type <t>` | string | 否 | 训练类型：sft \| sft-lora \| dpo \| dpo-lora \| cpt（默认：sft-lora）。在接口边界转换为服务端值（例如 sft-lora -> efficient\_sft、dpo -> dpo\_full）。 |
| `--n-epochs <n>` | number | 否 | 训练轮数（默认：3） |
| `--batch-size <n>` | number | 否 | 单设备 Batch Size（限制在 \[8, 1024\]）。小数据集（<100KB）自动设为 8 |
| `--learning-rate <str>` | string | 否 | 以字符串形式指定学习率以保留精度（例如 "1.6e-5"） |
| `--max-length <n>` | number | 否 | 最大序列长度 |

**示例**：创建文本模型微调任务

<a id="code-block-2"></a>

```bash
bl finetune text create --base-model qwen3-8b --datasets file-xxx
```

-   训练类型遵循 `<method>` / `<method>-lora` 命名约定：sft（全量）| sft-lora（LoRA）| dpo（全量）| dpo-lora（LoRA）| cpt。这些值会在接口边界映射为服务端 training\_type，因此 CLI 的其他部分不会接触服务端原始字符串。
-   提交任务前（非 dry-run），会通过 listFoundationModels 检查模型训练能力（无需登录控制台）；如果训练类型不受支持，会立即失败并列出该模型实际支持的训练类型。
-   n\_epochs 默认为 3。其他超参数未设置时使用平台默认值。
-   学习率以字符串形式传递，避免 JSON 数字精度损失。
-   提交前检查：如果训练数据集的样本数不大于 batch\_size，会在上传或消耗额度前拒绝任务（否则平台会在数据处理约 10 分钟后才失败）。

<a id="音频微调"></a>

## 音频微调

<a id="bl-finetune-audio-create"></a>

### bl finetune audio create

创建音频 TTS 模型微调任务（sft-lora）。需要 API Key 鉴权。

**语法**

<a id="code-block-3"></a>

```bash
bl finetune audio create
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--base-model <model>` | string | 是 | 要微调的基础模型（例如 qwen3-8b；不是输出模型名称） |
| `--datasets <ids\|paths>` | string | 是 | 数据集文件 ID 或本地路径，以逗号分隔（文本使用 .jsonl，音频、图片和视频使用 .zip）。本地路径会先验证并上传，再使用对应的 file-id。 |
| `--validations <ids\|paths>` | string | 否 | 验证数据集文件 ID 或本地路径，以逗号分隔（与 --datasets 一样自动上传）。 |
| `--model-name <name>` | string | 否 | 训练完成后的输出模型名称 |
| `--suffix <text>` | string | 否 | 平台追加的输出后缀（finetuned\_output\_suffix） |

**示例**：创建音频 TTS 模型微调任务

<a id="code-block-4"></a>

```bash
bl finetune audio create --base-model cosyvoice-v3-flash --datasets ./audio.zip
```

-   音频 TTS 训练使用 sft-lora（efficient\_sft）和固定的 CosyVoice 超参数默认值；没有可设置的训练类型或超参数选项。

<a id="图像微调"></a>

## 图像微调

<a id="bl-finetune-image-create"></a>

### bl finetune image create

创建图片生成模型微调任务（sft-lora）。需要 API Key 鉴权。

**语法**

<a id="code-block-5"></a>

```bash
bl finetune image create
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--base-model <model>` | string | 是 | 要微调的基础模型（例如 qwen3-8b；不是输出模型名称） |
| `--datasets <ids\|paths>` | string | 是 | 数据集文件 ID 或本地路径，以逗号分隔（文本使用 .jsonl，音频、图片和视频使用 .zip）。本地路径会先验证并上传，再使用对应的 file-id。 |
| `--validations <ids\|paths>` | string | 否 | 验证数据集文件 ID 或本地路径，以逗号分隔（与 --datasets 一样自动上传）。 |
| `--model-name <name>` | string | 否 | 训练完成后的输出模型名称 |
| `--suffix <text>` | string | 否 | 平台追加的输出后缀（finetuned\_output\_suffix） |
| `--generation-type <t2i\|i2i>` | string | 否 | 生成类型：t2i（默认）\| i2i。用于设置 generation\_type/max\_pixels。通过 file-id 训练 I2I 或使用 --dry-run 时必填（本地数据会自动识别 input\_img）。 |
| `--learning-rate <str>` | string | 否 | 以字符串形式指定学习率以保留精度（例如 "3e-5"） |

**示例**：创建图片生成模型微调任务

<a id="code-block-6"></a>

```bash
bl finetune image create --base-model wan2.7-image-pro --datasets ./images.zip
```

-   图片生成训练使用 sft-lora（efficient\_sft）和固定默认值；仅 --learning-rate 可覆盖。通过 --generation-type（默认 t2i）声明 T2I 或 I2I，并设置 generation\_type/max\_pixels。本地数据会自动识别类型（包含 input\_img 的记录训练 I2I）；通过 file-id 训练 I2I 或使用 --dry-run 时，请显式传入 --generation-type。

<a id="视频微调"></a>

## 视频微调

<a id="bl-finetune-video-create"></a>

### bl finetune video create

创建视频生成模型微调任务（Wan i2v/kf2v，efficient\_sft）。需要 API Key 鉴权。

**语法**

<a id="code-block-7"></a>

```bash
bl finetune video create
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--base-model <model>` | string | 是 | 要微调的基础模型（例如 qwen3-8b；不是输出模型名称） |
| `--datasets <ids\|paths>` | string | 是 | 数据集文件 ID 或本地路径，以逗号分隔（文本使用 .jsonl，音频、图片和视频使用 .zip）。本地路径会先验证并上传，再使用对应的 file-id。 |
| `--validations <ids\|paths>` | string | 否 | 验证数据集文件 ID 或本地路径，以逗号分隔（与 --datasets 一样自动上传）。 |
| `--model-name <name>` | string | 否 | 训练完成后的输出模型名称 |
| `--suffix <text>` | string | 否 | 平台追加的输出后缀（finetuned\_output\_suffix） |
| `--n-epochs <n>` | number | 否 | 训练轮数（默认：50） |
| `--batch-size <n>` | number | 否 | Batch Size（默认值因模型而异：wan2.7 为 1，wan2.5/2.2 为 4） |
| `--learning-rate <str>` | string | 否 | 以字符串形式指定学习率以保留精度（默认："2e-5"） |

**示例**：创建视频生成模型微调任务

<a id="code-block-8"></a>

```bash
bl finetune video create --base-model wan2.7-i2v --datasets file-xxx
```

-   视频生成训练（Wan i2v/kf2v）使用 efficient\_sft 和模型专属默认值：wan2.7（batch\_size=1、max\_pixels=102400），wan2.5/2.2（batch\_size=4，max\_pixels 因模型而异）。可通过 --batch-size/--n-epochs 覆盖。
-   数据集为包含 data.jsonl、帧图片和视频的 .zip 归档。
-   建议至少准备 10 个训练样本；20–100 个样本可获得更稳定的效果。

<a id="微调任务管理"></a>

## 微调任务管理

<a id="bl-finetune-list"></a>

### bl finetune list

列出微调任务。需要 API Key 鉴权。

**语法**

<a id="code-block-9"></a>

```bash
bl finetune list [--page <n>] [--page-size <n>] [--status <s>] [--base-model <model>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--page <n>` | number | 否 | 页码（默认：1） |
| `--page-size <n>` | number | 否 | 每页结果数（默认：10，最多：100） |
| `--status <s>` | string | 否 | 按状态筛选（PENDING / RUNNING / SUCCEEDED / FAILED / CANCELED） |
| `--base-model <model>` | string | 否 | 按基础模型 ID 筛选（服务端筛选） |

**示例**：列出运行中的微调任务

<a id="code-block-10"></a>

```bash
bl finetune list --status RUNNING
```

<a id="bl-finetune-get"></a>

### bl finetune get

获取单个微调任务的详情。需要 API Key 鉴权。

**语法**

<a id="code-block-11"></a>

```bash
bl finetune get --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 微调任务 ID |

**示例**：获取单个微调任务详情

<a id="code-block-12"></a>

```bash
bl finetune get --job-id ft-xxx
```

<a id="bl-finetune-watch"></a>

### bl finetune watch

查询微调任务状态（默认：单次非阻塞获取）。使用 --follow 持续轮询至终态。需要 API Key 鉴权。

**语法**

<a id="code-block-13"></a>

```bash
bl finetune watch --job-id <id> [--follow] [--interval <sec>] [--poll-timeout <sec>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 微调任务 ID |
| `--follow` | switch | 否 | 阻塞并轮询至终态（旧版行为）。不使用时仅查询一次状态并立即返回。 |
| `--interval <sec>` | number | 否 | 使用 --follow 时的轮询间隔秒数（默认：${DEFAULT\_INTERVAL\_SEC}，最小：${MIN\_INTERVAL\_SEC}）。未使用 --follow 时忽略。 |
| `--poll-timeout <sec>` | number | 否 | 使用 --follow 时，在指定秒数后停止轮询（默认：无限制）。未使用 --follow 时忽略。 |

**示例**：查询微调任务状态

<a id="code-block-14"></a>

```bash
bl finetune watch --job-id ft-xxx                       # 单次查询，立即返回
```

-   默认不使用 --follow，执行非阻塞的单次状态查询：获取一次后立即返回。该模式适用于 Agent / 脚本，由调用方控制轮询节奏，CLI 不会持续占用终端。
-   终态 FAILED/CANCELED 会触发普通 CLI 错误（非零退出码）；SUCCEEDED 或仍在运行时返回 0。使用 --follow 时，超过 --poll-timeout 会触发超时错误。
-   需要在人工终端中阻塞跟踪时使用 --follow；自行驱动轮询（例如通过 Agent）时使用默认模式。
-   要查看逐步骤训练输出（而非状态），请使用 `finetune logs`。

<a id="bl-finetune-logs"></a>

### bl finetune logs

获取微调任务的训练日志。需要 API Key 鉴权。

**语法**

<a id="code-block-15"></a>

```bash
bl finetune logs --job-id <id> [--page <n>] [--page-size <n>] [--search <keyword>] [--tail <n>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 微调任务 ID |
| `--page <n>` | number | 否 | 页码（默认：1） |
| `--page-size <n>` | number | 否 | 每页行数（默认：由服务端决定） |
| `--search <keyword>` | string | 否 | 不区分大小写的子字符串筛选。设置后会获取全部日志页并在客户端筛选（忽略 --page）。 |
| `--tail <n>` | number | 否 | 仅保留最后 N 条记录。设置后会获取全部日志页并保留末尾 N 条（忽略 --page）。 |

**示例**：获取微调任务训练日志

<a id="code-block-16"></a>

```bash
bl finetune logs --job-id ft-xxx
```

<a id="bl-finetune-metrics"></a>

### bl finetune metrics

查询微调任务的训练指标。需要 API Key 鉴权。

**语法**

<a id="code-block-17"></a>

```bash
bl finetune metrics --job-id <id> [--page <n>] [--page-size <n>] [--workspace-id <id>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 微调任务 ID |
| `--page <n>` | number | 否 | 页码，从 1 开始（默认：1） |
| `--page-size <n>` | number | 否 | 每页记录数（默认：100） |
| `--workspace-id <id>` | string | 否 | 作为 X-DashScope-WorkSpace 发送的工作空间 ID，使用任务所属工作空间。API Key 已绑定工作空间时可省略。 |

**示例**：查询微调任务的训练指标

<a id="code-block-18"></a>

```bash
bl finetune metrics --job-id ft-xxx
```

-   查询 `GET /api/v1/fine-tunes/{job_id}/basic_metrics`。每条指标记录原样返回（step 加动态指标字段）；空列表是正常结果。
-   指标不在服务端筛选，接口返回完整结果，由调用方从每条记录中选取指标字段。使用 --page/--page-size 分页。

<a id="bl-finetune-checkpoints"></a>

### bl finetune checkpoints

列出微调任务生成的 Checkpoint。需要 API Key 鉴权。

**语法**

<a id="code-block-19"></a>

```bash
bl finetune checkpoints --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 微调任务 ID |

**示例**：列出微调任务生成的 Checkpoint

<a id="code-block-20"></a>

```bash
bl finetune checkpoints --job-id ft-xxx
```

-   SUCCEEDED Checkpoint 中显示的 `model_name` 可直接作为 `deploy create --model-name` 的输入。
-   Checkpoint 创建后约 15 天过期，`expire_time` 显示截止时间。请在过期前导出或部署。

<a id="bl-finetune-export"></a>

### bl finetune export

将 Checkpoint 发布为可部署模型。需要 API Key 鉴权。

**语法**

<a id="code-block-21"></a>

```bash
bl finetune export --job-id <id> --checkpoint <name> --model-name <name>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 微调任务 ID |
| `--checkpoint <name>` | string | 是 | 来自 `finetune checkpoints` 的 Checkpoint 标识 |
| `--model-name <name>` | string | 是 | 可部署模型名称 |

**示例**：将 Checkpoint 发布为可部署模型

<a id="code-block-22"></a>

```bash
bl finetune export --job-id ft-xxx --checkpoint ckpt-3 --model-name my-qwen-sft
```

-   必须先执行此操作，`deploy <modality> create` 才能使用 Checkpoint。任务达到 SUCCEEDED 后，平台可能自动导出最佳 Checkpoint；对于非最佳 Checkpoint，显式导出是标准方式。

<a id="bl-finetune-cancel"></a>

### bl finetune cancel

取消正在运行的微调任务。需要 API Key 鉴权。

**语法**

<a id="code-block-23"></a>

```bash
bl finetune cancel --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 微调任务 ID |

**示例**：取消正在运行的微调任务

<a id="code-block-24"></a>

```bash
bl finetune cancel --job-id ft-xxx
```

-   只有 PENDING / RUNNING 状态的任务可以取消。已完成、失败或已取消的任务会返回服务端错误（原样透传）。

<a id="bl-finetune-delete"></a>

### bl finetune delete

删除微调任务记录。需要 API Key 鉴权。

**语法**

<a id="code-block-25"></a>

```bash
bl finetune delete --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 微调任务 ID |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

> **警告**
>
> 该操作会永久删除指定的微调任务记录，且无法撤销。

**示例**：删除微调任务记录

<a id="code-block-26"></a>

```bash
bl finetune delete --job-id ft-xxx
```

-   该操作不可撤销——任务记录将被永久删除。
-   请先通过 `finetune cancel` 取消 RUNNING 任务，平台拒绝删除仍在运行的任务。

<a id="bl-finetune-capability"></a>

### bl finetune capability

查询微调训练能力：按模型查询其支持的训练类型，或按训练类型查询支持它的模型。无需鉴权。

**语法**

<a id="code-block-27"></a>

```bash
bl finetune capability --base-model <m> | --training-type <t>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--base-model <m>` | string | 否 | 列出该基础模型支持的训练类型。 |
| `--training-type <t>` | string | 否 | 列出支持该训练类型的模型：sft \| sft-lora \| dpo \| dpo-lora \| cpt。 |

**示例**：查询 qwen3-8b 模型支持的训练类型

<a id="code-block-28"></a>

```bash
bl finetune capability --base-model qwen3-8b
```

-   \--base-model 和 --training-type 必须且只能指定一个。
-   训练类型遵循 `<method>` / `<method>-lora` 命名约定：sft | sft-lora | dpo | dpo-lora | cpt。（服务端没有 cpt-lora 变体。）
-   查询公开 API listFoundationModels，无需登录控制台。

<a id="bl-finetune-params"></a>

### bl finetune params

查询基础模型的训练超参配置。需要 API Key 鉴权。

**语法**

<a id="code-block-29"></a>

```bash
bl finetune params --base-model <model> [--training-type <t>] [--param-type <hyper|resource>] [--mtu-spec-code <code>] [--modality <text|vision>] [--reasoning-mode <instruct|thinking>] [--lang <locale>] [--workspace-id <id>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--base-model <model>` | string | 是 | 要查询训练参数的基础模型（例如 qwen3-8b） |
| `--training-type <t>` | string | 否 | 训练类型：sft \| sft-lora \| dpo \| dpo-lora \| cpt（默认：sft-lora）。映射为服务端 training\_type（例如 sft-lora -> efficient\_sft）。 |
| `--mtu-spec-code <code>` | string | 否 | MTU 规格代码，资源组查询时必填（例如 MTU2） |
| `--param-type <hyper\|resource>` | string | 否 | 参数组：hyper \| resource。省略时返回全部参数组。 |
| `--modality <text\|vision>` | string | 否 | 训练模态：text \| vision。仅对支持动态训练选项的模型有效；作为 hyper\_parameters 中的 modality 发送。 |
| `--reasoning-mode <instruct\|thinking>` | string | 否 | 推理模式：instruct（非思考）\| thinking。仅对支持动态训练选项的模型有效；作为 hyper\_parameters 中的 reasoning\_mode 发送。 |
| `--lang <locale>` | string | 否 | 服务端展示文本的语言（例如 en、zh）。省略时使用服务端默认值。 |
| `--workspace-id <id>` | string | 否 | 作为 X-DashScope-WorkSpace 发送的工作空间 ID。API Key 已绑定工作空间时可省略。 |

**示例**：查询基础模型的训练超参

<a id="code-block-30"></a>

```bash
bl finetune params --base-model qwen3-8b
```

**示例**：查询动态训练选项

<a id="code-block-31"></a>

```bash
bl finetune params --base-model qwen3.7-plus-2026-05-26 --modality vision --reasoning-mode thinking
```

-   查询 GET /api/v1/fine-tunes/fine-tunes-params。每个 hyper\_params 条目保留服务端字段名（recommend\_value、defaultValue、is\_advanced\_parameter 等）。
-   \--modality / --reasoning-mode 合并为一个 hyper\_parameters JSON 查询参数。支持的值和组合因模型而异；无效组合由服务端拒绝并原样返回。不支持动态训练选项的模型会忽略这两个参数。
-   输出中的 resume\_from\_checkpoint 表示该训练类型是否支持恢复训练。

<a id="bl-finetune-price"></a>

### bl finetune price

估算微调任务的训练费用（按 Token 计费）。

**语法**

<a id="code-block-32"></a>

```bash
bl finetune price --base-model <model> --datasets <ids> [--training-type <type>] [--n-epochs <n>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--base-model <model>` | string | 是 | 待微调的基座模型（例如 qwen3-8b；不是输出模型名称） |
| `--datasets <ids>` | string | 是 | 训练数据集文件 ID，多个以逗号分隔 |
| `--training-type <type>` | string | 否 | 训练类型：sft \| dpo \| cpt（默认：sft） |
| `--n-epochs <n>` | number | 否 | 训练轮数（默认：3） |

**示例**：估算 qwen3-8b 使用 file-ft-xxx 数据集的微调费用

<a id="code-block-33"></a>

```bash
bl finetune price --base-model qwen3-8b --datasets file-ft-xxx
```

-   该结果仅为估算值——服务端根据数据集计算 Token 用量，最终费用以账单为准。
-   支持估算 sft / dpo / cpt 的 Token 计费；此命令不支持训练单元（MTU）计费估算。
-   除 --n-epochs 外，其他超参数会使用具有代表性的固定默认值进行估算。

<a id="模型压缩"></a>

## 模型压缩

模型压缩用于量化支持的全参微调模型。先通过 `templates` 查询可用模板，再创建压缩任务；任务成功后，返回的 `quantized_output` 可作为 `deploy text create --model-name` 的输入。模型压缩 API 目前仅在北京地域开放。

<a id="bl-finetune-compress-templates"></a>

### bl finetune compress templates

列出可量化的模型及其压缩模板。需要 API Key 鉴权。

**语法**

<a id="code-block-34"></a>

```bash
bl finetune compress templates [--model <model>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 否 | 按自定义模型 ID 或基础模型名称筛选 |

**示例**：查看支持压缩的模型和模板

<a id="code-block-35"></a>

```bash
bl finetune compress templates
```

-   仅返回支持的全参微调模型；LoRA 模型和已量化模型不会返回。
-   模板 ID 位于 `output.custom_models[].templates[].template_id`。`output.base_models` 只列出可量化的基础模型名称，不包含模板 ID。
-   `templates[].hyper_parameters` 为空表示该模板没有可调超参数，创建压缩任务时省略 --hparam。

<a id="bl-finetune-compress-create"></a>

### bl finetune compress create

创建模型压缩任务。需要 API Key 鉴权。

**语法**

<a id="code-block-36"></a>

```bash
bl finetune compress create --model <model> --template-id <id> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 是 | 源自定义模型 ID |
| `--template-id <id>` | string | 是 | 压缩模板 ID |
| `--job-name <name>` | string | 否 | 唯一任务名称，最多 50 个字符 |
| `--description <text>` | string | 否 | 任务描述，最多 200 个字符 |
| `--hparam <key=value>` | array | 否 | 覆盖超参数（可重复） |
| `--calibration-files <file-id,...>` | string | 否 | 校准数据集文件 ID，多个用逗号分隔 |
| `--suffix <suffix>` | string | 否 | 输出模型后缀（1–8 个小写字母或数字） |

**示例**：使用指定模板创建压缩任务

<a id="code-block-37"></a>

```bash
bl finetune compress create --model qwen3.5-flash-2026-02-23-ft-xxx --template-id quant-flash-nvfp4-mlp-nomtp
```

<a id="bl-finetune-compress-list"></a>

### bl finetune compress list

列出模型压缩任务。需要 API Key 鉴权。

**语法**

<a id="code-block-38"></a>

```bash
bl finetune compress list [filters] [--page <n>] [--page-size <n>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--status <status>` | string | 否 | 按任务状态筛选 |
| `--model <model>` | string | 否 | 按源模型 ID 筛选 |
| `--template-id <id>` | string | 否 | 按模板 ID 筛选 |
| `--quant-spec <spec>` | string | 否 | 按量化规格筛选 |
| `--quant-method <method>` | string | 否 | 按量化方法筛选 |
| `--start-time <time>` | string | 否 | 任务开始时间不早于该时间 |
| `--end-time <time>` | string | 否 | 任务结束时间不晚于该时间 |
| `--search <keyword>` | string | 否 | 搜索任务 ID 或名称 |
| `--search-field <job_id\|job_name>` | string | 否 | 将 --search 限定为任务 ID 或名称 |
| `--sort-order <asc\|desc>` | string | 否 | 按创建时间排序（默认：desc） |
| `--page <n>` | number | 否 | 页码（默认：1） |
| `--page-size <n>` | number | 否 | 每页结果数（默认：10，最多：100） |

**示例**：列出最近成功的压缩任务

<a id="code-block-39"></a>

```bash
bl finetune compress list --status SUCCEEDED --page-size 20
```

<a id="bl-finetune-compress-get"></a>

### bl finetune compress get

获取模型压缩任务详情。需要 API Key 鉴权。

**语法**

<a id="code-block-40"></a>

```bash
bl finetune compress get --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 压缩任务 ID |

**示例**：查看指定压缩任务详情

<a id="code-block-41"></a>

```bash
bl finetune compress get --job-id quant-xxx
```

<a id="bl-finetune-compress-watch"></a>

### bl finetune compress watch

探测或持续跟踪压缩任务状态。需要 API Key 鉴权。

**语法**

<a id="code-block-42"></a>

```bash
bl finetune compress watch --job-id <id> [--follow] [--interval <sec>] [--poll-timeout <sec>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 压缩任务 ID |
| `--follow` | switch | 否 | 轮询直到任务进入终态 |
| `--interval <sec>` | number | 否 | 使用 --follow 时的轮询间隔（默认：10，最小：1） |
| `--poll-timeout <sec>` | number | 否 | 超过该时长后停止轮询 |

**示例**：持续跟踪压缩任务直到结束

<a id="code-block-43"></a>

```bash
bl finetune compress watch --job-id quant-xxx --follow
```

-   不传 --follow 时只执行一次非阻塞状态探测。
-   任务成功后，可将 `quantized_output` 传给 `deploy text create --model-name`。

<a id="bl-finetune-compress-logs"></a>

### bl finetune compress logs

获取模型压缩任务日志。需要 API Key 鉴权。

**语法**

<a id="code-block-44"></a>

```bash
bl finetune compress logs --job-id <id> [--offset <n>] [--lines <n> | --tail <n>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 压缩任务 ID |
| `--offset <n>` | number | 否 | 跳过前 N 行（默认：0） |
| `--lines <n>` | number | 否 | 读取行数（默认：100，最多：1000） |
| `--tail <n>` | number | 否 | 读取最后 N 行日志 |

**示例**：读取最后 20 行压缩日志

<a id="code-block-45"></a>

```bash
bl finetune compress logs --job-id quant-xxx --tail 20
```

<a id="bl-finetune-compress-cancel"></a>

### bl finetune compress cancel

取消模型压缩任务。需要 API Key 鉴权。

**语法**

<a id="code-block-46"></a>

```bash
bl finetune compress cancel --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 压缩任务 ID |

**示例**：取消指定压缩任务

<a id="code-block-47"></a>

```bash
bl finetune compress cancel --job-id quant-xxx
```

-   仅 PENDING、QUEUING 或 RUNNING 状态的任务可以取消。

<a id="bl-finetune-compress-delete"></a>

### bl finetune compress delete

删除模型压缩任务记录。需要 API Key 鉴权。

**语法**

<a id="code-block-48"></a>

```bash
bl finetune compress delete --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | 压缩任务 ID |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

> **警告**
>
> 该操作会永久删除压缩任务记录，且无法撤销。

**示例**：预览删除指定压缩任务记录

<a id="code-block-49"></a>

```bash
bl finetune compress delete --job-id quant-xxx --dry-run
```

-   仅终态任务可以删除；删除任务记录不会删除其量化输出模型。

<a id="强化学习训练"></a>

## 强化学习训练

<a id="bl-finetune-rl-authorize"></a>

### bl finetune rl authorize

检查并授权强化学习训练访问权限（准入白名单、服务关联角色、业务开通状态）。需要控制台鉴权。

**语法**

<a id="code-block-50"></a>

```bash
bl finetune rl authorize [--authorize]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--authorize` | switch | 否 | 在服务角色已手动授权后允许启用 RL（不带此 flag 时为只读探测） |
| `--yes` | switch | 否 | 确认执行此高风险操作 |
| `--console-region <region>` | string | 否 | 控制台网关地域（如 cn-beijing、ap-southeast-1） |
| `--console-site <site>` | string | 否 | 控制台站点：domestic、international |
| `--workspace-id <id>` | string | 否 | 业务空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID） |

> **警告**
>
> CLI 绝不自动创建服务关联角色。缺失角色时返回 REQUIRES\_USER\_ACTION 并中止，需先按[环境准备](../../../model-user-guide/model-training/fine-tuning/rl-overview/rl-training-overview.md#wjp6ghg8df9o4)手动授权。

**示例**：只读探测 RL 准入状态

<a id="code-block-51"></a>

```bash
bl finetune rl authorize
```

**示例**：仅在明确确认后启用 RL

<a id="code-block-52"></a>

```bash
bl finetune rl authorize --authorize --yes
```

-   不带 `--authorize` 时为只读探测，每项能力报告 READY / MISSING / UNKNOWN / REQUIRES\_USER\_ACTION / FAILED；查询失败视为 UNKNOWN，不假定已启用。
-   仅启用 RL，不自动启用 OPD。CI 中传 `--authorize --yes` 以允许变更；单独 `--yes` 不扩展权限。

<a id="bl-finetune-rl-run"></a>

### bl finetune rl run

提交强化学习训练任务。需要 API Key 鉴权。

**语法**

<a id="code-block-53"></a>

```bash
bl finetune rl run --model <id> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--config-file <path>` | string | 否 | 可选的任务 YAML 文件；显式 CLI flag 优先 |
| `--name <name>` | string | 否 | 任务名称 |
| `--model <id>` | string | 否 | 基座模型 ID |
| `--train-file <path>` | array | 否 | 本地训练文件（可重复） |
| `--train-file-id <id>` | array | 否 | 已上传的训练文件 ID（可重复） |
| `--validation-file <path>` | array | 否 | 本地验证文件（可重复） |
| `--validation-file-id <id>` | array | 否 | 已上传的验证文件 ID（可重复） |
| `--code-dir <path>` | string | 否 | 函数包源码目录 |
| `--requirements <path>` | string | 否 | 相对于 code-dir 的 requirements 路径 |
| `--rollout <classpath>` | string | 否 | Rollout 函数类路径 |
| `--reward <name=classpath>` | array | 否 | Reward 函数（可重复） |
| `--hp <key=value>` | array | 否 | 超参数（可重复，按类型解析） |
| `--charge-type <value>` | string | 否 | 资源计费方式 |
| `--mtu-spec <code>` | string | 否 | MTU 规格代码 |
| `--mtu-count <int>` | number | 否 | MTU 容量 |
| `--watch` | switch | 否 | 等待任务到达终态 |
| `--wait-timeout <seconds>` | number | 否 | `--watch` 最大轮询秒数（默认不限；超时不取消云端任务） |
| `--install-runtime` | switch | 否 | 允许首次准备托管运行时 |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

> **警告**
>
> 该操作创建计费的 RL 训练任务，消耗算力资源。在隔离沙箱内运行，需先通过 `bl finetune runtime prepare` 准备运行时，或传 `--install-runtime`。

**示例**：提交 RL 训练任务并等待完成

<a id="code-block-54"></a>

```bash
bl finetune rl run --model qwen3.5-9b --train-file ./data/train.jsonl --code-dir . --rollout functions.rollout.MyRollout --charge-type mtu_postpaid --mtu-spec MTU4 --mtu-count 24 --watch
```

**示例**：通过 YAML 配置提交任务

<a id="code-block-55"></a>

```bash
bl finetune rl run --config-file job.yaml --watch
```

**示例**：预览任务规格（不提交）

<a id="code-block-56"></a>

```bash
bl finetune rl run --model qwen3.5-9b --train-file ./data/train.jsonl --dry-run
```

-   `--watch` 超时仅停止等待，不取消云端任务。

<a id="bl-finetune-rl-get"></a>

### bl finetune rl get

获取强化学习训练任务详情。需要 API Key 鉴权。

**语法**

<a id="code-block-57"></a>

```bash
bl finetune rl get --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | RL 任务 ID |

<a id="bl-finetune-rl-list"></a>

### bl finetune rl list

列出强化学习训练任务。需要 API Key 鉴权。

**语法**

<a id="code-block-58"></a>

```bash
bl finetune rl list
```

<a id="bl-finetune-rl-watch"></a>

### bl finetune rl watch

探测 RL 任务状态（默认单次非阻塞获取）。需要 API Key 鉴权。

**语法**

<a id="code-block-59"></a>

```bash
bl finetune rl watch --job-id <id> [--follow] [--interval <sec>] [--poll-timeout <sec>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | RL 任务 ID |
| `--follow` | switch | 否 | 阻塞轮询直至终态；不带此 flag 时单次获取后立即返回 |
| `--interval <sec>` | number | 否 | `--follow` 轮询间隔秒数（默认 10，最小 1） |
| `--poll-timeout <sec>` | number | 否 | `--follow` 最大轮询秒数（默认不限） |

**示例**：单次状态探测

<a id="code-block-60"></a>

```bash
bl finetune rl watch --job-id ft-xxx
```

**示例**：持续轮询直至终态

<a id="code-block-61"></a>

```bash
bl finetune rl watch --job-id ft-xxx --follow
```

-   默认（无 `--follow`）为非阻塞单次探测。终态 FAILED/CANCELED 返回非零退出码；SUCCEEDED 或仍在运行返回 0。
-   直接查询 fine-tunes 端点，无需沙箱运行时。逐步训练输出请使用 `bl finetune rl logs`。

<a id="bl-finetune-rl-logs"></a>

### bl finetune rl logs

获取强化学习训练任务日志。需要 API Key 鉴权。

**语法**

<a id="code-block-62"></a>

```bash
bl finetune rl logs --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | RL 任务 ID |

<a id="bl-finetune-rl-cancel"></a>

### bl finetune rl cancel

取消强化学习训练任务。需要 API Key 鉴权。

**语法**

<a id="code-block-63"></a>

```bash
bl finetune rl cancel --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | RL 任务 ID |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

-   仅 PENDING、QUEUING 或 RUNNING 状态的任务可以取消。

<a id="bl-finetune-rl-delete"></a>

### bl finetune rl delete

删除强化学习训练任务记录。需要 API Key 鉴权。

**语法**

<a id="code-block-64"></a>

```bash
bl finetune rl delete --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | RL 任务 ID |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

> **警告**
>
> 该操作会永久删除任务记录，且无法撤销。

-   仅终态任务可以删除。

<a id="在线蒸馏-opd"></a>

## 在线蒸馏（OPD）

<a id="bl-finetune-opd-authorize"></a>

### bl finetune opd authorize

检查并授权在线蒸馏访问权限。需要控制台鉴权。

**语法**

<a id="code-block-65"></a>

```bash
bl finetune opd authorize [--authorize]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--authorize` | switch | 否 | 在服务角色已手动授权后允许启用 OPD（不带此 flag 时为只读探测） |
| `--yes` | switch | 否 | 确认执行此高风险操作 |
| `--workspace-id <id>` | string | 否 | 业务空间 ID |

> **警告**
>
> CLI 绝不自动创建服务关联角色。缺失角色时返回 REQUIRES\_USER\_ACTION 并中止。

<a id="bl-finetune-opd-run"></a>

### bl finetune opd run

提交纯模型在线蒸馏任务（pg\_opd）。需要 API Key 鉴权。

**语法**

<a id="code-block-66"></a>

```bash
bl finetune opd run --base-model <id> --teacher-model <id> --datasets <ids|paths> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--base-model <id>` | string | 是 | 学生基座模型 ID（如 qwen3.5-9b） |
| `--teacher-model <id>` | string | 是 | 平台登记的教师模型 ID（不接受任意 URL 或密钥） |
| `--datasets <ids\|paths>` | string | 是 | 逗号分隔的数据集文件 ID 或本地 .jsonl 路径；本地路径先验证并上传 |
| `--validations <ids\|paths>` | string | 否 | 逗号分隔的验证文件 ID 或本地路径（自动上传） |
| `--job-name <name>` | string | 否 | 训练任务显示名称 |
| `--hyper-parameters-file <path>` | string | 否 | 训练与资源超参数 JSON 文件；`--hp` 优先覆盖 |
| `--resource-config-file <path>` | string | 否 | resource\_config JSON 文件（charge\_type / mtu\_spec\_code / mtu\_capacity）；资源 flag 优先覆盖 |
| `--hp <key=value>` | array | 否 | 超参数覆盖（可重复，按类型解析） |
| `--charge-type <value>` | string | 否 | resource\_config.charge\_type；pg\_opd 仅支持 mtu\_postpaid（默认） |
| `--mtu-spec <code>` | string | 否 | resource\_config.mtu\_spec\_code（如 MTU4）；必需 |
| `--mtu-count <int>` | number | 否 | resource\_config.mtu\_capacity（学生 GPU + 教师 GPU）；必需 |
| `--workspace-id <id>` | string | 否 | 用于上传、参数查询、创建和读取的业务空间 |
| `--watch` | switch | 否 | 等待任务到达终态 |
| `--wait-timeout <seconds>` | number | 否 | `--watch` 最大轮询秒数（默认不限；超时不取消云端任务） |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

> **警告**
>
> 该操作创建计费的 OPD 训练任务，消耗算力资源。强制 training\_type=pg\_opd，无需 rollout/reward 函数，不创建函数计算资源。直接从宿主机通过 fine-tunes OpenAPI 提交，无需沙箱运行时。

**示例**：预览任务规格（不提交）

<a id="code-block-67"></a>

```bash
bl finetune opd run --base-model qwen3.5-9b --teacher-model qwen3.8-flash --datasets file-xxx --hyper-parameters-file ./hp.json --resource-config-file ./resource.json --dry-run
```

**示例**：提交 OPD 训练任务并等待完成

<a id="code-block-68"></a>

```bash
bl finetune opd run --base-model qwen3.5-9b --teacher-model qwen3.5-397b-a17b --datasets ./train.jsonl --hp n_epochs=1 --hp batch_size=64 --charge-type mtu_postpaid --mtu-spec MTU4 --mtu-count 24 --watch
```

-   超参数按原样发送（JSON 文件 → `--hp` 覆盖）。省略字段由服务端和所选教师默认值解析，CLI 不填充 recommend\_value。
-   mtu\_capacity 必须等于学生 GPU + 教师 GPU。推荐配置及模型配对参见[模型与训练单元](../../../model-user-guide/model-training/fine-tuning/opd-overview/opd-training-overview.md#opd-models)。
-   `--watch` 超时仅停止等待，不取消云端任务。

<a id="bl-finetune-opd-params"></a>

### bl finetune opd params

查询学生基座模型支持的超参数。需要 API Key 鉴权。

**语法**

<a id="code-block-69"></a>

```bash
bl finetune opd params --base-model <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--base-model <id>` | string | 是 | 学生基座模型 ID |

<a id="bl-finetune-opd-get"></a>

### bl finetune opd get

获取在线蒸馏任务详情。需要 API Key 鉴权。

**语法**

<a id="code-block-70"></a>

```bash
bl finetune opd get --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | OPD 任务 ID |

<a id="bl-finetune-opd-watch"></a>

### bl finetune opd watch

探测 OPD 任务状态。需要 API Key 鉴权。

**语法**

<a id="code-block-71"></a>

```bash
bl finetune opd watch --job-id <id> [--follow] [--interval <sec>] [--poll-timeout <sec>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | OPD 任务 ID |
| `--follow` | switch | 否 | 阻塞轮询直至终态 |
| `--interval <sec>` | number | 否 | `--follow` 轮询间隔秒数（默认 10） |
| `--poll-timeout <sec>` | number | 否 | `--follow` 最大轮询秒数（默认不限） |

<a id="bl-finetune-opd-logs"></a>

### bl finetune opd logs

获取在线蒸馏任务日志。需要 API Key 鉴权。

**语法**

<a id="code-block-72"></a>

```bash
bl finetune opd logs --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | OPD 任务 ID |

<a id="bl-finetune-opd-cancel"></a>

### bl finetune opd cancel

取消在线蒸馏任务。需要 API Key 鉴权。

**语法**

<a id="code-block-73"></a>

```bash
bl finetune opd cancel --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | OPD 任务 ID |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

-   仅 PENDING、QUEUING 或 RUNNING 状态的任务可以取消。

<a id="bl-finetune-opd-delete"></a>

### bl finetune opd delete

删除在线蒸馏任务记录。需要 API Key 鉴权。

**语法**

<a id="code-block-74"></a>

```bash
bl finetune opd delete --job-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--job-id <id>` | string | 是 | OPD 任务 ID |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

> **警告**
>
> 该操作会永久删除任务记录，且无法撤销。

-   仅终态任务可以删除。

<a id="沙箱运行时管理"></a>

## 沙箱运行时管理

<a id="bl-finetune-runtime-prepare"></a>

### bl finetune runtime prepare

准备 RL/OPD 使用的托管 Python/SDK 运行时。无需鉴权。

**语法**

<a id="code-block-75"></a>

```bash
bl finetune runtime prepare [--manifest <path>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--manifest <path>` | string | 否 | 可选的运行时清单文件（默认使用内置已审核清单） |

**示例**：准备运行时

<a id="code-block-76"></a>

```bash
bl finetune runtime prepare
```

**示例**：使用自定义清单

<a id="code-block-77"></a>

```bash
bl finetune runtime prepare --manifest ./runtime-manifest.json
```

-   本地下载并校验运行时，不创建训练任务。设置 BAILIAN\_RL\_RUNTIME 指向本地 dashscope Python 目录可复用开发运行时。
-   CPython 下载在 GitHub 不可达时回退到内置 npmmirror 镜像；设置 BAILIAN\_RL\_PYTHON\_MIRROR 使用自定义镜像前缀。完整性始终通过已审核 SHA256 校验。
-   PyPI CDN 缓慢时，设置 BAILIAN\_RL\_PIP\_INDEX\_URL 使用稳定镜像（如 [https://pypi.tuna.tsinghua.edu.cn/simple/）；pip](https://pypi.tuna.tsinghua.edu.cn/simple/%EF%BC%89%EF%BC%9Bpip) 仍通过 `--require-hashes` 校验每个包哈希。
-   同时回收超过 24 小时的孤儿运行目录（崩溃残留）；正常调用结束时自动清理。

<a id="bl-finetune-runtime-doctor"></a>

### bl finetune runtime doctor

检查 RL 运行时和沙箱隔离状态（凭证拒绝、主目录重定向、SDK 导入）。无需鉴权。

**语法**

<a id="code-block-78"></a>

```bash
bl finetune runtime doctor
```

**示例**：检查运行时状态

<a id="code-block-79"></a>

```bash
bl finetune runtime doctor
```

-   只读自检，不创建云资源。运行时缺失时跳过必检项（不视为通过），命令返回非零退出码。
-   增强加固（内核网络强制、进程树、内存）不可用时降级提示，不导致整体检查失败。
-   宿主网络可达性（API / 运行时下载 / PyPI 主机）作为建议性检查：被阻断的主机降级提示（Agent 沙箱常阻断出站网络），不导致整体检查失败。

<a id="bl-finetune-runtime-clean"></a>

### bl finetune runtime clean

回收孤儿沙箱运行目录和已过时的运行时版本。无需鉴权。

**语法**

<a id="code-block-80"></a>

```bash
bl finetune runtime clean [--ttl-hours <hours>] [--dry-run]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--ttl-hours <hours>` | number | 否 | 孤儿运行目录的年龄阈值（默认 24 小时） |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

> **警告**
>
> 该操作永久删除孤儿运行目录和已过时运行时版本，且无法撤销。

**示例**：预览清理计划

<a id="code-block-81"></a>

```bash
bl finetune runtime clean --dry-run
```

**示例**：回收超过 48 小时的孤儿目录

<a id="code-block-82"></a>

```bash
bl finetune runtime clean --ttl-hours 48
```

-   正常调用结束时自动清理运行目录；仅崩溃残留（超过 TTL）保留在 runs/ 下。runtimes/rl/ 下的过时运行时版本被回收，仅保留当前已审核基线。
-   不触碰当前基线运行时、BAILIAN\_RL\_RUNTIME 开发目录或内容寻址下载缓存。仅本地操作：无需凭证，不涉及云资源。
