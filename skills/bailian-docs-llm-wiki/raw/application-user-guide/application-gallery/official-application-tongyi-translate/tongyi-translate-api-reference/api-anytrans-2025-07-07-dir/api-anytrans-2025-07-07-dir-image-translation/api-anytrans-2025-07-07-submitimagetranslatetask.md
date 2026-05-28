# SubmitImageTranslateTask - 提交图片翻译任务

通义多模态翻译提交图片翻译任务

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AnyTrans/2025-07-07/SubmitImageTranslateTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AnyTrans/2025-07-07/SubmitImageTranslateTask)

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

anytrans:SubmitImageTranslateTask

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /anytrans/translate/image/submit HTTP/1.1
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

format

string

否

翻译形式

image

sourceLanguage

string

是

源语言

zh

targetLanguage

array

是

目标语言列表

string

是

目标语言

en

text

string

是

待翻译的图片 url

https://img.alicdn.com/imgextra/i3/2214557014466/O1CN0174Thmb1irTsyTXYFO\_!!4611686018427386306-0-item\_pic.jpg

scene

string

是

翻译模型

枚举值：

-   general：专业版。
-   flash：轻量版。

flash

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

ML

src

string

否

源文本

机器学习

textTransform

object

否

译文大小写转换

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

paramMap

any

否

扩展参数配置（bizUserld：业务层面的用户 ID，用来区分不 同业务用户，做到“按用户隔离”的术语干预，互不影响。 bizType：业务场景类型/标识，用来区分不同场景，做到 “按场景隔离”的术语干预，互不影响。）

枚举值：

-   bizType：业务场景类型。
-   bizUserId：业务用户id。

{"bizUserld":"123456","bizType":session"}

trackingData

string

否

用户自定义透传数据，翻译服务不做处理，原样返回，用于埋点等场景

{"traceId":"trace\_123456"}

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

code

string

响应错误码

success

message

string

响应消息

success

requestId

string

请求 id，用于追溯 API 调用链路

42FF90E5-5D40-5797-AAF6-8A4D837CCCD5

success

boolean

调用是否成功

true

httpStatusCode

string

HTTP 状态码

200

data

object

返回数据

taskId

string

图片翻译任务 id

2746f4be-cff2-465e-a2c6-12bff30ce0f9

status

string

翻译状态

枚举值：

-   in\_process：翻译中。
-   success：已完成。

success

trackingData

string

用户自定义透传数据，翻译服务不做处理，原样返回，用于埋点等场景

{"traceId":"trace\_123456"}

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "success",
  "message": "success",
  "requestId": "42FF90E5-5D40-5797-AAF6-8A4D837CCCD5",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "taskId": "2746f4be-cff2-465e-a2c6-12bff30ce0f9",
    "status": "success",
    "trackingData": {
      "traceId": "trace_123456"
    }
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

2026-03-17

OpenAPI 错误码发生变更、OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/SubmitImageTranslateTask?updateTime=2026-03-17#workbench-doc-change-demo)

2025-12-25

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/SubmitImageTranslateTask?updateTime=2025-12-25#workbench-doc-change-demo)
