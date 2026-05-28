# RunCustomHotTopicAnalysis - 自定义热点话题分析

自定义热点话题分析。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunCustomHotTopicAnalysis)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunCustomHotTopicAnalysis)

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

aimiaobi:RunCustomHotTopicAnalysis

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/miaoce/runCustomHotTopicAnalysis HTTP/1.1
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

AskUser

string

否

模型反问

模型反问

UserBack

string

否

用户针对模型反问的输入

用户针对模型反问的输入

Prompt

string

是

用户输入 Prompt

用户输入Prompt

ForceAnalysisExistsTopic

boolean

否

针对重复的话题，是否强制分析并覆盖已有的话题分析

false

SessionId

string

否

每次请求唯一标识

3f7045e099474ba28ceca1b4eb6d6e21

TaskId

string

否

整轮对话任务唯一标识

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

3f7045e099474ba28ceca1b4eb6d6e21

## 返回参数

名称

类型

描述

示例值

object

CustomHoTTopicBaseLlmResponse

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

Articles

array<object>

参照文章

Article

object

文章对象

Author

string

作者

作者

Content

string

内容

文章内容

DocId

string

文档-自定义的唯一 ID

文档-自定义的唯一ID

DocUuid

string

内部文档唯一标识

a2103fcfbd5441f1991c72f8834833e3

PubTime

string

发布时间

2024-08-27 14:50:47

Source

string

来源

央视网

Summary

string

文章摘要

文章摘要

Tag

string

标签

文章标签

Title

string

标题

文章标题

Url

string

文章 URL

https://www.example.com/aaa.docx

AskUser

array

反问列表

AskUser

string

模型反问

xxx

AsyncTaskId

string

异步任务 ID

异步任务ID

Attitude

string

自定义选题视角

自定义选题视角

SearchQuery

string

query 改写结果

大模型改变世界

Text

string

文本生成结果

文本生成结果

TopicId

string

话题 ID

话题ID

Usage

object

token 使用量

InputTokens

long

输入使用的 Token 数量

60

OutputTokens

long

输出 Token 数量

13

TotalTokens

long

总 token 数量

73

RequestId

string

请求 ID

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
      "Articles": [
        {
          "Author": "作者",
          "Content": "文章内容",
          "DocId": "文档-自定义的唯一ID",
          "DocUuid": "a2103fcfbd5441f1991c72f8834833e3",
          "PubTime": "2024-08-27 14:50:47",
          "Source": "央视网",
          "Summary": "文章摘要",
          "Tag": "文章标签",
          "Title": "文章标题",
          "Url": "https://www.example.com/aaa.docx"
        }
      ],
      "AskUser": [
        "xxx"
      ],
      "AsyncTaskId": "异步任务ID",
      "Attitude": "自定义选题视角",
      "SearchQuery": "大模型改变世界",
      "Text": "文本生成结果",
      "TopicId": "话题ID"
    },
    "Usage": {
      "InputTokens": 60,
      "OutputTokens": 13,
      "TotalTokens": 73
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
