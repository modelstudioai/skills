# UploadDoc - 文档上传

妙读上传文档接口。

## 接口说明

文档上传是通过异步调用的方式实现，调用之后需要使用 getDocInfo 接口进行循环检查文档状态，当文档状态为 1 时，才能进行后续的文档摘要、生成全文脑图、问答内容总结、抽取关键词、改写等操作。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/UploadDoc)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/UploadDoc)

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

aimiaobi:UploadDoc

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

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-yigtrrjl377rcbab

Docs

array<object>

是

文档

object

是

文档

DocName

string

是

文档名称

文档1.pdf

FileUrl

string

是

文件 url

http://xxx/ccc.pdf

CategoryId

string

否

文档所在目录，如果不填值是 default

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

内部错误码

successful

Data

object

文档信息

DocIds

array

成功的文档 Id 数组

docIds

string

文档 ID

aaaxxx

ExistedIds

array

因为已经存在无法上传的文档 Id

existedIds

string

文档 Id

ccccc

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

Id of the request

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Data": {
    "DocIds": [
      "aaaxxx"
    ],
    "ExistedIds": [
      "ccccc"
    ]
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
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
