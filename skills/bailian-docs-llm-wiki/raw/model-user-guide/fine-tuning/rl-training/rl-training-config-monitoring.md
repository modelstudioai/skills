# 强化学习训练配置 — 提交与配置

本篇是 RL 训练**提交方式与参数配置**的覆盖，覆盖三种提交方式（run / YAML / submit\_job）、Runtime 资源配置、训练超参（必填 + 选填）、任务管理（SDK / CLI）以及配置类常见问题。

**与其他篇的边界：**

-   训练指标速查、13 组指标全集、问题排查（看到指标异常如何处理）、控制台 5 个页签、Tracing 装饰器、自定义指标 → 见基础 [强化学习的可观测配置与指标参考](raw/model-user-guide/fine-tuning/rl-training/observable-configuration-for-reinforcement-learning.md)

## 提交训练任务

RL 训练支持三种提交方式，推荐使用 **一步完成（run）**快速启动。三种方式灵活度递增：

**方式**

**说明**

**适用场景**

**分步操作**

分别注册函数、上传数据、提交任务

需要单独调试每个步骤

**一步完成（run）**

自动注册 + 上传 + 提交

快速启动训练

**YAML 配置**

从配置文件加载，支持运行时覆盖

多次实验、参数管理

**配置优先级**（后者覆盖前者）：

`__init__()` 初始化 < YAML 配置文件 < `run()` / `submit_job()` 运行时参数

### 推荐：一步完成（run）

自动完成函数注册、数据上传和任务提交，最快的上手方式：

```
from dashscope.finetune.reinforcement import (
    RolloutFunctionComponent, RewardFunctionComponent,
    FunctionComponentModel, FunctionComponentRuntime,
    TrainingDataset, ValidationDataset, DataSourceType,
)
from dashscope.finetune.agentic_rl import AgenticRL

# Rollout 与 Reward 共用的 runtime 配置（生产建议 memory_size >= 4096）
rollout_runtime = {
    "cpu": 2, "memory_size": 4096, "disk_size": 512, "concurrency": 30,
    "capacity": 30, "min_capacity": 30, "max_capacity": 60,
    "memory_scale_threshold": 0.6, "concurrency_scale_threshold": 0.6,
    "env": {},
}

client = AgenticRL()
result = await client.run(
    job_name="agentic-rl",                          # 实验标识
    # ---- 基础模型 ----
    model="qwen3.5-9b",                             # 待训练的基础模型

    # ---- 训练 / 验证数据 ----
    training_datasets=[TrainingDataset(
        data_source_type=DataSourceType.FILE_ID,
        file_name="./data/calc_train_min.jsonl",
    )],
    validation_datasets=[ValidationDataset(
        data_source_type=DataSourceType.FILE_ID,
        file_name="./data/calc_validation_min.jsonl",
    )],

    # ---- Rollout & Reward 函数 ----
    functions=[
        RolloutFunctionComponent(
            name="rollout-1",                      # 函数名称，用于日志和监控
            timeout=600,
            fcmodel=FunctionComponentModel(
                classpath="functions.rollout.rollout.CalcXRolloutProcessor"),  # 入口类（示例占位名，实际类名由您定义）
            runtime=FunctionComponentRuntime(**rollout_runtime)),
        RewardFunctionComponent(
            name="reward-1",                       # 函数名称
            weight=1.0,                            # 多 Reward 时的权重
            timeout=120,
            reward_metric_weight={                 # 多指标时各指标的权重
                "reward_metric_weightA": 0.3, "reward_metric_weightB": 0.7},
            fcmodel=FunctionComponentModel(
                classpath="functions.reward.reward.DemoRewardProcessor"),
            runtime=FunctionComponentRuntime(
                cpu=2, memory_size=4096, disk_size=512,
                concurrency=30, capacity=30,
                min_capacity=30, max_capacity=60,
                memory_scale_threshold=0.6,
                concurrency_scale_threshold=0.6)),
    ],

    # ---- 计算资源配置 ----
    resources={
        "charge_type": "mtu_postpaid",             # 按量付费
        "mtu_spec_code": "MTU4",                   # 资源规格
        "mtu_capacity": 24,                        # MTU 卡数
    },

    # ---- 超参数（必填字段完整列表见下方 §训练超参数 §代码示例） ----
    hyper_parameters={
        "algorithm": "gspo",
        "batch_size": 64,
        "eval_steps": 1,
        "kl_loss_coef": 0.002,
        "learning_rate": 2e-6,
        "lr_scheduler_type": "linear",
        "max_length": 8192,
        "n_epochs": 1,
        "n_rollouts": 8,
        "ppo_mini_batch_size": 8,
        "save_strategy": "epoch",
        # ... 完整字段同下方 §代码示例
    })
```

