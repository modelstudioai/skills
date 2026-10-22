# 添加轨迹评测数据

轨迹数据结构说明与轨迹评测集数据添加方式

轨迹（Trajectory）是 AI Agent 在任务执行过程中生成的结构化时序数据，完整记录从接收用户指令开始，Agent 在多轮交互中进行的思考、行动和观察。轨迹评测用于评估 Agent 执行过程的可靠性，例如步骤逻辑是否通顺、是否存在无关冗余步骤，与仅评估最终输出互补。

## 什么是轨迹

轨迹数据为 JSON 格式，核心字段包括：

字段

说明

schema\_version

轨迹结构版本

session\_id

会话 ID

trajectory\_id

轨迹 ID

agent

执行轨迹的智能体信息（名称、版本等）

steps

步骤列表。每个步骤记录来源（user 或 agent）、消息内容、时间戳及执行详情（Span ID、耗时、Token 消耗等）

extra

轨迹级执行详情：Span 标识、Span 类型、状态、耗时、语义格式（semantic\_profile）及输入输出明细。agent、steps、final\_metrics 下也各含 extra，承载各自的附加信息

final\_metrics

汇总指标，包括总步数、Token 消耗、工具调用次数、首字延迟等

轨迹数据示例（节选）：

```
{
  "schema_version": "ATIF-v1.8",
  "session_id": "0efe2dc279b09aaf9d51b378af01f520",
  "trajectory_id": "0efe2dc279b09aaf9d51b378af01f520:f4f2aa362afe7ae7",
  "agent": {
    "name": "invoke_agent_app",
    "version": "2"
  },
  "steps": [
    {
      "source": "user",
      "message": "Hello",
      "timestamp": "2026-10-13T02:11:36.660Z",
      "step_id": 1
    },
    {
      "source": "agent",
      "message": "Hello! How can I help you?",
      "timestamp": "2026-10-13T02:11:36.660Z",
      "step_id": 2
    }
  ],
  "extra": {
    "span_kind": "CHAIN",
    "operation_type": "invoke_agent_app",
    "duration_ms": 4499,
    "status": "1",
    "semantic_profile": "bailian.trace-atif/v1"
  },
  "final_metrics": {
    "total_steps": 2,
    "total_prompt_tokens": 4984,
    "total_completion_tokens": 52
  }
}
```

**说明**单条新增轨迹数据时，点击**轨迹样例**可插入一条完整示例轨迹，作为手工录入的参考模板。

## 创建轨迹评测集

创建评测集时，场景选择**轨迹**，系统自动生成默认表结构：

列名

数据类型

必填

描述

input

String

是

用户输入

reference\_output

String

否

参考输出

trajectory

轨迹

是

智能体执行轨迹

可在默认表结构上继续编辑列配置。详细步骤参考[创建与管理](raw/_short/agenteval-evaluation-set-946c810bda606877.md)。

## 添加轨迹数据

### 单条新增

在评测集详情页点击**添加数据** > **单条新增**，在弹窗中逐项填写：

-   **input**（String，必填）：用户输入，最多 10000 字符。
-   **reference\_output**（String，选填）：参考输出，最多 10000 字符。
-   **trajectory**（轨迹，必填）：智能体执行轨迹。

trajectory 字段以代码编辑器形式编辑，支持折叠、展开与复制。轨迹字段上方提供以下操作：

-   **轨迹样例**：插入一条示例轨迹 JSON。已有轨迹内容时，插入样例会覆盖当前内容，须在确认弹窗中二次确认。
-   **通过 TraceID 导入**：输入 Trace ID，导入该 Trace 对应的轨迹数据。请确保 Trace 当前有效。
-   **预览**：将当前轨迹数据渲染为 Trace 视图，查看调用链、输入输出、状态、耗时与 Token 消耗等详情。

**警告**轨迹数据须为合法的 JSON 对象，单条轨迹大小不能超过 1 MB，否则无法保存。

### 批量导入

在评测集详情页点击**添加数据** > **批量导入**：

1.  上传本地文件。支持 .xls、.xlsx、.csv 格式，单个文件最大 20 MB。
2.  选择导入方式：**追加数据**（保留已有数据，新数据追加到评测集末尾）或**全量覆盖**（清空已有数据后写入）。
3.  配置列映射：将文件中的数据列映射到评测集的数据列，并核对字段类型一致。

**说明**导入过程中如存在失败数据，可在导入结果中下载日志查看失败原因。

## 通过 Trace 回流评测数据

应用观测中的 Trace 可直接导出为轨迹评测数据：在应用观测的 Trace 列表批量选择 Trace，配置 Trace 字段与评测集字段的映射关系，导入评测集。操作步骤参考[应用观测](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)中的添加到评测集。
