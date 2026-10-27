# Model OPD 开发

Model OPD 开发：纯蒸馏无需编写函数组件，叠加 Reward（进阶用法）评分函数开发，含数据格式与常见问题

Model OPD 开发只需准备数据与提交配置即可开训（纯蒸馏，无需编写函数组件）——学生模型输出生成由百炼完成，无需编写。需按业务目标在线优化时，再编写 Reward 评分函数叠加到训练流程（进阶用法）。两种用法差异如下。训练概述见[在线策略蒸馏训练概述](opd-training-overview.md)。

**维度**

**无 Reward（纯蒸馏）**

**有 Reward**

开发工作

仅准备数据与提交配置，无需编写函数组件

额外编写 Reward 评分函数

训练信号

教师模型逐 token 概率分布（唯一监督）

教师分布 + 任务奖励（按标准答案或多维度评分）

适用场景

教师模型已是任务上限、无需按任务目标在线优化

需按业务目标在线优化、拉向标准答案

## 数据格式

每行一条 JSONL，`messages` 为对话列表，`rollout_extra` 携带附加信息。

```
{"messages":[{"role":"system","content":"<任务说明>"},{"role":"user","content":"<用户输入>"}],"rollout_extra":{"solution":"<ground_truth（标准答案）>"}}
```

`messages` 中 `system` 放任务说明，`user` 为用户输入。`rollout_extra.solution` 存 ground truth（标准答案），供 Reward 读取。纯蒸馏不注册 Reward，`rollout_extra` 仅作数据标记不被消费；启用 Reward 时 Reward 从 `solution` 取评分基准。

## 无 Reward 开发参考（纯蒸馏）

纯蒸馏不写任何函数，开发工作仅为准备数据与提交配置。

### 提交代码

`functions=None` 使控制面（调度层）执行原生 Rollout（百炼内置的采样生成，学生模型直接生成输出、不传 tools 参数；相对 Agentic OPD 的多轮/自定义交互与自定义 Rollout）。教师模型蒸馏为唯一监督信号。纯蒸馏须传 `None` 而非空列表 `[]`（控制面对两者处理不保证相同）。

```
from dashscope.finetune.agentic_rl import AgenticRL
from dashscope.finetune.reinforcement import (
    DataSourceType, TrainingDataset, ValidationDataset,
)

client = AgenticRL()
result = await client.run(
    job_name="my-pure-distill",  # 任务名，唯一标识本次训练
    model=student_model,  # 学生模型 ID，被蒸馏的对象
    teacher_model=teacher_model,  # 教师模型 ID，提供 token 概率分布作为蒸馏监督信号
    training_datasets=[
        TrainingDataset(
            data_source_type=DataSourceType.FILE_ID,  # 数据来源类型：文件 ID（百炼已上传的文件）
            file_name="data/train.jsonl",  # 训练集路径，JSONL 格式
        )
    ],
    validation_datasets=[
        ValidationDataset(
            data_source_type=DataSourceType.FILE_ID,
            file_name="data/validation.jsonl",  # 验证集路径，用于训练中评估
        )
    ],
    functions=None,  # None 而非空列表：控制面据此执行原生 Rollout（纯蒸馏，不注册任何函数组件）
    hyper_parameters={...},  # 超参、opd_teacher_* 部署参数见训练配置
)
```

## 叠加 Reward（进阶用法）

注册 Reward 组件后，控制面在每条 Rollout 后调用它评分，产出分维度指标参与训练。

### Reward 函数结构

继承 `AbstractRewardProcessor`，实现 `async process(input: RewardInput) -> RewardOutput`，关键约定如下：

-   **装饰器自动接入 Tracing**：`process` 用 `@observe_processor` 装饰，追踪客户端（trace client）由装饰器隐式注入，process 方法内不显式调用
-   **输入字段**：`RewardInput` 含 `ground_truth` 与 `agent_output`（原生 Rollout 产出，只读）
-   **输出字段**：`RewardOutput` 含 `Reward(reward_score, reward_metrics)` 与 `TaskStatus`

