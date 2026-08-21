# RunTextPolishing - 润色

创作-文本润色。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunTextPolishing)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunTextPolishing)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

aimiaobi:RunTextPolishing

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/runTextPolishing HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

Content

string

是

文本内容

文本内容

Prompt

string

否

自定义的润色要求

自定义的润色要求

OriginContent

string

否

原始文章

原始文章内容

TaskId

string

否

任务 ID，（同一个任务 ID 共享会话，任务超时时间 12 个小时）

taskld-xxxxx

## 返回参数

名称

类型

描述

示例值

object

BaseLlmResponse

Header

object

响应头

ErrorCode

string

错误码

错误码

ErrorMessage

string

错误信息

错误信息

Event

string

SSE 事件。task-started:开始，task-finished:结束，task-failed:失败

task-started

OriginSessionId

string

父会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

SessionId

string

会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

TaskId

string

任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

TraceId

string

全链路 ID

全链路ID

Payload

object

响应体

Output

object

输出

Text

string

文本生成结果

文本生成结果

Usage

object

token 消耗

InputTokens

long

输入使用的 Token 数量

1

OutputTokens

long

输出使用的 Token 数量

1

TotalTokens

long

本次调用使用的所有 Token 数总和

2

RequestId

string

请求唯一标识

3f7045e099474ba28ceca1b4eb6d6e21

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "错误码",
    "ErrorMessage": "错误信息",
    "Event": "task-started",
    "OriginSessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TraceId": "全链路ID"
  },
  "Payload": {
    "Output": {
      "Text": "文本生成结果"
    },
    "Usage": {
      "InputTokens": 1,
      "OutputTokens": 1,
      "TotalTokens": 2
    }
  },
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-12-29

OpenAPI 错误码发生变更、OpenAPI 入参发生变更

[查看变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunTextPolishing?updateTime=2025-12-29#workbench-doc-change-demo)

2025-12-25

OpenAPI 错误码发生变更、OpenAPI 入参发生变更

[查看变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunTextPolishing?updateTime=2025-12-25#workbench-doc-change-demo)
