# Agent

智能体是一份可复用的配置：模型、系统提示词、工具包、技能。每次更新自动递增版本号，会话创建时锁定当时版本。

## 版本机制

智能体使用 `version` 整数字段跟踪配置历史，行为如下：

-   更新接口采用**全量替换**语义，成功后 `version` 自动 +1，请求体需带当前值用作乐观锁，不一致返回 409。
-   会话创建时锁定当时 `version`，已有会话不受后续更新影响；查询历史版本通过 `GET /agents/{agent_id}?version=N`。
-   归档为软操作，`archived_at` 被填入归档时间；归档后不可用于新建会话，已有会话不受影响。

## 智能体操作

**操作**

**端点**

**说明**

[创建 Agent](https://help.aliyun.com/zh/model-studio/agent-create)

`POST /agents`

创建智能体，初始 `version` 为 1

[获取 Agent](https://help.aliyun.com/zh/model-studio/agent-get)

`GET /agents/{agent_id}`

默认返回最新版本；带 `?version=N` 查询历史版本

[列出 Agent](https://help.aliyun.com/zh/model-studio/agent-list)

`GET /agents`

分页列出工作空间下的智能体，默认不含已归档

[更新 Agent](https://help.aliyun.com/zh/model-studio/agent-update)

`POST /agents/{agent_id}`

全量替换；请求体需带 `version` 作乐观锁，成功后递增

[归档 Agent](https://help.aliyun.com/zh/model-studio/agent-archive)

`POST /agents/{agent_id}/archive`

软归档；不可用于新建会话，已有会话不受影响

[列出 Agent 版本](https://help.aliyun.com/zh/model-studio/agent-versions)

`GET /agents/{agent_id}/versions`

分页返回该智能体的全部历史版本
