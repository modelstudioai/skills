# 在线策略蒸馏训练配置

百炼在线策略蒸馏训练配置：提交方式、教师模型配置、超参数、调参避坑、任务管理与常见问题

OPD 训练提交时需配置教师模型与超参。本文给出三种提交方式、教师模型配置、超参取值、调参决策、任务管理与常见问题排查。

## 提交训练任务

三种提交方式，灵活度递增。配置优先级：`__init__()`（SDK 初始化函数）默认值 < YAML < `run()` 运行时参数（后者覆盖前者）。传入 `teacher_model` 触发蒸馏。

### 推荐：一步完成（run）

通过 `AgenticRL().run(...)` 一步完成函数注册、数据上传与任务提交，多传 `teacher_model` 触发蒸馏。

```
from dashscope.finetune.agentic_rl import AgenticRL          # OPD 训练客户端
from dashscope.finetune.reinforcement import (               # 组件与数据类型
    RewardFunctionComponent, FunctionComponentModel,
    FunctionComponentRuntime, TrainingDataset,
    ValidationDataset, DataSourceType,
)

client = AgenticRL()                                        # 初始化训练客户端
result = await client.run(                                  # 异步提交：注册函数→上传数据→提交任务
    job_name="my-opd-job",
    model="qwen3.5-9b",                        # 学生模型（训练对象，被蒸馏的学生）
    teacher_model="qwen3.5-397b-a17b",         # 教师模型，OPD 唯一新增参数；传入即触发蒸馏
    training_datasets=[TrainingDataset(        # 训练集：FILE_ID 方式由 SDK 自动上传并换 file_id
        data_source_type=DataSourceType.FILE_ID,
        file_name="./data/train.jsonl")],
    validation_datasets=[ValidationDataset(    # 验证集：用于训练中评估，指标驱动调参
        data_source_type=DataSourceType.FILE_ID,
        file_name="./data/validation.jsonl")],
    functions=[
        # 不传 Rollout 组件 → Model OPD（原生 Rollout）；传 Rollout 组件 → Agentic OPD（自定义 Rollout，支持多轮/自定义交互）
        RewardFunctionComponent(               # 仅传 Reward 组件：在原生 Rollout + 教师蒸馏基础上叠加任务奖励
            name="reward-1", weight=1.0, timeout=120,   # weight=奖励权重，timeout=单次打分超时秒数
            fcmodel=FunctionComponentModel(
                zipdir=".",  # 工作区根目录（含 functions/），SDK 打包此目录上传至 FC
                classpath="functions.reward.reward.MyRewardProcessor"),  # 入口类全路径（示例类名，实际由您自定义）
            runtime=FunctionComponentRuntime(
                cpu=2, memory_size=4096, disk_size=512,            # 函数实例 CPU/内存/磁盘
                concurrency=20, capacity=10, min_capacity=10, max_capacity=30)),  # 并发与弹性容量
    ],
    # 纯蒸馏场景：改传 functions=None（而非空列表 []），不注册任何函数，reward 派生指标不上报
    hyper_parameters={                         # 训练超参，完整字段见下方 §训练超参数
        "algorithm": "gspo", "learning_rate": 1e-6, "lr_scheduler_type": "cosine",
        "n_epochs": 1, "n_rollouts": 8, "batch_size": 128,
    },
    resources={"charge_type": "mtu_postpaid", "mtu_spec_code": "MTU4", "mtu_capacity": 24},  # 计费资源：后付费/规格/容量
)
```

**说明**

`resources` 配置训练计费资源：`charge_type: mtu_postpaid` 表示按 MTU（百炼算力规格单位）后付费计费，`mtu_spec_code` 指定规格（如 `MTU4`），`mtu_capacity` 指定容量。

