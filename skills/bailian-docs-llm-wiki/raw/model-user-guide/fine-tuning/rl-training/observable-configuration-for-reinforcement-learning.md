# 强化学习的可观测配置与指标参考

## 概述

强化学习训练基于 **OpenTelemetry** 实现了Tracing。您只需在函数代码中添加少量装饰器和包装调用，训练过程中的每一次 LLM 调用、每一次工具调用、每一个评分细节都会自动记录，并导出到 **ARMS（应用实时监控服务）**，在百炼控制台可视化展示。

本篇以 _agentic-rl-example_ 项目（CalcX 计算器场景）为主线，演示从零配置到控制台查看效果的完整流程，并提供指标参考字典、问题排查决策、FAILED 排查流程。训练提交与超参配置请参见 [强化学习训练配置 — 提交与配置](raw/model-user-guide/fine-tuning/rl-training/rl-training-config-monitoring.md)。

## 接入 Tracing

以下以 agentic-rl-example 的 `CalcXRolloutProcessor` 为例，3 步完成 Tracing 接入。

### Step 1：添加依赖

在项目根目录的 `requirements.txt` 中添加以下 OpenTelemetry 相关依赖：

```
opentelemetry-api==1.41.1
opentelemetry-sdk==1.41.1
opentelemetry-exporter-otlp-proto-http==1.41.1
opentelemetry-processor-baggage==0.62b1
loongsuite-util-genai==0.4.0
```

**说明**`dashscope`、`fastapi`、`uvicorn`、`pyyaml` 已在运行环境中预装；如需固定版本也可在 requirements.txt 中声明。

### Step 2：添加观测代码

代码改动集中在 5 个装饰器/函数。它们会自动嵌套，形成完整的调用链：

```
[ENTRY: ROLLOUT] @observe_processor          ← Rollout 处理器入口
├── [LLM] trace_client / @observe_llm        ← LLM 调用
│   └── (OpenAI / LangChain / DashScope API)
├── [TOOL] trace_tool / @observe_tool        ← 工具调用
│   ├── tool: calculator (MCP)
│   └── tool: response_scorer (自定义)
└── [custom] rollout_metrics                 ← Rollout 自定义指标

[ENTRY: REWARD] @observe_processor           ← Reward 处理器入口
├── [LLM] trace_client / @observe_llm        ← LLM 调用（评分用）
├── [TOOL] trace_tool / @observe_tool        ← 工具调用
└── [custom] reward_metrics                  ← Reward 自定义指标
```

#### @observe\_processor — 追踪处理器入口

加在 `process()` 方法上，创建顶层 ENTRY Span。SDK 根据父类自动识别类型：继承 `AbstractRolloutProcessor` → ROLLOUT 类型，继承 `AbstractRewardProcessor` → REWARD 类型。自动记录每次调用的输入、输出、耗时、成功/失败状态。

**Rollout 侧（**`functions/rollout/rollout.py`）：

```
from dashscope.finetune.reinforcement.component.observability import (
    observe_processor
)

class CalcXRolloutProcessor(AbstractRolloutProcessor):
    @observe_processor  # Span 类型 = ROLLOUT
    async def process(self, input: RolloutInput) -> RolloutOutput:
        await self._async_setup()
        return await self._async_process(input)
```

**Reward 侧（**`functions/reward/reward.py`）：

```
class DemoRewardProcessor(AbstractRewardProcessor):
    @observe_processor  # Span 类型 = REWARD
    async def process(self, input: RewardInput) -> RewardOutput:
        messages = input.agent_output.messages
        content = messages[-1].get("content", "") if messages else ""
        score = await evaluate(content, input.ground_truth)
        return RewardOutput(
            reward=Reward(
                reward_score=score,
                reward_metrics={"test1": 0.5, "test2": 0.3}
            ),
            status=TaskStatus.SUCCESS,
            error=None,
        )
```

#### trace\_client() — 追踪 LLM 客户端

在初始化方法中调用，包装 LLM 客户端实例。之后该客户端的所有 LLM 请求都会自动产生 LLM Span，记录模型名、请求内容、Token 用量、延迟等。

**支持的客户端类型（鸭子类型自动检测）：**

