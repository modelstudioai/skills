# 强化学习训练配置 — 提交与配置

本篇是 RL 训练**提交方式与参数配置**的覆盖，覆盖三种提交方式（run / YAML / submit\_job）、Runtime 资源配置、训练超参全量分组表、任务管理（SDK / CLI）以及配置类常见问题。

**与其他篇的边界：**

-   训练指标速查、7 组指标全集、问题排查（看到指标异常如何处理）、控制台 5 个页签、Tracing 装饰器、自定义指标 → 见基础 [强化学习的可观测配置与指标参考](observable-configuration-for-reinforcement-learning.md)

<a id="提交训练任务"></a>

<a id="fvj2mhbpok02o"></a>

## 提交训练任务

> **说明**
>
> 首次提交或更换自研函数/数据后，建议先完成[强化学习提交前自检](rl-pre-submission-checklist.md)的分层检查（免费本地校验 → 远程函数测试 → 链路冒烟），再正式提交。

RL 训练支持三种提交方式，推荐使用 **一步完成（run）**快速启动。三种方式灵活度递增：

| 方式 | 说明 | 适用场景 |
| --- | --- | --- |
| **分步操作** | 分别注册函数、上传数据、提交任务 | 需要单独调试每个步骤 |
| **一步完成（run）** | 自动注册 + 上传 + 提交 | 快速启动训练 |
| **YAML 配置** | 从配置文件加载，支持运行时覆盖 | 多次实验、参数管理 |

**配置优先级**（后者覆盖前者）：

`__init__()` 初始化 < YAML 配置文件 < `run()` / `submit_job()` 运行时参数

<a id="推荐-一步完成-run"></a>

<a id="rceg51vlo2i2a"></a>

### 推荐：一步完成（run）

自动完成函数注册、数据上传和任务提交，最快的上手方式（`run()` 为异步方法，完整脚本须包在 `async def main()` 中并用 `asyncio.run(main())` 执行，可运行完整示例见概述篇）：

<a id="code-block"></a>

```text
from dashscope.finetune.reinforcement import (
    RolloutFunctionComponent, RewardFunctionComponent,
    FunctionComponentModel, FunctionComponentRuntime,
    TrainingDataset, ValidationDataset, DataSourceType,
)
from dashscope.finetune.agentic_rl import AgenticRL

# Rollout 与 Reward 共用的 runtime 配置（生产须 memory_size >= 4096）
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
        "charge_type": "mtu_postpaid",             # 计费方式：后付费填 mtu_postpaid；预付费填 mtu_prepaid 并提供 instance_id（联系商务经理获取）
        "mtu_spec_code": "MTU4",                   # 训练单元规格
        "mtu_capacity": 24,                        # 本次任务占用的 MTU 数量，不必用满已购容量
    },

    # ---- 超参数（低成本试跑起点；未传参数由服务端自动补全，全量表见下方 §训练超参数） ----
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
        "save_strategy": "steps",
        # ... 参数含义与取值范围见下方 §训练超参数
    })
```

<a id="yaml-配置"></a>

<a id="owgwlslyqboyz"></a>

### YAML 配置

适合需要多次实验或管理多组参数的场景。先定义 YAML 配置文件，再加载执行：

<a id="code-block-2"></a>

```text
## job.yaml
name: agentic-rl-from-yaml                    # 实验标识
model:
  name: qwen3.5-9b                            # 基础模型

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
      zipdir: "./"                            # 打包根目录（函数代码所在目录）
      classpath: "functions.rollout.rollout.CalcXRolloutProcessor"  # 入口类（示例占位名，实际类名由您定义）
      requirements_path: "./requirements.txt" # 依赖清单
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
    name: "reward-1"
    weight: 1.0
    timeout: 120
    fcmodel:
      zipdir: "./"
      classpath: "functions.reward.reward.DemoRewardProcessor"
      requirements_path: "./requirements.txt"
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
  type: "reinforcement"
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
    save_strategy: "steps"                   # 保存策略（按步数保存）
    save_total_limit: 1                        # 最多保留 checkpoint 数
  resources:
    charge_type: "mtu_postpaid"               # 计费方式：后付费填 mtu_postpaid；预付费填 mtu_prepaid 并提供 instance_id（联系商务经理获取）
    mtu_spec_code: "MTU4"                      # 训练单元规格
    mtu_capacity: 24                           # 本次任务占用的 MTU 数量，不必用满已购容量
```

加载并执行：

<a id="code-block-3"></a>

```text
client = AgenticRL()
## 加载 YAML 配置并初始化（job.yaml 为配置文件；name 标识本次实验）
client.init(config_path="job.yaml", name="agentic-rl-from-yaml")
## 也可把初始化后的配置导出为 YAML 复核（可选）
client.tuning.to_yaml(file_path="init.yaml")
## run() 为异步方法：完整脚本须包在 async main() 中执行（可运行完整示例见概述篇）
result = await client.run()

## 也可以在运行时覆盖部分参数（优先级高于 YAML 配置；调整幅度参考调参决策表）
result = await client.run(hyper_parameters={"learning_rate": 4e-6})
```

<a id="分步提交-submit-job"></a>

<a id="my257615kf2ow"></a>

### 分步提交（submit\_job）