### YAML 配置

适合需要多次实验或管理多组参数的场景。先定义 YAML 配置文件，再加载执行：

```
## config.yaml
job_name: "agentic-rl"
workspace_dir: "./"
model: "qwen3.5-9b"                         # 基础模型
mode: "reinforcement"

datasets:
  - type: "training"
    data_source_type: "file_id"
    file_name: "./data/calc_train_min.jsonl"
  - type: "validation"
    data_source_type: "file_id"
    file_name: "./data/calc_validation_min.jsonl"

functions:
  - type: "rollout"
    name: "rollout-1"
    timeout: 600
    fcmodel:
      classpath: "functions.rollout.rollout.CalcXRolloutProcessor"  # 入口类（示例占位名，实际类名由您定义）
    runtime:
      cpu: 2
      memory_size: 4096                      # 内存（MB）
      disk_size: 512                         # 磁盘（MB）
      concurrency: 30                        # 单实例并发数
      capacity: 30                           # 初始实例数
      min_capacity: 30                       # 弹性伸缩下限
      max_capacity: 60                       # 弹性伸缩上限
      memory_scale_threshold: 0.6            # 内存使用率扩容阈值（0~1）
      concurrency_scale_threshold: 0.6       # 并发使用率扩容阈值（0~1）
      env: {}

  - type: "reward"
    name: "rewards-1"
    weight: 1.0
    timeout: 120
    reward_metric_weight:
      reward_metric_weightA: 0.3
      reward_metric_weightB: 0.7
    fcmodel:
      classpath: "functions.reward.reward.DemoRewardProcessor"
    runtime:
      cpu: 2
      memory_size: 4096
      disk_size: 512
      concurrency: 30
      capacity: 30
      min_capacity: 30
      max_capacity: 60
      memory_scale_threshold: 0.6
      concurrency_scale_threshold: 0.6
      env: {}

training:
  hyper_parameters:
    algorithm: "gspo"                          # 训练算法
    batch_size: 64                             # 每步训练样本数
    eval_steps: 1                             # 每隔多少步做一次评估
    kl_loss_coef: 0.002                        # KL 散度惩罚系数
    learning_rate: 2e-6                        # 学习率
    lr_scheduler_type: "linear"               # 学习率调度策略
    max_length: 8192                           # 最大序列长度
    n_epochs: 1                                # 训练轮次
    n_rollouts: 8                              # 每条 prompt 的采样数
    ppo_mini_batch_size: 8                     # PPO mini-batch 大小
    save_steps: 100                            # 每隔多少步保存 checkpoint
    save_strategy: "epoch"                    # 保存策略
    save_total_limit: 1                        # 最多保留 checkpoint 数
  resources:
    charge_type: "mtu_postpaid"               # 按量付费
    mtu_spec_code: "MTU4"                      # 资源规格
    mtu_capacity: 24                           # MTU 卡数
```

加载并执行：

```
client = AgenticRL()
## 加载 YAML 配置并初始化（job.yaml 为配置文件；name 标识本次实验）
client.init(config_path="job.yaml", name="agentic-rl-from-yaml")
## 也可把初始化后的配置导出为 YAML 复核（可选）
client.tuning.to_yaml(file_path="init.yaml")
## lazy_load=False 表示立即注册函数和上传数据
result = await client.run(lazy_load=False)

## 也可以在运行时覆盖部分参数（优先级高于 YAML 配置）
result = await client.run(hyper_parameters={"learning_rate": "2e-4"})
```

### 分步提交（submit\_job）

适用于需要单独调试每个步骤的场景。函数已注册、数据已上传后，直接引用 Entity ID 提交任务：

