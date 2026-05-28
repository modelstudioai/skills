# GetDocTranslateTask - 文档翻译结果获取

通义多模态翻译获取文档翻译结果

## 接口说明

文档翻译结果查询接口

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AnyTrans/2025-07-07/GetDocTranslateTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AnyTrans/2025-07-07/GetDocTranslateTask)

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

anytrans:GetDocTranslateTask

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /anytrans/translate/doc/get HTTP/1.1
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

taskId

string

是

文档翻译任务 id

d3a2397bc2c14ab4a2e40a4f5b46241b

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

响应消息

success

requestId

string

请求 id，用于追溯 API 调用链路

AC642EEB-C29D-54DF-8F52-622565BBB78A

success

boolean

接口调用是否成功

true

httpStatusCode

string

http 响应码

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

翻译状态

枚举值：

-   translating：翻译中。
-   translated：翻译完成。

translated

charactersCount

integer

字符统计

4

pageCount

integer

页数统计

2

translateFileUrl

string

翻译结果 URL

http://translate-ai-data-dev.oss-cn-hangzhou.aliyuncs.com/tongyiTranslate/123456789/a7630164ce894c799cca0f0822c36f84\_merge.md

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "success",
  "message": "success",
  "requestId": "AC642EEB-C29D-54DF-8F52-622565BBB78A",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "taskId": "d3a2397bc2c14ab4a2e40a4f5b46241b",
    "status": "translated",
    "charactersCount": 4,
    "pageCount": 2,
    "translateFileUrl": "http://translate-ai-data-dev.oss-cn-hangzhou.aliyuncs.com/tongyiTranslate/123456789/a7630164ce894c799cca0f0822c36f84_merge.md"
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

暂无变更历史
