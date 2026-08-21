# RunScriptChat - 影视互娱剧本创作-交互式创作

长剧本创作。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunScriptChat)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunScriptChat)

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

quanmiaolightapp:RunScriptChat

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runScriptChat HTTP/1.1
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

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-rz8db8d00rcn2p0xc

prompt

string

是

用户输入的剧本指令

创建角色：林晓晓

taskId

string

否

任务唯一标识

**说明**-   taskId 默认无需填写，系统将自动生成。当后续任务填写的 taskId 相同时，表示这些任务属于同一组对话。
-   建议手动赋值 taskId，以便关联上下文。

a3d1c2ac-f086-4a21-9069-f5631542f5a2

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

end

boolean

输出是否完成，true 表示完成

true

header

object

流式输出 header 头，包含返回通用信息

errorCode

string

异常错误码

403

errorMessage

string

异常错误信息

Pop sign mismatch, please check log.

event

string

事件类型

result-generated

eventInfo

string

事件描述

模型生成事件描述

requestId

string

请求 ID

F8A35034-EDCF-5C50-95A5-1044316F36E3

sessionId

string

一次会话 ID

147648697127\_914847410985\_1730600302167

taskId

string

一次生成任务 ID

d3be9981-ca2d-4e17-bf31-1c0a628e9f99

traceId

string

链路 traceid

2150432017236011824686132ecdbc

payload

object

返回结果的 payload，json 结构

output

object

输出内容对象

text

string

输出内容

以下是角色信息

usage

object

大模型 Token 用量信息

inputTokens

long

输入 Token 数量

100

outputTokens

long

输出 Token 数量

100

totalTokens

long

总 Token 数量

200

## 示例

正常返回示例

`JSON`格式

```
{
  "end": true,
  "header": {
    "errorCode": 403,
    "errorMessage": "Pop sign mismatch, please check log.",
    "event": "result-generated",
    "eventInfo": "模型生成事件描述",
    "requestId": "F8A35034-EDCF-5C50-95A5-1044316F36E3",
    "sessionId": "147648697127_914847410985_1730600302167",
    "taskId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99",
    "traceId": "2150432017236011824686132ecdbc"
  },
  "payload": {
    "output": {
      "text": "以下是角色信息"
    },
    "usage": {
      "inputTokens": 100,
      "outputTokens": 100,
      "totalTokens": 200
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

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
