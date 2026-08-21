# RunKeywordsExtractionGeneration - 关键词抽取

AI妙笔-创作-抽取关键词。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunKeywordsExtractionGeneration)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunKeywordsExtractionGeneration)

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

aimiaobi:RunKeywordsExtractionGeneration

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/runKeywordsExtractionGeneration HTTP/1.1
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

ReferenceData

object

是

生成需要的数据

Contents

array

是

正文列表

string

是

正文

xxx

TaskId

string

否

关联创作文章唯一标识

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

xxx

Prompt

string

否

自定义提示词

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

AccessForbid

ErrorMessage

string

错误信息。

xx

Event

string

SSE 事件。

task-failed

SessionId

string

会话 ID

1a3d7c9f-3a6d-4e49-b176-2d8721a27397

TaskId

string

任务 ID

8d55b429d7c6d321fcff54823e8d317b

TraceId

string

全链路 ID

210bc4e817219607963985396de8bd

Payload

object

响应体

Output

object

输出

Text

string

文本生成结果

xxx

Usage

object

token 用量

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

419F3FBE-5C8D-5949-AC29-E9615235D15A

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "AccessForbid",
    "ErrorMessage": "xx",
    "Event": "task-failed",
    "SessionId": "1a3d7c9f-3a6d-4e49-b176-2d8721a27397",
    "TaskId": "8d55b429d7c6d321fcff54823e8d317b",
    "TraceId": "210bc4e817219607963985396de8bd"
  },
  "Payload": {
    "Output": {
      "Text": "xxx"
    },
    "Usage": {
      "InputTokens": 1,
      "OutputTokens": 1,
      "TotalTokens": 2
    }
  },
  "RequestId": "419F3FBE-5C8D-5949-AC29-E9615235D15A"
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
