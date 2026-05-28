# GetIndexJobStatus - 查询知识库创建任务状态

查询指定的知识库创建任务或知识库追加任务的当前状态。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（`AliyunBailianDataFullAccess`或`AliyunBailianDataReadOnlyAccess`均可，已包括 sfm:GetIndexJobStatus 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   您需要有一个正在执行中的知识库作业任务（创建知识库任务可以调用 **SubmitIndexJob** 接口，创建知识库追加任务可以调用 **SubmitIndexAddDocumentsJob** 接口），并且获得相应的`JobId`。
-   本接口调用间隔建议在 5 秒以上。
-   本接口具有幂等性。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/GetIndexJobStatus)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/GetIndexJobStatus)

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

sfm:GetIndexJobStatus

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{WorkspaceId}/index/job/status HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

是

业务空间 ID，请确保您要操作的知识库在此业务空间中。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3z7uw7fwz0vexxxx

JobId

string

是

知识库作业任务 ID，即 **SubmitIndexJob** 接口或 **SubmitIndexAddDocumentsJob** 接口返回的`Data.Id`。

20230718xxxx-146c93bf

IndexId

string

是

知识库 ID，即 **CreateIndex** 接口返回的`Data.Id`。

79c0alxxxx

PageNumber

integer

否

**SubmitIndexJob** 接口和 **SubmitIndexAddDocumentsJob** 接口均支持批量导入文件。本接口返回的字段包括知识库作业任务的总状态`Status`及各文件导入的状态`Document.Status`。若文件较多，可通过`PageNumber`参数进行分页查询。起始值为 1，默认值为 1。

1

pageSize

integer

否

指定分页查询时每页展示的文件导入任务数量。最大值不限。默认值为 10。

10

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Code

string

错误状态码。

Index.Forbidden

Data

object

接口业务数据字段。

Documents

array<object>

本次导入的文件列表。

rows

object

文件对象。

Code

string

错误状态码。

Index.Document.ChunkError

DocId

string

文件 ID。

file\_9a65732555b54d5ea10796ca5742ba22\_xxxxxxxx

DocName

string

文件名称。

XXX产品介绍

Message

string

错误信息。

document parse error

Status

string

文件导入状态。可能值：

-   INSERT\_ERROR：文件导入失败。
-   RUNNING：文件导入中。
-   DELETED：文件已删除。
-   FINISH：文件导入成功。

RUNNING

JobId

string

作业任务 ID。

66122af12a4e45ddae6bd6c84555xxxx

Status

string

知识库作业任务的当前状态。可能值：

-   COMPLETED：执行成功。
-   FAILED：执行失败。
-   RUNNING：执行中。
-   PENDING：等待执行。

PENDING

Message

string

错误信息。

User not authorized to operate on the specified resource.

RequestId

string

请求 ID。

17204B98-xxxx-4F9A-8464-2446A84821CA

Status

string

接口返回的状态码。

200

Success

boolean

接口调用是否成功，可能值为：

-   true：成功。
-   false：失败。

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "Index.Forbidden",
  "Data": {
    "Documents": [
      {
        "Code": "Index.Document.ChunkError",
        "DocId": "file_9a65732555b54d5ea10796ca5742ba22_xxxxxxxx",
        "DocName": "XXX产品介绍",
        "Message": "document parse error",
        "Status": "RUNNING",
        "GmtModified": 0
      }
    ],
    "JobId": "66122af12a4e45ddae6bd6c84555xxxx",
    "Status": "PENDING"
  },
  "Message": "User not authorized to operate on the specified resource.",
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA",
  "Status": 200,
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
