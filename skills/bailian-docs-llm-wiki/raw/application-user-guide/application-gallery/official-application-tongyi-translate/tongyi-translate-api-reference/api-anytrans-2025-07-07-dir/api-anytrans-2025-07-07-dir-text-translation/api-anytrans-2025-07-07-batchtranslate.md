# BatchTranslate - 批量文本翻译

通义多模态翻译批量翻译

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AnyTrans/2025-07-07/BatchTranslate)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AnyTrans/2025-07-07/BatchTranslate)

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

anytrans:BatchTranslate

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /anytrans/translate/batch HTTP/1.1
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

当前请求所使用的百炼业务空间 id

llm-kqtrcpdee4xm29xx

sourceLanguage

string

是

源语言

zh

targetLanguage

string

是

目标语言

en

text

object

是

待翻译的批量文本

{"0":"明天天气怎么样？","1":"你中午吃饭了吗"}

scene

string

否

翻译模型

枚举值：

-   mt-plus：专业版。
-   mt-turbo：轻量版。

mt-turbo

format

string

否

翻译形式

text

appName

string

否

调用来源

baidufanyi

ext

object

否

控制翻译功能的扩展参数

examples

array<object>

否

翻译示例列表

object

否

翻译示例

tgt

string

否

目标文本

hello

src

string

否

源文本

你好

domainHint

string

否

领域提示（一段英文自然语言文本，用于指示大模型翻译的风格）

this sentence from an e-commerce product image, please provide a translation that is both highly concise and no more than 1.2 times the length of the original.

sensitives

array

否

敏感词库

string

否

待过滤的敏感词

password

terminologies

array<object>

否

翻译术语库

object

否

待干预术语对

tgt

string

否

干预后译文

API

src

string

否

源文本

应用接口

textTransform

object

否

译文文本转换

toLower

boolean

否

译文全转为小写

枚举值：

-   true：是。
-   false：否。

false

toUpper

boolean

否

译文全转为大写

枚举值：

-   true：是。
-   false：否。

false

toTitle

boolean

否

译文全转为 capitalized 首字母大写

枚举值：

-   true：是。
-   false：否。

false

config

object

否

翻译行为控制

skipCsiCheck

boolean

否

是否跳过绿网检测（如果需要跳过绿网检测，需要先完成绿网关闭流程后再调用）

false

paramMap

any

否

扩展参数配置（bizUserld：业务层面的用户 ID，用来区分不 同业务用户，做到“按用户隔离”的术语干预，互不影响。 bizType：业务场景类型/标识，用来区分不同场景，做到 “按场景隔离”的术语干预，互不影响。）

枚举值：

-   bizType：业务场景类型。
-   bizUserId：业务用户id。

{"bizUserld":"123456","bizType":session"}

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

code

string

响应状态码

200

message

string

响应信息

success

requestId

string

请求 id，用于追溯 API 调用链路

3BE338D3-16B1-513F-8DD2-57C8528DEAAA

success

boolean

接口调用是否成功

true

httpStatusCode

string

http 状态码

200

data

object

返回数据

translationList

array<object>

批量翻译结果

translationList

object

单条翻译结果

code

long

响应状态码

200

message

string

响应信息

OK

index

string

单条翻译结果的索引

0

translation

string

该索引对应的翻译结果

What will the weather be like tomorrow?

usage

object

token 用量

inputTokens

long

输入 token 数

53

outputTokens

long

输出 token 数

8

totalTokens

long

总 token 数

61

## 示例

正常返回示例

`JSON`格式

```
{
  "code": 200,
  "message": "success",
  "requestId": "3BE338D3-16B1-513F-8DD2-57C8528DEAAA",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "translationList": [
      {
        "code": 200,
        "message": "OK",
        "index": 0,
        "translation": "What will the weather be like tomorrow?",
        "detectedLang": "",
        "usage": {
          "inputTokens": 53,
          "outputTokens": 8,
          "totalTokens": 61
        }
      }
    ]
  }
}
```

## 错误码

HTTP status code

错误码

错误信息

400

IdempotentParameterMismatch

The request uses the same client token as a previous, but non-identical request. Do not reuse a client token with different requests, unless the requests are identical.

访问[错误中心](< https://api.aliyun.com/document/AnyTrans/2025-07-07/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-04-15

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/BatchTranslate?updateTime=2026-04-15#workbench-doc-change-demo)

2026-03-26

OpenAPI 错误码发生变更、OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/BatchTranslate?updateTime=2026-03-26#workbench-doc-change-demo)

2025-12-25

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/BatchTranslate?updateTime=2025-12-25#workbench-doc-change-demo)
