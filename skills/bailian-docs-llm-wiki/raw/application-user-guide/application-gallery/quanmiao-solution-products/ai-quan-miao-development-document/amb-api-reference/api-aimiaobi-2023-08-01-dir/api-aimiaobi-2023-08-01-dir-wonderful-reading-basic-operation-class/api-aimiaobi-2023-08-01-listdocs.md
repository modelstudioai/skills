# ListDocs - 获取文档列表

妙读获取文档列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDocs)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDocs)

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

aimiaobi:ListDocs

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

WorkspaceId

string

是

阿里云百炼业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。

llm-2setzb9x4ewsd

DocName

string

否

文档名称

企业2022年報

DocType

string

否

文档类型

pdf

Skip

integer

否

跳过 n 条记录，用于分页

10

MaxResults

integer

否

返回的最大结果数

20

NextToken

string

否

下一页的 token

52a33dc83779f63641e16f5146cd7125

Statuses

array

否

文档状态列表

integer

否

状态值

0

CategoryId

string

否

文档所在目录

default

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Code

string

返回结果编码。

successful

Data

array<object>

返回数据结果列表

Data

object

分页数据

CreateTime

long

创建时间

2024-01-04 11:46:07

DocId

string

文档 ID

12345

DocName

string

文档名称

标题093

DocType

string

文档类型

pdf

Status

integer

状态

0

StatusMessage

string

状态消息

导入完成

CategoryId

string

文档所在目录

default

HttpStatusCode

integer

http 状态码

200

MaxResults

integer

最大返回结果数

10

Message

string

返回消息。

successful

NextToken

string

下一页 Token

CAESGgoSChAKDGNvbXBsZXRlVGltZRABCgQiAggAGAAiQAoJANEQ4mYAAAAACjMDLgAAADFTNzMyZDMwMzAzMDM4NzA3MjZjN2E2NDYyNzUzODMxMzY3ODM0NmIzNTZkNjc=

RequestId

string

请求 Id

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功

true

TotalCount

integer

总记录数

70

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Data": [
    {
      "CreateTime": 0,
      "DocId": 12345,
      "DocName": "标题093",
      "DocType": "pdf",
      "Status": 0,
      "StatusMessage": "导入完成",
      "CategoryId": "default"
    }
  ],
  "HttpStatusCode": 200,
  "MaxResults": 10,
  "Message": "successful",
  "NextToken": "CAESGgoSChAKDGNvbXBsZXRlVGltZRABCgQiAggAGAAiQAoJANEQ4mYAAAAACjMDLgAAADFTNzMyZDMwMzAzMDM4NzA3MjZjN2E2NDYyNzUzODMxMzY3ODM0NmIzNTZkNjc=",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "TotalCount": 70
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
