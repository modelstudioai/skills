# RunNetworkContentAudit - 网络内容安全审核

轻应用-网络内容审核。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunNetworkContentAudit)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunNetworkContentAudit)

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

quanmiaolightapp:RunNetworkContentAudit

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runNetworkContentAudit HTTP/1.1
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

百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/use-workspace)

llm-xx

modelId

string

否

模型 ID

qwen-max

businessType

string

否

业务类型

clueMining

taskDescription

string

否

任务描述

给你一条待分析文本数据，请你按照标签体系来对数据进行打标。

content

string

是

待分析文本

待分析文本

tags

array<object>

否

标签体系列表

object

否

标签列表。

tagName

string

否

标签名称

xxxx

tagDefinePrompt

string

否

标签定义提示词

xxxx

extraInfo

string

否

额外信息

额外信息

outputFormat

string

否

输出格式

请返回如下JSON格式，{"key1":"","key2":""}

apiKey

string

否

集成接入的 API 密钥。获取[API- KEY](https://help.aliyun.com/zh/model-studio/get-api-key)

sk-60fd85c1a28f4873abb952e954b0ed27

## 返回参数

名称

类型

描述

示例值

object

响应

header

object

消息头

errorCode

string

错误码 code

AccessForbidden

errorMessage

string

错误描述

错误信息

event

string

事件

task-finished

sessionId

string

会话唯一标识

xxxx

taskId

string

任务唯一标识

xxxx

traceId

string

全链路唯一标识

xxxxx

payload

object

消息体

output

object

输出结果

text

string

输出摘要文本

xxxx

usage

object

token 消耗

inputTokens

long

输入 token

100

outputTokens

long

输出 token

100

totalTokens

long

总 token

200

requestId

string

Id of the request

5D0E915E-655D-59A8-894F-93873F73AAE5

## 示例

正常返回示例

`JSON`格式

```
{
  "header": {
    "errorCode": "AccessForbidden",
    "errorMessage": "错误信息",
    "event": "task-finished",
    "sessionId": "xxxx",
    "taskId": "xxxx",
    "traceId": "xxxxx"
  },
  "payload": {
    "output": {
      "text": "xxxx"
    },
    "usage": {
      "inputTokens": 100,
      "outputTokens": 100,
      "totalTokens": 200
    }
  },
  "requestId": "5D0E915E-655D-59A8-894F-93873F73AAE5"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
