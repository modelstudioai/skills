# RunBookIntroduction - 书籍导读（抽取书籍卖点/书籍摘要）

基于一本书，抽取书籍的内容概要，以及结构化的卖点、热词信息。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunBookIntroduction)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunBookIntroduction)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

aimiaobi:RunBookIntroduction

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /miaodu/stream/runBookIntroduction HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-vtmox6g2bhq2qv5c

DocId

string

是

文档 ID

3YQRatoe8phnpIsIE6z7DTPknhG8Fj

SessionId

string

是

对话 ID

0f56f98a-f2d8-47ec-98e9-1cbdcffa9539

SummaryPrompt

string

否

总结自定义要求

用英文输出

KeyPointPrompt

string

否

关键点自定义要求

用英文输出

CleanCache

boolean

否

true

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

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

success

ErrorMessage

string

错误信息。

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

会话 ID

411c4dfa-2168-4379-a902-675d67f453f8

TaskId

string

任务 ID

d3be9981-ca2d-4e17-bf31-1c0a628e9f99

TraceId

string

全链路 ID

46e5c2b5-0877-4f09-bd91-ab0cf314e48b

Payload

object

响应体

Output

object

输出内容对象

Summary

string

书籍简介

简介内容

KeyPoint

string

书籍卖点

卖点内容

Introductions

array<object>

array<object>

Summary

string

本段摘要内容

Title

string

本段标题内容

Blocks

array<object>

object

Height

integer

600

PageId

integer

10

Width

integer

600

X

integer

10

Y

integer

10

BeginTime

integer

0

EndTime

integer

1200

Usage

object

token 用量

InputTokens

integer

输入 Token 数量

100

OutputTokens

integer

输出 Token 数量

100

TotalTokens

integer

总 Token 数量

200

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Header": {
    "ErrorCode": "success",
    "ErrorMessage": "success",
    "Event": "finished",
    "EventInfo": "模型生成事件",
    "SessionId": "411c4dfa-2168-4379-a902-675d67f453f8",
    "TaskId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99",
    "TraceId": "46e5c2b5-0877-4f09-bd91-ab0cf314e48b"
  },
  "Payload": {
    "Output": {
      "Summary": "简介内容",
      "KeyPoint": "卖点内容",
      "Introductions": [
        {
          "Summary": "本段摘要内容",
          "Title": "本段标题内容",
          "Blocks": [
            {
              "Height": 600,
              "PageId": 10,
              "Width": 600,
              "X": 10,
              "Y": 10,
              "BeginTime": 0,
              "EndTime": 1200
            }
          ]
        }
      ]
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

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunBookIntroduction#workbench-doc-change-demo)。
