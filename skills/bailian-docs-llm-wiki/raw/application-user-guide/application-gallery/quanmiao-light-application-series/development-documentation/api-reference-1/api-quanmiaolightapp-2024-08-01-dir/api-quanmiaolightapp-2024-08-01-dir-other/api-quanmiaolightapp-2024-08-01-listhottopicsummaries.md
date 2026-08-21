# ListHotTopicSummaries - 查询完整播报单（热榜）

阿里云百炼-轻应用-车机/内容平台新闻热榜互动-查询完整播报单（热榜）：通过这个接口可以获取播报单所有内容。

## 接口说明

通过这个接口可以获取“完整播报单（热榜）”下所有内容，包括频道、热点、热度、播报摘要等，默认获取当前最近版本的播报单，通过制定版本可以获取指定时间段系统版本或自定义版本的播报单内容。

建议走最新的[**GetHotTopicBroadcast**](https://help.aliyun.com/zh/model-studio/user-guide/api-aimiaobi-2023-08-01-gethottopicbroadcast?spm=a2c4g.11186623.help-menu-2400256.d_1_3_3_2_0_3_11_2.773720a2vwX3bA&scm=20140722.H_2857057._.OR_help-T_cn~zh-V_1)接口：出入参更完善。

欢迎前往[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)体验。

通过 SDK 方式调用 API 可参考控制台“API”页签下的 java、python 示例。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/ListHotTopicSummaries)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/ListHotTopicSummaries)

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

quanmiaolightapp:ListHotTopicSummaries

list

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/listHotTopicSummaries HTTP/1.1
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

百炼业务空间唯一标识，百炼首页左上角获取

llm-xxx

category

string

否

分类

xx

hotTopic

string

否

热点话题

xx

hotTopicVersion

string

否

热点话题版本

2024-09-13\_12

nextToken

string

否

下一页的 token

JlroP3CjgQh5PQDlH3ArzADkBTPZgVqo+64jhZRglNq0mEYoV5SlGb/Juvo8CdfYE9rlwEr2pIJQwdaYotak9g==

maxResults

integer

否

每页返回最大数量。

**说明** 默认 100，最大 1000。

20

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

code

string

状态码

xx

data

array<object>

热点信息列表

data

object

热点信息

category

string

热点话题分类

财经

hotTopic

string

热点话题名称

xx

hotTopicVersion

string

热点话题摘要版本

2024-09-13\_12

hotValue

double

热度

1000000

id

string

热点话题 ID

db5dc5b3d8954a30b65ba700c9dda3bb

news

array<object>

文章列表

news

object

文章

comments

array<object>

结构化摘要列表

comments

object

结构化摘要

text

string

内容

xx

content

string

正文

xx

pubTime

string

发布时间

2024-09-10 15:32:00

title

string

标题

xx

url

string

url

http://xxx

summary

object

热点话题结构化摘要

summaries

array<object>

结构化摘要列表

summaries

object

结构化摘要

summary

string

摘要

xx

title

string

标题

xx

textSummary

string

热点话题文本摘要

xx

httpStatusCode

integer

http 状态码

200

maxResults

integer

最大返回结果数

20

message

string

错误说明

success

nextToken

string

下一页的 token

JlroP3CjgQh5PQDlH3ArzADkBTPZgVqo+64jhZRglNq0mEYoV5SlGb/Juvo8CdfYE9rlwEr2pIJQwdaYotak9g==

requestId

string

请求唯一标识

117F5ABE-CF02-5502-9A3F-E56BC9081A64

success

boolean

是否成功：true 成功，false 失败

True

totalCount

integer

总数

200

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "xx",
  "data": [
    {
      "category": "财经",
      "hotTopic": "xx",
      "hotTopicVersion": "2024-09-13_12",
      "hotValue": 1000000,
      "id": "db5dc5b3d8954a30b65ba700c9dda3bb",
      "news": [
        {
          "comments": [
            {
              "text": "xx"
            }
          ],
          "content": "xx",
          "pubTime": "2024-09-10 15:32:00",
          "title": "xx",
          "url": "http://xxx"
        }
      ],
      "summary": {
        "summaries": [
          {
            "summary": "xx",
            "title": "xx"
          }
        ]
      },
      "textSummary": "xx"
    }
  ],
  "httpStatusCode": 200,
  "maxResults": 20,
  "message": "success",
  "nextToken": "JlroP3CjgQh5PQDlH3ArzADkBTPZgVqo+64jhZRglNq0mEYoV5SlGb/Juvo8CdfYE9rlwEr2pIJQwdaYotak9g==",
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64",
  "success": true,
  "totalCount": 200
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
