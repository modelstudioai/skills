# 任务中心

查看通过异步方式调用智能体应用或工作流应用产生的后台任务，包括任务的执行状态、输入输出与时间信息。

任务中心用于管理通过异步方式调用应用时产生的后台任务。以异步模式调用工作流应用或智能体应用时，系统立即返回 Task ID，任务在后台执行，可在任务中心查看该任务的执行状态与结果。

## 进入任务中心

访问[任务中心](https://bailian.console.aliyun.com/flow-agent/app-task-center)页面，或在控制台左侧导航点击**任务中心**。

## 任务列表

任务列表展示以下列：

列

说明

Task ID

任务的唯一标识，即异步调用返回的 Task ID。

状态

任务的执行状态，取值见下方[任务状态](https://help.aliyun.com/zh/model-studio/flow-agent-task-center#h-fa-tc-status)。

输入

本次任务的请求内容，以 JSON 形式展示。

输出

任务的返回内容，以 JSON 形式展示，包含输出文本与 token 用量等信息。

来源

产生任务的应用类型，包括智能体、工作流和组件。

渠道

任务的发起渠道。通过 API 异步调用产生的任务显示为 **API**。

创建时间

任务的创建时间。

更新时间

任务状态最近一次变更的时间。

操作

点击**详情**查看该任务的完整输入与输出。

## 查找任务

在列表上方的搜索框中输入 Task ID 查找目标任务，点击**重置**清空搜索条件。

## 任务状态

状态

说明

进行中

任务已创建但尚未结束。未调度、已调度、执行中、等待中等内部状态在列表中统一显示为进行中。

成功

任务执行完成，可在**输出**列或详情页查看结果。

失败

任务执行出错，可在**输出**列或详情页查看错误信息。

已取消

任务被取消。通过 API 取消异步任务后，列表中显示为该状态。

已停止

任务被停止。

已删除

任务已删除。

## 相关文档

-   [调用工作流应用](raw/application-user-guide/agent-development/llm-application/bailian-application-calling/invoke-workflow-application.md)：以异步模式调用工作流应用并获取 Task ID。
-   [工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)：异步运行模式的说明。
-   [应用限流](raw/application-user-guide/agent-development/llm-application/bailian-application-calling/flow-agent-rate-limiting.md)：异步任务提交与同步调用共享单应用 QPS 配额。
