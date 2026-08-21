# GetTopicSelectionPerspectiveAnalysisTask - 获取选题视角分析任务结果

获取选题视角分析任务结果。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetTopicSelectionPerspectiveAnalysisTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetTopicSelectionPerspectiveAnalysisTask)

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

aimiaobi:GetTopicSelectionPerspectiveAnalysisTask

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

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

xxxxx\_p\_efm

TaskId

string

否

任务唯一 ID

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

c9f226b02cca4f42a84c5e955c39dfd2

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

ErrorMessage

string

错误信息

错误信息

FreshViewPointsResult

object

新颖选题视角分析结果

Attitudes

array<object>

新颖选题视角-观点列表

Attitude

object

Attitude

string

当前观点

当前观点

AttitudeType

string

观点类型

观点类型

Ratio

string

当前观点占比

当前观点占比

ViewPoints

array<object>

选题视角列表

ViewPoint

object

Outlines

array<object>

大纲

Outline

object

大纲列表

Outline

string

大纲

大纲

Summary

string

大纲摘要

大纲摘要

Point

string

生成的视角

视角

Summary

string

摘要

摘要

HotViewPointsResult

object

热门选题视角分析结果

Attitudes

array<object>

热门选题视角-观点列表

Attitude

object

热门选题视角-观点列表

Attitude

string

当前观点

当前观点

AttitudeType

string

观点类型

观点类型

News

array<object>

相关新闻列表

New

object

新闻对象

Content

string

新闻内容

Content

DocId

string

文档-自定义的唯一 ID

9957175DEDCF49C5ACF7A956B4FD67B2

DocUuid

string

文章唯一 ID

"123456"

ImageUrls

array

文章配图 URL

ImageUrl

string

文章图片外链

https://www.example.com/aaa.png

Source

string

新闻来源

夸克

Summary

string

新闻摘要

新闻摘要

Tags

array

标签

Tag

string

文章标签

\["标签1","标签2"\]

Title

string

新闻标题

新闻标题

Topic

string

文章主题

文章主题

Url

string

URL 链接

http://www.example.com

CreateTime

string

创建时间

2024-05-08 02:23:01

PubTime

string

发布时间

2024-05-08 02:23:02

Ratio

string

当前观点占比

当前观点占比

ViewPoints

array<object>

选题视角列表

ViewPoint

object

Outlines

array<object>

大纲

Outline

object

大纲对象

Outline

string

大纲

大纲

Summary

string

大纲摘要

大纲摘要

Point

string

生成的视角

视角

Summary

string

摘要

摘要

Status

string

任务状态（PENDING：待执行, RUNNING：执行中, SUCCESSED：成功, SUSPENDED：暂停, FAILED：失败, CANCELED：取消）

SUSPENDED

TimedViewPointsResult

object

时效性选题视角分析结果

Attitudes

array<object>

时效性选题视角-观点列表

Attitude

object

观点对象

Attitude

string

当前观点

当前观点

AttitudeType

string

观点类型

观点类型

PubTime

string

发布时间

2024-01-22 10:29

Ratio

string

当前观点占比

当前观点占比

Source

string

新闻来源

新浪

Title

string

当前观点，等价于新闻标题

标题

Url

string

新闻 URL

http://www.example.com/news/1.html

ViewPoints

array<object>

选题视角列表

ViewPoint

object

视角对象

Outlines

array<object>

大纲

Outline

object

大纲对象

Outline

string

大纲

大纲

Summary

string

大纲摘要

大纲摘要

Point

string

生成的视角

视角

Summary

string

摘要

摘要

Topic

string

热点主题事件

热点主题事件

TopicSummaryResult

object

热点主题事件摘要

Summaries

array<object>

摘要列表

Summarie

object

摘要对象

DocList

array<object>

生成该标题摘要引用的文章

DocList

object

文章对象

Source

string

文章源

头条

Title

string

文章标题

标题

Url

string

文章 URL

http://www.example.com

Summary

string

摘要

摘要

Title

string

标题

