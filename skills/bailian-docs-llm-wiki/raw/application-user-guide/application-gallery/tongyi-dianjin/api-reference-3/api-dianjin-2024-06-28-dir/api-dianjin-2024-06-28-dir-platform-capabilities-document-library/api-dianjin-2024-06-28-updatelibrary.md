# UpdateLibrary - 更新文档库

更新文档库，可用于更新文档库的名称、描述、索引配置等信息。

## 接口说明

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
    
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/UpdateLibrary)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/UpdateLibrary)

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

dianjin:UpdateLibrary

update

\*全部资源

`*`

无

无

## 请求语法

```
PUT /{workspaceId}/api/library/update HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

业务空间 id

llm-xxxxx

body

object

否

请求体参数。

description

string

否

文档库描述

文档库描述

indexSetting

object

否

文档库索引配置

chunkStrategy

object

否

分块策略

docTreeSplit

boolean

否

版面切分

true

docTreeSplitSize

integer

否

版面切分大小

160

enhanceGraph

boolean

否

是否增强图片

true

enhanceTable

boolean

否

是否增强表格

true

overlap

integer

否

chunk 重叠长度

20

sentenceSplit

boolean

否

是否按照句子切分：默认为 true

true

sentenceSplitSize

integer

否

按照句子切分的平均长度

160

size

integer

否

定长切分的 chunk 长度

256

split

boolean

否

是否切块

true

modelConfig

object

否

模型配置

temperature

double

否

温度

0.8

topP

double

否

topP

0.8

promptRoleStyle

string

否

prompt 角色风格

你是一位文档分析专家，非常善于从给定的知识中，找到重点，像老师给学生讲课一样把问题回答清晰。你的回答富有逻辑性，遇到复杂问题，你善于一步一步思考。

queryEnhancer

object

否

query 增强

enableFollowUp

boolean

否

多轮增强

true

enableMultiQuery

boolean

否

是否利用大模型知识拆解问题

true

enableOpenQa

boolean

否

是否利用大模型知识回答问题

true

enableQueryRewrite

boolean

否

是否根据领域知识改写问题

true

enableSession

boolean

否

记录 session

true

localKnowledgeId

string

否

知识改写使用的文档库 id

sjdhgfc

withDocumentReference

boolean

否

是否带文档引用

true

recallStrategy

object

否

召回策略

documentRankType

string

否

合并&排序策略

枚举值：

-   model：使用BGE进行排序。
-   llm：使用大模型进行排序。

model

limit

integer

否

两路合并总结的结果数

10

textIndexSetting

object

否

文本索引设置

category

string

否

文本索引类型

ElasticSearch

enable

boolean

否

文本索引是否开启

true

indexAnalyzer

string

否

文本索引的索引分析器: (Standard, IkMaxWord, IkSmart)

Standard

rankThreshold

double

否

文本索引排序阈值

0.5

searchAnalyzer

string

否

文本索引的搜索分析器: (Standard, IkMaxWord, IkSmart)

Standard

topK

integer

否

文本索引最后总结结果数

50

vectorIndexSetting

object

否

向量索引设置

category

string

否

向量索引来源：建议填写 ADB

ADB

embeddingType

string

否

向量索引文本 Embedding 模型

DashScope

enable

boolean

否

是否开启

true

rankThreshold

double

否

向量索引排序阈值

0.5

topK

integer

否

向量索引最后总结结果数

10

libraryId

string

是

文档库 id

dsfbashdbb

libraryName

string

否

文档库名称

测试文档库

## 返回参数

名称

类型

描述

示例值

object

ResultCode

cost

long

耗时

null

data

string

响应数据

null

dataType

string

数据类型

null

errCode

string

错误码

0

message

string

错误信息

ok

requestId

string

请求 id

eb2b6139-ddf1-91a0-a47f-df7617ae9032

success

boolean

是否成功

true

time

string

时间戳

2024-04-24 11:54:34

## 示例

正常返回示例

`JSON`格式

```
{
  "cost": 0,
  "data": null,
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "eb2b6139-ddf1-91a0-a47f-df7617ae9032",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
