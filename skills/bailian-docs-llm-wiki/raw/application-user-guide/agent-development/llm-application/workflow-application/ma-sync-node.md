# MA 同步执行节点

向托管智能体（Managed Agent）提交任务，并同步等待最终执行结果，适用于需要在当前流程内拿到执行结果再继续的场景。

## 功能说明

适用于需要在当前流程内拿到 Agent 执行结果再继续的场景，如 Agent 完成多步任务后，结果进入大模型节点生成回复。

## 配置项

配置项

说明

会话模式

默认模式。

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

超时时间

会话执行的超时时间（分钟）。

## 相关文档

-   [Managed Agent 概述](raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-introduction.md)：Managed Agent 的创建与管理。
-   [创建 Session](raw/application-api-reference/managed-agents-api/session-api/session-create.md)：Managed Agent 执行的底层会话机制。
