# RunDocSummary - 文档摘要

针对一篇文章、视频或者URL，生成文章的摘要内容，即全文总结。此外支持多种多语言的输入和输出。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocSummary)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocSummary)

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

aimiaobi:RunDocSummary

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /miaodu/stream/runDocSummary HTTP/1.1
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

阿里云百炼业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。

llm-2setzb9x4ewsd

SessionId

string

是

对话 ID

0f56f98a-f2d8-47ec-98e9-1cbdcffa9539

DocId

string

否

文档 ID

12345

Query

string

否

自定义要求

请总结一下这篇文档

RecommendContent

string

否

要总结的内容

要总结的内容

CleanCache

boolean

否

清除当前缓存

true

ModelName

string

否

用户自定义模型名称

quanmiao-max、quanmiao-plus

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Header

object

响应头

ErrorCode

string

错误码

success

ErrorMessage

string

错误信息

success

Event

string

事件类型

task-started

EventInfo

string

事件描述

模型生成事件

SessionId

string

会话 ID

92e16ccb-92b6-4894-abbf-fc6e2929a0df

TaskId

string

任务 ID

b057f2fa-2277-477b-babf-cbc062307828

TraceId

string

全链路 ID

2150451a17191950923411783e2927

Payload

object

响应体

Output

object

输出

Content

string

总结内容

总结内容

Usage

object

大模型 token 用量信息

InputTokens

long

输入使用的 Token 数量

100

OutputTokens

long

输出 Token 数量

100

TotalTokens

long

总 oken 数量

200

RequestId

string

请求 Id

3259D344-E871-5DE0-8FFE-CDA21F8D4382

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "success",
    "ErrorMessage": "success",
    "Event": "task-started",
    "EventInfo": "模型生成事件",
    "SessionId": "92e16ccb-92b6-4894-abbf-fc6e2929a0df",
    "TaskId": "b057f2fa-2277-477b-babf-cbc062307828",
    "TraceId": "2150451a17191950923411783e2927"
  },
  "Payload": {
    "Output": {
      "Content": "总结内容"
    },
    "Usage": {
      "InputTokens": 100,
      "OutputTokens": 100,
      "TotalTokens": 200
    }
  },
  "RequestId": "3259D344-E871-5DE0-8FFE-CDA21F8D4382"
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
