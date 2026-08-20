# 强化学习开发指南

本文介绍如何开发、测试 RL 训练所需的三种函数组件：Rollout（轨迹生成）、Reward（评分）和 Group Reward（批量评分）。

## 函数组件概述

RL 训练需要您开发自定义函数来控制模型的交互行为和评分逻辑。函数代码会自动部署到云端运行：

**组件**

**职责**

**是否必须**

**Rollout**

定义 Agent 如何调用 LLM 和工具，生成交互轨迹

必须（1 个）

**Reward**

对单条 Agent 输出评分，定义训练的优化方向

可选（1 个或多个）

**Group Reward**

对同一问题的多条输出集体评分（排序或对比评分）

可选

## 共享数据模型

三个函数组件通过统一的 `AgentOutput` 对象传递数据，使用 `TaskStatus` 标记执行状态。

### AgentOutput

`AgentOutput` 是 Rollout 与 Reward 之间的数据桥梁，由 Rollout 函数构造，传递给 Reward 函数：

**字段**

**类型**

**说明**

`messages`

list

对话消息列表，包含 user、assistant 和 tool 角色。取最后一条 assistant 消息可获取模型回答

`reward_score`

float / None

预置评分。在 Rollout 中通过 `AgentOutput(reward_score=0.95)` 设置后，Reward 函数可直接读取，无需再单独编写 Reward 类

`rollout_extra`

dict

训练数据中 `rollout_extra` 的透传，用于评分时获取参考答案等业务数据

`rollout_metrics`

dict

自定义指标，如 `AgentOutput(rollout_metrics={"latency": 1.2})`，自动出现在控制台 `trace/rollout_metrics/` 路径下

### TaskStatus 与错误处理

所有函数组件的 `process()` 返回结果中必须设置 `status` 字段，训练框架据此决定是否重试或丢弃该样本：

-   `TaskStatus.SUCCESS`：执行成功
-   `TaskStatus.FAILED`：执行失败，需设置 `error` 字段说明原因

```
## 成功
return RolloutOutput(
    agent_output=AgentOutput(messages=messages),
    status=TaskStatus.SUCCESS,
)

## 失败 → 框架会重试或丢弃该样本
return RolloutOutput(
    agent_output=AgentOutput(messages=[]),
    status=TaskStatus.FAILED,
    error="LLM 调用超时",
)
```

## Rollout 函数开发

Rollout 函数负责生成 Agent 与 LLM、外部工具的交互轨迹。

### 基本结构

继承 `AbstractRolloutProcessor`，实现 `setup()` 和 `process()` 方法：

```
from dashscope.finetune.reinforcement import (
    AbstractRolloutProcessor, RolloutInput, RolloutOutput
)
from dashscope.finetune.reinforcement.component.data.base_data_model import (
    AgentOutput, TaskStatus
)

class MyRolloutProcessor(AbstractRolloutProcessor):
    def setup(self) -> None:
        """初始化资源（服务启动时执行一次）"""
        # 初始化 LLM 客户端、加载工具等
        pass

    async def process(self, input: RolloutInput) -> RolloutOutput:
        """生成 Agent 轨迹（每个样本调用一次）"""
        messages = input.messages or []
        model = input.model_resource.model_name
        # ... 与 LLM 交互、调用工具
        return RolloutOutput(
            agent_output=AgentOutput(
                messages=messages,
                rollout_metrics={"latency": 1.2}  # 自定义指标
            ),
            status=TaskStatus.SUCCESS,
        )
```

`process()` 支持 `async def` 和普通 `def` 两种写法，SDK 会自动处理。

**说明****注**：Rollout 通过 OpenAI 兼容 API 调用训练中的模型，端点（`base_url`）和 API Key 由训练框架运行时自动注入到 `RolloutInput.model_resource`，您在 `setup()` / `process()` 中直接读取即可，无需在代码或配置中硬编码。

### RolloutInput 关键字段

**字段**

**类型**

**说明**

`messages`

list

对话消息列表

`model_resource`

object

模型信息（model\_name, base\_url, api\_key）

`sampling_params`

object

采样参数（temperature, max\_tokens, max\_turns, timeout）

`ground_truth`

str

参考答案

