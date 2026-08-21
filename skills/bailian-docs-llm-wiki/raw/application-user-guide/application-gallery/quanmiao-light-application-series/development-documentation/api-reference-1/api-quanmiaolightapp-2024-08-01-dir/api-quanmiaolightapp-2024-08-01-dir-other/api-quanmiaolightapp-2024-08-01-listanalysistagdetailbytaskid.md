# ListAnalysisTagDetailByTaskId - 获取挖掘结果明细列表

获取挖掘分析结果明细列表

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/ListAnalysisTagDetailByTaskId)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/ListAnalysisTagDetailByTaskId)

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

quanmiaolightapp:ListAnalysisTagDetailByTaskId

list

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/quanmiao/lightapp/listAnalysisTagDetailByTaskId HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

nextToken

string

否

标记当前开始读取的位置，置空表示从头开始

JlroP3CjgQh5PQDlH3ArzADkBTPZgVqo+64jhZRglNq0mEYoV5SlGb/Juvo8CdfYE9rlwEr2pIJQwdaYotak9g==

maxResults

integer

否

本次读取的最大数据记录数量

20

workspaceId

string

是

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

taskId

string

是

挖掘的任务 ID

a3d1c2ac-f086-4a21-9069-f5631542f5a2

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

totalCount

integer

TotalCount 本次请求条件下的数据总量，此参数为可选参数，默认可不返回

200

nextToken

string

表示当前调用返回读取到的位置，空代表数据已经读取完毕

xxxxx

requestId

string

Id of the request

xxxxxxx

maxResults

integer

MaxResults 本次请求所返回的最大记录条数

100

code

string

响应 Code 码

DataNotExists

message

string

响应消息

成功

success

boolean

此次请求是否成功

false

data

array<object>

标签挖掘明细列表

data

object

标签挖掘明细

content

string

标签素材内容

xxxx

contentTags

array<object>

标签挖掘内容列表

contentTags

object

tagName

string

标签名称

标签名称

tags

array

标签值列表

tags

string

标签值

标签值

originResponse

string

原始挖掘响应

原始响应

sourceList

array

溯源原文列表，启用 sourceTrace 时会返回该字段

sourceList

string

溯源原文，启用 sourceTrace 时会返回该字段

## 示例

正常返回示例

`JSON`格式

```
{
  "totalCount": 200,
  "nextToken": "xxxxx",
  "requestId": "xxxxxxx",
  "maxResults": 100,
  "code": "DataNotExists",
  "message": "成功",
  "success": false,
  "data": [
    {
      "content": "xxxx",
      "contentTags": [
        {
          "tagName": "标签名称",
          "tags": [
            "标签值"
          ]
        }
      ],
      "originResponse": "原始响应",
      "sourceList": [
        ""
      ]
    }
  ]
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
