# GetStyleLearningResult - 获取文体学习分析结果

获取文体学习分析结果。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetStyleLearningResult)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetStyleLearningResult)

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

aimiaobi:GetStyleLearningResult

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

业务空间唯一标识：AgentKey

xxxxx\_p\_efm

Id

long

是

文体学习 ID

39

## 返回参数

名称

类型

描述

示例值

object

PlainResult

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

Data

object

业务数据

MaterialIdList

array

素材 ID 集合

MaterialIdList

long

素材库 ID

4

CustomTextIdList

array

自定义内容 ID 集合

CustomTextIdList

long

自定义内容 ID

25

ContentList

array<object>

自定义内容实体内容

ContentList

object

自定义内容

Id

long

主键 ID

1

Title

string

标题

标题

Content

string

内容

内容

CreateTime

string

创建时间

创建时间

UpdateTime

string

修改时间

修改时间

CreateUser

string

创建用户

创建用户

UpdateUser

string

修改用户

修改用户

MaterialInfoList

array<object>

素材详细信息

MaterialInfoList

object

Id

long

主键

50

DocType

string

文档类型，pdf、word、url、image

文档类型，pdf、word、url、image

Title

string

文档标题

文档标题

Summary

string

文档摘要

文档摘要

Author

string

作者

作者

PubTime

string

发布时间

发布时间

DocKeywords

array

文档标签用于分类等、不同 keyword 之间逗号分割

DocKeyword

string

关键词

中欧

Url

string

内部文档保存的 URL，支持多协议，http://,file://,ftp://:客户上传时保存到内部存储的 URL、长期保存、到期删除

内部文档保存的URL，支持多协议，http://,file://,ftp://:客户上传时保存到内部存储的URL、长期保存、到期删除

PublicUrl

string

临时的对外公开的 URL

临时的对外公开的URL

ExternalUrl

string

外部客户上传的 URL，仅用作记录保存

外部客户上传的URL，仅用作记录保存

SrcFrom

string

文档来源，user\_upload、search、viewpoint

文档来源，user\_upload、search、viewpoint

TextContent

string

解析后的文本内容，对于图片来说为空

解析后的文本内容，对于图片来说为空

HtmlContent

string

解析后的原始 html 内容

解析后的原始html内容

ShareAttr

integer

公开属性，按位存储，第一位表示是否在业务空间内共享、第二位表示是否在租户内共享，第三位表示在系统范围内共享

1

CreateTime

string

创建时间

创建时间

UpdateTime

string

修改时间

修改时间

CreateUser

string

创建用户 ID

创建用户ID

CreateUserName

string

创建用户姓名

创建用户姓名

UpdateUser

string

修改用户 ID

修改用户ID

UpdateUserName

string

修改用户姓名

修改用户姓名

ThumbnailInBase64

string

图片文档类型的 Base64 缩略图

图片文档类型的Base64缩略图

FileLength

integer

文件内容长度

41

Id

long

文体学习分析结果 ID

33

TaskId

string

文体分析时的任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

AigcResult

string

AIGC 生成的内容

AIGC 生成的内容

RewriteResult

string

用户修订后内容

用户修订后内容

StyleName

string

用户修订后内容

用户修订后内容

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200,
  "Data": {
    "MaterialIdList": [
      4
    ],
    "CustomTextIdList": [
      25
    ],
    "ContentList": [
      {
        "Id": 1,
        "Title": "标题",
        "Content": "内容",
        "CreateTime": "创建时间",
        "UpdateTime": "修改时间",
        "CreateUser": "创建用户",
        "UpdateUser": "修改用户"
      }
    ],
    "MaterialInfoList": [
      {
        "Id": 50,
        "DocType": "文档类型，pdf、word、url、image",
        "Title": "文档标题",
        "Summary": "文档摘要",
        "Author": "作者",
        "PubTime": "发布时间",
        "DocKeywords": [
          "中欧"
        ],
        "Url": "内部文档保存的URL，支持多协议，http://,file://,ftp://:客户上传时保存到内部存储的URL、长期保存、到期删除",
        "PublicUrl": "临时的对外公开的URL",
        "ExternalUrl": "外部客户上传的URL，仅用作记录保存",
        "SrcFrom": "文档来源，user_upload、search、viewpoint",
        "TextContent": "解析后的文本内容，对于图片来说为空",
        "HtmlContent": "解析后的原始html内容",
        "ShareAttr": 1,
        "CreateTime": "创建时间",
        "UpdateTime": "修改时间",
        "CreateUser": "创建用户ID",
        "CreateUserName": "创建用户姓名",
        "UpdateUser": "修改用户ID",
        "UpdateUserName": "修改用户姓名",
        "ThumbnailInBase64": "图片文档类型的Base64缩略图",
        "FileLength": 41
      }
    ],
    "Id": 33,
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "AigcResult": "AIGC 生成的内容",
    "RewriteResult": "用户修订后内容",
    "StyleName": "用户修订后内容"
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
