# RunDocSmartCard - 文档智能卡片

针对划选的文字或指定chat，自动打标并生成一个卡片笔记。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocSmartCard)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocSmartCard)

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

aimiaobi:RunDocSmartCard

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /miaodu/stream/runDocSmartCard HTTP/1.1
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

DocId

string

是

文档 ID

84ufBYEeLMZOjRFo84HJ7ySL3Efr55

SessionId

string

是

对话 ID

3f7045e099474ba28ceca1b4eb6d6e21

Prompt

string

否

提示词

自定义提示词

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

1813ceee-7fe5-41b4-87e5-982a4d18cca5

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

finished

EventInfo

string

事件描述

模型生成事件

SessionId

string

通话唯一 ID

07181f55-2311-48af-8048-132a77dee020

TaskId

string

任务 ID。

8d55b429d7c6d321fcff54823e8d317b

TraceId

string

全链路 ID

0abb781c17337107444473701ed7c3

Payload

object

响应体

Output

object

输出内容对象

Content

string

卡片标题

标题内容

Tags

array

卡片标签数组

tags

string

卡片标签

标签内容

Usage

object

token 用量

InputTokens

long

输入使用的 Token 数量

1

OutputTokens

long

输出 Token 数量

100

TotalTokens

long

总 token 数量

101

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Header": {
    "ErrorCode": "success",
    "ErrorMessage": "success",
    "Event": "finished",
    "EventInfo": "模型生成事件",
    "SessionId": "07181f55-2311-48af-8048-132a77dee020",
    "TaskId": "8d55b429d7c6d321fcff54823e8d317b",
    "TraceId": "0abb781c17337107444473701ed7c3"
  },
  "Payload": {
    "Output": {
      "Content": "标题内容",
      "Tags": [
        "标签内容"
      ]
    },
    "Usage": {
      "InputTokens": 1,
      "OutputTokens": 100,
      "TotalTokens": 101
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
