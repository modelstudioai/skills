# ListAutoClipsTask - 智能混剪任务列表

列出智能混剪任务列表

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListAutoClipsTask)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListAutoClipsTask)

## **授权信息**

当前API暂无授权信息透出。

## 请求语法

```
POST  HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

否

百炼业务空间

llm-2setzb9x4ewsd

TaskName

string

否

任务名称

task001

TaskType

string

否

任务类型

type001

TaskStatus

integer

否

任务状态

0

CreateTimeStart

string

否

任务开始时间

2023-02-19 07:28:11

CreateTimeEnd

string

否

任务结束时间

2023-03-18 02:00:00

Current

integer

否

当前页码

1

Size

integer

否

每页条数：默认 10

10

Skip

integer

否

废弃

null

MaxResults

integer

否

废弃

null

NextToken

string

否

废弃

null

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

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Code

string

状态码

success

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

successful

Success

boolean

是否成功：true 成功，false 失败

true

MaxResults

integer

废弃

null

NextToken

string

废弃

null

TotalCount

integer

废弃

null

Current

integer

当前页码

1

Size

integer

每页条数

10

Total

integer

总记录数

20

Data

array<object>

业务数据

object

业务数据

TaskId

string

任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

TaskName

string

任务名称

任务名称

TaskType

string

任务类型

type001

TaskStatus

integer

任务状态

0

TaskStep

string

upload

upload clips generate

CreateTimeStart

string

起始创建时间。

2023-03-18 02:00:00

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Code": "success",
  "HttpStatusCode": 200,
  "Message": "successful",
  "Success": true,
  "MaxResults": 0,
  "NextToken": "null",
  "TotalCount": 0,
  "Current": 1,
  "Size": 10,
  "Total": 20,
  "Data": [
    {
      "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
      "TaskName": "任务名称",
      "TaskType": "type001",
      "TaskStatus": 0,
      "TaskStep": "upload\nclips\ngenerate",
      "CreateTimeStart": "2023-03-18 02:00:00\n"
    }
  ]
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListAutoClipsTask#workbench-doc-change-demo)。