```
from dashscope.finetune.reinforcement import (
    AbstractRewardProcessor, Reward, RewardInput, RewardOutput, TaskStatus,
)
from dashscope.finetune.reinforcement.component.observability import observe_processor

class MyRewardProcessor(AbstractRewardProcessor):
    @observe_processor  # 装饰器：自动接入 Tracing，追踪客户端隐式注入，方法内不显式调用
    async def process(self, input: RewardInput) -> RewardOutput:
        # 入参 input: RewardInput，含 ground_truth（评分基准）与 agent_output（原生 Rollout 产出，只读）
        # 返回 RewardOutput，含 Reward(reward_score, reward_metrics) 与 TaskStatus
        # 1. 取数据：ground_truth + 末轮 assistant 文本
        ground_truth = input.ground_truth  # 优先取注入的标准答案
        if ground_truth is None:
            if input.agent_output.rollout_extra:  # 回退到数据侧 rollout_extra.solution
                ground_truth = input.agent_output.rollout_extra.get("solution")
        messages = input.agent_output.messages  # Rollout 对话历史
        content = messages[-1]["content"] if messages else ""  # 末轮 assistant 回答文本
        # 2. 剥离思考链 thinking（见输出文本清理）
        content = strip_reasoning(content)
        # 3. 评分：返回 dict，含主分 reward_score 与附加维度
        metrics = your_scoring_function(content, ground_truth)
        # 4. reward_score 单独赋给 Reward.reward_score，其余进 reward_metrics
        reward_score = metrics.pop("reward_score")  # 从 dict 取出主分，避免重复进 metrics
        return RewardOutput(
            reward=Reward(reward_score=reward_score, reward_metrics=metrics),  # 主分 + 维度 dict[float]
            status=TaskStatus.SUCCESS, error=None,  # 处理结果状态，失败置 TaskStatus.FAIL 并填 error
        )
```

`RewardInput` / `RewardOutput` 关键字段：

**字段**

**来源**

**用途**

`ground_truth`

RewardInput（源自 rollout\_extra.solution）

评分基准

`agent_output.messages`

原生 Rollout 产出

取末轮 assistant content

`reward_score`

Reward.reward\_score

主分，单独上报

`reward_metrics`

Reward.reward\_metrics

其余维度 dict\[float\]

`status`

TaskStatus

处理结果状态

### 输出文本清理

原生 Rollout 的输出里，除了学生的回答，还混着思考过程与工具调用格式的文本。不清理会干扰 Reward 评分，需先剔掉这些只留回答再评分。清理步骤：

1.  剥离思考链 thinking
2.  剔除工具调用文本

```
import re
# 占位标签示意，实际正则按业务定义
# 实际标签名取自学生模型的 chat template（如 <think>...</think>），按实际模型定义正则
THINKING_BLOCK = re.compile(r"imd.*?imd_end", re.DOTALL)  # 匹配完整 thinking 块（含闭标签）
LEADING_THINK = re.compile(r"^.*?imd_end", re.DOTALL)  # 首个闭标签前可能有散落 thinking，先删完整块再取 tail
TOOL_CALL_BLOCK = re.compile(r"tool_call.*?end_tool_call|function=.*?end_function", re.DOTALL)  # 工具调用文本块

def strip_reasoning(content):
    # 入参 content: 末轮 assistant 原始文本；返回: 仅保留回答正文
    # 剥完整 thinking 块 + 首个闭标签前内容 + 工具调用文本
    content = THINKING_BLOCK.sub("", content)  # 先删成对 thinking 块
    content = LEADING_THINK.sub("", content)  # 再删首个闭标签前的散落 thinking
    content = TOOL_CALL_BLOCK.sub("", content)  # 最后删工具调用文本
    return content
```

### 评分逻辑

`reward_score` 为主奖励标量，`reward_metrics` 为附加维度字典（每值 float）。`reward_score` 单独赋给 `Reward.reward_score`，不重复进 `reward_metrics`（`metrics.pop("reward_score")`）。维度划分与权重由任务决定，按业务自行实现。

下面是最小可跑实现：content 含 ground\_truth 即得 1.0，否则 0.0，便于先跑通链路再扩展维度。

```
def your_scoring_function(content, ground_truth):
    # 入参 content: 清理后的回答文本；ground_truth: 标准答案（评分基准）
    # 返回 dict：reward_score 为主分（必填，被 pop 单独上报），其余键为附加维度
    # 最小实现：content 含 ground_truth 即得 1.0，否则 0.0
    hit = float(ground_truth in content) if ground_truth else 0.0  # 命中标记，无 ground_truth 则 0
    return {
        "reward_score": hit,  # 主奖励标量，单独赋给 Reward.reward_score
        "coverage": hit,  # 附加维度示例：覆盖率，扩展维度后自行调整
    }
```

### 提交启用 Reward 的训练任务

写好 `MyRewardProcessor` 后，用 `RewardFunctionComponent` 把它注册到 `functions` 列表即可。`run()` 一步完成注册 → 上传数据 → 提交任务。