-   OpenAI 客户端（`AsyncOpenAI` / `OpenAI`）
-   OpenAI completions 资源（`.chat.completions`）
-   LangChain ChatOpenAI 等类（通过 `.client` / `.async_client`）
-   DashScope Generation 类（传入类本身，非实例）

**示例（**`functions/rollout/rollout.py`）：

```
from langchain_openai import ChatOpenAI
from dashscope.finetune.reinforcement.component.observability import (
    trace_client
)

class CalcXRolloutProcessor(AbstractRolloutProcessor):
    def _build_llm(self, input: RolloutInput) -> ChatOpenAI:
        resource = input.model_resource
        params = input.sampling_params or {}
        # api_key 来自 input.model_resource.api_key（兼容 SecretStr）
        api_key = (
            resource.api_key.get_secret_value()
            if hasattr(resource.api_key, "get_secret_value")
            else resource.api_key
        )
        llm = ChatOpenAI(
            model=resource.model_name,
            openai_api_key=api_key,
            openai_api_base=resource.base_url,
            temperature=params.get("temperature", 0.7),
            max_tokens=params.get("max_tokens", 2048),
            request_timeout=params.get("timeout", 60.0),
            extra_body={"enable_thinking": params.get("enable_thinking", False)},
            streaming=False,
        )
        trace_client(llm)  # 包装后自动追踪所有 LLM 调用
        return llm
```

#### trace\_tool() — 追踪工具调用

在获取工具实例后调用，包装工具对象。之后每次工具调用都会产生 TOOL Span，记录工具名、参数、返回值、延迟。

**支持的输入格式：**

-   单个 LangChain BaseTool
-   列表 / 元组 / 字典（自动遍历）
-   LangGraph ToolNode（自动展开 `.tools_by_name`）
-   MCP 工具（自动检测，provider 设为 "mcp"）
-   自定义 provider（`trace_tool(tool, provider="my-plugin")`）

**示例（**`functions/rollout/rollout.py`）：

```
from dashscope.finetune.reinforcement.component.observability import (
    trace_tool
)

class CalcXRolloutProcessor(AbstractRolloutProcessor):
    def _get_mcp_servers(self) -> dict:
        return {
            "calculator": {
                "transport": "sse",
                "url": "http://localhost:10086/sse",
            },
        }

    async def _init_resources_async(self):
        client = MultiServerMCPClient(self._get_mcp_servers())
        tools = await client.get_tools()
        trace_tool(tools)  # 必须在 get_tools() 之后调用
```

**警告****MCP 特别注意：**MCP Server 和 Client 运行在不同进程中。Server 端的 `@observe_tool` 对 Client 端**无效**。必须在 Client 端调用 `get_tools()` 之后，对返回的工具列表执行 `trace_tool(tools)`。

#### @observe\_llm — 自定义 LLM 函数

当 `trace_client()` 无法自动检测您的 LLM 客户端时，用此装饰器手动标记 LLM 调用函数。

**签名要求：**函数必须包含 `*` 后的关键字参数 `model` 和 `messages`。

**示例（**`functions/rollout/rollout_only.py`，演示覆盖 trace 分支）：

```
from dashscope.finetune.reinforcement.component.observability import (
    observe_llm
)

class DemoRolloutProcessor(AbstractRolloutProcessor):
    @observe_llm  # 标记为 LLM Span
    async def _call_llm(
        self,
        *,
        messages: List[Dict],
        model: str,
    ) -> Any:
        # 自定义 LLM 调用逻辑
        ...
```

#### @observe\_tool — 自定义工具函数

当 `trace_tool()` 无法自动检测您的工具时（如普通 Python 函数充当工具），用此装饰器手动标记。可通过 `name` 参数自定义 Span 名称。

**示例（**`functions/rollout/rollout_only.py`，演示覆盖 trace 分支）：

```
from dashscope.finetune.reinforcement.component.observability import (
    observe_tool
)

class DemoRolloutProcessor(AbstractRolloutProcessor):
    @observe_tool(name="response_scorer")  # 标记为 TOOL Span
    def _score_response(self, *, messages: List[Dict]) -> float:
        # 自定义评分逻辑（如调用外部 grader 或本地 reward 模型）
        ...

    @observe_tool(name="trace_tool_tester")
    async def _call_tools(self) -> Dict[str, Any]:
        # 调用各类工具并记录 Tool Span
        ...
```

