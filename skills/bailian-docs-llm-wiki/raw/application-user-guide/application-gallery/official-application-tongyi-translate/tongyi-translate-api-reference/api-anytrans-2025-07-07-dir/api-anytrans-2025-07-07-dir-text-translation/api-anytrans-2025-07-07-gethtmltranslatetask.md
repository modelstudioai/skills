# GetHtmlTranslateTask - 获取html翻译任务结果

通义多模态翻译获取html翻译结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AnyTrans/2025-07-07/GetHtmlTranslateTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AnyTrans/2025-07-07/GetHtmlTranslateTask)

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

anytrans:GetHtmlTranslateTask

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /anytrans/translate/html/get HTTP/1.1
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

否

html 翻译任务 id

868c2fdd-96c2-4546-96d2-a259b8f35252

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

04B53310-CB1A-14B4-AC85-26C154D8366A

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

translation

string

翻译结果

<!DOCTYPE html> <html lang="zh-CN"> <head> <meta charset="utf-8"/> <meta content="width=device-width, initial-scale=1.0" name="viewport"/> <title>My First Webpage</title> </head> <body> <h1>Welcome to my webpage!</h1> <p>This is a simple HTML page.</p> <p>Learning HTML is the first step to entering web development.</p> <a href="https://www.example.com">Click here to visit the sample website</a> </body> </html>

usage

object

token 用量

inputTokens

long

输入 token 数

22

outputTokens

long

输出 token 数

19

totalTokens

long

总 token 数

41

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "success",
  "message": "success",
  "requestId": "04B53310-CB1A-14B4-AC85-26C154D8366A",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "translation": "<!DOCTYPE html>\n\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\"/>\n<meta content=\"width=device-width, initial-scale=1.0\" name=\"viewport\"/>\n<title>My First Webpage</title>\n</head>\n<body>\n<h1>Welcome to my webpage!</h1>\n<p>This is a simple HTML page.</p>\n<p>Learning HTML is the first step to entering web development.</p>\n<a href=\"https://www.example.com\">Click here to visit the sample website</a>\n</body>\n</html>",
    "usage": {
      "inputTokens": 22,
      "outputTokens": 19,
      "totalTokens": 41
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

暂无变更历史