`functions` 参数决定运行模式（纯蒸馏 / Model OPD / Agentic OPD），与 `teacher_model` 无关——`teacher_model` 只负责触发蒸馏。模式选型详见[概述适用场景](opd-training-overview.md#opd-scenarios)。此处仅列 SDK 层的取值映射，区分依据是是否传入 Rollout 组件（决定用原生 Rollout 还是自定义 Rollout）：

-   **Model OPD**：不传 Rollout 组件 → 用原生 Rollout，含纯蒸馏（`functions=None`）与加 Reward（仅传 Reward 组件叠加任务奖励）两档
-   **Agentic OPD（无 Reward）**：仅传 Rollout 组件 → 自定义 Rollout（支持多轮对话、自定义交互、结构化 tool call）+ 教师蒸馏
-   **Agentic OPD（含 Reward）**：同时传 Rollout + Reward → 自定义 Rollout + 教师蒸馏 + Reward
-   传 `None`（而非空列表 `[]`）→ 纯蒸馏，reward 派生指标不上报，蒸馏损失类指标与 teacher 健康类指标仍正常上报

### YAML 配置

适合多次实验或管理多组参数，通过 `teacher_model` 字段指定教师模型。

```
## config.yaml（简化示意）
name: "my-opd-job"
model:
  name: "qwen3.5-9b"                           # 学生模型（训练对象）
teacher_model: "qwen3.5-397b-a17b"             # 教师模型（OPD 新增），传入即触发蒸馏

datasets:
  - type: "training"                           # 训练集
    data_source_type: "file_id"                # file_id 方式：SDK 自动上传并换 file_id
    file_name: "./data/train.jsonl"
  - type: "validation"                         # 验证集，训练中评估用
    data_source_type: "file_id"
    file_name: "./data/validation.jsonl"

functions:                                     # 不传 Rollout 组件即 Model OPD；纯蒸馏写 functions: null
  - type: "reward"                             # 仅传 Reward：原生 Rollout + 教师蒸馏 + 任务奖励
    name: "reward-1"
    weight: 1.0                                # 奖励权重，多 reward 时加权求和
    timeout: 120                               # 单次打分超时秒数
    fcmodel:
      classpath: "functions.reward.reward.MyRewardProcessor"  # 入口类全路径（示例类名，实际由您自定义）
    runtime:
      cpu: 2                                   # 函数实例 CPU 核数
      memory_size: 4096                        # 内存 MB
      concurrency: 20                          # 单实例并发打分数
      capacity: 10                             # 当前实例数
      min_capacity: 10                         # 最小实例数（保底）
      max_capacity: 30                         # 最大实例数（弹性上限）

training:
  type: "pg_opd"                               # OPD 训练类型；传 teacher_model 后自动置此值，无需手填
  hyper_parameters:
    algorithm: "gspo"                          # 训练算法
    learning_rate: 1e-6                         # 学习率，OPD 起点低于 SFT
    lr_scheduler_type: "cosine"                 # 学习率调度器
    n_epochs: 1                                # 训练轮次
    # ... 完整字段见下方 §训练超参数
  resources:
    charge_type: "mtu_postpaid"                # 后付费计费
    mtu_spec_code: "MTU4"                       # 算力规格
    mtu_capacity: 24                           # 容量
```

加载并执行：

```
client = AgenticRL()                                            # 初始化训练客户端
client.init(config_path="config.yaml", name="my-opd-from-yaml") # 加载 YAML 配置，name 覆盖 YAML 中的 job_name
result = await client.run()                                     # 异步提交任务；run() 参数覆盖 init() 与 YAML 默认值
```

### CLI 命令

通过 `dashscope rl run` 提交，`--teacher-model` 覆盖 YAML 中的 `teacher_model`。

```
dashscope rl run -c config.yaml --teacher-model qwen3.5-397b-a17b
# -c 指定 YAML 配置文件路径
# --teacher-model 指定教师模型，覆盖 YAML 中的 teacher_model 字段；传入即启用 OPD
```

`--teacher-model` help 文案（原文）：Enable OPD with this teacher model (overrides YAML); Rollout and Reward are optional. 含义：启用 OPD 并指定教师模型（覆盖 YAML）；Rollout 与 Reward 可选。

常用 CLI 命令：

**操作**

**命令**

**说明**

提交训练

`dashscope rl run -c config.yaml --teacher-model "教师模型" [--verbose|-o json]`

读 YAML 配置提交；--verbose 人类可读，-o json 机器可读

上传数据

`dashscope rl upload_data --training-files "文件路径" --validation-files "文件路径" -o json`

仅上传数据，返回 File ID

示例提交脚本 submit\_job.py（参考实现，classpath 为示例类名）

示例目录附带的 `submit_job.py` 把超参挂成命令行参数，可按需调整。`--no-reward` 是示例侧便利开关（非 SDK 参数），等价于 SDK 层 `functions=None`。`zipdir` 推荐显式指定以避免入口类定位失败。关键片段如下：

```
import asyncio
from dashscope.finetune.agentic_rl import AgenticRL          # OPD 训练客户端
from dashscope.finetune.reinforcement import (                # 组件与数据类型
    RewardFunctionComponent, FunctionComponentModel,
    FunctionComponentRuntime, TrainingDataset,
    ValidationDataset, DataSourceType,
)

async def submit(args):
    client = AgenticRL()                                    # 初始化训练客户端
    # 纯蒸馏时传 None 而非空列表：None 使控制面（调度层）执行原生 Rollout，[] 不一定等价
    # --no-reward 是示例侧便利开关（非 SDK 参数），等价于 SDK 层 functions=None
    function_components = (
        None if args.no_reward                              # 纯蒸馏：不注册任何函数
        else [RewardFunctionComponent(                      # 加 Reward：原生 Rollout + 教师蒸馏 + 任务奖励
            name="reward-1", weight=1.0, timeout=120,       # weight=奖励权重，timeout=单次打分超时秒数
            fcmodel=FunctionComponentModel(
                zipdir=str(args.workspace_dir.resolve()),   # 工作区根目录，显式指定避免入口类定位失败
                classpath="functions.reward.reward.MyRewardProcessor"),  # 入口类全路径（示例类名，实际由您自定义）
            runtime=FunctionComponentRuntime(**build_runtime()))]        # 并发与弹性容量由 build_runtime() 构造
    )
    result = await client.run(                              # 异步提交：注册→上传→提交
        job_name=args.job_name,
        model=args.student_model,          # 学生模型（训练对象）
        teacher_model=args.teacher_model,  # 教师模型，传入即触发蒸馏
        training_datasets=[...],           # 训练集（示例省略构造）
        validation_datasets=[...],         # 验证集（示例省略构造）
        functions=function_components,     # None=纯蒸馏；[Reward...]=Model OPD；含 Rollout=Agentic OPD
        hyper_parameters={...},            # 训练超参（示例省略，见下方 §训练超参数）
    )
    return result.output.job_id            # 返回 job_id，供后续查询/取消/日志使用
```

## 配置教师模型

`teacher_model` 是触发蒸馏的提交参数。传入即触发蒸馏，不传则不触发。传入后 SDK 内部字段 `training_type` 自动置为 `pg_opd`（策略蒸馏训练类型标识，对应 YAML 中的 `training.type`），无需也不能手动指定训练类型。

**行为结论**：

-   传 `teacher_model` 即强制 `training_type=pg_opd`，无需也不能手动指定训练类型
-   YAML 中写 `training.type: pg_opd` 但未传 `teacher_model` 时，控制面报错 `error 3006`（教师模型缺失）
-   `hyper_parameters` 中未声明的键不会被识别，不会报错也不会生效

### 三条硬约束

教师模型配置须同时满足以下三条约束，任一不满足都会导致蒸馏失效或提交被拒。

**约束**

**说明**

**违反时的表现**

必须是百炼模型 ID

仅接受百炼注册的模型 ID，非 HuggingFace 仓库名或权重路径

`400 InvalidParameter: teacher_model must be a valid model ID`

师生同 model family

教师与学生模型的 tokenizer 必须可对齐（tokenizer 对齐：词表一致，token id 一一对应，如同属 Qwen3.5 系列）

词表不对齐时 token 级分布无法逐位置对应，蒸馏信号失效

教师模型能力强于学生模型

蒸馏是将大模型能力迁移至小模型

教师不强于学生时无蒸馏增益

## 训练超参数

`hyper_parameters` 字段名与取值范围一致，按 4 组分类：**算法**（algorithm；kl\_loss\_coef OPD 未启用）/ **优化**（learning\_rate, lr\_scheduler\_type, lr\_warmup\_steps, n\_epochs）/ **数据吞吐**（batch\_size, n\_rollouts, ppo\_mini\_batch\_size, max\_length, max\_prompt\_length）/ **评估保存**（eval\_steps, save\_steps, save\_strategy, save\_total\_limit）。

### 必填参数综合表

下方综合表合并字段定义、取值范围与按模型规模 × 数据阶段的起点推荐；直接采用起点列即可启动训练，再按 §调参决策表迭代。

**说明**OPD 学习率起点较低（1e-6）：蒸馏是微调学生模型已有能力而非重建，学习率过大易先破坏输出格式。

参数

简介

取值范围

小模型快速验证

正式训练

大模型

algorithm

训练算法

gspo

gspo

gspo

gspo

kl\_loss\_coef

KL 损失系数（OPD 未启用）

\[0, 10\]

—

—

—

learning\_rate

学习率

\[0, 1\]

1e-6

3e-6 ~ 5e-6

2e-6 ~ 3e-6

lr\_scheduler\_type

调度器

cosine / constant

cosine

cosine

cosine

lr\_warmup\_steps

预热步数（-1 = 自动；小数据冒烟设 0 避免超过总步数）

\>= -1

0

\-1

\-1

n\_epochs

训练轮次

\[1, 200\]

1

2 ~ 3

1 ~ 2

batch\_size

每步样本数

\[1, 100000\]

128

128 ~ 256

256 ~ 512

n\_rollouts

每条 prompt 采样数

\[1, 1024\]

8

8

8 ~ 16

ppo\_mini\_batch\_size

PPO mini-batch

\[1, 100000\]

8

16 ~ 32

32 ~ 64

max\_length

prompt + resp 最大 token

\[1, 131072\]

8192

8192 ~ 16384

8192 ~ 16384

max\_prompt\_length

prompt 最大 token

\[1, 131072\]

2048

2048 ~ 4096

2048 ~ 4096

eval\_steps

评估间隔（建议总步数 / 10~20）

\[1, 999999\]

1

总步数 / 10~20

总步数 / 10~20

save\_steps

保存间隔（建议 eval\_steps × 2~3）

\[1, 999999\]

1

eval\_steps × 2~3

eval\_steps × 2~3

save\_strategy

保存策略

steps / epoch

steps

steps

steps

save\_total\_limit

最多保留 ckpt

\[1, 200\]

2

3

2 ~ 3

**模型规模分界**：学生模型参数量 ≤14B 算小模型，≥30B 算大模型（如 Qwen3.5-9b 属小，397b-A17b 属大）。表中"小模型快速验证"列适用于链路冒烟与小规模训练，"大模型"列适用于正式大规模训练；介于两者之间取两列并集后按实际收敛情况微调。

**三个必须一起调整的参数关系**（决定调参时哪几个必须联动）：

-   **样本数**：`batch_size × n_rollouts = 每步实际生成样本数`
-   **mini-batch 上限**：`ppo_mini_batch_size ≤ batch_size × n_rollouts`
-   `learning_rate` 决定蒸馏收敛速度——OPD 无 `kl_loss_coef` 约束模型偏离初始策略（防止输出风格漂移），学习率是唯一控制收敛速度的参数

### 选填参数

以下参数用于控制分布式训练资源配置，一般使用默认值即可。表中默认值为未传时的取值，实际取值以提交时传入为准。

**参数**

**说明**

**默认值**

**取值范围**

n\_gpus\_rollout

Rollout 阶段 GPU 数量

8

\[1, 1024\]

n\_gpus\_training

训练阶段 GPU 数量

8

\[1, 1024\]

nnodes\_rollout

Rollout 阶段节点数

1

\[1, 256\]

nnodes\_training

训练阶段节点数

2

\[1, 256\]

### 教师模型部署参数与不启用项

**以下参数需特别注意，理解后可避免误调不会生效的参数。**

-   **algorithm**：默认 `gspo`（GSPO，分组相对策略优化）。启用 reward 时决定策略优化的实现方式；纯蒸馏（不注册 reward）时不参与损失计算，一般无需改动
-   **教师模型的部署资源**：可显式配置 `opd_teacher_*` 参数，不传取默认值。示例默认值如下：

教师模型经 vLLM（百炼推理引擎）部署，KV cache（推理显存中缓存已计算 token 的机制）容量决定打分吞吐。按教师模型规模与序列长度调整：

-   **序列长**：调高 `opd_teacher_max_model_len`（伴随 `opd_teacher_max_num_batched_tokens`↑）
-   **显存紧**：调低 `opd_teacher_gpu_memory_utilization`

其余参数一般保持默认。

**参数**

**demo 默认值**

opd\_teacher\_nnodes

1

opd\_teacher\_n\_gpus\_per\_node

8

opd\_teacher\_infer\_tp

8

opd\_teacher\_gpu\_memory\_utilization

0.75

opd\_teacher\_max\_model\_len

34816

opd\_teacher\_max\_num\_batched\_tokens

4096

opd\_teacher\_max\_num\_seqs

2

opd\_teacher\_num\_replicas

1

-   **kl\_loss\_coef**：OPD 不消费该参数——蒸馏不通过 KL 散度（衡量两个概率分布差异的指标）约束策略偏离，收敛速度由 `learning_rate` 单独控制。必填表中标"—"即表示 OPD 不消费。保留默认或留空均可，无需清零或删除。

## 调参与避坑

### 调参决策表

指标异常时对照本表选择首选调整项与幅度；完整指标含义与排查决策树见[在线策略蒸馏可观测配置](opd-observable-config.md)。

现象

首选调整

调整幅度

兜底

distillation/loss 不降

learning\_rate ↑

× 1.5~2

查 valid\_token\_rate + Reward 函数

distillation/loss 爆炸

learning\_rate ↓

× 0.5

查教师模型健康指标

valid\_token\_rate < 1

提工单（教师模型侧）

—

确认师生同 model family

过拟合（验证集不再提升）

n\_epochs ↓

\-1~2

save\_strategy=steps 早停

Reward 信号不生效（success\_rate=0）

查 FC 调用与 Reward 函数

—

本地 test\_functions 复现评分

Rollout 慢

n\_rollouts ↓ / max\_length 收紧

—

加并发（FunctionComponentRuntime.concurrency/capacity，见开发篇）

OOM

ppo\_mini\_batch\_size ↓

× 0.5

max\_length ↓ / 调并行参数

截断率高

max\_length ↑

\+ 2048

查 max\_prompt\_length

### 调参操作建议

-   先看 `valid_token_rate`：该指标小于 1 时教师模型打分存在缺失，其余指标解释力下降，应先排查再调超参
-   一次只动一个变量：同时调 `learning_rate` 和 `batch_size` 会无法归因
-   训练 `eval_steps × 3` 步再判断趋势：蒸馏曲线噪声较小但短周期难以判断趋势，至少 3 个评估间隔再判断走向

### 反模式

以下配置在实践中已证实会导致训练失败或资源浪费，应避免。

反模式

后果

用 SFT 的 lr 起点（5e-5）执行 OPD

训练发散——蒸馏对 lr 敏感，比 SFT 低一个量级

n\_epochs 设 10+ 期待"训透"

加深对教师模型风格的过拟合，验证集崩塌

用 HuggingFace 仓库名当 teacher\_model

400 InvalidParameter: teacher\_model must be a valid model ID

教师模型能力弱于学生模型

无蒸馏增益，白费算力

max\_length=32K 求保险

teacher vLLM 按 opd\_teacher\_max\_model\_len 预留 KV cache、max\_num\_seqs 被压低（demo 仅 2），打分吞吐下降；短序列不会显存爆。按实际最长序列 ×1.2~1.5 设定，32K 仅在序列真有 32K 时才需要

传空列表 \[\] 当纯蒸馏

控制面对 \[\] 与 None 处理未必相同，可能无法执行原生 rollout；纯蒸馏须传 None

## 任务管理

本节给出训练任务的查询、取消、删除与查看日志命令，以及实验管理与续训方法。

### SDK / CLI 命令对照

任务管理命令（查询、取消、删除、日志）如下，提交时多传 `teacher_model`：

**操作**

**SDK**

**CLI**

查询状态

`AgenticRL.get(job_id="ft-xxx")`

`dashscope rl get "ft-xxx" -o json`

列举任务

`AgenticRL.list()`

`dashscope rl list --page 1 --size 10 -o json`

取消任务

`AgenticRL.cancel(job_id="ft-xxx")`

`dashscope rl cancel "ft-xxx"`

删除任务

`AgenticRL.delete(job_id="ft-xxx")`

暂不支持 CLI，用 SDK

查看日志

`AgenticRL.logs(job_id="ft-xxx", lines=100)`

`dashscope rl logs "ft-xxx" --offset 1 --lines 100`

### 实验管理

-   YAML 多实验模式：`job_name` 标识实验、`finetuned_output` 标识产出模型，每次实验改这两个即可隔离；YAML 集中管理配置便于 Git 版本化
-   配置优先级：`__init__()` < YAML < `run()` 运行时参数——做对照实验只改最外层
-   扫参 / CI 场景（进阶用法，一般用户可跳过）：函数已稳定只换超参时，可在 `functions` 组件级传入 `entity_id`（如 `RewardFunctionComponent(..., entity_id="rw-xxx")`）复用已注册组件，省去重复注册与上传。Entity ID（`ro-` 表示 Rollout、`rw-` 表示 Reward）从首次注册返回值中取，字段名 `entity_id`，可入 CI 配置长期复用：

```
result = await client.run(...)                    # 首次提交：注册函数组件并上传代码/数据
entity_id = result.output.entity_id              # 从首次注册返回值取 entity_id，ro- 表示 Rollout、rw- 表示 Reward
# 后续扫参/CI 只换超参时，在组件级传 entity_id="rw-xxx" 复用已注册组件，省去重复注册与上传
```

### 续训与 Checkpoint

**Checkpoint 保留与选择**：

-   `save_strategy=steps` + `save_steps=100` + `save_total_limit=3`：最多保留 3 个，超出自动清理最旧
-   选哪个 Checkpoint：启用 reward 时看 `validation/data/reward/mean@1` 选最佳点（纯蒸馏不启用 reward 时该指标不上报，依据 `actor/distillation/loss` 趋稳点选择），不一定是最后一个
-   保留 3~5 个权衡空间与回滚需求

**基于已发布 Checkpoint 续训**：

-   续训 = 把上次产出的模型作为 `model` 入参再次提交，超参可微调（lr 通常调小）
-   适用：数据增量 / Reward 调整 / 长链路逐步收敛
-   注意：基础模型版本须一致，跨基座模型不可直接续训
-   多阶段训练流水线中，每阶段产出可作为下一阶段的 `model` 入参逐级递进

## 后续步骤

-   回顾原理与场景选型 → [在线策略蒸馏训练概述](opd-training-overview.md)
-   Model OPD 开发（纯蒸馏/Reward） → [Model OPD 开发](opd-model-development-guide.md)
-   Agentic OPD 开发（自定义 Rollout） → [Agentic OPD 开发](opd-agentic-development-guide.md)
-   训练指标速查、效果判断与问题排查 → [在线策略蒸馏可观测配置](opd-observable-config.md)

## 常见问题

teacher\_model 报错 400 InvalidParameter

填了 HuggingFace 仓库名或权重路径。改用百炼模型 ID（如 `qwen3.5-397b-a17b`），确保已在百炼开通该模型。

SDK 版本与环境变量

安装以示例目录附带的 wheel 为准（当前 1.27.5），不依赖 PyPI 版本号判断是否支持 OPD。

旧版 SDK 有两个拦截点（按出现时机区分）：

-   提交前拦截：示例 `submit_job.py` 在调用 `AgenticRL.run(...)` 前校验其签名是否接受 `teacher_model` 参数——旧版 SDK 签名不含该参数，提交前即报错
-   提交时拦截（旧版 SDK 排查）：更早版本会把 `training_type` 写成 `pg-opd`（连字符），而控制面只接受 `pg_opd`（下划线），提交时被拒收

`FC_LAYER_USED` 仅识别 `true`/`1`/`yes`，`on` 会被当作 `false`。建议只写小写 `true` / `false`，避免 `on` 等取值歧义。

端点与 URL 配置

两套端点：`DASHSCOPE_HTTP_BASE_URL`（控制面，`/api/v1` 提交训练）与 `MODEL_BASE_URL`（推理，`/compatible-mode/v1` 离线评测）是两套端点，API Key 必须与对应端点匹配，不匹配会返回 `InvalidApiKey` / HTTP 401。

`DASHSCOPE_HTTP_BASE_URL` 末尾若有多余空格或 `/`，会拼出非法 URL，请确保末尾干净。