### Step 3：提交任务

提交任务时，Runtime 的 `env` 字段留空即可——Tracing **默认开启**：

```
from dashscope.finetune.agentic_rl import AgenticRL
from dashscope.finetune.reinforcement import (
    RolloutFunctionComponent, RewardFunctionComponent,
    FunctionComponentModel, FunctionComponentRuntime
)

client = AgenticRL()

rollout_runtime = FunctionComponentRuntime(
    cpu=2, memory_size=4096, disk_size=512,
    concurrency=30, capacity=30,
    min_capacity=30, max_capacity=60,
    memory_scale_threshold=0.6,
    concurrency_scale_threshold=0.6,
    env={}  # 留空 = 默认开启 Tracing
)

reward_runtime = FunctionComponentRuntime(
    cpu=2, memory_size=4096, disk_size=512,
    concurrency=30, capacity=30,
    min_capacity=30, max_capacity=60,
    memory_scale_threshold=0.6,
    concurrency_scale_threshold=0.6,
    env={}
)

result = await client.run(
    model="qwen3.5-9b",
    functions=[
        RolloutFunctionComponent(
            name="rollout-1",
            fcmodel=FunctionComponentModel(
                classpath="functions.rollout.rollout.CalcXRolloutProcessor"),
            runtime=rollout_runtime,
        ),
        RewardFunctionComponent(
            name="reward-1",
            weight=1.0,
            fcmodel=FunctionComponentModel(
                classpath="functions.reward.reward.DemoRewardProcessor"),
            runtime=reward_runtime,
        ),
    ],
    ...
)
```

**说明****如需关闭 Tracing**（节省成本），在 `env` 中设置 `{"ENABLE_TRAJECTORY": "false"}` 即可。关闭后 Actor/Critic/Perf 等系统指标不受影响，仅 Tracing 数据停止采集。

### Tracing 性能与成本权衡

#### 数据链路与成本来源

-   **数据流**：函数代码（三个核心装饰器）→ OpenTelemetry SDK → ARMS → 控制台轨迹/指标页签
-   **成本来源**：ARMS Span 存储（按量计费）+ 函数侧少量 CPU/网络开销 + 训练延迟少量增加

#### 开发期 vs 大规模训练的开关策略

阶段

Tracing 状态

采集数据

不采集数据

成本影响

开发 / 小批量调试

**全开**

全部（轨迹 + Reward 分析 + 工具调用 + 系统指标）

—

低

灰度 / 发布前确认

**保留**

全部

—

中

大规模正式训练（9B × 数万条 × 多 epoch）

**可关闭**

actor/critic/trajectory/perf/timing 系统指标

轨迹回放 / 工具调用详情 / 自定义 metrics 在 trace/ 下的曲线

显著降低

关闭命令：`runtime.env = {"ENABLE_TRAJECTORY": "false"}`。

#### 自定义指标的成本治理

-   `reward_metrics` / `rollout_metrics` 数量与基数（cardinality）影响 ARMS 存储
-   **避免高基数字段**（user\_id / request\_id）当指标 key
-   关键指标 ≤10 个，不留临时调试指标
-   `@sub_reward_func` 子维度合并后落到对应 Reward 函数的 `reward_metrics` 下，路径可控

## 自定义指标

在代码中通过以下入口定义的 key-value 指标，会自动出现在控制台**指标**页签的 `trace/` 分组和**Reward 分析**页面：

**入口**

**代码位置**

**控制台路径**

reward\_metrics

`Reward(reward_metrics={"acc": 0.8})`

`trace/reward_metrics/{reward-name}/acc/{avg,sum}`

rollout\_metrics

`AgentOutput(rollout_metrics={"latency": 1.2})`

`trace/rollout_metrics/latency/{avg,sum}`

子维度评分

`@sub_reward_func("toxicity")` 内返回的 reward\_metrics

合并到对应 Reward 函数的 `reward_metrics` 中

**多 Reward 函数场景：**通过 `RewardFunctionComponent(name="reward-1")` 为每个 Reward 函数设置唯一名称，在指标路径中区分（`trace/reward_metrics/reward-1/...`）。还可以通过 `reward_metric_weight` 细分子指标在综合评分中的权重。

## 控制台查看效果