```
from dashscope.finetune.agentic_rl import AgenticRL
from dashscope.finetune.reinforcement import (
    RewardFunctionComponent, FunctionComponentModel,
    FunctionComponentRuntime, TrainingDataset,
    ValidationDataset, DataSourceType,
)

client = AgenticRL()
result = await client.run(
    job_name="my-opd-reward-job",  # 任务名
    model=student_model,  # 学生模型 ID
    teacher_model=teacher_model,  # 教师模型 ID，蒸馏监督信号
    training_datasets=[TrainingDataset(
        data_source_type=DataSourceType.FILE_ID,
        file_name="data/train.jsonl")],  # 训练集
    validation_datasets=[ValidationDataset(
        data_source_type=DataSourceType.FILE_ID,
        file_name="data/validation.jsonl")],  # 验证集
    functions=[RewardFunctionComponent(  # 注册 Reward 组件，控制面在每条 Rollout 后调用评分
        name="reward-1",  # 组件名，唯一标识
        weight=1.0,  # 奖励权重，多 Reward 时按加权聚合
        timeout=120,  # 单次调用超时（秒），超时按失败处理
        fcmodel=FunctionComponentModel(
            zipdir=".",  # 工作区根目录（含 functions/）
            classpath="functions.reward.reward.MyRewardProcessor"),  # 入口类（示例类名，实际由您自定义）
        runtime=FunctionComponentRuntime(  # 组件运行时资源配置
            cpu=2, memory_size=4096, disk_size=512,  # CPU/内存(MB)/磁盘(MB)
            concurrency=20, capacity=10, min_capacity=10, max_capacity=30))],  # 并发与弹性容量配置
    hyper_parameters={...},  # 超参、opd_teacher_* 部署参数见训练配置
)
```

`classpath` 指向 `MyRewardProcessor` 所在模块路径；`zipdir="."` 把整个工作区打包上传。完整字段说明见[训练配置](opd-training-config.md)。

### 函数测试

提交训练前先本地验证 Reward 评分逻辑，避免到训练任务里才发现评分错误（浪费算力）。对 `your_scoring_function` 输入样例 content 与 ground\_truth，断言各维度值符合预期。把以下测试与 `your_scoring_function`、`strip_reasoning` 放进同一文件（如 `test_reward.py`），本地即可跑通。

```
def test_hit():
    # 用例：content 含 ground_truth → 命中，主分与覆盖率均为 1.0
    metrics = your_scoring_function("query_status done", "query_status")  # 入参: 回答文本、标准答案
    assert metrics["reward_score"] == 1.0  # 主分单独校验
    assert metrics["coverage"] == 1.0  # 附加维度校验

def test_thinking_residual():
    # 用例：带思考链残留，strip 后含 ground_truth → 命中
    content = "imd thinking imd_end query_status"  # 含 thinking 块的原始输出
    cleaned = strip_reasoning(content)  # 清理后应只剩 "query_status"
    metrics = your_scoring_function(cleaned, "query_status")
    assert metrics["coverage"] == 1.0  # 验证清理 + 评分链路打通

def test_miss():
    # 用例：content 不含 ground_truth → 主分 0.0
    metrics = your_scoring_function("delete_item failed", "query_status")
    assert metrics["reward_score"] == 0.0
```

运行测试：

```
python -m pytest test_reward.py -v
```

测试覆盖命中、思考链残留、未命中等场景。扩展维度后相应增加断言。

## 后续步骤

-   训练配置（超参、资源、数据源）见 [在线策略蒸馏训练配置](opd-training-config.md)
-   可观测（Tracing、指标面板）见 [在线策略蒸馏可观测配置](opd-observable-config.md)

## 常见问题

reward\_metrics 不显示

检查 `reward_score` 是否通过 pop 取出后单独赋给 `Reward.reward_score`，其余维度值是否均为 float。

评分为 0（coverage 不命中）

原生 Rollout parser 不执行，content 残留 thinking 与工具调用文本；需先 `strip_reasoning` 清理后，再按你定义的维度（如 `coverage`）判定，而非直接判原始 content。

teacher\_model 报错

常见原因：`teacher_model` 填了非百炼登记的模型 ID（如 HuggingFace 仓库名）。排查：改用百炼支持的模型 ID，完整列表与更多原因见 [训练配置常见问题](opd-training-config.md#opd-faq)。

ground\_truth 取不到（为空）

检查数据 JSONL 每条 `rollout_extra.solution` 是否有值。Reward 先从 `input.ground_truth` 取，缺失时回退到 `input.agent_output.rollout_extra.solution`；两者都空则评分为 0。

本地测试报 ModuleNotFoundError

确认 `functions/` 目录含 `__init__.py`（使目录成为可导入的 Python 包）；`classpath` 与文件路径对齐，如 `functions.reward.my_reward.MyRewardProcessor` 对应 `functions/reward/my_reward.py` 内的 `MyRewardProcessor` 类。
