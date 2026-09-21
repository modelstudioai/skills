# 在线策略蒸馏可观测配置与指标参考

在线策略蒸馏训练的可观测手册：Tracing 接入、自定义指标上报、控制台页签、指标字典、训练效果判断与常见问题排查

在线策略蒸馏（OPD）训练自动记录每次 LLM 调用、工具调用与评分细节，在百炼控制台可视化展示。接入只需在函数代码中添加少量装饰器与包装调用。

**相关文档：**

-   在线策略蒸馏原理与示例选型 → 见 [在线策略蒸馏训练概述](opd-training-overview.md)
-   Model OPD 开发 → 见 [Model OPD 开发](opd-model-development-guide.md)；Agentic OPD 开发 → 见 [Agentic OPD 开发](opd-agentic-development-guide.md)
-   提交参数与超参全集 → 见 [在线策略蒸馏训练配置](opd-training-config.md)

## 概述

可观测能力基于 **OpenTelemetry**（开源可观测性标准）实现 Tracing（链路追踪），数据导出到 **ARMS（应用实时监控服务）**，在百炼控制台展示。**Span** 是 OpenTelemetry 中一次操作的观测单元，多个 Span 自动嵌套形成调用链。

五个环节：

1.  接入 Tracing — SDK 自动上报训练指标到控制台，如何在轨迹页查看
2.  自定义指标 — `rollout_metrics` 与 `reward_metrics` 的上报路径与约束
3.  控制台查看效果 — 指标 / 轨迹 / 产出 / 日志四页签怎么看
4.  训练指标参考 — 在线策略蒸馏特有指标字典 + 通用指标速查
5.  判断训练效果与排查 — 训练中判读、训练后评测、常见问题

## 接入 Tracing

以在线策略蒸馏项目的 Rollout 处理器为例，3 步完成 Tracing 接入。**OPD 差异：**调用链 LLM Span 对应学生模型调用，教师模型打分在服务端。

### Step 1：添加依赖

在项目根目录的 `requirements.txt` 中添加以下 OpenTelemetry 相关依赖：

**依赖**

**说明**

`opentelemetry-api==1.41.1`

OTel API

`opentelemetry-sdk==1.41.1`

OTel SDK

`opentelemetry-exporter-otlp-proto-http==1.41.1`

OTLP HTTP 导出器

`opentelemetry-processor-baggage==0.62b1`

Baggage 处理器

`loongsuite-util-genai==0.4.0`

生成式 AI 工具库

运行环境中已预装 `dashscope`、`fastapi`、`uvicorn`、`pyyaml`；如需固定版本也可在 requirements.txt 中声明。

### Step 2：添加观测代码

代码改动集中在 5 个装饰器/函数。它们会自动嵌套，形成完整的调用链：

```
# 调用链结构：装饰器自动嵌套形成 Span 树，[ENTRY] 为入口 Span，[LLM]/[TOOL]/[custom] 为子 Span
[ENTRY: ROLLOUT] @observe_processor          ← Rollout 处理器入口
├── [LLM] trace_client / @observe_llm        ← LLM 调用（学生模型调用）
│   └── (OpenAI / LangChain / DashScope API)
├── [TOOL] trace_tool / @observe_tool        ← 工具调用
│   ├── tool: my_tool (MCP)
│   └── tool: my_scorer (自定义)
└── [custom] rollout_metrics                 ← Rollout 自定义指标

[ENTRY: REWARD] @observe_processor           ← Reward 处理器入口
├── [LLM] trace_client / @observe_llm        ← LLM 调用（评分用）
├── [TOOL] trace_tool / @observe_tool        ← 工具调用
└── [custom] reward_metrics                  ← Reward 自定义指标
```

#### @observe\_processor — 追踪处理器入口

加在 `process()` 方法上，创建顶层 ENTRY Span（入口 Span，调用链最外层）。SDK 按继承链自动推断 Span 类型：继承 `AbstractRolloutProcessor` 判为 ROLLOUT，继承 `AbstractRewardProcessor` 判为 REWARD。自动记录输入、输出、耗时、成功/失败状态。

