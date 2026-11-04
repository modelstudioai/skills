# MA 异步任务节点

通过提交任务与查询任务的方式处理托管智能体（Managed Agent）的长时间任务，提交后不阻塞当前工作流执行。

## 功能说明

适用于耗时较长的 Agent 任务，如长程工具调用、代码执行。工作流可先行处理其他分支，后续按需查询执行结果；执行记录可在[任务中心](raw/application-user-guide/agent-development/llm-application/flow-agent-task-center.md)查看。

## 配置项

配置项

说明

会话模式

默认模式。

操作类型

提交任务。

Agent

选择要调用的托管智能体，可点击**管理 Agent** 跳转管理页面。

环境

可选。选择会话运行的环境，可点击**管理环境**。

密钥库

可选。选择注入会话的密钥库，可点击**管理密钥库**。

资源

可选。将文件或记忆挂载到会话中，可点击**管理文件**。

环境变量

可选。为会话运行时注入环境变量。

User Message

传给智能体的消息，支持输入 / 插入变量引用上游节点输出。

Agent、环境、密钥库等配置项与 MA 同步执行节点一致，参见[MA 同步执行节点](raw/application-user-guide/agent-development/llm-application/workflow-application/ma-sync-node.md)。

## 相关文档

-   [Managed Agent 概述](raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-introduction.md)：Managed Agent 的创建与管理。
-   [任务中心](raw/application-user-guide/agent-development/llm-application/flow-agent-task-center.md)：异步任务的状态查询与执行记录。
