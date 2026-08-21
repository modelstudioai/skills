# RunHotTopicChat - 播报单（热榜）问答

阿里云百炼轻应用-车机/内容平台新闻热榜互动-播报单（热榜）问答：可以对播报单、新闻、开放域内容问答。

## 接口说明

## [](#当前接口-runhottopicchat-说明)当前接口 RunHotTopicChat 说明

通过此接口，可以对播报单（热榜）、热榜新闻、开放域内容做问答，包括频道推荐、热点推荐、热点内容问答等。

欢迎前往[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)体验。

**通过 SDK 方式调用 API，请可参考[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)“API”页签下的 java、python 示例！**

**通过 SDK 方式调用 API，请可参考[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)“API”页签下的 java、python 示例！**

**通过 SDK 方式调用 API，请可参考[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)“API”页签下的 java、python 示例！**

## [](#新闻热榜互动全量-api-说明)新闻热榜互动全量 API 说明

### [](#api-明细)API 明细

#### [](#ai-妙笔-sdk-下对应-alibabacloud-aimiaobi20230801)AI 妙笔 SDK 下：对应 alibabacloud-aimiaobi20230801

-   [**GetHotTopicBroadcast**](https://help.aliyun.com/zh/model-studio/user-guide/api-aimiaobi-2023-08-01-gethottopicbroadcast?spm=a2c4g.11186623.help-menu-search-2400256.d_0) - **查询完整播报单（热榜）** --常用
-   [SubmitCustomHotTopicBroadcastJob](https://help.aliyun.com/zh/model-studio/user-guide/api-aimiaobi-2023-08-01-submitcustomhottopicbroadcastjob?spm=a2c4g.11186623.help-menu-2400256.d_1_3_3_2_0_3_11_1.6e8226ccRBFaYz) - 提交自定义播报单任务
-   [GetCustomHotTopicBroadcastJob](https://help.aliyun.com/zh/model-studio/user-guide/api-aimiaobi-2023-08-01-getcustomhottopicbroadcastjob?spm=a2c4g.11186623.help-menu-2400256.d_1_3_3_2_0_3_11_0.fd006c4cdnYwwj) - 获取自定义播报单任务结果

#### [](#阿里云百炼全妙轻应用-sdk-下对应-alibabacloud-quanmiaolightapp20240801)阿里云百炼全妙轻应用 SDK 下：对应 alibabacloud-quanmiaolightapp20240801

-   **RunHotTopicChat** - **播报单（热榜）问答** --常用
-   [RunHotTopicSummary](https://help.aliyun.com/zh/model-studio/user-guide/api-quanmiaolightapp-2024-08-01-runhottopicsummary?spm=a2c4g.11186623.help-menu-2400256.d_1_3_4_3_1_3_4_1.420a7c48CBWA8o) - 播报单热点自定义摘要生成

### [](#场景说明)场景说明

#### [](#场景-1获取完整播报单热榜全量或者部分频道热点)场景 1：获取完整播报单（热榜）全量或者部分频道热点：

-   GetHotTopicBroadcast：查询播报单

#### [](#场景-2针对播报单或通用领域问题做问答)场景 2：针对播报单或通用领域问题做问答：

-   RunHotTopicChat：问答

#### [](#场景-3内置播报单热榜不满足要求需要个性化定制频道个性化摘要等)场景 3：内置播报单（热榜）不满足要求，需要个性化定制（频道、个性化摘要等）：

-   SubmitCustomHotTopicBroadcastJob：提交自定义播报单任务
-   GetCustomHotTopicBroadcastJob：轮训自定义播报单任务状态
-   GetHotTopicBroadcast：获取自定义播报单信息

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunHotTopicChat)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunHotTopicChat)

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

quanmiaolightapp:RunHotTopicChat

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runHotTopicChat HTTP/1.1
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

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

modelId

string

否

数据模型 ID。默认：qwen-max-latest

qwen-max-latest

modelCustomPromptTemplate

string

否

prompt 模版

xx

generateOptions

array

否

生成模式列表：默认 textChatGenerate

string

否

生成模式：summaryChatGenerate、newsChatGenerate 和控制台第三步两个选项对应，可以直接使用，其他场景可以按需要组合：

-   能力组合：内置好的，原子能力+搜索源的组合
    -   summaryChatGenerate：对应轻应用控制台“仅针对聚合新闻播报单内已包含的信息进行回答”，包括 categoryRecommend, hotTopicSummarySearch, textChatGenerate
    -   newsChatGenerate：对应轻应用控制台“允许针对新闻的原始素材和互联网开放域进行搜索后回答“，包括 hotTopicNewsSearch, internetSearch, textChatGenerate
-   原子能力：
    -   categoryRecommend：频道热点推荐，比如“推荐下体育新闻”
    -   textChatGenerate：问答，仅次选项时，必须明确指定源 internetSearch、hotTopicSummarySearch、hotTopicNewsSearch，比如“xxx 事件哪天发生的”
    -   queryRecommend：开启 query 推荐，单独结构返回
-   搜索源：
    -   hotTopicSummarySearch：热榜摘要搜索源
    -   hotTopicNewsSearch：热榜新闻详情搜索源
    -   internetSearch：互联网通用领域搜索源

newsChatGenerate

taskId

string

否

对话任务唯一标识：多轮时，这个值保持不变

a3d1c2ac-f086-4a21-9069-f5631542f5a2

originalSessionId

string

否

原始会话唯一标识：重试场景

a3d1c2ac-f086-4a21-9069-f5631542f5ax

prompt

string

否

用户问题

帮我播报体育热点

hotTopicVersion

string

否

热榜版本

2024-09-13\_12

category

string

否

热榜频道

体育

hotTopics

array

否

热点名称列表

string

否

热点标题名称

xxx

imageCount

integer

否

配图张数：不一定都有图，取值\[1-3\]

1

stepForBroadcastContentConfig

object

否

新闻播报内容配置：仅 Saas 用，Paas 调用建议走 hotTopicVersion

categories

array

否

选择的频道列表

string

否

频道

体育

customHotValueWeights

array<object>

否

热度计算维度，不传，则走默认

object

否

热度计算维度列表

dimension

string

否

权重维度唯一标识：

-   views("阅读量")
-   comments("发表观点量")
-   ups("点赞数")
-   downs("点踩数")
-   publishTime("发布时间")

comments

weight

integer

否

权重，0-10 之间

1

topicCount

integer

否

话题数量

20

messages

array<object>

否

上下文

object

否

角色：user、assistant、system

role

string

否

内容

user

content

string

否

发生时间

xxx

createTime

string

否

时间

2024-12-10 18:51:29

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

header

object

消息头

errorCode

string

错误码 code

InvalidParam

errorMessage

string

错误描述

xx

event

string

事件

task-finished

eventInfo

string

事件描述信息

xx

sessionId

string

会话唯一标识

xxx

taskId

string

任务唯一标识

d3be9981-ca2d-4e17-bf31-1c0a628e9f99

traceId

string

全链路唯一标识

2150451a17191950923411783e2927

payload

object

消息体

output

object

输出结果

articles

array<object>

参照内容列表

articles

object

内容列表

content

string

正文

xxx

pubTime

string

发布时间

2024-09-22 16:45:06

score

double

相关度

0.8

searchSourceName

string

文章来源名称

互联网

select

boolean

是否参照

true

summary

string

摘要

xx

title

string

标题

test

url

string

链接

http://xxx

hotTopicSummaries

array<object>

热点列表

hotTopicSummaries

object

热点

customHotValue

double

自定义热度值

100000

hotTopic

string

热点话题名称

xx

hotTopicVersion

string

热点话题摘要版本

2024-09-13\_08

hotValue

double

热度值

100000

textSummary

string

热点话题文本摘要

xxx

customTextSummary

string

自定义热点话题文本摘要

xxx

news

array<object>

新闻列表

news

object

新闻

title

string

标题

xxx

url

string

url

http://xxx

images

array<object>

图片列表

images

object

图片

url

string

图片

http://www.example.com/xxx.png

url

string

热点话题的 URL

http://www.example.com/xxx.html

pubTime

string

热点话题发布时间

2025-05-20 12:00:00

multimodalMedias

array<object>

配图

multimodalMedias

object

配图

fileUrl

string

链接

http://xxxx

mediaType

string

类型：

-   image：图片

image

sortScore

double

相关度

0.8

recommendQueries

array

推荐 query 列表

recommendQueries

string

推荐 query

关于xx你有什么看法？

searchQuery

string

改写后 query

xxx

text

string

生成正文：答案等

xx

category

string

新闻播报场景的领域识别（时政、社会、国际等频道识别）

国际

keyword

string

新闻播报场景的关键字识别

AI

location

string

新闻播报场景的地点名识别

杭州

usage

object

token 消耗

inputTokens

long

输入 token

100

outputTokens

long

输出 token

100

totalTokens

long

总 token

200

requestId

string

请求唯一标识

04DA1A52-4E51-56CB-BA64-FDDA0B53BAE8

## 示例

正常返回示例

`JSON`格式

```
{
  "header": {
    "errorCode": "InvalidParam",
    "errorMessage": "xx",
    "event": "task-finished",
    "eventInfo": "xx",
    "sessionId": "xxx",
    "taskId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99",
    "traceId": "2150451a17191950923411783e2927"
  },
  "payload": {
    "output": {
      "articles": [
        {
          "content": "xxx",
          "pubTime": "2024-09-22 16:45:06",
          "score": 0.8,
          "searchSourceName": "互联网",
          "select": true,
          "summary": "xx",
          "title": "test",
          "url": "http://xxx"
        }
      ],
      "hotTopicSummaries": [
        {
          "customHotValue": 100000,
          "hotTopic": "xx",
          "hotTopicVersion": "2024-09-13_08",
          "hotValue": 100000,
          "textSummary": "xxx",
          "customTextSummary": "xxx",
          "news": [
            {
              "title": "xxx",
              "url": "http://xxx"
            }
          ],
          "images": [
            {
              "url": "http://www.example.com/xxx.png"
            }
          ],
          "url": "http://www.example.com/xxx.html",
          "pubTime": "2025-05-20 12:00:00"
        }
      ],
      "multimodalMedias": [
        {
          "fileUrl": "http://xxxx",
          "mediaType": "image",
          "sortScore": 0.8
        }
      ],
      "recommendQueries": [
        "关于xx你有什么看法？"
      ],
      "searchQuery": "xxx",
      "text": "xx",
      "category": "国际",
      "keyword": "AI",
      "location": "杭州"
    },
    "usage": {
      "inputTokens": 100,
      "outputTokens": 100,
      "totalTokens": 200
    }
  },
  "requestId": "04DA1A52-4E51-56CB-BA64-FDDA0B53BAE8"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
