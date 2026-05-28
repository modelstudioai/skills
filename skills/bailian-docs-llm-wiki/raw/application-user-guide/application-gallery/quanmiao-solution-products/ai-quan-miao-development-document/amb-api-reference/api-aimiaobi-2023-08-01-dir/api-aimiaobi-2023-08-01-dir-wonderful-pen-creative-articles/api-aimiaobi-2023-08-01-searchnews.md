# SearchNews - 信息检索

根据输入检索新闻，目前仅支持互联网搜索。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SearchNews)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SearchNews)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

aimiaobi:SearchNews

list

\*全部资源

`*`

无

无

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/quanmiao-paas-agentkey-get-guide)

xxxxx\_p\_efm

SearchSources

array

否

检索源列表

string

否

搜索源 code。非必填、目前仅支持：QuarkCommonNews。

QuarkCommonNews

Query

string

否

检索 Query

检索Query

PageSize

integer

否

每页记录数，默认 10

10

Page

integer

否

当前页号。默认 1

1

IncludeContent

boolean

否

是否包含正文

false

FilterNotNull

boolean

否

是否过滤空内容

false

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

PageResult

Code

string

状态码

successful

Current

integer

当前页码

1

Data

array<object>

业务数据

object

返回结果。

Author

string

作者（部分新闻可能没有）

作者

Content

string

内容（必返回）

文章内容

DocUuid

string

内部文档唯一标识（必返回）

9a598b44c6444da5907b8ea68a5f82c4

ImageUrls

array

图片地址（已经不会返回，不建议使用）

string

新闻图像的 URL。

https://www.example.com/aaaa.jpg

PubTime

string

发布时间（必返回）

2024-01-18 06:46:22

SearchSource

string

内部搜索源标识（必返回）

QuarkCommonNews

SearchSourceName

string

内部搜索源名称（必返回）

夸克检索

Source

string

来源（部分新闻可能没有）

央视网

Summary

string

文章摘要（部分新闻可能没有）

文章摘要

Tag

string

标签（部分新闻可能没有）

文章标签

Title

string

标题（必返回）

文章标题

UpdateTime

string

系统更新时间（已经不会返回，不建议使用）

2024-01-18 06:46:22

Url

string

文章 URL（必返回）

文章URL

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

Size

integer

每页记录数

10

Success

boolean

是否成功：true 成功，false 失败

true

Total

integer

总记录数

100

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Current": 1,
  "Data": [
    {
      "Author": "作者",
      "Content": "文章内容",
      "DocUuid": "9a598b44c6444da5907b8ea68a5f82c4",
      "ImageUrls": [
        "https://www.example.com/aaaa.jpg"
      ],
      "PubTime": "2024-01-18 06:46:22",
      "SearchSource": "QuarkCommonNews",
      "SearchSourceName": "夸克检索",
      "Source": "央视网",
      "Summary": "文章摘要",
      "Tag": "文章标签",
      "Title": "文章标题",
      "UpdateTime": "2024-01-18 06:46:22",
      "Url": "文章URL"
    }
  ],
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Size": 10,
  "Success": true,
  "Total": 100
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/SearchNews#workbench-doc-change-demo)。
