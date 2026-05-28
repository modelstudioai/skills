# GenerateOutputFormat - 获取输出格式示例

轻应用-标签挖掘-获取示例输出格式。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GenerateOutputFormat)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GenerateOutputFormat)

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

quanmiaolightapp:GenerateOutputFormat

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/generateOutputFormat HTTP/1.1
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

业务空间唯一标识

llm-xxxxxxx

businessType

string

否

业务类型

clueMining

taskDescription

string

否

任务描述

给你一条待分析文本数据，请你按照标签体系来对数据进行打标。

content

string

否

待分析文本

待分析文本

tags

array<object>

是

标签体系列表

object

是

标签体系对象

tagName

string

否

标签名称

xxxx

tagDefinePrompt

string

否

标签定义提示词

xxxx

extraInfo

string

否

额外信息

额外信息

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

code

string

状态码

successful

data

object

示例格式对象

outputFormat

string

输出格式

请直接以如下JSON格式输出，不要输出其他内容： { "是否近期买房": "", "购房付款方式": "", "家庭人口数量": "", "房间数量需求": "", "买房投资诉求": "", "客户买房类型": "", "客户买房预算": "", "客户居住地": "", "用户核心需求": \[ "" \], "年龄": "", "性别": "", "职业":"" }

httpStatusCode

integer

http 状态码

200

message

string

错误说明

ok

requestId

string

Id of the request

117F5ABE-CF02-5502-9A3F-E56BC9081A64

success

boolean

是否成功：true 成功，false 失败

True

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "successful",
  "data": {
    "outputFormat": "请直接以如下JSON格式输出，不要输出其他内容：\n{\n    \"是否近期买房\": \"\",\n    \"购房付款方式\": \"\",\n    \"家庭人口数量\": \"\",\n    \"房间数量需求\": \"\",\n    \"买房投资诉求\": \"\",\n    \"客户买房类型\": \"\",\n    \"客户买房预算\": \"\",\n    \"客户居住地\": \"\",\n    \"用户核心需求\": [\n        \"\"\n    ],\n    \"年龄\": \"\",\n    \"性别\": \"\",\n    \"职业\":\"\"\n}\n"
  },
  "httpStatusCode": 200,
  "message": "ok",
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64",
  "success": true
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