标题

WebReviewPointsResult

object

网评选题视角分析结果

Attitudes

array<object>

网友选题视角-观点列表

Attitude

object

Attitude

string

当前观点

当前观点

AttitudeType

string

观点类型

观点类型

Comments

array<object>

网友观点列表

Comment

object

对象

Source

string

来源

来源

Text

string

内容

内容

Title

string

标题

标题

Url

string

当前所属的 URL

当前所属的URL

Username

string

用户名

用户名

Ratio

string

当前观点占比

当前观点占比

ViewPoints

array<object>

选题视角列表

ViewPoint

object

Outlines

array<object>

大纲

Outline

object

大纲对象

Outline

string

大纲

大纲

Summary

string

大纲摘要

大纲摘要

Point

string

生成的视角

视角

Summary

string

摘要

摘要

HttpStatusCode

integer

http 状态码

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
    "ErrorMessage": "错误信息",
    "FreshViewPointsResult": {
      "Attitudes": [
        {
          "Attitude": "当前观点",
          "AttitudeType": "观点类型",
          "Ratio": "当前观点占比",
          "ViewPoints": [
            {
              "Outlines": [
                {
                  "Outline": "大纲",
                  "Summary": "大纲摘要"
                }
              ],
              "Point": "视角",
              "Summary": "摘要"
            }
          ]
        }
      ]
    },
    "HotViewPointsResult": {
      "Attitudes": [
        {
          "Attitude": "当前观点",
          "AttitudeType": "观点类型",
          "News": [
            {
              "Content": "Content",
              "DocId": "9957175DEDCF49C5ACF7A956B4FD67B2",
              "DocUuid": 123456,
              "ImageUrls": [
                "https://www.example.com/aaa.png"
              ],
              "Source": "夸克",
              "Summary": "新闻摘要",
              "Tags": [
                [
                  "标签1",
                  "标签2"
                ]
              ],
              "Title": "新闻标题",
              "Topic": "文章主题",
              "Url": "http://www.example.com",
              "CreateTime": "2024-05-08 02:23:01",
              "PubTime": "2024-05-08 02:23:02"
            }
          ],
          "Ratio": "当前观点占比",
          "ViewPoints": [
            {
              "Outlines": [
                {
                  "Outline": "大纲",
                  "Summary": "大纲摘要"
                }
              ],
              "Point": "视角",
              "Summary": "摘要"
            }
          ]
        }
      ]
    },
    "Status": "SUSPENDED",
    "TimedViewPointsResult": {
      "Attitudes": [
        {
          "Attitude": "当前观点",
          "AttitudeType": "观点类型",
          "PubTime": "2024-01-22 10:29",
          "Ratio": "当前观点占比",
          "Source": "新浪",
          "Title": "标题",
          "Url": "http://www.example.com/news/1.html",
          "ViewPoints": [
            {
              "Outlines": [
                {
                  "Outline": "大纲",
                  "Summary": "大纲摘要"
                }
              ],
              "Point": "视角",
              "Summary": "摘要"
            }
          ]
        }
      ]
    },
    "Topic": "热点主题事件",
    "TopicSummaryResult": {
      "Summaries": [
        {
          "DocList": [
            {
              "Source": "头条",
              "Title": "标题",
              "Url": "http://www.example.com"
            }
          ],
          "Summary": "摘要",
          "Title": "标题"
        }
      ]
    },
    "WebReviewPointsResult": {
      "Attitudes": [
        {
          "Attitude": "当前观点",
          "AttitudeType": "观点类型",
          "Comments": [
            {
              "Source": "来源",
              "Text": "内容",
              "Title": "标题",
              "Url": "当前所属的URL",
              "Username": "用户名"
            }
          ],
          "Ratio": "当前观点占比",
          "ViewPoints": [
            {
              "Outlines": [
                {
                  "Outline": "大纲",
                  "Summary": "大纲摘要"
                }
              ],
              "Point": "视角",
              "Summary": "摘要"
            }
          ]
        }
      ]
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