```
from dashscope.finetune.reinforcement import (
    AgenticRLFunctionComponent, FunctionType, FunctionComponentRuntime
)
from dashscope.finetune.agentic_rl import AgenticRL

client = AgenticRL()

## ---- 定义函数列表（使用已注册的 entity_id，无需再传 classpath） ----
functions = [
    AgenticRLFunctionComponent(
        type=FunctionType.ROLLOUT,
        entity_id="ro-xxxxx",                  # 注册时返回的 entity_id
        runtime=FunctionComponentRuntime(
            cpu=2, memory_size=4096, disk_size=512,
            concurrency=2, capacity=5)),       # submit_job 场景可按需调整并发
    AgenticRLFunctionComponent(
        type=FunctionType.REWARD,
        name="reward-1",
        weight=1.0,                            # 多 Reward 时的权重
        entity_id="rw-xxxxx",                  # 注册时返回的 entity_id
        runtime=FunctionComponentRuntime(
            cpu=2, memory_size=4096, disk_size=512,
            concurrency=10, capacity=8)),
]

## ---- 提交训练任务（数据使用已上传的 file_id） ----
result = await client.submit_job(
    model="qwen3.5-9b",                       # 基础模型
    training_file_ids=training_ids,            # 已上传数据的 file_id 列表
    validation_file_ids=validation_ids,
    functions=functions,
    resources={
        "charge_type": "mtu_postpaid",         # 按量付费
        "mtu_spec_code": "MTU4",               # 资源规格
        "mtu_capacity": 24,                    # MTU 卡数
    },
    hyper_parameters={
        "algorithm": "gspo",
        "batch_size": 64,
        "eval_steps": 1,
        "kl_loss_coef": 0.002,
        "learning_rate": 2e-6,
        "lr_scheduler_type": "linear",
        "max_length": 8192,
        "n_epochs": 1,
        "n_rollouts": 8,
        "ppo_mini_batch_size": 8,
        "save_strategy": "epoch",
        # ... 完整字段同上方 run() 示例
    })

print(f"Job ID: {result.output.job_id}")
```

### CLI 命令参考

以上三种方式均可通过 CLI 完成，常用命令如下：

**操作**

**命令**

**说明**

一步完成

`dashscope rl run --model "模型名" --rollout-classpaths "classpath" --reward-classpaths "classpath" --training-files "文件路径" --verbose`

自动注册 + 上传 + 提交

YAML 配置

`dashscope rl run -c job.yaml -o json`

从 YAML 加载配置

分步提交

`dashscope rl submit --model "模型名" --rollout-id "ro-xxx" --reward-ids '["rw-xxx"]' --training-file-ids "file-xxx"`

使用已注册的 Entity ID

上传数据

`dashscope rl upload_data --training-files "文件路径" --validation-files "文件路径" -o json`

仅上传数据，返回 File ID

## 训练参数配置

### Runtime 资源配置

为 Rollout 和 Reward 函数配置计算资源（`FunctionComponentRuntime`）：

**字段**

**类型**

**默认值**

**说明**

cpu

int

1

每实例 vCPU 数

memory\_size

int

10

内存（MB）

disk\_size

int

10

磁盘（MB）

concurrency

int

2

每实例最大并发请求数

capacity

int

10

初始实例数

min\_capacity

int

\-

最小实例数（弹性伸缩下限）

max\_capacity

int

50

最大实例数（弹性伸缩上限）

memory\_scale\_threshold

float

\-

内存使用率触发扩容的阈值（0~1）

concurrency\_scale\_threshold

float

\-

并发使用率触发扩容的阈值（0~1）

env

dict

{}

环境变量（如 ENABLE\_TRAJECTORY）

enable\_vpc\_config

bool

\-

VPC 网络开关。需开通请联系商务经理

**示例**：

**说明**：表中 `memory_size` 和 `disk_size` 的默认值（10 MB）为函数计算（FC）系统默认最小值。RL 训练实际运行时内存占用远高于此，**建议** `memory_size` >= 4096 MB，`disk_size` >= 512 MB。

```
from dashscope.finetune.reinforcement import FunctionComponentRuntime

rollout_runtime = FunctionComponentRuntime(
    cpu=2,
    memory_size=4096,
    disk_size=512,
    concurrency=30,
    capacity=30,
    min_capacity=30,
    max_capacity=60,
    memory_scale_threshold=0.6,
    concurrency_scale_threshold=0.6,
    env={"ENABLE_TRAJECTORY": "true"},
)
```

#### FC Runtime 调优深化

`FunctionComponentRuntime` 是 RL 训练吞吐和稳定性的重要环节。理解四角关系 + 弹性策略 + Rollout/Reward 差异化才能避免"启动异常"。

**四角关系：cpu × memory\_size × concurrency × capacity**

