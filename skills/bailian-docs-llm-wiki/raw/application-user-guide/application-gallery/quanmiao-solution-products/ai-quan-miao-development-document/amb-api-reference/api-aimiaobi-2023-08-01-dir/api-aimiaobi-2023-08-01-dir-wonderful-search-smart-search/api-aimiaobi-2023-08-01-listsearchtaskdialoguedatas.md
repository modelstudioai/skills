# ListSearchTaskDialogueDatas - 查询搜索生成任务对话详情中数据列表

查询搜索生成任务对话详情中数据列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListSearchTaskDialogueDatas)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListSearchTaskDialogueDatas)

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

aimiaobi:ListSearchTaskDialogueDatas

list

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

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

Query

string

否

查询条件

xx

TaskId

string

否

任务唯一标识

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

xxx

OriginalSessionId

string

否

历史对话唯一标识：全量原始素材来源

xx

SessionId

string

是

历史对话唯一标识：参考素材来源

xx

MultimodalSearchType

string

否

搜索数据类型

text

SearchModel

string

否

搜索 agent 类型

ClusterGenerate

SearchModelDataValue

string

否

搜索 agent 分类下的数据

xxx

IncludeContent

boolean

否

是否包含正文

true

PageNumber

integer

否

当前页码

1

PageSize

integer

否

每页条数：默认 10

10

## 返回参数

名称

类型

描述

示例值

object

响应结果

RealtimeSearch

boolean

是否实时搜索

true

SearchType

string

搜索类型

realtime

Articles

array<object>

文章列表

Article

object

文章

PubTime

string

发布时间

2024-11-25 14:25:59

Source

string

来源

新华社

Title

string

标题

文章标题

Content

string

内容

文章内容

Author

string

作者

作者

Url

string

文章 URL

https://www.example.com/aaa.docx

Summary

string

文章摘要

文章摘要

DocUuid

string

内部文档唯一标识

xxx

DocId

string

文档-自定义的唯一 ID

文档-自定义的唯一ID

MultimodalMedias

array<object>

多模态信息

MultimodalMedia

object

多模态信息

MediaId

string

多模态数据唯一标识

多模态数据唯一标识

MediaType

string

多模态数据类型

多模态数据类型

FileUrl

string

图片或视频文件地址

图片或视频文件地址

DocType

string

文档类型

text

CategoryUuid

string

类目唯一标识

xx

Extend1

string

扩展字段 1

xx

Extend2

string

扩展字段 2

xx

Extend3

string

扩展字段 3

xx

Images

array<object>

图片列表

Image

object

图片对象

MediaId

string

多模态数据唯一标识

多模态数据唯一标识

MediaType

string

多模态数据类型

多模态数据类型

FileUrl

string

图片或视频文件地址

图片或视频文件地址

Videos

array<object>

视频列表

Video

object

视频信息列表

MediaId

string

多模态数据唯一标识

多模态数据唯一标识

MediaType

string

多模态数据类型

多模态数据类型

FileUrl

string

图片或视频文件地址

图片或视频文件地址

PageNumber

integer

当前页码

1

PageSize

integer

每页记录条数

10

TotalCount

integer

总记录条数

100

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

Code

string

状态码

NoData

Message

string

错误说明

success

HttpStatusCode

integer

http 状态码

200

Audios

array<object>

语音列表

Audio

object

语音信息

MediaId

string

多模态数据唯一标识

xxxx

FileUrl

string

图片或视频文件地址

http://xxx

## 示例

正常返回示例

`JSON`格式

```
{
  "RealtimeSearch": true,
  "SearchType": "realtime",
  "Articles": [
    {
      "PubTime": "2024-11-25 14:25:59",
      "Source": "新华社",
      "Title": "文章标题",
      "Content": "文章内容",
      "Author": "作者",
      "Url": "https://www.example.com/aaa.docx",
      "Summary": "文章摘要",
      "DocUuid": "xxx",
      "DocId": "文档-自定义的唯一ID",
      "MultimodalMedias": [
        {
          "MediaId": "多模态数据唯一标识",
          "MediaType": "多模态数据类型",
          "FileUrl": "图片或视频文件地址"
        }
      ],
      "DocType": "text",
      "CategoryUuid": "xx",
      "Extend1": "xx",
      "Extend2": "xx",
      "Extend3": "xx"
    }
  ],
  "Images": [
    {
      "MediaId": "多模态数据唯一标识",
      "MediaType": "多模态数据类型",
      "FileUrl": "图片或视频文件地址"
    }
  ],
  "Videos": [
    {
      "MediaId": "多模态数据唯一标识",
      "MediaType": "多模态数据类型",
      "FileUrl": "图片或视频文件地址"
    }
  ],
  "PageNumber": 1,
  "PageSize": 10,
  "TotalCount": 100,
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200,
  "Audios": [
    {
      "MediaId": "xxxx",
      "FileUrl": "http://xxx"
    }
  ]
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