适用于需要单独调试每个步骤的场景。函数已注册、数据已上传后，直接引用 Entity ID 提交任务（函数注册的完整流程见[强化学习提交前自检](rl-pre-submission-checklist.md)与[强化学习开发指南](rl-function-development-guide.md)）：

<a id="code-block-4"></a>

```text
from dashscope.finetune.reinforcement import (
    AgenticRLFunctionComponent, FunctionType, FunctionComponentRuntime,
    Dataset, DatasetsType, DataSourceType,
)
from dashscope.finetune.agentic_rl import AgenticRL

client = AgenticRL()

## ---- 上传训练/验证数据（返回 file_id 列表） ----
training_ids, validation_ids = await client.upload_datasets(
    training_files=["./data/calc_train_min.jsonl"],
    validation_files=["./data/calc_validation_min.jsonl"])

## ---- 定义函数列表（以 entity_id 引用已注册的函数，无需再传 classpath） ----
## 注意：分步提交的函数组件为 AgenticRLFunctionComponent；
## 多 Reward 权重（weight）在 run() 方式的 RewardFunctionComponent 上配置（见上方示例）
functions = [
    AgenticRLFunctionComponent(
        type=FunctionType.ROLLOUT,
        entity_id="ro-xxxxx",                  # 注册时返回的 entity_id
        runtime=FunctionComponentRuntime(
            cpu=2, memory_size=4096, disk_size=512,
            concurrency=2, capacity=5)),       # 演示用最小配置，生产参考下文 FC 调优
    AgenticRLFunctionComponent(
        type=FunctionType.REWARD,
        name="reward-1",
        entity_id="rw-xxxxx",                  # 注册时返回的 entity_id
        runtime=FunctionComponentRuntime(
            cpu=2, memory_size=4096, disk_size=512,
            concurrency=10, capacity=8)),
]

## ---- 提交训练任务（submit_job 为同步调用；数据以 datasets 引用已上传的 file_id） ----
result = client.submit_job(
    model="qwen3.5-9b",                       # 基础模型
    datasets=[
        Dataset(type=DatasetsType.TRAINING,
                data_source_type=DataSourceType.FILE_ID,
                file_id=training_ids[0]),      # 已上传数据返回的 file_id
        Dataset(type=DatasetsType.VALIDATION,
                data_source_type=DataSourceType.FILE_ID,
                file_id=validation_ids[0]),
    ],
    functions=functions,
    resources={
        "charge_type": "mtu_postpaid",         # 计费方式：后付费填 mtu_postpaid；预付费填 mtu_prepaid 并提供 instance_id（联系商务经理获取）
        "mtu_spec_code": "MTU4",               # 训练单元规格
        "mtu_capacity": 24,                    # 本次任务占用的 MTU 数量，不必用满已购容量
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
        "save_strategy": "steps",
        # ... 字段同上方 run() 示例
    })

print(f"Job ID: {result.output.job_id}")
```

<a id="cli-命令参考"></a>

<a id="1st10lerw7r7n"></a>

### CLI 命令参考

以上三种方式均可通过 CLI 完成，常用命令如下：

> **说明**
>
> 本页命令以 `dashscope` 前缀示例（适用于 dashscope 2.0.x）。安装 dashscope 2.1.0 及以上版本时，本文全部 CLI 命令加 `dashscope1` 前缀使用（如 `dashscope1 rl get "ft-xxx"`），参数不变。表内命令为最小参数示例；超参、资源配置等完整参数建议经 `job.yaml`（`dashscope rl run -c job.yaml`）传递。

| 操作 | 命令 | 说明 |
| --- | --- | --- |
| 一步完成 | `dashscope rl run --model "模型名" --rollout-classpaths "classpath" --reward-classpaths "classpath" --training-files "文件路径" --verbose` | 自动注册 + 上传 + 提交 |
| YAML 配置 | `dashscope rl run -c job.yaml -o json` | 从 YAML 加载配置 |
| 分步提交 | `dashscope rl submit --model "模型名" --rollout-id "ro-xxx" --reward-ids '["rw-xxx"]' --training-file-ids "file-xxx"` | 使用已注册的 Entity ID |
| 上传数据 | `dashscope rl upload_data --training-files "文件路径" --validation-files "文件路径" -o json` | 仅上传数据，返回 File ID |

<a id="训练参数配置"></a>

<a id="yq27okdqt7r0y"></a>

## 训练参数配置

<a id="runtime-资源配置"></a>

<a id="15b4d8fbwsxob"></a>

### Runtime 资源配置

为 Rollout 和 Reward 函数配置计算资源（`FunctionComponentRuntime`）：

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| cpu | int | 1 | 每实例 vCPU 数 |
| memory\_size | int | 10 | 内存（MB） |
| disk\_size | int | 10 | 磁盘（MB） |
| concurrency | int | 2 | 每实例最大并发请求数 |
| capacity | int | 10 | 初始实例数 |
| min\_capacity | int | \- | 最小实例数（弹性伸缩下限） |
| max\_capacity | int | 50 | 最大实例数（弹性伸缩上限） |
| memory\_scale\_threshold | float | \- | 内存使用率触发扩容的阈值（0~1） |
| concurrency\_scale\_threshold | float | \- | 并发使用率触发扩容的阈值（0~1） |
| env | dict | {} | 环境变量（如 ENABLE\_TRAJECTORY） |
| enable\_vpc\_config | bool | \- | VPC 网络开关。需开通请联系商务经理 |

