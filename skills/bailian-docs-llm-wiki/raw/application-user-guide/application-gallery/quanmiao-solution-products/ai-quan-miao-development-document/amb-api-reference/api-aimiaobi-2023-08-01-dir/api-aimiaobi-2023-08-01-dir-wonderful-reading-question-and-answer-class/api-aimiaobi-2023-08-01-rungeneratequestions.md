# RunGenerateQuestions - 猜你想问

输入一个query，返回几个相关query。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunGenerateQuestions)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunGenerateQuestions)

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

aimiaobi:RunGenerateQuestions

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /miaodu/stream/runGenerateQuestions HTTP/1.1
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

llm-w335gauzlbba2vze

SessionId

string

否

对话 ID

f486c4e2-b773-4d65-88f8-2ba540610456

DocId

string

否

文档 ID

oOgIwodFANW1u5MnqxysOh1rtld3xn

ReferenceContent

string

否

要从中提取问题的文档内容，如果不为空则以此文本为准，为空则以 docId 为准

关联内容

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

RateLimit

ErrorMessage

string

调用失败时，返回的出错信息。

success

Event

string

event 名称

finished

EventInfo

string

事件描述

模型生成事件

SessionId

string

会话 ID

3cd10828-0e42-471c-8f1a-931cde20b035

TaskId

string

任务 ID

d3be9981-ca2d-4e17-bf31-1c0a628e9f99

TraceId

string

全链路 ID

0bc3b4b417362160345997589e5f6e

Payload

object

响应体

Output

object

输出

Content

string

问题内容

问题1\\n问题2\\n问题3\\n

Usage

object

token 用量

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

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Header": {
    "ErrorCode": "RateLimit",
    "ErrorMessage": "success",
    "Event": "finished",
    "EventInfo": "模型生成事件",
    "SessionId": "3cd10828-0e42-471c-8f1a-931cde20b035",
    "TaskId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99",
    "TraceId": "0bc3b4b417362160345997589e5f6e"
  },
  "Payload": {
    "Output": {
      "Content": "问题1\\n问题2\\n问题3\\n"
    },
    "Usage": {
      "InputTokens": 100,
      "OutputTokens": 100,
      "TotalTokens": 200
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
