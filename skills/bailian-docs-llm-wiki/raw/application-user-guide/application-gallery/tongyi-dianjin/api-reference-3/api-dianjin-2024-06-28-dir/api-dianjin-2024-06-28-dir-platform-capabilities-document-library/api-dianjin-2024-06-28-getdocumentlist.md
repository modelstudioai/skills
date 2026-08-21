# GetDocumentList - 获取文档列表

获取文档库内文档列表，可分页查询，也根据文档状态进行过滤查询。

## 接口说明

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
    
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GetDocumentList)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetDocumentList)

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

dianjin:GetDocumentList

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/api/library/listDocument HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

路径参数，业务空间 id。

llm-xxxx

page

integer

否

页码

1

pageSize

integer

否

页数

10

status

string

否

文档状态

即将可用

libraryId

string

是

文档库 id

3akzl28vap

## 返回参数

名称

类型

描述

示例值

object

返回结果

cost

long

耗时

null

data

object

响应数据

currentPage

long

当前页码（分页参数）。

1

pageSize

long

页面大小（分页参数）。

10

records

array<object>

记录

record

object

docId

string

文档 id

8326748346

documentMeta

object

文档元数据

fileType

string

文档类型

pdf

gmtCreate

string

创建时间

2024-01-01 00:00:00

gmtModified

string

修改时间

2024-01-01 00:00:00

libraryId

string

文档所属库 id

skjdhshbv

statusCode

string

文档状态 (WaitRefresh: 等待刷新, InQueue: 待处理, FetchingData: 数据获取中, Embedding: 文档处理中, Error: 错误, Completed: 可用, Null: 未知)

WaitRefresh

title

string

文档标题

test

url

string

文档链接（该字段即将废弃），该值为空，如需要获取文档链接，可使用 GetDocumentUrl 获取该值。

null

totalPages

long

总页数（分页参数）。

10

totalRecords

long

总记录数量。

100

dataType

string

数据类型

null

errCode

string

错误码

0

message

string

错误信息

ok

requestId

string

请求 id

5E3FBAF1-17AF-53B7-AF0A-CDCEEB6DE658

success

boolean

是否成功

true

time

string

时间戳

2024-04-24 11:54:34

## 示例

正常返回示例

`JSON`格式

```
{
  "cost": 0,
  "data": {
    "currentPage": 1,
    "pageSize": 10,
    "records": [
      {
        "docId": 8326748346,
        "documentMeta": {
          "test": "test",
          "test2": 1
        },
        "fileType": "pdf",
        "gmtCreate": "2024-01-01 00:00:00",
        "gmtModified": "2024-01-01 00:00:00",
        "libraryId": "skjdhshbv",
        "statusCode": "WaitRefresh",
        "title": "test",
        "url": null
      }
    ],
    "totalPages": 10,
    "totalRecords": 100
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "5E3FBAF1-17AF-53B7-AF0A-CDCEEB6DE658",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