**说明**：表中 `memory_size` 和 `disk_size` 的默认值（10 MB）为函数计算（FC）系统默认最小值。RL 训练实际运行时内存占用远高于此，生产任务**须**将 `memory_size` 提升至 4096 MB 以上、`disk_size` 至 512 MB 以上。

**示例**：

<a id="code-block-5"></a>

```text
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

<a id="fc-runtime-调优深化"></a>

<a id="547vvx6sgmydz"></a>

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

| 函数类型 | 资源画像 | 推荐配置 |
| --- | --- | --- |
| Rollout | IO 密集（LLM/工具调用） | `concurrency` 拉高（30+），CPU 不必很高，`timeout` 600s 起 |
| Reward | CPU/计算密集（评分/正则/模型评分） | `concurrency` 视评分耗时；调用 LLM 评分时按限速降并发；`timeout` 120s 起 |

多 Reward 函数分别配置 Runtime。

**并发估算公式**：

-   `目标并发 ≈ batch_size × n_rollouts × 单次 Rollout 平均耗时(s) / 期望单 step 耗时(s)`（同时处于 in-flight 的 Rollout 请求数）
-   反推 `concurrency × capacity ≥ 目标并发 × 1.2 缓冲`

<a id="训练超参数"></a>

<a id="kl137moij3u9o"></a>

### 训练超参数

RL 训练超参由服务端超参组统一定义：qwen3.5-9b 对应 qwen-rl-v1（33 项）；35B 系列（qwen3.6-flash-2026-04-16 / qwen3.5-flash-2026-02-23 / qwen3.6-35b-a3b）对应 qwen-rl-m35b-v1（35 项，另含 2 个 9B 没有的 MoE 并行参数）。提交时按所选模型自动匹配超参组，无需指定组名。

提交任务时无需传入全部超参：控制台表单中除 `clip_ratio_low`、`tau_pos`、`tau_neg`、`inference_gpu_memory_utilization` 外均为必填项；API 提交时，未传入的参数由服务端自动补全（`clip_ratio_low`、`tau_pos`、`tau_neg` 三项不在任务详情中回显）。qwen3.5-flash-2026-02-23 例外：该模型须显式传入 `nnodes_rollout`（取值见下方推荐训练配置表）。

控制台首屏仅展示基础参数（`n_epochs`、`learning_rate`、`batch_size`，35B 另含 `expert_model_parallel_size`），其余为高级参数，默认折叠且已预填，直接提交即可。

参数按功能分为 6 组：算法与优化、批次与采样、序列长度、学习率与调度、评估与保存、分布式并行与资源。

<a id="算法与优化"></a>

<a id="yyexxd46coagv"></a>

#### 算法与优化

| 参数 | 取值范围或枚举 | 说明 |
| --- | --- | --- |
| algorithm | grpo / dapo / gspo / sapo / cispo | RL 训练算法，选型建议见「算法选型」 |
| use\_kl\_loss | true / false | 是否在损失中加入 KL 正则项，约束策略不偏离参考模型过远 |
| kl\_loss\_coef | — | KL 损失系数，越大对参考模型的约束越强 |
| clip\_ratio\_high | — | 重要性采样比上界裁剪幅度，与 clip\_ratio\_low 配合控制策略更新幅度 |
| clip\_ratio\_low | — | 重要性采样比下界裁剪幅度 |
| tau\_pos | — | SAPO 门控温度，作用于正优势样本（见 SAPO 专用超参数） |
| tau\_neg | — | SAPO 门控温度，作用于负优势样本（见 SAPO 专用超参数） |
| max\_off\_policy\_threshold | — | 样本允许的最大 off-policy 程度（以 rollout 策略与当前策略的版本差度量，超过即丢弃） |
| max\_off\_policy\_strategy | drop | 超过阈值样本的处理策略，当前仅支持丢弃 |

<a id="批次与采样"></a>

<a id="hp-batch-sampling"></a>

#### 批次与采样

| 参数 | 取值范围或枚举 | 说明 |
| --- | --- | --- |
| batch\_size | \[8, 2048\]，步进 8 | 每个训练步采样的 prompt 批大小 |
| n\_rollouts | \[1, 64\] | 每个 prompt 生成的回复数量，用于组内优势估计 |
| ppo\_mini\_batch\_size | \[1, 256\] | 策略更新时的 mini-batch 大小（以 prompt 计） |
| n\_epochs | \[1, 200\]，步进 1 | 训练轮数（数据集遍历次数） |
| num\_warmup\_batches | \[0, 2147483647\]，步进 1 | 正式训练前的预热批数，0 表示不预热 |

Rollout 生成侧的采样参数（`temperature`、`top_p` 等）不在上表超参内，在 Rollout 函数代码中设置（经 `input.sampling_params` 读取并兜底，透传写法见《强化学习的可观测配置与指标参考》的[trace\_client 采样参数透传](observable-configuration-for-reinforcement-learning.md#8n1cfkkp2rzro)）。

<a id="序列长度"></a>

<a id="hp-seq-length"></a>

#### 序列长度

| 参数 | 取值范围或枚举 | 说明 |
| --- | --- | --- |
| max\_prompt\_length | \[128, 131072\] | prompt 最大 token 长度 |
| max\_length | \[128, 131072\] | 单条样本（prompt + 回复）最大总 token 长度，须不小于 max\_prompt\_length |
| enable\_thinking | true / false | 是否允许模型在回复中输出思考内容；开启后响应显著变长，需同步评估 max\_length |

<a id="学习率与调度"></a>

<a id="hp-lr-scheduler"></a>

#### 学习率与调度

| 参数 | 取值范围或枚举 | 说明 |
| --- | --- | --- |
| learning\_rate | — | 学习率 |
| lr\_scheduler\_type | linear / cosine / inverse\_square\_root / constant | 学习率调度策略 |
| lr\_warmup\_steps | \[-1, 2147483647\] | 学习率预热步数，-1 表示由训练框架决定 |

<a id="评估与保存"></a>

<a id="hp-eval-save"></a>

#### 评估与保存

| 参数 | 取值范围或枚举 | 说明 |
| --- | --- | --- |
| eval\_steps | \[1, 2147483647\] | 每隔多少训练步执行一次评估 |
| save\_strategy | steps | checkpoint 保存策略，当前仅支持按步数保存 |
| save\_steps | \[1, 2147483647\] | 每隔多少训练步保存一次 checkpoint |
| save\_total\_limit | \[1, 10\]，步进 1 | 最多保留的 checkpoint 数，超出后删除最旧 |

<a id="分布式并行与资源"></a>

<a id="ngwtolw8f43ih"></a>

#### 分布式并行与资源

| 参数 | 取值范围或枚举 | 说明 |
| --- | --- | --- |
| nnodes\_training | 1 / 2 / 4 / 8 | 训练节点数 |
| n\_gpus\_training | 1 / 2 / 4 / 8 | 每训练节点 GPU 数，训练总卡数 = nnodes\_training × n\_gpus\_training |
| tensor\_model\_parallel\_size | 1 / 2 / 4 / 8 | 训练张量模型并行度（TP） |
| pipeline\_model\_parallel\_size | 1 / 2 / 4 / 8 | 训练流水线模型并行度（PP） |
| sequence\_parallel\_size | 1 / 2 / 4 / 8 | Context Parallel（CP）并行度，沿序列切分、分摊长序列显存 |
| expert\_model\_parallel\_size | 1 / 2 / 4 / 8 / 16 / 32 / 64 / 128 | MoE 专家模型并行度（EP），须整除模型专家数，仅 35B 系列提供 |
| nnodes\_rollout | 1 / 2 / 4 / 8 | 推理（rollout）节点数 |
| n\_gpus\_rollout | 1 / 2 / 4 / 8 | 每推理节点 GPU 数，推理总卡数 = nnodes\_rollout × n\_gpus\_rollout |
| inference\_tensor\_parallel\_size | 1 / 2 / 4 / 8 | 推理引擎张量并行度 |
| inference\_expert\_parallel\_size | 1 / 2 / 4 / 8 / 16 | 推理引擎专家并行度，仅 35B 系列提供 |
| inference\_gpu\_memory\_utilization | \[0, 1\] | 推理引擎 GPU 显存占用比例（KV cache 等），越大吞吐越高但 OOM 风险越大 |

**参数约束**（提交时服务端会校验以下组合，以实际校验结果为准）：

-   `batch_size = N × ppo_mini_batch_size`（N 为正整数）；`batch_size`、`n_rollouts`、`ppo_mini_batch_size` 之间须满足整除关系，保证 mini-batch 均匀切分到各数据并行 worker
-   `max_length` ≥ `max_prompt_length`，两者增大都会显著增加显存占用
-   训练总卡数（`nnodes_training × n_gpus_training`）须能被 TP × PP × CP 整除，商为数据并行度；MoE 模型还须满足 EP 与总卡数的整除关系
-   推理总卡数（`nnodes_rollout × n_gpus_rollout`）须与推理侧各并行度的乘积匹配

> **警告**
>
> `mtu_capacity`（`resources` 中的 MTU 数量）必须严格等于两阶段资源规模之和：`mtu_capacity = nnodes_rollout × n_gpus_rollout + nnodes_training × n_gpus_training`。调整任一参数后，必须同步修改 `mtu_capacity`，保持二者严格相等。

<a id="推荐训练配置"></a>

<a id="k7m3xvq9t2w8"></a>

#### 推荐训练配置

按上下文长度分档，各模型的推荐训练配置如下：

<a id="sec-tabs"></a>

<a id="16k-上下文"></a>

<a id="16k-上下文-h4"></a>

#### 16k 上下文

各模型上下文为 16k，按下表配置提交即可（表中未列出的超参无需传入）；需要 128k 上下文时切换页签：

| 参数 | qwen3.5-9b | 35B 系列（含 flash） |
| --- | --- | --- |
| `nnodes_rollout` | 1 | 1 |
| `n_gpus_rollout` | 8 | 8 |
| `nnodes_training` | 2 | 4 |
| `n_gpus_training` | 8 | 8 |
| `tensor_model_parallel_size` | 8 | 4 |
| `expert_model_parallel_size` | \- | 8 |
| `inference_expert_parallel_size` | \- | 1 |
| **对应 mtu\_capacity** | **24** | **40** |

<a id="128k-上下文"></a>

<a id="128k-上下文-h4"></a>

#### 128k 上下文

训练数据需要 128k 上下文长度时（`max_length` = 131072），在 `hyper_parameters` 中按模型使用以下配置：

| 参数 | qwen3.5-9b | qwen3.6-35b-a3b |
| --- | --- | --- |
| `max_prompt_length` | 130048 | 130048 |
| `max_length` | 131072 | 131072 |
| `nnodes_training` | 4 | 4 |
| `nnodes_rollout` | 2 | 2 |
| `tensor_model_parallel_size` | 2 | 2 |
| `pipeline_model_parallel_size` | 2 | 2 |
| `sequence_parallel_size` | 8 | 8 |
| `expert_model_parallel_size` | \- | 8 |
| `inference_gpu_memory_utilization` | \- | 0.75 |
| `inference_tensor_parallel_size` | 1 | 2 |
| `inference_expert_parallel_size` | \- | 2 |
| **对应 mtu\_capacity** | 48 | 48 |

> **说明**
>
> 9b 模型无 MoE 相关并行参数（表中以 - 表示，`inference&#95;gpu&#95;memory&#95;utilization` 以 - 表示无需传入）。`n&#95;gpus&#95;rollout` 与 `n&#95;gpus&#95;training` 保持 8 不变（2×8 + 4×8 = 48）；mtu\_capacity 为 48，提交时 resources 中的训练单元数量须相应调整。flash 系列（qwen3.6-flash-2026-04-16 / qwen3.5-flash-2026-02-23）需要 128k 上下文时，可参照 qwen3.6-35b-a3b 列配置。

