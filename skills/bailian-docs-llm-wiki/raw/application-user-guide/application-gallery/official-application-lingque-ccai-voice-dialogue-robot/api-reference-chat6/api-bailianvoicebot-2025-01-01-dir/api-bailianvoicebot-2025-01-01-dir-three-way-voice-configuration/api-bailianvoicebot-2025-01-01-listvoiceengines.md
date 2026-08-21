# ListVoiceEngines - 获取三方语音引擎列表

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/ListVoiceEngines)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/ListVoiceEngines)

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

bailianvoicebot:ListVoiceEngines

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

PageNumber

integer

是

页号

1

PageSize

integer

是

每页条数

10

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

RequestId

string

Id of the request

D771A1B6-3D5F-174A-BEE1-98CE1000D337

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

Instance llm-rj6aqmctjcit4acy does not exist.

Data

object

语音引擎分页结果

PageNumber

integer

页号

1

PageSize

integer

每页条数

10

TotalCount

integer

总数量

100

VoiceEngines

array<object>

语音引擎对象列表

voiceEngine

object

语音引擎对象

NlsEngine

string

语音引擎

VOLC

NlsEngineName

string

显示名称

豆包

ConfigSchema

string

引擎配置

\[{\\"displayName\\":\\"AppKey\\",\\"maxLength\\":64,\\"name\\":\\"AppKey\\",\\"order\\":1,\\"required\\":true},{\\"displayName\\":\\"AccessKey\\",\\"maxLength\\":64,\\"name\\":\\"AccessKey\\",\\"order\\":2,\\"required\\":true}\]

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
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "Code": "OK",
  "HttpStatusCode": 200,
  "Message": "Instance llm-rj6aqmctjcit4acy does not exist.",
  "Data": {
    "PageNumber": 1,
    "PageSize": 10,
    "TotalCount": 100,
    "VoiceEngines": [
      {
        "NlsEngine": "VOLC",
        "NlsEngineName": "豆包",
        "ConfigSchema": "[{\\\"displayName\\\":\\\"AppKey\\\",\\\"maxLength\\\":64,\\\"name\\\":\\\"AppKey\\\",\\\"order\\\":1,\\\"required\\\":true},{\\\"displayName\\\":\\\"AccessKey\\\",\\\"maxLength\\\":64,\\\"name\\\":\\\"AccessKey\\\",\\\"order\\\":2,\\\"required\\\":true}]"
      }
    ]
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

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/ListVoiceEngines?updateTime=2026-04-22#workbench-doc-change-demo)
