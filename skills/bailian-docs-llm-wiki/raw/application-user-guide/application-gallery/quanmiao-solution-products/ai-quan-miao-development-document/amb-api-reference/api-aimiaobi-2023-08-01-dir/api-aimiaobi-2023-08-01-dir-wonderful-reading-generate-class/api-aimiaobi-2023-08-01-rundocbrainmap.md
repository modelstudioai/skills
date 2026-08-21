# RunDocBrainmap - 全文脑图

针对文章或者书，生成三级脑图，且支持生成多语种，支持控制脑图第二级数量，支持控制叶子节点的字数。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocBrainmap)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocBrainmap)

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

aimiaobi:RunDocBrainmap

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /miaodu/stream/runDocBrainmap HTTP/1.1
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

阿里云百炼业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

SessionId

string

是

会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

DocId

string

是

文档 ID

12345

Prompt

string

否

脑图自定义 prompt 要求

请按英文输出

CleanCache

boolean

否

是否清理掉之前的缓存

true

NodeNumber

integer

否

第二级有几个节点

3

WordNumber

integer

否

节点文字的个数

20

referenceContent

string

否

要生成脑图的内容，优先级高于 docId

要生成脑图的内容

ModelName

string

否

用户自定义模型名称

quanmiao-max、quanmiao-plus

ResponseFormat

integer

否

0

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

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

task-failed

EventInfo

string

事件描述

模型生成事件

SessionId

string

会话 ID

07181f55-2311-48af-8048-132a77dee020

TaskId

string

任务 ID

161816

TraceId

string

全链路 ID

6427cdf4-2ffe-4d05-b0ef-c4adceea90f4

Payload

object

响应体

Output

object

输出

Content

string

脑图 json 内容

{"xxxx":"xxx"}

Usage

object

token 消耗

InputTokens

integer

输入使用的 Token 数量

65

OutputTokens

integer

输出 Token 数量

100

TotalTokens

integer

总 oken 数量

165

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
    "Event": "task-failed",
    "EventInfo": "模型生成事件",
    "SessionId": "07181f55-2311-48af-8048-132a77dee020",
    "TaskId": "161816",
    "TraceId": "6427cdf4-2ffe-4d05-b0ef-c4adceea90f4"
  },
  "Payload": {
    "Output": {
      "Content": "{\"xxxx\":\"xxx\"}"
    },
    "Usage": {
      "InputTokens": 65,
      "OutputTokens": 100,
      "TotalTokens": 165
    }
  },
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5"
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunDocBrainmap#workbench-doc-change-demo)。