> **重要**
>
> 35B 调参建议：35B 系列模型建议优先 GSPO 算法；`learning_rate` 可降至 9B 的 1/2~2/3；`n_rollouts` 提高到 8~16 平摊采样开销；`expert_model_parallel_size` 如需显式调小可从 2/4 试起，`inference_tensor_parallel_size` 可提高至 4。

<a id="代码示例"></a>

<a id="n8ievm2zwo6g9"></a>

#### 代码示例

第一次训练建议先用以下低成本试跑配置验证链路，通过后交由服务端补全超参正式训练：

<a id="code-block-6"></a>

```text
# 验证链路用：小 batch + 单 epoch 快速确认配置可提交，跑通后由服务端补全超参
hyper_parameters = {
    "algorithm": "gspo",
    "learning_rate": 2e-6,
    "n_epochs": 1,
    "batch_size": 64,
    "n_rollouts": 8,
    "ppo_mini_batch_size": 8,        # 64 = 8 × 8
    "kl_loss_coef": 0.002,
    "lr_scheduler_type": "linear",
    "lr_warmup_steps": -1,
    "max_length": 8192,
    "max_prompt_length": 1024,
    "eval_steps": 1,
    "save_strategy": "steps",
    "save_steps": 100,
    "save_total_limit": 1,
}
```

