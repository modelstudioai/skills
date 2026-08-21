# ListMaterialDocuments - 获取素材列表

获取素材列表：获取素材库中素材列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListMaterialDocuments)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListMaterialDocuments)

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

aimiaobi:ListMaterialDocuments

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

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

33a2658aaabf4c24b45d50e575125311\_p\_beebot\_public

Query

string

否

支持对 title、content、content 的综合查询

小猫

Id

long

否

素材主键 ID

69

Title

string

否

根据素材标题全文检索

新闻标题

DocType

string

否

文档类型 (html: 网页, plainText: 纯文本, image: 图片, pdf: pdf, word: word, excel: excel, csv: csv, jsonLine: jsonLine)

jsonLine

DocTypeList

array

否

文档类型列表 (html: 网页, plainText: 纯文本, image: 图片, pdf: pdf, word: word, excel: excel, csv: csv, jsonLine: jsonLine)

DocTypeList

string

否

文件类型对象。

html

Content

string

否

文档内容全文检索

新闻内容

ShareAttr

integer

否

共享属性：0：个人私有，1：业务空间范围内共享

1

Keywords

array

否

文档关键词

Keyword

string

否

关键词

关键词

CreateTimeStart

string

否

创建时间-开始范围，格式：yyyy-MM-dd HH:mm:ss

2023-02-19 07:28:11

CreateTimeEnd

string

否

创建时间-结束范围，格式：yyyy-MM-dd HH:mm:ss

2023-03-18 02:00:00

UpdateTimeStart

string

否

更新时间-开始范围，格式：yyyy-MM-dd HH:mm:ss

2023-03-18 02:00:00

UpdateTimeEnd

string

否

更新时间-结束范围，格式：yyyy-MM-dd HH:mm:ss

2023-03-18 03:00:00

GeneratePublicUrl

boolean

否

是否生成文件公共 URL

true

Current

integer

否

当前页码

1

Size

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

返回分页后的素材列表

Code

string

状态码

DataNotExists

Current

integer

当前页码

1

Data

array<object>

列表对象

Data

object

素材对象

Author

string

作者

作者

CreateTime

string

创建时间

2023-03-18 02:00:00

CreateUser

string

创建用户 ID

"1"

CreateUserName

string

创建用户姓名

创建用户名

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

35

PubTime

string

发布时间，格式：yyyy-MM-dd HH:mm:ss

2023-03-18 02:00:00

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

摘要

TextContent

string

解析后的文本内容，对于图片来说为空

文档内容

ThumbnailInBase64

string

图片文档类型的 Base64 缩略图

base64编码的图像二进制数据

Title

string

文档标题

文档标题

UpdateTime

string

修改时间

2023-03-18 02:00:00

UpdateUser

string

修改用户 ID

"1"

UpdateUserName

string

修改用户姓名

更新用户名

Url

string

内部文档保存的 URL，支持多协议，http://,file://,ftp://:客户上传时保存到内部存储的 URL、长期保存、到期删除

https://www.example.com

FileKey

string

文件唯一标识

oss://default/oss-bucket-name/aimiaobi/2021/07/01/1625126400000/1.docx

FileAttr

object

媒体文件属性

Duration

double

时长。

120

FileName

string

文件名

xxx.mp4

Width

integer

视频宽度

100

MimeType

string

文件 MIME 类型

image/png

FileLength

long

文件内容长度

1048576

Height

integer

视频高度

1024

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

Size

integer

每页记录数

10

Success

boolean

是否成功：true 成功，false 失败

false

Total

integer

总记录数

100

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "DataNotExists",
  "Current": 1,
  "Data": [
    {
      "Author": "作者\n\n",
      "CreateTime": "2023-03-18 02:00:00\n",
      "CreateUser": 1,
      "CreateUserName": "创建用户名",
      "DocKeywords": [
        "关键词"
      ],
      "DocType": "pdf",
      "ExternalUrl": "https://www.example.com\n",
      "HtmlContent": "网页内容",
      "Id": 35,
      "PubTime": "2023-03-18 02:00:00\n",
      "PublicUrl": "https://www.example.com\n",
      "ShareAttr": 1,
      "SrcFrom": "user_upload",
      "Summary": "摘要",
      "TextContent": "文档内容",
      "ThumbnailInBase64": "base64编码的图像二进制数据",
      "Title": "文档标题\n\n",
      "UpdateTime": "2023-03-18 02:00:00\n",
      "UpdateUser": 1,
      "UpdateUserName": "更新用户名",
      "Url": "https://www.example.com",
      "FileKey": "oss://default/oss-bucket-name/aimiaobi/2021/07/01/1625126400000/1.docx",
      "FileAttr": {
        "Duration": 120,
        "FileName": "xxx.mp4",
        "Width": 100,
        "MimeType": "image/png",
        "FileLength": 1048576,
        "Height": 1024
      }
    }
  ],
  "HttpStatusCode": 200,
  "Message": "数据不存在",
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Size": 10,
  "Success": false,
  "Total": 100
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
