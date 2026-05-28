# GetMaterialById - 获取素材

获取素材：获取素材库中素材详细信息。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetMaterialById)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetMaterialById)

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

aimiaobi:GetMaterialById

get

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

67c520d1fa43455ea44fb69fa402d54d\_p\_beebot\_public

Id

long

是

任务主键 ID

60

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

object

业务数据

Author

string

作者

文档作者

CreateTime

string

创建时间

2023-03-21 11:34:19

CreateUser

string

创建用户 ID

1

DocKeywords

array

文档标签用于分类等、不同 keyword 之间逗号分割

DocKeyword

string

关键词

关键词

DocType

string

文档类型，pdf、word、url、image

pdf

ExternalUrl

string

外部客户上传的 URL，仅用作记录保存

https://www.example.com

HtmlContent

string

网页内容

网页内容

Id

long

主键

32

PubTime

string

发布时间

2023-04-11 06:14:07

PublicUrl

string

临时的对外公开的 URL

https://www.example.com

ShareAttr

integer

公开属性，按位存储，第一位表示是否在业务空间内共享、第二位表示是否在租户内共享，第三位表示在系统范围内共享

1

SrcFrom

string

文档来源，user\_upload、search、viewpoint

user\_upload

Summary

string

文档摘要

文档摘要

TextContent

string

解析后的文本内容，对于图片来说为空

文本内容

ThumbnailInBase64

string

图片文档类型的 Base64 缩略图

Base64编码的缩略图

Title

string

文档标题

文档标题

UpdateTime

string

修改时间

2022-04-08 19:33:01

UpdateUser

string

修改用户 ID

1

Url

string

内部文档保存的 URL

https://www.example.com

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
  "Data": {
    "Author": "文档作者",
    "CreateTime": "2023-03-21 11:34:19",
    "CreateUser": 1,
    "DocKeywords": [
      "关键词"
    ],
    "DocType": "pdf",
    "ExternalUrl": "https://www.example.com\n",
    "HtmlContent": "网页内容",
    "Id": 32,
    "PubTime": "2023-04-11 06:14:07\n",
    "PublicUrl": "https://www.example.com\n",
    "ShareAttr": 1,
    "SrcFrom": "user_upload",
    "Summary": "文档摘要",
    "TextContent": "文本内容",
    "ThumbnailInBase64": "Base64编码的缩略图",
    "Title": "文档标题",
    "UpdateTime": "2022-04-08 19:33:01",
    "UpdateUser": 1,
    "Url": "https://www.example.com"
  },
  "HttpStatusCode": 200,
  "Message": "数据不存在",
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Success": false
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
