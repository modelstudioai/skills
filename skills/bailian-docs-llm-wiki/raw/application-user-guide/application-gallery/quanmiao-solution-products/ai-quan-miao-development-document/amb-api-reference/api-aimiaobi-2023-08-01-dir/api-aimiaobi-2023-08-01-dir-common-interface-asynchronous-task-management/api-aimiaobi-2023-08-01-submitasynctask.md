# SubmitAsyncTask - 提交异步任务

执行系统预定义的异步任务。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitAsyncTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitAsyncTask)

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

aimiaobi:SubmitAsyncTask

create

\*全部资源

`*`

无

无

## 请求参数

名称

类型

必填

描述

示例值

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

2daaa2e0c209xb26acb97009ea77bd4b\_p\_efm

TaskName

string

否

任务名称定义

任务名称

TaskCode

string

是

任务定义：详见任务定义表

MaterialDocumentUpload

TaskParam

string

否

任务提交参数

{"fileUrl":"https://www.example.com/aaa.doc","fileName":"文件名称","shareAttr":1}

TaskExecuteTime

string

否

任务执行时间，默认立即执行。格式：YYYY-MM-DD HH:mm:ss

2023-10-14 14:30:00

## 返回参数

名称

类型

描述

示例值

object

PlainResult

Code

string

状态码

successful

Data

object

业务数据

TaskId

string

任务唯一 ID

xxxx

TaskIntermediateResult

any

中间结果

{}

TaskName

string

任务名称

任务名称

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

successful

RequestId

string

请求唯一标识

3f7045e099474ba28ceca1b4eb6d6e21

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Data": {
    "TaskId": "xxxx",
    "TaskIntermediateResult": {},
    "TaskName": "任务名称"
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