-   单实例吞吐 = `concurrency`（受 cpu / memory\_size 承载力约束）
-   集群吞吐 = `concurrency × capacity`（Rollout 阶段有效并发上限）
-   FC 系统默认（`memory_size=10MB / concurrency=2 / capacity=10`）**生产必须改**：`memory_size ≥ 4096` / `disk_size ≥ 512`
-   `capacity` 是初始实例数，与 `min_capacity / max_capacity` 形成弹性区间

**弹性策略：scale\_threshold 与 min/max\_capacity**

-   `memory_scale_threshold` / `concurrency_scale_threshold`（0~1）任一触达即扩容；推荐 **0.6~0.7**（过高来不及扩、过低浪费实例）
-   冷启动有秒级延迟，`min_capacity` 设常态负载下限避免首步等待
-   `max_capacity` 兜底防异常并发打爆账单（MTU 控训练资源、capacity 控函数资源、二者解耦）

**Rollout 与 Reward 的差异化配置**

函数类型

资源画像

推荐配置

Rollout

IO 密集（LLM/工具调用）

`concurrency` 拉高（30+），CPU 不必很高，`timeout` 600s 起

Reward

CPU/计算密集（评分/正则/模型评分）

`concurrency` 视评分耗时；调用 LLM 评分时按限速降并发；`timeout` 120s 起

多 Reward 函数分别配置 Runtime。各场景的特殊值（Agent / 代码生成等）见《强化学习训练最佳实践》各场景配方。

**并发估算公式**：

-   `目标并发 = batch_size × n_rollouts / 期望单 step 耗时(s)`
-   反推 `concurrency × capacity ≥ 目标并发 × 1.2 缓冲`

### 训练超参数

15 个**必填**超参 + 10 个**选填**（分布式资源，默认即可）。下方综合表把字段定义、取值范围、按模型规模 × 数据阶段的起点推荐合并为一张——直接照抄起点列即可"可直接启动训练"，再按 §调参决策表 迭代。

#### 必填参数综合表（字段 / 范围 / 起点推荐）

按 4 组分类：**算法**（algorithm, kl\_loss\_coef）/ **优化**（learning\_rate, lr\_scheduler\_type, lr\_warmup\_steps, n\_epochs）/ **数据吞吐**（batch\_size, n\_rollouts, ppo\_mini\_batch\_size, max\_length, max\_prompt\_length）/ **评估保存**（eval\_steps, save\_steps, save\_strategy, save\_total\_limit）。

参数

简介

取值范围

9b 快速验证

9b 正式训练

35B-A3B MoE

algorithm

RL 算法

gspo / grpo / dapo

gspo

gspo

**gspo**（强约束）

kl\_loss\_coef

KL 损失系数

\[0, 10\]

0.002

0.001

0.0005 ~ 0.001

learning\_rate

学习率

\[0, 1\]

2e-6

5e-6 ~ 7e-6

3e-6 ~ 5e-6

lr\_scheduler\_type

调度器

cosine / linear / constant

linear

cosine

cosine

lr\_warmup\_steps

学习率预热步数（-1 = 框架自动）

≥ -1

\-1

\-1

\-1

n\_epochs

训练轮次

\[1, 200\]

1

3 ~ 5

2 ~ 3

batch\_size

每步样本数

\[1, 100000\]

64

128 ~ 512

256 ~ 512

n\_rollouts

每 prompt 采样数

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

8192

8192 ~ 16384

max\_prompt\_length

prompt 最大 token

\[1, 131072\]

1024

2048

2048 ~ 4096

eval\_steps

评估间隔（建议总步数 / 10~20）

\[1, 999999\]

1

50

50

save\_steps

保存间隔（建议 eval\_steps × 2~3）

\[1, 999999\]

100

100

100

save\_strategy

保存策略

steps / epoch / no

epoch

epoch

epoch

save\_total\_limit

最多保留 ckpt

\[1, 200\]

1

3

2

**三大强耦合**（决定调参时哪几个必须一起动）：

-   `batch_size × n_rollouts = 每步实际生成样本数`
-   `ppo_mini_batch_size ≤ batch_size × n_rollouts`
-   `learning_rate × kl_loss_coef` 共同决定策略漂移速度

#### 选填参数（高级配置）

以下参数用于控制分布式训练资源配置，一般情况下使用默认值即可。

**参数**

**说明**

**默认值**

**取值范围**

expert\_model\_parallel\_size

