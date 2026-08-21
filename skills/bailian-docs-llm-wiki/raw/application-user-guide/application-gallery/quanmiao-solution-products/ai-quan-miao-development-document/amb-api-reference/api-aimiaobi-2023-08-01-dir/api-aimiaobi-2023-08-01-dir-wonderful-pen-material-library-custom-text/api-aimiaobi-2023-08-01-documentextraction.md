# DocumentExtraction - 文档提取

从链接中提取文档内容。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/DocumentExtraction)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/DocumentExtraction)

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

aimiaobi:DocumentExtraction

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

xxxxx\_p\_efm

Urls

array

是

待提取的链接列表

Url

string

是

URL 链接，URL 长度不能超过 2048

http://www.example.com/

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

successful

Data

array<object>

业务数据

Data

object

文档对象

Author

string

作者

作者

Content

string

内容

文章内容

DocId

string

文档-自定义的唯一 ID

文档-自定义的唯一ID

DocUuid

string

内部文档唯一标识

8df2d69d63a247b6b52ff455b2d426b6

PubTime

string

发布时间

2024-05-14 08:54:33

Source

string

来源

新闻来源

Summary

string

文章摘要

文章摘要

Tag

string

标签

文章标签

Title

string

标题

文章标题

Url

string

文章 URL

https://www.example.com/aaa.docx

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

successful

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Data": [
    {
      "Author": "作者",
      "Content": "文章内容",
      "DocId": "文档-自定义的唯一ID",
      "DocUuid": "8df2d69d63a247b6b52ff455b2d426b6",
      "PubTime": "2024-05-14 08:54:33",
      "Source": "新闻来源",
      "Summary": "文章摘要",
      "Tag": "文章标签",
      "Title": "文章标题",
      "Url": "https://www.example.com/aaa.docx"
    }
  ],
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
