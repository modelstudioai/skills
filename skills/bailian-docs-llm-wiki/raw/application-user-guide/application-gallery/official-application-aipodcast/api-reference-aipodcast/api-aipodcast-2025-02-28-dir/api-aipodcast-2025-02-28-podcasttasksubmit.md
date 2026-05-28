# PodcastTaskSubmit - 播客任务提交

ai播客生成任务提交。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AIPodcast/2025-02-28/PodcastTaskSubmit)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AIPodcast/2025-02-28/PodcastTaskSubmit)

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

aipodcast:PodcastTaskSubmit

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /podcast/task/submit HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

当前请求所使用的百炼业务空间 id

llm-ep8ba0dr6seiddxx

fileUrls

array

否

用播客任务生成的文件可访问链接

string

否

文件可访问链接

http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202503241702148295/script.txt?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1742810622&Signature=TBBdikHzOWW3YqDw3sNMTXiMo6A%3D

topic

string

否

播客内容生成的主题

甲流来袭，我们该如何应对？

counts

integer

否

对话人数

枚举值：

-   1：单人。
-   2：双人。

2

voices

array

否

指定播客生成的人声音色，数组中的起始音色，为第一个对话人的音色

枚举值：

-   Dylan：北京话-男声。
-   en\_female：女声。
-   Cherry：女声。
-   Ethan：男声。
-   news\_male：男声。
-   Jada：吴语-女声。
-   Chelsie：女声。
-   en\_male：男声。
-   news\_female：女声。
-   Serena：女声。
-   Sunny：四川话-女声。

string

否

人声音色

news\_female

text

string

否

文案

最近，甲型流感似乎成了大家热议的话题。但你真的了解甲流吗？它和普通感冒有什么区别？为什么症状看起来如此严重？更重要的是，我们应该如何预防和治疗？本期对话中，我们将深入探讨甲流的传播方式、易感人群以及科学的防护措施，帮助你在流感高发季节保护自己和家人的健康。

sourceLang

string

否

播客内容生成的结果（包含播客稿、播客音频）语种选型，目前仅支持中文及英文，默认语种为中文。

zh

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

code

string

响应状态码。

"success"

message

string

响应消息。

"success"

requestId

string

请求 id，用于追溯 API 调用链路。

9CE5B91A-6E6B-55FB-A1AF-037DF01C84B3

success

boolean

true 接口调用成功，false 接口调用失败

True

httpStatusCode

string

HTTP 状态码。

200

data

object

返回数据

taskId

string

任务唯一标识

63c4e0eaab3b4c0db208ecafa990e8d1

taskStatus

string

任务状态。

-   PENDING：待执行
-   RUNNING：执行中
-   SUCCEEDED：成功
-   INVALID：失效
-   FAILED：失败
-   UNKNOWN： 未知

SUCCEEDED

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "success",
  "message": "success",
  "requestId": "9CE5B91A-6E6B-55FB-A1AF-037DF01C84B3",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "taskId": "63c4e0eaab3b4c0db208ecafa990e8d1",
    "taskStatus": "SUCCEEDED"
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AIPodcast/2025-02-28/errorCode>)查看更多错误码。