专家模型并行大小（MoE 模型适用）。

1

\[1, 256\]

inference\_gpu\_memory\_utilization

Rollout 推理时的 GPU 显存利用率上限。

0.7

(0, 1\]

inference\_tensor\_parallel\_size

Rollout 推理时的张量并行数。

2

\[1, 256\]

n\_gpus\_rollout

Rollout 阶段使用的 GPU 数量。

8

\[1, 1024\]

n\_gpus\_training

训练阶段使用的 GPU 数量。

8

\[1, 1024\]

nnodes\_rollout

Rollout 阶段使用的节点数。

1

\[1, 256\]

nnodes\_training

训练阶段使用的节点数。

2

\[1, 256\]

pipeline\_model\_parallel\_size

流水线模型并行大小。

1

\[1, 256\]

sequence\_parallel\_size

序列并行大小。

1

\[1, 256\]

tensor\_model\_parallel\_size

张量模型并行大小。

1

\[1, 256\]

#### 代码示例

```
hyper_parameters = {
    # 必填参数
    "algorithm": "gspo",
    "batch_size": 64,
    "eval_steps": 1,
    "kl_loss_coef": 0.002,
    "learning_rate": 2e-6,
    "lr_scheduler_type": "linear",
    "lr_warmup_steps": -1,
    "n_epochs": 1,
    "n_rollouts": 8,
    "ppo_mini_batch_size": 8,
    "save_steps": 100,
    "save_strategy": "epoch",
    "save_total_limit": 1,
    "max_length": 8192,
    "max_prompt_length": 1024,
    # 选填参数（高级配置，一般无需修改）
    "n_gpus_rollout": 8,
    "n_gpus_training": 8,
    "nnodes_rollout": 1,
    "nnodes_training": 2,
    "inference_tensor_parallel_size": 2,
    "inference_gpu_memory_utilization": 0.7,
    "tensor_model_parallel_size": 1,
    "pipeline_model_parallel_size": 1,
    "sequence_parallel_size": 1,
    "expert_model_parallel_size": 1,
}
```

### 算法选型：GSPO / GRPO / DAPO

平台默认 GSPO；切换需带明确动机（复现 / 长 CoT / 收敛异常）。

-   **GRPO**（DeepSeekMath 2024）：**Token 级**重要性采样 + 组内相对优势，去 critic
-   **GSPO**（Qwen 2025，**平台默认**）：**Sequence 级**重要性采样，方差更低，MoE 训练稳定
-   **DAPO**：GRPO + Clip-Higher（0.2/0.28）+ Dynamic Sampling + Token-level Loss + Overlong Reward Shaping，长 CoT 推理优化

维度

GRPO

GSPO

DAPO

重要性采样粒度

Token 级

Sequence 级

Token 级 + Clip-Higher

KL 约束典型用法

β ≈ 0.04

β ≈ 0.001

β = 0

MoE 稳定性

易抖

原生稳定

需调

长 CoT 友好度

一般

好

**最好**

平台是否默认

否

**是**

否

推荐场景

短回复 / 入门

通用首选 / MoE

长链推理 / 数学 / 代码

**选型决策路径**：

-   默认 GSPO（平台默认对齐）；MoE（qwen3.5-35b-a3b）几乎只选 GSPO
-   切 GRPO：需 Token 级细粒度信号 / 与社区 GRPO 实现对齐
-   切 DAPO：响应长度 > 4K / Reward 全对全错塌缩 / 后期 entropy 崩

### 调参决策表（现象 → 调谁 → 怎么调）

指标异常时请对照本表选择首选调整项与调整幅度；P1~P9 完整排查详见《强化学习的可观测配置与指标参考》§问题排查决策树。

现象

首选调整

调整幅度

兜底

P1 不收敛

learning\_rate ↑

× 1.5~2

查 Reward 函数与数据

P2 震荡

learning\_rate ↓ + batch\_size ↑

lr×0.5；bs×2

n\_rollouts ↑

P3 KL 爆炸

kl\_loss\_coef ↑

× 5~10

降 lr

KL ≈ 0、不学

kl\_loss\_coef ↓

× 0.1

切 DAPO

P4 熵崩塌

切 DAPO

Clip-Higher

n\_rollouts ↑

Rollout 慢

n\_rollouts ↓ / max\_length 收紧

—

加并发（见高级并行）

OOM

ppo\_mini\_batch\_size ↓

