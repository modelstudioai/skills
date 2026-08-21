# CreatePredefinedDocument - 创建预定义文档

根据业务场景灵活构建文档块。

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
    
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/CreatePredefinedDocument)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/CreatePredefinedDocument)

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

dianjin:CreatePredefinedDocument

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/library/document/createPredefinedDocument HTTP/1.1
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

请求体。

chunks

array<object>

否

文档块列表

Chunk

object

否

chunkMeta

object

否

文档块元信息

{"a": "1"}

chunkOrder

integer

否

顺序，可以不填

1

chunkText

string

否

文档块文本

这是一段测试文本

chunkType

string

否

文档块类型

text

libraryId

string

否

文档库 id

a1b2c3

metadata

object

否

元数据

{"a": "1"}

title

string

否

文档标题

测试文档

## 返回参数

名称

类型

描述

示例值

object

ResultCode

cost

long

耗时

null

data

string

返回数据

1782981430906818562

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

0a06dfe617018288881568684e2937

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
  "data": 1782981430906818600,
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "0a06dfe617018288881568684e2937",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
