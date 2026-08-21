# ListInterveneImportTasks - 列出干预项导入任务

获得导入任务列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListInterveneImportTasks)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListInterveneImportTasks)

## 授权信息

当前API暂无授权信息透出。

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

xxxxx\_p\_efm

PageIndex

integer

否

页号

1

PageSize

integer

否

每页尺寸

20

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

success

Data

object

业务数据

PageIndex

integer

页号

1

PageSize

integer

页尺寸

10

StatusList

array<object>

任务状态信息

StatusList

object

Msg

string

任务信息

Success

Percentage

integer

完成百分比

5

Status

integer

任务状态

Success

TaskId

string

任务 Id

4854

TaskName

string

任务名字

12344454

TotalSize

integer

总页数

0

Code

integer

干预服务返回的状态码

200

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

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
  "Code": "success",
  "Data": {
    "PageIndex": 1,
    "PageSize": 10,
    "StatusList": [
      {
        "Msg": "Success",
        "Percentage": 5,
        "Status": 0,
        "TaskId": 4854,
        "TaskName": 12344454
      }
    ],
    "TotalSize": 0,
    "Code": 200
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