训练开始后，在百炼控制台进入**模型调优**页面，点击任务名称进入详情，即可看到观测数据。以下说明"您在代码中做了什么 → 在控制台看到什么"的对应关系。

任务详情包含以下 5 个页签，按"先看进度 → 再看行为 → 出问题再下钻"顺序使用：

页签

主要回答

何时使用

详情

任务进度与状态

任何时候，先看

轨迹

模型实际做了什么、得分为何

验证模型行为、归因低分样本

指标

训练定量趋势

看曲线判断收敛性、发现拐点

产出

Checkpoint 列表与发布

训练完成后选模型

日志

stdout / stderr / 报错堆栈

FAILED 时排查

### 详情页签

查看任务基本信息：任务 ID、训练模型、训练方法（RL-全参训练）、数据配置等。**重点关注任务状态：**

-   **PENDING**：任务排队中，等待资源分配
-   **RUNNING**：训练进行中，可切换到其他页签查看实时数据
-   **SUCCESS**：训练完成，切换到**产出**页签发布模型
-   **FAILED**：训练失败，查看**日志**页签或通过 SDK / CLI 获取日志（`AgenticRL.logs(job_id="ft-xxx")` / `dashscope rl logs "ft-xxx"`）

### 轨迹详情 — 对应 @observe\_processor

在**轨迹**页签的**轨迹详情**子页面，可以看到每次 Rollout 的完整交互过程：

-   **轨迹列表：**展示所有采样轨迹，支持按 Sample ID / 轨迹 ID / Epoch / Step 筛选
-   **对话过程：**完整的多轮交互（user → assistant → tool\_call → tool\_result → assistant），直观看到模型的推理链
-   **Reward 分数：**每个 Step 显示对应的 Reward 分数和状态（SUCCESS/FAILED）

关注：工具调用是否正确？对话轮次是否合理？模型是否在重复无效操作？

### 工具调用分析 — 对应 trace\_tool / @observe\_tool

在**轨迹**页签的**工具调用分析**子页面，可以查看：

-   **工具调用记录：**工具名称、调用参数、返回结果和耗时
-   **Tracing 子页签：**每条轨迹的 Span 树，可展开查看每次工具调用和 LLM 请求的完整详情

**典型用途：**排查 Agent 的工具调用失败——哪个工具报错？参数传递是否正确？耗时是否过长？

### Reward 分析 — 对应 reward\_metrics

**概念定义**：

-   **Sample**：训练数据中一条原始样本（一道题、一条指令、一个 prompt）。
-   **Trajectory**：同一 Sample 在 `n_rollouts` 次采样下产生的具体一条交互轨迹。
-   关系：一条 Sample → N 条 Trajectory（N = `n_rollouts`）。

在**轨迹**页签的**Reward 分析**子页面，从三个维度评估训练效果：

-   **Step 维度：**选择训练 Step，查看该 Step 下所有样本的 Reward 聚合（平均分、成功率、趋势图），判断整体训练趋势
-   **Sample 维度：**选择 Sample ID，查看同一样本在不同轨迹中的 Reward 对比，发现问题样本
-   **Trajectory 维度：**查看单条轨迹的每个评分维度原始分，用于归因分析

### 指标页签 — 对应 rollout\_metrics / reward\_metrics

在**指标**页签的 `trace/` 分组，可以看到您在代码中定义的所有自定义指标的聚合曲线（avg / sum）。

完整 7 组 113+ 个指标见本篇下方 §训练指标参考；看到指标异常如何归因 → 本篇 §问题排查决策树（P1~P9）。

### 产出页签

训练完成后，在**产出**页签中可以看到 Checkpoint 列表，每行包含 Checkpoint ID、发布状态和剩余保存时间。

1.  选择目标 Checkpoint，点击**发布**按钮
2.  等待发布完成（状态从"待发布"变为"已发布"）
3.  发布后即可通过模型名称在 API 中调用

训练完成不等于训练成功——必须看 `validation/data/reward/mean@1` 选最佳 Checkpoint，不一定是最后一个。Checkpoint 保留策略 / 续训 / SFT→DPO→RL 衔接路径见《强化学习训练配置 — 提交与配置》§续训、Checkpoint 与渐进式训练。

### 日志页签