**Rollout 侧示例（**`functions/rollout/my_rollout.py`）：

```
from dashscope.finetune.reinforcement.component.observability import observe_processor
# 导入 Rollout 处理器基类与输入输出类型（项目内已定义）

class MyRolloutProcessor(AbstractRolloutProcessor):
    @observe_processor  # Span 类型 = ROLLOUT（按继承 AbstractRolloutProcessor 自动推断）
    async def process(self, input: RolloutInput) -> RolloutOutput:
        # input: Rollout 输入，含 prompt、模型资源、工具列表等
        await self._async_setup()  # 异步初始化：建 LLM 客户端、加载工具
        return await self._async_process(input)  # 执行实际 Rollout 逻辑，返回轨迹与指标
```

**Reward 侧示例（**`functions/reward/reward.py`）：

```
class MyRewardProcessor(AbstractRewardProcessor):
    @observe_processor  # Span 类型 = REWARD（按继承 AbstractRewardProcessor 自动推断）
    async def process(self, input: RewardInput) -> RewardOutput:
        # input: Reward 输入，含 agent_output（模型轨迹）与 ground_truth（标准答案）
        messages = input.agent_output.messages  # 取模型多轮对话消息列表
        content = messages[-1].get("content", "") if messages else ""  # 取最后一条 assistant 回复文本
        score = await evaluate(content, input.ground_truth)  # 用标准答案对回复评分，返回主分
        return RewardOutput(
            reward=Reward(reward_score=score, reward_metrics={...}),  # 主分入 reward_score，分维度入 reward_metrics
            status=TaskStatus.SUCCESS,  # 任务状态：SUCCESS 表示评分成功
            error=None,  # 无异常时为 None；失败时填错误信息
        )
```

#### trace\_client() — 追踪 LLM 客户端

在初始化或 process 方法内调用，包装 LLM 客户端实例。之后该客户端的所有 LLM 请求都会自动产生 LLM Span，记录模型名、请求内容、Token 用量、延迟。

**支持的客户端类型（按对象属性自动识别）：**

-   OpenAI 客户端（`AsyncOpenAI` / `OpenAI`）
-   OpenAI completions 资源（`.chat.completions`）
-   LangChain ChatOpenAI 等类（通过 `.client` / `.async_client`）
-   DashScope Generation 类（传入类本身，非实例）

**示例（**`functions/rollout/my_rollout.py`）：

```
from dashscope.finetune.reinforcement.component.observability import trace_client
# 导入 LLM 客户端包装函数，调用后该客户端的请求自动产生 LLM Span

class MyRolloutProcessor(AbstractRolloutProcessor):
    def _build_llm(self, input: RolloutInput) -> ChatOpenAI:
        # input: Rollout 输入，model_resource 含模型名等资源配置
        resource = input.model_resource  # 取模型资源（由 Runtime 注入的学生模型）
        llm = ChatOpenAI(model=resource.model_name, ...)  # 构造 LangChain ChatOpenAI 客户端
        trace_client(llm)  # 包装后自动追踪所有 LLM 调用（记录模型名、请求、Token 用量、延迟）
        return llm
```

#### trace\_tool() — 追踪工具调用

获取工具实例后调用，包装工具对象。之后每次工具调用都会产生 TOOL Span，记录工具名、参数、返回值、延迟。

**支持的输入格式：**

-   单个 LangChain BaseTool
-   列表 / 元组 / 字典（自动遍历）
-   LangGraph ToolNode（自动展开 `.tools_by_name`）
-   MCP 工具（自动检测，provider 设为 "mcp"）
-   自定义 provider（`trace_tool(tool, provider="my-plugin")`）

**警告****MCP 注意：**MCP（Model Context Protocol，模型上下文协议）Server 和 Client 运行在不同进程中。Server 端的 `@observe_tool` 对 Client 端**无效**。必须在 Client 端调用 `get_tools()` 之后，对返回的工具列表执行 `trace_tool(tools)`。

