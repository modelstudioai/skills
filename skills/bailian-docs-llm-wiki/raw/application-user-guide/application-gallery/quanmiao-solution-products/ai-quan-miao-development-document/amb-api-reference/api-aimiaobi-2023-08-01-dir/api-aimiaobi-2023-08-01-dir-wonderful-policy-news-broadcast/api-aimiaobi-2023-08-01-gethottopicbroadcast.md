# GetHotTopicBroadcast - 查询完整播报单（热榜）

查询新闻播报单。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetHotTopicBroadcast)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetHotTopicBroadcast)

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

aimiaobi:GetHotTopicBroadcast

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

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

HotTopicVersion

string

否

热点版本

2024-10-11\_13

Topics

array

否

话题筛选

Topic

string

否

热点主题

\["主题1","主题2"\]

CalcTotalToken

boolean

否

是否计算总 Token 数

false

Category

string

否

分类筛选

分类筛选

StepForNewsBroadcastContentConfig

object

否

热点播报单内容配置

Categories

array

否

选择的频道列表

Categorie

string

否

频道

\["科技","经济","时政","娱乐"\]

CustomHotValueWeights`deprecated`

array<object>

否

自定义热度权重

CustomHotValueWeight

object

否

自定义权重

Dimension

string

否

维度 KEY

views

Weight

integer

否

权重

1

TopicCount

integer

否

话题数量

10

StepForCustomSummaryStyleConfig

object

否

自定义输出风格配置

SummaryImageCount

integer

否

摘要-配图数量

90

SummaryModel

string

否

摘要模型

摘要模型

SummaryPrompt

string

否

摘要-自定义 Prompt

摘要-自定义Prompt

Size

integer

否

每页大小

5

Current

integer

否

当前页码

1

Locations

array

否

新闻地域检索列表（keyword 过滤）

string

否

新闻地域检索（keyword 过滤）

重庆

LocationQuery

string

否

热点地域的全文检索（该参数存在时 current 不生效）

重庆 成都 浙江 杭州

Query

string

否

全文检索（针对标题、热点摘要、地域的全文检索）（该参数存在时 current 不生效）

重庆新闻

## 返回参数

名称

类型

描述

示例值

object

PlainResult

Code

string

状态码

NoData

Data

object

业务数据

Data

array<object>

热点播报单列表信息

Data

object

热点信息

Category

string

热点话题分类

热点话题分类

CreateTime

string

创建时间

创建时间

CustomHotValue

double

自定义热度值

34.7905341705522

CustomTextSummary

string

自定义热点话题文本摘要

自定义热点话题文本摘要

HotTopic

string

热点话题名称

热点话题名称

HotTopicVersion

string

热点话题摘要版本

热点话题摘要版本

HotValue

double

热度值

1.4120480606282884

Id

string

热点话题 ID

热点话题ID

Images

array<object>

热点话题图片列表

Image

object

图片对象

Url

string

URL 链接

http://www.example.com/a.png

InputToken

integer

输入 Token

29

News

array<object>

文章列表

New

object

新闻对象

AnalysisCategory

string

模型分类结果

科技

AnalysisTopic

string

聚合后热点名称

聚合后热点名称

Author

string

作者

作者

Category

array

分类

Category

string

分类

科技

Comments

array<object>

新闻内容

Comment

object

对象

Text

string

内容

内容

Username

string

用户名

用户名

Content

string

新闻内容

新闻内容

CreateTime

string

入库时间

2024-06-13 08:45:05

Domain

string

来源

夸克

Dt

string

入库日期

2024111110

HotTopic

string

原始热点名称

原始热点名称

ImgList

array

图片列表

ImgList

string

图片 URL

http://www.example.com/a.png

Logo

string

logo

https://www.example.com/a.png

PubTime

string

发布时间

2024-10-10 12:12:00

Summary

string

摘要

摘要

Title

string

标题

标题

Url

string

新闻 URL

http://www.example.com/a.png

Uuid

string

主键 ID

主键ID

Website

string

网站

网站

OutputToken

integer

输出 Token

22

Summary

object

热点话题结构化摘要

InputToken

integer

生成此摘要的输入 Token 数

17

OutputToken

integer

生成此摘要的输出 Token 数

41

Summaries

array<object>

结构化摘要列表

Summarie

object

结构化摘要

Summary

string

摘要

摘要

Title

string

标题

标题

TextSummary

string

热点话题文本摘要

热点话题文本摘要

Locations

array

热点的地域信息列表

locations

string

热点的地域信息

成都

Url

string

热榜 URL

http://www.example.com/a.html

PubTime

string

发布时间

2025-08-01 12:00:00

TotalCount

integer

总数

100

TotalTokenInfo

object

全部生成预计所需要的 Token 数

HotTopicCount

integer

热点总数

100

InputTokens

integer

预计输入 Token 数

100

OutputTokens

integer

预计输出 Token 数

100

WordCount

integer

预计总字数

100

HttpStatusCode

integer

HTTP 状态码

200

Message

string

错误说明

success

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Data": {
    "Data": [
      {
        "Category": "热点话题分类",
        "CreateTime": "创建时间",
        "CustomHotValue": 34.7905341705522,
        "CustomTextSummary": "自定义热点话题文本摘要",
        "HotTopic": "热点话题名称",
        "HotTopicVersion": "热点话题摘要版本",
        "HotValue": 1.4120480606282884,
        "Id": "热点话题ID",
        "Images": [
          {
            "Url": "http://www.example.com/a.png"
          }
        ],
        "InputToken": 29,
        "News": [
          {
            "AnalysisCategory": "科技",
            "AnalysisTopic": "聚合后热点名称",
            "Author": "作者",
            "Category": [
              "科技"
            ],
            "Comments": [
              {
                "Text": "内容",
                "Username": "用户名"
              }
            ],
            "Content": "新闻内容\n\n",
            "CreateTime": "2024-06-13 08:45:05",
            "Domain": "夸克",
            "Dt": 2024111110,
            "HotTopic": "原始热点名称",
            "ImgList": [
              "http://www.example.com/a.png"
            ],
            "Logo": "https://www.example.com/a.png",
            "PubTime": "2024-10-10 12:12:00",
            "Summary": "摘要",
            "Title": "标题",
            "Url": "http://www.example.com/a.png",
            "Uuid": "主键ID",
            "Website": "网站"
          }
        ],
        "OutputToken": 22,
        "Summary": {
          "InputToken": 17,
          "OutputToken": 41,
          "Summaries": [
            {
              "Summary": "摘要",
              "Title": "标题"
            }
          ]
        },
        "TextSummary": "热点话题文本摘要",
        "Locations": [
          "成都"
        ],
        "Url": "http://www.example.com/a.html",
        "PubTime": "2025-08-01 12:00:00"
      }
    ],
    "TotalCount": 100,
    "TotalTokenInfo": {
      "HotTopicCount": 100,
      "InputTokens": 100,
      "OutputTokens": 100,
      "WordCount": 100
    }
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