在**日志**页签查看训练运行日志，也可通过 SDK / CLI 获取：`AgenticRL.logs(job_id="ft-xxx", lines=100)` 或 `dashscope rl logs "ft-xxx" --lines 100`。

FAILED 任务排查步骤见本篇 §常见问题 → 训练期 FAILED 排查流程。

## 训练指标参考

### 关键指标速查

以下指标按监控维度组织，帮助快速判断训练是否健康：

**监控维度**

**关键指标**

**核心说明**

**健康判据**

**任务表现与泛化**

`critic/rewards/mean`

北极星指标。反映模型在当前训练批次上获得的平均收益，即模型是否在“学习有效策略”

**健康：**稳步上升，直至收敛。

`validation/data/reward/mean@1`

泛化能力指标。衡量模型在新 Prompt 上首次输出的质量，体现真实泛化能力

**健康：**与训练奖励趋势一致地稳步上升。

**训练稳定性**

`actor/entropy`

衡量策略输出的不确定性，平衡探索与利用

**健康：**训练初期较高，随后缓慢下降，保持在非零水平。

`actor/ppo_kl`

当前策略相对于初始模型的偏离程度

**健康：**维持在 0.01 - 0.05 范围内。

`actor/pg_clipfrac`

重要性采样裁剪触发率，反映策略漂移速度

**健康：**通常保持在 1% 以下。

**系统效率与边界**

`trajectory/response_length_non_aborted/mean`

未被截断的有效回复的平均 Token 数

**健康：**与任务需求相符。

`trajectory/.../clip_ratio`

Prompt 或 Response 达到最大长度被强制截断的比例

**健康：**极低，接近 0%。

`timing/s/step`

完整 RL step（生成 + 评估 + 更新）的总耗时

**健康：**相对平稳。

### 排查思维框架

#### 指标分层解读法

-   **必看**（日常体检 8-10 个）：北极星 + 三个核心指标 + 截断率 + 单步耗时（健康判据已在关键指标速查表）
-   **选看**（按场景）：Agent 看 `trace/num_llm_calls` / `trajectory/num_turns`；长文看 length 系列
-   **排错下钻**：timing 子项 / fully\_async 队列 / critic 分布 max/min

控制台 5 个页签的使用场景见上方「控制台查看效果」节的页签速查表。

### 问题排查决策树（P1~P9）

指标页签看到异常曲线 → 对照本节定位对应问题 → 按建议调参（参考《强化学习训练配置 — 提交与配置》§调参决策表）。

#### P1 不收敛 & P2 震荡

-   **P1 主信号**：`critic/rewards/mean` 长平台 + `actor/ppo_kl ≈ 0` + `actor/grad_norm` 极小
-   **P1 根因**：lr 太小 / Reward 恒返回相同值 / 数据不足
-   **P2 主信号**：`rewards/mean` 大幅震荡 + `grad_norm` 飙升 + `pg_clipfrac` >5%
-   **P2 根因**：lr 过大 / batch 过小 / advantage 方差未归一化

#### P3 KL 爆炸 & P4 熵骤降（模式崩溃）

-   **P3 主信号**：`actor/ppo_kl` 持续 >0.1 + `pg_clipfrac` 同步升 + 轨迹乱码/重复
-   **P3 处置建议**：`kl_loss_coef` ↑（0.001 → 0.01）+ lr ↓ + `ppo_mini_batch_size` ↓
-   **P4 主信号**：`actor/entropy` 几十步内贴 0 + `rewards/mean` 虚假上升 + Sample 维度同模板复述
-   **P4 根因**：Reward 单模式过度奖励 / KL 太小 / 温度过低

#### P5 Reward Hacking & P6 验证集崩塌

-   **P5 主信号**：训练 reward 涨 + validation 停 / 跌 + `response_length_non_aborted/mean` 线性暴涨 + 某 `reward_metrics` 子维独占增益
-   **P5 归因路径**：指标异常 → 轨迹 Sample 抽样 → 看 assistant 是否堆字数 / 抄题面 / 借助工具钻 Reward 漏洞（详见《强化学习开发指南》§Reward Hacking 识别与防御）
-   **P6 主信号**：`validation/data/reward/mean@1` 出现下行拐点而训练 reward 仍升
-   **P6 处置建议**：早停（在产出页签选取较早的 Checkpoint）+ KL 约束 ↑ + 扩验证集