<a id="算法选型-gspo-grpo-dapo-sapo-cispo"></a>

<a id="450zgadanz9ot"></a>

### 算法选型：GSPO / GRPO / DAPO / SAPO / CISPO

服务端默认算法为 grpo（未指定 algorithm 时自动生效），作为保守基线适合入门与短回复场景；长序列、MoE 场景建议显式指定 gspo（通用推荐）；其余切换需带明确动机（复现 / 长 CoT / 收敛异常）。本文代码示例统一显式指定 gspo；首次跑通直接使用默认 grpo 亦可。

-   **GRPO**（DeepSeekMath 2024）：**Token 级**重要性采样 + 组内相对优势，去 critic
-   **GSPO**（Qwen 2025，**通用推荐**）：**Sequence 级**重要性采样，方差更低，长序列训练稳定性更优
-   **DAPO**：GRPO + Clip-Higher（clip\_ratio\_low=0.2 / clip\_ratio\_high=0.28）+ Dynamic Sampling + Token-level Loss + Overlong Reward Shaping，长 CoT 推理优化
-   **SAPO**（[arXiv 2511.20347](https://arxiv.org/abs/2511.20347)）：用平滑门控替代 PPO 的硬裁剪——重要性比值 r 偏离 1 后梯度平滑衰减，而非像硬裁剪那样直接归零；门控温度越大衰减越快、越接近硬裁剪，越小越平缓、越接近不裁剪的 PG
-   **CISPO**（[arXiv 2506.13585](https://arxiv.org/abs/2506.13585)）：截断重要性采样权重而非更新本身——r 超出上界的 token 梯度仍然保留（PPO 会将这些 token 的梯度置 0）

**R3（专家路由回放）**：所有 RL 算法（GSPO / GRPO / DAPO / SAPO / CISPO）**默认启用**——Rollout 推理时记录 MoE 专家路由、训练时回放该路由，显著缩小训推两侧的 logprob 偏差（logprob diff），端到端精度相应提升。默认生效、无需配置，暂不提供关闭选项（技术背景见 [arXiv 2510.11370](https://arxiv.org/abs/2510.11370) 与 [verl Router Replay](https://github.com/verl-project/verl/blob/main/examples/router_replay/README.md)）。

| 维度 | GRPO | GSPO | DAPO |
| --- | --- | --- | --- |
| 重要性采样粒度 | Token 级 | Sequence 级 | Token 级 + Clip-Higher |
| kl\_loss\_coef 典型值 | ≈ 0.04 | ≈ 0.001 | 0 |
| MoE 稳定性 | 易抖 | 原生稳定 | 需调 |
| 长 CoT 友好度 | 一般 | 好 | **最好** |
| 服务端默认 | **是** | 否 | 否 |
| 推荐场景 | 短回复 / 入门 | 通用首选 / 长序列 | 长链推理 / 数学 / 代码 |

**选型决策路径**：

-   默认 grpo（未指定 algorithm 时的服务端默认）；长序列或 MoE（qwen3.6-35b-a3b）建议 GSPO，其优势更多体现在长序列训练稳定性
-   切 GRPO：需 Token 级细粒度信号 / 与社区 GRPO 实现对齐
-   切 DAPO：响应长度 > 4K / Reward 全对全错塌缩 / 后期 entropy 崩
-   切 SAPO：希望策略更新幅度平滑可控（无硬裁剪），配合 `tau_pos` / `tau_neg` 分别调节正 / 负优势 token 更新的保守程度
-   切 CISPO：希望越界 token 保留梯度（截断 IS 权重而非硬置零）；默认截断区间 \[0, 1.2\]，无需额外参数

SAPO / CISPO 的裁剪机制（平滑门控 / IS 权重截断）与上表三个算法的维度口径不同，上表不直接适用；两者切换后的指标含义变化见[《强化学习的可观测配置与指标参考》§算法相关的指标口径](observable-configuration-for-reinforcement-learning.md#algo-metric-caliber)。

<a id="sapo-专用超参数"></a>

<a id="sapo-cispo-hyperparams"></a>

#### SAPO 专用超参数

| 参数 | 说明 | 取值范围 |
| --- | --- | --- |
| tau\_pos | SAPO 门控温度，作用于 advantage > 0 的 token | \> 0 |
| tau\_neg | SAPO 门控温度，作用于 advantage ≤ 0 的 token | \> 0 |

> **警告**
>
> tau\_pos / tau\_neg **必须为正数**（门控计算含 4/tau，非正数会除零或翻转梯度符号）。推荐 `tau_pos ≥ 1.0`，且 `tau_neg &gt; tau_pos`（负优势 token 的更新更保守）。

配置示例（在 hyper\_parameters 中指定）：

<a id="sec-tabs-2"></a>

<a id="cispo"></a>

<a id="cispo-h4"></a>

#### CISPO

<a id="code-block-7"></a>

```text
# IS 权重截断区间默认 [0, 1.2]，其余参数不用动
"algorithm": "cispo"
```

<a id="sapo-默认-tau"></a>

<a id="sapo-默认-tau-h4"></a>

#### SAPO（默认 tau）

<a id="code-block-8"></a>

```text
# 默认使用论文的 tau，无需显式指定
"algorithm": "sapo"
```

<a id="sapo-调大-tau-neg"></a>

<a id="sapo-调大-tau-neg-h4"></a>

#### SAPO（调大 tau\_neg）

<a id="code-block-9"></a>

```text
# 希望负优势 token 的更新更保守时，调大 tau_neg
"algorithm": "sapo", "tau_pos": 1.0, "tau_neg": 1.3
```

<a id="调参决策表-现象-调谁-怎么调"></a>

<a id="ali8hhzwdicae"></a>

### 调参决策表（现象 → 调谁 → 怎么调）

指标异常时请对照本表选择首选处置项与调整幅度（Reward 区分度的本地排查方法见[强化学习提交前自检](rl-pre-submission-checklist.md)）；P1~P9 完整排查详见《强化学习的可观测配置与指标参考》的[问题排查决策树](observable-configuration-for-reinforcement-learning.md#4h2izjeep16wy)。

| 现象 | 首选处置 | 调整幅度 | 兜底 |
| --- | --- | --- | --- |
| P1 不收敛 | 先查 Reward 区分度，再 learning\_rate ↑ | × 1.5~2 | 查数据量与重复度 |
| P2 震荡 | learning\_rate ↓ | ×0.5 | 仍震荡再 batch\_size ×2；n\_rollouts ↑ |
| P3 KL 爆炸 | kl\_loss\_coef ↑ | × 5~10 | 降 lr |
| KL ≈ 0、不学 | 查 Reward 区分度（本地 test\_functions 零成本） | — | 同 P1：数据 / lr 排查 |
| P4 熵崩塌 | clip\_ratio\_high ↑ | 0.2 → 0.28 | 切 DAPO 或 n\_rollouts ↑ |
| Rollout 慢 | n\_rollouts ↓ / max\_length 收紧 | — | 加 n\_gpus\_rollout（见高级并行）或 FC 并发（见 FC 调优） |
| OOM（训练侧） | ppo\_mini\_batch\_size ↓ | × 0.5 | max\_length ↓ / tensor\_mp ↑（见高级并行；Rollout 侧 OOM 亦见该节） |
| P9 截断率高 | max\_length ↑ | \+ 2048 | 查 max\_prompt\_length |
| P6 过拟合 | 止损选点：按验证指标选较早 Checkpoint 发布 | — | 下次实验 n\_epochs 降至 1~2 |

<a id="调参操作建议"></a>

<a id="70mk1tqz0r2tf"></a>

### 调参操作建议

-   **一次只动一个变量**：同时调 `learning_rate` 和 `batch_size` 会无法归因
-   **跑满**`eval_steps × 3`**个评估周期且不少于 150 步再判断**：50 步看不出趋势——RL 不是 SFT，曲线噪声大

调整优先级隐含在调参决策表的“首选处置”列；保留中间 Checkpoint 的具体设置见 §续训、Checkpoint 与渐进式训练。

<a id="超参设置反模式"></a>

<a id="g5dlozwa0kse0"></a>

### 超参设置反模式

| 反模式 | 后果 |
| --- | --- |
| 用 SFT 的 lr 起点（5e-5）跑 RL | 训练易发散——RL 对 lr 比 SFT 敏感得多 |
| `n_epochs` 设 10+ 期待"训透" | RL 不是 SFT；过多 epoch 触发 P6 验证集崩塌 |
| `kl_loss_coef=0` 且 `n_epochs` > 1 或 lr 偏大 | 无 KL 兜底，策略易漂移（KL=0 本身可行，DAPO 即不使用 KL、靠 ratio 裁剪控制漂移，但须 on-policy 且 lr 保守） |
| `n_rollouts=1` | 组内优势恒为 0，策略零更新（GRPO/GSPO/DAPO 等组内相对优势算法均需 ≥2；组内 Reward 无方差时同样零梯度） |
| 默认并行配置下 `max_length=32K` 求保险 | 显存爆 + Rollout 变慢，按场景设到刚够即可（128k 上下文见推荐训练配置） |

<a id="高级并行参数与显存估算"></a>

<a id="8skxa5du6tbh9"></a>

### 高级并行参数与显存估算

各并行参数的取值范围与说明见「分布式并行与资源」分组表；下文 `tensor_mp` / `inference_tp` / `expert_mp` / `CP` 分别为 `tensor_model_parallel_size` / `inference_tensor_parallel_size` / `expert_model_parallel_size` / `sequence_parallel_size`（Context Parallel）的简写。

**何时需要调整资源配置（5 类触发，OOM 分训练侧 / Rollout 侧）**：

-   **训练侧 OOM** → `tensor_mp` ↑ 或 `ppo_mini_batch_size` ↓
-   **Rollout 侧 OOM** → `inference_gpu_memory_utilization` ↓ 0.1（rollout 与训练在不同节点，调低只影响 rollout 单卡的 KV cache 上限）
-   **Rollout 慢** → 加 `n_gpus_rollout`；长上下文 / 大模型场景才考虑 `inference_tp` ↑
-   **单步训练慢** → 加 `n_gpus_training`，长序列加 `sequence_parallel_size`
-   **MoE 模型** → 必调 `expert_model_parallel_size`

**显存估算说明**：

-   单 GPU 显存 ≈ 模型权重（bf16 约 2 字节/参数）+ 优化器（AdamW 约 8 字节/参数，不含 fp32 master weights）+ 激活值（随 bs × seq\_len 增长）+ KV cache
-   9B dense 权重+优化器约 90 GB/实例（不含激活与 KV cache），需 TP 分摊
-   `inference_gpu_memory_utilization` 调低 = rollout 单卡 KV cache 上限变小，OOM 风险降低
-   **不要**盲目加节点，先 TP 切分；常见反例：模型不大、卡数充裕时仍调高 `tensor_mp` → 通讯吃掉收益、`inference_gpu_memory_utilization=0.95` → OOM 抖动、Dense 模型设 `expert_mp > 1` → 报错、并行度乘积超过训练总卡数 → 配置非法

<a id="任务管理"></a>

<a id="ikviw8lqtv2nw"></a>

## 任务管理

| 操作 | SDK | CLI |
| --- | --- | --- |
| 查询状态 | `AgenticRL.get(job_id="ft-xxx")` | `dashscope rl get "ft-xxx" -o json` |
| 列举任务 | `AgenticRL.list()` | `dashscope rl list --page 1 --size 10 -o json` |
| 取消任务 | `AgenticRL.cancel(job_id="ft-xxx")` | `dashscope rl cancel "ft-xxx"` |
| 查看日志 | `AgenticRL.logs(job_id="ft-xxx", lines=100)` | `dashscope rl logs "ft-xxx" --offset 1 --lines 100` |

<a id="实验管理"></a>

<a id="6jr9z7qfcf82b"></a>

### 实验管理

<a id="yaml-多实验模式"></a>

<a id="ae8xc6fe5aeuf"></a>

#### YAML 多实验模式

-   `job_name` 标识实验、`tuned_model_name` 标识产出模型，每次实验改这两个即可隔离
-   YAML 集中管理 model/datasets/functions/runtime/hyper\_parameters 便于 Git 版本化
-   优先级 `__init__()` < YAML < `run()/submit_job()` 运行时参数——做对照实验只改最外层

<a id="扫参-ci-集成场景为何选-submit-job"></a>

<a id="zl6sdn6eb8tcy"></a>

#### 扫参 / CI 集成场景为何选 submit\_job

三种提交方式的场景决策：

-   **扫参 / CI**：函数已稳定只换超参 → `submit_job(entity_id=...)` 省去重复注册+上传（10x+ 提速）
-   **首次 / 调试 Reward**：用 `run()` 每次自动重注册防止代码不同步
-   Entity ID（`ro-` Rollout / `rw-` Reward）从首次注册返回值取，可入 CI 配置长期复用

<a id="ci-集成与命令对照"></a>

<a id="byqzqrlravo03"></a>

#### CI 集成与命令对照

-   `dashscope rl run -c job.yaml -o json` 提交后解析 `job_id` 轮询 status，FAILED 直接拉 logs 告警；`-o json` 是 CI 解析必备

<a id="续训-checkpoint-与渐进式训练"></a>

<a id="li0dod5x67q2o"></a>

### 续训、Checkpoint 与渐进式训练

训练完成不等于训练成功——必须选对 Checkpoint 才发布。

<a id="checkpoint-保留与选择"></a>

<a id="pwsw4eolrpy2h"></a>

#### Checkpoint 保留与选择

-   `save_strategy=steps` + `save_steps=100` + `save_total_limit=3`：最多保留 3 个、超出自动清理最旧
-   **选哪个 Checkpoint**：必须看 `validation/data/reward/mean@1` 选最佳点，**不一定是最后一个**
-   保留 3~5 个权衡空间与回滚需求

<a id="基于已发布-checkpoint-续训"></a>

<a id="eedur2ygyugrc"></a>

#### 基于已发布 Checkpoint 续训

-   续训 = 把上次产出的模型作为 `model` 入参再次提交，超参可微调（lr 通常调小）
-   适用：数据增量 / Reward 调整 / 长链路逐步收敛
-   注意：基础模型版本须一致，跨基座模型不可直接续训
-   在多阶段训练流水线中，每阶段产出可作为下一阶段的 `model` 入参逐级递进（CPT/SFT/DPO/RL 概念见[强化学习训练概述](rl-training-overview.md)）

<a id="常见问题"></a>

<a id="7dm08x8e1lxul"></a>

## 常见问题

<a id="函数注册失败"></a>

<a id="iv8t2ede39t9r"></a>

### 函数注册失败

-   检查 classpath 是否正确（格式：module.path.ClassName）
-   确认 requirements.txt 存在于项目根目录
-   确认所有依赖已列入 requirements.txt

<a id="任务提交失败"></a>

<a id="czgc194tses7s"></a>

### 任务提交失败

-   检查 Entity ID 和 File ID 是否有效
-   确认基座模型在当前地域可用
-   检查 functions 列表中每个 Reward 组件的 runtime 配置是否完整；CLI 提交时确认 reward 相关参数与函数组件数量一致

<a id="如何优化性能"></a>

<a id="z1un738dyw9je"></a>

### 如何优化性能？

-   I/O 密集型任务使用 async def process
-   在 CPU/内存允许的范围内提高 concurrency
-   ENABLE\_TRAJECTORY 会增加存储和延迟，正式训练时按需开启

<a id="trace-看不到如何排查"></a>

<a id="ih2r6a9vjp1le"></a>

### Trace 看不到如何排查

排查步骤详见《强化学习的可观测配置与指标参考》的 [Trace 看不到如何排查](observable-configuration-for-reinforcement-learning.md#x92gxpfav5tt9)（含 ARMS 授权、`ENABLE_TRAJECTORY` 开关、依赖检查的完整流程）。

<a id="如何查看训练日志"></a>

<a id="ouh15atempvuh"></a>

### 如何查看训练日志？

-   SDK：`AgenticRL.logs(job_id="ft-xxx", lines=100)`
-   CLI：`dashscope rl logs "ft-xxx" --offset 1 --lines 100`
-   也可在百炼控制台的训练详情页查看

<a id="如何将-checkpoint-发布为可用模型"></a>

<a id="shvfwl4n7ufd0"></a>

### 如何将 Checkpoint 发布为可用模型？

-   切换到百炼控制台训练详情页的产出页签，找到目标 Checkpoint，点击"发布"按钮
-   发布后的模型可通过模型名称在 API 中直接调用

<a id="训练-reward-不涨如何排查"></a>

<a id="9157093r4tl14"></a>

### 训练 Reward 不涨如何排查

Reward 不涨属于“P1 不收敛”场景，按以下顺序排查：

1.  **看主信号**：`critic/rewards/mean` 长平台 + `actor/ppo_kl ≈ 0` + `actor/grad_norm` 极小 → P1
2.  **常见根因**（按排查成本从低到高）：Reward 函数恒返回相同值（本地 `test_functions` 零成本可查）→ 数据不足或重复 → lr 太小
3.  **首选处置建议**：先本地用 `test_functions` 确认评分有区分度（不是恒 0 或恒 1，方法见[强化学习提交前自检](rl-pre-submission-checklist.md)）；确认有区分度后 `learning_rate × 1.5~2`（参考调参决策表）
4.  **兜底**：查数据量与重复度

完整 P1~P9 问题排查决策树详见《强化学习的可观测配置与指标参考》的[问题排查决策树](observable-configuration-for-reinforcement-learning.md#4h2izjeep16wy)。

<a id="后续步骤"></a>

<a id="oxczmune6uufl"></a>

## 后续步骤

-   回顾概述 → [强化学习](rl-training-overview.md)
-   了解函数开发 → [强化学习开发指南](rl-function-development-guide.md)
-   了解可观测性配置与轨迹查看 → [强化学习的可观测配置与指标参考](observable-configuration-for-reinforcement-learning.md)
