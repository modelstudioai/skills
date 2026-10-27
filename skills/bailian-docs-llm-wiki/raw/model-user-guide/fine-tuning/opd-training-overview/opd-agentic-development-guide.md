# Agentic OPD 开发

Agentic OPD 必须自定义 Rollout（自行控制生成过程，如多轮交互、传入 tools 参数产生结构化 tool\_call），Reward 可选。本文介绍不启用 Reward 与启用 Reward 两种模式的函数开发。

本文介绍 Agentic OPD 的函数开发。Agentic OPD 必须自定义 Rollout（自行控制生成过程，如多轮对话、自定义交互、传入 `tools` 参数产生结构化 `tool_call`（工具调用）等），Reward 可选。由三部分组成：工具定义 + Rollout（采样产轨迹）+ Reward（评分，可选）。训练概述见 [在线策略蒸馏训练概述](opd-training-overview.md)。

## 开发概览

Agentic OPD 与 Model OPD 的关键区别在是否涉及工具调用、多轮或自定义交互：

1.  **Model OPD** 用于纯文本任务，学生模型直接生成文本输出。
2.  **Agentic OPD** 用于需工具调用或多轮交互的任务，通过传入 `tools` 参数由框架把工具信息直接传给模型，模型返回结构化的 `tool_calls` 字段（原生工具调用）。

不启用 Reward 时 functions 列表只含 `RolloutFunctionComponent`，训练信号以教师模型蒸馏为主。

两种模式差异如下。

**维度**

**无 Reward（只 Rollout）**

**有 Reward（Rollout + Reward）**

开发工作

编写 Rollout 函数（自定义生成过程）

额外编写 Reward 评分函数

训练信号

教师模型蒸馏为唯一监督

教师蒸馏 + 任务奖励

适用场景

只需工具调用形态对齐、教师模型已是上限

需按业务目标优化工具选择与参数

## 数据格式

每行一条 JSONL，含 `messages`（对话）与 `rollout_extra`（附加信息）两个字段。

-   `messages`：对话列表，按 user/assistant 交替排列，首轮可为 user 或 system。
-   `rollout_extra`：附加信息，可存 sample\_id、category、solution 等。`solution` 是 JSON 字符串，存标准答案供 Reward 评分；不启用 Reward 时仅作标记不被消费。

