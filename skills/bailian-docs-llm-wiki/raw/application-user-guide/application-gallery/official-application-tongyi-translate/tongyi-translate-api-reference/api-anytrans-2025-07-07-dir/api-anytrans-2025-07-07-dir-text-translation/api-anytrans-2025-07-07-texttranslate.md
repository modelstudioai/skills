# TextTranslate - 文本翻译接口

通义多模态翻译文本翻译

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AnyTrans/2025-07-07/TextTranslate)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AnyTrans/2025-07-07/TextTranslate)

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

anytrans:TextTranslate

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /anytrans/translate/text HTTP/1.1
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

业务空间 Id

llm-kqtrcpdee4xm29xx

format

string

否

文本格式

text

sourceLanguage

string

是

源语种代码

zh

targetLanguage

string

是

目标语种代码

en

text

string

是

待翻译的文本

今天天气怎么样

scene

string

否

模型类型

枚举值：

-   mt-plus：专业版。
-   mt-turbo：轻量版。

mt-turbo

ext

object

否

控制翻译行为的扩展参数

examples

array<object>

否

翻译示例列表

object

否

翻译示例

src

string

否

源文案

你好

tgt

string

否

目标文案

hello

domainHint

string

否

领域提示

technology

agent

string

否

专家 agent

枚举值：

-   game：游戏译者。
-   medical：医学翻译大师。
-   ao3：AO3译者。
-   mixlang：中英夹杂。
-   twitter：Twitter翻译增强器。
-   ecom：金融翻译顾问。
-   music：音乐专家。
-   dongbei：东北话。
-   design：设计师。
-   legal：法律行业译者。
-   reddit：Reddit翻译增强器。
-   vocab：词汇助手。
-   wordalign：分词对照翻译助手。
-   academy：学术论文翻译师。
-   news：新闻媒体译者。
-   tech：科技类翻译大师。
-   github：GitHub翻译增强器。
-   chess：国际象棋专家。
-   web3：Web3翻译大师。
-   bai2wen：白话文转文言文。
-   ebook：电子书译者。
-   sublearn：潜意识学习。
-   summarize：段落总结专家。
-   simplify：英文简化大师。
-   wen2bai：文言文转白话文。
-   finance：金融翻译顾问。
-   novel：小说译者。

game

sensitives

array

否

敏感词列表

string

否

敏感词列表

password

terminologies

array<object>

否

翻译术语库

object

否

翻译术语库

src

string

否

源文案

机器学习

tgt

string

否

目标文案

ML

textTransform

object

否

译文文本转换

toLower

boolean

否

转小写

枚举值：

-   true：是。
-   false：否。

false

toUpper

boolean

否

转大写

枚举值：

-   true：是。
-   false：否。

false

toTitle

boolean

否

首字母大写

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

fasle

prefix

string

否

前缀配置

Today's weather

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

错误信息

success

requestId

string

Id of the request

299C57B2-EBB4-57E2-A6FE-723B874ACB74

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

translation

string

翻译结果

How does Mogujie solve the data annotation challenge by building a platform?

usage

object

token 消耗

inputTokens

long

输入 token 数

491

outputTokens

long

输出 Token 数量

400

totalTokens

long

总 token 量

891

## 示例

正常返回示例

`JSON`格式

```
{
  "code": 200,
  "message": "success",
  "requestId": "299C57B2-EBB4-57E2-A6FE-723B874ACB74",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "translation": "How does Mogujie solve the data annotation challenge by building a platform?",
    "detectedLang": "",
    "usage": {
      "inputTokens": 491,
      "outputTokens": 400,
      "totalTokens": 891
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

2026-04-15

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/TextTranslate?updateTime=2026-04-15#workbench-doc-change-demo)

2026-03-26

OpenAPI 错误码发生变更、OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/TextTranslate?updateTime=2026-03-26#workbench-doc-change-demo)

2025-12-25

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/TextTranslate?updateTime=2025-12-25#workbench-doc-change-demo)

2025-12-11

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/TextTranslate?updateTime=2025-12-11#workbench-doc-change-demo)

2025-11-25

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/TextTranslate?updateTime=2025-11-25#workbench-doc-change-demo)
