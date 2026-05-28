# ListApplications - 查询语音机器人应用列表

查询语音机器人应用列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/ListApplications)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/ListApplications)

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

bailianvoicebot:ListApplications

none

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

BusinessUnitId

string

是

百炼业务空间 ID

llm-c11iig67g863rih8

SearchPattern

string

否

模板名称，模糊搜索。

通用

PageNumber

integer

是

页码

1

PageSize

integer

是

每页显示条数

10

## 返回参数

名称

类型

描述

示例值

object

Code

string

接口状态或 POP 错误码。

OK

HttpStatusCode

integer

http 状态码

200

Message

string

响应信息

successful

RequestId

string

请求 ID

D771A1B6-3D5F-174A-BEE1-98CE1000D337

Data

object

返回结果

PageNumber

integer

当前的页数。

1

PageSize

integer

每页大小。

1000

TotalCount

integer

总数

6

Applications

array<object>

应用列表信息。

Application

object

应用列表信息。

CreatedTime

long

创建时间

1729909690

UpdatedTime

long

修改时间

1729909348

ApplicationId

string

应用 ID。

a395011f-a247-400f-bc69-28796749fd52

Name

string

应用名称

测试001

Description

string

应用描述

描述一下这个应用

Concurrency

integer

并发设置

10

NluEngine

string

Nlu 引擎

PROMPTS

NluAccessType

string

Nlu 调用方式

MANAGED

DraftVersionId

string

草稿版本 ID

20904943-f711-494f-9f1f-e7f340f37707

PublishedVersionId

string

发布版本 ID

20904943-f711-494f-9f1f-e7f340f37707

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "OK",
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "Data": {
    "PageNumber": 1,
    "PageSize": 1000,
    "TotalCount": 6,
    "Applications": [
      {
        "CreatedTime": 1729909690,
        "UpdatedTime": 1729909348,
        "ApplicationId": "a395011f-a247-400f-bc69-28796749fd52\n",
        "Name": "测试001\n",
        "Description": "描述一下这个应用",
        "Concurrency": 10,
        "NluEngine": "PROMPTS",
        "NluAccessType": "MANAGED",
        "DraftVersionId": "20904943-f711-494f-9f1f-e7f340f37707\n",
        "PublishedVersionId": "20904943-f711-494f-9f1f-e7f340f37707\n"
      }
    ]
  }
}
```

## 错误码

HTTP status code

错误码

错误信息

400

Parameter.Enumeration

The parameter %s must be one of the value of enumeration %s.

400

Parameter.Blank

The parameter %s must not be null or empty.

400

Parameter.Empty

The parameter %s may not be null or empty.

400

Parameter.Null

The parameter %s may not be null.

403

Permission.Unauthorized

You are not authorized to perform this action. %s privileges are required.

404

NotExists.InstanceId

The specified instance %s does not exist.

访问[错误中心](< https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-01-28

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/ListApplications?updateTime=2026-01-28#workbench-doc-change-demo)
