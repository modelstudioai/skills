# ListAsyncTasks - 获取异步任务列表

获取异步任务列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListAsyncTasks)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListAsyncTasks)

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

aimiaobi:ListAsyncTasks

list

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

cd327c3d5d5e44159cc716e23bfa530e\_p\_beebot\_public

TaskName

string

否

任务名称精确查询

任务名称

TaskCode

string

否

任务 Code 精确查询

MaterialDocumentUpload

TaskType

string

否

任务类型精确查询

暂无

TaskStatus

integer

否

任务状态精确查询 (0: 待执行, 1: 执行中, 2: 成功, 3: 暂停, 4: 失败可重试, 5: 失败不可重试, 6: 取消)

1

TaskStatusList

array

否

任务状态列表精确查询 (0: 待执行, 1: 执行中, 2: 成功, 3: 暂停, 4: 失败可重试, 5: 失败不可重试, 6: 取消)

TaskStatusList

integer

否

任务状态

1

TaskTypeList

array

否

任务类型列表精确查询

TaskTypeList

string

否

任务分类

test

CreateTimeStart

string

否

任务创建时间 开始查询,格式为：YYYY-MM-DD HH:mm:ss

2023-02-19 07:28:11

CreateTimeEnd

string

否

任务创建时间 结束查询,格式为：YYYY-MM-DD HH:mm:ss

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

## 返回参数

名称

类型

描述

示例值

object

PageResult

Code

string

状态码

successful

Current

integer

当前页。

1

Data

array<object>

返回的数据内容。

Data

object

任务列表。

CreateTime

string

创建日期

2020-12-23 15:41:58

CreateUser

string

创建者

1111

Id

long

任务主键 ID

1

TaskCode

string

任务标识，标识为哪一个任务

MaterialDocumentUpload

TaskDefinition

string

可选的任务定义配置，JSON 格式,这里的参数会覆盖系统配置的定义

{}

TaskEndTime

string

任务实际结束时间

2023-03-09 00:00:00

TaskErrorMessage

string

任务执行错误消息-供客户端查看

系统内部错误

TaskExecuteTime

string

任务执行时间，只会轮询任务到期可执行的任务、为空表示立即执行

2023-10-14 14:30:00

TaskId

string

唯一任务 ID，作用等价于 id

3f7045e099474ba28ceca1b4eb6d6e21

TaskInnerErrorMessage

string

任务内部的执行错误消息,一些异常栈、内部线程栈等敏感信息打印在这里

系统错误

TaskIntermediateResult

string

任务中间执行结果，当一个任务可分成多步骤时，每个步骤的输出，可保存在这里。后续从暂停中恢复可以读取中间结果，从中间结果继续

{}

TaskName

string

任务名

任务名

TaskParam

string

任务执行输入参数，JSON 格式

{}

TaskProgressMessage

string

任务执行进度信息

{}

TaskResult

string

任务执行结果信息

{}

TaskRetryCount

string

任务已经重试的次数

1

TaskStartTime

string

任务实际开始时间

2023-03-20 10:53:00

TaskStatus

integer

任务执行状态，0-待执行、1-执行中、2-执行成功、3-暂停、4-执行失败-可重试、5-执行失败-不可重试,6-任务取消

1

TaskType

string

任务分类,多个任务分类一逗号分隔

test

UpdateTime

string

更新日期

2023-02-16 10:29:16

UpdateUser

string

更新者

111

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

428DCC0D-3C63-5306-BD1B-124396AB97BE

Size

integer

每页记录数

10

Success

boolean

是否成功：true 成功，false 失败

true

Total

integer

总记录数

20

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Current": 1,
  "Data": [
    {
      "CreateTime": "2020-12-23 15:41:58",
      "CreateUser": 1111,
      "Id": 1,
      "TaskCode": "MaterialDocumentUpload",
      "TaskDefinition": {},
      "TaskEndTime": "2023-03-09 00:00:00",
      "TaskErrorMessage": "系统内部错误",
      "TaskExecuteTime": "2023-10-14 14:30:00",
      "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
      "TaskInnerErrorMessage": "系统错误",
      "TaskIntermediateResult": {},
      "TaskName": "任务名",
      "TaskParam": {},
      "TaskProgressMessage": {},
      "TaskResult": {},
      "TaskRetryCount": 1,
      "TaskStartTime": "2023-03-20 10:53:00",
      "TaskStatus": 1,
      "TaskType": "test",
      "UpdateTime": "2023-02-16 10:29:16",
      "UpdateUser": 111
    }
  ],
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "428DCC0D-3C63-5306-BD1B-124396AB97BE",
  "Size": 10,
  "Success": true,
  "Total": 20
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