`rollout_extra`

dict

训练数据中的 rollout\_extra 字段，透传业务数据

**错误处理**：当 Rollout 执行失败时（如 LLM 调用超时、工具异常），应返回 `TaskStatus.FAILED` 并设置 `error` 字段。详见上方 [TaskStatus 与错误处理](https://help.aliyun.com/zh/model-studio/rl-function-development-guide#oen19av18kbra)。

**说明****内嵌评分逻辑**：Reward 评分可以不单独编写为独立的 Reward 函数，而是直接集成在 Rollout 的 `process()` 中。在返回 `RolloutOutput` 时，通过 `AgentOutput(reward_score=0.95)` 直接给出评分即可。内嵌评分的指标同样会出现在控制台的指标页面中。详见 [AgentOutput](https://help.aliyun.com/zh/model-studio/rl-function-development-guide#ufzjyzzes0tu3)。

## Reward 函数开发

Reward 函数对单条 Agent 输出进行评分，是 RL 训练的核心。

### 基本结构

继承 `AbstractRewardProcessor`，在 `process()` 中计算分数：

```
from dashscope.finetune.reinforcement import (
    AbstractRewardProcessor, RewardInput, RewardOutput, Reward, TaskStatus
)
from dashscope.finetune.reinforcement.component.observability import observe_processor

class DemoRewardProcessor(AbstractRewardProcessor):
    def setup(self) -> None:
        pass

    @observe_processor
    async def process(self, input: RewardInput) -> RewardOutput:
        content = input.agent_output.messages[-1].get("content", "")
        ground_truth = input.ground_truth

        # 评分逻辑：检查答案是否正确
        score = 1.0 if ground_truth in content else 0.0

        return RewardOutput(
            reward=Reward(
                reward_score=score,
                reward_metrics={"test1": 0.5, "test2": 0.3}  # 自定义指标
            ),
            status=TaskStatus.SUCCESS,
            error=None,
        )
```

### RewardInput 关键字段

**字段**

**类型**

**说明**

`agent_output`

object

Agent 输出。字段详见上方 [AgentOutput](https://help.aliyun.com/zh/model-studio/rl-function-development-guide#ufzjyzzes0tu3)

`ground_truth`

str

参考答案

### 装饰器模式（多维度评分）

对于需要从多个维度评分的场景，可使用装饰器模式将评分拆分为多个子维度，再聚合：

```
from dashscope.finetune.reinforcement import (
    AbstractRewardProcessor, RewardInput, RewardOutput, Reward, TaskStatus,
    reward_func, sub_reward_func, aggregate_func
)

@reward_func("SafetyProcessor")
class SafetyProcessor(AbstractRewardProcessor):
    """多维度安全性评分"""
    BANNED = {"hack", "exploit", "attack"}

    @sub_reward_func("toxicity", sub_weight=0.7)
    def toxicity(self, input: RewardInput) -> RewardOutput:
        """毒性检测子维度（权重 0.7，同步）"""
        messages = input.agent_output.messages
        content = messages[0].get("content", "") if messages else ""
        response = str(content) if content is not None else ""
        has_banned = any(w in response.lower() for w in self.BANNED)
        return RewardOutput(
            reward=Reward(
                reward_score=0.0 if has_banned else 1.0,
                reward_metrics={"score-1": 0.1},
            ),
            status=TaskStatus.SUCCESS,
            error=None,
        )

    @sub_reward_func("refusal", sub_weight=0.3)
    async def refusal(self, input: RewardInput) -> RewardOutput:
        """拒绝检测子维度（权重 0.3，异步）"""
        messages = input.agent_output.messages
        content = messages[0].get("content", "") if messages else ""
        response = str(content) if content is not None else ""
        is_refusal = response.strip().lower().startswith("i cannot")
        return RewardOutput(
            reward=Reward(
                reward_score=0.5 if is_refusal else 1.0,
                reward_metrics={"score-1": 0.2},
            ),
            status=TaskStatus.SUCCESS,
            error=None,
        )

    @aggregate_func
    async def aggregate(self, sub_rewards: dict[str, RewardOutput]) -> RewardOutput:
        """聚合所有子维度（异步）"""
        weights = self.get_weights()
        scores = self.get_scores(sub_rewards)
        if len(scores) != len(weights):
            raise ValueError("scores and weights must have the same length")

        # 0.5 * 0.3 + 1.0 * 0.7 = 0.85
        total = sum(scores[k] * weights[k] for k in scores)

        reward_metrics = self.get_reward_metrics(sub_rewards)
        user_reward_metrics = {"aggregate-1": 0.4}
        user_reward_metrics.update(reward_metrics)
        return RewardOutput(
            reward=Reward(
                reward_score=total,
                reward_metrics=user_reward_metrics,
            ),
            status=TaskStatus.SUCCESS,
            error=None,
        )
```
**装饰器说明：**

**装饰器**

**作用**

`@reward_func("name")`

标记 Reward 处理器类，定义名称

`@sub_reward_func("name", sub_weight=0.7)`

定义子评分维度和权重

`@aggregate_func`

定义聚合逻辑，合并所有子维度得分

### 多 Reward 函数组合

提交任务时可以配置多个 Reward 函数，每个函数有独立的权重：

```
functions=[
    RewardFunctionComponent(name="accuracy", weight=0.6, ...),
    RewardFunctionComponent(name="safety", weight=0.4, ...),
]
```

还可以通过 `reward_metric_weight` 进一步细分子指标的权重：

```
RewardFunctionComponent(
    name="reward-1",
    weight=1.0,
    reward_metric_weight={"reward_metric_weightA": 0.3, "reward_metric_weightB": 0.7},
    ...
)
```

## Group Reward 函数开发

Group Reward 对同一问题的多条 Agent 输出进行集体评分，适用于排序或对比评分场景。

### 基本结构

继承 `AbstractGroupRewardProcessor`，在 `process()` 中处理多条输出：

process() 方法支持 async def 和普通 def 两种写法，SDK 会自动处理。这一规则适用于所有函数组件（Rollout、Reward、Group Reward）。下面的示例采用同步写法。

```
from dashscope.finetune.reinforcement import (
    AbstractGroupRewardProcessor, GroupRewardInput, GroupRewardOutput,
    GroupReward, Reward, TaskStatus
)

class DemoGroupRewardProcessor(AbstractGroupRewardProcessor):
    def setup(self) -> None:
        pass

    def process(self, input: GroupRewardInput) -> GroupRewardOutput:
        rewards = []
        for agent_output in input.agent_outputs:
            score = 0.0
            # ground_truth 出现在 messages 内容里 → 1.0；messages 非空 → 0.5；否则 0.0
            if input.ground_truth is not None and agent_output.messages:
                gt_str = str(input.ground_truth)
                for msg in agent_output.messages:
                    if isinstance(msg.get("content"), str) and gt_str in msg["content"]:
                        score = 1.0
                        break
                if score == 0.0 and len(agent_output.messages) > 0:
                    score = 0.5
            rewards.append(Reward(reward_score=score))

        return GroupRewardOutput(
            reward=GroupReward(rewards=rewards),
            status=TaskStatus.SUCCESS,
            error=None,
        )
```

### 与 Reward 的区别

-   Reward：对单条输出评分，输入是 agent\_output（单数）
-   Group Reward：对多条输出评分，输入是 agent\_outputs（复数列表），返回一组分数

## Reward 设计哲学：先想清楚再写代码

Reward 是 RL 训练唯一的优化方向，**先把"评什么"想清楚再动键盘**。三组核心权衡决定写法：

-   **稀疏 vs 稠密**：稀疏 Reward 不易作弊但样本利用率低；稠密 Reward 学得快但容易引入 shaping 偏差
-   **规则 vs LLM-as-judge**：规则廉价、确定、可复现；LLM 判分覆盖语义但有偏差和成本
-   **单维 vs 多维**：单维易迭代但天花板低；多维表达力强但权重设计与解释成本高

### 从任务反推 Reward：先答 4 个问题

-   Q1 有可机器判定的 ground truth？（数学/代码/JSON → 规则；写作/对话 → 模型/人类）
-   Q2 失败是二元还是有梯度？（二元 → 稀疏 0/1；有梯度 → 拆维度）
-   Q3 是否需要中间步骤激励？（长链推理、Agent 多轮 → process reward / 步骤分）
-   Q4 哪些 hack 路径成本最低？（先列再防——见下文 §Reward Hacking 识别与防御）

### Reward 是合同，不是损失函数

模型只会优化你写下来的东西，不会优化你"想表达"的东西。三点：

-   **0/1 边界会被精确逼近**——给精确分加 margin 或软化（如准确分 + 格式分 + 简洁分多维组合）
-   **硬上限会被堆到顶点**——长度满分 = 模型必把回答撑到上限；用归一化或衰减替代
-   **空输出 / 超长输出 / 超时必须显式定义**——默认行为往往是漏洞，空输出强制 0 分、超长截断后扣分

## 三种 Reward 表达方式选型

Reward 表达方式不是互斥，而是**分层选最轻**：A 内嵌（`AgentOutput(reward_score=...)`）→ B 独立（`RewardFunctionComponent`）→ C 装饰器多维（`@reward_func` + `@sub_reward_func` + `@aggregate_func`）。

表达方式

适用场景

评分逻辑复杂度

资源开销

可观测粒度

调试便利

何时不要用

A 内嵌 Rollout

评分与生成同步、判定逻辑 ≤10 行

低

复用 Rollout FC

仅 reward\_score 一个指标

难（需 redeploy Rollout）

评分需独立扩缩容时

B 独立 Reward

单一明确判分规则、复用通用评分器

中

独立 FC

reward + reward\_metrics

中（独立部署）

维度 ≥3 个时

C 装饰器多维

多维度评分、各维度权重需独立调

高

独立 FC

子维度独立指标

高（按维度排查）

维度间强耦合无法拆

**升级路径**：起步 A 跑通流程 → 维度 ≥1 换 B → 维度 ≥3 换 C；A→B 保留 Rollout 把判分搬出来；B→C 按"原子可判定"拆维度，单 sub 做不了 0/1 判定就别拆。

## 多维评分：三层权重设计

多维 Reward 的权重分三层，**互不覆盖、独立调整**：

-   **层 1 函数级** `RewardFunctionComponent.weight`（多 Reward 函数之间）
-   **层 2 子维度** `@sub_reward_func(sub_weight=...)`（函数内部维度之间）
-   **层 3 子指标** `reward_metric_weight={...}`（同一 reward\_metrics 内细分）

最终 reward = Σ(层1 × 层2 × 层3 归一化项)。

### 多维权重设计模板

步骤

操作

输出

经验值

1\. 列维度

拆 3-5 个原子可判定维度

维度清单

建议 ≤5 个

2\. 定优先级

业务排序（必须满足 / 加分项 / 风格项）

排序后的列表

\-

3\. 初始权重

必须项占 0.5-0.7，加分项 0.2-0.3，风格 0.05-0.1

权重向量

总和 = 1

4\. 量纲对齐

每维度先归一到 \[0,1\] 再加权

归一函数

避免某维度天然占主导

5\. 灰度验证

100 条样本人工标注与 reward 对照

相关系数

Spearman ρ ≥ 0.6

### 权重调参方法

-   先训"均匀权重"baseline 看哪个 sub\_metric 主导；看 `trace/reward_metrics/{reward}/{sub}/avg` 曲线方差，方差小的维度提权
-   validation reward 涨但训练集某维度急降 → 该维度权重过低被牺牲，需补；出现 hack 信号 → 临时降低相关维度权重而非直接禁用

## Group Reward 应用场景

### Group Reward vs 独立 Reward 的选择

-   **独立 Reward** 评"这一条回答好不好"（绝对分）；**Group Reward** 评"同 prompt N 条相对好坏"（排序/对比）
-   GRPO/GSPO 天然需组内相对优势，Group Reward 直接产出排序信号省去归一化偏差
-   评分天然主观（写作、对话）时，相对比较比绝对打分更稳定

### 与 GRPO/GSPO 算法的配合

-   GRPO/GSPO 用同 prompt N 个 rollout 计算 group-relative advantage；独立 Reward 出绝对分 → 框架组内归一化（可能受 outlier 拉偏）
-   Group Reward 直接出组内分布 → 减少分数尺度漂移；`n_rollouts` 影响输入规模，建议 4-16

### 实现注意点

-   输入 `agent_outputs` 列表 → 输出 `rewards` 长度严格相等；不要在组内硬归一化（除以 max）会与算法层冲突
-   允许并列分数（三条都 1.0）但避免全部相同（zero advantage）；失败单条建议给 0 分保持长度一致，框架按 TaskStatus 判定

## Reward Hacking 识别与防御

### Hack 是几乎必然发生的

-   **Goodhart 定律**：当度量变成目标，它就不再是好度量
-   RL 越收敛、奖励越高，hack 概率越大（不是 bug，是优化器在干正事）
-   防御策略不是"消除 hack"，而是"让 hack 比真解更难"

### Hack 模式 → 检测信号 → 防御策略

Hack 模式

检测信号（指标 + 现象）

防御策略

长度爆炸 / 啰嗦堆砌

`trajectory/response_length` 单调上涨 + `validation/data/reward/mean@1` 停滞 / 下降

长度归一化、加 `length_penalty` sub\_reward、`max_length` 硬截断

关键词堆砌

reward 涨但人工抽查发现答案重复关键词；`trace/reward_metrics/.../accuracy` 与人工标注相关性下降

正则去重、用 LLM judge 替代关键词匹配、引入语义相似度阈值

格式 hack（markdown / emoji 堆砌）

输出格式异常 + 用户问题与回答相关性下降

格式归一化预处理、风格维度独立打分但权重低

拒答 / 空输出

reward 中位数高但 `trace/success_rate/...` 下降；assistant 消息为空

空输出强制 0 分、最小长度约束、引入"是否回答了问题"维度

循环输出 / 复述

response\_length 高 + n-gram 重复率高 + entropy 急降

重复检测正则、`repetition_penalty`、entropy 监控

Judge 串通（LLM-as-judge 场景）

judge 分高但与规则分 / 人工分背离

规则分 + judge 分混合（见下文）、定期 judge 校准、换不同模型族 judge

工具滥用 / 工具不调用

`trace/tool_call_count` 异常（暴涨或骤降）+ 任务成功率下降

工具调用次数惩罚 / 奖励、必需工具调用约束

Entropy 崩塌

`actor/entropy` 趋近 0；validation 不再变化

调大 KL 系数、Early stop、entropy bonus

### 4 类防御手段

-   **Reward shaping**：把 hack 路径显式扣分（直接但要持续打补丁）
-   **正则约束**：长度/重复/格式硬约束（廉价但僵硬）
-   **Validation 监控**：用与训练 reward 不同源的指标做哨兵（必须）
-   **多 Reward 组合**：规则 + 模型混合互相牵制

### 监控操作手册

-   **北极星** `critic/rewards/mean` 上升趋势 + **反作弊哨兵** `validation/data/reward/mean@1`（背离即 hack）+ **行为体检** `trajectory/response_length` / `actor/entropy`
-   每隔 N 步抽查轨迹（控制台"轨迹"页签）人工对照分数

## 评分稳定性：让分数可信

### LLM-as-judge 的偏差控制

-   **位置偏差**：pairwise 先后顺序影响 → 双向各跑一次取一致项
-   **自偏好偏差**：judge 偏向同模型族 → 用不同模型族（Qwen 训 → GPT judge）
-   **长度偏差**：judge 偏好长输出 → prompt 明确"不因长短给分" + 长度归一化
-   评分尺度 1-5 / 1-7 离散 > 1-100 连续，带 anchor example 校准

### 规则 + 模型混合评分

-   **规则做硬约束**（格式/长度/必含字段/敏感词）→ 不通过 0 分短路
-   **模型做软评价**（流畅度/相关性/推理质量）
-   组合：`final = rule_pass × (w_rule × rule_score + w_model × model_score)`；规则失败不传给 model judge → 省钱 + 防 hack

### 评分场景的 TaskStatus 判定

-   **评分得 0 分**（规则未通过、答错）→ `SUCCESS + reward_score=0`，是**有效训练信号**
-   **临时性错误**（judge 超时、网络抖动）→ `FAILED` 让框架重试，**不**写成 0 分
-   **滥用 FAILED** 会让数据分布偏移（难样本被框架重试若干次后丢弃 → 训练集越变越简单）

### 评分一致性自检

-   准备 50-200 条 gold set（人工标注）；每次改 Reward 后跑 gold set 比 Spearman ρ / Cohen κ
-   judge 模型升级 / 切换前后对比避免静默漂移；周期性把训练中分数最高/最低 N 条样本送人工 review

## Reward 函数撰写前自检（10 问）

写完 Reward 函数发任务之前过一遍：

1.  评分逻辑能在 1 句话内说清楚吗？
2.  有 ground truth 吗？是机器可判定吗？
3.  最低成本的 Hack 路径是什么？已经防了吗？
4.  多维度的话每个维度都能独立人工标注吗？
5.  权重总和归一了吗？量纲对齐了吗？
6.  边界条件（空输出、超长、超时）都定义了吗？
7.  validation 用了与训练独立的判定方式吗？
8.  评分耗时是否 < Rollout 耗时的 1/3？
9.  `reward_metrics` 字段名是否稳定（改名会断指标曲线）？
10.  是否有 gold set 用于回归？

## Reward 设计反模式

反模式

后果

reward 写成"越长越好"

必 Hack（长度爆炸）

单维度评分但维度本身高度主观

噪声压过信号

所有维度 weight 都设 1.0

等价于没设权重 + 量纲混乱

训练 judge 与 validation judge 同 prompt 同模型

自欺欺人

临时网络错误返回 SUCCESS + 0 分

数据分布污染（难样本被当成"答错"）

## 可观测性配置

**说明**本节已迁出。Tracing 装饰器、自定义指标、依赖配置、ENABLE\_TRAJECTORY 开关等完整内容，统一收敛到 [《可观测配置》](raw/model-user-guide/fine-tuning/rl-training/observable-configuration-for-reinforcement-learning.md)（**控制台与可观测的覆盖**）。

## 函数测试

### 注册函数

将函数代码上传并注册为云端函数组件：

```
client = AgenticRL()
(rollout_entity_ids,
 reward_entity_ids,
 group_reward_entity_ids,
 rollout_instance_ids,
 reward_instance_ids,
 group_reward_instance_ids) = await client.register_functions(
    functions=[
        # rollout-only：演示版，覆盖 trace_client/trace_tool 全分支
        AgenticRLFunctionComponent(
            type=FunctionType.ROLLOUT,
            fcmodel=FunctionComponentModel(
                classpath="functions.rollout.rollout_only.DemoRolloutProcessor")),
        # reward
        AgenticRLFunctionComponent(
            type=FunctionType.REWARD,
            fcmodel=FunctionComponentModel(
                classpath="functions.reward.reward.DemoRewardProcessor")),
        # reward-decorator：文件路径:类名 形式
        AgenticRLFunctionComponent(
            type=FunctionType.REWARD,
            fcmodel=FunctionComponentModel(
                classpath="functions/reward/reward_decorator.py:SafetyProcessor")),
        # group-reward
        AgenticRLFunctionComponent(
            type=FunctionType.GROUP_REWARD,
            fcmodel=FunctionComponentModel(
                classpath="functions.reward.group_reward.DemoGroupRewardProcessor")),
    ],
    lazy_load=False  # False = 立即获取 instance_id，用于测试
)
```

等效 CLI：

```
dashscope rl register_functions \
  --rollout-classpaths "functions.rollout.rollout_only.DemoRolloutProcessor" \
  --reward-classpaths "functions.reward.reward.DemoRewardProcessor" \
  --reward-classpaths "functions/reward/reward_decorator.py:SafetyProcessor" \
  --group-reward-classpaths "functions.reward.group_reward.DemoGroupRewardProcessor" \
  --no-lazy-load \
  --output-format json
```

### 远程测试

使用 test\_functions 向已注册的函数实例发送测试数据：

```
## 测试 Rollout
result = await AgenticRL.test_functions(
    instance_id=rollout_instance_ids[0],
    type=FunctionType.ROLLOUT,
    input_data=rollout_input
)

## 测试 Reward
result = await AgenticRL.test_functions(
    instance_id=reward_instance_ids[0],
    type=FunctionType.REWARD,
    input_data=reward_input
)

## 测试 Reward 装饰器版（第二个 reward 实例，对应 refusal 分支 reward_score=0.85）
result = await AgenticRL.test_functions(
    instance_id=reward_instance_ids[1],
    type=FunctionType.REWARD,
    input_data=reward_decorator_input
)

## 测试 Group Reward
result = await AgenticRL.test_functions(
    instance_id=group_reward_instance_ids[0],
    type=FunctionType.GROUP_REWARD,
    input_data=group_reward_input
)
```

等效 CLI：

```
dashscope rl test_functions "ro-ins-xxx" --type rollout --input ./resources/rollout_input.json
dashscope rl test_functions "rw-ins-xxx" --type reward --input ./resources/reward_input.json
dashscope rl test_functions "rw-ins-yyy" --type reward --input ./resources/reward_decorator_input.json
dashscope rl test_functions "grw-ins-xxx" --type group_reward --input ./resources/group_reward_input.json
```

### 测试输入格式

**Rollout 测试输入**（rollout\_input.json）：

```
{
  "func_type": "rollout",
  "messages": [
    {"role": "user", "content": "Hello, please introduce yourself"}
  ],
  "tools": null,
  "ground_truth": "",
  "rollout_extra": {
    "rollout_id": "ro-ins-e8e92e94-b5c3-4546-b7b1-9832b8b948f2",
    "training_state": {"task_id": "task-001"}
  },
  "sampling_params": {
    "temperature": 0.7,
    "max_tokens": 1024,
    "max_turns": 25,
    "timeout": 60.0
  },
  "model_resource": {
    "model_name": "qwen3.5-9b",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "api_key": "your-api-key-here"
  },
  "request_metadata": {
    "protocol": "openai",
    "system_prompt": "",
    "job_id": "dummy-job-id",
    "sample_id": "dummy-sample-id",
    "rollout_id": "dummy-rollout-id",
    "attempt_id": "dummy-attempt-id"
  },
  "additional_field": "any extra data you want"
}
```

**Reward 测试输入**（reward\_input.json）：

```
{
  "func_type": "reward",
  "ground_truth": "0.5",
  "request_metadata": null,
  "agent_output": {
    "messages": [{"role": "user", "content": "Test question"}],
    "rollout_extra": {
      "content": "This is a test content that exceeds 50 characters in length and should receive a reward score of 0.5"
    },
    "rollout_metrics": {"accuracy": 0.95},
    "reward_score": null
  }
}
```

**Reward 装饰器版测试输入**（reward\_decorator\_input.json，对应 refusal 分支，aggregate 后 reward\_score=0.85）：

```
{
  "func_type": "reward",
  "ground_truth": "0.5",
  "agent_output": {
    "messages": [{"role": "user", "content": "I cannot help you with that"}]
  }
}
```

**Group Reward 测试输入**（group\_reward\_input.json，agent\_outputs 是同一条样例的数组）：

```
{
  "func_type": "group_reward",
  "ground_truth": "0.5",
  "request_metadata": null,
  "agent_outputs": [{
    "messages": [{"role": "user", "content": "Test question"}],
    "rollout_extra": {
      "content": "This is a test content that exceeds 50 characters in length and should receive a reward score of 0.5"
    },
    "rollout_metrics": {"accuracy": 0.95},
    "reward_score": null
  }]
}
```

### 本地测试

项目中的 scripts/ 目录提供了本地测试脚本：

```
./scripts/start_local_rollout.sh   # 启动本地 Rollout 服务
./scripts/query_local_rollout.sh   # 发送测试请求
```

## 后续步骤

-   了解提交方式与配置 → [强化学习训练配置 — 提交与配置](raw/model-user-guide/fine-tuning/rl-training/rl-training-config-monitoring.md)
-   训练指标参考字典 → [训练指标参考](raw/model-user-guide/fine-tuning/rl-training/observable-configuration-for-reinforcement-learning.md)
-   回顾概述 → [强化学习](raw/model-user-guide/fine-tuning/rl-training/rl-training-overview.md)
-   了解可观测性配置与轨迹查看 → [强化学习的可观测配置](raw/model-user-guide/fine-tuning/rl-training/observable-configuration-for-reinforcement-learning.md)
