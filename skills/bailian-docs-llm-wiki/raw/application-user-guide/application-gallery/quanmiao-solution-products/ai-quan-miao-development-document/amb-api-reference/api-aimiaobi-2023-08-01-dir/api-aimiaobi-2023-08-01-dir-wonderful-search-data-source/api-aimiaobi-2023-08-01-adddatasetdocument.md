# AddDatasetDocument - 数据源-添加文档到数据集

添加文档到数据源。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/AddDatasetDocument)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/AddDatasetDocument)

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

aimiaobi:AddDatasetDocument

create

\*全部资源

`*`

无

无

## 请求语法

```
POST  HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

DatasetId

integer

否

数据集唯一标识

1

DatasetName

string

否

数据集名称

数据集名称

Document

object

是

文档

DocUuid

string

否

文档系统唯一 ID：自动生成，不建议传入

xxxx

Url

string

否

文章 URL：公网可访问地址

http://xxx

Content

string

否

内容

正文

Summary

string

否

文章摘要

文章摘要

Title

string

否

文档标题

标题

PubTime

string

否

发布时间

2024-12-09 13:35:40

SourceFrom

string

否

来源

xxx媒体

MultimodalIndexName

string

否

废弃：不可用

xxxx

DisableHandleMultimodalMedia

boolean

否

当前记录多模态数据（图片、视频）是否落索引库，默认 true

false

MultimodalMedias

array<object>

否

文档中多模态数据列表：

-   仅富文本等文档中存在多模态数据（图片、视频）时，可以通过这个字段传入，进而可以在搜索接口召回对应数据。
    
-   文档本身为多模态数据时，此字段为空，通过 docType+url 指定数据即可。
    

object

否

多模态数据

MediaId

string

否

多模态数据唯一标识：不建议传入，系统会自动生成

xxxx

MediaType

string

否

多模态数据类型：

-   image：图片
    
-   video：视频
    

image

FileUrl

string

否

文件地址：公网可访问

http://xxx

DocId

string

否

文档业务侧唯一 ID

xx

DocType

string

否

文档类型：

-   plainText：纯文本，content 必选
    
-   richText：富文本：html，content 必选
    
-   text：文本文件，url 必选
    
-   pdf：url 必选
    
-   word：url 必选
    
-   image：图片，url 必选，支持 gif、png、jpg、jpeg 等大多数常见图片格式
    
-   video：视频，url 必选，支持 MP4、AVI、WMV、MOV 等大多数常见视频格式
    

image

Extend1

string

否

扩展字段 1

xxx

Extend2

string

否

扩展字段 2

xxxx

Extend3

string

否

扩展字段 3

xxx

Metadata

object

否

meta 信息

VideoShots

array<object>

否

分镜信息

object

否

分镜信息

StartTime

integer

否

开始时间；毫秒

1000

EndTime

integer

否

结束时间：毫秒

2000

Text

string

否

分镜分析文本信息

xxx

AsrSentences

array<object>

否

语音或者字幕信息

object

否

语音或者字幕信息

StartTime

integer

否

开始时间：毫秒

1000

EndTime

integer

否

技术时间：毫秒

2000

Text

string

否

语音或者字幕信息

xxx

Text

string

否

meta 描述信息：废弃字段

xxx

KeyValues

array<object>

否

keyValue 结构 metadata

object

否

keyValue 结构 metadata

Key

string

否

名称

xx

Value

string

否

参数值

xx

CategoryUuid

string

否

类目唯一标识

xx

Tags

array

否

标签名称

string

否

标签名称

xx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应结果

Data

object

业务数据

DocUuid

string

文档系统唯一标识

8df2d69d63a247b6b52ff455b2d426b6

DocId

string

文档业务侧唯一标识

xxx

Status

integer

状态：

-   1：创建完成
    
-   2：文本索引构建完成
    
-   3：多模态索引构建完成
    
-   100：全量构建完成
    
-   0：失败
    

1

ErrorCode

string

异常错误码

Success

ErrorMessage

string

错误信息

错误信息

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

## 示例

正常返回示例

`JSON`格式

```
{
  "Data": {
    "DocUuid": "8df2d69d63a247b6b52ff455b2d426b6",
    "DocId": "xxx",
    "Status": 1,
    "ErrorCode": "Success",
    "ErrorMessage": "错误信息"
  },
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/AddDatasetDocument#workbench-doc-change-demo)。
