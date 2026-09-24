# 在线策略蒸馏训练概述

百炼在线策略蒸馏训练概述——基本概念、训练方式选型、端到端流程、环境准备与任务提交

本文帮助您了解百炼在线策略蒸馏（OPD）训练的基本概念、适用场景与端到端流程。本文提供概览与关键说明，各环节的详细操作步骤见对应文档：

**文档**

**内容**

[Model OPD 开发](opd-model-development-guide.md)

纯蒸馏与 Reward 函数开发、数据格式、函数测试

[Agentic OPD 开发](opd-agentic-development-guide.md)

自定义 Rollout（传入 tools 参数产生结构化 tool\_call）、Agentic Reward 开发

[训练配置](opd-training-config.md)

提交方式、教师模型配置、超参数、环境变量、调参与避坑

[可观测配置](opd-observable-config.md)

Tracing 接入、自定义指标、指标字典、效果判断、排查决策树

在线策略蒸馏基本概念及与微调、传统蒸馏的区别

OPD（在线策略蒸馏）是用更强教师模型对学生模型逐 token 监督的训练方式。教师模型对学生模型输出每个 token 给出概率分布，学生模型自己生成输出，每一步都有指导信号。目标是把大模型在特定任务上的能力迁移到更小的同族模型，在保持效果的同时降低推理成本。

**原理**

OPD 训练每步：

1.  **学生生成**：学生模型生成一段输出
2.  **教师给分布**：教师模型对输出每个 token 位置给出概率分布（即教师认为该位置各 token 出现的可能性）
3.  **算差异**：学生模型对比自己的概率分布与教师分布，计算每个 token 位置的差异（KL 散度，衡量两个概率分布差异的指标）
4.  **更新靠拢**：以此为损失更新参数，让每个 token 向教师模型靠拢

教师模型只给概率分布，不生成文本、不参与对话或工具调用。每个 token 位置都有指导信号，不是等整条输出结束才给一个总评分。

**OPD 与微调、传统模型蒸馏的区别**

**维度**

**微调（SFT）**

**传统模型蒸馏**

**在线策略蒸馏（OPD）**

训练数据

人工标注

教师模型预生成输出

学生模型生成

指导方式

固定标签

教师模型完整输出

教师模型逐 token 概率分布

学生模型参与生成

否

否

是

纠错

无

无

逐 token 纠正

## 全流程概览

OPD 训练从环境准备到模型部署，共 5 步：

1.  **环境准备** — 安装 SDK、获取 API Key、完成授权
2.  **准备数据与代码** — JSONL 数据，纯蒸馏无需写函数
3.  **提交训练任务** — 传 `teacher_model` 触发蒸馏，纯蒸馏零代码
4.  **训练状态观测** — 查看蒸馏损失、教师模型信号是否健康、验证集指标
5.  **发布与部署模型** — 最后 Checkpoint 自动发布，部署后通过 API 调用

### 工作机制

每轮训练数据流如下：

```
训练数据（用户问题 + 参考答案）
            │
            ▼
学生模型生成：学生模型按当前策略生成候选输出
            │
            ▼
教师模型前向：教师模型对学生模型输出逐 token 给概率分布
            │
            ▼
蒸馏更新：学生模型最小化自身分布与教师模型分布差异（KL 散度）
            │
            ▼
（可选）Reward 评分：启用 Reward 时叠加任务奖励信号
            │
            ▼
循环迭代：用更新后的模型重新采样，逐轮向教师模型靠拢
```

教师模型只给概率分布，不生成文本、不参与对话或工具调用。纯蒸馏仅由教师模型逐 token 指导；同时启用奖励（Reward）时，教师模型分布与任务奖励共同驱动学生模型。

## 模型与训练单元

教师模型须为百炼已开通的模型，与学生模型同系列且能力更强。

#### 华北2（北京）

**教师模型**

**学生模型**

**邀测标识**

**推荐训练单元**

qwen3.5-122b-a10b

qwen3.5-27b

邀测

IV 型（MTU4）× 24

qwen3.5-397b-a17b

qwen3.5-27b

邀测

IV 型（MTU4）× 24

qwen3.5-122b-a10b

qwen3.5-2b

邀测

IV 型（MTU4）× 24

qwen3.5-27b

