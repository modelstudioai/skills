# TermEdit - 术语库编辑

通义多模态翻译术语库编辑

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AnyTrans/2025-07-07/TermEdit)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AnyTrans/2025-07-07/TermEdit)

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

anytrans:TermEdit

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /anytrans/translate/intervene/edit HTTP/1.1
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

action

string

是

操作类型

枚举值：

-   ADD：新增。
-   DELETE：删除。
-   MODIFY：修改。

ADD

sourceLanguage

string

是

源语言

en

targetLanguage

string

是

目标语言

zh

scene

string

是

模型类型

枚举值：

-   mt-plus：专业版。
-   mt-turbo：轻量版。

mt-turbo

ext

object

是

扩展参数

terms

array<object>

是

干预术语列表

object

是

干预术语

termId

string

否

干预术语 id

92669964

src

string

是

源文本

大模型

tgt

string

是

干预后译文

LLM

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

success

message

string

响应信息

success

requestId

string

请求 id

1DCD50EC-D218-1844-9CD8-E97CAB9D31BE

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

terms

array<object>

干预术语列表

terms

object

干预术语

termId

string

术语 id

92669964

src

string

源文本

大模型

tgt

string

目标文本

LLM

failCount

long

失败数量

0

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "success",
  "message": "success",
  "requestId": "1DCD50EC-D218-1844-9CD8-E97CAB9D31BE",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "terms": [
      {
        "termId": 92669964,
        "src": "大模型",
        "tgt": "LLM"
      }
    ],
    "failCount": 0
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

2025-12-25

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/TermEdit?updateTime=2025-12-25#workbench-doc-change-demo)