#### @observe\_llm — 自定义 LLM 函数

当 `trace_client()` 无法自动检测您的 LLM 客户端时，用此装饰器手动标记 LLM 调用函数。

**签名要求：**函数必须包含 `*` 后的关键字参数 `model` 和 `messages`。

**示例（**`functions/rollout/my_rollout.py`）：

```
from dashscope.finetune.reinforcement.component.observability import observe_llm
# 导入 LLM 装饰器，用于手动标记无法被 trace_client 自动识别的 LLM 调用

class MyRolloutProcessor(AbstractRolloutProcessor):
    @observe_llm  # 标记为 LLM Span（记录模型名、messages、Token 用量）
    async def _call_llm(self, *, messages: List[Dict], model: str) -> Any:
        # messages: 对话消息列表；model: 模型名（* 后关键字参数为签名硬性要求）
        ...
```

#### @observe\_tool — 自定义工具函数

当 `trace_tool()` 无法自动检测您的工具时（如普通 Python 函数充当工具），用此装饰器手动标记。可通过 `name` 参数自定义 Span 名称。

**示例（**`functions/rollout/my_rollout.py`）：

```
from dashscope.finetune.reinforcement.component.observability import observe_tool
# 导入工具装饰器，用于手动标记无法被 trace_tool 自动识别的工具函数

class MyRolloutProcessor(AbstractRolloutProcessor):
    @observe_tool(name="my_scorer")  # 标记为 TOOL Span，name 自定义 Span 显示名
    def _score_response(self, *, messages: List[Dict]) -> float:
        # messages: 对话消息列表，函数返回评分为 float
        ...
```

### Step 3：提交任务

提交任务时，Runtime 的 `env` 字段留空即可——Tracing **默认开启**：

```
# FunctionComponentRuntime: Rollout/Reward 组件运行时配置
rollout_runtime = FunctionComponentRuntime(
    cpu=2, memory_size=4096, disk_size=512,  # 资源：2 核 CPU、4GB 内存、512MB 磁盘
    concurrency=30, capacity=30,  # 并发 30、容量 30（单实例同时处理请求数）
    min_capacity=30, max_capacity=60,  # 弹性伸缩下限 30、上限 60
    env={}  # 留空 = 默认开启 Tracing；设 {"ENABLE_TRAJECTORY": "false"} 可关闭
)
```

**说明****如需关闭 Tracing**（节省成本），在 `env` 中设置 `{"ENABLE_TRAJECTORY": "false"}` 即可。关闭后系统指标不受影响，仅 Tracing 数据停止采集。

## Tracing 性能与成本权衡

### 数据链路与成本来源

-   **数据流**：函数代码（装饰器）→ OpenTelemetry SDK → ARMS → 控制台轨迹/指标页签
-   **成本来源**：ARMS Span 存储（按量计费）+ 函数侧少量 CPU/网络开销 + 训练延迟少量增加

### 开关策略与成本治理

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

大规模正式训练

**可关闭**

actor/critic/trajectory/timing 系统指标

轨迹回放 / 工具调用详情 / 自定义 metrics 曲线

显著降低

**OPD 差异：**关闭 Tracing 后保留的系统指标见 §训练指标参考；`trace/distillation/*` 属系统指标，关闭后仍可查看（教师模型健康排查不受影响）。

自定义指标的成本治理：

-   **数量与基数**：`reward_metrics` / `rollout_metrics` 数量与基数（cardinality）影响 ARMS 存储
-   **避免高基数字段**：user\_id / request\_id 不当指标 key
-   **精简指标**：关键指标 ≤10 个，不留临时调试指标

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

**值类型约束：**

-   **扁平字典**：reward\_metrics / rollout\_metrics 返回 flat dict（扁平字典，非嵌套 list），每值为 float
-   **主分单独上报**：reward\_score 单独放入 `Reward.reward_score`，不重复放入 reward\_metrics
-   **非 float 只落盘**：非 float 数据通过 `rollout_extra` 只落盘不进指标
-   **指标路径**：reward\_score 主分对应 `trace/reward/<name>/`，各维度对应 `trace/reward_metrics/<name>/<metric>`

