# RunDocTranslation - 文档翻译

中英文互译接口。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocTranslation)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocTranslation)

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

aimiaobi:RunDocTranslation

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /miaodu/stream/runDocTranslation HTTP/1.1
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

llm-xxx

SessionId

string

是

对话 ID

2e6b3987-f743-4d4c-8326-d9c41a6af3ee

DocId

string

否

文档 ID

12345

TransType

string

否

翻译方式

toChinese toEnglish toJapenese toRussian toFrench toGerman toItalian toKorean toSpanish toPortuguese

RecommendContent

string

否

要翻译的内容

要翻译的内容

CleanCache

boolean

否

是否清除当前缓存

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

错误码消息

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

411c4dfa-2168-4379-a902-675d67f453f8

TaskId

string

任务 ID

50a1cc8e-717e-4a2b-a76b-dc9734a8564b

TraceId

string

全链路 ID

ebd19b12-0cae-488f-9e41-5a1c825f545b

Payload

object

响应体

Output

object

输出

Content

string

翻译内容

翻译内容

Usage

object

token 用量

InputTokens

long

输入使用的 Token 数量

100

OutputTokens

long

输出使用的 Token 数量

100

TotalTokens

long

本次调用使用的所有 Token 数总和

200

RequestId

string

请求 Id

1813ceee-7fe5-41b4-87e5-982a4d18cca5

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
    "SessionId": "411c4dfa-2168-4379-a902-675d67f453f8",
    "TaskId": "50a1cc8e-717e-4a2b-a76b-dc9734a8564b",
    "TraceId": "ebd19b12-0cae-488f-9e41-5a1c825f545b"
  },
  "Payload": {
    "Output": {
      "Content": "翻译内容"
    },
    "Usage": {
      "InputTokens": 100,
      "OutputTokens": 100,
      "TotalTokens": 200
    }
  },
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5"
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
