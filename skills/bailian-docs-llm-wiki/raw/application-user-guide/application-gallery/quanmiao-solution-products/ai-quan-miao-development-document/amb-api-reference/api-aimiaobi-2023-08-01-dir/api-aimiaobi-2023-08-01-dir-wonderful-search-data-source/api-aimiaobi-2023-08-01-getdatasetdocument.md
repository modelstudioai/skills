# GetDatasetDocument - 数据源-获取文档详情

获取数据源文档。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetDatasetDocument)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetDatasetDocument)

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

aimiaobi:GetDatasetDocument

get

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

xxxx

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

DocUuid

string

否

内部文档唯一标识

xxx

DocId

string

否

文档-自定义的唯一 ID

xxx

IncludeFields

array

否

包含的字段列表

string

否

包含的字段：比如 metadata

metadata

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

文档系统唯一 ID

xxx

Url

string

文章 URL

https://www.aliyun.com

Content

string

内容

文章内容

Summary

string

文章摘要

文章摘要

Title

string

标题

文档标题

PubTime

string

发布时间，格式：yyyy-MM-dd HH:mm:ss

2024-05-14 08:54:33

SourceFrom

string

来源

来源

DisableHandleMultimodalMedia

boolean

当前记录是否落多模态索引库

true

DocId

string

文档用户侧唯一 ID

xxx

Metadata

object

字典信息

Text

string

文档维度 meta

xx

VideoShots

array<object>

视频分片信息

object

视频分片信息

StartTime

integer

视频分片开始时间：毫秒

1000

EndTime

integer

视频分片结束时间：毫秒

2000

Text

string

视频分片：内容

xxx

AsrSentences

array<object>

asr 结果

object

asr 结果

StartTime

integer

开始时间：毫秒

1000

EndTime

integer

结束时间：毫秒

2000

Text

string

asr 内容

xxx

KeyValues

array<object>

object

Key

string

Value

string

DocType

string

文档类型：比如 video、image

video

Status

integer

文档状态：100：成功 0：失败 1：索引或排队中

100

CategoryUuid

string

Tags

array

string

Extend1

string

Extend2

string

Extend3

string

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
    "DocUuid": "xxx",
    "Url": "https://www.aliyun.com",
    "Content": "文章内容",
    "Summary": "文章摘要",
    "Title": "文档标题\n\n",
    "PubTime": "2024-05-14 08:54:33",
    "SourceFrom": "来源",
    "DisableHandleMultimodalMedia": true,
    "DocId": "xxx",
    "Metadata": {
      "Text": "xx",
      "VideoShots": [
        {
          "StartTime": 1000,
          "EndTime": 2000,
          "Text": "xxx"
        }
      ],
      "AsrSentences": [
        {
          "StartTime": 1000,
          "EndTime": 2000,
          "Text": "xxx"
        }
      ],
      "KeyValues": [
        {
          "Key": "",
          "Value": ""
        }
      ]
    },
    "DocType": "video",
    "Status": 100,
    "CategoryUuid": "",
    "Tags": [
      ""
    ],
    "Extend1": "",
    "Extend2": "",
    "Extend3": ""
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/GetDatasetDocument#workbench-doc-change-demo)。
