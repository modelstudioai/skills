# RunMultiDocIntroduction - 多文档聚合摘要

针对多篇文章、视频或者URL，生成总分结构的摘要（几篇文章的综合概述、关键要点）。此外支持多种多语言的输入和输出。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunMultiDocIntroduction)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunMultiDocIntroduction)

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

aimiaobi:RunMultiDocIntroduction

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /miaodu/stream/runMultiDocIntroduction HTTP/1.1
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

llm-2setzb9x4ewsd

DocIds

array

是

多个文档 Id 数组

string

是

文档 Id

10022

SessionId

string

是

对话 ID

75bf82fa-b71b-45d7-ae40-0b00e496cd9e

SummaryPrompt

string

否

摘要-自定义 Prompt

请简明扼要

KeyPointPrompt

string

否

重点-自定义 Prompt

请简明扼要

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

RequestId

string

Id of the request

3f7045e099474ba28ceca1b4eb6d6e21

Header

object

响应头

ErrorCode

string

错误码

200

ErrorMessage

string

错误信息。

Message does not exist.

Event

string

SSE 事件。

finished

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

46e5c2b5-0877-4f09-bd91-ab0cf314e48b

Payload

object

响应体

Output

object

输出

Summary

string

大纲摘要

大纲摘要内容

KeyPoints

array<object>

关键点信息。

KeyPoints

object

关键点信息。

KeyPoint

string

关键点信息

关键点信息

Source

string

信息来源

信息来源

Usage

object

token 用量

InputTokens

long

输入 Token 数量

65

OutputTokens

long

输出 Token 数量

100

TotalTokens

long

总 Token 数量

165

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Header": {
    "ErrorCode": 200,
    "ErrorMessage": "Message does not exist.",
    "Event": "finished",
    "EventInfo": "模型生成事件",
    "SessionId": "92e16ccb-92b6-4894-abbf-fc6e2929a0df",
    "TaskId": "b057f2fa-2277-477b-babf-cbc062307828",
    "TraceId": "46e5c2b5-0877-4f09-bd91-ab0cf314e48b"
  },
  "Payload": {
    "Output": {
      "Summary": "大纲摘要内容",
      "KeyPoints": [
        {
          "KeyPoint": "关键点信息",
          "Source": "信息来源"
        }
      ]
    },
    "Usage": {
      "InputTokens": 65,
      "OutputTokens": 100,
      "TotalTokens": 165
    }
  }
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