#### P7 训练变慢 & P8 输出乱码 & P9 截断率高

-   **P7 主信号**：`timing/s/step` 突增
-   **P7 下钻**：`rollout/agent_loop_latency` / `update_actor`；根因 response\_length 上涨 / FC 扩容滞后（看 fully\_async 队列）/ 工具延迟
-   **P8 主信号**：轨迹乱码 / 非自然语言，通常 P3 KL 已爆 → 与 P3 联动处置
-   **P9 主信号**：`trajectory/response_length/clip_ratio` 或 `prompt_length/clip_ratio` 高
-   **P9 处置建议**：`max_length` ↑ 或缩 prompt；同时检查 Reward 是否变相鼓励长输出

### 控制台三维度归因

#### Step / Sample / Trajectory 三维度的协同用法

**标准路径**：指标页签看到拐点 → Step 锁定"哪段训练坏了"（趋势拐点）→ Sample 找"哪些样本拉偏均值" → Trajectory 看"这一条推理链 / 工具调用细节" → 回到代码改 Reward / 数据。

#### 工具调用分析与 Tracing Span 树

-   **工具调用分析**：工具名 / 参数 / 返回 / 耗时——排查 Agent 工具失败必看
-   **Tracing 子页签**给每条轨迹 Span 树（ENTRY:ROLLOUT → LLM → TOOL → REWARD）
-   **典型用法**：Reward 突然变低 → 看某工具是否开始报错 / MCP server 是否不可用
-   **注意**：Server 端 `@observe_tool` 对 Client 无效，必须 Client 端 `trace_tool(tools)`

#### 自定义指标（rollout\_metrics / reward\_metrics）的归因价值

-   系统指标只告诉你"坏了"，**自定义指标告诉你"哪一维度坏了"**
-   **命名规范建议**：按业务子维度命名（accuracy / format\_score / tool\_success\_rate / answer\_length）
-   **多 Reward 函数场景**：通过 `RewardFunctionComponent(name=...)` 区分；通过 `reward_metric_weight` 调权重
-   **反模式**：把日志或调试信息塞进 metrics，导致 cardinality 爆炸

### 日志 / 指标 / 轨迹 / Tracing 协同排查

四类观测源各回答不同问题：**日志**→"何时失败、报错堆栈"、**指标**→"是不是 / 有多严重"、**轨迹**→"为什么 / 哪条样本"、**Tracing**→"哪段慢 / 哪个外部依赖坏了"。按问题类型选观测源：

问题类型

主用

次用

不必看

训练发散

指标

轨迹

日志

任务 FAILED

日志

指标

轨迹

Reward 不涨

指标 → 轨迹

reward\_metrics

日志

工具调用错

Tracing

日志

—

训练变慢

指标 timing

Tracing

—

输出质量差

轨迹

reward\_metrics

—

#### 何时该跳出控制台

-   怀疑 Reward 实现 → 用 `test_functions` 本地复现
-   怀疑数据 → 抽 JSONL 看 `rollout_extra`
-   怀疑超参 → 回提交脚本对照《强化学习训练配置 — 提交与配置》

### 指标分组总览

训练过程中产出的指标按前缀分为以下分组，各分组的详细指标说明见下方折叠面板：

**分组前缀**

**指标数**

**类型**

**说明**