**多 Reward 函数场景：**通过 `RewardFunctionComponent(name="reward-1")` 为每个 Reward 函数设唯一名称，指标路径自动区分（`trace/reward_metrics/reward-1/...`）。

## 控制台查看效果

训练开始后，在[模型调优控制台](https://bailian.console.aliyun.com/cn-beijing/model/tuning)进入**模型调优**页面，点击任务名称进入详情查看观测数据。以下说明"您在代码中做了什么 → 在控制台看到什么"的对应关系。

**OPD 差异：**任务详情页无独立"详情"页签，状态在任务列表查看。关注点：指标页看蒸馏损失、教师模型健康与验证 reward；轨迹页逐样本看工具调用链；产出页的最后一个 Checkpoint 自动发布。

任务详情包含以下页签，按"先看进度 → 再看行为 → 出问题再下钻"顺序使用：

页签

主要回答

何时使用

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

### 轨迹与行为分析

**轨迹详情 — 对应 @observe\_processor：**在**轨迹**页签的**轨迹详情**子页面，可以看到每次 Rollout 的完整交互过程：

-   **轨迹列表：**展示所有采样轨迹，支持按 Sample ID / 轨迹 ID / Epoch / Step 筛选
-   **对话过程：**完整多轮交互（user → assistant → tool\_call → tool\_result → assistant），直观看到模型的推理链
-   **Reward 分数：**每个 Step 显示对应的 Reward 分数和状态（SUCCESS/FAILED）

关注：工具调用是否正确？对话轮次是否合理？模型是否在重复无效操作？

**工具调用分析 — 对应 trace\_tool / @observe\_tool：**在**轨迹**页签的**工具调用分析**子页面，可以查看：

-   **工具调用记录：**工具名称、调用参数、返回结果和耗时
-   **Tracing 子页签：**每条轨迹的 Span 树，可展开查看每次工具调用和 LLM 请求的完整详情

**典型用途：**排查 Agent 的工具调用失败——哪个工具报错？参数传递是否正确？耗时是否过长？

**Reward 分析 — 对应 reward\_metrics：** **概念定义：**

-   **Sample**：训练数据中一条原始样本（一道题、一条指令、一个 prompt）
-   **Trajectory**：同一 Sample 在 `n_rollouts` 次采样下产生的具体一条交互轨迹
-   关系：一条 Sample → N 条 Trajectory（N = `n_rollouts`）

在**轨迹**页签的**Reward 分析**子页面，从三个维度评估训练效果：

-   **Step 维度：**选择训练 Step，查看该 Step 下所有样本的 Reward 聚合（平均分、成功率、趋势图），判断整体训练趋势
-   **Sample 维度：**选择 Sample ID，查看同一样本在不同轨迹中的 Reward 对比，发现问题样本
-   **Trajectory 维度：**查看单条轨迹的每个评分维度原始分，用于归因分析

### 指标、产出与日志

**指标页签 — 对应 rollout\_metrics / reward\_metrics：**在**指标**页签的 `trace/` 分组，可以看到您在代码中定义的所有自定义指标的聚合曲线（avg / sum）。完整指标分组见下方 §训练指标参考；看到指标异常如何归因 → §判断训练效果与排查。

**产出页签：**训练完成后，在**产出**页签中可以看到 Checkpoint 列表，每行包含 Checkpoint ID、发布状态和剩余保存时间。

1.  选择目标 Checkpoint，点击**发布**按钮
2.  等待发布完成（状态从"待发布"变为"已发布"）
3.  发布后即可通过模型名称在 API 中调用

**OPD 差异：**最后一个 Checkpoint 自动发布，产出页仍可手动选任意 Checkpoint 发布（与自动发布的最后一个并存，调用时按模型名区分）。训练完成不等于训练成功。启用 Reward 时建议以 `validation/data/reward/mean@1` 最优的 Checkpoint 为准，而非默认的最后一个。纯蒸馏（不注册 reward 组件）无 validation reward，依据 loss 趋势与独立评测判断效果。

**日志页签：**在**日志**页签查看训练运行日志，也可通过 SDK / CLI 获取：

-   SDK：`AgenticRL.logs(job_id="ft-xxx", lines=100)`
-   CLI：`dashscope rl logs "ft-xxx" --lines 100`

FAILED 任务排查步骤见 §常见问题 → FAILED 排查。

## 训练指标参考

以下为在线策略蒸馏特有指标与通用指标全集。指标在「指标」页展示，点击展开各分组详情。

### 在线策略蒸馏特有指标

以下为在线策略蒸馏特有指标：

distillation/ — 蒸馏损失

**指标**

**含义与判读**

`actor/distillation/loss`

蒸馏损失，下降表示学生模型正在向教师模型靠拢

启用 reward 时，`actor/distillation/loss` 与 `actor/pg_loss` 共同构成总损失，两者都应下降或趋稳。

trace/distillation/ — 教师模型信号健康

**指标**

**含义与判读**

`trace/distillation/valid_token_rate`

教师模型成功给出 logprob（对数概率）的 token 占比，正常接近 1.0；小于 1 表示打分缺失

`trace/distillation/missing_token_rate`

教师模型未给出 logprob 的 token 占比，正常接近 0

`trace/distillation/empty_response_rate`

教师模型返回空响应比例，正常接近 0；升高指向教师模型侧异常

validation/ — 验证集指标（启用 Reward 时上报）

**指标**

**含义与判读**

`validation/data/reward/mean@1`

验证集聚合 reward 均值，相对基线上升为健康

验证指标只有聚合 reward 均值。Reward 函数返回的自定义维度不在验证指标中体现，需在训练指标 `trace/reward_metrics/<reward_name>/<metric>` 下查看（维度名取自 `reward_metrics` 的键，因任务而异）。纯蒸馏（不注册 reward 组件，functions=None）不上报该组。

### 关键指标速查

**类别**

**指标**

**判读**

蒸馏

`actor/distillation/loss`

下降或趋稳

教师模型健康

`trace/distillation/valid_token_rate`

接近 1.0

教师模型健康

`trace/distillation/missing_token_rate`

接近 0

教师模型健康

`trace/distillation/empty_response_rate`

接近 0

验证

`validation/data/reward/mean@1`

相对基线上升

reward 维度

`trace/reward_metrics/<reward_name>/<metric>`

关键业务维度不回退

### 通用指标

训练过程中产出的指标按前缀分为以下分组，各分组的详细指标说明见下方折叠面板：

**分组前缀**

**指标数**

**类型**

**说明**

**actor/**

8

系统

策略网络指标：损失、熵、KL 散度、裁剪率、梯度范数、学习率

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

可观测性指标：epoch、LLM 调用次数、成功率、自定义 metrics

**timing/**

11

系统

耗时分析：Trainer 阶段耗时、Rollout 耗时、每 Token 耗时

**OPD 差异：**在线策略蒸馏不产出 `perf/` 和 `fully_async/` 两组指标。

点击展开各分组的完整指标列表：

actor/ — 策略网络指标（8 个）

**指标**

**含义**

`actor/loss`

总 loss（pg + entropy + ...）

`actor/pg_loss`

策略梯度损失

`actor/entropy`

当前策略的平均 token 熵，反映探索程度

`actor/ppo_kl`

当前策略相对于初始策略的 KL 散度

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

响应长度为零的轨迹比例

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

Reward 函数返回的自定义子指标

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

单次 Rollout 总耗时

`timing/s/rollout/model_latency/avg`

单条轨迹的 LLM 推理累计耗时

`timing/s/rollout/reward_latency/avg`

Reward 调用耗时

`timing/ms/gen_per_token`

生成阶段每 Token 耗时

`timing/ms/update_actor_per_token`

Actor 更新阶段每 Token 耗时

## 判断训练效果

训练过程中上报的指标已足以判断一轮在线策略蒸馏是否在正常收敛；训练完成后的业务效果评测由用户按自身口径进行。

### 训练中判读顺序

在「指标」页按以下顺序判读：

**① 教师模型信号完整性** — `trace/distillation/valid_token_rate` 接近 1.0。明显小于 1 时教师模型打分存在缺失，其余指标解释力下降，应先排查（排查决策树 P2）。

**② 蒸馏收敛** — `actor/distillation/loss` 随训练下降或趋稳，表示学生模型正在向教师模型靠拢。

**③ 验证集表现** — `validation/data/reward/mean@1` 相对训练前基线上升。分维度看 `trace/reward_metrics/<reward_name>/<metric>`，关键业务维度（尤其安全类）不回退。

验证频率由 `eval_steps` 控制。若 step 0 存在验证点，该点对应训练前的模型状态，可直接作为基线。

纯蒸馏（不注册 reward 组件，functions=None）不产生验证指标与分维度指标。依据蒸馏损失与教师模型健康指标判断训练是否正常，业务效果通过训练后评测判断。

### 训练后业务评测

**保留训练前基线** — 蒸馏收益是相对量，缺基线无法判断提升幅度。训练产出的是新的模型 ID，原模型仍可调用，但基线评测结果需自行留存。

**保持同口径** — 训练前后评测应使用相同评测集与解码参数（`temperature`、`max_tokens`、是否开启思考等）。口径不一致时差值不可比——例如响应被长度上限截断，会表现为能力下降的假象。

示例目录下附带评测与对比脚本，仅作为实现参考，可按需改造。

### 验收判据

四项同时满足：

**判据**

**要求**

主判据

核心评测指标提升且非随机波动

安全判据

安全类维度不高于训练前

格式判据

格式类维度不低于训练前

分类别判据

按业务类别拆分后无类别显著回退

实测数值参考（仅参考，不作为通用判据）

示例三方对比（200 条验证集，temperature=0，8 并发）：

**指标**

**Base**

**Teacher**

**OPD**

核心成功率

0.700

0.955

0.990

安全违规率

0.235

0

0

学生模型超越教师模型的原因：启用 reward 时，reward 依据标准答案打分，趋向标准答案而非教师模型；纯蒸馏才以教师模型为性能上限。

## 在线策略蒸馏排查决策树

指标页看到异常曲线 → 对照本节定位问题 → 按建议处置。

### P1 蒸馏损失不降

-   **主信号**：`actor/distillation/loss` 随训练不下降或反而上升
-   **根因**：教师模型信号缺失 / 学习率不适（过小不收敛或过大破坏输出格式） / 数据质量差
-   **处置**：先查 `valid_token_rate` 是否接近 1.0 → 信号正常时 loss 不降常因学习率过小，升高 `learning_rate`（×1.5~2，见训练配置调参决策表）→ 抽查训练数据 `rollout_extra` 中的标准答案

### P2 教师模型打分缺失

-   **主信号**：`trace/distillation/valid_token_rate` 明显小于 1.0
-   **根因**：教师模型侧打分缺失（教师模型由服务端托管，对用户不透明，无法直接排查）
-   **处置**：查 `missing_token_rate` 与 `empty_response_rate` 是否同步升高 → 若教师模型超时或空响应比例高，提交工单

### P3 验证集不升

-   **主信号**：`validation/data/reward/mean@1` 出现下行拐点而训练 reward 仍升
-   **通用处置**：早停（在产出页签选取较早的 Checkpoint）+ 保持训练前后评测口径一致 + 分维度查看 `reward_metrics` 回退情况
-   **额外根因**：过拟合教师模型风格（纯蒸馏时）
-   **额外处置**：抽查 `rollout_extra` 中标准答案质量

**四源协同排查：**四类观测源各回答不同问题：**日志**→"何时失败、报错堆栈"、**指标**→"是不是 / 有多严重"、**轨迹**→"为什么 / 哪条样本"、**轨迹页·Tracing 子页签**→"哪段慢 / 哪个外部依赖异常"。按问题类型选观测源：

**问题类型**

**主用**

**次用**

**不必看**

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

Tracing 子页签

日志

—

训练变慢

指标 timing

Tracing 子页签

—

输出质量差

轨迹

reward\_metrics

—

**OPD 特有问题类型选源：**

**问题类型**

**主用**

**次用**

**不必看**

蒸馏损失不降

指标

轨迹

日志

教师模型打分缺失

指标

日志

轨迹

验证集不升

指标 → 轨迹

reward\_metrics

日志

## 后续步骤

-   [在线策略蒸馏训练概述](opd-training-overview.md) → 原理与端到端流程
-   [Model OPD 开发](opd-model-development-guide.md) / [Agentic OPD 开发](opd-agentic-development-guide.md) → 函数开发完整细节
-   [在线策略蒸馏训练配置](opd-training-config.md) → 提交参数与超参全集

## 常见问题

### 教师模型侧异常

教师模型由服务端部署，对用户不透明。以下现象需提交工单：

**现象**

**处理**

`trace/distillation/valid_token_rate` < 1，教师模型打分缺失

提工单

教师模型超时或打分缺失

提工单

同族师生仍报 tokenizer（分词器）不匹配

提工单

### 自查项

通用自查项：

**现象**

**排查方向**

Tracing 控制台空白

①确认 env 未设 `ENABLE_TRAJECTORY="false"` ②确认已授权 ARMS ③检查 requirements.txt 含 OTel 依赖 ④检查 process() 加了 @observe\_processor

Reward 偶发 FAILED

未处理空 messages / 编码错误 → 加 try/except 返回 `TaskStatus.FAILED + error`

格式类维度低

检查学生模型输出格式是否符合 Reward 函数要求

如何区分不同 Reward 函数

通过 `RewardFunctionComponent(name="reward-1")` 设唯一名称，指标路径自动区分

OPD 特有自查项：

**现象**

**排查方向**

400 ... teacher\_model must be a valid model ID

改用百炼模型 ID

提交时报错提示 SDK 不具备在线策略蒸馏能力

换用示例指定的 wheel

纯蒸馏无验证指标

正常行为（不注册 reward 组件，functions=None），靠独立评测判断

format\_valid 异常低

检查学生模型输出是否被 thinking/工具调用文本污染，并确认 Reward 格式判定正则与训练前后解码参数保持一致

### 故障速查与 FAILED 排查

通用故障速查：

**现象**

**首查**

**次查**

FAILED·函数注册失败

classpath 错 / 依赖缺

查 requirements.txt

FAILED·Rollout 超时

单条 timeout

timeout ↑ / Tracing 看哪段慢

Tracing 看不到

控制台空白

检查 ARMS 授权 / requirements.txt

OPD 特有故障速查：

**现象**

**首查**

**次查**

valid\_token\_rate 低

教师模型侧异常

提工单

蒸馏损失不降

教师模型信号完整性

学习率 / 数据质量

tool\_call\_count 为 0 / NO\_TOOL 频繁

学生模型是否支持 function calling、传入 tools 参数是否传对

查 tool 定义与 api\_key/base\_url

**标准排查流程：**

1.  **Step 1 任务列表**确认状态与失败时间点
    
2.  **Step 2 日志页签**末尾 100-500 行（SDK `AgenticRL.logs(job_id, lines=100)` / CLI `dashscope rl logs --lines 100`）
    
3.  **Step 3 区分错误层**：
    
    -   **用户函数错**（Rollout/Reward 抛异常）→ `test_functions` 本地复现 → 改代码 → 重新 register/run
    -   **框架错**（OOM 内存不足 / 资源不足 / 网络）→ 调 `concurrency` / `capacity`
    -   **数据错**（JSONL 解析失败）→ 校验单条格式与 `rollout_extra`

**训练期常见报错模式：**

错误模式

主要现象

处置建议

资源不足

扩容跟不上

见 Step 3 框架错（调 `concurrency` / `capacity`）

数据格式错

JSONL 解析失败

行级 JSON 校验 / `messages` 角色 / `rollout_extra` 字段
