# GetDocumentChunkList - 获取文档块列表

获取文档块列表，可根据查询条件过滤。

## 接口说明

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
    
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GetDocumentChunkList)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetDocumentChunkList)

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

dianjin:GetDocumentChunkList

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/library/getDocumentChunk HTTP/1.1
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

路径参数，业务空间 id

llm-xxxxx

body

object

否

请求体参数。

chunkIdList

array

否

文档块 id 列表

chunkIdList

string

否

文档块 id

83648326438746

docId

string

是

文档 id

182364872346

libraryId

string

是

文档库 id

dsjgfdjgfxxx

order

string

否

排序方式

desc

orderBy

string

否

排序字段

gmtCreate

page

integer

否

页码

1

pageSize

integer

否

每页大小

10

searchQuery

string

否

搜索查询关键词

test

## 返回参数

名称

类型

描述

示例值

object

ResultCode<PageVO\>

cost

long

耗时

null

data

object

响应数据

currentPage

long

当前页

1

pageSize

long

每页记录数

10

records

array<object>

记录

record

object

chunkId

string

文档块 id

28377468263482764

chunkMeta

object

文档块元数据

{"a":"1"}

chunkOssUrl

string

文档块 oss 地址

oss-xxxx-hangzhou.com/test.pdf

chunkText

string

文档块文本

这是一段测试文本

chunkType

string

文档块类型

枚举值：

-   faq：faq。
-   text：text。
-   graph：graph。
-   table：table。
-   structure：structure。

text

docId

string

文档 id

8947387648356

fileType

string

文档类型

pdf

libraryId

string

文档库 id

jhsdvne

libraryName

string

文档库名称

测试文档库

nextChunkId

string

后一个文档块 id

947538465

pos

array<object>

文档块位置

po

object

版面的位置信息

axisArray

array

坐标

axisArray

double

坐标

394.3

page

integer

页码

1

textHighlightArea

array

文本高亮区域，用于文本类型的文件高亮

textHighlightArea

integer

文本高亮区域

38

preChunkId

string

前一个文档块 id

9848346548365

score

float

文档块分数

0.5

title

string

文档标题

test

totalPages

long

总页数

10

totalRecords

long

总记录数

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

2B8F6DC9-6FAF-576F-9095-CCD90FB2BDDF

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
        "chunkId": 28377468263482764,
        "chunkMeta": {
          "a": 1
        },
        "chunkOssUrl": "oss-xxxx-hangzhou.com/test.pdf",
        "chunkText": "这是一段测试文本",
        "chunkType": "text",
        "docId": 8947387648356,
        "fileType": "pdf",
        "libraryId": "jhsdvne",
        "libraryName": "测试文档库",
        "nextChunkId": 947538465,
        "pos": [
          {
            "axisArray": [
              394.3
            ],
            "page": 1,
            "textHighlightArea": [
              38
            ]
          }
        ],
        "preChunkId": 9848346548365,
        "score": 0.5,
        "title": "test"
      }
    ],
    "totalPages": 10,
    "totalRecords": 100
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "2B8F6DC9-6FAF-576F-9095-CCD90FB2BDDF",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