qwen3.5-2b

邀测

IV 型（MTU4）× 24

qwen3.5-35b-a3b

qwen3.5-2b

邀测

IV 型（MTU4）× 24

qwen3.5-397b-a17b

qwen3.5-2b

邀测

IV 型（MTU4）× 24

qwen3.5-122b-a10b

qwen3.5-35b-a3b

邀测

IV 型（MTU4）× 24

qwen3.5-397b-a17b

qwen3.5-35b-a3b

邀测

IV 型（MTU4）× 24

qwen3.5-122b-a10b

qwen3.5-4b

邀测

IV 型（MTU4）× 24

qwen3.5-27b

qwen3.5-4b

邀测

IV 型（MTU4）× 24

qwen3.5-35b-a3b

qwen3.5-4b

邀测

IV 型（MTU4）× 24

qwen3.5-397b-a17b

qwen3.5-4b

邀测

IV 型（MTU4）× 24

qwen3.5-122b-a10b

qwen3.5-9b

邀测

IV 型（MTU4）× 24

qwen3.5-27b

qwen3.5-9b

邀测

IV 型（MTU4）× 24

qwen3.5-35b-a3b

qwen3.5-9b

邀测

IV 型（MTU4）× 24

qwen3.5-397b-a17b

qwen3.5-9b

邀测

IV 型（MTU4）× 24

#### 新加坡

**教师模型**

**学生模型**

**邀测标识**

**推荐训练单元**

\-

\-

\-

\-

## 快速开始

以纯蒸馏基础样例完成全流程 5 步，零代码即可开训。纯蒸馏无需编写任何函数，仅由教师模型逐 token 指导学生模型训练。

### 环境准备

环境准备需完成以下几项：API Key、服务授权、SDK 安装、工作区目录、核心环境变量。

