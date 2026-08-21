# GetAppConfig - 获取配置信息

获取app配置。

## 接口说明

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
    
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GetAppConfig)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetAppConfig)

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

dianjin:GetAppConfig

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/api/app/config HTTP/1.1
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

object

返回数据

embeddingTypeList

array<object>

embedding 类型列表

embeddingTypeList

object

k-v 对

string

value

DashScope

frontendConfig

object

前端配置

boolean

是否开启

true

libraryDocumentStatusList

array<object>

文档库文档状态列表

libraryDocumentStatusList

object

k-v 对

string

value

Completed

llmHelperTypeList

array<object>

大模型类型列表

llmHelperTypeList

object

k-v 对

string

value

qwen-max

textIndexCategoryList

array

文本索引类别列表

textIndexCategoryList

string

文本索引类别

ElasticSearch

vectorIndexCategoryList

array

向量索引类别列表

vectorIndexCategoryList

string

向量索引类别

ADB

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

None

requestId

string

请求 id

EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258

success

boolean

是否成功

True

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
    "embeddingTypeList": [
      {
        "key": "DashScope"
      }
    ],
    "frontendConfig": {
      "key": true
    },
    "libraryDocumentStatusList": [
      {
        "key": "Completed"
      }
    ],
    "llmHelperTypeList": [
      {
        "key": "qwen-max"
      }
    ],
    "textIndexCategoryList": [
      "ElasticSearch"
    ],
    "vectorIndexCategoryList": [
      "ADB"
    ]
  },
  "dataType": null,
  "errCode": 0,
  "message": "None",
  "requestId": "EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