**actor/**

8

系统

PPO 策略网络指标：损失、熵、KL 散度、裁剪率、梯度范数、学习率

**critic/**

12

系统

奖励与价值评估：score / rewards / advantages / returns 的 mean / max / min

**trajectory/**

15

系统

轨迹统计：回复长度、Prompt 长度、截断率、中止率、对话轮次

**trace/**

40+

**混合**

可观测性指标：epoch、LLM 调用次数、成功率、自定义 reward\_metrics 和 rollout\_metrics

**timing/**

11

系统

耗时分析：Trainer 各阶段耗时（秒）、Rollout 耗时、每 Token 耗时（毫秒）

**perf/**

3

系统

性能总览：Token 总数、每步耗时、每 GPU 吞吐量

**fully\_async/**

24

系统

异步训练调度：队列状态、参数版本、staleness 统计、处理耗时分布

### 指标分组详情

点击展开各分组的完整指标列表：

actor/ — 策略网络指标（8 个）

**指标**

**含义**

`actor/loss`

总 loss（pg + entropy + ...）

`actor/pg_loss`

Policy Gradient loss

`actor/entropy`

当前策略的平均 token 熵，反映探索程度

`actor/ppo_kl`

当前策略相对于初始 Policy（SFT 模型）的 KL 散度

`actor/pg_clipfrac`

重要性采样裁剪触发率，反映策略漂移速度

`actor/pg_clipfrac_lower`

Dual-clip 下方裁剪触发率（未开启 dual-clip 时恒为 0）

`actor/grad_norm`

梯度范数

`actor/lr`

当前学习率

critic/ — 奖励与价值评估（12 个）

**指标**

**含义**

`critic/score/{mean,max,min}`

原始 reward score 统计（扣除 KL 前）

`critic/rewards/{mean,max,min}`

扣除 KL 惩罚后的最终训练 Reward 统计

`critic/advantages/{mean,max,min}`

优势函数统计，反映当前策略相对基线的改进

`critic/returns/{mean,max,min}`

Returns（Critic target）统计

trajectory/ — 轨迹统计（15 个）

**指标**

**含义**

`trajectory/response_length/{mean,max,min}`

响应 token 数统计（包含 abort 样本）

`trajectory/response/aborted_ratio`

响应长度为零的轨迹比例（rollout 异常或被 cancel）

`trajectory/response_length_non_aborted/{mean,max,min}`

排除 abort 后的有效响应 token 数统计

`trajectory/response_length/clip_ratio`

Response 达到最大长度被截断的比例

`trajectory/prompt_length/{mean,max,min}`

Prompt token 数统计

`trajectory/prompt_length/clip_ratio`

Prompt 达到最大长度被截断的比例

`trajectory/num_turns/{mean,max,min}`

Agent 与 LLM 交互的轮数统计

trace/ — 可观测性指标

**指标**

**含义**

`trace/training/epoch`

当前训练 epoch

`trace/num_llm_calls/{avg,sum}`

每条 / 总 LLM 调用次数

`trace/success_rate/agent/{avg,sum}`

Agent 任务成功率 / 累计成功条数

`trace/success_rate/reward/{avg,sum}`

Reward 计算成功率 / 累计成功条数

`trace/attempts/agent/{avg,sum}`

Agent 平均 / 累计 HTTP 尝试次数（含重试）

`trace/reward/<reward_name>/{avg,sum}`

单个 Reward 函数的平均 / 累计值

`trace/reward_metrics/<reward_name>/<metric>/...`

Reward 函数返回的自定义子指标（用户自定义）

timing/ — 耗时分析（11 个）

分为三个子组：`timing/s/*`（Trainer 阶段耗时，秒）、`timing/s/rollout/*`（Rollout 侧耗时，秒）、`timing/ms/*_per_token`（每 Token 耗时，毫秒）。

**指标**

**含义**

`timing/s/step`

完整一个 Trainer step 的总耗时

`timing/s/trainer_fetch_batch`

Trainer 等待并拉取一个 batch 的耗时

`timing/s/old_log_prob`

旧 policy 的 log-prob 计算耗时

`timing/s/adv`

Advantage 计算耗时

`timing/s/update_actor`

Actor 反向传播 + 优化器步进耗时

`timing/s/param_sync`

Rollouter 从 Trainer 同步参数的耗时

`timing/s/rollout/agent_loop_latency/avg`

单次 Rollout 总耗时（Agent + Reward + 后处理）

`timing/s/rollout/model_latency/avg`

单条轨迹的 LLM 推理累计耗时

`timing/s/rollout/reward_latency/avg`

Reward 调用耗时

`timing/ms/gen_per_token`

生成阶段每 Token 耗时

`timing/ms/update_actor_per_token`

Actor 更新阶段每 Token 耗时

perf/ — 性能总览（3 个）

**指标**

**含义**

`perf/total_num_tokens`

本 step 处理的 Token 总数

`perf/time_per_step`

每个 step 总耗时

`perf/throughput`

每 GPU 吞吐量（tokens/s/GPU）

### 自定义指标

自定义指标完整定义详见本篇 §自定义指标。

## 常见问题

### 故障速查总表

问题关键字

主信号

处置建议

详见

Reward 不涨

`critic/rewards/mean` 平台

检查 lr / Reward 函数

本篇 P1

KL 爆炸 / 输出乱码

`actor/ppo_kl` >0.1

`kl_loss_coef` ↑ / lr ↓

本篇 P3 / P8

Reward Hacking

训练 reward 涨 + validation 跌

切换信号 / shaping

本篇 P5 + 《强化学习开发指南》

截断率高

`clip_ratio` 高

`max_length` ↑

本篇 P9

FAILED·函数注册失败

classpath 错 / 依赖缺

查 `requirements.txt`

《强化学习训练配置 — 提交与配置》

FAILED·Rollout 超时

单条 timeout

`timeout` ↑ / Tracing 看哪段慢

本篇 ↓FAILED 排查

FAILED·资源不足

MTU 或 FC 容器

查 `fully_async` 队列

《强化学习训练配置 — 提交与配置》

Tracing 看不到

控制台空白

检查 ARMS 授权 / `requirements.txt`

本篇 ↓Trace 看不到

### 训练期 FAILED 排查流程

训练期 FAILED 排查（指标异常触发）见本节；基础设施类故障（FC 注册失败 / 上传超时 / 资源不足等）见《强化学习训练配置 — 提交与配置》§常见问题。

#### 标准排查流程

1.  **Step 1 详情页签**确认状态与失败时间点
    
2.  **Step 2 日志页签**末尾 100-500 行（SDK `AgenticRL.logs(job_id, lines=100)` / CLI `dashscope rl logs --lines 100`）
    
3.  **Step 3 区分错误层**：
    
    -   **用户函数错**（Rollout/Reward 抛异常）→ `test_functions` 本地复现 → 改代码 → 重新 register/run
    -   **框架错**（OOM / 资源不足 / 网络）→ 看 `fully_async` 队列 + 调 `concurrency` / `capacity`
    -   **数据错**（JSONL 解析失败）→ 校验单条格式与 `rollout_extra`

#### 训练期常见报错模式

错误模式

主要现象

处置建议

Rollout 超时

`timeout` 触发 / LLM 慢 / 工具慢

加超时 + Tracing 看哪段慢

Reward 偶发 FAILED

未处理空 messages / 编码错误

加 try/except 返回 `TaskStatus.FAILED + error`

资源不足

MTU 不够 / FC 扩容跟不上

看 fully\_async 队列 + 调 `concurrency` / `capacity`

数据格式错

JSONL 解析失败

行级 JSON 校验 / `messages` 角色 / `rollout_extra` 字段

### Trace 数据查看入口

在百炼控制台完成 ARMS 授权后：

-   **轨迹**页签 → 轨迹详情 / Reward 分析 / 工具调用分析
-   **指标**页签 → trace/ 分组

### Trace 看不到如何排查

按以下顺序排查：

1.  确认 Runtime `env` 中**没有**设置 `ENABLE_TRAJECTORY="false"`（默认开启，无需显式设置）
2.  确认已在百炼控制台授权 **ARMS 服务**
3.  检查 `requirements.txt` 是否包含 OpenTelemetry 相关依赖
4.  检查 `process()` 方法是否添加了 `@observe_processor` 装饰器

### 开启 Tracing 对性能有影响吗？

Tracing 会增加少量存储和延迟开销。建议在开发调试阶段开启，正式大规模训练时如只需看训练指标（Actor/Critic/Perf 等）而无需轨迹详情，可以关闭：在 Runtime `env` 中设置 `{"ENABLE_TRAJECTORY": "false"}`。关闭后系统指标不受影响。

### 如何在指标中区分不同的 Reward 函数？

通过 `RewardFunctionComponent(name="reward-1")` 为每个 Reward 函数设置唯一名称。该名称会出现在指标路径中（`trace/reward_metrics/reward-1/...`），控制台会自动按名称分组展示。

### 如何关闭 Tracing 以节省成本？

在 Runtime 的 `env` 中设置 `{"ENABLE_TRAJECTORY": "false"}`。可以通过 `FunctionComponentRuntime(env={"ENABLE_TRAJECTORY": "false"})` 或 YAML 中按 block style 设置：

```
env:
  ENABLE_TRAJECTORY: "false"
```
