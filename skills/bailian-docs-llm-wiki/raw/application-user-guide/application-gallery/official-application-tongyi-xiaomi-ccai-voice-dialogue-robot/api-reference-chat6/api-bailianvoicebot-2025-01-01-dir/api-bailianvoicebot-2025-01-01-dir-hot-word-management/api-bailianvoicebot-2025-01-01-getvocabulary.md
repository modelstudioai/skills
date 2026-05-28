# GetVocabulary - 获取热词信息

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/GetVocabulary)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/GetVocabulary)

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

bailianvoicebot:GetVocabulary

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

BusinessUnitId

string

是

百炼业务空间 ID

llm-zop7ukgtksltamo4

VocabularyId

string

是

热词 ID

d74d6290-7cbe-4436-b5d7-014ebb0f4061

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

OK

HttpStatusCode

integer

http 状态码

200

Message

string

错误信息

Instance llm-zzu528i29ecnprcl does not exist.

RequestId

string

请求 ID

D771A1B6-3D5F-174A-BEE1-98CE1000D337

Data

object

热词对象

VocabularyId

string

热词 ID

af81a389-91f0-4157-8d82-720edd02b66b

Name

string

热词名称

金融场景热词

Description

string

描述

包含金融场景专业术语

CreatedTime

long

创建时间

1773453676000

UpdatedTime

long

更新时间

1773453676000

InstanceId

string

百炼业务空间 ID

llm-zop7ukgtksltamo4

TenantId

string

租户 ID

1308144684576655

WordCount

string

热词数量

50

Words

string

热词

{\\"苹果\\":\\"2\\",\\"香蕉\\":\\"3\\"}

Params

array

动态错误参数列表

param

string

动态错误参数

llm-xdne77rxe14ziszr

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "OK",
  "HttpStatusCode": 200,
  "Message": "Instance llm-zzu528i29ecnprcl does not exist.",
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "Data": {
    "VocabularyId": "af81a389-91f0-4157-8d82-720edd02b66b",
    "Name": "金融场景热词",
    "Description": "包含金融场景专业术语",
    "CreatedTime": 1773453676000,
    "UpdatedTime": 1773453676000,
    "InstanceId": "llm-zop7ukgtksltamo4",
    "TenantId": 1308144684576655,
    "WordCount": 50,
    "Words": "{\\\"苹果\\\":\\\"2\\\",\\\"香蕉\\\":\\\"3\\\"}"
  },
  "Params": [
    "llm-xdne77rxe14ziszr"
  ]
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-04-22

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/GetVocabulary?updateTime=2026-04-22#workbench-doc-change-demo)
