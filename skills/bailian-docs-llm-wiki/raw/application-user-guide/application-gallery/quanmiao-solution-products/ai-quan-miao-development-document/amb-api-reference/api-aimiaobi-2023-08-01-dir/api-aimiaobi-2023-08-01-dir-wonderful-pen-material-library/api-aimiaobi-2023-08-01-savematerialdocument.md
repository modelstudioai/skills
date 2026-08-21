# SaveMaterialDocument - 保存素材

保存素材：保存素材库中素材。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SaveMaterialDocument)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SaveMaterialDocument)

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

aimiaobi:SaveMaterialDocument

create

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

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

c160c841c8e54295bf2f441432785944\_p\_efm

DocType

string

是

文档类型 (html: 网页, plainText: 纯文本, image: 图片, pdf: pdf, word: word, excel: excel, csv: csv, jsonLine: jsonLine)

excel

Title

string

否

文档标题

新闻标题

Author

string

否

作者

作者名称

PubTime

string

否

发布时间,格式：yyyy-MM-dd HH:mm:ss

2023-04-11 06:14:07

DocKeywords

array

否

文档标签用于分类等

DocKeyword

string

否

关键词

关键词

Url

string

否

素材的 URL

http://xxxxx/xxx

ExternalUrl

string

否

外部客户上传的 URL，仅用作记录保存

http://xxxxx/xxx

SrcFrom

string

否

文档来源 (UserUpload: 用户上传, IntellijSearch: 智搜, HotViewPoint: 热点视角)

IntellijSearch

TextContent

string

否

解析后的文本内容，对于图片来说为空

文本内容

HtmlContent

string

否

带格式的内容

网页内容

ShareAttr

integer

否

共享属性：0：个人私有，1：业务空间范围内共享

1

BothSavePrivateAndShare

boolean

否

是否同时将素材保存为私有库与共享库

false

Summary

string

否

摘要

摘要

## 返回参数

名称

类型

描述

示例值

object

PlainResult

Code

string

状态码

DataNotExists

Data

long

业务数据

12

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

数据不存在

RequestId

string

请求唯一标识

3f7045e099474ba28ceca1b4eb6d6e21

Success

boolean

是否成功：true 成功，false 失败

false

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "DataNotExists",
  "Data": 12,
  "HttpStatusCode": 200,
  "Message": "数据不存在",
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Success": false
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
