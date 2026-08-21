# QueryAsyncTask - 查询异步任务明细

查询已提交异步任务执行明细。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/QueryAsyncTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/QueryAsyncTask)

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

aimiaobi:QueryAsyncTask

get

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

33a2658aaabf4c24b45d50e575125311\_p\_beebot\_public

TaskId

string

否

任务唯一 ID

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

3f7045e099474ba28ceca1b4eb6d6e21

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

CreateTime

string

创建日期

2021-07-25 14:34:33

CreateUser

string

创建者

"12121"

TaskCode

string

任务标识，标识为哪一个任务

MaterialDocumentUpload

TaskErrorMessage

string

任务执行错误消息

error

TaskId

string

唯一任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

TaskIntermediateResult

string

任务中间执行结果，当一个任务可分成多步骤时，每个步骤的输出，可保存在这里。后续从暂停中恢复可以读取中间结果，从中间结果继续

"{}"

TaskName

string

任务名

任务名称

TaskParam

string

任务执行输入参数，JSON 格式

"{\\"fileKey\\":\\"oss://default/xxxx/xxxx/xxx\\",\\"fileName\\":\\"xxxxx.doc\\"}"

TaskProgressMessage

string

任务执行进度信息

"{}"

TaskResult

string

任务执行结果信息

"{}"

TaskRetryCount

string

任务已经重试的次数

"3"

TaskStatus

integer

任务执行状态，0-待执行、1-执行中、2-执行成功、3-暂停、4-执行失败-可重试、5-执行失败-不可重试,6-任务取消

1

UpdateTime

string

更新日期

2023-04-27 18:07:43

UpdateUser

string

更新者

"12121"

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

867C4ABE-4381-5BC2-9810-5A5F334F71CF

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
    "CreateTime": "2021-07-25 14:34:33",
    "CreateUser": 12121,
    "TaskCode": "MaterialDocumentUpload",
    "TaskErrorMessage": "error",
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TaskIntermediateResult": {},
    "TaskName": "任务名称",
    "TaskParam": {
      "fileKey": "oss://default/xxxx/xxxx/xxx",
      "fileName": "xxxxx.doc"
    },
    "TaskProgressMessage": {},
    "TaskResult": {},
    "TaskRetryCount": 3,
    "TaskStatus": 1,
    "UpdateTime": "2023-04-27 18:07:43",
    "UpdateUser": 12121
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "867C4ABE-4381-5BC2-9810-5A5F334F71CF",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
