# SubmitDocTranslateTask - 文档翻译任务提交

通义多模态翻译提交文档翻译任务。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AnyTrans/2025-07-07/SubmitDocTranslateTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AnyTrans/2025-07-07/SubmitDocTranslateTask)

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

anytrans:SubmitDocTranslateTask

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /anytrans/translate/doc/submit HTTP/1.1
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

llm-kqtrcpdee4xm29xc

format

string

否

翻译形式

text

sourceLanguage

string

是

源语言

zh

targetLanguage

string

否

目标语言

en

text

string

是

待翻译文件 URL

https://xxx-hangzhou.aliyuncs.com/docs/tmp/%E6%A0%B7%E4%BE%8B\_%E6%97%A0%E5%9B%BE.pdf

scene

string

是

翻译模型

枚举值：

-   mt-plus：mt-plus。
-   mt-turbo：mt-turbo。

mt-turbo

ext

object

否

控制翻译功能的扩展参数

domainHint

string

否

领域风格提示，让译文符合某个领域的表达特征

This text comes from a rigorous academic paper. Please provide a translation that complies with academic standards.

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

config

object

否

翻译行为配置

skipImgTrans

boolean

否

是否翻译 PDF 文档中的图片

false

isBilingual

boolean

否

文档翻译结果是否双语展示

false

paramMap

any

否

扩展参数配置（bizUserld：业务层面的用户 ID，用来区分不 同业务用户，做到“按用户隔离”的术语干预，互不影响。 bizType：业务场景类型/标识，用来区分不同场景，做到 “按场景隔离”的术语干预，互不影响。）

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

响应状态码

success

message

string

响应信息

success

requestId

string

请求 id，用于追溯 API 调用链路

377A48D7-7CFA-53F9-8CA2-14FE3F2774B6

success

boolean

调用是否成功

true

httpStatusCode

string

http 状态码

200

data

object

返回数据

taskId

string

文档翻译任务 id

d3a2397bc2c14ab4a2e40a4f5b46241b

status

string

任务状态

ready

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
  "requestId": "377A48D7-7CFA-53F9-8CA2-14FE3F2774B6",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "taskId": "d3a2397bc2c14ab4a2e40a4f5b46241b",
    "status": "ready",
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

描述

400

IdempotentParameterMismatch

The request uses the same client token as a previous, but non-identical request. Do not reuse a client token with different requests, unless the requests are identical.

\-

429

Request.RateLimit.UserControl

Request Rate Limit User Control.

触发用户限流控制

访问[错误中心](< https://api.aliyun.com/document/AnyTrans/2025-07-07/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-05-19

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/SubmitDocTranslateTask?updateTime=2026-05-19#workbench-doc-change-demo)

2026-03-17

OpenAPI 错误码发生变更、OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/SubmitDocTranslateTask?updateTime=2026-03-17#workbench-doc-change-demo)

2025-12-25

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/SubmitDocTranslateTask?updateTime=2025-12-25#workbench-doc-change-demo)