**API Key** 从[百炼控制台 API-KEY 页](https://bailian.console.aliyun.com/?tab=app#/api-key)获取，设为环境变量 `DASHSCOPE_API_KEY`。

**服务授权** 首次使用时，在[模型调优控制台](https://bailian.console.aliyun.com/cn-beijing/model/tuning)一键授权 ARMS（应用实时监控服务，承载 OpenTelemetry 指标上报）、函数计算（FC）、日志服务（SLS）三项云服务。OpenTelemetry 是开源可观测性数据标准，ARMS 为其提供托管与可视化，分别用于指标上报、函数运行、日志采集。

**SDK** 以示例目录附带的 wheel 文件为准安装（版本随示例更新，当前 1.27.5）：

```
# 安装示例目录附带的 dashscope SDK wheel 文件（版本随示例更新，当前 1.27.5）
# 该 wheel 同名相对路径需填入 FC_PYPI_LIB，供远端函数运行时安装
python -m pip install ./dashscope-*.whl
```

**工作区目录** 从[示例代码包](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/files/6a4b3c2d1e0f92ef.zip)获取，含 wheel（Python 打包安装文件）、函数代码、数据、依赖、提交脚本，结构如下；获取与提交脚本的完整实现见[训练配置](opd-training-config.md)：

```
workspace/
├── dashscope-*.whl          # SDK wheel：示例附带的 dashscope 安装包，本机与远端均按此版本安装
├── functions/               # Rollout/Reward 函数代码目录；纯蒸馏 functions=None 可留空
├── data/                    # JSONL 训练/验证数据；每行一个样本（messages + rollout_extra）
├── requirements.txt         # 函数依赖清单；FC_LAYER_USED=true 时注册阶段据此构建 layer，跳过冷启动 pip
└── submit_job.py            # 提交脚本：调用 AgenticRL().run() 完成注册→上传→提交三步
```

三个核心环境变量：

-   `DASHSCOPE_API_KEY`（必需）：鉴权。
-   `FC_PYPI_LIB`（必需）：指定函数运行时安装的 SDK 包，填 wheel 相对路径（远端解析，本机绝对路径无法命中）；纯蒸馏（functions=None）不涉及函数运行时，可跳过此项。
-   `FC_LAYER_USED`（可选，默认 true）：true 时在注册阶段依据 requirements.txt 构建 layer，跳过冷启动 pip 安装；false 时由远端运行时冷启动安装。

```
export DASHSCOPE_API_KEY="sk-your-api-key"                       # 鉴权密钥，从百炼控制台 API-KEY 页获取（必需）
export FC_PYPI_LIB=./dashscope-1.27.5-py3-none-any.whl          # 远端函数运行时安装的 SDK 包，填 wheel 相对路径；纯蒸馏可不设（必需，纯蒸馏除外）
export FC_LAYER_USED=true                                        # true：注册阶段按 requirements.txt 构建 layer，跳过冷启动 pip 安装；false：远端冷启动安装
```

`FC_PYPI_LIB` 填实际 wheel 文件名（版本号随示例更新）。

提交前示例脚本会校验所装 SDK 的 `AgenticRL.run` 是否接受 `teacher_model` 参数，不接受则直接报错退出。其余环境变量（控制面端点、推理端点、日志级别等）见[训练配置](opd-training-config.md)。

### 准备数据与代码

JSONL 每行一个样本，含 `messages` 与 `rollout_extra` 两个字段。`messages` 为对话输入（ChatML 格式），`rollout_extra` 存放参考答案或其他业务数据，供 Reward/自定义 Rollout 启用时消费。

```
{
  "messages": [                          // 对话输入，ChatML 格式；每条 message 含 role 与 content
    {"role": "user", "content": "<您的业务问题>"}
  ],
  "rollout_extra": {"solution": "<参考答案或其他业务数据>"}  // 参考答案/业务数据，供 Reward 或自定义 Rollout 启用时消费；纯蒸馏仅透传不消费
}
```

快速验证用几十条即可；正式训练数百到数千条，视任务复杂度而定。纯蒸馏时 `rollout_extra` 仅作数据透传不被消费。

### 提交训练任务

入口 `AgenticRL().run(...)`，传 `teacher_model` 即触发蒸馏。`run()` 一步完成：注册函数到 FC → 上传训练数据 → 提交训练任务。纯蒸馏不注册函数。

最小提交代码示例

以下为最小提交代码示例，注释说明各参数含义。完整实现见[训练配置](opd-training-config.md)的 submit\_job.py。teacher\_model 为占位值，实际由您定义。

```
import asyncio
from dashscope.finetune.agentic_rl import AgenticRL          # OPD 提交客户端
from dashscope.finetune.reinforcement import (
    TrainingDataset, ValidationDataset, DataSourceType,       # 训练/验证数据集及数据源类型
)

async def main():
    client = AgenticRL()
    result = await client.run(
        job_name="my-opd-job",                                # 任务名（控制台展示用）
        model="qwen3.5-9b",                       # 学生模型（基座模型，被蒸馏对象）
        teacher_model="your-teacher-model-id",     # 教师模型，OPD 唯一新增参数；传值即触发蒸馏
        training_datasets=[TrainingDataset(
            data_source_type=DataSourceType.FILE_ID,          # 以文件方式上传训练数据
            file_name="./data/train.jsonl")],
        validation_datasets=[ValidationDataset(
            data_source_type=DataSourceType.FILE_ID,          # 验证集同样以文件方式上传
            file_name="./data/validation.jsonl")],
        functions=None,                            # 纯蒸馏：不注册任何函数；Agentic OPD 在此传 Rollout/Reward 函数
        hyper_parameters={
            "n_epochs": 1, "n_rollouts": 8, "learning_rate": 1e-6,  # 蒸馏是微调模型已有能力，学习率起点 1e-6
            "eval_steps": 1, "ppo_mini_batch_size": 8,
            "lr_scheduler_type": "cosine",  # kl_loss_coef OPD 未启用，见训练配置
            # opd_teacher_* 部署参数见训练配置
        },
        resources={
            "charge_type": "mtu_postpaid",           # MTU 后付费计费
            "mtu_spec_code": "MTU4",                  # 训练单元规格
            "mtu_capacity": 24,                      # 容量（并发资源数）
        },
    )
    # HTTP 200 返回 job_id（查询训练状态的唯一标识）；否则打印原始响应便于排查
    print(result.output.job_id if result.status_code == 200 else result)

asyncio.run(main())                                  # 启动异步主函数
```

**说明**也可以通过配置文件或 CLI（`dashscope rl run`）提交，三种方式与字段逐项说明见[训练配置](opd-training-config.md)。

### 起步技巧

-   **先选示例**：纯文本输出任务从 Model OPD 示例入手；输出依赖 API 级 tool call 或多轮/自定义交互时从 Agentic OPD 示例入手。
-   **先用精简数据**：几十条 + `n_epochs=1` 验证链路后再换完整数据集，避免在完整数据集上消耗 MTU 后才发现配置错误。
-   **超参保持默认**：`learning_rate` 起点 `1e-6`（蒸馏是微调模型已有能力而非重建，学习率过大易破坏输出格式），`lr_scheduler_type` 用 `cosine`；要调时一次只动一个变量，至少训练 `eval_steps × 3` 步再判断趋势。
-   **FAILED 先看日志**：任务失败 → 日志页签查看末尾报错，或 SDK 调用 `AgenticRL.logs(job_id="ft-xxx", lines=100)`。

## 训练后流程

### 观测与判断效果

`run()` 返回的 `job_id` 是查询训练状态的唯一标识。[模型调优控制台](https://bailian.console.aliyun.com/cn-beijing/model/tuning)进入任务详情页，含指标、轨迹、产出、日志四个页签。

观测重点：

-   `trace/distillation/valid_token_rate` 接近 1.0（教师模型信号完整）。
-   `actor/distillation/loss` 下降或趋稳（学生模型向教师模型靠拢）。
-   启用 Reward 时加看 `validation/data/reward/mean@1` 与 `trace/reward_metrics` 各维度相对基线上升。

训练后评测需保留训练前基线并保持一致的评测条件（相同评测集与解码参数）。完整指标含义、轨迹查看、验收判据与排查决策树见[可观测配置](opd-observable-config.md)。

### 发布与部署

训练完成后最后一个 Checkpoint 自动发布至[我的模型](https://bailian.console.aliyun.com/cn-beijing/model/custom)。如需发布中间 Checkpoint，前往[模型调优控制台](https://bailian.console.aliyun.com/cn-beijing/model/tuning)产出页面手动操作。发布后的模型可在我的模型页面部署，部署完成后即可通过 API 调用。

## 适用场景

适用场景按能力复杂度逐级拓展：纯蒸馏是基础能力，Reward 与自定义 Rollout 是在其上按需叠加的进阶能力（引入额外组件与更复杂的训练/生成链路）。

-   纯蒸馏（基础）：仅教师模型+数据，不写任何函数组件 → [Model OPD 开发](opd-model-development-guide.md)
-   +Reward（进阶）：加一个评分函数，在教师模型逐 token 指导基础上叠加任务奖励（按标准答案评分、按多维度指标评分） → [Model OPD 开发](opd-model-development-guide.md)
-   +自定义 Rollout（进阶，Agentic OPD）：输出依赖工具调用/多轮交互时自定义生成过程；可与 Reward 叠加，也可单独使用 → [Agentic OPD 开发](opd-agentic-development-guide.md)

两项进阶能力可独立启用、自由组合；选型先看生成路径：单轮生成可达 → 前两级（Model OPD）；需结构化机制（如原生 tool call）或自定义交互 → 第三级（Agentic OPD）。

## 后续步骤

-   [Model OPD 开发](opd-model-development-guide.md)：函数开发完整细节（Rollout/Reward 函数、Tracing 接入）。
-   [Agentic OPD 开发](opd-agentic-development-guide.md)：自定义 Rollout（传入 tools 参数、结构化输出）、Agentic Reward 开发。
-   [训练配置](opd-training-config.md)：提交方式、字段逐项说明、超参与环境变量。
-   [可观测配置](opd-observable-config.md)：指标含义、轨迹查看、验收判据与排查决策树。

## 常见问题

### 何时选 OPD 而非 SFT

需逐 token 纠错、学生模型从自身生成中学习 → OPD；仅有固定标注、预算敏感且不要求在线纠错 → SFT。

### 没有 reward 能否判断训练有效

能。纯蒸馏靠 `valid_token_rate` 趋近 1.0 与 `loss` 下降趋稳判断教师模型信号是否被吸收，最终效果靠训练后独立评测（保留基线、同口径对比）。若需在训练中按任务目标在线优化，则叠加 Reward（Model OPD 的进阶用法），代价是需提供可计算的 Reward 函数。
