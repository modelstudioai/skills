# GetProperties - 获取配置信息

获取配置信息。包括不限于智能配置的风格，推理相关元数据配置等。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetProperties)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetProperties)

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

aimiaobi:GetProperties

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

xxx\_efm

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

DataNotExists

Data

object

业务数据

ChatConfig

object

通话配置

ConsoleConfig

object

控制台配置

TipContent

string

提示内容

xx

Title

string

标题

AI妙笔

GeneralConfigMap

object

通用配置表

IntelligentSearchConfig

object

智搜配置

ProductDescription

string

首页产品描述

xxx

SearchSamples

array<object>

智搜推荐

SearchSample

object

sample

Articles

array<object>

文章列表

Article

object

文章

Select

boolean

前端传递时是否手动选择

true

Stared

boolean

是否为星标文章

false

Title

string

标题

xx

Url

string

文章 URL

http://xxx.com

Prompt

string

提示词

xx

Text

string

生成内容

xxx

SearchSources

array<object>

搜索源列表

SearchSource

object

搜索源

Code

string

数据集唯一标识: code+datasetName

xx

DatasetName

string

数据集唯一标识: code+datasetName

xx

Name

string

搜索源名称：中文

xx

CopilotPreciseSearchSources

array<object>

妙搜：搜索源配置

CopilotPreciseSearchSource

object

Code

string

数据集唯一标识: code+datasetName

x

DatasetName

string

数据集唯一标识: code+datasetName

x

Name

string

搜索源名称：中文

x

SearchSources

array<object>

搜索源下拉列表

SearchSource

object

搜索源

Label

string

搜索源名称

夸克通用搜索

Value

string

搜索源 code

SystemSearch

SlrAuthorized

boolean

SLR 是否已经授权

true

UserInfo

object

用户配置

AgentId

string

业务空间唯一标识

1

TenantId

string

租户唯一标识

1

UserId

string

用户 id

1

Username

string

用户名称

admin

WanxiangImageSizeConfig

array<object>

万相图片

WanxiangImageSizeConfig

object

万相图片尺寸

Name

string

图片尺寸比例

1:1

Value

string

图片尺寸像素

1024\*1024

WanxiangImageStyleConfig

array<object>

万相图片风格配置

WanxiangImageStyleConfig

object

Name

string

风格名称

默认

Pic

string

风格图片地址

https://img.alicdn.com/imgextra/i4/O1CN01RzKicz1W0YWzYkWcK\_!!6000000002726-2-tps-132-104.png

Value

string

风格 code

<auto>

SearchSourceList

array<object>

指定的搜索源列表

SearchSourceList

object

Code

string

搜索源类型：对应(SystemSearch：系统内置搜索，CustomSemanticSearch：自建语义索引搜索，ThirdSearch：三方 API 搜索)

SystemSearch

Name

string

搜索源描述

互联网检索

DatasetName

string

数据源唯一标识

QuarkCommonNews

MiaosouConfig

object

妙搜配置

UseDocSize

long

数据集已使用文档数

1

MaxDocSize

long

数据集可用文档数

1

ModelInfos

array<object>

智能搜索支持的模型列表

ModelInfos

object

智能搜索支持的模型

ModelName

string

模型名称

全妙-Max

ModelId

string

模型 id

quanmiao-max

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

数据不存在

RequestId

string

请求唯一标识

3f7045e099474ba28ceca1b4eb6d6e21

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "DataNotExists",
  "Data": {
    "ChatConfig": {
      "test": "test",
      "test2": 1
    },
    "ConsoleConfig": {
      "TipContent": "xx",
      "Title": "AI妙笔"
    },
    "GeneralConfigMap": {
      "test": "test",
      "test2": 1
    },
    "IntelligentSearchConfig": {
      "ProductDescription": "xxx",
      "SearchSamples": [
        {
          "Articles": [
            {
              "Select": true,
              "Stared": false,
              "Title": "xx",
              "Url": "http://xxx.com"
            }
          ],
          "Prompt": "xx",
          "Text": "xxx"
        }
      ],
      "SearchSources": [
        {
          "Code": "xx",
          "DatasetName": "xx",
          "Name": "xx"
        }
      ],
      "CopilotPreciseSearchSources": [
        {
          "Code": "x",
          "DatasetName": "x",
          "Name": "x"
        }
      ]
    },
    "SearchSources": [
      {
        "Label": "夸克通用搜索",
        "Value": "SystemSearch"
      }
    ],
    "SlrAuthorized": true,
    "UserInfo": {
      "AgentId": 1,
      "TenantId": 1,
      "UserId": 1,
      "Username": "admin"
    },
    "WanxiangImageSizeConfig": [
      {
        "Name": "1:1",
        "Value": "1024*1024"
      }
    ],
    "WanxiangImageStyleConfig": [
      {
        "Name": "默认",
        "Pic": "https://img.alicdn.com/imgextra/i4/O1CN01RzKicz1W0YWzYkWcK_!!6000000002726-2-tps-132-104.png",
        "Value": "<auto>"
      }
    ],
    "SearchSourceList": [
      {
        "Code": "SystemSearch",
        "Name": "互联网检索",
        "DatasetName": "QuarkCommonNews"
      }
    ],
    "MiaosouConfig": {
      "UseDocSize": 1,
      "MaxDocSize": 1,
      "ModelInfos": [
        {
          "ModelName": "全妙-Max",
          "ModelId": "quanmiao-max"
        }
      ]
    }
  },
  "HttpStatusCode": 200,
  "Message": "数据不存在",
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