× 0.5

max\_length ↓ / 调并行参数

P9 截断率高

max\_length ↑

\+ 2048

查 max\_prompt\_length

P6 过拟合

n\_epochs ↓

\-1~2

save\_strategy=steps 早停

### 调参操作建议

-   **一次只动一个变量**：同时调 `learning_rate` 和 `batch_size` 会无法归因
-   **跑满**`eval_steps × 3`**步再判断**：50 步看不出趋势，至少 150 步——RL 不是 SFT，曲线噪声大

调整优先级隐含在调参决策表的「首选调整」列；保留中间 Checkpoint 的具体设置见 §续训、Checkpoint 与渐进式训练。

### 超参设置反模式

反模式

后果

用 SFT 的 lr 起点（5e-5）跑 RL

训练易发散——RL 对 lr 比 SFT 敏感一个量级

`n_epochs` 设 10+ 期待"训透"

RL 不是 SFT；过多 epoch 触发 P6 验证集崩塌

`kl_loss_coef=0` 期待"自由探索"

模型快速漂移、输出乱码（除非 DAPO）

`n_rollouts=1`

失去组内相对优势，退化为普通 PG

`max_length=32K` 求保险

显存爆 + Rollout 变慢，按场景设到刚够即可

### 模型规模差异化配置：9B vs 35B-A3B MoE

配置维度

qwen3.5-9b (Dense)

qwen3.5-35b-a3b (MoE)

algorithm 强约束

任选

**GSPO**

learning\_rate

5e-6 ~ 7e-6

3e-6 ~ 5e-6

kl\_loss\_coef

0.001

0.0005 ~ 0.001

n\_rollouts

8

8 ~ 16

expert\_model\_parallel\_size

1

2 ~ 4

tensor\_model\_parallel\_size

1 ~ 2

2 ~ 4

inference\_tensor\_parallel\_size

2

4

**9B Dense 要点**：并行参数保持默认 1（不需 `expert_model_parallel_size`）；24 个 IV 型 MTU 是 Demo 最低。

**35B MoE 要点**：必须 GSPO（避免 Token 级算法在 MoE 路由下不稳定）；`expert_model_parallel_size` 从 2/4 起调；lr 降到 dense 的 1/2~2/3；`n_rollouts` 提到 8~16 平摊采样开销。

### 高级并行参数与显存估算

**并行参数家族**：

-   训练侧 `n_gpus_training` / `nnodes_training` / `tensor_model_parallel_size` / `pipeline_model_parallel_size` / `sequence_parallel_size` / `expert_model_parallel_size`
-   推理侧 `n_gpus_rollout` / `nnodes_rollout` / `inference_tensor_parallel_size` / `inference_gpu_memory_utilization`
-   约束：`n_gpus_training = tensor_mp × pipeline_mp × data_parallel`

**何时需要改默认值（4 类触发）**：

-   **显存 OOM** → `inference_gpu_memory_utilization` ↓ 0.1 + `tensor_mp` ↑
-   **Rollout 慢** → 加 `n_gpus_rollout` / `inference_tp`
-   **单步训练慢** → 加 `n_gpus_training`，长序列加 `sequence_parallel_size`
-   **MoE 模型** → 必调 `expert_model_parallel_size`

**显存估算说明**：

-   单 GPU 显存 ≈ 模型权重(bf16=2B/param) + 优化器(AdamW≈8B/param) + 激活值(随 bs × seq\_len) + KV cache
-   9B dense bf16 ≈ 90 GB / 实例需 TP 分摊
-   `inference_gpu_memory_utilization` 调低 = 推理侧让显存给训练侧
-   **不要**盲目加节点，先 TP 切分；常见反例：`tensor_mp` 调到 8 → 通讯吃掉收益、`inference_gpu_memory_utilization=0.95` → OOM 抖动、Dense 模型设 `expert_mp > 1` → 报错、`n_gpus_training < tensor_mp × pipeline_mp` → 配置非法

## 任务管理

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

`dashscope rl delete "ft-xxx"`

查看日志

`AgenticRL.logs(job_id="ft-xxx", lines=100)`

`dashscope rl logs "ft-xxx" --offset 1 --lines 100`

### 实验管理

#### YAML 多实验模式