样例（实际为单行，此处展开便于阅读）。样例中的工具（如 `query_status`、`delete_item`）在下方[工具定义](#tool-definitions)节定义，Rollout 通过传入 `tools` 参数注入工具见[Rollout 函数结构](#rollout-structure)节：

#### 单轮 · tool\_call

用户询问项目状态，标准答案是调用 `query_status` 工具查询：

```
{
  "messages": [
    {"role": "user", "content": "查询项目 P100 的状态"}
  ],
  "rollout_extra": {
    "sample_id": "train-query-001",
    "solution": "{\"decision\":\"tool_call\",\"tool_calls\":[{\"name\":\"query_status\",\"arguments\":{\"item_id\":\"P100\"}}]}"
  }
}
```

#### 多轮 · tool\_call

用户要删除项目，assistant 先确认，用户确认后标准答案调用 `delete_item` 工具：

```
{
  "messages": [
    {"role": "user", "content": "删除项目 P200"},
    {"role": "assistant", "content": "CONFIRM: 请确认删除项目 P200"},
    {"role": "user", "content": "确认删除"}
  ],
  "rollout_extra": {
    "solution": "{\"decision\":\"tool_call\",\"tool_calls\":[{\"name\":\"delete_item\",\"arguments\":{\"item_id\":\"P200\"}}]}"
  }
}
```

#### 单轮 · 无工具调用

用户信息不足（没给项目编号），标准答案是澄清而非调工具：

```
{
  "messages": [
    {"role": "user", "content": "项目编号是什么？"}
  ],
  "rollout_extra": {
    "sample_id": "train-clarify-003",
    "solution": "{\"decision\":\"clarify\",\"mentions\":[\"编号\"]}"
  }
}
```

## Rollout 函数开发

Agentic OPD 必须自定义 Rollout（自行控制生成过程）。本节给出 Rollout 函数开发：工具定义、Rollout 函数结构、Tracing 接入。

### 工具定义

工具定义是 Rollout 的前置依赖。先定义 tool\_spec，再实现 Rollout 处理器，二者同属 `functions/` 子包。目录结构如下（`__init__.py` 使目录成为可导入的 Python 包，缺则 classpath 解析失败）：

```
functions/
├── __init__.py
├── tool_spec.py          # SYSTEM_PROMPT、TOOL_DEFINITIONS、DESTRUCTIVE_TOOLS
├── rollout/
│   ├── __init__.py
│   └── my_rollout.py      # MyRolloutProcessor
└── reward/
    ├── __init__.py
    └── my_reward.py        # MyRewardProcessor（启用 Reward 时）
```

提交脚本的 `classpath` 指向 `functions.rollout.my_rollout.MyRolloutProcessor`（即 `functions/rollout/my_rollout.py` 内的 `MyRolloutProcessor` 类），Reward 类同理指向 `functions.reward.my_reward.MyRewardProcessor`。

工具定义含三个部分：

-   **系统提示词**：约束何时调用工具、何时回复文本前缀
-   **工具定义列表**：JSON Schema 列表，供 Rollout 内传入 `tools` 参数直接使用，框架自动渲染工具信息给模型；格式与 OpenAI function calling 一致
-   **高危操作集合**：标记破坏性工具名称，供 Reward 判断模型是否误调危险工具

与 Model OPD 的区别：Model OPD 用于纯文本任务；Agentic OPD 用于需工具调用或多轮交互的任务，通过传入 `tools` 参数由框架传工具产生原生 `tool_calls`。

```
# 通用化工具定义模板
# TOOL_DEFINITIONS：工具定义列表，供 Rollout 传入 tools 参数，框架自动渲染给模型
# DESTRUCTIVE_TOOLS：破坏性工具名集合，供 Reward 判断模型是否误调危险工具

# 系统提示词：约束模型何时调工具、何时回退为文本前缀（CLARIFY/NO_TOOL/CONFIRM）
SYSTEM_PROMPT = """You are a tool-routing assistant.
Call tools only when the request is clear and all required arguments are known.
If required information is missing, reply exactly with CLARIFY: <question>.
If no tool is appropriate, reply exactly with NO_TOOL: <answer>.
Destructive actions require explicit user confirmation first; otherwise reply with CONFIRM: <question>."""

# 工具定义列表，格式与 OpenAI function calling 一致，每项含 type/function(name/description/parameters)
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "query_status",  # 查询类工具：按 item_id 返回状态
            "description": "Look up the status of an item by its identifier.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {  # 必填参数：待查询项目的标识符
                        "type": "string",
                        "description": "Identifier of the item to query.",
                    }
                },
                "required": ["item_id"],  # 声明 item_id 为必填
                "additionalProperties": False,  # 禁止额外字段，校验更严格
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_item",  # 破坏性工具：删除项目，须用户确认后才执行
            "description": "Delete an item after the user explicitly confirms.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {"type": "string"},   # 待删除项目标识符
                    "reason": {"type": "string"},     # 删除原因，留痕审计
                },
                "required": ["item_id", "reason"],  # 两参数均必填
                "additionalProperties": False,
            },
        },
    },
    # 按任务添加更多工具定义
]

# 高危操作名称集合，供 Reward 判断模型是否误调危险工具
DESTRUCTIVE_TOOLS = {
    "delete_item",
    # 按任务添加更多高危工具名
}
```

### Rollout 函数结构

继承 `AbstractRolloutProcessor`，实现 `async process(input: RolloutInput) -> RolloutOutput`。`@observe_processor` 装饰 `process`（自动接入 Tracing）。关键步骤：

1.  **取模型资源**：从 `RolloutInput` 取 `model_resource`（api\_key/base\_url/model\_name）与 `sampling_params`
2.  **构造并包装 LLM**：构造 `ChatOpenAI`，调 `trace_client` 包装
3.  **采样**：传入 `tools` 参数注入工具定义，`ainvoke` 采样（单轮、不执行工具）
4.  **构造输出**：构造 `AgentOutput`（含原生 `tool_calls`、`rollout_metrics`），置于 `RolloutOutput.agent_output`
5.  **异常兜底**：返回 `ROLLOUT_ERROR` 兜底文本，状态置 FAILED

数据流：`RolloutInput → AgentOutput → RolloutOutput`。

```
# 通用化 Agentic OPD Rollout 处理器模板
import time
import json
from typing import Any
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage  # langchain 消息类型，对应 user/assistant/system
from langchain_openai import ChatOpenAI  # 封装 OpenAI 兼容接口的 LLM 客户端
from dashscope.finetune.reinforcement import RolloutInput, RolloutOutput  # 输入/输出数据模型
from dashscope.finetune.reinforcement.component.data.base_data_model import (
    AgentOutput,   # 学生输出，含 messages/tool_calls/rollout_metrics
    TaskStatus,    # 任务状态枚举：SUCCESS / FAILED
)
from dashscope.finetune.reinforcement.component.observability import (
    observe_processor,  # 装饰器：自动为 process 接入 Tracing Span
    trace_client,      # 包装自构造 LLM 客户端，使其请求产生 LLM Span
)
from dashscope.finetune.reinforcement.component.processor.abstract_rollout_processor import (
    AbstractRolloutProcessor,  # 抽象基类，子类须实现 async process
)
from functions.tool_spec import SYSTEM_PROMPT, TOOL_DEFINITIONS  # 工具定义与系统提示词

def _to_langchain_messages(messages):
    """将 dict messages 转为 langchain 消息对象，首条注入 SYSTEM_PROMPT。"""
    converted = [SystemMessage(content=SYSTEM_PROMPT)]  # 默认塞入系统提示词
    for msg in messages:
        role = msg.get("role")
        content = str(msg.get("content") or "")
        if role == "system":
            converted[0] = SystemMessage(content=content)  # 数据自带 system 则覆盖默认
        elif role == "assistant":
            converted.append(AIMessage(content=content))
        else:  # user 或其他角色按 user 处理
            converted.append(HumanMessage(content=content))
    return converted

def _assistant_to_openai(message):
    """将 langchain AIMessage 转为 OpenAI 格式 dict，含 tool_calls。"""
    tool_calls = []
    for call in message.tool_calls or []:  # 遍历模型产出的原生工具调用
        tool_calls.append({
            "id": call.get("id") or "tool-call",  # 调用 ID，缺失时给默认值
            "type": "function",
            "function": {
                "name": call.get("name"),
                "arguments": json.dumps(call.get("args") or {}, ensure_ascii=False),  # args 序列化为 JSON 字符串
            },
        })
    result = {"role": "assistant", "content": str(message.content or "")}
    if tool_calls:
        result["tool_calls"] = tool_calls  # 有工具调用时挂到 tool_calls 字段
    return result

class MyRolloutProcessor(AbstractRolloutProcessor):
    """Agentic OPD Rollout 处理器。
    传入 tools 参数让学生模型产生原生 tool_call，chat-completions parser 生效，content 干净。"""

    def setup(self) -> None:
        pass  # 初始化钩子，无资源需预热时留空

    @observe_processor  # 装饰后 process 自动接入 Tracing
    async def process(self, input: RolloutInput) -> RolloutOutput:
        started = time.perf_counter()  # 计时起点，用于上报 latency
        try:
            # 1. 取模型资源：api_key/base_url/model_name 来自 RolloutInput.model_resource
            resource = input.model_resource
            api_key = (  # Secret 类型取真实值，普通字符串直用
                resource.api_key.get_secret_value()
                if hasattr(resource.api_key, "get_secret_value")
                else resource.api_key
            )
            sampling = input.sampling_params or {}  # 采样参数字典，可能为空
            # 2. 构造 LLM 客户端：ChatOpenAI 封装 OpenAI 兼容接口
            llm = ChatOpenAI(
                model=resource.model_name,
                openai_api_key=api_key,
                openai_api_base=resource.base_url,
                temperature=float(sampling.get("temperature", 0.2)),
                max_tokens=int(sampling.get("max_tokens", 512)),
                request_timeout=float(sampling.get("timeout", 60.0)),
                extra_body={"enable_thinking": False},  # 关闭思考链输出，content 干净
                streaming=False,  # 非流式，便于一次性取 tool_calls
            )
            # Rollout 自构造 LLM，trace_client 须显式调用，否则请求不产生 LLM Span
            trace_client(llm)
            # 3. 采样：传入 tools 参数注入工具定义，tool_choice=auto 由模型自行决定是否调用
            model = llm.bind_tools(TOOL_DEFINITIONS, tool_choice="auto")
            response = await model.ainvoke(_to_langchain_messages(input.messages))
            latency = round(time.perf_counter() - started, 4)  # 本轮采样耗时（秒）
            # 4. 构造输出：原生 tool_calls 与 rollout_metrics 一并放入 AgentOutput
            return RolloutOutput(
                agent_output=AgentOutput(
                    messages=[*input.messages, _assistant_to_openai(response)],  # 追加学生回复
                    rollout_extra=input.rollout_extra,  # 透传附加信息供 Reward 读取
                    rollout_metrics={
                        "latency": latency,  # 采样延迟
                        "tool_call_count": float(len(response.tool_calls or [])),  # 本轮工具调用次数
                    },
                    reward_score=0.0,  # 占位，由 Reward 覆写
                ),
                status=TaskStatus.SUCCESS,
                error=None,
            )
        except Exception as exc:
            # 5. 异常兜底：返回 ROLLOUT_ERROR 文本 + FAILED，保轨迹不中断，Reward 据前缀跳过评分
            latency = round(time.perf_counter() - started, 4)
            return RolloutOutput(
                agent_output=AgentOutput(
                    messages=[
                        *input.messages,
                        {"role": "assistant", "content": "ROLLOUT_ERROR: rollout failed"},
                    ],
                    rollout_extra=input.rollout_extra,
                    rollout_metrics={"latency": latency, "tool_call_count": 0.0},
                    reward_score=0.0,
                ),
                status=TaskStatus.FAILED,
                error=type(exc).__name__,  # 上报异常类型名，便于排查
            )
```

RolloutInput 与 AgentOutput 字段表：

**字段**

**来源**

**含义**

`model_resource`

RolloutInput

含 api\_key/base\_url/model\_name，构造 ChatOpenAI

`sampling_params`

RolloutInput

temperature/max\_tokens/timeout 等采样参数

`messages`

RolloutInput

输入对话列表，含 system/user/assistant

`rollout_extra`

RolloutInput

透传到 AgentOutput，供 Reward 读取

`messages`

AgentOutput

输出对话，末轮 assistant 含 tool\_calls

`rollout_metrics`

AgentOutput

上报 latency（秒）与 tool\_call\_count（float）

`reward_score`

AgentOutput

占位 0.0，由 Reward 覆写

`status`

RolloutOutput

SUCCESS 或 FAILED

`error`

RolloutOutput

异常类型名，正常时为 None

### Tracing 接入

Rollout 自构造 LLM 客户端，与 Reward（`@observe_processor` 隐式注入）不同，需显式调用 `trace_client` 包装客户端。接入步骤：

1.  从 `RolloutInput` 取 `model_resource`（含 api\_key/base\_url/model\_name）与 `sampling_params`，构造 LLM 客户端（如 `ChatOpenAI`）
2.  调用 `trace_client(llm)` 包装——之后该客户端的所有 LLM 请求自动产生 LLM Span（记录模型名、请求内容、Token 用量、延迟）
3.  包装后再传入 `tools` 参数并 `ainvoke` 采样

最小片段（完整代码见[Rollout 函数结构](#rollout-structure)）：

```
from langchain_openai import ChatOpenAI
from dashscope.finetune.reinforcement.component.observability import trace_client

resource = input.model_resource  # 从 RolloutInput 取模型凭证与地址
llm = ChatOpenAI(model=resource.model_name, openai_api_key=resource.api_key,
                 openai_api_base=resource.base_url, temperature=0.2, max_tokens=512)
trace_client(llm)  # 包装后该客户端所有 LLM 请求自动产生 LLM Span（模型名/Token/延迟）
model = llm.bind_tools(TOOL_DEFINITIONS, tool_choice="auto")  # 传入 tools 参数注入工具定义
response = await model.ainvoke(messages)  # 异步采样，返回含 tool_calls 的 AIMessage
```

示例用 LangChain 的 `ChatOpenAI`（推荐，封装 OpenAI 兼容接口）；也可直接用 `openai` SDK，替换 `ChatOpenAI` 及消息类即可。

不调用 `trace_client` 则 LLM 请求不产生 Span，轨迹页看不到工具调用链（训练不受影响）。完整 Tracing 配置（装饰器、Span 类型、指标路径）见[可观测配置](opd-observable-config.md)。

## 无 Reward 开发参考

不启用 Reward 时 functions 列表只含 Rollout 组件，教师模型蒸馏为唯一监督信号。用 `AgenticRL` 客户端提交，functions 列表只含 `RolloutFunctionComponent`，不传 `RewardFunctionComponent`。构造 `function_components` 指定工作目录与 classpath，配置 `teacher_model`（教师模型）与学生模型、数据集路径、资源规格。`teacher_model` 字段触发蒸馏，超参配置见[训练配置](opd-training-config.md)。

```
# 通用化 Agentic OPD 提交脚本（不启用 Reward）
import asyncio
from pathlib import Path
from dashscope.finetune.agentic_rl import AgenticRL  # Agentic RL/OPD 提交客户端
from dashscope.finetune.reinforcement import (
    DataSourceType,            # 数据源类型枚举（FILE_ID 表示按文件 ID 传数据）
    FunctionComponentModel,    # 组件模型：指定打包目录与 classpath
    FunctionComponentRuntime,  # 组件运行时：cpu/内存/并发等规格
    RolloutFunctionComponent,  # Rollout 组件，functions 列表元素之一
    TrainingDataset,
    ValidationDataset,
)

# 工作目录：须含 functions/ 子包 + requirements.txt，提交时整体打包上传
WORKSPACE = Path(__file__).resolve().parent

def build_runtime():
    """函数运行时资源规格。"""
    return {
        "cpu": 2,                       # vCPU 数
        "memory_size": 4096,            # 内存（MB）
        "disk_size": 512,               # 磁盘（MB）
        "concurrency": 20,              # 单实例并发请求数
        "capacity": 10,                 # 初始实例数
        "min_capacity": 10,             # 最小实例数（缩容下限）
        "max_capacity": 30,            # 最大实例数（扩容上限）
        "memory_scale_threshold": 0.6,  # 内存利用率达 60% 触发扩容
        "concurrency_scale_threshold": 0.6,  # 并发利用率达 60% 触发扩容
        "env": {},                      # 注入函数运行环境的环境变量
    }

async def submit():
    client = AgenticRL()
    # 不启用 Reward：functions 只含 RolloutFunctionComponent
    function_components = [
        RolloutFunctionComponent(
            name="my-rollout",           # 组件名，需在 functions 列表内唯一
            timeout=120,                 # 单次采样超时（秒），超时计 FAILED
            fcmodel=FunctionComponentModel(
                zipdir=str(WORKSPACE.resolve()),  # 打包根目录（含 functions/）
                classpath="functions.rollout.my_rollout.MyRolloutProcessor",  # 处理器全限定类名
            ),
            runtime=FunctionComponentRuntime(**build_runtime()),
        ),
    ]
    result = await client.run(
        job_name="my-agentic-opd",
        model="<student-model-id>",          # 学生模型 ID，被蒸馏对象
        teacher_model="<teacher-model-id>",  # 教师模型 ID，触发蒸馏
        training_datasets=[
            TrainingDataset(
                data_source_type=DataSourceType.FILE_ID,
                file_name=str(WORKSPACE / "data" / "train.jsonl"),  # 训练集 JSONL 路径
            )
        ],
        validation_datasets=[
            ValidationDataset(
                data_source_type=DataSourceType.FILE_ID,
                file_name=str(WORKSPACE / "data" / "validation.jsonl"),  # 验证集 JSONL 路径
            )
        ],
        functions=function_components,
        hyper_parameters={
            # 超参与 opd_teacher_* 部署参数见训练配置
        },
        resources={
            "charge_type": "mtu_postpaid",  # 计费方式：MTU 后付费
            "mtu_spec_code": "MTU4",        # MTU 规格编码
            "mtu_capacity": 24,            # MTU 容量
        },
    )
    if result.status_code != 200:  # 非 200 视为提交失败，抛错便于上层捕获
        raise RuntimeError(f"submission failed: status={result.status_code}")
    return result.output.job_id  # 返回训练任务 ID

if __name__ == "__main__":
    print(f"job_id={asyncio.run(submit())}")  # 同步等待异步提交完成并打印 job_id
```

## 启用 Reward 开发

Reward 为可选组件，启用后在 functions 列表中追加 `RewardFunctionComponent`。Agentic Reward 比 Model OPD 更简洁：经由 chat-completions 接口，解析器（parser）生效，输出内容（content）干净无需剥离思考文本。

### Reward 函数结构

继承 `AbstractRewardProcessor`，实现 `async process(input: RewardInput) -> RewardOutput`，`@observe_processor` 装饰 `process`（自动接入 Tracing）。process 做五件事：

1.  **跳过失败样本**：Rollout 失败时（末轮 content 以 `ROLLOUT_ERROR:` 开头）直接返回 0 分，不评分
2.  **取标准答案**：`ground_truth`（评分基准，优先从 `RewardInput` 取，缺失时从数据的 `rollout_extra.solution` 读）
3.  **取学生输出**：从末轮 assistant 消息取 `tool_calls`（学生模型产生的工具调用）
4.  **评分**：对比标准答案与学生输出，算出 `reward_score`（主分）与 `reward_metrics`（各维度分）
5.  **构造返回**：`reward_score` 单独放 `Reward.reward_score`，其余维度进 `reward_metrics`，包装成 `RewardOutput`

`agent_output`（学生输出）由 Rollout 产出，Reward 只读不写。完整 Tracing 配置见[可观测配置](opd-observable-config.md)。

```
# 通用化 Agentic OPD Reward 处理器模板
import json
from typing import Any, Iterable, Mapping
from dashscope.finetune.reinforcement import (
    AbstractRewardProcessor,  # 抽象基类，子类实现 async process
    Reward,        # 评分载体：reward_score 主分 + reward_metrics 各维度
    RewardInput,   # 输入：含 ground_truth 与 agent_output
    RewardOutput,  # 输出：Reward + status + error
    TaskStatus,
)
from dashscope.finetune.reinforcement.component.observability import observe_processor
from functions.tool_spec import DESTRUCTIVE_TOOLS  # 破坏性工具名集合，评分可据此判误调

def _parse_args(value):
    """将 arguments 解析为 dict，支持 dict/JSON 字符串/None。"""
    if isinstance(value, Mapping):
        return dict(value)  # 已是 dict 直接转
    if not value:
        return {}  # None/空串返回空 dict
    parsed = json.loads(str(value))  # JSON 字符串解析
    return dict(parsed) if isinstance(parsed, Mapping) else {}

def _normalized_calls(calls):
    """将 tool_calls 规范化为可比较的排序列表。
    argument 整体序列化相等：json.dumps + sort_keys 后字符串比较。"""
    normalized = []
    for call in calls:
        normalized.append((
            str(call.get("name", "")),  # 工具名
            json.dumps(  # 参数整体序列化为紧凑字符串，键排序后比较
                dict(call.get("arguments") or {}),
                ensure_ascii=False,
                sort_keys=True,        # 键排序消除顺序差异
                separators=(",", ":"),  # 紧凑输出，无多余空白
            ),
        ))
    return sorted(normalized)  # 排序后列表比较，与调用顺序无关

def your_scoring_function(messages, ground_truth):
    """通用评分函数。Agentic 经由 chat-completions，parser 生效，content 干净无需剥离思考文本。
    以下给最小可计算实现（decision + tool_name + argument 三项全对得 1.0），维度与权重按业务扩展。
    返回 dict 含 reward_score（主分）+ 若干自定义维度（float）。"""
    # ground_truth 可能是 dict 或 JSON 字符串，统一成 dict
    expected = (
        ground_truth
        if isinstance(ground_truth, Mapping)
        else json.loads(str(ground_truth))
    )
    # 取末轮 assistant 消息（学生模型的最终输出）
    assistant = next(
        (
            m for m in reversed(messages)
            if str(m.get("role", "")).lower() == "assistant"
        ),
        messages[-1] if messages else {},  # 无 assistant 时退化取末轮
    )
    # 从 tool_calls 提取预测调用（chat-completions parser 生效，结构化提取）
    predicted_calls = []
    for raw in assistant.get("tool_calls") or []:
        func = raw.get("function", raw)  # 兼容扁平结构与 OpenAI 嵌套 function 结构
        predicted_calls.append({
            "name": str(func.get("name", "")),
            "arguments": _parse_args(func.get("arguments")),
        })
    # 最小可计算实现：decision + tool_name + argument 三项全对得 1.0
    exp_decision = str(expected.get("decision", ""))  # 标准决策：tool_call / clarify
    exp_calls = expected.get("tool_calls") or []  # 标准工具调用列表
    # decision_ok：标准要求 tool_call 且学生确有产出调用
    decision_ok = exp_decision == "tool_call" and len(predicted_calls) > 0
    # name_ok：逐个比对工具名是否一致
    name_ok = all(
        pc["name"] == str(ec.get("name", ""))
        for pc, ec in zip(predicted_calls, exp_calls)
    ) if (predicted_calls and exp_calls) else False
    # arg_ok：name 全对后比对参数整体序列化相等
    arg_ok = all(
        _normalized_calls([pc]) == _normalized_calls([{
            "name": str(ec.get("name", "")),
            "arguments": ec.get("arguments", {}),
        }])
        for pc, ec in zip(predicted_calls, exp_calls)
    ) if name_ok else False
    # 主分：三项全对得 1.0，否则 0.0（按业务改加权/连续值）
    reward_score = 1.0 if (decision_ok and name_ok and arg_ok) else 0.0
    return {
        "reward_score": float(reward_score),
        "decision_accuracy": float(decision_ok),          # 决策是否正确（是否该调工具）
        "tool_name_accuracy": float(name_ok),             # 工具名是否选对
        "argument_accuracy": float(arg_ok),               # 参数是否全对
    }

class MyRewardProcessor(AbstractRewardProcessor):
    """Agentic OPD Reward 处理器。
    chat-completions parser 生效，content 干净无需剥离思考文本。"""

    @observe_processor  # 装饰后 process 自动接入 Tracing
    async def process(self, input: RewardInput) -> RewardOutput:
        # 0. Rollout 失败样本跳过评分：检查末轮 content 是否 ROLLOUT_ERROR 兜底前缀
        last_msg = (input.agent_output.messages or [{}])[-1]
        last_content = str(last_msg.get("content", ""))
        if last_content.startswith("ROLLOUT_ERROR:"):
            # Rollout 失败直接返回 0 分，状态 FAILED，不进入评分逻辑
            return RewardOutput(
                reward=Reward(reward_score=0.0, reward_metrics={}),
                status=TaskStatus.FAILED,
                error="rollout failed",
            )
        # 1. 取 ground_truth：优先 RewardInput，缺失时从 rollout_extra.solution 读
        ground_truth = input.ground_truth
        if ground_truth is None and input.agent_output.rollout_extra:
            ground_truth = input.agent_output.rollout_extra.get("solution")
        # 2. 评分：调用评分函数得到主分 + 各维度 dict
        metrics = your_scoring_function(input.agent_output.messages, ground_truth)
        # 3. reward_score 单独经由 Reward.reward_score 上报，其余进 reward_metrics（不重复）
        reward_score = metrics.pop("reward_score")
        return RewardOutput(
            reward=Reward(reward_score=reward_score, reward_metrics=metrics),
            status=TaskStatus.SUCCESS,
            error=None,
        )
```

RewardInput 与 RewardOutput 字段表：

**字段**

**来源**

**含义**

`ground_truth`

RewardInput

评分基准，可为 None

`agent_output`

RewardInput

Rollout 产出，Reward 只读

`messages`

agent\_output.messages

含 tool\_calls 的对话轨迹

`rollout_extra`

agent\_output.rollout\_extra

透传的附加信息，可取 solution

`reward_score`

Reward

主分，单独上报，不进 metrics

`reward_metrics`

Reward

其余维度 dict，每值 float

`status`

RewardOutput

SUCCESS 或 FAILED

`error`

RewardOutput

异常信息，正常时为 None

### 评分逻辑

`reward_score` 为主奖励标量，`reward_metrics` 为附加维度字典（每值 float）。评分函数实现见上方[Reward 函数结构](#reward-structure)节。关键约定：

-   **主分单独上报**：`reward_score` 单独赋给 `Reward.reward_score`，不重复进 `reward_metrics`（`metrics.pop("reward_score")`）
-   **维度自定**：维度与权重由任务定，按业务自行实现
-   **参数比对**：argument 比对用整体序列化相等：`json.dumps(args, sort_keys=True, separators=(",", ":"))` 后字符串比较
-   **聚焦业务约束**：教师模型蒸馏已提供稠密的分布级监督，Reward 不必面面俱到——把精力放在教师模型难以覆盖的业务约束上（如 `safe_action` 是否误调破坏性工具、`format_valid` 格式是否合规）

### 提交启用 Reward 的训练任务

写好 `MyRewardProcessor` 后，在 `functions` 列表中同时注册 `RolloutFunctionComponent` 与 `RewardFunctionComponent` 两个组件。`run()` 一步完成注册 → 上传数据 → 提交任务。

```
from dashscope.finetune.agentic_rl import AgenticRL
from dashscope.finetune.reinforcement import (
    DataSourceType,
    FunctionComponentModel,
    FunctionComponentRuntime,
    RolloutFunctionComponent,
    RewardFunctionComponent,  # Reward 组件，启用 Reward 时追加
    TrainingDataset,
    ValidationDataset,
)

client = AgenticRL()
result = await client.run(
    job_name="my-agentic-opd-reward",
    model="<student-model-id>",          # 学生模型 ID
    teacher_model="<teacher-model-id>",  # 教师模型 ID，触发蒸馏
    training_datasets=[TrainingDataset(
        data_source_type=DataSourceType.FILE_ID,
        file_name="data/train.jsonl")],   # 训练集 JSONL
    validation_datasets=[ValidationDataset(
        data_source_type=DataSourceType.FILE_ID,
        file_name="data/validation.jsonl")],  # 验证集 JSONL
    functions=[
        # Rollout 组件：与无 Reward 模式一致
        RolloutFunctionComponent(
            name="my-rollout", timeout=120,  # 采样超时 120s
            fcmodel=FunctionComponentModel(
                zipdir=".",  # 工作区根目录（含 functions/）
                classpath="functions.rollout.my_rollout.MyRolloutProcessor"),  # Rollout 处理器类
            runtime=FunctionComponentRuntime(
                cpu=2, memory_size=4096, disk_size=512,
                concurrency=20, capacity=10, min_capacity=10, max_capacity=30)),
        # Reward 组件：weight 为奖励权重，多个 Reward 时按权重加权
        RewardFunctionComponent(
            name="my-reward", weight=1.0, timeout=120,  # 权重 1.0，评分超时 120s
            fcmodel=FunctionComponentModel(
                zipdir=".",
                classpath="functions.reward.my_reward.MyRewardProcessor"),  # Reward 处理器类
            runtime=FunctionComponentRuntime(
                cpu=2, memory_size=4096, disk_size=512,
                concurrency=20, capacity=10, min_capacity=10, max_capacity=30)),
    ],
    hyper_parameters={
        # 超参与 opd_teacher_* 部署参数见训练配置
    },
)
```

`RolloutFunctionComponent` 与无 Reward 模式一致，`RewardFunctionComponent` 指向 `MyRewardProcessor` 所在模块。完整字段说明见[训练配置](opd-training-config.md)。

### 函数测试

提交训练前先本地验证评分逻辑与 Rollout 输出结构，避免到训练任务里才发现错误（浪费算力）。

对 `your_scoring_function` 输入样例 messages + ground\_truth，断言 `reward_score` 与各维度值。Rollout 可构造 mock `RolloutInput` 本地调用 `process` 验证输出结构。本地单测只验证函数逻辑，不验证远程训练效果。

测试用 `pytest` 运行（未装先 `pip install pytest`）：

```
# 运行评分函数本地测试，-v 显示每个用例明细
python -m pytest test_scoring.py -v
```

构造 mock `RolloutInput` 调用 Rollout `process`，需填充三个字段：`model_resource`（api\_key/base\_url/model\_name）、`sampling_params`（采样参数）、`messages`（对话列表）。示例：

```
from dashscope.finetune.reinforcement import RolloutInput
from dashscope.finetune.reinforcement.component.data.base_data_model import (
    ModelResource,  # 模型凭证与地址封装
)

# 构造 mock RolloutInput：填充三个必填字段 + 透传的 rollout_extra
mock_input = RolloutInput(
    model_resource=ModelResource(
        model_name="<student-model-id>",       # 学生模型 ID
        base_url="<inference-endpoint>",        # 推理服务地址
        api_key="<your-api-key>",               # 推理服务 API Key
    ),
    sampling_params={"temperature": 0.2, "max_tokens": 512, "timeout": 60.0},  # 采样参数
    messages=[{"role": "user", "content": "查询项目 P100 的状态"}],  # 输入对话
    rollout_extra={"sample_id": "test-001"},  # 附加信息，Reward 也可读
)
output = await MyRolloutProcessor().process(mock_input)  # 本地调用 process，验证输出结构
```
```
# 通用化评分函数本地测试骨架
import json
import unittest
# 按实际落盘路径 import（your_scoring_function 定义见上方 Reward 模板，可抽到 functions/reward/scoring.py 或与处理器同模块）
from functions.reward.scoring import your_scoring_function  # 路径按实际调整

class ScoringTest(unittest.TestCase):
    def test_correct_tool_call(self):
        """工具调用完全匹配时 reward_score 应为 1.0。"""
        # 标准答案：决策为 tool_call，调 query_status 且 item_id=P100
        expected = {
            "decision": "tool_call",
            "tool_calls": [
                {"name": "query_status", "arguments": {"item_id": "P100"}}
            ],
        }
        # 学生输出：与标准完全一致的 tool_calls（OpenAI 嵌套结构）
        messages = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "type": "function",
                        "function": {
                            "name": "query_status",
                            "arguments": '{"item_id": "P100"}',  # JSON 字符串形式
                        },
                    }
                ],
            }
        ]
        score = your_scoring_function(messages, json.dumps(expected))  # expected 传 JSON 字符串也兼容
        self.assertEqual(1.0, score["reward_score"])  # 全对应得满分 1.0

    def test_wrong_argument(self):
        """参数错误时 reward_score 应低于 1.0。"""
        # 标准答案同上
        expected = {
            "decision": "tool_call",
            "tool_calls": [
                {"name": "query_status", "arguments": {"item_id": "P100"}}
            ],
        }
        # 学生输出：工具名对但 item_id 错（P999 ≠ P100）
        messages = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "type": "function",
                        "function": {
                            "name": "query_status",
                            "arguments": '{"item_id": "P999"}',  # 参数值错误
                        },
                    }
                ],
            }
        ]
        score = your_scoring_function(messages, expected)  # expected 传 dict 也兼容
        self.assertLess(score["reward_score"], 1.0)  # 参数错则不得满分

if __name__ == "__main__":
    unittest.main()
```

## 后续步骤

-   训练参数与提交配置 → [在线策略蒸馏训练配置](opd-training-config.md)
-   可观测配置见 [在线策略蒸馏可观测配置](opd-observable-config.md)
-   回顾训练概述 → [在线策略蒸馏训练概述](opd-training-overview.md)

## 常见问题

Agentic OPD 开发中高频遇到的 Rollout 与 Reward 问题排查。

Rollout 频繁触发兜底返回

检查是否传入正确的工具定义列表（`tools` 参数）、`tool_choice` 是否为 auto、api\_key 与 base\_url 是否有效。

tool\_call\_count 为 0

检查工具定义列表是否完整、系统提示词是否明确指示何时调用工具、学生模型是否支持 function calling。

teacher\_model 报错

常见原因：`teacher_model` 填了非百炼登记的模型 ID（如 HuggingFace 仓库名）。排查：改用百炼支持的模型 ID，完整列表与更多原因见 [训练配置常见问题](opd-training-config.md#opd-faq)。

reward\_metrics 不上报或维度缺失

检查 `reward_score` 是否 pop 出来单独经 `Reward.reward_score`，其余维度值是否均为 float；`ground_truth` 是否从 `rollout_extra.solution` 正确读取。

ground\_truth 取不到（为空）

检查数据 JSONL 每条 `rollout_extra.solution` 是否有值。Reward 先从 `input.ground_truth` 取，缺失时回退到 `input.agent_output.rollout_extra.solution`；两者都空则评分为 0。

本地测试报 ModuleNotFoundError

确认 `functions/` 目录含 `__init__.py`（使目录成为可导入的 Python 包）；`classpath` 与文件路径对齐，如 `functions.rollout.my_rollout.MyRolloutProcessor` 对应 `functions/rollout/my_rollout.py` 内的 `MyRolloutProcessor` 类。
