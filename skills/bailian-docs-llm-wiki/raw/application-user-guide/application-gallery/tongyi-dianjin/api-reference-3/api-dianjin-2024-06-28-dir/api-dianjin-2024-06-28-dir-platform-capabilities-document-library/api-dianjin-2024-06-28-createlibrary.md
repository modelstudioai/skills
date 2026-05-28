# CreateLibrary - 创建文档库

创建文档库。创建一个新的文档库，文档库用作隔离文档信息、索引信息，如果使用场景中需要经常按类别去做自然语言检索，建议创建多个文档库，来隔离不同类型的数据。支持按照格式自定义向量索引和文本索引。

## 接口说明

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
    
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/CreateLibrary)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/CreateLibrary)

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

dianjin:CreateLibrary

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/library/create HTTP/1.1
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

llm-ik\*\*\*\*\*\*RVYCKzt

body

object

否

请求体。

description

string

是

文档库的描述

描述文档库的具体作用

indexSetting

object

否

文档库的索引设置

chunkStrategy

object

否

分段策略

docTreeSplit

boolean

否

版面切分

true

docTreeSplitSize

integer

否

版面切分大小

300

enhanceGraph

boolean

否

是否解析文档中的图片内容

true

enhanceTable

boolean

否

是否解析文档中的表格内容

true

overlap

integer

否

chunk 重叠长度

20

sentenceSplit

boolean

否

按句子切分

true

sentenceSplitSize

integer

否

按句子切分大小

300

size

integer

否

chunk 大小

300

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

用于控制模型回复的随机性和多样性。具体来说，temperature 值控制了生成文本时对每个候选词的概率分布进行平滑的程度。较高的 temperature 值会降低概率分布的峰值，使得更多的低概率词被选择，生成结果更加多样化；而较低的 temperature 值则会增强概率分布的峰值，使得高概率词更容易被选择，生成结果更加确定。

取值范围： \[0, 2)，不建议取值为 0，无意义。

0.8

topP

double

否

生成过程中的核采样方法概率阈值，例如，取值为 0.8 时，仅保留概率加起来大于等于 0.8 的最可能 token 的最小集合作为候选集。取值范围为（0,1.0)，取值越大，生成的随机性越高；取值越低，生成的确定性越高。

0.8

promptRoleStyle

string

否

prompt 风格角色。通过指定角色，描述语气风格，来控制最终回答质量。如：文档分析专家、温柔的客服、专业的金融行业分析师。

你是一位信息处理专家，耐心、友好、逻辑清晰。

queryEnhancer

object

否

问题增强配置

enableFollowUp

boolean

否

是否根据历史记录改写问题

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

是否使用问题改写

true

enableSession

boolean

否

是否开启多轮对话

true

localKnowledgeId

string

否

知识改写使用的文档库 id

xxxx

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

-   linear：linear。
-   model：model。

model

limit

integer

否

两路合并总结的结果数

20

textIndexSetting

object

否

文本索引配置

category

string

否

文本索引类型，目前只支持 ElasticSearch。

ElasticSearch

enable

boolean

否

是否启用文本索引。

枚举值：

-   true：true。
-   false：false。

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

向量索引来源：目前只支持 ADB

ADB

embeddingType

string

否

向量索引文本 Embedding 类型

枚举值：

-   DashScope：DashScope。

DashScope

enable

boolean

否

是否开启

枚举值：

-   true：true。
-   false：false。

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

50

libraryName

string

是

文档库的名称

金融知识文档库

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

300

data

string

返回数据

a1b2c3

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

成功

requestId

string

请求 id

xxxx-xxxx-xxxx-xxxx

success

boolean

是否成功

true

time

string

时间戳

null

## 示例

正常返回示例

`JSON`格式

```
{
  "cost": 300,
  "data": "a1b2c3",
  "dataType": null,
  "errCode": 0,
  "message": "成功",
  "requestId": "xxxx-xxxx-xxxx-xxxx",
  "success": true,
  "time": null
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