-   `job_name` 标识实验、`tuned_model_name` 标识产出模型，每次实验改这两个即可隔离
-   YAML 集中管理 model/datasets/functions/runtime/hyper\_parameters 便于 Git 版本化
-   优先级 `__init__()` < YAML < `run()/submit_job()` 运行时参数——做对照实验只改最外层

#### 扫参 / CI 集成场景为何选 submit\_job

三种提交方式的场景决策：

-   **扫参 / CI**：函数已稳定只换超参 → `submit_job(entity_id=...)` 省去重复注册+上传（10x+ 提速）
-   **首次 / 调试 Reward**：用 `run()` 每次自动重注册防止代码不同步
-   Entity ID（`ro-` Rollout / `rw-` Reward）从首次注册返回值取，可入 CI 配置长期复用

#### CI 集成与命令对照

-   `dashscope rl run -c job.yaml -o json` 提交后解析 `job_id` 轮询 status，FAILED 直接拉 logs 告警；`-o json` 是 CI 解析必备

### 续训、Checkpoint 与渐进式训练

训练完成不等于训练成功——必须选对 Checkpoint 才发布。

#### Checkpoint 保留与选择

-   `save_strategy=steps` + `save_steps=100` + `save_total_limit=3`：最多保留 3 个、超出自动清理最旧
-   **选哪个 Checkpoint**：必须看 `validation/data/reward/mean@1` 选最佳点，**不一定是最后一个**
-   保留 3~5 个权衡空间与回滚需求

#### 基于已发布 Checkpoint 续训

-   续训 = 把上次产出的模型作为 `model` 入参再次提交，超参可微调（lr 通常调小）
-   适用：数据增量 / Reward 调整 / 长链路逐步收敛
-   注意：基础模型版本须一致，跨基座模型不可直接续训
-   在多阶段训练流水线中，每阶段产出可作为下一阶段的 `model` 入参逐级递进（CPT/SFT/DPO/RL 概念见《强化学习训练概述》）

## 常见问题

### 函数注册失败

-   检查 classpath 是否正确（格式：module.path.ClassName）
-   确认 requirements.txt 存在于项目根目录
-   确认所有依赖已列入 requirements.txt

### 任务提交失败

-   检查 Entity ID 和 File ID 是否有效
-   确认基座模型在当前地域可用
-   检查 reward\_runtimes 列表长度是否与 reward\_ids 一致

### 如何优化性能？

-   I/O 密集型任务使用 async def process
-   在 CPU/内存允许的范围内提高 concurrency
-   ENABLE\_TRAJECTORY 会增加存储和延迟，正式训练时按需开启

### Trace 看不到如何排查

排查步骤详见《强化学习的可观测配置与指标参考》§常见问题 → Trace 看不到如何排查（含 ARMS 授权、`ENABLE_TRAJECTORY` 开关、依赖检查的完整流程）。

### 如何查看训练日志？

-   SDK：`AgenticRL.logs(job_id="ft-xxx", lines=100)`
-   CLI：`dashscope rl logs "ft-xxx" --offset 1 --lines 100`
-   也可在百炼控制台的训练详情页查看

### 如何将 Checkpoint 发布为可用模型？

-   切换到百炼控制台训练详情页的产出页签，找到目标 Checkpoint，点击"发布"按钮
-   发布后的模型可通过模型名称在 API 中直接调用

### 训练 Reward 不涨如何排查

Reward 不涨属于「P1 不收敛」场景，按以下顺序排查：

1.  **看主信号**：`critic/rewards/mean` 长平台 + `actor/ppo_kl ≈ 0` + `actor/grad_norm` 极小 → P1
2.  **常见根因**（按概率）：lr 太小 / Reward 函数恒返回相同值 / 数据不足或重复
3.  **首选处置建议**：`learning_rate × 1.5~2`（参考调参决策表）
4.  **兜底**：本地 `test_functions` 复现 Reward 函数，确认评分有梯度（不是恒 0 或恒 1）

完整 P1~P9 问题排查决策树详见《强化学习的可观测配置与指标参考》§问题排查决策树。

## 后续步骤

-   回顾概述 → [强化学习](raw/model-user-guide/fine-tuning/rl-training/rl-training-overview.md)
-   了解函数开发 → [强化学习开发指南](raw/model-user-guide/fine-tuning/rl-training/rl-function-development-guide.md)
-   了解可观测性配置与轨迹查看 → [强化学习的可观测配置与指标参考](raw/model-user-guide/fine-tuning/rl-training/observable-configuration-for-reinforcement-learning.md)
