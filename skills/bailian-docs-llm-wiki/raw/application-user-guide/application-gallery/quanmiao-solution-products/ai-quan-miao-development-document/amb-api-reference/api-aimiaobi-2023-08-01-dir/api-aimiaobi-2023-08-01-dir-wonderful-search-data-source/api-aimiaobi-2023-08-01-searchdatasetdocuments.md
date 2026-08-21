# SearchDatasetDocuments - 数据源-搜索文档

搜索数据源文档。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SearchDatasetDocuments)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SearchDatasetDocuments)

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

aimiaobi:SearchDatasetDocuments

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

xx

Query

string

是

搜索内容

搜索内容

DatasetId

integer

否

数据集唯一标识：和 DatasetName 二选一必选

1

DatasetName

string

否

数据集名称

数据集名称

IncludeContent

boolean

否

是否包含正文：默认 false

false

Extend1

string

否

业务参数

业务参数

PageSize

string

否

返回数据条数

10

CategoryUuids

array

否

string

否

Tags

array

否

string

否

Extend2

string

否

Extend3

string

否

CreateTimeStart

integer

否

CreateTimeEnd

integer

否

StartTime

integer

否

EndTime

integer

否

DocUuids

array

否

string

否

DocIds

array

否

string

否

SearchMode

string

否

DocTypes

array

否

string

否

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

Documents

array<object>

文档列表

array<object>

文档列表

DocUuid

string

文档系统唯一 ID

xxx

Url

string

URL 链接

xx

Content

string

内容

xx

Summary

string

文章摘要

文章摘要

Title

string

标题

xx

PubTime

string

发布时间，格式：yyyy-MM-dd HH:mm:ss

2024-12-09 17:09:40

SourceFrom

string

来源

来源

DocId

string

文档用户侧唯一 ID

xx

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

Tags

array

标签。

string

标签名称

xx

SearchSourceType

string

数据集类型

xx

SearchSource

string

数据集唯一标识

xx

SearchSourceName

string

搜索信源名称

xx

Score

number

阈值

0.5

ChunkInfos

array<object>

仅 document 模式返回：文章维度相关 chunk 列表

object

片段

Chunk

string

片段

xx

Score

number

阈值

0.77

Chunk

string

仅 chunk 模式返回：片段

xx

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
    "Documents": [
      {
        "DocUuid": "xxx",
        "Url": "xx",
        "Content": "xx",
        "Summary": "文章摘要",
        "Title": "xx",
        "PubTime": "2024-12-09 17:09:40",
        "SourceFrom": "来源",
        "DocId": "xx",
        "DocType": "text",
        "CategoryUuid": "xx",
        "Extend1": "xx",
        "Extend2": "xx",
        "Extend3": "xx",
        "Tags": [
          "xx"
        ],
        "SearchSourceType": "xx",
        "SearchSource": "xx",
        "SearchSourceName": "xx",
        "Score": 0.5,
        "ChunkInfos": [
          {
            "Chunk": "xx",
            "Score": 0.77
          }
        ],
        "Chunk": "xx"
      }
    ]
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/SearchDatasetDocuments#workbench-doc-change-demo)。
