# ListDatasetDocuments - 数据源-文档列表

查询数据源文档列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDatasetDocuments)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDatasetDocuments)

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

aimiaobi:ListDatasetDocuments

list

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

Query

string

否

搜索条件

搜索条件

DatasetId

integer

否

数据集唯一标识：DatasetName、DatasetId 二选一必填

1

DatasetName

string

否

数据集名称

数据集名称

Status

integer

否

文档状态：

-   1：创建完成
    
-   2：文本索引构建完成
    
-   3：多模态索引构建完成
    
-   100：全量构建完成
    
-   0：失败
    

100

DocType

string

否

文档类型：

-   plainText：纯文本
    
-   richText：富文本
    
-   text：文本文件
    
-   pdf：
    
-   word：
    
-   image：图片
    
-   video：视频
    

text

DatasetDescription

string

否

废弃

xx

IncludeFields

array

否

包括字段

string

否

包括字段

-   content：正文
    
-   chunks：片段
    

content

ExcludeFields

array

否

排除字段：

-   content：正文
    

string

否

排除字段

content

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

CategoryUuids

array

否

类目唯一标识

string

否

类目唯一标识

xx

Tags

array

否

标签

string

否

标签

xx

Extend1

string

否

自定义扩展字段。

xx

Extend2

string

否

自定义扩展字段。

xx

Extend3

string

否

自定义扩展字段。

xx

CreateTimeStart

integer

否

起始创建时间，时间戳形式。

111

CreateTimeEnd

integer

否

截止创建时间，时间戳形式。

111

DocUuids

array

否

文档唯一标识

string

否

文档唯一标识

xxx

DocIds

array

否

文档 ID 数组

string

否

文档 ID

xxx

StartTime

integer

否

开始时间；毫秒

111

EndTime

integer

否

结束时间：毫秒

1111

Title

string

否

标题

xxx

NextToken

string

否

下一页的唯一标识：查询第 10000 条以上数据时，必传

xxx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应结果

Data

array<object>

业务数据

array<object>

业务数据

DocUuid

string

内部文档唯一 ID

内部文档唯一ID

Url

string

url

https://xxx/xx

Content

string

正文

xx

Summary

string

文章摘要

xx

Title

string

标题

xx

PubTime

string

发布时间

2022-01-01 00:00:00

SourceFrom

string

来源

来源

DisableHandleMultimodalMedia

boolean

当前记录是否落多模态索引库

false

MultimodalMedias

array<object>

多模态信息

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

DocId

string

用户指定的文档唯一 ID

xx

DocType

string

文档类型

text

Status

integer

文档索引构建状态

100

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

CreateTime

string

创建时间

2025-04-14 19:59:53

UpdateTime

string

修改时间

2025-04-14 19:59:53

UpdateUser

string

更新用户

1

CreateUser

string

创建者

1

Tags

array

标签。

string

标签。

xx

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

NextToken

string

下一页的唯一标识

xxx

## 示例

正常返回示例

`JSON`格式

```
{
  "Data": [
    {
      "DocUuid": "内部文档唯一ID",
      "Url": "https://xxx/xx",
      "Content": "xx",
      "Summary": "xx",
      "Title": "xx",
      "PubTime": "2022-01-01 00:00:00",
      "SourceFrom": "来源",
      "DisableHandleMultimodalMedia": false,
      "MultimodalMedias": [
        {
          "MediaId": "多模态数据唯一标识",
          "MediaType": "多模态数据类型",
          "FileUrl": "图片或视频文件地址"
        }
      ],
      "DocId": "xx",
      "DocType": "text",
      "Status": 100,
      "CategoryUuid": "xx",
      "Extend1": "xx",
      "Extend2": "xx",
      "Extend3": "xx",
      "CreateTime": "2025-04-14 19:59:53",
      "UpdateTime": "2025-04-14 19:59:53",
      "UpdateUser": "1",
      "CreateUser": "1",
      "Tags": [
        "xx"
      ]
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
  "NextToken": "xxx"
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListDatasetDocuments#workbench-doc-change-demo)。
