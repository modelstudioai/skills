# 强化学习提交前自检

使用 test\_functions 测试体系完成 RL 训练提交前自检：从 Demo 包自带测试工具到自定义函数测试，再到提交前冒烟验证。

RL 训练按**训练单元**小时计费（以 IV 型 24 实例后付费为例，约 984 元/小时），任务启动后才暴露的错误成本最高。提交前的自检以 **test\_functions 测试体系**为主线：先用 Demo 包自带的测试工具验证环境与链路，再测试自定义函数，最后以一次立即取消的冒烟提交确认配置——本地测试免费，冒烟提交约 16 元起，通过后再正式提交。

<a id="demo-包测试工具一览"></a>

<a id="precheck-tools"></a>

## Demo 包测试工具一览

Demo 包（[准备数据与代码](rl-training-overview.md#q1cnqj4wku12f)）自带一整套函数测试设施：

| 工具 | 用途 |
| --- | --- |
| `test_functions.py` | 测试脚本：对 Rollout / Reward / 装饰器 Reward / Group Reward 四类函数各提供独立的「注册 → 远程测试 → 拉取日志」完整闭环 |
| `resources/*.json`（4 份） | 四类函数的测试输入样例（rollout\_input / reward\_input / reward\_decorator\_input / group\_reward\_input），字段结构见下方详解 |
| `cli.sh` | 本地测试与查询命令集合（等效 CLI 入口） |
| `scripts/start_local_*.sh` | 本地启动函数服务脚本（Reward 类可用；Rollout 版脚本的 classpath 指向不存在的模块会启动失败，改用[环境变量方式](rl-pre-submission-checklist.md#precheck-own-local)启动） |

测试输入 JSON 的字段结构与训练期框架下发的请求一致，测试通过即表明函数在训练期的调用行为符合预期。

<a id="测试-demo-函数"></a>

<a id="precheck-demo"></a>

## 测试 Demo 函数

<a id="运行-test-functions-py"></a>

<a id="precheck-demo-run"></a>

### 运行 test\_functions.py

在项目根目录（需设置 `DASHSCOPE_API_KEY` 环境变量，见[环境准备](rl-training-overview.md#wjp6ghg8df9o4)）执行：

<a id="code-block"></a>

```text
python test_functions.py
```

脚本默认只运行 Rollout 测试（`__main__` 中其余三类被注释），测试其余函数时取消对应注释或自行调用：

<a id="code-block-2"></a>

```text
# test_functions.py 末尾 —— 四个测试函数完全独立，删除任一调用不影响其余
asyncio.run(test_rollout(
    classpath="functions.rollout.rollout_only.DemoRolloutProcessor",
    input_path="./resources/rollout_input.json"))
# asyncio.run(test_reward(
#     classpath="functions.reward.reward.DemoRewardProcessor",
#     input_path="./resources/reward_input.json"))
# asyncio.run(test_reward_decorator(
#     classpath="functions/reward/reward_decorator.py:SafetyProcessor",
#     input_path="./resources/reward_decorator_input.json"))
# asyncio.run(test_group_reward(
#     classpath="functions.reward.group_reward.DemoGroupRewardProcessor",
#     input_path="./resources/group_reward_input.json"))
```

每个测试函数内部是一个完整闭环：

<a id="code-block-3"></a>

```text
注册函数（register_functions，lazy_load=False 立即拉起实例）
    → 拿到 instance_id
    → 远程调用（test_functions 发送测试输入）
    → 拉取实例日志（query_all_function_instance_logs）
```

<a id="测试输入字段详解"></a>

<a id="precheck-demo-input"></a>

### 测试输入字段详解

四份测试输入的顶层字段：

| 字段 | 适用函数 | 说明 |
| --- | --- | --- |
| `func_type` | 全部 | 函数类型：rollout / reward / group\_reward（装饰器 Reward 填 reward） |
| `messages` | Rollout | 对话消息列表，训练期来自数据集每行的 messages 字段 |
| `ground_truth` | 全部 | 参考答案，评分逻辑可读取（训练期取值链路见开发指南 RewardInput 字段说明） |
| `rollout_extra` | Rollout | 数据集 rollout\_extra 的透传内容，自定义业务数据 |
| `sampling_params` | Rollout | 采样参数：temperature、max\_tokens、max\_turns、timeout |
| `model_resource` | Rollout | 推理端点：model\_name、base\_url、api\_key（训练期由框架自动注入，测试时需自填可用端点；示例值见[开发指南 — 测试输入格式](rl-function-development-guide.md#1xmfkk4iqijlr)） |
| `agent_output` | Reward 类 | 被评分的 Agent 输出：messages、rollout\_extra、rollout\_metrics、reward\_score |
| `agent_outputs` | Group Reward | 同一样本多条输出的数组（复数），与单条 agent\_output 区分 |
| `request_metadata` | 可选 | 框架元信息（job\_id、sample\_id 等），测试时可省略或填占位值 |
| `tools` | Rollout 可选 | 可用工具列表，无工具传 null |
| `additional_field` | 可选 | 任意自定义附加字段，框架原样传入 |

<a id="预期返回值"></a>

<a id="precheck-demo-expected"></a>

### 预期返回值

四份 Demo 测试输入的实测返回（本地服务与云端 test\_functions 双端一致）：

| 测试输入 | 被测函数 | 预期返回 |
| --- | --- | --- |
| rollout\_input.json | DemoRolloutProcessor | status=success，reward\_score=0.95（Rollout 内嵌评分逻辑，测试输入使用占位推理端点，不实际调用推理） |
| reward\_input.json | DemoRewardProcessor | status=success，reward\_score=0.0，reward\_metrics 含 test1/test2 |
| reward\_decorator\_input.json | SafetyProcessor（装饰器） | status=success，reward\_score=0.85（子维度加权聚合结果） |
| group\_reward\_input.json | DemoGroupRewardProcessor | status=success，rewards 数组长度与 agent\_outputs 一致，单条 0.5 |

返回值与预期不一致时，先核对测试输入是否被改动；输入原样而不一致，则通过[日志查询](rl-pre-submission-checklist.md#precheck-api-logs)定位。

<a id="测试自定义函数"></a>

<a id="precheck-own"></a>

## 测试自定义函数

Demo 四类函数测试全部通过后，环境与链路已验证。将 classpath 换为自定义函数、测试输入换为自构造用例，走同一条测试路径。自定义函数源码放在项目 `functions&#47;` 目录下（classpath 即相对项目根的模块路径，如 `functions&#47;reward&#47;my&#95;reward.py` 对应 `functions.reward.my&#95;reward.MyRewardProcessor`）；注册时 SDK 打包项目代码与 `requirements.txt` 上传，依赖须全部列入 requirements.txt。

<a id="构造测试用例"></a>

<a id="precheck-own-cases"></a>

### 构造测试用例

为自定义评分逻辑构造 3 个可人工推算**预期得分**的测试输入——预期得分以自定义评分逻辑为准：

| 用例 | 构造方法 | 预期得分 |
| --- | --- | --- |
| 满分样例 | messages 中放一条必然命中评分条件的回答（包含正确答案、满足格式），ground\_truth 填对应真值 | 评分逻辑的满分（如 1.0） |
| 零分样例 | messages 中放一条必然不命中的回答（答案错误、格式不符） | 0.0 |
| 边界样例 | 最易判错的形态：空 messages、超长回答、答案部分匹配、大小写不同 | 按已定义的边界行为（边界行为未定义时，先在评分逻辑中补充定义） |

三份输入分别保存（如 `my_reward_test_full.json`、`my_reward_test_zero.json`、`my_reward_test_edge.json`）。Reward 类输入模板（字段结构见[测试输入字段详解](rl-pre-submission-checklist.md#precheck-demo-input)）：

<a id="code-block-4"></a>

```text
{
  "func_type": "reward",
  "ground_truth": "42",
  "agent_output": {
    "messages": [
      {"role": "user", "content": "计算 6 × 7"},
      {"role": "assistant", "content": "### ANSWER: 42 ###"}
    ]
  }
}
```

<a id="本地服务验证"></a>

<a id="precheck-own-local"></a>

### 本地服务验证

远程测试前，先在本地以服务方式运行自定义函数并验证三份用例（Rollout 输入结构见[测试输入字段详解](rl-pre-submission-checklist.md#precheck-demo-input)）。服务启动约需数秒，报 connection refused 时稍候重试：

<a id="code-block-5"></a>

```text
# 终端 1：启动本地函数服务（bash，PROCESSOR_CLASS 换为自定义类）
FUNC_TYPE=reward PROCESSOR_CLASS=functions.reward.my_reward.MyRewardProcessor \
PYTHONPATH=. python -m dashscope.finetune.reinforcement.component.server.server

# 终端 2：逐个发送三份测试用例
curl -X POST http://localhost:8000/api/v1 \
  -H "Content-Type: application/json" \
  -d @my_reward_test_full.json
```

Windows PowerShell 等价命令：

<a id="code-block-6"></a>

```text
# 终端 1
$env:FUNC_TYPE="reward"
$env:PROCESSOR_CLASS="functions.reward.my_reward.MyRewardProcessor"
$env:PYTHONPATH="."
python -m dashscope.finetune.reinforcement.component.server.server

# 终端 2（Windows PowerShell 下 curl 为 Invoke-WebRequest 别名，@file 语法不可用；推荐统一使用 Invoke-RestMethod）
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1 `
  -ContentType "application/json" -InFile my_reward_test_full.json
```

预期返回示例：

<a id="code-block-7"></a>

```text
{"reward": {"reward_score": 1.0, "reward_metrics": {"accuracy": 1.0}},
 "status": "success", "error": null, "error_code": null}
```

**通过标准**：三份输入的返回 `status` 均为 `success`，且 `reward` 中的 `reward_score` 与预期得分逐个一致；任一不一致即为评分逻辑缺陷，修复至一致后再进入远程测试。评分得 0 分属于有效结果——`TaskStatus` 返回 `SUCCESS`；临时性错误（超时、网络抖动）才返回 `FAILED`（详见[开发指南 — 评分场景的 TaskStatus 判定](rl-function-development-guide.md#w7c3666zyodte)）。

Rollout 函数本地实测需将测试输入中的 `model_resource` 换为可用的推理端点与 API Key：须使用支持推理调用的 API Key（在百炼控制台 **API-KEY** 页面创建，`sk-` 前缀）。训练提交所用的凭证若不支持推理调用，此处会返回 401（Incorrect API key）。训练期无需自行配置推理端点——端点与 Key 由训练框架运行时自动注入（见[RolloutInput 关键字段](rl-function-development-guide.md#hsqmkbop4ep9m)）。

评分逻辑设计层面，提交前建议完成两项自检：[Reward 函数撰写前自检（10 问）](rl-function-development-guide.md#wwlu3s40nlo1y)；准备 50-200 条人工标注的 gold set（金标准答案集）用于[评分一致性自检](rl-function-development-guide.md#mzq5byvdu3psw)。同时注意 `reward_metrics` 的字段名保持稳定——改名会中断控制台指标曲线的连续性。

<a id="远程测试自定义函数"></a>

<a id="precheck-own-remote"></a>

### 远程测试自定义函数

将函数注册到云端并在真实 FC 容器中执行——本地与容器环境的差异（依赖安装、打包路径、运行时行为）仅此步骤可暴露（需已设置 `DASHSCOPE_API_KEY` 环境变量，见[环境准备](rl-training-overview.md#wjp6ghg8df9o4)）。首次注册包含函数依赖层构建，约需 1-3 分钟且期间无输出，属正常现象。

<a id="code-block-8"></a>

```text
import asyncio, json
from dashscope.finetune.reinforcement import (
    AgenticRLFunctionComponent, FunctionType, FunctionComponentModel)
from dashscope.finetune.agentic_rl import AgenticRL

async def main():
    client = AgenticRL()
    # 注册自定义函数（classpath 与本地服务为同一字符串）
    ids = await client.register_functions(
        functions=[AgenticRLFunctionComponent(
            type=FunctionType.REWARD,
            fcmodel=FunctionComponentModel(
                classpath="functions.reward.my_reward.MyRewardProcessor"))],
        lazy_load=False)   # 立即拉起实例用于测试
    # ids 为 6 元组：(rollout_entity, reward_entity, group_reward_entity,
    #  rollout_instance, reward_instance, group_reward_instance) 的 ID 列表
    reward_entity_ids, reward_instance_ids = ids[1], ids[4]

    # 逐个发送本地验证过的三份测试用例（input_data 接受 dict）
    for case in ["my_reward_test_full.json", "my_reward_test_zero.json",
                 "my_reward_test_edge.json"]:
        with open(case, "r", encoding="utf-8") as f:
            input_data = json.load(f)
        result = await AgenticRL.test_functions(
            instance_id=reward_instance_ids[0],
            functype=FunctionType.REWARD,
            input_data=input_data,
        )
        print(case, result)

asyncio.run(main())
```

每次 `register_functions` 与每次提交都会注册新的函数实体并累积在账号中（本地项目根目录会生成 `start.sh` 与临时打包文件，可忽略或删除）。测试产生的函数实例可在控制台**函数计算**页面查看与管理。

**通过标准**：三份用例的返回与本地验证结果逐项一致。不一致时优先检查 `requirements.txt`（容器按其安装依赖），再通过实例日志定位（见[日志查询](rl-pre-submission-checklist.md#precheck-api-logs)）——函数实例在启动阶段即失败时日志可能尚未产生（返回空列表），此时以 `test_functions` 返回结果中的错误信息为准。

<a id="test-functions-细节"></a>

<a id="precheck-api"></a>

## test\_functions 细节

<a id="sdk-签名"></a>

<a id="precheck-api-sdk"></a>

### SDK 签名

<a id="code-block-9"></a>

```text
result = await AgenticRL.test_functions(
    instance_id="rw-ins-xxx",     # 注册返回的函数实例 ID
    functype=FunctionType.REWARD, # 函数类型枚举
    input_data=input_data,        # 测试输入（dict，结构见测试输入字段详解）
    pull_logs=True,               # 可选：返回时顺带拉取实例日志
)
```

| 参数 | 说明 |
| --- | --- |
| `instance_id` | 函数实例 ID（ro-ins- / rw-ins- / grw-ins- 前缀），来自 register\_functions 返回值，或 CLI 注册命令输出 |
| `functype` | FunctionType 枚举：ROLLOUT / REWARD / GROUP\_REWARD；注意 SDK 参数名为 functype（CLI 参数名为 --type） |
| `input_data` | 测试输入，dict 类型（从 JSON 文件 json.load 或按字段详解自构造） |
| `pull_logs` | 可选，True 时返回结果附带实例日志 |

`register_functions` 返回 6 元组（rollout/reward/group\_reward 三类的 entity 与 instance ID 列表，未注册类型为空列表）；`lazy_load` 取值语义与完整解包示例见[开发指南 — 注册函数](rl-function-development-guide.md#uvhi6w23xr3dl)。

<a id="cli-对照"></a>

<a id="precheck-api-cli"></a>

### CLI 对照

> **说明**
>
> 本页命令以 `dashscope` 前缀示例（适用于 dashscope 2.0.x）。安装 dashscope 2.1.0 及以上版本时，本文全部 CLI 命令加 `dashscope1` 前缀使用（如 `dashscope1 rl get "ft-xxx"`），参数不变。

| 操作 | 命令 |
| --- | --- |
| 测试函数 | `dashscope rl test_functions "rw-ins-xxx" --type reward --input my_reward_test_full.json`（--type 取值：rollout / reward / group\_reward） |
| 上传数据 | `dashscope rl upload_data --training-files "路径" --validation-files "路径" -o json` |
| 查询任务 | `dashscope rl get "ft-xxx" -o json`（list / cancel / logs 同形式） |

<a id="日志查询"></a>

<a id="precheck-api-logs"></a>

### 日志查询

测试失败时拉取函数实例日志（`query_all_function_instance_logs`）：日志约需 30 秒才就绪（test\_functions.py 的测试函数内置了这一步）；函数实例在启动阶段即失败时日志可能尚未产生（返回空列表），此时以 `test_functions` 返回结果中的错误信息为准。调用方式与完整示例见[开发指南 — 远程测试](rl-function-development-guide.md#qq53zf5yd79le)。

<a id="提交冒烟测试"></a>

<a id="precheck-smoke"></a>

## 提交冒烟测试

函数测试全部通过后，真实提交一次确认服务端接受全部配置，随后立即取消。除下述两项外，参数与正式提交完全一致：`batch_size` 调为 8、数据换成约 10 行的精简文件（数据格式见[数据格式](rl-training-overview.md#5iw0jbydlzmrf)）。完整参数写法见[配置篇 — 一步完成（run）](rl-training-config-monitoring.md#rceg51vlo2i2a)。计费口径：以 24 实例后付费为例约 984 元/小时（后付费最小计费粒度 1 分钟，即约 16 元/分钟）；从提交到取消控制在 1 分钟内约 16 元起，取消动作每延迟 1 分钟增加约 16 元。

<a id="code-block-10"></a>

```text
import asyncio
from dashscope.finetune.agentic_rl import AgenticRL

async def main():
    client = AgenticRL()
    # run 为 async；参数为正式提交的完整参数（函数/数据/超参/资源）
    result = await client.run(
        model="your-model",
        functions=[...], training_datasets=[...], validation_datasets=[...],
        hyper_parameters={...}, resources={...})

    # 先确认提交结果再取 job_id（提交被拒时 output 为空，直接取值会报错）
    if result.status_code != 200:
        print(f"提交被拒: {result.message}")   # 服务端拒绝原因（如 batch_size 超范围）
        return

    # ---- 拿到 job_id 后立即执行以下两行（get/cancel 为同步方法，无需 await）----
    job_id = result.output.job_id
    g = AgenticRL.get(job_id=job_id)      # 回显任务详情，核对超参与资源配置
    c = AgenticRL.cancel(job_id=job_id)   # 立即取消，控制费用

asyncio.run(main())
```

**通过标准**：

-   `run` 正常返回（`status_code` 为 200）且 `job_id` 非空——函数注册、数据上传、参数校验全链路被服务端接受
-   `get` 回显的 `hyper_parameters` 中，未显式填写的字段会被服务端自动补全（如 `enable_thinking`、`max_off_policy_strategy` 等）——核对补全值与预期无冲突
-   核对两项资源配置：`mtu_capacity` = nnodes\_rollout × n\_gpus\_rollout + nnodes\_training × n\_gpus\_training（[分布式并行与资源](rl-training-config-monitoring.md#ngwtolw8f43ih)）；函数 Runtime 的 memory\_size ≥ 4096、disk\_size ≥ 512（[Runtime 资源配置](rl-training-config-monitoring.md#15b4d8fbwsxob)）
-   冒烟场景数据量与 batch\_size 配合：少量数据（如 10 行）即可，此时数据量低于正式提交的 `batch_size`，须同步下调 `batch_size` 至不大于数据行数（服务端要求取值范围 8~2048，[批次与采样参数表](rl-training-config-monitoring.md#hp-batch-sampling)），冒烟设为 8 即可

> **警告**
>
> 拿到 job\_id 后立即执行 cancel——未取消的任务会排队进入 RUNNING 并按训练单元小时计费。若脚本在 cancel 前抛错（如对同步方法误用 await），任务可能已提交但脚本丢失 job\_id，此时通过 `AgenticRL.list()` 找回最新任务再取消。

<a id="首次训练的费用与时长"></a>

<a id="precheck-cost"></a>

## 首次训练的费用与时长

本节为**提交后首次训练**的验收口径（非提交前步骤）：用最小数据量 + 1 个 epoch 实际执行一次训练，确认首个 step 能产出轨迹与指标、Reward 有梯度（非恒 0 恒 1）。

**时长预期**（demo 精简数据 128 条、batch\_size=64、24 实例后付费的实测口径）：

-   提交到进入 RUNNING 约 1 分钟（资源排队正常时）
-   **首个 step 产出轨迹与指标通常需 30 分钟以上**（首个 step 需完成全部 Rollout 采样；实测 25 分钟未见产出属正常现象，勿提前判定失败）
-   完整运行至 SUCCEEDED 约 1 小时 45 分钟

**费用口径**（按训练单元小时计，单价见[训练单元价格](rl-training-overview.md#oqko35akuagq7)）：

-   以「首个 step 指标出现且正常」为停止点，通常在数百元量级；完整运行约千余元
-   任务在进入训练前取消**不计费**（实测 usage 为 0）；进入训练后按实际用量计，任务详情的 `usage` 字段回显累计用量
-   全量训练费用估算：`实例数 × 预计时长 × 小时单价`——预计时长可用「数据量 / batch\_size × 每 step 耗时 × n\_epochs」粗算，或先以精简首跑的实测时长等比放大

首个 step 指标是否正常的判定标准（`critic/rewards/mean`、`actor/entropy` 等健康判据）见[可观测配置 — 关键指标速查](observable-configuration-for-reinforcement-learning.md#o5q4qmcgearll)。具体实践（精简数据集、`n_epochs=1`）见[强化学习训练概述 — 起步技巧](rl-training-overview.md#akqzafaiuln0r)。

完成自检流程后仅变更部分项目时，无需重复全部自检项：

-   **更换数据**（新数据集或数据扩量）→ 重新提交前执行一次冒烟测试即可
-   **修改函数代码** → 从[本地服务验证](rl-pre-submission-checklist.md#precheck-own-local)重起
-   **仅调整超参或资源配置** → 从提交冒烟测试重起（约 16 元验证新配置被服务端接受）

<a id="常见报错速查"></a>

<a id="precheck-errors"></a>

## 常见报错速查

覆盖测试至提交环节的高频报错。任务已进入训练后（首个 step 崩溃、采样超时、输出乱码等）的报错归因，请转[可观测配置 — 问题排查决策树](observable-configuration-for-reinforcement-learning.md#4h2izjeep16wy)。

| 环节 | 错误信息 | 原因分析 | 处理方法 |
| --- | --- | --- | --- |
| 本地服务 | 401 Incorrect API key（Rollout 实测调用） | 所用 Key 不支持推理调用 | 换百炼控制台创建的 sk- 前缀推理 Key（见[本地服务验证](rl-pre-submission-checklist.md#precheck-own-local)） |
| 远程测试 | `Invalid classpath for startup script`（注册即报，路径含反斜杠），或 `Precondition Failed`（test\_functions 返回，实例启动即退出时日志为空） | Windows 打包兼容问题（CLI 与 SDK 共用打包链路，两侧均复现；注册时的 `Temp file cleanup failed` 警告可忽略） | 在 WSL 或 Linux 环境执行可完全规避（未安装 WSL 时可通过 `wsl --install` 安装）；该问题已反馈 DashScope SDK 维护方 |
| 远程测试 | ModuleNotFoundError（实例日志中） | requirements.txt 缺依赖，或包结构无法在容器内解析 | 补齐 requirements.txt 并回到本地服务复现 |
| 提交 | ValidationError: extra inputs are not permitted（如 weight） | 该参数不属于当前组件类型（weight 是 RewardFunctionComponent 的字段，不在 AgenticRLFunctionComponent 上） | 核对组件类型与字段归属；分步提交不带 weight |
| 提交 | \[3005\] Job submission failed: TypeError（unexpected keyword argument） | 调用了不存在的方法参数（如 run(lazy\_load=...)、submit\_job(training\_file\_ids=...)） | 数据集用 datasets=\[Dataset(type=DatasetsType.VALIDATION, data\_source\_type=DataSourceType.FILE\_ID, file\_id=...)\] 完整三参数传入；其余参数以本页与[提交训练任务](rl-training-config-monitoring.md#fvj2mhbpok02o)示例为准 |
| 提交 | \[400\] InvalidParameter：batch\_size need to be in range \[8, 2048\] | batch\_size 超出服务端允许范围（冒烟时数据量少，batch\_size 须调至 8） | 调整 batch\_size 至 8~2048；冒烟场景配合少量数据 |
| 提交 | \[1002\] I/O error: Failed to load from dict | YAML 方言错误（不支持的顶层键或字段类型） | 使用[配置篇 YAML 配置](rl-training-config-monitoring.md#owgwlslyqboyz)的 job.yaml 模板结构 |
| 提交 | TypeError: object FineTune can't be used in 'await' expression | 对同步方法（submit\_job / get / cancel / list / logs）误用 await | 去掉 await；注意 run/register\_functions/upload\_datasets/test\_functions 为 async，任务管理类方法为同步 |

<a id="后续步骤"></a>

<a id="precheck-next"></a>

## 后续步骤

-   自检全过，提交正式训练 → [强化学习训练配置 — 提交与配置](rl-training-config-monitoring.md)
-   函数开发细节与设计哲学 → [强化学习开发指南](rl-function-development-guide.md)
-   训练启动后的指标观察与异常归因 → [强化学习的可观测配置与指标参考](observable-configuration-for-reinforcement-learning.md)
-   回顾端到端流程 → [强化学习训练概述](rl-training-overview.md)
