# RunSearchGeneration - 妙搜-智能搜索

AI妙搜-智能搜索生成：对应妙搜首页的搜索生成能力。此接口支持通用搜索和媒资搜索。支持用户问题澄清、多模态知识搜索、多agent生成等能力。 - 通用搜索：可以对数据集中知识进行语义检索，并对搜索结果进行多agent后处理，包括总结生成、摘编、时间线总结等。 - 媒资搜索：应搜尽搜，全文检索，召回更多相关知识，并可进行多agent后处理，包括聚类、新闻抽取等。

## 接口说明

### 接入说明：

-   当前接口为 http-sse 协议。
    
-   由于 OpenAPI 门户目前对 SSE 推理协议不兼容（无法直接调试），接口 SDK 方式调用示例（支持**java、python**版本的 **sdk**）请参考[妙搜最佳实践](https://help.aliyun.com/zh/model-studio/user-guide/best-practices-for-miaosou-api/?spm=a2c4g.11186623.help-menu-2400256.d_1_3_3_2_1_2.42a64a34eIyBhn)文档。
    
-   其中获取 Java 异步 SDK 的最新版本：请点击[链接](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc)获取。
    

### 搜索数据来源：

支持三种类型数据集：详见[妙搜最佳实践](https://help.aliyun.com/zh/model-studio/user-guide/best-practices-for-miaosou-api/?spm=a2c4g.11186623.help-menu-2400256.d_1_3_3_2_1_2.42a64a34eIyBhn)

-   内置”互联网检索“数据集：支持互联网开放域文本、图片、视频（暂未开放）的搜索；
    
-   语义（RAG）数据集：可以管理企业私域知识库，支持文本、图片、视频、语音（暂未开放）；
    
-   三方 api 数据集：可以直接集成企业自己的搜索 api。
    

## 权限说明

### 前置条件

-   登录阿里云百炼控制台，确认阿里云百炼是开通可用状态。
    
-   主账号调用：默认有所有 API 调用权限。
    
-   子账号调用：子账号默认无权限（AccessForbid）调用当前 API，需要同时在 **RAM 控制台**和**阿里云百炼控制台**中做授权。
    

### RAM 控制台授权说明

去 [RAM 控制台](https://ram.console.aliyun.com/users)授权，具体 RAM 授权操作，参考 [RAM 文档](https://help.aliyun.com/zh/ram/user-guide/create-a-custom-policy)，步骤如下：

#### 授予内置权限策略

授予子账号” [AliyunAiMiaoBiFullAccess](https://ram.console.aliyun.com/policies/detail?policyType=System&policyName=AliyunAiMiaoBiFullAccess) “ 权限。

### 阿里云百炼控制台授权说明

使用主账号或有阿里云百炼管理员权限的子账号，登录阿里云百炼控制台，在[权限管理](https://bailian.console.aliyun.com/?tab=app#/authority)页面添加子账号“新增用户”。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunSearchGeneration)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunSearchGeneration)

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

aimiaobi:RunSearchGeneration

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaosou/runSearchGeneration HTTP/1.1
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

阿里云百炼业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。

llm-xxx

TaskId

string

否

会话任务唯一标识

**说明**

TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

7AA2AE16-D873-5C5F-9708-15396C382EB1

Prompt

string

否

搜索词

杭州亚运会吉祥物是什么

OriginalSessionId

string

否

原会话唯一标识：通常为空，非空时，表示当前对话基于此轮对话生成，会加载原始轮对话参数，搜索结果等，同时会替换生成结果，适用于，重新生成、修改数据源、新增 agent 生成场景

xxx

ChatConfig

object

否

会话配置信息

xxx

GenerateTechnology

string

否

生成技术：

-   copilotReference：问答式搜索
    
-   copilotPrecise：纯搜索
    

**枚举值：**

-   copilotPrecise :
    
    copilotPrecise
    
-   copilotReference :
    
    copilotReference
    

copilotReference

SearchParam

object

否

搜索参数

StartTime

integer

否

开始时间

1725983999999

EndTime

integer

否

结束时间

1725983999999

SearchSources

array<object>

否

搜索源列表

object

否

搜索源：

Code、DatasetName 两个字段必传，来唯一标识一个搜索源。

内置互联网搜索对应：

-   Code=SystemSearch
    
-   DatasetName=QuarkCommonNews
    

Code

string

否

搜索源类型：

-   SystemSearch：系统内置搜索
    
-   CustomSemanticSearch：自建语义索引搜索
    
-   ThirdSearch：三方 API 搜索
    

**枚举值：**

-   SystemSearch :
    
    SystemSearch
    
-   ThirdSearch :
    
    ThirdSearch
    
-   CustomSemanticSearch :
    
    CustomSemanticSearch
    

SystemSearch

DatasetName

string

否

搜索源唯一标识：对应页面数据集名称，比如 4cb0eda3fad841758262dbe8d61191

QuarkCommonNews

MultimodalSearchTypes

array

否

搜索范围列表

string

否

搜索范围：

-   text：文档
    
-   image：图片
    
-   audio：音频
    
-   video：视频
    

**枚举值：**

-   image :
    
    image
    
-   text :
    
    text
    
-   video :
    
    video
    

text

SearchTextMinScore

number

否

文本搜索阈值：仅自建数据源(0, 1)

0.66

SearchImageMinScore

number

否

图片搜索阈值：仅自建数据源(0, 1)

0.66

SearchVideoMinScore

number

否

视频搜索阈值：仅自建数据源(0, 1)

0.66

SearchAudioMinScore

number

否

语音搜索阈值：仅自建数据源(0, 1)

0.66

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

扩展字段 1

xxx

Extend2

string

否

扩展字段 2

xxx

Extend3

string

否

扩展字段 3

xxx

CreateTimeStart

integer

否

起始创建时间，时间戳形式。

111111111111

CreateTimeEnd

integer

否

截止创建时间，时间戳形式。

111111111111

DocIds

array

否

文档 ID 数组

string

否

文档 ID

x

DocUuids

array

否

文档唯一标识

string

否

文档唯一标识

x

SearchModels

array

否

搜索类型列表

string

否

搜索类型：

-   TextGenerate：总结生成答案（默认）
    
-   ExcerptGenerate：用原文语句回答
    
-   TimelineGenerate：按时间线总结
    
-   PreciseSearch：纯搜索（追问）
    
-   ClusterGenerate：聚类
    
-   ExtractNewsElementGenerate：抽取新闻要素
    

**枚举值：**

-   TextGenerate :
    
    TextGenerate
    
-   ExtractNewsElementGenerate :
    
    ExtractNewsElementGenerate
    
-   ClusterGenerate :
    
    ClusterGenerate
    
-   TimelineGenerate :
    
    TimelineGenerate
    
-   ExcerptGenerate :
    
    ExcerptGenerate
    

TextGenerate

GenerateLevel

string

否

回答的详细程度：

-   concise：简洁（默认）
    
-   enhance：增强
    
-   free：自由
    
-   deepResearch：研究
    

**枚举值：**

-   concise :
    
    concise
    
-   enhance :
    
    enhance
    

concise

EnableThinking

boolean

否

是否开启思考

false

ExcludeGenerateOptions

array

否

跳过的生成选项列表

string

否

跳过的生成选项

-   think(query 改写)
    
-   multimodalSearchThink（多模态搜索思考）
    
-   queryRecommend（query 推荐）
    

think

ModelCustomPromptTemplate

string

否

问答式搜索-总结生成答案-纯文本 prompt 模版，必须包含变量 query、content，比如：

```
# 角色
你是一个专业的文章检索和问答专家，擅长文章检索和回答用户问题。

# 任务目标
请你根据检索到的相关文章，回答或表述用户问题“{query}”。

# 任务限制
- 如果用户问题中提到具体日期，请考虑知识日期做筛选。
- 生成内容结构条理。
- 生成内容尽量精简。
- 不要使用其他数据，不要杜撰。
- 如果不能回答用户问题，请输出对应语言的拒识文案:
  - 中文："根据已知信息无法回答。"
  - 英文："Unable to answer based on the known information."

# 输入数据
## 检索到的相关文章
{content}
```

\# 角色 你是一个专业的文章检索和问答专家，擅长文章检索和回答用户问题。 # 任务目标 请你根据检索到的相关文章，回答或表述用户问题“{query}”。 # 任务限制 - 如果用户问题中提到具体日期，请考虑知识日期做筛选。 - 生成内容结构条理。 - 生成内容尽量精简。 - 不要使用其他数据，不要杜撰。 - 如果不能回答用户问题，请输出对应语言的拒识文案: - 中文："根据已知信息无法回答。" - 英文："Unable to answer based on the known information." # 输入数据 ## 检索到的相关文章 {content}

ModelCustomVlPromptTemplate

string

否

问答式搜索-总结生成答案-纯文本 prompt 模版，必须包含变量 query、content，比如：

```
# 角色
你是一个专业的文章检索和问答专家，擅长文章检索和回答用户问题。

# 任务目标
请你根据检索到的相关文章和图片，回答或表述用户问题“{query}”。

# 任务限制
- 如果用户问题中提到具体日期，请考虑知识日期做筛选。
- 生成内容结构条理。
- 生成内容尽量精简。
- 如果图片内容可以回答，可以忽略文章内容。
- 不要使用其他数据，不要杜撰。
- 如果不能回答用户问题，请输出对应语言的拒识文案:
    - 中文："根据已知信息无法回答。"
    - 英文："Unable to answer based on the known information."

# 输入数据
## 检索到的相关文章
{content}
```

\# 角色 你是一个专业的文章检索和问答专家，擅长文章检索和回答用户问题。 # 任务目标 请你根据检索到的相关文章和图片，回答或表述用户问题“{query}”。 # 任务限制 - 如果用户问题中提到具体日期，请考虑知识日期做筛选。 - 生成内容结构条理。 - 生成内容尽量精简。 - 如果图片内容可以回答，可以忽略文章内容。 - 不要使用其他数据，不要杜撰。 - 如果不能回答用户问题，请输出对应语言的拒识文案: - 中文："根据已知信息无法回答。" - 英文："Unable to answer based on the known information." # 输入数据 ## 检索到的相关文章 {content}

AgentContext

object

否

上下文

BizContext

object

否

业务上下文

MultimodalMediaSelection

object

否

用户输入或选中的多模态数据

SelectionType

string

否

参照数据来源类型，取值范围： ‒ 全量的：all，历史会话中取全量数据，仅支持聚类场景； ‒ 选中的：selected，生成时，会取 textSearchResult 中数据；

all

SessionId

string

否

生成参照会话唯一标识：搜索生成时当前对话下取数据，比如聚类，目前仅媒资搜索场景-聚类需要

3f7045e099474ba28ceca1b4eb6d6e21

OriginalSessionId

string

否

原始会话唯一标识：搜索结果取这个会话中的全量，目前仅媒资搜索场景需要

原始会话唯一标识：搜索结果取这个会话中的全量，目前仅媒资搜索场景需要

SearchModel

string

否

仅聚类，对聚类子类内容二次聚类时传入，ClusterGenerate

TextGenerate

SearchModelDataValue

string

否

searchModel=ClusterGenerate 时，取子类 topic 名称，注意如果原值有引号时也要带上

分类1

TextSearchResult

object

否

文本搜索结果

SearchResult

array<object>

否

文本搜索结果列表

object

否

文本搜索结果

SearchSourceType

string

否

搜索信源类型，同 searchSource.code

SystemSearch

SearchSource

string

否

搜索信源唯一标识，同 searchSource.datasetName

QuarkCommonNews

SearchSourceName

string

否

搜索信源名称

互联网搜索

PubTime

string

否

发布时间

2024-11-25 14:25:59

Source

string

否

来源

新华社

Title

string

否

标题

文章标题

Content

string

否

内容

文章内容

Url

string

否

文章 URL

https://www.example.com/aaa.docx

Summary

string

否

文章摘要

文章摘要

DocUuid

string

否

内部文档唯一标识

xxx

Score

number

否

相关度

1

Chunks

array

否

相关 chunk

string

否

片段

xx

DocId

string

否

文档-自定义的唯一 ID

文档-自定义的唯一ID

SkipCurrentSupplement

boolean

否

是否跳过反问

false

AskUser

string

否

反问

您想了解关于xx的哪些信息？

AskUserKeywords

array

否

反问推荐关键词列表

string

否

反问推荐关键词

xx

UserBack

string

否

反问用户反馈

地点

UserBackKeywords

array

否

反问用户反馈关键词列表

string

否

反问用户反馈关键词

xx

CurrentStep

string

否

当前步骤

think

NextStep

string

否

下一步

generate

SupplementDataType

string

否

思考-需要补充的数据类型：searchQuery

searchQuery

SupplementEnable

boolean

否

思考-是否需要补充

true

ModelId

string

否

模型 id：

-   quanmiao-max：全妙-Max
    
-   quanmiao-plus：全妙-Plus
    

quanmiao-max

FileUrl

string

否

图片 url：适用于图搜、图文（prompt）混合搜索生成等场景

http://xxxx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Payload

object

响应体

Output

object

输出

AgentContext

object

上下文数据

BizContext

object

业务上下文

CurrentStep

string

任务当前操作步数。

start

NextStep

string

下一步:think、search、generat

search

GeneratedContent

object

生成内容

ClusterTopicResult

object

聚类结果

ClusterTopics

array<object>

聚类列表

array<object>

聚类

Topic

string

主题

xx

ImageSearchResult

object

图片搜索结果

SearchResult

array<object>

搜索结果列表

array<object>

搜索结果

Article

object

文章

SearchSourceName

string

搜索信源名称

互联网搜索

Title

string

标题

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

DocUuid

string

内部文档唯一标识

xx

DocId

string

文档-自定义的唯一 ID

xx

CategoryUuid

string

类目唯一标识

xx

Tags

array

标签。

string

标签。

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

SearchSourceType

string

数据集类型

xx

SearchSource

string

数据集唯一标识

xx

MediaId

string

多模态数据唯一标识

xx

FileUrl

string

文件 url

xx

Current

integer

当前页码

1

Size

integer

每页记录数

1

Total

integer

总记录数

1

TextSearchResult

object

文档搜索结果

SearchResult

array<object>

搜索结果列表

array<object>

搜索结果

SearchSourceType

string

搜索信源类型，同 searchSource.code

SystemSearch

SearchSource

string

搜索信源唯一标识，同 searchSource.datasetName

QuarkCommonNews

SearchSourceName

string

搜索信源名称

互联网搜索

PubTime

string

发布时间,格式：yyyy-MM-dd HH:mm:ss

2023-04-04 08:39:09

Title

string

标题

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

DocUuid

string

内部文档唯一标识

xx

DocId

string

文档-自定义的唯一 ID

xx

MultimodalMedias

array<object>

多模态信息列表

object

多模态信息

MediaId

string

多模态数据唯一标识

xx

MediaType

string

多模态数据文件类型，取值：

-   video：视频。
    
-   image：图片。
    

image

FileUrl

string

文件 url

xx

CategoryUuid

string

类目唯一标识

xx

Tags

array

标签

string

标签

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

Current

integer

当前页码

1

Size

integer

每页记录数

1

Total

integer

总数

1

VideoSearchResult

object

视频搜索结果

SearchResult

array<object>

搜索结果

array<object>

搜索结果

Article

object

文章

SearchSourceName

string

搜索信源名称

互联网搜索

Title

string

标题

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

DocUuid

string

内部文档唯一标识

xx

DocId

string

文档-自定义的唯一 ID

xx

CategoryUuid

string

类目

xx

Tags

array

标签

string

标签

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

x

SearchSourceType

string

数据集类型

xx

SearchSource

string

数据集唯一标识

xx

MediaId

string

多模态数据唯一标识

xx

ClipInfos

array<object>

匹配信息列表

object

匹配信息

Score

number

参考置信度

0.9

From

number

开始时间

1

To

number

结束时间

1

Text

string

对应文本，比如 asr 转写结果

xx

Type

string

文本类型：比如 asr

asr

FileUrl

string

文件 url

xx

Current

integer

当前页码

1

Size

integer

每页记录数

1

Total

integer

总记录数

1

AudioSearchResult

object

语音结果

SearchResult

object

语音结果

FileUrl

string

url

http://xx

MediaId

string

id

xxx

ClipInfos

array<object>

匹配信息列表

object

匹配信息

Score

number

阈值

1

From

number

开始位置

1

To

number

结束位置

1

Text

string

文本内容

xx

Type

string

类型

asr

Article

object

对应文档

Title

string

标题

xx

Url

string

url

http://xx

Summary

string

摘要

xx

DocUuid

string

docUuid

xx

DocId

string

docId

xx

SearchSourceName

string

搜索源

xx

CategoryUuid

string

类目唯一标识

xx

Tags

array

标签名称

string

标签值。

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

SearchSourceType

string

数据集类型

xx

SearchSource

string

数据集唯一标识

xx

Current

integer

当前页

1

Size

integer

大小

1

Total

integer

总数

1

TextGenerate

string

文本结果

xx

GenerateFinished

boolean

当前 agent 是否生成完成

true

ExcerptResult

object

原文语句回答结果

TextGenerate

string

生成文本

xx

SearchResult

array<object>

搜索结果列表

array<object>

搜索结果

TraceabilityId

integer

溯源定位 id

1

SearchSourceType

string

搜索信源类型，同 searchSource.code

SystemSearch

SearchSource

string

搜索信源唯一标识，同 searchSource.datasetName

QuarkCommonNews

SearchSourceName

string

搜索信源名称

互联网搜索

PubTime

string

发布时间,格式：yyyy-MM-dd HH:mm:ss

2023-04-04 08:39:09

Title

string

标题

xx

Content

string

正文

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

Excerpt

string

原文语句回答内容

xx

Select

boolean

是否参照

true

DocUuid

string

内部文档唯一标识

xx

Score

number

置信度，仅供参考

0.99

Chunks

array

片段列表

string

片段

xx

DocId

string

文档-自定义的唯一 ID

xx

TextGenerateMultimodalMediaList

array<object>

配图列表

array<object>

配图

Start

integer

开始位置

1

End

integer

结束位置

1

DocUuid

string

内部文档唯一标识

xx

MultimodalMediaList

array<object>

多模态数据列表

array<object>

多模态数据

Article

object

文章

DocId

string

文档-自定义的唯一 ID

xx

DocUuid

string

内部文档唯一标识

xx

SearchSourceName

string

搜索信源名称

互联网搜索

Title

string

标题

xx

Url

string

文章 URL

xx

MediaId

string

多模态数据唯一标识

xx

MediaType

string

多模态数据文件类型，取值： video：视频。 image：图片。

image

FileUrl

string

文件 url

xx

MultimodalMedias

array<object>

多模态信息列表

object

多模态信息

MediaId

string

多模态数据唯一标识

xx

MediaType

string

多模态数据文件类型，取值：

-   video：视频。
    
-   image：图片。
    

image

FileUrl

string

文件 URL。

xx

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

标签名称

string

标签名称

xx

GenerateFinished

boolean

当前 agent 是否生成完成

true

GenerateLevel

string

回答的详细程度：

-   concise：简洁（默认）
    
-   enhance：增强
    

concise

ReasonTextGenerate

string

深度思考内容

xx

NewsElementResult

object

新闻抽取结果

TextGenerate

string

文本生成内容

x

NewsElementArticleList

array<object>

新闻抽取列表

array<object>

新闻抽取

TextGenerate

string

文本生成内容

xx

Article

object

文章

SearchSourceType

string

搜索信源类型，同 searchSource.code

SystemSearch

SearchSource

string

搜索信源唯一标识，同 searchSource.datasetName

QuarkCommonNews

SearchSourceName

string

搜索信源名称

互联网搜索

PubTime

string

发布时间,格式：yyyy-MM-dd HH:mm:ss

2023-04-04 08:39:09

Title

string

标题

xx

Content

string

正文

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

Select

boolean

是否参照

true

DocUuid

string

内部文档唯一标识

xx

Score

number

置信度，仅供参考

0.99

DocId

string

文档-自定义的唯一 ID

xx

CategoryUuid

string

类目唯一标识

xx

Tags

array

标签名称

string

标签名称

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

NewsElementList

array<object>

新闻列表

array<object>

新闻

Time

string

时间

时间

Location

string

地点

xx

People

string

人物

xx

Event

object

事件

task-started

CauseList

array

原因列表

string

原因

xx

ProcessList

array

经过列表

string

经过

xx

ResultList

array

结果列表

string

结果

xx

GenerateFinished

boolean

当前 agent 是否生成完成

true

TextGenerateResult

object

总结生成答案

TextGenerate

string

文本生成结果

xx

TextGenerateMultimodalMediaList

array<object>

配图列表

array<object>

配图

Start

integer

开始位置

1

End

integer

结束位置

1

MultimodalMediaList

array<object>

多模态数据列表

array<object>

多模态数据

Article

object

文章

SearchSourceName

string

搜索源名称

xx

Title

string

标题

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

DocUuid

string

内部文档唯一标识

xx

DocId

string

文档-自定义的唯一 ID

xx

MediaId

string

媒资 ID。

xx

MediaType

string

多模态数据文件类型，取值： video：视频。 image：图片。

image

FileUrl

string

文件 url

xx

ReferenceList

array<object>

参考文章列表

object

参考文章

TraceabilityId

integer

溯源定位 id

1

SearchSourceType

string

搜索信源类型，同 searchSource.code

SystemSearch

SearchSource

string

搜索信源唯一标识，同 searchSource.datasetName

QuarkCommonNews

SearchSourceName

string

搜索信源名称

互联网搜索

PubTime

string

发布时间，格式：yyyy-MM-dd HH:mm:ss

2023-04-04 08:39:09

Source

string

来源

新华社

Title

string

标题

xx

Content

string

正文

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

Select

boolean

是否参照

true

DocUuid

string

内部文档唯一标识

xx

Score

number

置信度，仅供参考

0.99

Chunks

array

片段列表

string

片段

xx

DocId

string

文档-自定义的唯一 ID

xx

CategoryUuid

string

类目唯一标识

xx

Tags

array

标签名称

string

标签名称

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

MultimodalSearchResultList

array<object>

多模态搜索结果列表

array<object>

多模态搜索结果

SearchResult

array<object>

搜索结果列表

array<object>

搜索结果

Article

object

文章

SearchSourceName

string

搜索源名称

xx

Title

string

标题

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

DocUuid

string

内部文档唯一标识

xx

DocId

string

文档-自定义的唯一 ID

xx

MediaId

string

媒资 ID。

xx

MediaType

string

多模态数据文件类型，取值： video：视频。 image：图片。

image

ClipInfos

array<object>

匹配信息列表

object

匹配信息

Score

number

置信度，仅供参考

0.1

From

number

开始时间

1

To

number

结束时间

1

Text

string

对应文本，比如 asr 转写结果

xx

Type

string

类型：比如 asr

asr

FileUrl

string

文件 url

xx

TimelineDateStr

string

时间脉络-时间

时间脉络-时间

Current

integer

当前页

1

Size

integer

每页条数

1

Total

integer

总条数

1

SearchType

string

搜索类型

realtime

SearchQuery

string

搜索 query

xx

GenerateTraceability

object

溯源信息

Duplicate

number

综合溯源相关度

0.9

Coordinates

array<object>

溯源位置列表

array<object>

溯源位置

GenerateCoordinate

object

生成文档块的坐标

X

integer

编号：1 开始

1

Y

integer

开始位置

1

Z

integer

结束位置

1

NewsCoordinate

object

参考文档块的坐标

X

integer

编号：1 开始

1

Y

integer

开始位置

1

Z

integer

结束位置

1

MediaType

string

媒资类型

image

GenerateFinished

boolean

当前 agent 是否生成完成

true

GenerateLevel

string

回答的详细程度：

-   concise：简洁（默认）
    
-   enhance：增强
    

concise

ReasonTextGenerate

string

深度思考内容

xx

TimelineResult

object

按时间总结结果

TextGenerate

string

文本生成结果

xx

ReferenceList

array<object>

参考文章列表

object

参考文章

TraceabilityId

integer

溯源定位 id

1

SearchSourceType

string

搜索信源类型，同 searchSource.code

SystemSearch

SearchSource

string

搜索信源唯一标识，同 searchSource.datasetName

QuarkCommonNews

SearchSourceName

string

搜索信源名称

互联网搜索

PubTime

string

发布时间，格式：yyyy-MM-dd HH:mm:ss

2023-04-04 08:39:09

Source

string

来源

新华社

Title

string

标题

xx

Content

string

正文

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

Select

boolean

选择情况

true

DocUuid

string

内部文档唯一标识

xx

Score

number

置信度，仅供参考

0.99

Chunks

array

片段列表

string

片段

xx

DocId

string

文档-自定义的唯一 ID

xx

CategoryUuid

string

类目唯一标识

xx

Tags

array

标签名称

string

标签名称

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

MultimodalSearchResultList

array<object>

多模态搜索结果列表

array<object>

多模态搜索结果

SearchResult

array<object>

搜索结果列表

array<object>

搜索结果

Article

object

文章

SearchSourceName

string

搜索信源名称

互联网搜索

Title

string

标题

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

DocUuid

string

内部文档唯一标识

xx

DocId

string

文档-自定义的唯一 ID

xx

MediaId

string

多模态数据唯一标识

xx

MediaType

string

多模态数据文件类型，取值： video：视频。 image：图片。

image

ClipInfos

array<object>

匹配信息列表

object

匹配信息

Score

number

置信度，仅供参考

0.99

From

number

开始时间

1

To

number

结束时间

1

Text

string

对应文本，比如 asr 转写结果

xx

Type

string

类型：比如 asr

asr

FileUrl

string

文件 URL。

xx

TimelineDateStr

string

时间字符串

2024-09-11

GenerateTraceability

object

溯源信息

Duplicate

number

相关度

0.9

Coordinates

array<object>

溯源位置

array<object>

溯源位置

GenerateCoordinate

object

生成文档块的坐标

X

integer

编号：1 开始

1

Y

integer

开始位置

1

Z

integer

结束位置

1

NewsCoordinate

object

参照文章的坐标

X

integer

编号：1 开始

1

Y

integer

开始位置

1

Z

integer

结束位置

1

MediaType

string

媒资类型

image

TextGenerateMultimodalMediaList

array<object>

配图列表

array<object>

配图

Start

integer

开始位置

1

End

integer

结束位置

1

MultimodalMediaList

array<object>

多模态数据列表

array<object>

多模态数据

Article

object

文章

SearchSourceName

string

搜索信源名称

互联网搜索

Title

string

标题

xxxx

Url

string

文章 URL

xx

Summary

string

摘要

xx

DocUuid

string

内部文档唯一标识

xx

DocId

string

文档-自定义的唯一 ID

xx

MediaId

string

多模态数据唯一标识

xx

MediaType

string

多模态数据文件类型，取值： video：视频。 image：图片。

image

FileUrl

string

文件 url

xx

GenerateFinished

boolean

当前 agent 是否生成完成

true

ReasonTextGenerate

string

深度思考内容

xx

VideoSearchResult

object

视频搜索结果

SearchResult

array<object>

搜索结果列表

array<object>

搜索结果

Article

object

文章

SearchSourceName

string

搜索信源名称

互联网搜索

Title

string

标题

xx

Url

string

文章 URL

xx

Summary

string

摘要

xx

DocUuid

string

内部文档唯一标识

xx

DocId

string

文档-自定义的唯一 ID

xx

CategoryUuid

string

类目唯一标识

xx

Tags

array

标签。

string

标签

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

MediaId

string

多模态数据唯一标识

xx

ClipInfos

array<object>

匹配信息列表

object

匹配信息

Score

number

参考置信度

0.8

From

number

片段起始时间。

1

To

number

结束时间

1

Text

string

对应文本，比如 asr 转写结果

xx

Type

string

类型：比如 asr

asr

FileUrl

string

文件 url

xx

TraceabilityId

string

溯源唯一标识

1

ImageSearchResult

object

图片搜索结果

SearchResult

array<object>

搜索结果列表

array<object>

搜索结果

Article

object

文章

SearchSourceName

string

搜索信源名称

互联网搜索

Title

string

标题

xx

Url

string

文章 URL

xx

Summary

string

文章摘要

xx

DocUuid

string

内部文档唯一标识

xx

DocId

string

文档-自定义的唯一 ID

xx

CategoryUuid

string

类目唯一标识

xx

Tags

array

标签名称

string

标签名称

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

MediaId

string

媒体数据唯一标识

xx

FileUrl

string

文件 url

xx

TraceabilityId

string

溯源唯一标识

1

TextSearchResult

object

文本文档搜索结果

Current

integer

当前页

1

Size

integer

当前页大小

1

Total

integer

总条数

1

SearchResult

array<object>

搜素结构

object

搜索结果

DocId

string

文档业务唯一标识

xx

DocUuid

string

系统内部文档唯一标识

xx

SearchSourceType

string

数据源类型

SystemSearch

SearchSource

string

数据源唯一标识

QuarkCommonNews

SearchSourceName

string

数据源描述

xxx

PubTime

string

发布时间

2024-11-25 14:25:59

Content

string

正文

xx

Url

string

url

xx

Title

string

标题

xx

Summary

string

摘要

xx

TraceabilityId

string

溯源唯一标识

1

CategoryUuid

string

类目唯一标识

xx

Tags

array

标签名称

string

标签名称

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

AudioSearchResult

object

语音结果

SearchResult

array<object>

语音结果

array<object>

语音结果

MediaId

string

id

xxx

FileUrl

string

url

http://xxx

Article

object

归属文档

Title

string

标题

xx

Url

string

url

http://xxx

Summary

string

摘要

xxx

DocUuid

string

uuid

xx

DocId

string

id

xx

SearchSourceName

string

搜索源

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

标签列表

string

标签值。

x

CategoryUuid

string

类目唯一标识

xx

ClipInfos

array<object>

匹配列表

object

匹配信息

Score

number

阈值

0.9

From

number

开始位置

1

To

number

结束位置

2

Text

string

文本内容

xx

Type

string

文本类型

asr

TraceabilityId

string

溯源唯一标识

1

SearchKeywords

array

思考-query 理解关键词列表

string

思考-query 理解关键词

xx

SearchQueryList

array

文本搜索 query 列表

string

文本搜索 query

xx

RecommendSearchQueryList

array

生成-推荐列表

string

生成-推荐

xx

SupplementDataType

string

思考-需要补充的数据类型：searchQuery

searchQuery

SupplementEnable

boolean

思考-是否需要补充

true

ModelId

string

模型 id

xx

TokenCalculate

object

运行统计信息

FirstTokenTime

number

首 TOKEN 时间

1

SearchTime

number

搜索耗时

1

OutputAvgTime

number

每秒平均输出的 token 数量

1

Time

number

总耗时

1

TotalTokens

integer

总 token 数

1

AskUser

string

反问

您想了解关于xx的哪些信息？

AskUserKeywords

array

反问推荐关键词列表

string

反问推荐关键词

时间

Messages

array<object>

研究模式消息列表

array<object>

研究模式消息

Id

string

节点 id

xx

Content

string

生成文本

xx

GenerateFinished

boolean

当前节点是否完成

Clarifications

boolean

是否需要澄清

SearchQueries

array

搜索 query 列表

string

搜索 query

xx

SearchResult

array<object>

搜索结果

array<object>

搜索结果

MultimodalSearchQuery

string

多模态搜索 query

xx

Texts

array<object>

文本搜索列表

object

文本搜索

DocUuid

string

id

xx

Images

array<object>

图片搜索列表

object

图片搜索

MediaId

string

id

xx

Audios

array<object>

音频结果列表

object

音频结果

MediaId

string

id

xx

Videos

array<object>

视频结果列表

object

视频结果

MediaId

string

id

1

NodeCode

string

节点 code:

-   generateStartStatement
    
-   generateSearchQueries
    
-   multiSearch
    
-   readSearchResult
    
-   reflection
    
-   generate
    

generateStartStatement

SearchQuery

string

当前节点搜索 query

xx

Usage

object

token 用量

OutputTokens

integer

输出 Token 数量

2

InputTokens

integer

输入 Token 数量

1

TotalTokens

integer

总 oken 数量

3

Header

object

响应头

SessionId

string

对话 ID

x

TraceId

string

全链路 ID

xx

TaskId

string

任务 ID

x

OriginSessionId

string

源会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

Event

string

SSE 事件。

task-failed

ErrorCode

string

错误码

AccessForbid

ErrorMessage

string

异常错误信息

xx

EventInfo

string

事件描述

xx

ResponseTime

integer

响应时间，单位为毫秒（ms）。

1

RequestId

string

请求唯一标识

xx

## 示例

正常返回示例

`JSON`格式

```
{
  "Payload": {
    "Output": {
      "AgentContext": {
        "BizContext": {
          "CurrentStep": "start",
          "NextStep": "search",
          "GeneratedContent": {
            "ClusterTopicResult": {
              "ClusterTopics": [
                {
                  "Topic": "xx",
                  "ImageSearchResult": {
                    "SearchResult": [
                      {
                        "Article": {
                          "SearchSourceName": "互联网搜索",
                          "Title": "xx",
                          "Url": "xx",
                          "Summary": "xx",
                          "DocUuid": "xx",
                          "DocId": "xx",
                          "CategoryUuid": "xx",
                          "Tags": [
                            "xx"
                          ],
                          "Extend1": "xx",
                          "Extend2": "xx",
                          "Extend3": "xx",
                          "SearchSourceType": "xx",
                          "SearchSource": "xx"
                        },
                        "MediaId": "xx",
                        "FileUrl": "xx"
                      }
                    ],
                    "Current": 1,
                    "Size": 1,
                    "Total": 1
                  },
                  "TextSearchResult": {
                    "SearchResult": [
                      {
                        "SearchSourceType": "SystemSearch",
                        "SearchSource": "QuarkCommonNews",
                        "SearchSourceName": "互联网搜索",
                        "PubTime": "2023-04-04 08:39:09",
                        "Title": "xx",
                        "Url": "xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx",
                        "MultimodalMedias": [
                          {
                            "MediaId": "xx",
                            "MediaType": "image",
                            "FileUrl": "xx"
                          }
                        ],
                        "CategoryUuid": "xx",
                        "Tags": [
                          "xx"
                        ],
                        "Extend1": "xx",
                        "Extend2": "xx",
                        "Extend3": "xx"
                      }
                    ],
                    "Current": 1,
                    "Size": 1,
                    "Total": 1
                  },
                  "VideoSearchResult": {
                    "SearchResult": [
                      {
                        "Article": {
                          "SearchSourceName": "互联网搜索",
                          "Title": "xx",
                          "Url": "xx",
                          "Summary": "xx",
                          "DocUuid": "xx",
                          "DocId": "xx",
                          "CategoryUuid": "xx",
                          "Tags": [
                            "xx"
                          ],
                          "Extend1": "xx",
                          "Extend2": "xx",
                          "Extend3": "x",
                          "SearchSourceType": "xx",
                          "SearchSource": "xx"
                        },
                        "MediaId": "xx",
                        "ClipInfos": [
                          {
                            "Score": 0.9,
                            "From": 1,
                            "To": 1,
                            "Text": "xx",
                            "Type": "asr"
                          }
                        ],
                        "FileUrl": "xx"
                      }
                    ],
                    "Current": 1,
                    "Size": 1,
                    "Total": 1
                  },
                  "AudioSearchResult": {
                    "SearchResult": {
                      "FileUrl": "http://xx",
                      "MediaId": "xxx",
                      "ClipInfos": [
                        {
                          "Score": 1,
                          "From": 1,
                          "To": 1,
                          "Text": "xx",
                          "Type": "asr"
                        }
                      ],
                      "Article": {
                        "Title": "xx",
                        "Url": "http://xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx",
                        "SearchSourceName": "xx",
                        "CategoryUuid": "xx",
                        "Tags": [
                          "xx"
                        ],
                        "Extend1": "xx",
                        "Extend2": "xx",
                        "Extend3": "xx",
                        "SearchSourceType": "xx",
                        "SearchSource": "xx"
                      }
                    },
                    "Current": 1,
                    "Size": 1,
                    "Total": 1
                  }
                }
              ],
              "TextGenerate": "xx",
              "GenerateFinished": true
            },
            "ExcerptResult": {
              "TextGenerate": "xx",
              "SearchResult": [
                {
                  "TraceabilityId": 1,
                  "SearchSourceType": "SystemSearch",
                  "SearchSource": "QuarkCommonNews",
                  "SearchSourceName": "互联网搜索",
                  "PubTime": "2023-04-04 08:39:09",
                  "Title": "xx",
                  "Content": "xx",
                  "Url": "xx",
                  "Summary": "xx",
                  "Excerpt": "xx",
                  "Select": true,
                  "DocUuid": "xx",
                  "Score": 0.99,
                  "Chunks": [
                    "xx"
                  ],
                  "DocId": "xx",
                  "TextGenerateMultimodalMediaList": [
                    {
                      "Start": 1,
                      "End": 1,
                      "DocUuid": "xx",
                      "MultimodalMediaList": [
                        {
                          "Article": {
                            "DocId": "xx",
                            "DocUuid": "xx",
                            "SearchSourceName": "互联网搜索",
                            "Title": "xx",
                            "Url": "xx"
                          },
                          "MediaId": "xx",
                          "MediaType": "image",
                          "FileUrl": "xx"
                        }
                      ]
                    }
                  ],
                  "MultimodalMedias": [
                    {
                      "MediaId": "xx",
                      "MediaType": "image",
                      "FileUrl": "xx"
                    }
                  ],
                  "CategoryUuid": "xx",
                  "Extend1": "xx",
                  "Extend2": "xx",
                  "Extend3": "xx",
                  "Tags": [
                    "xx"
                  ]
                }
              ],
              "GenerateFinished": true,
              "GenerateLevel": "concise",
              "ReasonTextGenerate": "xx"
            },
            "NewsElementResult": {
              "TextGenerate": "x",
              "NewsElementArticleList": [
                {
                  "TextGenerate": "xx",
                  "Article": {
                    "SearchSourceType": "SystemSearch",
                    "SearchSource": "QuarkCommonNews",
                    "SearchSourceName": "互联网搜索",
                    "PubTime": "2023-04-04 08:39:09",
                    "Title": "xx",
                    "Content": "xx",
                    "Url": "xx",
                    "Summary": "xx",
                    "Select": true,
                    "DocUuid": "xx",
                    "Score": 0.99,
                    "DocId": "xx",
                    "CategoryUuid": "xx",
                    "Tags": [
                      "xx"
                    ],
                    "Extend1": "xx",
                    "Extend2": "xx",
                    "Extend3": "xx"
                  },
                  "NewsElementList": [
                    {
                      "Time": "时间",
                      "Location": "xx",
                      "People": "xx",
                      "Event": {
                        "CauseList": [
                          "xx"
                        ],
                        "ProcessList": [
                          "xx"
                        ],
                        "ResultList": [
                          "xx"
                        ]
                      }
                    }
                  ]
                }
              ],
              "GenerateFinished": true
            },
            "TextGenerateResult": {
              "TextGenerate": "xx",
              "TextGenerateMultimodalMediaList": [
                {
                  "Start": 1,
                  "End": 1,
                  "MultimodalMediaList": [
                    {
                      "Article": {
                        "SearchSourceName": "xx",
                        "Title": "xx",
                        "Url": "xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx"
                      },
                      "MediaId": "xx",
                      "MediaType": "image",
                      "FileUrl": "xx"
                    }
                  ]
                }
              ],
              "ReferenceList": [
                {
                  "TraceabilityId": 1,
                  "SearchSourceType": "SystemSearch",
                  "SearchSource": "QuarkCommonNews",
                  "SearchSourceName": "互联网搜索",
                  "PubTime": "2023-04-04 08:39:09",
                  "Source": "新华社",
                  "Title": "xx",
                  "Content": "xx",
                  "Url": "xx",
                  "Summary": "xx",
                  "Select": true,
                  "DocUuid": "xx",
                  "Score": 0.99,
                  "Chunks": [
                    "xx"
                  ],
                  "DocId": "xx",
                  "CategoryUuid": "xx",
                  "Tags": [
                    "xx"
                  ],
                  "Extend1": "xx",
                  "Extend2": "xx",
                  "Extend3": "xx"
                }
              ],
              "MultimodalSearchResultList": [
                {
                  "SearchResult": [
                    {
                      "Article": {
                        "SearchSourceName": "xx",
                        "Title": "xx",
                        "Url": "xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx"
                      },
                      "MediaId": "xx",
                      "MediaType": "image",
                      "ClipInfos": [
                        {
                          "Score": 0.1,
                          "From": 1,
                          "To": 1,
                          "Text": "xx",
                          "Type": "asr"
                        }
                      ],
                      "FileUrl": "xx"
                    }
                  ],
                  "TimelineDateStr": "时间脉络-时间",
                  "Current": 1,
                  "Size": 1,
                  "Total": 1,
                  "SearchType": "realtime",
                  "SearchQuery": "xx"
                }
              ],
              "GenerateTraceability": {
                "Duplicate": 0.9,
                "Coordinates": [
                  {
                    "GenerateCoordinate": {
                      "X": 1,
                      "Y": 1,
                      "Z": 1
                    },
                    "NewsCoordinate": {
                      "X": 1,
                      "Y": 1,
                      "Z": 1,
                      "MediaType": "image"
                    }
                  }
                ]
              },
              "GenerateFinished": true,
              "GenerateLevel": "concise",
              "ReasonTextGenerate": "xx"
            },
            "TimelineResult": {
              "TextGenerate": "xx",
              "ReferenceList": [
                {
                  "TraceabilityId": 1,
                  "SearchSourceType": "SystemSearch",
                  "SearchSource": "QuarkCommonNews",
                  "SearchSourceName": "互联网搜索",
                  "PubTime": "2023-04-04 08:39:09",
                  "Source": "新华社",
                  "Title": "xx",
                  "Content": "xx",
                  "Url": "xx",
                  "Summary": "xx",
                  "Select": true,
                  "DocUuid": "xx",
                  "Score": 0.99,
                  "Chunks": [
                    "xx"
                  ],
                  "DocId": "xx",
                  "CategoryUuid": "xx",
                  "Tags": [
                    "xx"
                  ],
                  "Extend1": "xx",
                  "Extend2": "xx",
                  "Extend3": "xx"
                }
              ],
              "MultimodalSearchResultList": [
                {
                  "SearchResult": [
                    {
                      "Article": {
                        "SearchSourceName": "互联网搜索",
                        "Title": "xx",
                        "Url": "xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx"
                      },
                      "MediaId": "xx",
                      "MediaType": "image",
                      "ClipInfos": [
                        {
                          "Score": 0.99,
                          "From": 1,
                          "To": 1,
                          "Text": "xx",
                          "Type": "asr"
                        }
                      ],
                      "FileUrl": "xx"
                    }
                  ],
                  "TimelineDateStr": "2024-09-11"
                }
              ],
              "GenerateTraceability": {
                "Duplicate": 0.9,
                "Coordinates": [
                  {
                    "GenerateCoordinate": {
                      "X": 1,
                      "Y": 1,
                      "Z": 1
                    },
                    "NewsCoordinate": {
                      "X": 1,
                      "Y": 1,
                      "Z": 1,
                      "MediaType": "image"
                    }
                  }
                ]
              },
              "TextGenerateMultimodalMediaList": [
                {
                  "Start": 1,
                  "End": 1,
                  "MultimodalMediaList": [
                    {
                      "Article": {
                        "SearchSourceName": "互联网搜索",
                        "Title": "xxxx",
                        "Url": "xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx"
                      },
                      "MediaId": "xx",
                      "MediaType": "image",
                      "FileUrl": "xx"
                    }
                  ]
                }
              ],
              "GenerateFinished": true,
              "ReasonTextGenerate": "xx"
            },
            "VideoSearchResult": {
              "SearchResult": [
                {
                  "Article": {
                    "SearchSourceName": "互联网搜索",
                    "Title": "xx",
                    "Url": "xx",
                    "Summary": "xx",
                    "DocUuid": "xx",
                    "DocId": "xx",
                    "CategoryUuid": "xx",
                    "Tags": [
                      "xx"
                    ],
                    "Extend1": "xx",
                    "Extend2": "xx",
                    "Extend3": "xx"
                  },
                  "MediaId": "xx",
                  "ClipInfos": [
                    {
                      "Score": 0.8,
                      "From": 1,
                      "To": 1,
                      "Text": "xx",
                      "Type": "asr"
                    }
                  ],
                  "FileUrl": "xx",
                  "TraceabilityId": "1"
                }
              ]
            },
            "ImageSearchResult": {
              "SearchResult": [
                {
                  "Article": {
                    "SearchSourceName": "互联网搜索",
                    "Title": "xx",
                    "Url": "xx",
                    "Summary": "xx",
                    "DocUuid": "xx",
                    "DocId": "xx",
                    "CategoryUuid": "xx",
                    "Tags": [
                      "xx"
                    ],
                    "Extend1": "xx",
                    "Extend2": "xx",
                    "Extend3": "xx"
                  },
                  "MediaId": "xx",
                  "FileUrl": "xx",
                  "TraceabilityId": "1"
                }
              ]
            },
            "TextSearchResult": {
              "Current": 1,
              "Size": 1,
              "Total": 1,
              "SearchResult": [
                {
                  "DocId": "xx",
                  "DocUuid": "xx",
                  "SearchSourceType": "SystemSearch",
                  "SearchSource": "QuarkCommonNews",
                  "SearchSourceName": "xxx",
                  "PubTime": "2024-11-25 14:25:59",
                  "Content": "xx",
                  "Url": "xx",
                  "Title": "xx",
                  "Summary": "xx",
                  "TraceabilityId": "1",
                  "CategoryUuid": "xx",
                  "Tags": [
                    "xx"
                  ],
                  "Extend1": "xx",
                  "Extend2": "xx",
                  "Extend3": "xx"
                }
              ]
            },
            "AudioSearchResult": {
              "SearchResult": [
                {
                  "MediaId": "xxx",
                  "FileUrl": "http://xxx",
                  "Article": {
                    "Title": "xx",
                    "Url": "http://xxx",
                    "Summary": "xxx",
                    "DocUuid": "xx",
                    "DocId": "xx",
                    "SearchSourceName": "xx",
                    "Extend1": "xx",
                    "Extend2": "xx",
                    "Extend3": "xx",
                    "Tags": [
                      "x"
                    ],
                    "CategoryUuid": "xx"
                  },
                  "ClipInfos": [
                    {
                      "Score": 0.9,
                      "From": 1,
                      "To": 2,
                      "Text": "xx",
                      "Type": "asr"
                    }
                  ],
                  "TraceabilityId": "1"
                }
              ]
            }
          },
          "SearchKeywords": [
            "xx"
          ],
          "SearchQueryList": [
            "xx"
          ],
          "RecommendSearchQueryList": [
            "xx"
          ],
          "SupplementDataType": "searchQuery",
          "SupplementEnable": true,
          "ModelId": "xx",
          "TokenCalculate": {
            "FirstTokenTime": 1,
            "SearchTime": 1,
            "OutputAvgTime": 1,
            "Time": 1,
            "TotalTokens": 1
          },
          "AskUser": "您想了解关于xx的哪些信息？",
          "AskUserKeywords": [
            "时间"
          ]
        }
      },
      "Messages": [
        {
          "Id": "xx",
          "Content": "xx",
          "GenerateFinished": true,
          "Clarifications": true,
          "SearchQueries": [
            "xx"
          ],
          "SearchResult": [
            {
              "MultimodalSearchQuery": "xx",
              "Texts": [
                {
                  "DocUuid": "xx"
                }
              ],
              "Images": [
                {
                  "MediaId": "xx"
                }
              ],
              "Audios": [
                {
                  "MediaId": "xx"
                }
              ],
              "Videos": [
                {
                  "MediaId": "1"
                }
              ]
            }
          ],
          "NodeCode": "generateStartStatement",
          "SearchQuery": "xx"
        }
      ]
    },
    "Usage": {
      "OutputTokens": 2,
      "InputTokens": 1,
      "TotalTokens": 3
    }
  },
  "Header": {
    "SessionId": "x",
    "TraceId": "xx",
    "TaskId": "x",
    "OriginSessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "Event": "task-failed",
    "ErrorCode": "AccessForbid",
    "ErrorMessage": "xx",
    "EventInfo": "xx",
    "ResponseTime": 1
  },
  "RequestId": "xx"
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunSearchGeneration#workbench-doc-change-demo)。
